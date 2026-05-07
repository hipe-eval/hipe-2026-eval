# Filling `data/systems/`

This note explains how to place participant submissions into `data/systems/`
for the HIPE-2026 evaluation campaign.

## Directory

Put all participant system files directly under:

```text
data/systems/
```

Do not keep one subdirectory per team and do not keep the ZIP file structure.
After unpacking participant archives, copy or move the relevant `.jsonl` files
and their metadata files into this single flat directory.

## Prediction Files

Each prediction file must be named:

```text
teamN_<reference-stem>_runX.jsonl
```

where:

- `teamN` is the assigned numerical team identifier, for example `team1`.
  The reserved organizer baseline identifiers are `random` and `baseline`.
- `<reference-stem>` is the reference/input filename without `.jsonl`.
- `runX` is `run1`, `run2`, or `run3`.

Examples:

```text
team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-en_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl
team1_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl
random_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
baseline_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
```

The corresponding reference files are expected in `data/reference/`:

```text
HIPE-2026-v1.0-impresso-test-de.jsonl
HIPE-2026-v1.0-impresso-test-en.jsonl
HIPE-2026-v1.0-impresso-test-fr.jsonl
HIPE-2026-v1.0-surprise-test-fr.jsonl
```

The scorer derives the reference filename by removing the leading `teamN_` and
the trailing `_runX` from the prediction filename.

## Run Limit

Accept at most three runs per team and reference language file:

```text
team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-de_run2.jsonl
team1_HIPE-2026-v1.0-impresso-test-de_run3.jsonl
```

Do not add `run4` or later. The evaluation validation step is expected to fail
if more than three runs are present for the same team and reference file.

## Metadata Files

For each prediction file, add a sibling `*-info.json` file with the same base
name and `-info.json` suffix:

```text
team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl
team1_HIPE-2026-v1.0-impresso-test-de_run1-info.json
```

The info file must be a JSON object with these keys:

```json
{
  "hipe_parameter_count": 0,
  "team_parameter_count": 0,
  "hipe_model_size": 0,
  "team_model_size": 0
}
```

Use numeric values for `hipe_parameter_count` and `hipe_model_size`, because
these organizer estimates are used for efficiency ranking. Model size is in MB.

`team_parameter_count` and `team_model_size` should reflect what the team
reported. These values may be numbers, strings such as `"Claude"`, strings such
as `"not available"`, or `null`. Preserve the participant-provided information
there; the ranking depends on the numeric `hipe_*` fields.

Missing `*-info.json` files should be avoided, but they do not invalidate the
accuracy evaluation. Runs without info files are assigned the last rank for
parameter count and model size in the efficiency evaluation.

## Checklist

Before running evaluation, check:

- Every `.jsonl` file is directly under `data/systems/`.
- Every participant `.jsonl` filename starts with `team1_`, `team2_`, etc.;
  organizer baselines may start with `random_` or `baseline_`.
- Every `.jsonl` filename ends with `_run1.jsonl`, `_run2.jsonl`, or
  `_run3.jsonl`.
- No team has more than three runs for the same reference file.
- Each prediction filename maps to an existing file in `data/reference/` after
  removing `teamN_` and `_runX`.
- Each run has a matching `*-info.json` file whenever possible.
- `hipe_parameter_count` and `hipe_model_size` are numeric in every available
  info file.
