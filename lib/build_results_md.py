#!/usr/bin/env python3
"""Render HIPE-2026 ranking TSV files into a Markdown results page."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import load_json


RANKING_TITLES = {
    "ranking-overall-test-a.tsv": "Overall Test A",
    "ranking-efficiency-test-a.tsv": "Efficiency Test A",
    "ranking-generalization-test-b.tsv": "Generalization Test B",
    "ranking-impresso-test-de.tsv": "Impresso Test German",
    "ranking-impresso-test-en.tsv": "Impresso Test English",
    "ranking-impresso-test-fr.tsv": "Impresso Test French",
    "ranking-surprise-test-fr.tsv": "Surprise Test French",
}


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def markdown_table(headers: list[str], rows: list[dict[str, str]]) -> list[str]:
    if not headers:
        return ["No columns found.", ""]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(header, "") for header in headers) + " |")
    if not rows:
        lines.append("| " + " | ".join("" for _ in headers) + " |")
    lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rankings-dir", type=Path, default=Path("results/system-rankings"))
    parser.add_argument("--teams", type=Path, default=Path("lib/teams.json"))
    parser.add_argument("--output", type=Path, default=Path("HIPE_2026_evaluation_results.md"))
    args = parser.parse_args()

    teams = load_json(args.teams) if args.teams.is_file() else {}
    ranking_paths = sorted(args.rankings_dir.glob("*.tsv")) if args.rankings_dir.exists() else []

    lines = [
        "# HIPE-2026 Evaluation Results",
        "",
        "This file is generated from `results/system-rankings/*.tsv`.",
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
        for path in ranking_paths:
            title = RANKING_TITLES.get(path.name, path.stem.replace("-", " ").title())
            headers, rows = read_tsv(path)
            lines.extend([f"## {title}", ""])
            lines.extend(markdown_table(headers, rows))

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
