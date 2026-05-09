#!/usr/bin/env python3
"""Build merged diagnostics JSON files for HIPE-2026 submissions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from common import parse_reference_filename, parse_submission_filename


LABELS_BY_TARGET = {
    "at": ["TRUE", "PROBABLE", "FALSE"],
    "isAt": ["TRUE", "FALSE"],
}

BINARY_LABELS_BY_TARGET = {
    "at": ["TRUE", "FALSE"],
    "isAt": ["TRUE", "FALSE"],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path} on line {line_number}: {exc}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"{path} line {line_number} must contain a JSON object.")
            documents.append(payload)
    return documents


def documents_by_id(path: Path) -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for document in load_jsonl(path):
        document_id = document.get("document_id")
        if not isinstance(document_id, str):
            raise ValueError(f"{path} contains a document without a string document_id.")
        documents[document_id] = document
    return documents


def pair_key(pair: dict[str, Any]) -> tuple[str | None, str | None]:
    return pair.get("pers_entity_id"), pair.get("loc_entity_id")


def pairs_by_key(document: dict[str, Any] | None) -> dict[tuple[str | None, str | None], dict[str, Any]]:
    if document is None:
        return {}
    sampled_pairs = document.get("sampled_pairs")
    if not isinstance(sampled_pairs, list):
        return {}
    return {pair_key(pair): pair for pair in sampled_pairs if isinstance(pair, dict)}


def prediction_fields(pair: dict[str, Any] | None) -> tuple[str, str, str | None, str | None]:
    if pair is None:
        return "FALSE", "FALSE", None, None
    return (
        pair.get("at") or "FALSE",
        pair.get("isAt") or "FALSE",
        pair.get("at_explanation"),
        pair.get("isAt_explanation"),
    )


def normalize_label(value: Any) -> str:
    return value or "FALSE"


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


def targets_for_dataset(dataset: str) -> list[str]:
    if dataset == "surprise":
        return ["at"]
    return ["at", "isAt"]


def labels_for_target(target: str, at_label_mode: str) -> list[str]:
    labels_by_target = BINARY_LABELS_BY_TARGET if at_label_mode == "BINARY" else LABELS_BY_TARGET
    return labels_by_target[target]


def empty_confusion_matrices(targets: list[str], at_label_mode: str) -> dict[str, dict[str, Any]]:
    matrices: dict[str, dict[str, Any]] = {}
    for target in targets:
        labels = labels_for_target(target, at_label_mode)
        matrices[target] = {
            "labels": labels,
            "matrix": [[0 for _ in labels] for _ in labels],
            "rows": "gold",
            "columns": "prediction",
            "total": 0,
        }
    return matrices


def safe_divide(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def confusion_table(labels: list[str], matrix: list[list[int]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, values in zip(labels, matrix):
        row: dict[str, Any] = {"gold": label}
        for prediction_label, value in zip(labels, values):
            row[f"pred_{prediction_label}"] = value
        rows.append(row)
    return rows


def add_confusion_metrics(matrices: dict[str, dict[str, Any]]) -> None:
    for matrix_data in matrices.values():
        matrix = matrix_data["matrix"]
        labels = matrix_data["labels"]
        total = matrix_data["total"]
        correct = sum(matrix[index][index] for index in range(len(labels)))

        matrix_data["table"] = confusion_table(labels, matrix)
        matrix_data["accuracy"] = safe_divide(correct, total)
        per_label: dict[str, dict[str, Any]] = {}
        for index, label in enumerate(labels):
            true_positive = matrix[index][index]
            false_positive = sum(matrix[row_index][index] for row_index in range(len(labels))) - true_positive
            false_negative = sum(matrix[index][column_index] for column_index in range(len(labels))) - true_positive
            precision = safe_divide(true_positive, true_positive + false_positive)
            recall = safe_divide(true_positive, true_positive + false_negative)
            f1 = safe_divide(2 * precision * recall, precision + recall)
            per_label[label] = {
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "support": sum(matrix[index]),
                "true_positive": true_positive,
                "false_positive": false_positive,
                "false_negative": false_negative,
            }
        matrix_data["per_label"] = per_label


def add_confusion_observation(
    matrices: dict[str, dict[str, Any]],
    target: str,
    gold_value: Any,
    prediction_value: Any,
    at_label_mode: str,
) -> None:
    labels = matrices[target]["labels"]
    gold_label = normalize_target_label(gold_value, target, at_label_mode)
    prediction_label = normalize_target_label(prediction_value, target, at_label_mode)
    if gold_label not in labels:
        raise ValueError(f"Unexpected gold label for {target}: {gold_label!r}")
    if prediction_label not in labels:
        raise ValueError(f"Unexpected prediction label for {target}: {prediction_label!r}")
    gold_index = labels.index(gold_label)
    prediction_index = labels.index(prediction_label)
    matrices[target]["matrix"][gold_index][prediction_index] += 1
    matrices[target]["total"] += 1


def build_merged_analysis(
    gold_jsonl: Path,
    predictions_jsonl: Path,
    targets: list[str],
    at_label_mode: str,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    gold_documents = documents_by_id(gold_jsonl)
    prediction_documents = documents_by_id(predictions_jsonl)
    merged_documents: list[dict[str, Any]] = []
    confusion_matrices = empty_confusion_matrices(targets, at_label_mode)

    for document_id, gold_document in gold_documents.items():
        prediction_document = prediction_documents.get(document_id)
        prediction_pairs = pairs_by_key(prediction_document)
        gold_pairs = gold_document.get("sampled_pairs") or []
        merged_pairs: list[dict[str, Any]] = []

        for gold_pair in gold_pairs:
            if not isinstance(gold_pair, dict):
                continue
            system_pair = prediction_pairs.get(pair_key(gold_pair))
            sys_at, sys_is_at, sys_at_explanation, sys_is_at_explanation = prediction_fields(
                system_pair
            )
            system_values = {"at": sys_at, "isAt": sys_is_at}
            for target in targets:
                add_confusion_observation(
                    confusion_matrices,
                    target,
                    gold_pair.get(target),
                    system_values[target],
                    at_label_mode,
                )

            gold_at = normalize_target_label(gold_pair.get("at"), "at", at_label_mode)
            system_at = normalize_target_label(sys_at, "at", at_label_mode)
            gold_is_at = normalize_target_label(gold_pair.get("isAt"), "isAt", at_label_mode)
            system_is_at = normalize_target_label(sys_is_at, "isAt", at_label_mode)
            merged_pairs.append(
                {
                    "pers_entity_id": gold_pair.get("pers_entity_id"),
                    "pers_wikidata_QID": gold_pair.get("pers_wikidata_QID"),
                    "pers_mentions_list": list(gold_pair.get("pers_mentions_list") or []),
                    "loc_entity_id": gold_pair.get("loc_entity_id"),
                    "loc_wikidata_QID": gold_pair.get("loc_wikidata_QID"),
                    "loc_mentions_list": list(gold_pair.get("loc_mentions_list") or []),
                    "at": gold_at,
                    "SYS_at": system_at,
                    "CORRECT_at": system_at == gold_at,
                    "SYS_at_explanation": sys_at_explanation,
                    "isAt": gold_is_at,
                    "SYS_isAt": system_is_at,
                    "CORRECT_isAt": system_is_at == gold_is_at,
                    "SYS_isAt_explanation": sys_is_at_explanation,
                    "CORRECT": (system_at == gold_at) and (system_is_at == gold_is_at),
                }
            )

        merged_documents.append(
            {
                "document_id": gold_document.get("document_id"),
                "media": gold_document.get("media"),
                "source": gold_document.get("source"),
                "date": gold_document.get("date"),
                "language": gold_document.get("language"),
                "text": gold_document.get("text"),
                "sampled_pairs": merged_pairs,
            }
        )

    add_confusion_metrics(confusion_matrices)
    return merged_documents, confusion_matrices


def write_merged_analysis(documents: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(documents, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_diagnostic_metrics_payload(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def build_one_diagnostics(submission: Path, reference_dir: Path, output_dir: Path, at_label_mode: str) -> tuple[Path, Path]:
    parsed = parse_submission_filename(submission)
    reference = reference_dir / parsed.reference_filename
    if not reference.is_file():
        raise FileNotFoundError(f"Reference file not found for {submission.name}: {reference}")

    reference_cell = parse_reference_filename(reference.name)
    targets = targets_for_dataset(reference_cell.dataset)
    diagnostics_path = output_dir / f"{submission.stem}.diagnostics.json"
    diagnostic_metrics_path = output_dir / f"{submission.stem}.diagnostic_metrics.json"
    merged, confusion_matrices = build_merged_analysis(reference, submission, targets, at_label_mode)
    write_merged_analysis(merged, diagnostics_path)
    write_diagnostic_metrics_payload(
        {
            "submission": submission.name,
            "reference": reference.name,
            "team": parsed.team,
            "dataset": reference_cell.dataset,
            "split": reference_cell.split,
            "language": reference_cell.language,
            "run": parsed.run,
            "at_label_mode": at_label_mode,
            "confusion_matrices": confusion_matrices,
        },
        diagnostic_metrics_path,
    )
    return diagnostics_path, diagnostic_metrics_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--systems-dir",
        type=Path,
        default=Path("data/systems"),
        help="Directory containing participant JSONL submissions.",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        default=Path("data/reference"),
        help="Directory containing flat reference JSONL files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results.d/diagnostics"),
        help="Directory for generated diagnostics JSON files.",
    )
    parser.add_argument(
        "--at-label-mode",
        default="TERNARY",
        choices=["TERNARY", "BINARY"],
        help="TERNARY keeps PROBABLE as a separate at label; BINARY maps PROBABLE to TRUE for at.",
    )
    args = parser.parse_args()
    at_label_mode = parse_at_label_mode(args.at_label_mode)

    submissions = sorted(args.systems_dir.glob("*.jsonl")) if args.systems_dir.exists() else []
    if not submissions:
        print("[OK] No submission JSONL files found.")
        return 0

    failures = 0
    for submission in submissions:
        try:
            diagnostics_path, diagnostic_metrics_path = build_one_diagnostics(
                submission, args.reference_dir, args.output_dir, at_label_mode
            )
        except Exception as exc:
            print(f"[ERROR] {submission.name}: {exc}", file=sys.stderr)
            failures += 1
            continue
        print(f"[OK] Wrote {diagnostics_path}")
        print(f"[OK] Wrote {diagnostic_metrics_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
