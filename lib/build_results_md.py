#!/usr/bin/env python3
"""Render HIPE-2026 ranking TSV files into a Markdown results page."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import load_json


RANKING_TITLES = {
    "ranking-overall-test-a.tsv": "Accuracy Ranking Overall",
    "ranking-efficiency-test-a.tsv": "Efficiency Ranking Overall",
    "ranking-efficiency-impresso-test-de.tsv": "Efficiency Ranking German",
    "ranking-efficiency-impresso-test-en.tsv": "Efficiency Ranking English",
    "ranking-efficiency-impresso-test-fr.tsv": "Efficiency Ranking French",
    "ranking-generalization-test-b.tsv": "Generalization Ranking",
    "ranking-impresso-test-de.tsv": "Accuracy Ranking German",
    "ranking-impresso-test-en.tsv": "Accuracy Ranking English",
    "ranking-impresso-test-fr.tsv": "Accuracy Ranking French",
    "ranking-surprise-test-fr.tsv": "Surprise Test French",
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
    if not headers:
        return ["No columns found.", ""]
    lines = [
        "| " + " | ".join(headers) + " |",
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

        for path in ranking_paths:
            title = RANKING_TITLES.get(path.name, path.stem.replace("-", " ").title())
            headers, rows = read_tsv(path)
            headers, rows = with_diagnostic_links(headers, rows, args.diagnostics_dir)
            lines.extend([f"## {title}", ""])
            lines.extend(markdown_table(headers, rows))

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
