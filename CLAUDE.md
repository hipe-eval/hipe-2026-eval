# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Role

This repo orchestrates the official evaluation campaign for CLEF HIPE-2026 (person-place
relation extraction from multilingual historical documents). It is organizer-side only:
reference data, participant submissions, and all evaluation code/config live here. It does
**not** duplicate scorer logic — schema definitions and the core JSONL loading/evaluation
utilities are imported from the `HIPE-2026-data` git submodule (`HIPE-2026-data/scripts/`).
Prefer importing from that submodule over reimplementing evaluation logic in `lib/`.

Do not add a dummy/parallel pipeline — there is exactly one real evaluation pipeline. The
layout and workflow are meant to stay close to the `eval-template-repo/` template repo
(not present in this checkout) that this campaign was bootstrapped from.

Use `rg` for searching, per `AGENT.md`.

**The submodule is not checked out in this working copy** (`git submodule status` is empty).
Any command that touches `HIPE-2026-data/scripts` (validation, scoring) will fail until it's
initialized:

```bash
git submodule update --init --recursive
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # jsonschema, scikit-learn
```

## Commands

On macOS, invoke Makefile targets with `remake`, not the system `make` (per `AGENT.md`);
docs and target names still say `make` by convention. `make help` lists all targets.

```bash
make validate-reference    # validate data/reference/*.jsonl against the schema
make validate-submissions  # validate data/systems/*.jsonl against the schema
make validate-info         # validate *-info.json metadata + per-team run limits
make score                 # score every submission (depends on validate-submissions, validate-info)
make rankings               # build ranking TSVs (depends on score)
make diagnostics            # build per-run diagnostics JSON (depends on validate-submissions, validate-info)
make gt-validation          # build top-3 majority-vote GT validation workbooks (depends on rankings)
make ensemble               # build ensemble-aggregation analysis (depends on diagnostics, rankings)
make results-md             # render the final Markdown report (depends on rankings, diagnostics)
make eval-full              # results-md + ensemble: the full pipeline
make eval-full-refresh      # clean, then eval-full
make eval-binary            # eval-full with PROBABLE mapped to TRUE for `at`, writing to results-binary.d/
make clean                  # remove generated outputs
```

To score or validate one file directly (useful when iterating):

```bash
venv/bin/python lib/score_one.py data/systems/<file>.jsonl \
  --reference-dir data/reference --output-dir results.d/per-run \
  --schema-path HIPE-2026-data/schemas/hipe-2026-data.schema.json --data-repo HIPE-2026-data
```

There is no test suite in this repo; correctness is checked by running the pipeline above
against real data and inspecting `results.d/` output / the rendered Markdown report.

Generated-output locations are all overridable via Make variables (`RESULTS_DIR`,
`PER_RUN_DIR`, `RANKINGS_DIR`, `DIAGNOSTICS_DIR`, `GT_VALIDATION_DIR`, `AT_LABEL_MODE`).
`AT_LABEL_MODE` is `TERNARY` by default; `eval-binary` overrides it to `BINARY`.

## Pipeline Architecture

The pipeline is a strict DAG driven by the Makefile, one Python script per stage in `lib/`,
each independently invocable with its own CLI args:

```
validate_jsonl.py  →  score_one.py (via score_all.py)  →  build_rankings.py  →  build_results_md.py
                                    ↘  build_diagnostics.py  ↗                ↗
                                                            build_ensemble_analysis.py
                                    build_gt_validation.py (reads rankings + diagnostics-adjacent helpers)
```

- `lib/common.py` — shared regexes/dataclasses for parsing submission and reference
  filenames (`SUBMISSION_RE`, `REFERENCE_RE`), competition config loading, `*-info.json`
  reading, and the dense-ranking helper `competition_ranks` (ties share a rank; despite the
  name this is dense ranking, not standard competition ranking).
- `lib/score_one.py` — scores a single submission against its matching reference file. Adds
  `HIPE-2026-data/scripts` to `sys.path` and imports `check_jsonlschema` and
  `evaluation_utils` from the submodule for schema validation and JSONL reshaping/imputation.
  Missing predictions and `null` labels are imputed/normalized to `FALSE`. Writes one JSON
  file per run to `results.d/per-run/`.
- `lib/score_all.py` — thin wrapper that shells out `score_one.py` for every file in
  `data/systems/*.jsonl`.
- `lib/build_rankings.py` — aggregates `results.d/per-run/*.json` into ranking TSVs under
  `results.d/system-rankings/`.
- `lib/build_diagnostics.py` — merges gold + predicted labels per sampled pair into
  `<stem>.diagnostics.json` and confusion-matrix metrics into
  `<stem>.diagnostic_metrics.json`.
- `lib/build_ensemble_analysis.py` — aggregates predictions across multiple runs into three
  ensemble configurations (`full` = all team runs except `random`/`baseline`, `above_baseline`
  = runs scoring strictly above `baseline` in the overall ranking, `top5` = top-N by overall
  score, `--top-n` default 5); see `ENSEMBLE_PLAN.md` for the design rationale and exact
  member-selection rules. Note the implementation now reports `macro_recall` alongside
  `accuracy` per ensemble/task, even though `ENSEMBLE_PLAN.md` originally scoped this as
  accuracy-only — the plan doc is stale on that point. The binary (`results-binary.d/`)
  track is still excluded, as the plan describes.
- `lib/build_gt_validation.py` — takes the top 3 runs per ranking TSV, computes majority
  vote per pair, and writes Excel workbooks flagging mismatches with the reference label
  (three-way splits on `at` are `NO_MAJORITY`).
- `lib/build_results_md.py` — renders all ranking TSVs + diagnostics into the final
  `HIPE_2026_evaluation_results.md`.
- `lib/validate_info.py` — validates `*-info.json` sibling files and enforces the 3-runs-
  per-team-per-reference-file limit.

`results.d/` (and `results-binary.d/`) are fully generated — never hand-edit files there;
rerun the pipeline instead. Likewise, don't apply ad hoc transformations to reference/gold
data under `data/reference/` unless explicitly asked.

## Analysis Scripts

Exploratory/error analysis for the overview paper (OCR-quality strata, time strata,
proximity strata, QID bias, etc.) is a distinct concern from the evaluation pipeline above
and must stay structurally isolated from it:

- Analysis scripts do not live among the `lib/` pipeline stages and must never be wired into
  `eval-full`, `eval-full-refresh`, `eval-binary`, or `make ensemble`. They consume finished
  pipeline output; they are not a pipeline stage themselves.
- Analysis scripts are strictly read-only with respect to `results.d/`, `results-binary.d/`,
  and `data/reference/`. They may read freely from `results.d/diagnostics/`,
  `results.d/system-rankings/`, `results.d/ensemble/`, and `data/reference/`, but must never
  write into those directories or otherwise modify anything the pipeline produced — the
  existing "never hand-edit `results.d/`" rule extends to "never edit it from analysis code
  either."
- Analysis outputs (joined feature tables, figures, intermediate data) go under a new
  top-level `analysis.d/` directory, not `results.d/analysis/`. Keeping it a sibling of
  `results.d/` and `results-binary.d/` rather than nested inside `results.d/` matters
  concretely: `clean` and `eval-full-refresh` do `rm -rf $(RESULTS_DIR)`, and analysis output
  needs to survive pipeline reruns rather than get wiped alongside them.
- Once an analysis stage is added, give it its own `make analysis` target, deliberately left
  out of `eval-full`'s dependencies, so it can be run or re-run any number of times without
  running, or perturbing the state of, the evaluation pipeline.
- `analysis.d/` carries the same confidentiality constraint as the rest of the repo (private
  until results are published) and is gitignored the same way `results.d/` is.

## Evaluation Semantics

- Test A (`impresso`, dataset=`impresso`) evaluates both `at` (ternary: TRUE/PROBABLE/FALSE)
  and `isAt` (binary: TRUE/FALSE); this is the **Accuracy Profile**. The per-file score is
  `mean(at_macro_recall, isAt_macro_recall)`.
- Test B (`surprise`, `surprise-test-fr`) evaluates only `at`; this is the **Generalization
  Profile**, and its reference labels are **not yet adjudicated/final** (organizer-internal
  only until adjudication completes — see `RELEASE_PROCESS.md` / README "Data Status").
- `make eval-binary` remaps `PROBABLE → TRUE` for `at` before scoring (`AT_LABEL_MODE=BINARY`),
  changing `at_macro_recall` from a mean over 3 labels to a mean over 2.
- Missing documents, missing pairs, and remaining `null` labels are always treated as `FALSE`.
- Efficiency Profile ranks combine the Accuracy Profile rank with `hipe_parameter_count` and
  `hipe_model_size` ranks (organizer-verified values from `*-info.json`, not the
  team-reported `team_*` values). Missing/`null` values rank last. Balanced Efficiency
  weights Accuracy 50% and the two resource ranks 25% each.

## Filenames & Config

- Submissions: `data/systems/teamN_<reference-stem>_runX.jsonl` (+ sibling
  `..._runX-info.json`), `X` in 1–3, at most 3 runs per team per reference file. Reserved
  non-team identifiers: `random`, `baseline`. Full rules in `SUBMISSIONS.md`.
- References: `data/reference/HIPE-2026-<version>-<dataset>-<split>-<language>.jsonl`, parsed
  by `REFERENCE_RE` in `lib/common.py`.
- `lib/competition_config.json` — declares the 4 evaluation "cells" (impresso de/en/fr +
  surprise fr), each with its `profile` and `targets`.
- `lib/teams.json` — maps team IDs to display name / affiliation / country, used only for
  rendering the results Markdown.

## Confidentiality

This repository must stay **private** until results are officially published — reference
labels and participant submissions are sensitive campaign data. Be careful not to leak
`data/reference/`, `data/systems/`, or `results.d/` contents outside the repo.