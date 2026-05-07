# HIPE-2026 Eval Agent Guide

This repository orchestrates the HIPE-2026 evaluation campaign. It should stay close to the layout and workflow of `eval-template-repo/`, while using the HIPE-2026 relation-extraction scorer code from the `HIPE-2026-data/` submodule.

## Repository Role

The parent repository is responsible for campaign orchestration:

- storing organizer-side reference data in `data/reference/`;
- storing participant system submissions in `data/systems/`;
- validating JSONL files against `HIPE-2026-data/schemas/hipe-2026-data.schema.json`;
- scoring submitted runs against matching reference files;
- writing derived outputs under `results.d/`;
- building ranking TSVs and the generated results Markdown page.

The `HIPE-2026-data/` submodule remains the source of truth for:

- schema definition;
- data examples and released training/sandbox files;
- core JSONL loading and validation behavior;
- relation-evaluation utilities in `HIPE-2026-data/scripts/`.

Avoid duplicating scorer logic in this parent repository when it can be imported from the submodule.

## Expected Layout

Keep the layout analogous to the template repository:

```text
data/reference/
data/systems/
lib/
results.d/per-run/
results.d/system-rankings/
HIPE_2026_evaluation_results.md
```

Do not add a dummy pipeline unless explicitly requested. This task needs orchestration for the real evaluation campaign only.

## Makefile Workflow

Everything operational should be available through Makefile targets. On macOS, invoke targets with `remake`, not the system `make`. Keep command names in Makefiles and docs as `make` where convention requires it.

Important targets should include:

- `validate-reference`
- `validate-submissions`
- `score`
- `rankings`
- `results-md`
- `eval-full`
- `eval-full-refresh`
- `clean`

## Filename Conventions

Participant submission files should follow the task guideline pattern:

```text
teamN_<inputfile-stem>_runX.jsonl
```

Examples:

```text
team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-en_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl
team1_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl
```

The scorer should derive the reference file by removing the leading team prefix and trailing `_runX`.

Team identifiers are expected to be numerical names such as `team1`, `team2`,
and so on. Do not accept more than three runs per team and reference language
file.

Each run may have a sibling `*-info.json` file containing numeric
`hipe_parameter_count`, `team_parameter_count`, `hipe_model_size`, and
`team_model_size` values. Efficiency rankings use the `hipe_*` values. Missing
info files should not fail scoring, but should place the affected run last for
efficiency metadata ranks.

## Evaluation Semantics

Test A, the historical newspaper domain, evaluates both `at` and `isAt`. The main score is the average of macro recall for `at` and macro recall for `isAt`.

Surprise Test B evaluates only `at`; it is the generalization profile.

Missing documents, missing pairs, and remaining `null` labels are treated as `FALSE`, matching the HIPE-2026 guidelines and data-submodule evaluator behavior.

## Editing Notes

- Preserve generated results as derived artifacts. Do not hand-edit files under `results.d/`.
- Keep generated reference/test gold data out of ad hoc transformations unless explicitly asked.
- Prefer direct imports from `HIPE-2026-data/scripts` for validation/scoring helpers.
- Use `rg` for searching.
- Use `remake` for local target execution.
