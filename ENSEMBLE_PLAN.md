# Ensemble Analysis Plan

## Goal

For every candidate pair evaluated in the competition, aggregate the predictions of
multiple system runs and compute:

1. **Label-distribution** — the percentage of systems (in a given ensemble) that
   predicted each label for that pair.
2. **Ensemble accuracy** — apply a plurality / majority vote across the ensemble and
   compare the aggregated prediction to the gold label.

Both the `at` task (ternary: TRUE / PROBABLE / FALSE, reported in the Test A tracks)
and the `isAt` task (binary: TRUE / FALSE, also in Test A) are covered. The
surprise-test-fr split is kept for the generalization (Test B) view.

---

## Ensemble Configurations

| ID  | Name               | Members                                                                                                                                                                                                                                                          |
| --- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (a) | **full-ensemble**  | Every system run in `results.d/diagnostics/`, excluding the `random` and `baseline` entries.                                                                                                                                                                     |
| (b) | **above-baseline** | Runs whose overall Test A score (from `ranking-overall-test-a.tsv`) is **strictly higher** than the `baseline` system (currently rank 17, score ≈ 0.5818). For Test B the analogous threshold in `ranking-generalization-test-b.tsv` is used (baseline rank 25). |
| (c) | **top-5**          | The 5 highest-scoring runs in `ranking-overall-test-a.tsv` (for Test A splits) and `ranking-generalization-test-b.tsv` (for the surprise-test-fr split).                                                                                                         |

> **Note on "best run per team"**: the configurations above operate at the _run_
> level (each submitted run counts once). If per-team aggregation is needed later,
> the script can be extended with a `--best-run-per-team` flag.

---

## Data Sources

| Source                                                        | Role                                                                                                                  |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `results.d/diagnostics/{run}.diagnostics.json`                | Per-document, per-pair predictions (`SYS_at`, `SYS_isAt`) and gold labels (`at`, `isAt`). One file per submitted run. |
| `results.d/system-rankings/ranking-overall-test-a.tsv`        | Ordered list of all runs with overall Test A scores → used to define ensembles (b) and (c).                           |
| `results.d/system-rankings/ranking-generalization-test-b.tsv` | Same for Test B (surprise-test-fr).                                                                                   |

The gold labels are already embedded inside each diagnostics file, so no separate
reference file needs to be loaded.

---

## Candidate-Pair Key

Each pair is uniquely identified by the triple:

```
(document_id, pers_entity_id, loc_entity_id)
```

This matches the logic in `lib/build_diagnostics.py` (`pair_key` function).

---

## Algorithm

```
for each (split, language) track:
    1. Identify the set of diagnostic files for that track.
    2. For each file, iterate over all documents and their sampled_pairs.
       Build a dict:
         pair_db[(doc_id, pers_id, loc_id)] = {
             "gold_at":   <str>,
             "gold_isAt": <str>,
             "predictions": [
                 {"run": "<team>_run<n>", "SYS_at": <str>, "SYS_isAt": <str>},
                 ...
             ]
         }
    3. For each ensemble config, filter `predictions` to the eligible runs.
    4. Per pair, compute label distributions:
         dist_at   = {label: count/N for label in [TRUE, PROBABLE, FALSE]}
         dist_isAt = {label: count/N for label in [TRUE, FALSE]}
    5. Plurality vote (most-voted label; ties broken alphabetically):
         vote_at   = argmax(dist_at)
         vote_isAt = argmax(dist_isAt)
    6. Accuracy across all pairs in the track:
         acc_at   = mean(vote_at   == gold_at)
         acc_isAt = mean(vote_isAt == gold_isAt)
```

Aggregate label distribution at the track level (summing over all pairs) to produce
the "90 % TRUE / 5 % PROBABLE / 5 % FALSE"-style summary.

---

## Output Files

All outputs go into a new directory **`results.d/ensemble/`**.

### Per-track detail file

`results.d/ensemble/<split>-<language>.ensemble.json`

```json
{
  "track": "impresso-test-en",
  "ensembles": {
    "full": {
      "num_runs": 47,
      "pairs_count": 810,
      "at": {
        "aggregate_distribution": {"TRUE": 0.62, "PROBABLE": 0.14, "FALSE": 0.24},
        "accuracy": 0.71,
        "pairs": [
          {
            "document_id": "...",
            "pers_entity_id": "...",
            "loc_entity_id": "...",
            "gold_at": "TRUE",
            "vote_at": "TRUE",
            "dist_at": {"TRUE": 0.85, "PROBABLE": 0.09, "FALSE": 0.06}
          }
        ]
      },
      "isAt": { "..." }
    },
    "above_baseline": { "..." },
    "top5":           { "..." }
  }
}
```

### Summary table

`results.d/ensemble/ensemble_summary.tsv`

Columns: `ensemble | track | task | accuracy | pct_TRUE | pct_PROBABLE | pct_FALSE | num_runs | num_pairs`

This is the human-readable table that directly answers questions like
"for the top-5 ensemble on impresso-test-en, 90 % of predictions were TRUE".

---

## New Script: `lib/build_ensemble_analysis.py`

### Invocation

```bash
python3 lib/build_ensemble_analysis.py \
    --diagnostics-dir  results.d/diagnostics \
    --rankings-dir     results.d/system-rankings \
    --output-dir       results.d/ensemble
```

### Key flags

| Flag                | Default                     | Description                                    |
| ------------------- | --------------------------- | ---------------------------------------------- |
| `--diagnostics-dir` | `results.d/diagnostics`     | Directory with `*.diagnostics.json` files      |
| `--rankings-dir`    | `results.d/system-rankings` | Directory with ranking TSVs                    |
| `--output-dir`      | `results.d/ensemble`        | Where to write outputs                         |
| `--top-n`           | `5`                         | How many runs to include in the top-N ensemble |

### Dependencies

Only standard library + modules already imported across the project (`json`, `pathlib`,
`csv`, `collections`). No new packages required.

---

## Makefile Target

Add to `Makefile`:

```make
ensemble: results.d/ensemble/ensemble_summary.tsv

results.d/ensemble/ensemble_summary.tsv: \
        $(wildcard results.d/diagnostics/*.diagnostics.json) \
        results.d/system-rankings/ranking-overall-test-a.tsv \
        results.d/system-rankings/ranking-generalization-test-b.tsv
	python3 lib/build_ensemble_analysis.py \
	    --diagnostics-dir  results.d/diagnostics \
	    --rankings-dir     results.d/system-rankings \
	    --output-dir       results.d/ensemble
```

---

## Scope / Out-of-Scope

**In scope**

- Test A accuracy metrics: `at_accuracy` and `isAt_accuracy` for impresso-test-de/en/fr.
- Test B accuracy metric for surprise-test-fr.
- Label-distribution percentages per ensemble config.

**Out of scope** (not changed by this plan)

- Existing per-run diagnostic metrics files.
- Existing ranking TSVs.
- F1 / precision / recall — the ensemble script reports accuracy only (matching the
  user request).
- Binary (`results-binary.d/`) track — excluded for now; can be added later by
  pointing at the binary diagnostics directory.
