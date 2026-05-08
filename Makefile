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

.PHONY: help install validate-reference validate-submissions validate-info score rankings diagnostics gt-validation results-md eval-full eval-full-refresh clean

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
		'  eval-full             Run validation, scoring, rankings, diagnostics, and Markdown rendering' \
		'  eval-full-refresh     Remove generated outputs before eval-full' \
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
	$(PYTHON) lib/score_all.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --output-dir $(PER_RUN_DIR) --schema-path $(SCHEMA_PATH) --data-repo $(DATA_REPO) --config $(CONFIG)

rankings: score
	$(PYTHON) lib/build_rankings.py --per-run-dir $(PER_RUN_DIR) --output-dir $(RANKINGS_DIR)

diagnostics: validate-submissions validate-info
	$(PYTHON) lib/build_diagnostics.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --output-dir $(DIAGNOSTICS_DIR)

gt-validation: rankings
	$(PYTHON) lib/build_gt_validation.py --systems-dir $(SUBMISSIONS_DIR) --reference-dir $(REFERENCE_DIR) --rankings-dir $(RANKINGS_DIR) --output-dir $(GT_VALIDATION_DIR)

results-md: rankings diagnostics
	$(PYTHON) lib/build_results_md.py --rankings-dir $(RANKINGS_DIR) --diagnostics-dir $(DIAGNOSTICS_DIR) --teams $(TEAMS) --output $(RESULTS_MD)

eval-full: results-md

eval-full-refresh: clean eval-full

clean:
	rm -rf $(RESULTS_DIR) $(RESULTS_MD)
