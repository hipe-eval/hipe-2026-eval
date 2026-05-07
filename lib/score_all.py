#!/usr/bin/env python3
"""Score all HIPE-2026 submissions in data/systems."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--systems-dir", type=Path, default=Path("data/systems"))
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/per-run"))
    parser.add_argument("--schema-path", type=Path, default=Path("HIPE-2026-data/schemas/hipe-2026-data.schema.json"))
    parser.add_argument("--data-repo", type=Path, default=Path("HIPE-2026-data"))
    parser.add_argument("--config", type=Path, default=Path("lib/competition_config.json"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    submissions = sorted(args.systems_dir.glob("*.jsonl")) if args.systems_dir.exists() else []
    if not submissions:
        print("[OK] No submission JSONL files found.")
        return 0

    failures = 0
    for submission in submissions:
        command = [
            sys.executable,
            str(Path(__file__).with_name("score_one.py")),
            str(submission),
            "--reference-dir",
            str(args.reference_dir),
            "--output-dir",
            str(args.output_dir),
            "--schema-path",
            str(args.schema_path),
            "--data-repo",
            str(args.data_repo),
            "--config",
            str(args.config),
        ]
        result = subprocess.run(command, check=False)
        if result.returncode:
            failures += 1

    if failures:
        print(f"[FAIL] {failures} submission(s) failed scoring.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
