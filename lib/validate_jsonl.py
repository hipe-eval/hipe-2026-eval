#!/usr/bin/env python3
"""Validate HIPE-2026 JSONL files against the data schema."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def add_data_scripts_path(data_repo: Path) -> None:
    scripts_path = data_repo / "scripts"
    sys.path.insert(0, str(scripts_path.resolve()))


def collect_jsonl_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.jsonl")))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="JSONL files or directories containing JSONL files.",
    )
    parser.add_argument(
        "--schema-path",
        type=Path,
        default=Path("HIPE-2026-data/schemas/hipe-2026-data.schema.json"),
        help="Path to the HIPE-2026 JSON schema.",
    )
    parser.add_argument(
        "--data-repo",
        type=Path,
        default=Path("HIPE-2026-data"),
        help="Path to the HIPE-2026-data submodule.",
    )
    args = parser.parse_args()

    add_data_scripts_path(args.data_repo)
    from check_jsonlschema import load_schema, validate_jsonl_file

    if not args.schema_path.is_file():
        print(f"[ERROR] Schema file not found: {args.schema_path}", file=sys.stderr)
        return 1

    files = collect_jsonl_files(args.paths)
    missing = [path for path in files if not path.is_file()]
    if missing:
        for path in missing:
            print(f"[ERROR] File not found: {path}", file=sys.stderr)
        return 1

    if not files:
        print("[OK] No JSONL files found.")
        return 0

    schema = load_schema(args.schema_path)
    errors = 0
    for file_path in files:
        print(f"Validating {file_path}...")
        file_errors = validate_jsonl_file(file_path, schema)
        if file_errors:
            print(f"[FAIL] {file_path} had {file_errors} error(s).")
        else:
            print(f"[OK] {file_path} passed validation.")
        errors += file_errors

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
