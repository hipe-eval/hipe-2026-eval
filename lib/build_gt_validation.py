#!/usr/bin/env python3
"""Build majority-vote ground-truth validation workbooks."""

from __future__ import annotations

import argparse
import csv
import html
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

from build_diagnostics import (
    documents_by_id,
    normalize_label,
    pair_key,
    pairs_by_key,
    prediction_fields,
    targets_for_dataset,
)
from common import parse_reference_filename, parse_submission_filename


TOP_N = 3


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def ranking_path_for_reference(reference: Path, rankings_dir: Path) -> Path:
    cell = parse_reference_filename(reference.name)
    return rankings_dir / f"ranking-{cell.dataset}-{cell.split}-{cell.language}.tsv"


def top_submission_names(ranking_path: Path) -> list[str]:
    rows = read_tsv(ranking_path)
    submissions = [row.get("submission", "") for row in rows if row.get("submission", "")]
    return submissions[:TOP_N]


def safe_join(values: Any) -> str:
    if not isinstance(values, list):
        return ""
    return "; ".join(str(value) for value in values)


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def majority_vote(values: list[str]) -> tuple[str, str]:
    counts = Counter(values)
    if not counts:
        return "", "NO_VOTES"
    label, count = counts.most_common(1)[0]
    if count > len(values) / 2:
        return label, "MAJORITY"
    return "", "NO_MAJORITY"


def load_submission_pairs(submission_paths: list[Path]) -> dict[str, dict[str, dict[tuple[str | None, str | None], dict[str, Any]]]]:
    loaded: dict[str, dict[str, dict[tuple[str | None, str | None], dict[str, Any]]]] = {}
    for path in submission_paths:
        documents = documents_by_id(path)
        loaded[path.name] = {
            document_id: pairs_by_key(document)
            for document_id, document in documents.items()
        }
    return loaded


def system_columns(index: int) -> list[str]:
    return [
        f"system{index}_team",
        f"system{index}_run",
        f"system{index}_submission",
        f"system{index}_label",
        f"system{index}_explanation",
    ]


def mismatch_headers() -> list[str]:
    headers = [
        "dataset",
        "split",
        "language",
        "chunk_name",
        "document_id",
        "source",
        "date",
        "target",
        "gold_label",
        "vote_label",
        "vote_status",
        "pers_entity_id",
        "pers_wikidata_QID",
        "pers_mentions_list",
        "loc_entity_id",
        "loc_wikidata_QID",
        "loc_mentions_list",
    ]
    for index in range(1, TOP_N + 1):
        headers.extend(system_columns(index))
    return headers


def build_mismatch_rows(
    reference: Path,
    submission_paths: list[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    cell = parse_reference_filename(reference.name)
    targets = targets_for_dataset(cell.dataset)
    gold_documents = documents_by_id(reference)
    submission_pairs = load_submission_pairs(submission_paths)
    parsed_submissions = {path.name: parse_submission_filename(path) for path in submission_paths}
    mismatch_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    totals = {target: {"pairs": 0, "mismatches": 0, "no_majority": 0} for target in targets}

    for document_id, gold_document in gold_documents.items():
        gold_pairs = gold_document.get("sampled_pairs") or []
        for gold_pair in gold_pairs:
            if not isinstance(gold_pair, dict):
                continue
            key = pair_key(gold_pair)
            for target in targets:
                predictions: list[dict[str, Any]] = []
                for submission_path in submission_paths:
                    system_pair = submission_pairs.get(submission_path.name, {}).get(document_id, {}).get(key)
                    sys_at, sys_is_at, sys_at_explanation, sys_is_at_explanation = prediction_fields(system_pair)
                    label = normalize_label(sys_at if target == "at" else sys_is_at)
                    explanation = sys_at_explanation if target == "at" else sys_is_at_explanation
                    predictions.append(
                        {
                            "submission": submission_path.name,
                            "parsed": parsed_submissions[submission_path.name],
                            "label": label,
                            "explanation": explanation,
                        }
                    )

                gold_label = normalize_label(gold_pair.get(target))
                vote_label, vote_status = majority_vote([prediction["label"] for prediction in predictions])
                totals[target]["pairs"] += 1
                if vote_status == "NO_MAJORITY":
                    totals[target]["no_majority"] += 1
                if vote_label == gold_label and vote_status == "MAJORITY":
                    continue

                totals[target]["mismatches"] += 1
                row: dict[str, Any] = {
                    "dataset": cell.dataset,
                    "split": cell.split,
                    "language": cell.language,
                    "chunk_name": document_id,
                    "document_id": document_id,
                    "source": gold_document.get("source"),
                    "date": gold_document.get("date"),
                    "target": target,
                    "gold_label": gold_label,
                    "vote_label": vote_label,
                    "vote_status": vote_status,
                    "pers_entity_id": gold_pair.get("pers_entity_id"),
                    "pers_wikidata_QID": gold_pair.get("pers_wikidata_QID"),
                    "pers_mentions_list": safe_join(gold_pair.get("pers_mentions_list")),
                    "loc_entity_id": gold_pair.get("loc_entity_id"),
                    "loc_wikidata_QID": gold_pair.get("loc_wikidata_QID"),
                    "loc_mentions_list": safe_join(gold_pair.get("loc_mentions_list")),
                }
                for index, prediction in enumerate(predictions, start=1):
                    parsed = prediction["parsed"]
                    row.update(
                        {
                            f"system{index}_team": parsed.team,
                            f"system{index}_run": parsed.run,
                            f"system{index}_submission": prediction["submission"],
                            f"system{index}_label": prediction["label"],
                            f"system{index}_explanation": prediction["explanation"],
                        }
                    )
                mismatch_rows.append(row)

    top_run_rows = []
    for index, submission_path in enumerate(submission_paths, start=1):
        parsed = parsed_submissions[submission_path.name]
        top_run_rows.append(
            {
                "position": index,
                "team": parsed.team,
                "run": parsed.run,
                "submission": submission_path.name,
            }
        )

    for target, target_totals in totals.items():
        pairs = target_totals["pairs"]
        mismatches = target_totals["mismatches"]
        summary_rows.append(
            {
                "dataset": cell.dataset,
                "split": cell.split,
                "language": cell.language,
                "target": target,
                "pairs": pairs,
                "flagged_rows": mismatches,
                "no_majority_rows": target_totals["no_majority"],
                "flagged_share": round(mismatches / pairs, 4) if pairs else 0.0,
            }
        )

    return mismatch_rows, top_run_rows, summary_rows


def column_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def cell_xml(row_index: int, column_index: int, value: Any) -> str:
    ref = f"{column_letter(column_index)}{row_index}"
    if isinstance(value, bool):
        return f'<c r="{ref}" t="b"><v>{1 if value else 0}</v></c>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}"><v>{value}</v></c>'
    text = html.escape(safe_text(value), quote=False)
    return f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>'


def sheet_xml(headers: list[str], rows: list[dict[str, Any]]) -> str:
    xml_rows = []
    all_rows = [dict(zip(headers, headers))] + rows
    for row_index, row in enumerate(all_rows, start=1):
        cells = [cell_xml(row_index, column_index, row.get(header, "")) for column_index, header in enumerate(headers, start=1)]
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        '</worksheet>'
    )


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = []
    for index, name in enumerate(sheet_names, start=1):
        sheets.append(
            f'<sheet name="{html.escape(name)}" sheetId="{index}" '
            f'r:id="rId{index}"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets>{"".join(sheets)}</sheets>'
        '</workbook>'
    )


def workbook_rels_xml(sheet_count: int) -> str:
    relationships = []
    for index in range(1, sheet_count + 1):
        relationships.append(
            f'<Relationship Id="rId{index}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{index}.xml"/>'
        )
    relationships.append(
        f'<Relationship Id="rId{sheet_count + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(relationships)}'
        '</Relationships>'
    )


def content_types_xml(sheet_count: int) -> str:
    overrides = [
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for index in range(1, sheet_count + 1):
        overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f'{"".join(overrides)}'
        '</Types>'
    )


def package_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '</Relationships>'
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )


def write_xlsx(path: Path, sheets: list[tuple[str, list[str], list[dict[str, Any]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        archive.writestr("_rels/.rels", package_rels_xml())
        archive.writestr("xl/workbook.xml", workbook_xml([name for name, _, _ in sheets]))
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(sheets)))
        archive.writestr("xl/styles.xml", styles_xml())
        for index, (_, headers, rows) in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", sheet_xml(headers, rows))


def build_one_workbook(reference: Path, systems_dir: Path, rankings_dir: Path, output_dir: Path) -> Path:
    ranking_path = ranking_path_for_reference(reference, rankings_dir)
    if not ranking_path.is_file():
        raise FileNotFoundError(f"Ranking file not found for {reference.name}: {ranking_path}")
    submission_names = top_submission_names(ranking_path)
    if len(submission_names) < TOP_N:
        raise ValueError(f"{ranking_path} contains fewer than {TOP_N} ranked submissions.")
    submission_paths = [systems_dir / name for name in submission_names]
    for path in submission_paths:
        if not path.is_file():
            raise FileNotFoundError(f"Ranked submission not found: {path}")

    mismatch_rows, top_run_rows, summary_rows = build_mismatch_rows(reference, submission_paths)
    output_path = output_dir / f"{reference.stem}.gt_validation.xlsx"
    write_xlsx(
        output_path,
        [
            ("mismatches", mismatch_headers(), mismatch_rows),
            ("top_runs", ["position", "team", "run", "submission"], top_run_rows),
            (
                "summary",
                ["dataset", "split", "language", "target", "pairs", "flagged_rows", "no_majority_rows", "flagged_share"],
                summary_rows,
            ),
        ],
    )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--systems-dir", type=Path, default=Path("data/systems"))
    parser.add_argument("--rankings-dir", type=Path, default=Path("results.d/system-rankings"))
    parser.add_argument("--output-dir", type=Path, default=Path("results.d/gt-validation"))
    args = parser.parse_args()

    references = sorted(args.reference_dir.glob("*.jsonl")) if args.reference_dir.exists() else []
    if not references:
        print("[OK] No reference JSONL files found.")
        return 0

    failures = 0
    for reference in references:
        try:
            output_path = build_one_workbook(reference, args.systems_dir, args.rankings_dir, args.output_dir)
        except Exception as exc:
            print(f"[ERROR] {reference.name}: {exc}", file=sys.stderr)
            failures += 1
            continue
        print(f"[OK] Wrote {output_path}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
