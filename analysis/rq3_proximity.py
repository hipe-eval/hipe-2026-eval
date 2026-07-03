#!/usr/bin/env python3
"""RQ3: does person-place proximity affect top5-ensemble accuracy? Pooled across
Domain A + Domain B as the primary view (per ANALYSIS_PLAN.md §10), with a per-domain
robustness split using the same pooled quartile bucket edges.

Reads analysis.d/tables/pair_level_features.parquet (read-only). Writes:
  analysis.d/tables/rq3_distance_quartiles.tsv             (pooled, primary)
  analysis.d/tables/rq3_distance_quartiles_by_domain.tsv   (same buckets, faceted by dataset)
  analysis.d/tables/rq3_distance_by_gold_label.tsv         (quartile x gold `at` label cross-tab)
  analysis.d/tables/rq3_distance_by_isat_label.tsv         (quartile x gold `isAt` label cross-tab)
  analysis.d/figures/rq3_proximity.pdf (+ .png)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from plotting_common import grouped_bar, new_figure, save_figure, set_title, style_axis


def macro_recall(df: pd.DataFrame, gold_col: str, correct_col: str) -> tuple[float | None, int]:
    sub = df.dropna(subset=[correct_col])
    if sub.empty:
        return None, 0
    recalls = [group[correct_col].mean() for _, group in sub.groupby(gold_col, observed=True)]
    return (sum(recalls) / len(recalls) if recalls else None), len(sub)


def build_quartile_table(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows = []
    for keys, group in df.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        at_recall, at_n = macro_recall(group, "gold_at", "top5_correct_at")
        isat_recall, isat_n = macro_recall(group, "gold_isAt", "top5_correct_isAt")
        row = dict(zip(group_cols, keys))
        row.update(
            {
                "n_pairs": len(group),
                "at_macro_recall": at_recall,
                "at_n": at_n,
                "isAt_macro_recall": isat_recall,
                "isAt_n": isat_n,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def assign_quartiles(matched: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, tuple[int, int]]]:
    """Also returns label -> (low, high) char-distance bounds per quartile, for the
    bin labels. The lowest quartile's lower bound is reported as the observed
    minimum rather than qcut's internal epsilon-shifted interval edge."""
    bins = pd.qcut(matched["min_char_distance"], 4, duplicates="drop")
    categories = bins.cat.categories
    observed_min = matched["min_char_distance"].min()
    label_map: dict = {}
    bounds: dict[str, tuple[int, int]] = {}
    for index, category in enumerate(categories):
        label = f"Q{index + 1}"
        label_map[category] = label
        low = observed_min if index == 0 else category.left
        bounds[label] = (int(round(low)), int(round(category.right)))
    matched = matched.copy()
    matched["distance_quartile"] = bins.map(label_map).astype(str)
    order = list(label_map.values())
    matched["distance_quartile"] = pd.Categorical(matched["distance_quartile"], categories=order, ordered=True)
    return matched, order, bounds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis.d"))
    args = parser.parse_args()

    df = pd.read_parquet(args.features)
    total = len(df)
    matched_mask = df["distance_match_status"] == "matched"
    matched = df[matched_mask].copy()

    unmatched_rate_by_track = df.groupby("track", observed=True)["distance_match_status"].apply(
        lambda s: (s == "unmatched").mean()
    )
    unmatched_count_by_track = df.groupby("track", observed=True)["distance_match_status"].apply(
        lambda s: (s == "unmatched").sum()
    )

    tables_dir = args.output_dir / "tables"
    figures_dir = args.output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    matched, quartile_order, quartile_bounds = assign_quartiles(matched)

    pooled_table = build_quartile_table(matched, ["distance_quartile"]).sort_values("distance_quartile").reset_index(drop=True)
    pooled_table.to_csv(tables_dir / "rq3_distance_quartiles.tsv", sep="\t", index=False)

    by_domain_table = (
        build_quartile_table(matched, ["dataset", "distance_quartile"])
        .sort_values(["dataset", "distance_quartile"])
        .reset_index(drop=True)
    )
    by_domain_table.to_csv(tables_dir / "rq3_distance_quartiles_by_domain.tsv", sep="\t", index=False)

    crosstab = pd.crosstab(matched["distance_quartile"], matched["gold_at"])
    crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0).round(4)
    crosstab_out = crosstab.add_suffix("_n").join(crosstab_pct.add_suffix("_pct"))
    crosstab_out.to_csv(tables_dir / "rq3_distance_by_gold_label.tsv", sep="\t")

    # isAt isn't evaluated for `surprise` (top5_correct_isAt is null there) — restrict
    # to the same rows isAt_macro_recall/isAt_n above are computed over.
    isat_matched = matched.dropna(subset=["top5_correct_isAt"])
    isat_crosstab = pd.crosstab(isat_matched["distance_quartile"], isat_matched["gold_isAt"])
    isat_crosstab_pct = isat_crosstab.div(isat_crosstab.sum(axis=1), axis=0).round(4)
    isat_crosstab_out = isat_crosstab.add_suffix("_n").join(isat_crosstab_pct.add_suffix("_pct"))
    isat_crosstab_out.to_csv(tables_dir / "rq3_distance_by_isat_label.tsv", sep="\t")

    fig, ax = new_figure()
    ticks = []
    for q, n in zip(pooled_table["distance_quartile"], pooled_table["n_pairs"]):
        low, high = quartile_bounds[str(q)]
        # 3 short lines rather than cramming the range onto the bucket-name line —
        # 4 narrow bar slots at single-column width overlap otherwise.
        ticks.append(f"{q}\n{low}–{high} chars\n(n={n})")
    grouped_bar(
        ax,
        ticks,
        {
            "at": list(pooled_table["at_macro_recall"]),
            "isAt": list(pooled_table["isAt_macro_recall"]),
        },
    )
    style_axis(ax)
    set_title(ax, "Top-5 ensemble macro-recall per person-place distance quartile")
    save_figure(fig, figures_dir / "rq3_proximity.pdf")

    print(
        f"[RQ3] total pairs: {total} | offset-matched: {len(matched)} "
        f"({len(matched) / total:.1%}) | unmatched: {total - len(matched)} ({1 - len(matched) / total:.1%})"
    )
    print("[RQ3] unmatched-mention rate by track (rate, count):")
    for track in unmatched_rate_by_track.index:
        print(f"  {track}: {unmatched_rate_by_track[track]:.1%} ({unmatched_count_by_track[track]} pairs)")
    print(pooled_table.to_string(index=False))

    if "PROBABLE" in crosstab_pct.columns and len(crosstab_pct) >= 2:
        first_q, last_q = quartile_order[0], quartile_order[-1]
        if first_q in crosstab_pct.index and last_q in crosstab_pct.index:
            probable_first = crosstab_pct.loc[first_q, "PROBABLE"]
            probable_last = crosstab_pct.loc[last_q, "PROBABLE"]
            if probable_first > 0 and probable_last >= 1.5 * probable_first:
                print(
                    f"[RQ3][CAVEAT] PROBABLE share is {probable_last:.1%} in {last_q} vs. "
                    f"{probable_first:.1%} in {first_q} — the largest-distance quartile is enriched for "
                    "PROBABLE (and possibly cross-sentential TRUE) cases; report macro-recall differences "
                    "across quartiles with this composition effect in mind, not as a pure distance effect."
                )

    print("[RQ3] isAt=TRUE share per distance quartile:")
    if "TRUE" in isat_crosstab_pct.columns:
        for q in quartile_order:
            if q in isat_crosstab_pct.index:
                print(f"  {q}: {isat_crosstab_pct.loc[q, 'TRUE']:.1%} TRUE (n={int(isat_crosstab.loc[q].sum())})")
        if len(isat_crosstab_pct) >= 2:
            first_q, last_q = quartile_order[0], quartile_order[-1]
            if first_q in isat_crosstab_pct.index and last_q in isat_crosstab_pct.index:
                true_first = isat_crosstab_pct.loc[first_q, "TRUE"]
                true_last = isat_crosstab_pct.loc[last_q, "TRUE"]
                if true_first > 0 and true_last <= 0.67 * true_first:
                    print(
                        f"[RQ3][CAVEAT] isAt=TRUE share drops from {true_first:.1%} in {first_q} to "
                        f"{true_last:.1%} in {last_q} — a system leaning toward predicting FALSE at long "
                        "range would look artificially strong on isAt macro recall there (FALSE-class "
                        "recall is easy when FALSE dominates support); check this before reading the "
                        "highest-distance-quartile isAt recall as a genuine strength."
                    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
