PYTHON ?= venv/bin/python
DATA_REPO ?= HIPE-2026-data
SCHEMA_PATH ?= $(DATA_REPO)/schemas/hipe-2026-data.schema.json
REFERENCE_DIR ?= data/reference
SUBMISSIONS_DIR ?= data/systems
RESULTS_DIR ?= results.d
PER_RUN_DIR ?= $(RESULTS_DIR)/per-run
RANKINGS_DIR ?= $(RESULTS_DIR)/system-rankings
DIAGNOSTICS_DIR ?= $(RESULTS_DIR)/diagnostics
GT_VALIDATION_DIR ?= $(RESULTS_DIR)/gt-validation
RESULTS_MD ?= HIPE_2026_evaluation_results.md
CONFIG ?= lib/competition_config.json
TEAMS ?= lib/teams.json
AT_LABEL_MODE ?= TERNARY
ENSEMBLE_DIR ?= $(RESULTS_DIR)/ensemble
ENSEMBLE_SUMMARY ?= $(ENSEMBLE_DIR)/ensemble_summary.tsv

.PHONY: help install validate-reference validate-submissions validate-info score rankings diagnostics gt-validation results-md ensemble eval-full eval-full-refresh eval-binary clean

help:
	@printf '%s\n' \
		'Targets:' \
		'  install               Install Python dependencies into the active environment' \
		'  validate-reference    Validate reference JSONL files' \
		'  validate-submissions  Validate submission JSONL files' \
		'  validate-info         Validate submission metadata and run limits' \
		'  score                 Score all submissions' \
		'  rankings              Build ranking TSV files' \
		'  diagnostics           Build per-submission diagnostics JSON files' \
		'  gt-validation         Build top-three majority-vote GT validation workbooks' \
		'  results-md            Render final Markdown results page' \
		'  ensemble              Build ensemble-aggregation analysis (label distributions + accuracy)' \
		'  eval-full             Run validation, scoring, rankings, diagnostics, ensemble, and Markdown rendering' \
		'  eval-full-refresh     Remove generated outputs before eval-full' \
		'  eval-binary           Run eval-full with PROBABLE mapped to TRUE for at labels' \
		'  clean                 Remove generated outputs'

install:
	$(PYTHON) -m pip install -r requirements.txt

validate-reference:
	$(PYTHON) lib/validate_jsonl.py --schema-path $(SCHEMA_PATH) --data-repo $(DATA_REPO) $(REFERENCE_DIR)

validate-submissions:
	$(PYTHON) lib/validate_jsonl.py --schema-path $(SCHEMA_PATH) --data-repo $(DATA_REPO) $(SUBMISSIONS_DIR)

validate-info:
	$(PYTHON) lib/validate_info.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR)

score: validate-submissions validate-info
	$(PYTHON) lib/score_all.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --output-dir $(PER_RUN_DIR) --schema-path $(SCHEMA_PATH) --data-repo $(DATA_REPO) --config $(CONFIG) --at-label-mode $(AT_LABEL_MODE)

rankings: score
	$(PYTHON) lib/build_rankings.py --per-run-dir $(PER_RUN_DIR) --output-dir $(RANKINGS_DIR)

diagnostics: validate-submissions validate-info
	$(PYTHON) lib/build_diagnostics.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --output-dir $(DIAGNOSTICS_DIR) --at-label-mode $(AT_LABEL_MODE)

gt-validation: rankings
	$(PYTHON) lib/build_gt_validation.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --rankings-dir $(RANKINGS_DIR) --output-dir $(GT_VALIDATION_DIR)

results-md: rankings diagnostics
	$(PYTHON) lib/build_results_md.py --rankings-dir $(RANKINGS_DIR) --diagnostics-dir $(DIAGNOSTICS_DIR) --teams $(TEAMS) --output $(RESULTS_MD) --at-label-mode $(AT_LABEL_MODE)

ensemble: diagnostics rankings
	$(PYTHON) lib/build_ensemble_analysis.py \
		--diagnostics-dir $(DIAGNOSTICS_DIR) \
		--rankings-dir    $(RANKINGS_DIR) \
		--output-dir      $(ENSEMBLE_DIR)

eval-full: results-md ensemble

eval-full-refresh: clean eval-full

eval-binary:
	$(MAKE) eval-full RESULTS_DIR=results-binary.d RESULTS_MD=HIPE_2026_evaluation_results-binary.md AT_LABEL_MODE=BINARY

clean:
	rm -rf $(RESULTS_DIR) $(RESULTS_MD)
