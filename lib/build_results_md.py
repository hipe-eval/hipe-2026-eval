#!/usr/bin/env python3
"""Render HIPE-2026 ranking TSV files into a Markdown results page."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import load_json


RANKING_TITLES = {
    "ranking-overall-test-a.tsv": "Accuracy Profile Ranking Overall",
    "ranking-efficiency-test-a.tsv": "Efficiency Profile Ranking Overall",
    "ranking-efficiency-impresso-test-de.tsv": "Efficiency Profile Ranking German",
    "ranking-efficiency-impresso-test-en.tsv": "Efficiency Profile Ranking English",
    "ranking-efficiency-impresso-test-fr.tsv": "Efficiency Profile Ranking French",
    "ranking-generalization-test-b.tsv": "Generalization Profile Ranking",
    "ranking-impresso-test-de.tsv": "Accuracy Profile Ranking German",
    "ranking-impresso-test-en.tsv": "Accuracy Profile Ranking English",
    "ranking-impresso-test-fr.tsv": "Accuracy Profile Ranking French",
    "ranking-surprise-test-fr.tsv": "Generalization Profile Ranking French",
}

RANKING_ORDER = [
    "ranking-overall-test-a.tsv",
    "ranking-impresso-test-de.tsv",
    "ranking-impresso-test-en.tsv",
    "ranking-impresso-test-fr.tsv",
    "ranking-generalization-test-b.tsv",
    "ranking-surprise-test-fr.tsv",
    "ranking-efficiency-test-a.tsv",
    "ranking-efficiency-impresso-test-de.tsv",
    "ranking-efficiency-impresso-test-en.tsv",
    "ranking-efficiency-impresso-test-fr.tsv",
]

DEFAULT_HEADER_LABELS = {
    "hipe_model_size": "hipe_model_size_mb",
    "rank_accuracy": "rank_impresso_profile_score",
    "rank_parameter_count": "rank_hipe_parameter_count",
    "rank_model_size": "rank_hipe_model_size",
}

RANKING_HEADER_LABELS = {
    "ranking-overall-test-a.tsv": {
        "score": "mean_impresso_profile_score",
    },
    "ranking-impresso-test-de.tsv": {
        "score": "impresso_profile_score",
    },
    "ranking-impresso-test-en.tsv": {
        "score": "impresso_profile_score",
    },
    "ranking-impresso-test-fr.tsv": {
        "score": "impresso_profile_score",
    },
    "ranking-generalization-test-b.tsv": {
        "score": "surprise_profile_score",
    },
    "ranking-surprise-test-fr.tsv": {
        "score": "surprise_profile_score",
    },
    "ranking-efficiency-test-a.tsv": {
        "efficiency_score": "mean_efficiency_profile_rank",
        "accuracy_score": "mean_impresso_profile_score",
    },
    "ranking-efficiency-impresso-test-de.tsv": {
        "efficiency_score": "mean_efficiency_profile_rank",
        "accuracy_score": "impresso_profile_score",
    },
    "ranking-efficiency-impresso-test-en.tsv": {
        "efficiency_score": "mean_efficiency_profile_rank",
        "accuracy_score": "impresso_profile_score",
    },
    "ranking-efficiency-impresso-test-fr.tsv": {
        "efficiency_score": "mean_efficiency_profile_rank",
        "accuracy_score": "impresso_profile_score",
    },
}


def format_cell(value: str) -> str:
    if value == "":
        return value
    try:
        numeric = float(value)
    except ValueError:
        return value
    return f"{numeric:.4f}".rstrip("0").rstrip(".")


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def with_diagnostic_links(
    headers: list[str],
    rows: list[dict[str, str]],
    diagnostics_dir: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    filtered_headers = [header for header in headers if header != "info_missing"]
    if "submission" not in headers:
        return filtered_headers, [{key: value for key, value in row.items() if key != "info_missing"} for row in rows]

    linked_headers = list(filtered_headers)
    if "diagnostics" not in linked_headers:
        linked_headers.append("diagnostics")

    linked_rows = []
    for row in rows:
        linked_row = {key: value for key, value in row.items() if key != "info_missing"}
        submission = row.get("submission", "")
        if submission.endswith(".jsonl"):
            stem = submission.removesuffix(".jsonl")
            comparison_link = f"[Comparison]({diagnostics_dir / f'{stem}.diagnostics.json'})"
            metrics_link = f"[Metrics]({diagnostics_dir / f'{stem}.diagnostic_metrics.json'})"
            linked_row["diagnostics"] = f"{comparison_link} / {metrics_link}"
        linked_rows.append(linked_row)

    return linked_headers, linked_rows


def markdown_table(headers: list[str], rows: list[dict[str, str]]) -> list[str]:
    return markdown_table_with_labels(headers, rows, {})


def markdown_table_with_labels(
    headers: list[str],
    rows: list[dict[str, str]],
    header_labels: dict[str, str],
) -> list[str]:
    if not headers:
        return ["No columns found.", ""]
    lines = [
        "| " + " | ".join(header_labels.get(header, header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(format_cell(row.get(header, "")) for header in headers)
            + " |"
        )
    if not rows:
        lines.append("| " + " | ".join("" for _ in headers) + " |")
    lines.append("")
    return lines


def anchor(title: str) -> str:
    chars = []
    for char in title.lower():
        if char.isalnum() or char == " " or char == "-":
            chars.append(char)
    return "".join(chars).strip().replace(" ", "-")


def sort_ranking_paths(paths: list[Path]) -> list[Path]:
    order = {name: index for index, name in enumerate(RANKING_ORDER)}
    return sorted(paths, key=lambda path: (order.get(path.name, len(order)), path.name))


def header_labels_for(path: Path) -> dict[str, str]:
    labels = dict(DEFAULT_HEADER_LABELS)
    labels.update(RANKING_HEADER_LABELS.get(path.name, {}))
    return labels


def score_definition_lines() -> list[str]:
    return [
        "## Profile Score Definitions",
        "",
        "- Accuracy Profile Ranking uses the `impresso` test files.",
        "- Generalization Profile Ranking uses the `surprise` test files.",
        "- For a label `l`, `recall_l = true_positives_l / gold_instances_l`.",
        "- `at_macro_recall = mean(recall_TRUE, recall_PROBABLE, recall_FALSE)` for the `at` labels.",
        "- `isAt_macro_recall = mean(recall_TRUE, recall_FALSE)` for the `isAt` labels.",
        "- `impresso_profile_score`: score for one `impresso` language file, computed as the mean of `at_macro_recall` and `isAt_macro_recall`.",
        "- `mean_impresso_profile_score`: mean of `impresso_profile_score` over the submitted `impresso` language files.",
        "- `surprise_profile_score`: score on a `surprise` file, computed as `at_macro_recall`; `isAt` is not evaluated for `surprise`.",
        "- `mean_efficiency_profile_rank`: mean of `rank_impresso_profile_score`, `rank_hipe_parameter_count`, and `rank_hipe_model_size`; lower is better.",
        "",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rankings-dir", type=Path, default=Path("results.d/system-rankings"))
    parser.add_argument("--diagnostics-dir", type=Path, default=Path("results.d/diagnostics"))
    parser.add_argument("--teams", type=Path, default=Path("lib/teams.json"))
    parser.add_argument("--output", type=Path, default=Path("HIPE_2026_evaluation_results.md"))
    args = parser.parse_args()

    teams = load_json(args.teams) if args.teams.is_file() else {}
    ranking_paths = (
        sort_ranking_paths(list(args.rankings_dir.glob("*.tsv")))
        if args.rankings_dir.exists()
        else []
    )

    lines = [
        "# HIPE-2026 Evaluation Results",
        "",
        f"This file is generated from `{args.rankings_dir}/*.tsv`.",
        "",
    ]

    if teams:
        lines.extend(["## Teams", ""])
        team_headers = ["team", "name", "affiliation"]
        team_rows = []
        for team_id, metadata in sorted(teams.items()):
            metadata = metadata if isinstance(metadata, dict) else {}
            team_rows.append(
                {
                    "team": team_id,
                    "name": str(metadata.get("name", "")),
                    "affiliation": str(metadata.get("affiliation", "")),
                }
            )
        lines.extend(markdown_table(team_headers, team_rows))

    if not ranking_paths:
        lines.extend(["## Rankings", "", "No ranking files found.", ""])
    else:
        toc_titles = [
            RANKING_TITLES.get(path.name, path.stem.replace("-", " ").title())
            for path in ranking_paths
        ]
        lines.extend(["## Table of Contents", ""])
        for title in toc_titles:
            lines.append(f"- [{title}](#{anchor(title)})")
        lines.append("")
        lines.extend(score_definition_lines())

        for path in ranking_paths:
            title = RANKING_TITLES.get(path.name, path.stem.replace("-", " ").title())
            headers, rows = read_tsv(path)
            headers, rows = with_diagnostic_links(headers, rows, args.diagnostics_dir)
            lines.extend([f"## {title}", ""])
            lines.extend(markdown_table_with_labels(headers, rows, header_labels_for(path)))

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
