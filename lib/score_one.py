#!/usr/bin/env python3
"""Score one HIPE-2026 submission file against its matching reference."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from sklearn.metrics import accuracy_score, recall_score

from common import (
    find_cell_for_reference,
    load_competition_config,
    parse_reference_filename,
    parse_submission_filename,
    read_info_file,
    write_json,
)


def add_data_scripts_path(data_repo: Path) -> None:
    sys.path.insert(0, str((data_repo / "scripts").resolve()))


def normalize_label(value: Any) -> str:
    if value is None:
        return "FALSE"
    return str(value)


def parse_at_label_mode(value: str) -> str:
    mode = value.upper()
    if mode not in {"TERNARY", "BINARY"}:
        raise ValueError(f"Invalid AT label mode '{value}'. Expected TERNARY or BINARY.")
    return mode


def normalize_target_label(value: Any, target: str, at_label_mode: str) -> str:
    label = normalize_label(value)
    if target == "at" and at_label_mode == "BINARY" and label == "PROBABLE":
        return "TRUE"
    return label


def collect_labels(
    gold_data: dict[str, Any],
    submission_data: dict[str, Any],
    targets: list[str],
    at_label_mode: str,
) -> dict[str, dict[str, list[str]]]:
    labels = {target: {"gold": [], "pred": []} for target in targets}

    for doc_id, gold_doc in gold_data.items():
        gold_pairs = gold_doc.get("sampled_pairs", {})
        submission_pairs = submission_data[doc_id].get("sampled_pairs", {})

        for pair_key, gold_pair in gold_pairs.items():
            submission_pair = submission_pairs[pair_key]
            for target in targets:
                labels[target]["gold"].append(normalize_target_label(gold_pair.get(target), target, at_label_mode))
                labels[target]["pred"].append(normalize_target_label(submission_pair.get(target), target, at_label_mode))

    return labels


def compute_target_metrics(gold: list[str], pred: list[str]) -> dict[str, Any]:
    if not gold:
        return {
            "macro_recall": None,
            "accuracy": None,
            "correct": 0,
            "total": 0,
        }

    accuracy = float(accuracy_score(gold, pred))
    macro_recall = float(recall_score(gold, pred, average="macro", zero_division=0))
    return {
        "macro_recall": macro_recall,
        "accuracy": accuracy,
        "correct": sum(1 for expected, actual in zip(gold, pred) if expected == actual),
        "total": len(gold),
    }


def score_labels(labels: dict[str, dict[str, list[str]]], targets: list[str]) -> tuple[dict[str, Any], dict[str, int]]:
    scores: dict[str, Any] = {}
    counts: dict[str, int] = {}
    macro_recalls: list[float] = []

    for target in targets:
        metrics = compute_target_metrics(labels[target]["gold"], labels[target]["pred"])
        scores[f"{target}_macro_recall"] = metrics["macro_recall"]
        scores[f"{target}_accuracy"] = metrics["accuracy"]
        counts[f"{target}_correct"] = metrics["correct"]
        counts[f"{target}_total"] = metrics["total"]
        if metrics["macro_recall"] is not None:
            macro_recalls.append(metrics["macro_recall"])

    scores["global_score"] = sum(macro_recalls) / len(macro_recalls) if macro_recalls else None
    return scores, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, help="Submission JSONL file to score.")
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing flat reference JSONL files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results.d/per-run"),
        help="Directory for per-run score JSON files.",
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
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("lib/competition_config.json"),
        help="Competition configuration JSON.",
    )
    parser.add_argument(
        "--at-label-mode",
        default="TERNARY",
        choices=["TERNARY", "BINARY"],
        help="TERNARY keeps PROBABLE as a separate at label; BINARY maps PROBABLE to TRUE for at.",
    )
    args = parser.parse_args()
    at_label_mode = parse_at_label_mode(args.at_label_mode)

    add_data_scripts_path(args.data_repo)
    from check_jsonlschema import load_schema, validate_jsonl_file
    from evaluation_utils import (
        flatten_predictions,
        impute_missing_submission_data,
        load_jsonl_to_reshaped_dict,
    )

    try:
        submission_name = parse_submission_filename(args.submission)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    reference_path = args.reference_dir / submission_name.reference_filename
    if not reference_path.is_file():
        print(f"[ERROR] Reference file not found: {reference_path}", file=sys.stderr)
        return 1

    schema = load_schema(args.schema_path)
    reference_errors = validate_jsonl_file(reference_path, schema)
    submission_errors = validate_jsonl_file(args.submission, schema)
    if reference_errors or submission_errors:
        print(
            "[ERROR] JSON Schema validation failed. "
            f"Reference errors: {reference_errors}; submission errors: {submission_errors}.",
            file=sys.stderr,
        )
        return 1

    config = load_competition_config(args.config)
    cell = find_cell_for_reference(config, reference_path.name)
    if cell is None:
        parsed_cell = parse_reference_filename(reference_path.name)
        targets = ["at", "isAt"] if parsed_cell.dataset == "impresso" else ["at"]
        profile = "accuracy" if parsed_cell.dataset == "impresso" else "generalization"
    else:
        targets = list(cell["targets"])
        profile = str(cell["profile"])

    gold_data = load_jsonl_to_reshaped_dict(reference_path)
    submission_data = load_jsonl_to_reshaped_dict(args.submission)
    submission_data = impute_missing_submission_data(gold_data, submission_data)

    # Keep the submodule helper in the import path and call surface, but collect
    # target-specific labels here so Test B can ignore isAt and nulls become FALSE.
    flatten_predictions(gold_data, submission_data)
    labels = collect_labels(gold_data, submission_data, targets, at_label_mode)
    scores, counts = score_labels(labels, targets)

    parsed_reference = parse_reference_filename(reference_path.name)
    info_path = args.submission.with_name(submission_name.info_filename)
    try:
        efficiency_metadata, warnings = read_info_file(info_path)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    payload = {
        "submission": args.submission.name,
        "reference": reference_path.name,
        "team": submission_name.team,
        "dataset": parsed_reference.dataset,
        "split": parsed_reference.split,
        "language": parsed_reference.language,
        "run": submission_name.run,
        "profile": profile,
        "at_label_mode": at_label_mode,
        "targets": targets,
        "scores": scores,
        "counts": counts,
        "efficiency_metadata": efficiency_metadata,
        "warnings": warnings,
    }

    output_path = args.output_dir / f"{args.submission.stem}.json"
    write_json(output_path, payload)
    print(f"[OK] Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
