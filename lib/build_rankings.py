#!/usr/bin/env python3
"""Build HIPE-2026 ranking TSV files from per-run score JSON files."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import competition_ranks, load_json, tsv_escape


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(fieldnames) + "\n")
        for row in rows:
            handle.write("\t".join(tsv_escape(row.get(field)) for field in fieldnames) + "\n")


def load_per_run_rows(per_run_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(per_run_dir.glob("*.json")):
        row = load_json(path)
        row["_score_path"] = path.name
        rows.append(row)
    return rows


def score_value(row: dict[str, Any]) -> float | None:
    value = row.get("scores", {}).get("global_score")
    return float(value) if value is not None else None


def impresso_test_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row["dataset"] == "impresso" and row["split"] == "test"]


def expected_impresso_languages(rows: list[dict[str, Any]]) -> set[str]:
    return {row["language"] for row in impresso_test_rows(rows)}


def build_cell_rankings(rows: list[dict[str, Any]], output_dir: Path) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["dataset"], row["split"], row["language"])].append(row)

    for (dataset, split, language), group in sorted(groups.items()):
        ranking_rows = []
        for row in group:
            ranking_rows.append(
                {
                    "team": row["team"],
                    "run": row["run"],
                    "submission": row["submission"],
                    "score": score_value(row),
                    "at_macro_recall": row.get("scores", {}).get("at_macro_recall"),
                    "isAt_macro_recall": row.get("scores", {}).get("isAt_macro_recall"),
                    "info_missing": row.get("efficiency_metadata", {}).get("info_missing"),
                }
            )

        ranks = competition_ranks(ranking_rows, "score", higher_is_better=True)
        for ranking_row in ranking_rows:
            ranking_row["rank"] = ranks[(ranking_row["team"], ranking_row["run"])]

        ranking_rows.sort(key=lambda row: (row["rank"], row["team"], row["run"], row["submission"]))
        output_path = output_dir / f"ranking-{dataset}-{split}-{language}.tsv"
        write_tsv(
            output_path,
            [
                "rank",
                "team",
                "run",
                "submission",
                "score",
                "at_macro_recall",
                "isAt_macro_recall",
                "info_missing",
            ],
            ranking_rows,
        )


def build_overall_test_a(rows: list[dict[str, Any]], output_dir: Path) -> list[dict[str, Any]]:
    expected_languages = expected_impresso_languages(rows)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in impresso_test_rows(rows):
        grouped[(row["team"], row["run"])].append(row)

    overall_rows = []
    for (team, run), group in sorted(grouped.items()):
        languages = {row["language"] for row in group}
        if languages != expected_languages:
            continue
        values = [score_value(row) for row in group]
        score = mean([value for value in values if value is not None])
        overall_rows.append(
            {
                "team": team,
                "run": run,
                "score": score,
                "languages": ",".join(sorted(languages)),
                "num_language_files": len(languages),
            }
        )

    ranks = competition_ranks(overall_rows, "score", higher_is_better=True)
    for row in overall_rows:
        row["rank"] = ranks[(row["team"], row["run"])]

    overall_rows.sort(key=lambda row: (row["rank"], row["team"], row["run"]))
    write_tsv(
        output_dir / "ranking-overall-test-a.tsv",
        ["rank", "team", "run", "score", "languages", "num_language_files"],
        overall_rows,
    )
    return overall_rows


def build_generalization_test_b(rows: list[dict[str, Any]], output_dir: Path) -> None:
    ranking_rows = []
    for row in rows:
        if row["dataset"] == "surprise" and row["split"] == "test":
            ranking_rows.append(
                {
                    "team": row["team"],
                    "run": row["run"],
                    "submission": row["submission"],
                    "score": row.get("scores", {}).get("at_macro_recall"),
                    "info_missing": row.get("efficiency_metadata", {}).get("info_missing"),
                }
            )

    ranks = competition_ranks(ranking_rows, "score", higher_is_better=True)
    for row in ranking_rows:
        row["rank"] = ranks[(row["team"], row["run"])]

    ranking_rows.sort(key=lambda row: (row["rank"], row["team"], row["run"], row["submission"]))
    write_tsv(
        output_dir / "ranking-generalization-test-b.tsv",
        ["rank", "team", "run", "submission", "score", "info_missing"],
        ranking_rows,
    )


def build_efficiency_test_a(rows: list[dict[str, Any]], overall_rows: list[dict[str, Any]], output_dir: Path) -> None:
    complete_systems = {(row["team"], row["run"]) for row in overall_rows}
    by_system: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in impresso_test_rows(rows):
        key = (row["team"], row["run"])
        if key in complete_systems:
            by_system[key].append(row)

    accuracy_by_system = {(row["team"], row["run"]): row["score"] for row in overall_rows}
    efficiency_rows = []
    for (team, run), group in sorted(by_system.items()):
        missing_info = any(row.get("efficiency_metadata", {}).get("info_missing") for row in group)
        parameter_values = [
            row.get("efficiency_metadata", {}).get("hipe_parameter_count")
            for row in group
            if row.get("efficiency_metadata", {}).get("hipe_parameter_count") is not None
        ]
        model_size_values = [
            row.get("efficiency_metadata", {}).get("hipe_model_size")
            for row in group
            if row.get("efficiency_metadata", {}).get("hipe_model_size") is not None
        ]

        efficiency_rows.append(
            {
                "team": team,
                "run": run,
                "accuracy_score": accuracy_by_system.get((team, run)),
                "hipe_parameter_count": None if missing_info else mean([float(value) for value in parameter_values]),
                "hipe_model_size": None if missing_info else mean([float(value) for value in model_size_values]),
                "info_missing": missing_info,
            }
        )

    accuracy_ranks = competition_ranks(efficiency_rows, "accuracy_score", higher_is_better=True)
    parameter_ranks = competition_ranks(efficiency_rows, "hipe_parameter_count", higher_is_better=False)
    model_size_ranks = competition_ranks(efficiency_rows, "hipe_model_size", higher_is_better=False)

    for row in efficiency_rows:
        key = (row["team"], row["run"])
        row["rank_accuracy"] = accuracy_ranks[key]
        row["rank_parameter_count"] = parameter_ranks[key]
        row["rank_model_size"] = model_size_ranks[key]
        row["efficiency_score"] = (
            row["rank_accuracy"] + row["rank_parameter_count"] + row["rank_model_size"]
        ) / 3

    efficiency_ranks = competition_ranks(efficiency_rows, "efficiency_score", higher_is_better=False)
    for row in efficiency_rows:
        row["rank"] = efficiency_ranks[(row["team"], row["run"])]

    efficiency_rows.sort(key=lambda row: (row["rank"], row["team"], row["run"]))
    write_tsv(
        output_dir / "ranking-efficiency-test-a.tsv",
        [
            "rank",
            "team",
            "run",
            "efficiency_score",
            "rank_accuracy",
            "rank_parameter_count",
            "rank_model_size",
            "accuracy_score",
            "hipe_parameter_count",
            "hipe_model_size",
            "info_missing",
        ],
        efficiency_rows,
    )


def build_efficiency_language_rankings(rows: list[dict[str, Any]], output_dir: Path) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["dataset"] == "impresso" and row["split"] == "test":
            groups[(row["dataset"], row["split"], row["language"])].append(row)

    for (dataset, split, language), group in sorted(groups.items()):
        efficiency_rows = []
        for row in group:
            metadata = row.get("efficiency_metadata", {})
            missing_info = metadata.get("info_missing")
            efficiency_rows.append(
                {
                    "team": row["team"],
                    "run": row["run"],
                    "submission": row["submission"],
                    "accuracy_score": score_value(row),
                    "hipe_parameter_count": None
                    if missing_info
                    else metadata.get("hipe_parameter_count"),
                    "hipe_model_size": None if missing_info else metadata.get("hipe_model_size"),
                    "info_missing": missing_info,
                }
            )

        accuracy_ranks = competition_ranks(efficiency_rows, "accuracy_score", higher_is_better=True)
        parameter_ranks = competition_ranks(efficiency_rows, "hipe_parameter_count", higher_is_better=False)
        model_size_ranks = competition_ranks(efficiency_rows, "hipe_model_size", higher_is_better=False)

        for row in efficiency_rows:
            key = (row["team"], row["run"])
            row["rank_accuracy"] = accuracy_ranks[key]
            row["rank_parameter_count"] = parameter_ranks[key]
            row["rank_model_size"] = model_size_ranks[key]
            row["efficiency_score"] = (
                row["rank_accuracy"] + row["rank_parameter_count"] + row["rank_model_size"]
            ) / 3

        efficiency_ranks = competition_ranks(efficiency_rows, "efficiency_score", higher_is_better=False)
        for row in efficiency_rows:
            row["rank"] = efficiency_ranks[(row["team"], row["run"])]

        efficiency_rows.sort(key=lambda row: (row["rank"], row["team"], row["run"], row["submission"]))
        write_tsv(
            output_dir / f"ranking-efficiency-{dataset}-{split}-{language}.tsv",
            [
                "rank",
                "team",
                "run",
                "submission",
                "efficiency_score",
                "rank_accuracy",
                "rank_parameter_count",
                "rank_model_size",
                "accuracy_score",
                "hipe_parameter_count",
                "hipe_model_size",
                "info_missing",
            ],
            efficiency_rows,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-run-dir", type=Path, default=Path("results.d/per-run"))
    parser.add_argument("--output-dir", type=Path, default=Path("results.d/system-rankings"))
    args = parser.parse_args()

    rows = load_per_run_rows(args.per_run_dir) if args.per_run_dir.exists() else []
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if not rows:
        print("[OK] No per-run score JSON files found.")
        return 0

    build_cell_rankings(rows, args.output_dir)
    overall_rows = build_overall_test_a(rows, args.output_dir)
    build_generalization_test_b(rows, args.output_dir)
    build_efficiency_test_a(rows, overall_rows, args.output_dir)
    build_efficiency_language_rankings(rows, args.output_dir)
    print(f"[OK] Wrote rankings to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
