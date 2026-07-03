#!/usr/bin/env python3
"""RQ1: does OCR quality affect top5-ensemble accuracy? Domain A (`impresso`) only —
Domain B (`surprise`) is literary text, not OCR'd.

Reads analysis.d/tables/pair_level_features.parquet (read-only). Writes:
  analysis.d/tables/rq1_ocr_tertiles.tsv
  analysis.d/tables/rq1_ocr_tertiles_by_language.tsv
  analysis.d/tables/rq1_ocr_correlation.tsv   (Spearman sanity check, not a regression)
  analysis.d/figures/rq1_ocr_quality.pdf
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

from plotting_common import bucket_tick_label, grouped_bar, new_figure, save_figure, style_axis


def macro_recall(df: pd.DataFrame, gold_col: str, correct_col: str) -> tuple[float | None, int]:
    sub = df.dropna(subset=[correct_col])
    if sub.empty:
        return None, 0
    recalls = [group[correct_col].mean() for _, group in sub.groupby(gold_col, observed=True)]
    return (sum(recalls) / len(recalls) if recalls else None), len(sub)


def build_tertile_table(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
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


def assign_tertiles(doc_scores: pd.DataFrame) -> pd.DataFrame:
    """qcut with duplicates='drop': falls back to fewer buckets if OCR scores repeat
    (e.g. many documents scoring a clean 1.0), rather than raising."""
    bins = pd.qcut(doc_scores["ocr_score"], 3, duplicates="drop")
    categories = bins.cat.categories
    label_map = {category: f"T{index + 1}" for index, category in enumerate(categories)}
    doc_scores = doc_scores.copy()
    doc_scores["ocr_tertile"] = bins.map(label_map).astype(str)
    order = list(label_map.values())
    doc_scores["ocr_tertile"] = pd.Categorical(doc_scores["ocr_tertile"], categories=order, ordered=True)
    return doc_scores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis.d"))
    args = parser.parse_args()

    df = pd.read_parquet(args.features)
    df_a = df[df["dataset"] == "impresso"].copy()

    doc_scores = df_a.drop_duplicates("document_id")[["document_id", "ocr_score"]].dropna()
    doc_scores = assign_tertiles(doc_scores)
    df_a = df_a.merge(doc_scores[["document_id", "ocr_tertile"]], on="document_id", how="left")
    df_a = df_a.dropna(subset=["ocr_tertile"])

    tables_dir = args.output_dir / "tables"
    figures_dir = args.output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    tertile_table = build_tertile_table(df_a, ["ocr_tertile"]).sort_values("ocr_tertile").reset_index(drop=True)
    tertile_table.to_csv(tables_dir / "rq1_ocr_tertiles.tsv", sep="\t", index=False)

    by_language = (
        build_tertile_table(df_a, ["language", "ocr_tertile"])
        .sort_values(["language", "ocr_tertile"])
        .reset_index(drop=True)
    )
    by_language.to_csv(tables_dir / "rq1_ocr_tertiles_by_language.tsv", sep="\t", index=False)

    doc_level = df_a.groupby("document_id", observed=True).agg(
        ocr_score=("ocr_score", "first"),
        at_accuracy=("top5_correct_at", "mean"),
        isAt_accuracy=("top5_correct_isAt", "mean"),
    )
    corr_rows = []
    for task in ["at", "isAt"]:
        sub = doc_level.dropna(subset=["ocr_score", f"{task}_accuracy"])
        if len(sub) >= 2:
            rho, p_value = spearmanr(sub["ocr_score"], sub[f"{task}_accuracy"])
        else:
            rho, p_value = None, None
        corr_rows.append({"task": task, "rho": rho, "p": p_value, "n_documents": len(sub)})
    pd.DataFrame(corr_rows).to_csv(tables_dir / "rq1_ocr_correlation.tsv", sep="\t", index=False)

    fig, ax = new_figure()
    ticks = [bucket_tick_label(str(label), n) for label, n in zip(tertile_table["ocr_tertile"], tertile_table["n_pairs"])]
    grouped_bar(
        ax,
        ticks,
        {
            "at": list(tertile_table["at_macro_recall"]),
            "isAt": list(tertile_table["isAt_macro_recall"]),
        },
    )
    style_axis(ax)
    ax.set_title("RQ1: OCR-quality tertile vs. top5-ensemble macro recall", fontsize=7)
    save_figure(fig, figures_dir / "rq1_ocr_quality.pdf")

    print(f"[RQ1] impresso pairs considered: {len(df_a)} across {len(doc_scores)} documents with an OCR score")
    print(tertile_table.to_string(index=False))
    print(pd.DataFrame(corr_rows).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
