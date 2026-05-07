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
results/                  # Generated evaluation output, not hand-edited
  per-run/                # Per-submission JSON scores and logs
  system-rankings/        # Ranking TSV files
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
remake results-md
remake eval-full
remake eval-full-refresh
```

`eval-full` validates submissions and info files, scores all submitted runs, builds TSV rankings, and renders the results Markdown document.

## Data Status

The official test data is not yet open in this working copy. Until gold files are available, `data/reference/` is expected to be empty or organizer-populated only. The pipeline should remain runnable against whatever reference and system files are present.
