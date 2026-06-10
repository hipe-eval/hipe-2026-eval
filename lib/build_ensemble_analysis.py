#!/usr/bin/env python3
"""Build ensemble analysis for HIPE-2026.

For every candidate pair in the diagnostics files, aggregate the predictions of
multiple system runs and compute:
  - label-distribution percentages (TRUE / PROBABLE / FALSE for 'at';
    TRUE / FALSE for 'isAt')
  - ensemble accuracy via plurality vote

Three ensemble configurations are produced:
  (a) full     – every team run (baseline and random excluded)
  (b) above_baseline – runs ranked strictly above the baseline system
  (c) top5     – the 5 highest-scoring runs

Usage::
    python3 lib/build_ensemble_analysis.py \
        --diagnostics-dir  results.d/diagnostics \
        --rankings-dir     results.d/system-rankings \
        --output-dir       results.d/ensemble

Outputs written to --output-dir:
  <track>.ensemble.json         per-pair detail
  ensemble_summary.tsv          compact summary table
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Map internal track id → test group (determines which ranking file to use)
TRACK_GROUP: dict[str, str] = {
    "impresso-test-de": "test_a",
    "impresso-test-en": "test_a",
    "impresso-test-fr": "test_a",
    "surprise-test-fr": "test_b",
}

RANKING_FILE: dict[str, str] = {
    "test_a": "ranking-overall-test-a.tsv",
    "test_b": "ranking-generalization-test-b.tsv",
}

AT_LABELS = ["TRUE", "PROBABLE", "FALSE"]
ISAT_LABELS = ["TRUE", "FALSE"]

# Regex to parse diagnostic filenames such as
#   team8_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json
# Reference stems like HIPE-2026-v1.0-impresso-test-en contain no underscores,
# so the track is derived from the ref group after stripping the version prefix.
DIAG_RE = re.compile(
    r"^(?P<team>[^_]+)_(?P<ref>HIPE-2026-[^_]+)_(?P<run>run\d+)\.diagnostics\.json$"
)
VERSION_PREFIX_RE = re.compile(r"^HIPE-2026-v[\d.]+-")

TOP_N = 5
EXCLUDE_TEAMS = {"baseline", "random"}

# Tracks that include the isAt (binary) subtask.
TRACKS_WITH_ISAT = {"impresso-test-de", "impresso-test-en", "impresso-test-fr"}


# ---------------------------------------------------------------------------
# Ranking helpers
# ---------------------------------------------------------------------------

def load_ranking(path: Path) -> list[dict[str, str]]:
    """Return rows from a TSV ranking file as dicts."""
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def baseline_score(rows: list[dict[str, str]]) -> float:
    """Return the score of the 'baseline' entry in the ranking."""
    for row in rows:
        if row["team"] == "baseline":
            return float(row["score"])
    raise ValueError("No 'baseline' row found in ranking.")


def above_baseline_runs(rows: list[dict[str, str]]) -> set[tuple[str, str]]:
    """Return (team, run) pairs with score strictly above the baseline."""
    threshold = baseline_score(rows)
    result: set[tuple[str, str]] = set()
    for row in rows:
        if row["team"] in EXCLUDE_TEAMS:
            continue
        if float(row["score"]) > threshold:
            result.add((row["team"], row["run"]))
    return result


def top_n_runs(rows: list[dict[str, str]], n: int = TOP_N) -> set[tuple[str, str]]:
    """Return (team, run) pairs for the top-N eligible entries."""
    eligible = [r for r in rows if r["team"] not in EXCLUDE_TEAMS]
    # Rows are already sorted by rank (ascending) in the files.
    result: set[tuple[str, str]] = set()
    for row in eligible[:n]:
        result.add((row["team"], row["run"]))
    return result


# ---------------------------------------------------------------------------
# Diagnostics loading
# ---------------------------------------------------------------------------

def load_diagnostics(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Core aggregation
# ---------------------------------------------------------------------------

PairKey = tuple[str, str, str]  # (document_id, pers_entity_id, loc_entity_id)


def build_pair_db(
    diag_files: list[tuple[str, str, Path]],  # [(team, run, path), ...]
) -> dict[PairKey, dict[str, Any]]:
    """
    Collect every run's predictions for every pair.

    Returns a dict keyed by (document_id, pers_entity_id, loc_entity_id).
    Each value holds the gold labels and a list of per-run predictions.
    """
    db: dict[PairKey, dict[str, Any]] = {}

    for team, run, path in diag_files:
        docs = load_diagnostics(path)
        for doc in docs:
            doc_id: str = doc["document_id"]
            for pair in doc.get("sampled_pairs", []):
                key: PairKey = (
                    doc_id,
                    pair.get("pers_entity_id", ""),
                    pair.get("loc_entity_id", ""),
                )
                if key not in db:
                    db[key] = {
                        "document_id": doc_id,
                        "pers_entity_id": pair.get("pers_entity_id"),
                        "loc_entity_id": pair.get("loc_entity_id"),
                        "gold_at": pair.get("at"),
                        "gold_isAt": pair.get("isAt"),
                        "predictions": [],
                    }
                db[key]["predictions"].append(
                    {
                        "run": f"{team}_{run}",
                        "SYS_at": pair.get("SYS_at"),
                        "SYS_isAt": pair.get("SYS_isAt"),
                    }
                )

    return db


def plurality_vote(counts: Counter) -> str | None:
    """Return the label with the highest count; ties broken alphabetically."""
    if not counts:
        return None
    max_count = max(counts.values())
    candidates = sorted(k for k, v in counts.items() if v == max_count)
    return candidates[0]


def aggregate_ensemble(
    db: dict[PairKey, dict[str, Any]],
    eligible_runs: set[str] | None,  # None → use all runs
    include_isat: bool = True,
) -> dict[str, Any]:
    """
    Compute per-pair distributions and plurality votes for a single ensemble.

    `eligible_runs` is a set of 'team_run' strings (e.g. 'team8_run1').
    Pass None to include every run in db.
    """
    pairs_at: list[dict[str, Any]] = []
    pairs_isAt: list[dict[str, Any]] = []

    total_correct_at = 0
    total_correct_isAt = 0
    count_at = 0
    count_isAt = 0

    # accumulators for aggregate label distributions
    agg_at: Counter = Counter()
    agg_isAt: Counter = Counter()
    total_votes_at = 0
    total_votes_isAt = 0

    # per-label TP and support for macro recall
    tp_at: Counter = Counter()
    support_at: Counter = Counter()
    tp_isAt: Counter = Counter()
    support_isAt: Counter = Counter()

    for key, entry in db.items():
        predictions = entry["predictions"]
        if eligible_runs is not None:
            predictions = [p for p in predictions if p["run"] in eligible_runs]
        if not predictions:
            continue

        gold_at = entry["gold_at"]
        gold_isAt = entry["gold_isAt"]

        # --- at ---
        at_counts: Counter = Counter(
            p["SYS_at"] for p in predictions if p["SYS_at"] is not None
        )
        n_at = sum(at_counts.values())
        dist_at = {lbl: round(at_counts.get(lbl, 0) / n_at, 6) if n_at else 0.0 for lbl in AT_LABELS}
        vote_at = plurality_vote(at_counts)
        agg_at.update(at_counts)
        total_votes_at += n_at

        if gold_at is not None and vote_at is not None:
            correct_at = int(vote_at == gold_at)
            total_correct_at += correct_at
            count_at += 1
            support_at[gold_at] += 1
            tp_at[gold_at] += correct_at
            pairs_at.append(
                {
                    "document_id": entry["document_id"],
                    "pers_entity_id": entry["pers_entity_id"],
                    "loc_entity_id": entry["loc_entity_id"],
                    "gold_at": gold_at,
                    "vote_at": vote_at,
                    "correct_at": bool(correct_at),
                    "dist_at": dist_at,
                    "num_predictions": n_at,
                }
            )

        # --- isAt ---
        if include_isat:
            isAt_counts: Counter = Counter(
                p["SYS_isAt"] for p in predictions if p["SYS_isAt"] is not None
            )
            n_isAt = sum(isAt_counts.values())
            dist_isAt = {lbl: round(isAt_counts.get(lbl, 0) / n_isAt, 6) if n_isAt else 0.0 for lbl in ISAT_LABELS}
            vote_isAt = plurality_vote(isAt_counts)
            agg_isAt.update(isAt_counts)
            total_votes_isAt += n_isAt

            if gold_isAt is not None and vote_isAt is not None:
                correct_isAt = int(vote_isAt == gold_isAt)
                total_correct_isAt += correct_isAt
                count_isAt += 1
                support_isAt[gold_isAt] += 1
                tp_isAt[gold_isAt] += correct_isAt
                pairs_isAt.append(
                    {
                        "document_id": entry["document_id"],
                        "pers_entity_id": entry["pers_entity_id"],
                        "loc_entity_id": entry["loc_entity_id"],
                        "gold_isAt": gold_isAt,
                        "vote_isAt": vote_isAt,
                        "correct_isAt": bool(correct_isAt),
                        "dist_isAt": dist_isAt,
                        "num_predictions": n_isAt,
                    }
                )

    # aggregate label distribution (% of all predictions across all pairs)
    agg_dist_at = {
        lbl: round(agg_at.get(lbl, 0) / total_votes_at, 6) if total_votes_at else 0.0
        for lbl in AT_LABELS
    }
    agg_dist_isAt = {
        lbl: round(agg_isAt.get(lbl, 0) / total_votes_isAt, 6) if total_votes_isAt else 0.0
        for lbl in ISAT_LABELS
    }

    acc_at = round(total_correct_at / count_at, 6) if count_at else None
    acc_isAt = round(total_correct_isAt / count_isAt, 6) if count_isAt else None

    # macro recall: mean of per-label recall over labels that appear in gold
    def _macro_recall(tp: Counter, support: Counter, labels: list[str]) -> float | None:
        recalls = [tp[lbl] / support[lbl] for lbl in labels if support[lbl] > 0]
        return round(sum(recalls) / len(recalls), 6) if recalls else None

    macro_recall_at = _macro_recall(tp_at, support_at, AT_LABELS)
    macro_recall_isAt = _macro_recall(tp_isAt, support_isAt, ISAT_LABELS) if include_isat else None

    result: dict[str, Any] = {
        "num_runs": len(eligible_runs) if eligible_runs is not None else None,
        "pairs_count": len(db),
        "at": {
            "aggregate_distribution": agg_dist_at,
            "accuracy": acc_at,
            "macro_recall": macro_recall_at,
            "pairs": pairs_at,
        },
    }
    if include_isat:
        result["isAt"] = {
            "aggregate_distribution": agg_dist_isAt,
            "accuracy": acc_isAt,
            "macro_recall": macro_recall_isAt,
            "pairs": pairs_isAt,
        }
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--diagnostics-dir",
        default="results.d/diagnostics",
        type=Path,
        help="Directory containing *.diagnostics.json files.",
    )
    p.add_argument(
        "--rankings-dir",
        default="results.d/system-rankings",
        type=Path,
        help="Directory containing ranking TSV files.",
    )
    p.add_argument(
        "--output-dir",
        default="results.d/ensemble",
        type=Path,
        help="Output directory.",
    )
    p.add_argument(
        "--top-n",
        default=TOP_N,
        type=int,
        help=f"Number of runs in the top-N ensemble (default: {TOP_N}).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    diag_dir: Path = args.diagnostics_dir
    rankings_dir: Path = args.rankings_dir
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Load rankings for each test group
    # ------------------------------------------------------------------
    rankings: dict[str, list[dict[str, str]]] = {}
    for group, fname in RANKING_FILE.items():
        rankings[group] = load_ranking(rankings_dir / fname)

    # Pre-compute eligible-run sets from the Test-A overall ranking.
    # For Test-B (surprise-test-fr) the same logic applies to its ranking.
    ensemble_runs: dict[str, dict[str, set[str]]] = {}
    for group, rows in rankings.items():
        ab_pairs = above_baseline_runs(rows)
        top_pairs = top_n_runs(rows, args.top_n)
        ensemble_runs[group] = {
            "above_baseline": {f"{t}_{r}" for t, r in ab_pairs},
            "top5": {f"{t}_{r}" for t, r in top_pairs},
        }

    # ------------------------------------------------------------------
    # Group diagnostic files by track
    # ------------------------------------------------------------------
    track_files: dict[str, list[tuple[str, str, Path]]] = defaultdict(list)

    for fpath in sorted(diag_dir.glob("*.diagnostics.json")):
        m = DIAG_RE.match(fpath.name)
        if not m:
            continue
        team = m.group("team")
        run = m.group("run")
        ref = m.group("ref")
        # Derive track by stripping the version prefix, e.g.
        # HIPE-2026-v1.0-impresso-test-en → impresso-test-en
        track = VERSION_PREFIX_RE.sub("", ref)
        if team in EXCLUDE_TEAMS:
            continue
        if track not in TRACK_GROUP:
            continue
        track_files[track].append((team, run, fpath))

    # ------------------------------------------------------------------
    # Per-track processing
    # ------------------------------------------------------------------
    summary_rows: list[dict[str, Any]] = []

    for track, files in sorted(track_files.items()):
        group = TRACK_GROUP[track]
        all_runs = {f"{team}_{run}" for team, run, _ in files}
        has_isat = track in TRACKS_WITH_ISAT

        print(f"Track {track}: {len(files)} run files, {len(all_runs)} unique runs")

        # Build the full pair database from all files for this track
        db = build_pair_db(files)
        print(f"  Pairs: {len(db)}")

        ensembles: dict[str, Any] = {}

        # (a) full
        ensembles["full"] = aggregate_ensemble(db, eligible_runs=None, include_isat=has_isat)
        ensembles["full"]["num_runs"] = len(all_runs)

        # (b) above_baseline
        ab_runs = ensemble_runs[group]["above_baseline"] & all_runs
        ensembles["above_baseline"] = aggregate_ensemble(db, ab_runs, include_isat=has_isat)
        ensembles["above_baseline"]["num_runs"] = len(ab_runs)

        # (c) top5
        t5_runs = ensemble_runs[group]["top5"] & all_runs
        ensembles["top5"] = aggregate_ensemble(db, t5_runs, include_isat=has_isat)
        ensembles["top5"]["num_runs"] = len(t5_runs)

        # Print quick summary
        for ename, edata in ensembles.items():
            isat_str = (
                f"| isAt acc={edata['isAt']['accuracy']} dist={edata['isAt']['aggregate_distribution']}"
                if has_isat else ""
            )
            print(
                f"  [{ename:16s}] runs={edata['num_runs']:2d} "
                f"| at acc={edata['at']['accuracy']} dist={edata['at']['aggregate_distribution']} "
                + isat_str
            )

        # Write per-track JSON (pairs detail)
        out_json = output_dir / f"{track}.ensemble.json"
        out_json.write_text(
            json.dumps(
                {"track": track, "ensembles": ensembles},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"  Written: {out_json}")

        # Accumulate summary rows
        for ename, edata in ensembles.items():
            at_dist = edata["at"]["aggregate_distribution"]
            summary_rows.append(
                {
                    "ensemble": ename,
                    "track": track,
                    "task": "at",
                    "macro_recall": edata["at"]["macro_recall"],
                    "accuracy": edata["at"]["accuracy"],
                    "pct_TRUE": at_dist.get("TRUE"),
                    "pct_PROBABLE": at_dist.get("PROBABLE"),
                    "pct_FALSE": at_dist.get("FALSE"),
                    "num_runs": edata["num_runs"],
                    "num_pairs": len(edata["at"]["pairs"]),
                }
            )
            if has_isat:
                isAt_dist = edata["isAt"]["aggregate_distribution"]
                summary_rows.append(
                    {
                        "ensemble": ename,
                        "track": track,
                        "task": "isAt",
                        "macro_recall": edata["isAt"]["macro_recall"],
                        "accuracy": edata["isAt"]["accuracy"],
                        "pct_TRUE": isAt_dist.get("TRUE"),
                        "pct_PROBABLE": None,
                        "pct_FALSE": isAt_dist.get("FALSE"),
                        "num_runs": edata["num_runs"],
                        "num_pairs": len(edata["isAt"]["pairs"]),
                    }
                )

    # ------------------------------------------------------------------
    # Write summary TSV
    # ------------------------------------------------------------------
    summary_path = output_dir / "ensemble_summary.tsv"
    fieldnames = [
        "ensemble",
        "track",
        "task",
        "macro_recall",
        "accuracy",
        "pct_TRUE",
        "pct_PROBABLE",
        "pct_FALSE",
        "num_runs",
        "num_pairs",
    ]
    with summary_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"\nSummary written: {summary_path}")


if __name__ == "__main__":
    main()
