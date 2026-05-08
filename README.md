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

## Repository Layout

```text
data/
  reference/              # Flat gold reference JSONL copies, added when test data is open
  systems/                # Participant submission JSONL files and matching *-info.json files
lib/
  score_one.py            # Score one submitted run against the matching reference file
  validate_jsonl.py       # Validate reference/submission files against the HIPE-2026 schema
  build_rankings.py       # Aggregate per-run JSON scores into TSV rankings
  build_diagnostics.py    # Build comparison and diagnostic metrics JSON files
  build_gt_validation.py  # Build GT validation workbooks from top-three majority votes
  build_results_md.py     # Render ranking TSVs into a Markdown results page
  competition_config.json # Official evaluation cells and weights
  teams.json              # Team ID to affiliation metadata
results.d/                # Generated evaluation output, not hand-edited
  per-run/                # Per-submission JSON scores and logs
  system-rankings/        # Ranking TSV files
  diagnostics/            # Per-submission diagnostics JSON files
  gt-validation/          # Top-three majority-vote GT validation workbooks
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

The main pipeline provides these targets:

```bash
make validate-reference
make validate-submissions
make validate-info
make score
make rankings
make diagnostics
make gt-validation
make results-md
make eval-full
make eval-full-refresh
```

`eval-full` validates submissions and info files, scores all submitted runs,
builds TSV rankings, writes diagnostics, and renders the results Markdown
document. `gt-validation` is separate because it is an organizer-facing review
artifact built from the current per-dataset rankings.

Generated paths can be redirected through Make variables:

| Variable            | Default                    | Purpose                                      |
| ------------------- | -------------------------- | -------------------------------------------- |
| `RESULTS_DIR`       | `results.d`                | Root directory for generated outputs         |
| `PER_RUN_DIR`       | `$(RESULTS_DIR)/per-run`   | Per-submission score JSON files              |
| `RANKINGS_DIR`      | `$(RESULTS_DIR)/system-rankings` | Ranking TSV files                       |
| `DIAGNOSTICS_DIR`   | `$(RESULTS_DIR)/diagnostics` | Comparison and diagnostic metrics JSON files |
| `GT_VALIDATION_DIR` | `$(RESULTS_DIR)/gt-validation` | GT validation Excel workbooks             |

## Profile Rankings and Scores

The results report uses profile names that match the dataset families:

- **Accuracy Profile Ranking** uses the `impresso` reference files.
- **Generalization Profile Ranking** uses the `surprise` reference files.
- **Efficiency Profile Ranking** combines the Accuracy Profile rank with model
  parameter-count and model-size ranks.

The overall Accuracy Profile Ranking includes only team runs that submitted all
`impresso` language files. Team runs with partial submissions are shown only in
the dataset-specific ranking tables.

For a label `l`:

```text
recall_l = true_positives_l / gold_instances_l
```

The `at` task has three labels:

```text
at_macro_recall = mean(recall_TRUE, recall_PROBABLE, recall_FALSE)
```

The `isAt` task has two labels:

```text
isAt_macro_recall = mean(recall_TRUE, recall_FALSE)
```

Per-file profile scores:

```text
impresso_profile_score = mean(at_macro_recall, isAt_macro_recall)
surprise_profile_score = at_macro_recall
```

Overall and efficiency scores:

```text
mean_impresso_profile_score = mean(impresso_profile_score over submitted impresso language files)
mean_efficiency_profile_rank = mean(rank_impresso_profile_score, rank_hipe_parameter_count, rank_hipe_model_size)
```

Higher is better for profile scores. Lower is better for
`mean_efficiency_profile_rank`. Ties receive the same competition rank.

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

The `team_*` fields record the values as submitted by the team. The `hipe_*`
fields are the organizer's authoritative values used in the Efficiency Profile
Ranking; they may differ if the organizers adjusted or verified the team-reported
numbers.

`hipe_parameter_count` and `hipe_model_size` are required to be numeric. All four
fields are required; `team_parameter_count` and `team_model_size` may be `null`
if not applicable. A missing info file is allowed and generates a validation
warning. The run remains in the Efficiency Profile Ranking, but its missing
parameter-count and model-size values are ranked last.

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
the corresponding reference file. `impresso` files include matrices for `at` and
`isAt`; `surprise` files include `at` only. Each matrix uses fixed label order,
reports rows as gold labels and columns as predictions, and includes:

- a dense numeric `matrix`;
- a human-readable `table` with one row per gold label and `pred_*` columns;
- micro-aggregated accuracy;
- per-label precision, recall, and F1;
- per-label support, true positives, false positives, and false negatives.

## GT Validation Workbooks

The `gt-validation` target writes one Excel workbook per reference dataset under
`results.d/gt-validation/` by default:

```text
results.d/gt-validation/<reference-stem>.gt_validation.xlsx
```

For each dataset, the target takes the top three submitted runs from the
corresponding ranking TSV, computes a majority vote for each sampled pair, and
lists cases where that majority vote does not match the reference label. A
three-way split for `at` is reported as `NO_MAJORITY` and included for review.

Each workbook contains:

- `mismatches`: one row per flagged pair/target, including the chunk name,
  entity IDs, mentions, gold label, vote label, vote status, and the three
  system labels and explanations;
- `top_runs`: the three system runs used for the vote;
- `summary`: flagged row counts per evaluated target.

## Data Status

> **This repository must remain private until the evaluation results are officially published.**

The impresso test sets (de, en, fr) are present under `data/reference/`. The surprise test set (`surprise-test-fr`) is present but **still requires adjudication** — its reference labels are not yet final and must not be treated as authoritative.

Until adjudication of the surprise set is complete, evaluation results derived from it are organizer-internal only.
