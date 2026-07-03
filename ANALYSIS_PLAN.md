# Error-Analysis Plan (Overview Paper)

## Status

**Planning only — nothing in this document has been implemented.** This plan is for
review before any code is written, mirroring the role `ENSEMBLE_PLAN.md` played for
`lib/build_ensemble_analysis.py`.

---

## 0. Findings from `ENSEMBLE_PLAN.md` / `lib/build_ensemble_analysis.py` (read first)

These three findings determine how the shared feature table below is built, so they are
stated up front rather than buried in the design.

**(a) Exact `top5` membership rule.**
`top_n_runs()` in `lib/build_ensemble_analysis.py` filters out `random`/`baseline` (same
exclusion as `full` and `above_baseline`), then takes the **first 5 rows in ranking
order** from the relevant ranking TSV. Ranking-TSV row order comes from
`build_rankings.py`, which sorts by `(rank, team, run[, submission])` — ties on `rank`
(dense ranking, so ties really do share a rank) are broken **alphabetically by team id,
then run**, not by including every tied member. Practically: if rank 5 is shared by three
teams, only the alphabetically-first ones fill out the top-5 slots — the other tied
team(s) are excluded from `top5` even though they're tied on score. There is no separate
"handle ties at the boundary" logic to reproduce; whoever sorts first in the TSV wins the
slot.

**(b) `top5` is one fixed run-set per test group, not per file.**
`top5` is computed **once per test group** — `ranking-overall-test-a.tsv` for the three
`impresso-test-{de,en,fr}` tracks, `ranking-generalization-test-b.tsv` for
`surprise-test-fr` — using the *overall* (cross-language-mean) score. That same
`{(team, run), ...}` set is then intersected per track with whichever runs actually have a
diagnostics file for that specific language (`t5_runs = ensemble_runs[group]["top5"] &
all_runs`). So `impresso-test-de/en/fr` all start from the **same** globally-top-5 run
set; if one of those five teams didn't submit a `de` run, the `de` track's realized top5
ensemble has fewer than 5 members for that file. This analysis plan must **not**
recompute a fresh top-5 per language file — it has to reuse exactly the run-set the
existing `results.d/ensemble/<track>.ensemble.json` files already encode, or the two
pipelines will silently disagree.

**(c) Tie handling on `at` is plurality-vote, not majority-with-`NO_MAJORITY`.**
`build_gt_validation.py`'s `NO_MAJORITY` convention (`majority_vote()`: requires **strict
majority**, `>50%` of predictions, else `("", "NO_MAJORITY")`) is **not** what
`build_ensemble_analysis.py` uses for the ensembles we're consuming here. Its
`plurality_vote()` takes the Counter argmax with ties broken **alphabetically** among
tied labels (`FALSE` < `PROBABLE` < `TRUE`), and always returns a label as long as
there's at least one prediction — there is no `NO_MAJORITY` state in
`results.d/ensemble/*.ensemble.json`. Every pair already carries a precomputed
`vote_at`/`correct_at` (and `vote_isAt`/`correct_isAt`) under this convention. **This
plan consumes those precomputed fields directly and does not re-derive votes** — re-
implementing voting here would risk it drifting from `build_ensemble_analysis.py`,
which CLAUDE.md's "prefer importing over reimplementing" principle argues against by
extension.

A fourth, related fact worth flagging here rather than later: `build_diagnostics.py`
always emits one merged pair per **gold** `sampled_pairs` entry, defaulting a run's
missing prediction to `("FALSE", "FALSE", None, None)` (`prediction_fields()`). So every
gold pair for every track is guaranteed to appear in `results.d/ensemble/*.ensemble.json`
with a real `vote_at`/`vote_isAt` — the shared feature table below can do a plain
dict-join on `(document_id, pers_entity_id, loc_entity_id)` without needing to handle
"pair missing from ensemble output" as a special case.

---

## 1. Scope recap (per CLAUDE.md "Analysis Scripts")

- New top-level `analysis/` directory for scripts (sibling to `lib/`), new top-level
  `analysis.d/` for outputs (sibling to `results.d/`, `results-binary.d/`) — **not**
  `results.d/analysis/`.
- Read-only against `results.d/`, `results-binary.d/`, `data/reference/`. Reads from
  `results.d/diagnostics/`, `results.d/system-rankings/`, `results.d/ensemble/`, and
  `data/reference/`; writes only to `analysis.d/`.
- Own `make analysis` target, never a dependency of `eval-full` / `eval-full-refresh` /
  `eval-binary` / `ensemble`.
- `analysis.d/` gitignore coverage: **already done** — the pending (uncommitted)
  `.gitignore` change on this branch already adds `analysis.d/` right after
  `results.d/` (line 213), and `AGENT.md`'s directory listing / target list already
  mention it. No further gitignore work is needed for this plan.
- Binary track (`results-binary.d/`) is out of scope, consistent with
  `ENSEMBLE_PLAN.md`'s exclusion of it.

---

## 2. The four RQs at a glance

| RQ  | Question                          | Domain(s)              | Bucketing                          |
| --- | ---------------------------------- | ----------------------- | ----------------------------------- |
| RQ1 | Does OCR quality affect accuracy?  | A (`impresso`) only     | OCR-score tertiles                  |
| RQ2 | Does time/period affect accuracy?  | A and B, kept separate  | ~20-30yr windows                    |
| RQ3 | Does person–place proximity affect accuracy? | A + B (pooled) | char-distance quartiles     |
| RQ4 | Does QID-linkage (vs NIL) affect accuracy, and does it differ by system? | A + B (whatever each system covers) | QID-linked vs NIL, per person/location, per system |

All four consume the same `top5` per-pair correctness signal (`correct_at`,
`correct_isAt`) for the ensemble view; RQ4 additionally pulls two individual systems'
per-pair correctness from `results.d/diagnostics/`.

---

## 3. Shared feature table

### 3.1 Why one table

One script builds `analysis.d/tables/pair_level_features.parquet` once; all four RQ
scripts read it rather than re-joining reference + ensemble data four times. This mirrors
the `lib/` → `results.d/` staged-DAG style already used by the eval pipeline, just kept
structurally separate per CLAUDE.md.

### 3.2 Inputs

- `data/reference/HIPE-2026-v1.0-{impresso-test-de,impresso-test-en,impresso-test-fr,surprise-test-fr}.jsonl`
  — document text, dates, media metadata, and per-pair gold labels + mention lists + QIDs.
- `results.d/ensemble/{impresso-test-de,impresso-test-en,impresso-test-fr,surprise-test-fr}.ensemble.json`
  — `ensembles.top5.at.pairs[]` / `ensembles.top5.isAt.pairs[]`, keyed by
  `(document_id, pers_entity_id, loc_entity_id)`, giving `vote_at`/`correct_at`,
  `vote_isAt`/`correct_isAt` (isAt absent for `surprise-test-fr`, per finding (0) above).
- `results.d/system-rankings/ranking-overall-test-a.tsv` and
  `ranking-generalization-test-b.tsv` — used only to resolve "Awakened's best run" for
  RQ4 (team1's top-ranked run per group), not to recompute top5.
- `results.d/diagnostics/{baseline,team1}_*_run*.diagnostics.json` — per-pair
  `SYS_at`/`CORRECT_at`, `SYS_isAt`/`CORRECT_isAt` for the two individual systems in RQ4.

### 3.3 Critical schema caveat: **there are no character offsets in the reference data**

This wasn't assumed correctly at the outset and needs to be flagged before RQ3 design
makes sense. Each `sampled_pairs` entry has:

```
pers_entity_id, pers_wikidata_QID, pers_mentions_list,
loc_entity_id,  loc_wikidata_QID,  loc_mentions_list,
at, at_explanation, isAt, isAt_explanation
```

`pers_mentions_list` / `loc_mentions_list` are **surface-string lists** (e.g.
`["Eva Hovis"]`, `["Rt. 2"]`) at cluster granularity — there is no `start`/`end`/`offset`
field anywhere in the schema (confirmed by grepping all four reference files; the
`HIPE-2026-data` submodule schema itself isn't available to double-check since the
submodule isn't checked out in this working copy). `pers_wikidata_QID` /
`loc_wikidata_QID` are the exact field names; NIL is represented as JSON `null`, not the
string `"NIL"` (the substring `"NIL"` does appear inside `pers_entity_id`/`loc_entity_id`
values as an ID-construction convention, but the QID field itself is `null`).

**Consequence for RQ3**: character offsets must be *recovered* by locating each mention
string inside the document's `text` field, not read off an existing field. See §3.5.

### 3.4 Table columns

| Column | Source | Notes |
| --- | --- | --- |
| `track`, `dataset`, `split`, `language` | filename via `lib/common.py:parse_reference_filename` | reuse, don't reimplement |
| `document_id` | reference | |
| `pers_entity_id`, `loc_entity_id` | reference | join key (with `document_id`) into ensemble/diagnostics |
| `pers_wikidata_QID`, `loc_wikidata_QID` | reference | raw; `None` = NIL |
| `pers_qid_linked`, `loc_qid_linked` | derived | `QID is not None` |
| `pers_mentions_list`, `loc_mentions_list` | reference | kept for RQ3 offset recovery + debugging |
| `gold_at`, `gold_isAt` | reference | |
| `top5_vote_at`, `top5_correct_at` | `results.d/ensemble/<track>.ensemble.json` | isAt columns absent (null) for `surprise-test-fr` |
| `top5_vote_isAt`, `top5_correct_isAt` | same | |
| `date`, `year` | reference `date` (+ parsed year) | impresso gives full ISO dates (`1960-11-23`), surprise gives bare years (`"1756"`) — year parsing must handle both |
| `media_source_type`, `media_publication_title`, `media_time_period` | reference `media.*` | context columns, not a bucketing key |
| `doc_text_len` | derived from `text` | quick sanity/debug column |
| `ocr_score` | RQ1 pipeline (impresso only, see §4) | `None` for `surprise` |
| `min_char_distance`, `distance_match_status` | RQ3 offset recovery (see §3.5) | `distance_match_status ∈ {matched, unmatched}` |

Grain: one row per `(document_id, pers_entity_id, loc_entity_id)` — i.e. per sampled pair,
across all four reference files. `ocr_score` and document-level columns are repeated
across all pairs of the same document (acceptable — this is an analysis table, not a
normalized store).

### 3.5 Offset-recovery approach for RQ3 (proposed, needs sign-off given the caveat above)

For each pair, for each mention string in `pers_mentions_list` and each in
`loc_mentions_list`: find all occurrences in `document.text` (word-boundary-aware
substring search, not naive `str.find`, to avoid matching inside a longer word). Compute
the minimum character gap between any person-mention occurrence span and any
location-mention occurrence span (gap between nearest edges, i.e. `max(0, other_start -
this_end)` in whichever order they appear — not center-to-center). Take the minimum over
all mention-string × occurrence combinations for that pair.

**Known failure modes to report, not silently absorb:**
- A mention string may occur multiple times in the document for reasons unrelated to
  this specific entity cluster (common surname reused for a different person, generic
  place name appearing twice) — the "minimum distance" can be an underestimate in this
  case. No good general fix; flag as a limitation in the RQ3 write-up.
- A mention string may not be found verbatim (OCR noise, orthographic variation,
  hyphenation across a line break) — these pairs get `distance_match_status =
  "unmatched"` and are **excluded** from the RQ3 quartile table, not imputed. The script
  must report the exclusion count/rate per track so it's visible whether this is a rare
  edge case or a meaningful chunk of the data.
- Pairs where a mention list has multiple distinct surface forms belonging to the same
  cluster (e.g. `["Photius", "patriarche Photius"]`) — all forms are searched; the
  minimum distance can come from any of them.

This methodology should be treated as the most likely thing to get pushback on in review
— flagging it explicitly rather than presenting `min_char_distance` as a clean derived
field.

---

## 4. RQ1 — OCR quality (Domain A / `impresso` only)

Domain B (`surprise`, literary text, not OCR'd) is excluded — confirmed by the reference
data itself (`media.source_type: "Literary text"` vs `"Newspaper"`), matching the plan's
premise.

**Scorer** (per the user's direction, not something this repo currently has — confirmed
absent from `lib/`, the rest of the repo, and the (uninitialized) `HIPE-2026-data`
submodule):

```python
from impresso_pipelines.ocrqa import OCRQAPipeline
ocrqa_pipeline = OCRQAPipeline()
def compute_ocr_qa_score(ocr_text, language):
    result = ocrqa_pipeline(ocr_text, language=language)
    return result["score"]
```

Run once per document (`text` field, `language` field), score in `[0, 1]`, stored as
`ocr_score` in the shared table. `impresso_pipelines` is not currently a dependency
(confirmed via `pip show` — not installed) and needs to be added to `requirements.txt`;
flagged as an open risk in §9 since its transitive dependency footprint hasn't been
checked in this environment.

**Outputs:**
- `analysis.d/tables/rq1_ocr_tertiles.tsv`: OCR-score tertile × macro recall for `at` and
  `isAt` (macro recall computed the same way as
  `build_ensemble_analysis.py:_macro_recall` — mean of per-label recall over labels
  present in gold — applied to the `top5_correct_at`/`top5_correct_isAt` pairs falling in
  each tertile bucket), with `n` (pair count) per bucket.
- `analysis.d/tables/rq1_ocr_tertiles_by_language.tsv`: same cut, faceted by `language`,
  to check the bucketed pattern isn't one language dominating a tertile.
- One-line sanity check: Spearman correlation (`scipy.stats.spearmanr`), **document-level**
  — `ocr_score` vs. document-level accuracy (mean `top5_correct_at` over that document's
  pairs) — reported as `rho`, `p`, `n` in the TSV or a small companion text file. Not a
  regression model.

---

## 5. RQ2 — Time (Domain A and Domain B, reported separately)

Different period and genre per domain — outputs are never pooled across A/B.

- Parse `year` from `date`: impresso full ISO dates (`YYYY-MM-DD`) → take `YYYY`;
  surprise bare-year strings (`"1756"`) → parse directly. Fall back to
  `media.time_period` only if `date` is unparseable (not expected to be needed, but
  cheap to guard).
- Bin into ~20–30 year windows (exact boundaries decided at implementation time based on
  the actual year range per domain — impresso's `media.time_period` example
  `"1738-2018"` suggests a wide range worth checking before fixing bin edges).
- `analysis.d/tables/rq2_time_bins_domainA.tsv`: bin × macro recall for `at` and `isAt`.
- `analysis.d/tables/rq2_time_bins_domainB.tsv`: bin × macro recall for `at` only
  (`isAt` isn't evaluated for `surprise`).
- Spearman sanity check per domain: year (continuous) vs. document-level accuracy.

**Empty bins (confirmed, printed by the script and kept as explicit zero-count
rows rather than dropped):**
- Domain A (10-year bins, 1800-2000): 3/20 empty — `1860-1870`, `1880-1890`,
  `1970-1980`.
- Domain B (50-year bins, 1500-1800): 1/6 empty — `1700-1750`.

---

## 6. RQ3 — Proximity (pooled across domains)

Uses `min_char_distance` from §3.5, restricted to pairs where
`distance_match_status == "matched"`.

- `analysis.d/tables/rq3_distance_quartiles.tsv`: distance quartile × macro recall for
  `at` and `isAt` (isAt rows naturally absent for `surprise` pairs), with `n` and the
  match/exclusion rate reported alongside.
- `analysis.d/tables/rq3_distance_by_gold_label.tsv`: cross-tab of distance quartile ×
  gold `at` label (TRUE/PROBABLE/FALSE), specifically to check whether `PROBABLE` and
  cross-sentential `TRUE` cases skew toward the larger-distance quartiles. If they do,
  this is called out as an interpretive caveat in the RQ3 section of the eventual
  write-up (e.g. "higher error in the top distance quartile may partly reflect that
  quartile being enriched for inherently harder PROBABLE/cross-sentential cases, not
  purely a distance effect") rather than reported as a bare number.

---

## 7. RQ4 — QID bias (three-way system comparison)

**Systems**: `baseline` (`HIPE-Ministral-Baseline`, single run per track — no "best run"
selection needed, it only ever submits `run1`), `team1` ("Awakened")'s best run (resolved
per test group from `ranking-overall-test-a.tsv` / `ranking-generalization-test-b.tsv` —
its top-ranked submitted run; if team1 has no run for a given track/language, that cell
is omitted with a note, not imputed), and the **top5 ensemble**.

**Per-pair correctness sources**:
- baseline, team1's best run → `results.d/diagnostics/<run>.diagnostics.json`
  (`CORRECT_at`/`CORRECT_isAt` fields, already computed).
- top5 ensemble → `results.d/ensemble/<track>.ensemble.json` (`correct_at`/`correct_isAt`,
  per finding (c) above).

**Split**: each system's pairs split by `pers_qid_linked` (QID-linked vs NIL person) and,
separately, by `loc_qid_linked` (QID-linked vs NIL location) — two independent 2-way
splits, not a 4-way cross of both simultaneously (matches "each split by QID-linked vs
NIL person entity, and separately by location entity" in the brief).

**Open question — `isAt` scoping in the figure**: `rq4_qid_bias.tsv` computes both
`at` and `isAt` for every system/entity_type/qid_status cell, but the figure only
plots `at` (2 panels: person, location). This was a scope decision made without
explicit sign-off — flagged here rather than silently left as-is. If `isAt` should
also be shown, the natural extension is 4 panels (person/at, person/isAt,
location/at, location/isAt) or a second figure.

**Output**: `analysis.d/tables/rq4_qid_bias.tsv` — columns `system | entity_type
(person/location) | qid_status (linked/NIL) | task (at/isAt) | macro_recall | accuracy |
n`.

**Interpretive caveat — QID/NIL exposure in the baseline's input** (important, and only
inferable, not confirmed, from this repo): the baseline's own prediction JSONL carries
`pers_entity_id`/`loc_entity_id`/`pers_wikidata_QID`/`loc_wikidata_QID` values that are
**byte-identical** to the reference file's values for the same pairs (spot-checked on
`sn91068761-1960-11-23-a-i0001`). No baseline prompt template, generation script, or
`baseline/` directory is checked into this repo — the baseline's predictions were
generated externally — so this can't be confirmed from a spec, only inferred structurally
from the field identity. It strongly suggests the entity-linking/QID/NIL resolution is
**given as input** to every system (including the baseline), not something the model
itself resolves. If that's right, an accuracy gap between QID-linked and NIL entities
reflects the model's differential *reasoning* about linked vs. unlinked entities, not a
difference in what information it had access to — this framing should go in the RQ4
write-up rather than presenting the QID/NIL split as if it might reflect an information
asymmetry. Worth a quick confirmation from whoever ran the baseline generation, since this
plan can't verify it further from what's in this repository.

---

## 8. Figures

One figure per RQ, shared style module `analysis/plotting_common.py`:

- Fixed y-axis `[0, 1]` on every figure.
- One consistent color pair for `at` vs. `isAt` (and, in RQ4, repurposed for
  linked/NIL) reused across all figures, defined once in `plotting_common.py`:
  `#4f97dd` (dusty blue) / `#a8522e` (terracotta). Chosen with the dataviz skill's
  `validate_palette.js` — passes lightness band, chroma floor, CVD separation
  (worst adjacent ΔE ~75-90 across protan/deutan/tritan), and ≥3:1 contrast vs.
  white with no WARNs — and additionally checked for raw-luminance separation
  (0.290 vs 0.146, ~1.7:1) so the pair stays distinguishable converted to true
  greyscale/print, not just under CVD simulation (a same-lightness pastel pair
  would pass CVD checks yet collapse to one gray on a photocopier).
- Vector output (PDF), sized for CEUR/LNCS single-column width (~8.5cm / 3.35in
  wide; height chosen per chart type, likely ~2.5in) — plus a `.png` at the same
  filename stem (200 dpi) alongside every vector file.
- Bars/points annotated with the metric value; bucket tick labels include `n` (e.g.
  `"Q1\n(n=214)"`), and RQ1/RQ3 additionally fold the bucket's own value interval
  into the label (e.g. `"T1\n0.58–0.87\n(n=237)"`, `"Q1\n0–44 chars\n(n=271)"`) —
  split across 3 short lines rather than one long line, which overlapped at
  single-column width with only 3-4 bar slots to share.
- Titles are plain descriptions, no `"RQn:"` prefix (e.g. "Top-5 ensemble
  macro-recall per OCR-quality tertile") — set via `plotting_common.set_title()`,
  which passes `wrap=True` so a title wraps to a second line against the actual
  rendered axes width instead of clipping (this is what was silently clipping
  RQ3's title before the prefix was even dropped).
- RQ2's Domain A panel (20 ten-year bins) thins its x-tick labels to every 5th
  bin (~50 years) to stay legible; Domain B (6 bins) labels every bin. Empty bins
  are kept as real rows with a null macro-recall (not dropped), so the plotted
  line breaks visibly at a gap instead of interpolating across missing years —
  see §5 finding below for which bins are actually empty in each domain.

| RQ | Chart | File |
| --- | --- | --- |
| RQ1 | grouped bar: OCR tertile × macro recall (at/isAt) | `analysis.d/figures/rq1_ocr_quality.pdf` (+ .png) |
| RQ2 | line chart, two panels (Domain A / Domain B): year bin × macro recall, gaps at empty bins | `analysis.d/figures/rq2_time.pdf` (+ .png) |
| RQ3 | grouped bar: distance quartile × macro recall (at/isAt) | `analysis.d/figures/rq3_proximity.pdf` (+ .png) |
| RQ4 | system-grouped bar (`at` task only): QID-linked vs NIL, faceted person/location, x-axis shows display names (Ministral baseline / Awakened (best run) / Top-5 ensemble) | `analysis.d/figures/rq4_qid_bias.pdf` (+ .png) |

---

## 9. Script/output layout

```
analysis/
  build_pair_features.py   → analysis.d/tables/pair_level_features.parquet
  rq1_ocr_quality.py        → analysis.d/tables/rq1_*.tsv, analysis.d/figures/rq1_ocr_quality.pdf
  rq2_time.py                → analysis.d/tables/rq2_*.tsv, analysis.d/figures/rq2_time.pdf
  rq3_proximity.py           → analysis.d/tables/rq3_*.tsv, analysis.d/figures/rq3_proximity.pdf
  rq4_qid_bias.py            → analysis.d/tables/rq4_qid_bias.tsv, analysis.d/figures/rq4_qid_bias.pdf
  plotting_common.py         → shared style constants (colors, figure size, y-axis)
```

`build_pair_features.py` may import `lib/common.py` (`parse_reference_filename`,
`load_json`) for filename parsing — that's reuse of shared helpers, not reimplementing
evaluation logic, and consistent with CLAUDE.md's stated preference. It must not import
anything from `lib/build_ensemble_analysis.py`'s voting logic; it only reads that script's
JSON output.

**Makefile**: one new target, explicitly not part of `eval-full`'s dependency chain:

```make
analysis: analysis.d/tables/pair_level_features.parquet
	$(PYTHON) analysis/rq1_ocr_quality.py
	$(PYTHON) analysis/rq2_time.py
	$(PYTHON) analysis/rq3_proximity.py
	$(PYTHON) analysis/rq4_qid_bias.py

analysis.d/tables/pair_level_features.parquet: \
        $(wildcard data/reference/*.jsonl) \
        $(wildcard results.d/ensemble/*.ensemble.json) \
        $(wildcard results.d/diagnostics/*.diagnostics.json)
	$(PYTHON) analysis/build_pair_features.py
```

`make help` gets a one-line addition describing `analysis`, matching the existing
help-text style.

### New dependencies (requirements.txt currently has only `jsonschema`, `scikit-learn`)

- `pandas` — table joins/aggregation.
- `pyarrow` — parquet I/O.
- `scipy` — `spearmanr` for the sanity-check correlations (not in `scikit-learn`).
- `matplotlib` — figures.
- `impresso_pipelines` — OCR-quality scorer (RQ1 only). **Not installed in this
  environment**, so its dependency weight (it may pull in ML runtime dependencies) hasn't
  been checked — worth a quick `pip install --dry-run` or checking its PyPI page before
  committing to it as a hard dependency versus making RQ1 optionally-skippable if the
  package is absent.

---

## 10. Open questions — resolved

1. **RQ2 bin edges: fixed, not runtime-derived.** Domain A (impresso, observed
   1800-1998) switched to **10-year windows**, 1800-2000, after checking the resulting
   bin population (see table below) — sparse but usable: 17/20 bins non-empty, only 3
   single-document bins (1820-1830, 1870-1880, 1980-1990, each 1 doc / 9-12 pairs), 3
   fully empty (1860-1870, 1880-1890, 1970-1980). Domain B (surprise, observed
   1542-1797) is **left at 50-year windows**, 1500-1800 — a same-resolution check
   showed 21/30 of its 10-year bins would be empty, with over half its pairs (240/480)
   collapsing into a single `1750-1760` bin (documents cluster heavily at year 1756),
   so 10-year resolution was rejected for Domain B. Both edge sets are stated
   explicitly in `analysis/rq2_time.py`'s module docstring and printed at runtime, not
   left implicit in code.

   Domain A @ 10-year (actual, now in code):

   | bin | docs | pairs | | bin | docs | pairs |
   |---|---|---|---|---|---|---|
   | 1800-1810 | 3 | 42 | | 1900-1910 | 2 | 25 |
   | 1810-1820 | 2 | 20 | | 1910-1920 | 6 | 79 |
   | 1820-1830 | 1 | 12 | | 1920-1930 | 7 | 98 |
   | 1830-1840 | 2 | 24 | | 1930-1940 | 7 | 78 |
   | 1840-1850 | 5 | 31 | | 1940-1950 | 4 | 44 |
   | 1850-1860 | 3 | 27 | | 1950-1960 | 2 | 18 |
   | 1860-1870 | 0 | 0 | | 1960-1970 | 5 | 63 |
   | 1870-1880 | 1 | 12 | | 1970-1980 | 0 | 0 |
   | 1880-1890 | 0 | 0 | | 1980-1990 | 1 | 9 |
   | 1890-1900 | 3 | 20 | | 1990-2000 | 1 | 16 |

   Domain B @ 10-year (hypothetical, not adopted — shown to justify keeping 50-year):
   26/30 documents fall into just 3 non-empty decades (1540-1550: 2 docs/32 pairs,
   1560-1570: 1/16, 1610-1620: 1/16, 1630-1640: 2/32, 1660-1670: 1/16, 1670-1680: 1/16,
   **1750-1760: 15 docs/240 pairs**, 1790-1800: 7 docs/112 pairs); the other 21 decade
   bins between 1500 and 1800 are empty.
2. **RQ3 pooling: keep pooled A+B as primary**, `rq3_distance_quartiles.tsv`. Added
   `rq3_distance_quartiles_by_domain.tsv` as a second table using the *same* pooled
   quartile bucket edges, faceted by `dataset`, as a robustness check.
3. **`impresso_pipelines` treated as a hard dependency** (added to `requirements.txt`,
   no graceful-skip path). Sanity-installed during implementation — see run report:
   installs cleanly, moderate footprint (`huggingface_hub`, `floret`,
   `pybloomfilter3`; no PyTorch/heavy ML runtime), but note it needs the `[ocrqa]`
   extra (the bare package raises `ImportError` pointing at the extra) and performs a
   **runtime** HuggingFace Hub download on first call — a network dependency at
   `make analysis` time, not just at `pip install` time.
4. **QID/NIL-exposure confirmation (blocks RQ4's interpretive write-up only)**: still
   unresolved as of implementation — `analysis/rq4_qid_bias.py`'s module docstring
   explicitly flags that its table/figure are computed but the interpretive framing
   from §7 is deliberately not asserted anywhere in the script's output, pending
   confirmation from whoever generated the `HIPE-Ministral-Baseline` submissions.
