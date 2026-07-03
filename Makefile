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
ANALYSIS_DIR ?= analysis.d
ANALYSIS_FEATURES ?= $(ANALYSIS_DIR)/tables/pair_level_features.parquet

.PHONY: help install validate-reference validate-submissions validate-info score rankings diagnostics gt-validation results-md ensemble eval-full eval-full-refresh eval-binary analysis clean

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
		'  analysis              Build overview-paper error-analysis tables/figures (RQ1/RQ2/RQ3/RQ4; not part of eval-full)' \
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

analysis: $(ANALYSIS_FEATURES)
	$(PYTHON) analysis/rq1_ocr_quality.py --features $(ANALYSIS_FEATURES) --output-dir $(ANALYSIS_DIR)
	$(PYTHON) analysis/rq2_time.py --features $(ANALYSIS_FEATURES) --output-dir $(ANALYSIS_DIR)
	$(PYTHON) analysis/rq3_proximity.py --features $(ANALYSIS_FEATURES) --output-dir $(ANALYSIS_DIR)
	$(PYTHON) analysis/rq4_qid_bias.py --features $(ANALYSIS_FEATURES) --reference-dir $(REFERENCE_DIR) --diagnostics-dir $(DIAGNOSTICS_DIR) --rankings-dir $(RANKINGS_DIR) --output-dir $(ANALYSIS_DIR)

$(ANALYSIS_FEATURES): $(wildcard $(REFERENCE_DIR)/*.jsonl) $(wildcard $(ENSEMBLE_DIR)/*.ensemble.json)
	$(PYTHON) analysis/build_pair_features.py --reference-dir $(REFERENCE_DIR) --ensemble-dir $(ENSEMBLE_DIR) --output $(ANALYSIS_FEATURES)

clean:
	rm -rf $(RESULTS_DIR) $(RESULTS_MD)
