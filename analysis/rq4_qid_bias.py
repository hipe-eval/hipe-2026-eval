#!/usr/bin/env python3
"""RQ4: does QID-linkage (vs. NIL) affect accuracy, and does it differ by system?

Three-way comparison: `baseline` (HIPE-Ministral-Baseline, single run per track),
`team1`'s ("Awakened") best-ranked run per test group, and the top5 ensemble. Each
split by QID-linked vs. NIL, separately for the person entity and the location entity.

NOTE per ANALYSIS_PLAN.md §7 approval: the table/figure below are the full computation,
but the interpretive framing of what QID/NIL exposure means for the baseline (whether
its prompt template actually receives pers_wikidata_QID/loc_wikidata_QID, or whether the
field identity observed between baseline predictions and the reference is coincidental)
is NOT confirmed and is deliberately NOT asserted here or anywhere in this script's
output — that write-up language is on hold pending confirmation from whoever generated
the HIPE-Ministral-Baseline submissions.

Reads analysis.d/tables/pair_level_features.parquet, results.d/system-rankings/*.tsv,
and results.d/diagnostics/{baseline,team1}_*.diagnostics.json (all read-only). Writes:
  analysis.d/tables/rq4_qid_bias.tsv
  analysis.d/figures/rq4_qid_bias.pdf
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from common import parse_reference_filename  # noqa: E402

from plotting_common import COLOR_AT, COLOR_ISAT, grouped_bar, new_figure, save_figure, style_axis

BASELINE_TEAM = "baseline"
COMPARISON_TEAM = "team1"
SYSTEM_ORDER = ["baseline", "team1_best", "top5_ensemble"]

TRACK_TEST_GROUP = {
    "impresso-test-de": "test_a",
    "impresso-test-en": "test_a",
    "impresso-test-fr": "test_a",
    "surprise-test-fr": "test_b",
}
RANKING_FILE_FOR_GROUP = {
    "test_a": "ranking-overall-test-a.tsv",
    "test_b": "ranking-generalization-test-b.tsv",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def best_run_for_team(ranking_path: Path, team: str) -> str | None:
    rows = [row for row in read_tsv(ranking_path) if row["team"] == team]
    if not rows:
        return None
    rows.sort(key=lambda row: int(row["rank"]))
    return rows[0]["run"]


def reference_tracks(reference_dir: Path) -> dict[str, str]:
    """Map track id -> reference stem (filename minus .jsonl), for building diagnostics filenames."""
    tracks = {}
    for path in sorted(reference_dir.glob("*.jsonl")):
        cell = parse_reference_filename(path.name)
        track = f"{cell.dataset}-{cell.split}-{cell.language}"
        tracks[track] = path.stem
    return tracks


def load_diagnostics_correctness(path: Path) -> dict[tuple, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    result = {}
    for document in payload:
        document_id = document["document_id"]
        for pair in document.get("sampled_pairs", []) or []:
            key = (document_id, pair.get("pers_entity_id"), pair.get("loc_entity_id"))
            result[key] = {
                "correct_at": pair.get("CORRECT_at"),
                "correct_isAt": pair.get("CORRECT_isAt"),
            }
    return result


def macro_recall(df: pd.DataFrame, gold_col: str, correct_col: str) -> tuple[float | None, int]:
    sub = df.dropna(subset=[correct_col])
    if sub.empty:
        return None, 0
    recalls = [group[correct_col].mean() for _, group in sub.groupby(gold_col, observed=True)]
    return (sum(recalls) / len(recalls) if recalls else None), len(sub)


def accuracy(df: pd.DataFrame, correct_col: str) -> tuple[float | None, int]:
    sub = df.dropna(subset=[correct_col])
    if sub.empty:
        return None, 0
    return sub[correct_col].mean(), len(sub)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, default=Path("analysis.d/tables/pair_level_features.parquet"))
    parser.add_argument("--reference-dir", type=Path, default=Path("data/reference"))
    parser.add_argument("--diagnostics-dir", type=Path, default=Path("results.d/diagnostics"))
    parser.add_argument("--rankings-dir", type=Path, default=Path("results.d/system-rankings"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis.d"))
    args = parser.parse_args()

    df = pd.read_parquet(args.features)
    tracks = reference_tracks(args.reference_dir)

    best_run_by_group = {}
    for group, ranking_file in RANKING_FILE_FOR_GROUP.items():
        ranking_path = args.rankings_dir / ranking_file
        run = best_run_for_team(ranking_path, COMPARISON_TEAM)
        best_run_by_group[group] = run
        print(f"[RQ4] {COMPARISON_TEAM}'s best run for {group} ({ranking_file}): {run}")

    baseline_correctness: dict[tuple, dict[str, Any]] = {}
    team1_correctness: dict[tuple, dict[str, Any]] = {}
    for track, stem in tracks.items():
        group = TRACK_TEST_GROUP[track]

        baseline_path = args.diagnostics_dir / f"{BASELINE_TEAM}_{stem}_run1.diagnostics.json"
        if baseline_path.is_file():
            baseline_correctness.update(load_diagnostics_correctness(baseline_path))
        else:
            print(f"[RQ4][WARN] Missing baseline diagnostics for {track}: {baseline_path}")

        team1_run = best_run_by_group.get(group)
        if team1_run is None:
            print(f"[RQ4][WARN] {COMPARISON_TEAM} has no ranked run for group {group} ({track}) — skipping.")
            continue
        team1_path = args.diagnostics_dir / f"{COMPARISON_TEAM}_{stem}_{team1_run}.diagnostics.json"
        if team1_path.is_file():
            team1_correctness.update(load_diagnostics_correctness(team1_path))
        else:
            print(f"[RQ4][WARN] Missing {COMPARISON_TEAM} diagnostics for {track}: {team1_path}")

    def lookup(row, table, field):
        entry = table.get((row["document_id"], row["pers_entity_id"], row["loc_entity_id"]))
        return entry[field] if entry else None

    df["baseline_correct_at"] = df.apply(lambda row: lookup(row, baseline_correctness, "correct_at"), axis=1)
    df["baseline_correct_isAt"] = df.apply(lambda row: lookup(row, baseline_correctness, "correct_isAt"), axis=1)
    df["team1_correct_at"] = df.apply(lambda row: lookup(row, team1_correctness, "correct_at"), axis=1)
    df["team1_correct_isAt"] = df.apply(lambda row: lookup(row, team1_correctness, "correct_isAt"), axis=1)

    system_cols = {
        "baseline": {"at": "baseline_correct_at", "isAt": "baseline_correct_isAt"},
        "team1_best": {"at": "team1_correct_at", "isAt": "team1_correct_isAt"},
        "top5_ensemble": {"at": "top5_correct_at", "isAt": "top5_correct_isAt"},
    }
    entity_cols = {"person": "pers_qid_linked", "location": "loc_qid_linked"}

    result_rows = []
    for entity_type, qid_col in entity_cols.items():
        for qid_status, flag in [("linked", True), ("NIL", False)]:
            subset = df[df[qid_col] == flag]
            for system, task_cols in system_cols.items():
                for task, correct_col in task_cols.items():
                    task_subset = subset if task == "at" else subset[subset["dataset"] == "impresso"]
                    gold_col = "gold_at" if task == "at" else "gold_isAt"
                    recall, recall_n = macro_recall(task_subset, gold_col, correct_col)
                    acc, acc_n = accuracy(task_subset, correct_col)
                    result_rows.append(
                        {
                            "system": system,
                            "entity_type": entity_type,
                            "qid_status": qid_status,
                            "task": task,
                            "macro_recall": recall,
                            "accuracy": acc,
                            "n": acc_n,
                        }
                    )

    result_table = pd.DataFrame(result_rows)

    tables_dir = args.output_dir / "tables"
    figures_dir = args.output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    result_table.to_csv(tables_dir / "rq4_qid_bias.tsv", sep="\t", index=False)

    # Figure: `at` task only, one panel per entity type, bars = linked vs NIL per system.
    # Reuses the same two-color pair used for at/isAt elsewhere, repurposed here for the
    # linked/NIL split (this chart doesn't itself contrast at vs isAt).
    fig, axes = new_figure(ncols=2)
    for ax, entity_type in zip(axes, entity_cols):
        panel = result_table[(result_table["entity_type"] == entity_type) & (result_table["task"] == "at")]
        pivot_recall = panel.pivot(index="system", columns="qid_status", values="macro_recall").reindex(SYSTEM_ORDER)
        pivot_n = panel.pivot(index="system", columns="qid_status", values="n").reindex(SYSTEM_ORDER)
        grouped_bar(
            ax,
            SYSTEM_ORDER,
            {"linked": list(pivot_recall["linked"]), "NIL": list(pivot_recall["NIL"])},
            colors={"linked": COLOR_AT, "NIL": COLOR_ISAT},
            ns={"linked": list(pivot_n["linked"]), "NIL": list(pivot_n["NIL"])},
        )
        style_axis(ax)
        ax.set_title(f"{entity_type.title()} entity (at)", fontsize=7)
    save_figure(fig, figures_dir / "rq4_qid_bias.pdf")

    print(f"[RQ4] baseline pairs matched: {len(baseline_correctness)} | {COMPARISON_TEAM} pairs matched: {len(team1_correctness)}")
    print(result_table.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
