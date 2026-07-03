#!/usr/bin/env python3
"""Build the shared per-pair feature table for the overview-paper error analysis.

Joins, per sampled pair in every `data/reference/*.jsonl` file: reference data
(document text, mention strings, Wikidata QIDs/NIL status, document metadata) with
the top5-ensemble per-pair correctness for `at` and `isAt` (from
`results.d/ensemble/<track>.ensemble.json`). Written once to
`analysis.d/tables/pair_level_features.parquet`; consumed by every RQ script.

Read-only against `results.d/` and `data/reference/`, per CLAUDE.md's "Analysis
Scripts" isolation rules. Not wired into `eval-full` / `make ensemble`.

Two per-pair columns are *derived* here rather than read off a schema field, because
no such field exists in the reference data:
  - `min_char_distance` / `distance_match_status`: reference `sampled_pairs` entries
    carry only surface-string mention lists (`pers_mentions_list`/`loc_mentions_list`),
    not character offsets. Offsets are recovered by locating each mention string in
    the document `text` (word-boundary-aware substring search); pairs where a mention
    string can't be located verbatim are marked `distance_match_status="unmatched"`
    and given a null distance rather than an imputed one. See ANALYSIS_PLAN.md §3.5
    for the known failure modes of this approach.
  - `ocr_score`: computed per document (impresso/Domain A only) via
    `impresso_pipelines.ocrqa.OCRQAPipeline`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import parse_reference_filename  # noqa: E402

YEAR_RE = re.compile(r"(\d{4})")

_ocrqa_pipeline = None


def get_ocrqa_pipeline():
    global _ocrqa_pipeline
    if _ocrqa_pipeline is None:
        from impresso_pipelines.ocrqa import OCRQAPipeline

        _ocrqa_pipeline = OCRQAPipeline()
    return _ocrqa_pipeline


def compute_ocr_score(text: str, language: str | None) -> float | None:
    if not text or not language:
        return None
    result = get_ocrqa_pipeline()(text, language=language)
    return result.get("score")


def parse_year(date_value: Any) -> int | None:
    if not date_value:
        return None
    match = YEAR_RE.search(str(date_value))
    return int(match.group(1)) if match else None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    documents = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                documents.append(json.loads(stripped))
    return documents


def load_ensemble_pairs(path: Path) -> tuple[dict[tuple, dict], dict[tuple, dict] | None]:
    """Return (at_map, isAt_map) keyed by (document_id, pers_entity_id, loc_entity_id).

    isAt_map is None when the track's top5 ensemble doesn't cover isAt (surprise-test-fr).
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    top5 = payload["ensembles"]["top5"]

    at_map = {}
    for pair in top5["at"]["pairs"]:
        key = (pair["document_id"], pair["pers_entity_id"], pair["loc_entity_id"])
        at_map[key] = {"vote_at": pair["vote_at"], "correct_at": pair["correct_at"]}

    isAt_map = None
    if "isAt" in top5:
        isAt_map = {}
        for pair in top5["isAt"]["pairs"]:
            key = (pair["document_id"], pair["pers_entity_id"], pair["loc_entity_id"])
            isAt_map[key] = {"vote_isAt": pair["vote_isAt"], "correct_isAt": pair["correct_isAt"]}

    return at_map, isAt_map


def find_occurrences(text: str, mention: str) -> list[tuple[int, int]]:
    """Word-boundary-aware occurrences of `mention` in `text` (not a regex \\b match,
    since mentions can end in punctuation like "B. Ad." where \\b behaves oddly)."""
    if not mention:
        return []
    spans = []
    for match in re.finditer(re.escape(mention), text):
        start, end = match.start(), match.end()
        before_ok = start == 0 or not text[start - 1].isalnum()
        after_ok = end == len(text) or not text[end].isalnum()
        if before_ok and after_ok:
            spans.append((start, end))
    return spans


def span_gap(a: tuple[int, int], b: tuple[int, int]) -> int:
    (s1, e1), (s2, e2) = a, b
    if e1 <= s2:
        return s2 - e1
    if e2 <= s1:
        return s1 - e2
    return 0


def min_char_distance(person_spans: list[tuple[int, int]], loc_spans: list[tuple[int, int]]) -> int | None:
    if not person_spans or not loc_spans:
        return None
    return min(span_gap(p, l) for p in person_spans for l in loc_spans)


def build_track_rows(
    reference_path: Path,
    ensemble_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cell = parse_reference_filename(reference_path.name)
    track = f"{cell.dataset}-{cell.split}-{cell.language}"

    ensemble_path = ensemble_dir / f"{track}.ensemble.json"
    at_map, isAt_map = load_ensemble_pairs(ensemble_path)

    documents = load_jsonl(reference_path)

    rows: list[dict[str, Any]] = []
    stats = {
        "track": track,
        "n_documents": len(documents),
        "n_pairs": 0,
        "n_ensemble_at_matched": 0,
        "n_isAt_available": isAt_map is not None,
        "n_ensemble_isAt_matched": 0,
        "n_offset_matched": 0,
        "n_offset_unmatched": 0,
    }

    for document in documents:
        document_id = document["document_id"]
        text = document.get("text") or ""
        language = document.get("language")
        media = document.get("media") or {}
        date = document.get("date")
        year = parse_year(date)
        doc_text_len = len(text)
        ocr_score = compute_ocr_score(text, language) if cell.dataset == "impresso" else None

        for pair in document.get("sampled_pairs", []) or []:
            stats["n_pairs"] += 1

            key = (document_id, pair.get("pers_entity_id"), pair.get("loc_entity_id"))
            ens_at = at_map.get(key)
            if ens_at is not None:
                stats["n_ensemble_at_matched"] += 1
            ens_isAt = isAt_map.get(key) if isAt_map is not None else None
            if isAt_map is not None and ens_isAt is not None:
                stats["n_ensemble_isAt_matched"] += 1

            pers_qid = pair.get("pers_wikidata_QID")
            loc_qid = pair.get("loc_wikidata_QID")
            pers_mentions = pair.get("pers_mentions_list") or []
            loc_mentions = pair.get("loc_mentions_list") or []

            person_spans = [span for mention in pers_mentions for span in find_occurrences(text, mention)]
            loc_spans = [span for mention in loc_mentions for span in find_occurrences(text, mention)]
            distance = min_char_distance(person_spans, loc_spans)
            if distance is None:
                stats["n_offset_unmatched"] += 1
                match_status = "unmatched"
            else:
                stats["n_offset_matched"] += 1
                match_status = "matched"

            rows.append(
                {
                    "track": track,
                    "dataset": cell.dataset,
                    "split": cell.split,
                    "language": cell.language,
                    "document_id": document_id,
                    "pers_entity_id": pair.get("pers_entity_id"),
                    "loc_entity_id": pair.get("loc_entity_id"),
                    "pers_wikidata_QID": pers_qid,
                    "loc_wikidata_QID": loc_qid,
                    "pers_qid_linked": pers_qid is not None,
                    "loc_qid_linked": loc_qid is not None,
                    "pers_mentions_list": list(pers_mentions),
                    "loc_mentions_list": list(loc_mentions),
                    "gold_at": pair.get("at"),
                    "gold_isAt": pair.get("isAt"),
                    "top5_vote_at": ens_at["vote_at"] if ens_at else None,
                    "top5_correct_at": ens_at["correct_at"] if ens_at else None,
                    "top5_vote_isAt": ens_isAt["vote_isAt"] if ens_isAt else None,
                    "top5_correct_isAt": ens_isAt["correct_isAt"] if ens_isAt else None,
                    "date": date,
                    "year": year,
                    "media_source_type": media.get("source_type"),
                    "media_publication_title": media.get("publication_title"),
                    "media_time_period": media.get("time_period"),
                    "doc_text_len": doc_text_len,
                    "ocr_score": ocr_score,
                    "min_char_distance": distance,
                    "distance_match_status": match_status,
                }
            )

    return rows, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--ensemble-dir", type=Path, default=Path("results.d/ensemble"))
    parser.add_argument("--output", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    args = parser.parse_args()

    reference_paths = sorted(args.reference_dir.glob("*.jsonl"))
    if not reference_paths:
        print("[ERROR] No reference JSONL files found.", file=sys.stderr)
        return 1

    all_rows: list[dict[str, Any]] = []
    all_stats: list[dict[str, Any]] = []
    for reference_path in reference_paths:
        rows, stats = build_track_rows(reference_path, args.ensemble_dir)
        all_rows.extend(rows)
        all_stats.append(stats)
        print(
            f"[build_pair_features] {stats['track']}: "
            f"{stats['n_documents']} documents, {stats['n_pairs']} pairs | "
            f"top5-at joined: {stats['n_ensemble_at_matched']}/{stats['n_pairs']} | "
            f"top5-isAt joined: "
            + (
                f"{stats['n_ensemble_isAt_matched']}/{stats['n_pairs']}"
                if stats["n_isAt_available"]
                else "n/a (isAt not evaluated for this track)"
            )
            + f" | offsets matched: {stats['n_offset_matched']}/{stats['n_pairs']} "
            f"({stats['n_offset_unmatched']} unmatched, "
            f"{stats['n_offset_unmatched'] / stats['n_pairs']:.1%})"
        )

    df = pd.DataFrame(all_rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.output, index=False)

    print(f"[build_pair_features] Total rows: {len(df)}")
    print(f"[build_pair_features] Written: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
