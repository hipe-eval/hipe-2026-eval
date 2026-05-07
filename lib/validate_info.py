#!/usr/bin/env python3
"""Validate HIPE-2026 submission metadata files and run limits."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from common import INFO_RE, parse_submission_filename, read_info_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--systems-dir",
        type=Path,
        default=Path("data/systems"),
        help="Directory containing participant JSONL submissions and info files.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing flat reference JSONL files.",
    )
    args = parser.parse_args()

    if not args.systems_dir.exists():
        print(f"[OK] Systems directory does not exist yet: {args.systems_dir}")
        return 0

    errors = 0
    warnings = 0
    submission_files = sorted(args.systems_dir.glob("*.jsonl"))
    info_files = sorted(args.systems_dir.glob("*-info.json"))

    run_groups: dict[tuple[str, str], set[str]] = defaultdict(set)
    expected_info_files: set[str] = set()

    for submission_file in submission_files:
        try:
            parsed = parse_submission_filename(submission_file)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            errors += 1
            continue

        reference_path = args.reference_dir / parsed.reference_filename
        if not reference_path.is_file():
            print(
                f"[ERROR] Missing reference for {submission_file.name}: {reference_path}",
                file=sys.stderr,
            )
            errors += 1

        run_groups[(parsed.team, parsed.reference_filename)].add(parsed.run)
        expected_info_files.add(parsed.info_filename)

        info_path = args.systems_dir / parsed.info_filename
        try:
            _, info_warnings = read_info_file(info_path)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            errors += 1
            continue

        for warning in info_warnings:
            print(f"[WARN] {warning}", file=sys.stderr)
            warnings += 1

    for (team, reference_filename), runs in sorted(run_groups.items()):
        if len(runs) > 3:
            print(
                f"[ERROR] {team} has {len(runs)} runs for {reference_filename}; maximum is 3.",
                file=sys.stderr,
            )
            errors += 1

    for info_file in info_files:
        if not INFO_RE.match(info_file.name):
            print(f"[ERROR] Invalid info filename: {info_file.name}", file=sys.stderr)
            errors += 1
        elif info_file.name not in expected_info_files:
            print(f"[ERROR] Info file has no matching submission: {info_file.name}", file=sys.stderr)
            errors += 1

    if errors:
        print(f"[FAIL] validate-info found {errors} error(s) and {warnings} warning(s).")
        return 1

    print(f"[OK] validate-info passed with {warnings} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
