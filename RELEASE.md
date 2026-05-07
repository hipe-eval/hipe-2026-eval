# Release 0.1.0

Initial evaluation campaign repository release for HIPE-2026.

## Included

- organizer-side evaluation orchestration through `remake` targets
- flat reference data layout under `data/reference/`
- submission layout under `data/systems/`
- baseline organizer systems:
  - `random`
  - `baseline`
- validation for HIPE-2026 JSONL files and per-run `*-info.json` metadata
- scoring wrappers using the `HIPE-2026-data` schema and evaluation utilities
- ranking generation for:
  - Accuracy Ranking
  - Generalization Ranking
  - Efficiency Ranking
- generated Markdown report rendering with links to diagnostics artifacts
- per-run document diagnostics and diagnostic metrics under `results.d/diagnostics/`
- release process documentation, including archive-branch handling for generated
  result snapshots

## Default Evaluation Layout

The Makefile is the source of truth for generated output paths:

```make
RESULTS_DIR ?= results.d
PER_RUN_DIR ?= $(RESULTS_DIR)/per-run
RANKINGS_DIR ?= $(RESULTS_DIR)/system-rankings
DIAGNOSTICS_DIR ?= $(RESULTS_DIR)/diagnostics
```

The generated report is:

```text
HIPE_2026_evaluation_results.md
```

`results.d/` is ignored by default and should be committed only when publishing
the intended official results snapshot. Intermediate generated results can be
archived on separate archive branches.

## Main Commands

Recommended setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Core evaluation commands:

```bash
remake validate-reference
remake validate-submissions
remake validate-info
remake eval-full
```

`eval-full` runs validation, scoring, ranking, diagnostics generation, and report
rendering through staged Makefile dependencies.

## Diagnostics

For each submitted run, the diagnostics target writes:

```text
results.d/diagnostics/<submission-stem>.diagnostics.json
results.d/diagnostics/<submission-stem>.diagnostic_metrics.json
```

The document diagnostics merge reference labels and system predictions for every
sampled pair. The diagnostic metrics files include confusion matrices,
human-readable matrix tables, micro-aggregated accuracy, and per-label
precision, recall, and F1.

## Notes

- Python dependencies are listed in `requirements.txt`.
- The `HIPE-2026-data/` checkout provides the schema and shared validation /
  evaluation utilities.
- Use `remake`, not the system `make`, when invoking Makefile targets in this
  local macOS workflow.
