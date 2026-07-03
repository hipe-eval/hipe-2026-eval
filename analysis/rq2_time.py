#!/usr/bin/env python3
"""RQ2: does document period affect top5-ensemble accuracy? Domain A and Domain B are
different periods and genres and are never pooled.

Fixed bin edges (approved in ANALYSIS_PLAN.md §10, not derived at runtime):
  Domain A (impresso, observed year range 1800-1998): 10-year windows, 1800-2000.
  Domain B (surprise, observed year range 1542-1797): 50-year windows, 1500-1800
  (left at 50-year width — 30 documents over 255 years would leave most 10-year
  bins near-empty; see ANALYSIS_PLAN.md §10 for the bin-population counts behind
  this choice).

Reads analysis.d/tables/pair_level_features.parquet (read-only). Writes:
  analysis.d/tables/rq2_time_bins_domainA.tsv
  analysis.d/tables/rq2_time_bins_domainB.tsv
  analysis.d/tables/rq2_time_correlation.tsv   (Spearman sanity check, not a regression)
  analysis.d/figures/rq2_time.pdf (+ .png)

Every bin on the fixed grid is kept in the output tables, including empty ones
(n_pairs=0, macro_recall left null) — they used to be silently dropped, which made
the line plot draw a straight line across a gap in the timeline as if adjacent bins
were continuous. NaN cells naturally break the plotted line instead of interpolating
through them.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

from plotting_common import TASK_COLORS, new_figure, save_figure, set_title, style_axis

DOMAIN_A_BIN_EDGES = list(range(1800, 2001, 10))
DOMAIN_B_BIN_EDGES = list(range(1500, 1801, 50))


def macro_recall(df: pd.DataFrame, gold_col: str, correct_col: str) -> tuple[float | None, int]:
    sub = df.dropna(subset=[correct_col])
    if sub.empty:
        return None, 0
    recalls = [group[correct_col].mean() for _, group in sub.groupby(gold_col, observed=True)]
    return (sum(recalls) / len(recalls) if recalls else None), len(sub)


def bin_label(left: int, right: int) -> str:
    return f"{left}-{right}"


def build_time_table(df: pd.DataFrame, bin_edges: list[int], include_isat: bool) -> pd.DataFrame:
    """One row per bin on the fixed grid, always — including bins with zero pairs
    (n_pairs=0, macro_recall=None/NaN). Empty bins are never dropped: doing so was
    the bug that made the line plot draw straight through a gap in the timeline."""
    order = [bin_label(a, b) for a, b in zip(bin_edges[:-1], bin_edges[1:])]
    rows = []
    for label in order:
        left, right = (int(x) for x in label.split("-"))
        group = df[(df["year"] >= left) & (df["year"] < right)]
        at_recall, at_n = macro_recall(group, "gold_at", "top5_correct_at")
        row = {"year_bin": label, "n_pairs": len(group), "at_macro_recall": at_recall, "at_n": at_n}
        if include_isat:
            isat_recall, isat_n = macro_recall(group, "gold_isAt", "top5_correct_isAt")
            row["isAt_macro_recall"] = isat_recall
            row["isAt_n"] = isat_n
        rows.append(row)

    table = pd.DataFrame(rows)
    table["year_bin"] = pd.Categorical(table["year_bin"], categories=order, ordered=True)
    return table.sort_values("year_bin").reset_index(drop=True)


def spearman_sanity_check(df: pd.DataFrame, task: str) -> tuple[float | None, float | None, int]:
    doc_level = df.groupby("document_id", observed=True).agg(
        year=("year", "first"),
        accuracy=(f"top5_correct_{task}", "mean"),
    )
    doc_level = doc_level.dropna(subset=["year", "accuracy"])
    if len(doc_level) < 2:
        return None, None, len(doc_level)
    rho, p_value = spearmanr(doc_level["year"], doc_level["accuracy"])
    return rho, p_value, len(doc_level)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis.d"))
    args = parser.parse_args()

    df = pd.read_parquet(args.features)
    df_a = df[df["dataset"] == "impresso"].copy()
    df_b = df[df["dataset"] == "surprise"].copy()

    tables_dir = args.output_dir / "tables"
    figures_dir = args.output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    table_a = build_time_table(df_a, DOMAIN_A_BIN_EDGES, include_isat=True)
    table_b = build_time_table(df_b, DOMAIN_B_BIN_EDGES, include_isat=False)
    table_a.to_csv(tables_dir / "rq2_time_bins_domainA.tsv", sep="\t", index=False)
    table_b.to_csv(tables_dir / "rq2_time_bins_domainB.tsv", sep="\t", index=False)

    corr_rows = []
    for domain_name, domain_df, tasks in [("A_impresso", df_a, ["at", "isAt"]), ("B_surprise", df_b, ["at"])]:
        for task in tasks:
            rho, p_value, n_documents = spearman_sanity_check(domain_df, task)
            corr_rows.append({"domain": domain_name, "task": task, "rho": rho, "p": p_value, "n_documents": n_documents})
    pd.DataFrame(corr_rows).to_csv(tables_dir / "rq2_time_correlation.tsv", sep="\t", index=False)

    # label_every=5 on Domain A's 10-year grid shows a tick roughly every 50 years
    # (the overlapping-label complaint); Domain B has few enough bins to label all.
    fig, axes = new_figure(ncols=2)
    for ax, table, title, include_isat, label_every in [
        (axes[0], table_a, "Domain A (impresso): macro recall per 10-year bin", True, 5),
        (axes[1], table_b, "Domain B (surprise): macro recall per 50-year bin", False, 1),
    ]:
        x = list(range(len(table)))
        n_pairs_list = list(table["n_pairs"])
        # NaN cells (empty bins) are neither drawn as a marker nor bridged by a
        # line segment — matplotlib breaks the line at NaN rather than interpolating.
        ax.plot(x, table["at_macro_recall"], marker="o", markersize=3, color=TASK_COLORS["at"], label="at")
        if include_isat:
            ax.plot(x, table["isAt_macro_recall"], marker="o", markersize=3, color=TASK_COLORS["isAt"], label="isAt")
        full_labels = [f"{label}\n(n={n})" for label, n in zip(table["year_bin"].astype(str), n_pairs_list)]
        tick_labels = [label if index % label_every == 0 else "" for index, label in enumerate(full_labels)]
        ax.set_xticks(x)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=5)
        style_axis(ax)
        set_title(ax, title)
        ax.legend(fontsize=6)
    save_figure(fig, figures_dir / "rq2_time.pdf")

    empty_a = table_a.loc[table_a["n_pairs"] == 0, "year_bin"].astype(str).tolist()
    empty_b = table_b.loc[table_b["n_pairs"] == 0, "year_bin"].astype(str).tolist()

    print(f"[RQ2] Domain A pairs: {len(df_a)} | Domain B pairs: {len(df_b)}")
    print("[RQ2] Domain A bin edges:", DOMAIN_A_BIN_EDGES)
    print(table_a.to_string(index=False))
    print(f"[RQ2] Domain A empty bins ({len(empty_a)}/{len(table_a)}): {empty_a}")
    print("[RQ2] Domain B bin edges:", DOMAIN_B_BIN_EDGES)
    print(table_b.to_string(index=False))
    print(f"[RQ2] Domain B empty bins ({len(empty_b)}/{len(table_b)}): {empty_b}")
    print(pd.DataFrame(corr_rows).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
