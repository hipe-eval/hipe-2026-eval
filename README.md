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

Clone the repository with its submodule:

```bash
git clone --recursive git@github.com:hipe-eval/hipe-2026-eval.git
cd hipe-2026-eval
```

If you already cloned without `--recursive`, initialise the submodule manually:

```bash
git submodule update --init --recursive
```

Create a local Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
make help
make validate-submissions
make eval-full
```

## Evaluation Pipeline

The real pipeline will provide these targets:

```bash
make validate-reference
make validate-submissions
make validate-info
make score
make rankings
make diagnostics
make results-md
make eval-full
make eval-full-refresh
```

`eval-full` validates submissions and info files, scores all submitted runs,
builds TSV rankings, writes diagnostics, and renders the results Markdown
document.

## Per-Run Metadata (`*-info.json`)

Each submitted run JSONL file must be accompanied by a metadata file with the same stem and an `-info.json` suffix:

```text
data/systems/<team>_<reference-stem>_<run>-info.json
```

The file must be a JSON object with exactly the following keys:

| Key                    | Type   | Description                                                                           |
| ---------------------- | ------ | ------------------------------------------------------------------------------------- |
| `hipe_parameter_count` | number | Organizer-decided parameter count used for ranking (derived from the team's report)   |
| `team_parameter_count` | number | Parameter count as reported by the team                                               |
| `hipe_model_size`      | number | Organizer-decided model size in MiB used for ranking (derived from the team's report) |
| `team_model_size`      | number | Model size in MiB as reported by the team                                             |

The `team_*` fields record the values as submitted by the team. The `hipe_*` fields are the organizer's authoritative values used in the Efficiency Ranking — they may differ if the organizers adjusted or verified the team-reported numbers.

`hipe_parameter_count` and `hipe_model_size` are required to be numeric. All four fields are required; `team_parameter_count` and `team_model_size` may be `null` if not applicable. A missing info file is allowed and generates a validation warning, but the run will be excluded from the Efficiency Ranking.

Example:

```json
{
  "hipe_parameter_count": 7000000000,
  "team_parameter_count": 7000000000,
  "hipe_model_size": 4096.5,
  "team_model_size": 4096.5
}
```

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

> **This repository must remain private until the evaluation results are officially published.**

The impresso test sets (de, en, fr) are present under `data/reference/`. The surprise test set (`surprise-test-fr`) is present but **still requires adjudication** — its reference labels are not yet final and must not be treated as authoritative.

Until adjudication of the surprise set is complete, evaluation results derived from it are organizer-internal only.
