# HIPE-2026 Evaluation Campaign

This repository orchestrates the official evaluation campaign for CLEF HIPE-2026, the shared task on person-place relation extraction from multilingual historical documents.

It is intentionally structured like the evaluation template repository used for HIPE-OCRepair, but adapted to this task:

- no dummy or parallel baseline evaluation pipeline;
- reference/test data and participant submissions are evaluated through one real pipeline;
- scoring reuses the `HIPE-2026-data` submodule code instead of duplicating schema loading, JSONL parsing, missing-prediction imputation, and metric utilities;
- all evaluation actions are orchestrated through Makefile targets.

## Related Repositories

- HIPE-2026 website: <https://hipe-eval.github.io/HIPE-2026/>
- Data submodule: `HIPE-2026-data/`
- Guidelines summary: `GUIDELINES.md`
- Submission loading instructions: `SUBMISSIONS.md`
- Template reference: `eval-template-repo/`

## Planned Repository Layout

```text
data/
  reference/              # Flat gold reference JSONL copies, added when test data is open
  systems/                # Participant submission JSONL files and matching *-info.json files
lib/
  score_one.py            # Score one submitted run against the matching reference file
  validate_jsonl.py       # Validate reference/submission files against the HIPE-2026 schema
  build_rankings.py       # Aggregate per-run JSON scores into TSV rankings
  build_results_md.py     # Render ranking TSVs into a Markdown results page
  competition_config.json # Official evaluation cells and weights
  teams.json              # Team ID to affiliation metadata
results.d/                # Generated evaluation output, not hand-edited
  per-run/                # Per-submission JSON scores and logs
  system-rankings/        # Ranking TSV files
  diagnostics/            # Per-submission diagnostics JSON files
HIPE_2026_evaluation_results.md # Generated final results page
```

The `HIPE-2026-data/` submodule remains the source of truth for the task schema and core evaluation utilities.

## Local Workflow

Create a local environment from the parent repository:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On macOS, use `remake` instead of the system `make` when invoking targets:

```bash
remake help
remake validate-submissions
remake eval-full
```

The Makefile and documentation still refer to `make` as the command name where that is the conventional target runner.

## Evaluation Pipeline

The real pipeline will provide these targets:

```bash
remake validate-reference
remake validate-submissions
remake validate-info
remake score
remake rankings
remake diagnostics
remake results-md
remake eval-full
remake eval-full-refresh
```

`eval-full` validates submissions and info files, scores all submitted runs,
builds TSV rankings, writes diagnostics, and renders the results Markdown
document.

## Diagnostics

The `diagnostics` target writes two JSON files per submitted run under
`results.d/diagnostics/` by default. Override `RESULTS_DIR` to place all
generated outputs under another directory.

Document-level diagnostics:

```text
results.d/diagnostics/<submission-stem>.diagnostics.json
```

This file merges the reference labels and system predictions for every sampled
pair. It includes `SYS_at`, `SYS_isAt`, correctness flags, and any system
explanations from `at_explanation` and `isAt_explanation`.

Diagnostic metrics:

```text
results.d/diagnostics/<submission-stem>.diagnostic_metrics.json
```

This file contains micro-aggregated confusion matrices over all sampled pairs in
the corresponding reference file. Test A files include matrices for `at` and
`isAt`; surprise Test B files include `at` only. Each matrix uses fixed label
order, reports rows as gold labels and columns as predictions, and includes:

- a dense numeric `matrix`;
- a human-readable `table` with one row per gold label and `pred_*` columns;
- micro-aggregated accuracy;
- per-label precision, recall, and F1;
- per-label support, true positives, false positives, and false negatives.

## Data Status

The official test data is not yet open in this working copy. Until gold files are available, `data/reference/` is expected to be empty or organizer-populated only. The pipeline should remain runnable against whatever reference and system files are present.
