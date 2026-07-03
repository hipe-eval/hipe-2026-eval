#!/usr/bin/env python3
"""RQ1: does OCR quality affect top5-ensemble accuracy? Domain A (`impresso`) only —
Domain B (`surprise`) is literary text, not OCR'd.

Reads analysis.d/tables/pair_level_features.parquet (read-only). Writes:
  analysis.d/tables/rq1_ocr_tertiles.tsv
  analysis.d/tables/rq1_ocr_tertiles_by_language.tsv
  analysis.d/tables/rq1_ocr_correlation.tsv   (Spearman sanity check, not a regression)
  analysis.d/figures/rq1_ocr_quality.pdf (+ .png)
  analysis.d/figures/rq1_ocr_quality_by_language.pdf (+ .png)   diagnostic, not a paper figure

The by-language table/figure is reindexed onto the full (language x tertile) grid so
a language with zero pairs in a tertile (e.g. no German documents in the highest-OCR
tertile) gets an explicit n_pairs=0 row instead of a silently missing one.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

from plotting_common import grouped_bar, new_figure, save_figure, set_title, style_axis


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


def assign_tertiles(doc_scores: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, tuple[float, float]]]:
    """qcut with duplicates='drop': falls back to fewer buckets if OCR scores repeat
    (e.g. many documents scoring a clean 1.0), rather than raising.

    Also returns label -> (low, high) OCR-score bounds per tertile, for the bin
    labels. The lowest tertile's lower bound is reported as the observed minimum
    rather than qcut's internal epsilon-shifted interval edge (e.g. 0.579 instead
    of the actual 0.58 minimum)."""
    bins = pd.qcut(doc_scores["ocr_score"], 3, duplicates="drop")
    categories = bins.cat.categories
    observed_min = doc_scores["ocr_score"].min()
    label_map: dict = {}
    bounds: dict[str, tuple[float, float]] = {}
    for index, category in enumerate(categories):
        label = f"T{index + 1}"
        label_map[category] = label
        low = observed_min if index == 0 else category.left
        bounds[label] = (low, category.right)
    doc_scores = doc_scores.copy()
    doc_scores["ocr_tertile"] = bins.map(label_map).astype(str)
    order = list(label_map.values())
    doc_scores["ocr_tertile"] = pd.Categorical(doc_scores["ocr_tertile"], categories=order, ordered=True)
    return doc_scores, bounds


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis.d"))
    args = parser.parse_args()

    df = pd.read_parquet(args.features)
    df_a = df[df["dataset"] == "impresso"].copy()

    doc_scores = df_a.drop_duplicates("document_id")[["document_id", "ocr_score"]].dropna()
    doc_scores, tertile_bounds = assign_tertiles(doc_scores)
    df_a = df_a.merge(doc_scores[["document_id", "ocr_tertile"]], on="document_id", how="left")
    df_a = df_a.dropna(subset=["ocr_tertile"])

    tables_dir = args.output_dir / "tables"
    figures_dir = args.output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    tertile_table = build_tertile_table(df_a, ["ocr_tertile"]).sort_values("ocr_tertile").reset_index(drop=True)
    tertile_table.to_csv(tables_dir / "rq1_ocr_tertiles.tsv", sep="\t", index=False)

    tertile_order = list(tertile_bounds.keys())
    languages = sorted(df_a["language"].unique())

    by_language = build_tertile_table(df_a, ["language", "ocr_tertile"])
    # Reindex onto the full (language x tertile) grid: a (language, tertile) combo
    # with zero pairs must appear as an explicit n_pairs=0 row, not be silently
    # absent (e.g. no German documents fall in the highest-OCR tertile at all).
    full_index = pd.MultiIndex.from_product([languages, tertile_order], names=["language", "ocr_tertile"])
    by_language = by_language.set_index(["language", "ocr_tertile"]).reindex(full_index).reset_index()
    for count_col in ["n_pairs", "at_n", "isAt_n"]:
        by_language[count_col] = by_language[count_col].fillna(0).astype(int)
    by_language["ocr_tertile"] = pd.Categorical(by_language["ocr_tertile"], categories=tertile_order, ordered=True)
    by_language = by_language.sort_values(["language", "ocr_tertile"]).reset_index(drop=True)
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
    ticks = []
    for label, n in zip(tertile_table["ocr_tertile"], tertile_table["n_pairs"]):
        low, high = tertile_bounds[str(label)]
        # 3 short lines rather than cramming the range onto the bucket-name line,
        # for the same reason as RQ3's quartile labels.
        ticks.append(f"{label}\n{low:.2f}–{high:.2f}\n(n={n})")
    grouped_bar(
        ax,
        ticks,
        {
            "at": list(tertile_table["at_macro_recall"]),
            "isAt": list(tertile_table["isAt_macro_recall"]),
        },
    )
    style_axis(ax)
    set_title(ax, "Top-5 ensemble macro-recall per OCR-quality tertile")
    save_figure(fig, figures_dir / "rq1_ocr_quality.pdf")

    # Diagnostic (not a paper figure): same tertile x macro-recall view, faceted
    # per language, to check whether the pooled tertile pattern holds within each
    # language or is driven by one language's document mix.
    fig_lang, axes_lang = new_figure(ncols=len(languages))
    for ax_lang, language in zip(axes_lang, languages):
        lang_table = by_language[by_language["language"] == language].sort_values("ocr_tertile").reset_index(drop=True)
        ticks = []
        for label, n in zip(lang_table["ocr_tertile"], lang_table["n_pairs"]):
            low, high = tertile_bounds[str(label)]
            ticks.append(f"{label}\n{low:.2f}–{high:.2f}\n(n={n})")
        grouped_bar(
            ax_lang,
            ticks,
            {
                "at": list(lang_table["at_macro_recall"]),
                "isAt": list(lang_table["isAt_macro_recall"]),
            },
        )
        style_axis(ax_lang)
        set_title(ax_lang, f"{language}: macro-recall per OCR-quality tertile")
    save_figure(fig_lang, figures_dir / "rq1_ocr_quality_by_language.pdf")

    doc_lang_tertile = (
        df_a.drop_duplicates("document_id")[["document_id", "language", "ocr_tertile"]]
        .groupby(["language", "ocr_tertile"], observed=True)
        .size()
    )

    print(f"[RQ1] impresso pairs considered: {len(df_a)} across {len(doc_scores)} documents with an OCR score")
    print(tertile_table.to_string(index=False))
    print(pd.DataFrame(corr_rows).to_string(index=False))
    print("[RQ1] per-language document counts per tertile:")
    print(doc_lang_tertile.to_string())
    print("[RQ1] per-language pair counts / macro recall per tertile:")
    print(by_language.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
