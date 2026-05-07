# HIPE-2026 Evaluation Campaign Implementation Plan

This plan describes how to turn this parent repository into the organizer-side evaluation campaign repository for HIPE-2026. The implementation should be done from this parent directory, not from inside the `HIPE-2026-data/` submodule.

## Goal

Build an evaluation orchestration repository analogous to `eval-template-repo/`, adapted to the HIPE-2026 person-place relation extraction task. The repository should validate submissions, score submitted runs against official references, aggregate scores into rankings, and render a final results Markdown page.

The implementation should avoid a dummy/parallel evaluation pipeline. Only the real campaign pipeline is needed.

## Key Constraints

- Reuse `HIPE-2026-data/` code wherever possible. Do not duplicate schema loading, JSONL validation, missing-submission imputation, or core scoring utilities if they can be imported from the submodule.
- Keep the directory layout close to `eval-template-repo/` so future maintainers recognize the workflow.
- Orchestrate operational steps with Makefile targets. On macOS, run targets with `remake`.
- Test data/gold data is not yet open, so the pipeline must tolerate empty `data/reference/` and `data/systems/` directories and be easy to validate later with synthetic or released files.

## Proposed Layout

```text
data/
  reference/              # Flat organizer-side gold JSONL copies, added when available
  systems/                # Participant submission JSONL files and matching *-info.json files
lib/
  score_one.py            # Score one submission file against matching reference
  validate_jsonl.py       # Validate JSONL files against HIPE-2026 schema
  build_rankings.py       # Build TSV rankings from per-run score JSON
  build_results_md.py     # Render final results Markdown from ranking TSVs
  competition_config.json # Evaluation cells and weights
  teams.json              # Optional team ID -> affiliation metadata
results.d/
  per-run/                # Generated per-run JSON scores and logs
  system-rankings/        # Generated ranking TSV files
HIPE_2026_evaluation_results.md # Generated final results page
Makefile
requirements.txt
README.md
AGENT.md
PLAN.md
```

## Data and Filename Assumptions

Reference files should be copied into `data/reference/` as a flat set of JSONL files,
without preserving the `HIPE-2026-data/data/.../vX.Y/` subdirectories. They should
use the released official input/reference stems, for example:

```text
HIPE-2026-v1.0-impresso-test-de.jsonl
HIPE-2026-v1.0-impresso-test-en.jsonl
HIPE-2026-v1.0-impresso-test-fr.jsonl
HIPE-2026-v1.0-surprise-test-fr.jsonl
```

System submissions should follow the guideline pattern:

```text
teamN_<reference-stem>_runX.jsonl
```

Examples:

```text
team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-en_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl
team1_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl
```

Team identifiers are expected to be numerical names such as `team1`, `team2`,
and so on. `score_one.py` should derive the reference filename by removing the
team prefix and trailing `_runX` suffix.

For every submitted run JSONL file, the systems directory may contain a sibling
metadata file:

```text
teamN_<reference-stem>_runX-info.json
```

The expected metadata keys are:

```json
{
  "hipe_parameter_count": 0,
  "team_parameter_count": 0,
  "hipe_model_size": 0,
  "team_model_size": 0
}
```

`hipe_*` values are the organizers' comparable estimates. `team_*` values are
what participants reported. Efficiency ranking should use `hipe_parameter_count`
and `hipe_model_size`, both numeric. Model size is assumed to be in MB, but only
relative ordering matters for ranking. The raw `team_*` values should be
preserved in per-run JSON and results tables for transparency, even when they
are not used directly for the ranking.

The submission directory is expected to respect the run limit of no more than
three runs per team and reference language file. Validation should detect and
fail on excess runs.

## Scoring Design

Use the existing `HIPE-2026-data/scripts` code as the core scoring basis:

- `check_jsonlschema.py` for schema loading and validation behavior.
- `evaluation_utils.py` for JSONL loading, reshaping sampled pairs, imputing missing submission data, flattening predictions, and metric calculation where applicable.

The parent repo wrapper should produce template-style JSON outputs under `results.d/per-run/`, for example:

```json
{
  "submission": "team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl",
  "reference": "HIPE-2026-v1.0-impresso-test-de.jsonl",
  "team": "team1",
  "dataset": "impresso",
  "split": "test",
  "language": "de",
  "run": "run1",
  "profile": "accuracy",
  "scores": {
    "at_macro_recall": 0.0,
    "isAt_macro_recall": 0.0,
    "global_score": 0.0
  },
  "efficiency_metadata": {
    "info_file": "team1_HIPE-2026-v1.0-impresso-test-de_run1-info.json",
    "hipe_parameter_count": 0,
    "team_parameter_count": 0,
    "hipe_model_size": 0,
    "team_model_size": 0,
    "info_missing": false
  },
  "counts": {
    "at_total": 0,
    "isAt_total": 0
  }
}
```

For Test A (`impresso`), score both `at` and `isAt` and compute:

```text
global_score = (MacroRecall_at + MacroRecall_isAt) / 2
```

For Test B (`surprise`), score only `at` for the generalization profile.

Missing documents, missing sampled pairs, and remaining `null` labels should be treated as `FALSE`, matching the guidelines and existing data-submodule behavior.

## Ranking Design

`build_rankings.py` should read `results.d/per-run/*.json` and write TSV files under `results.d/system-rankings/`. Ranking should be descending because higher macro recall/global score is better.

Recommended outputs:

```text
ranking-impresso-test-de.tsv
ranking-impresso-test-en.tsv
ranking-impresso-test-fr.tsv
ranking-surprise-test-fr.tsv
ranking-overall-test-a.tsv
ranking-generalization-test-b.tsv
ranking-efficiency-test-a.tsv
```

For Test A, overall ranking should combine the three `impresso` language files. A simple unweighted mean across available language-level `global_score` values is the conservative first implementation unless the official campaign later defines different weights.

For Test B, rank systems by `at_macro_recall` on the surprise dataset.

Efficiency ranking should follow the formula documented in `GUIDELINES.md`:

```text
R(system) = (rank_accuracy + rank_parameter_count + rank_model_size) / 3
```

Systems are ordered by increasing `R(system)`. Higher accuracy is better; lower
`hipe_parameter_count` and lower `hipe_model_size` are better. Ties should
receive the same rank. Missing `*-info.json` must not fail efficiency
evaluation, but the affected run should be assigned the last rank for both
parameter count and model size. Accuracy/generalization scoring should remain
independent of whether the info file is present.

## Makefile Targets

The parent Makefile should provide:

```text
install
validate-reference
validate-submissions
validate-info
score
rankings
results-md
eval-full
eval-full-refresh
clean
help
```

Suggested default variables:

```make
PYTHON ?= venv/bin/python
DATA_REPO ?= HIPE-2026-data
SCHEMA_PATH ?= $(DATA_REPO)/schemas/hipe-2026-data.schema.json
REFERENCE_DIR ?= data/reference
SUBMISSIONS_DIR ?= data/systems
RESULTS_DIR ?= results.d
PER_RUN_DIR := $(RESULTS_DIR)/per-run
RANKINGS_DIR := $(RESULTS_DIR)/system-rankings
DIAGNOSTICS_DIR := $(RESULTS_DIR)/diagnostics
RESULTS_MD := HIPE_2026_evaluation_results.md
```

`eval-full` should run:

```text
validate-submissions -> validate-info -> score -> rankings -> results-md
```

`eval-full-refresh` should remove derived outputs first, then run `eval-full`.

## Implementation Sequence

1. Create `requirements.txt` in the parent repo with the dependencies needed for the orchestration scripts. At minimum this should include the data-submodule requirements, currently `jsonschema` and `scikit-learn`.
2. Create the directory skeleton: `data/reference/`, `data/systems/`, `lib/`, and optionally `.gitkeep` files.
3. Implement `lib/validate_jsonl.py` as a thin wrapper around schema validation. Prefer importing from `HIPE-2026-data/scripts/check_jsonlschema.py` when possible.
4. Implement `lib/score_one.py` as a wrapper around `HIPE-2026-data/scripts/evaluation_utils.py`.
5. Implement `lib/validate_info.py` to validate run metadata files, enforce the
   three-run-per-team/per-reference limit, and report missing info files without
   blocking score generation.
6. Implement `lib/build_rankings.py` to aggregate per-run JSON into TSVs,
   including accuracy, generalization, and efficiency rankings.
7. Implement `lib/build_results_md.py` to render rankings and team metadata into `HIPE_2026_evaluation_results.md`.
8. Add `lib/competition_config.json` with official cells for `impresso` de/en/fr and `surprise` fr.
9. Add `lib/teams.json` as an initially empty object.
10. Add the parent `Makefile`.
11. Run syntax checks with `python3 -m py_compile lib/*.py`.
12. Do not run behavioral smoke tests yet. Until the evaluation setup is ready
    for test execution, restrict verification to syntactic checks.

## Open Decisions

- Confirm final reference filenames once test gold data is released.
- Confirm official weighting for Test A overall ranking. The first implementation can use unweighted language averages.
- Confirm whether generated `HIPE_2026_evaluation_results.md` should be committed after official evaluation or treated as fully generated until publication.
