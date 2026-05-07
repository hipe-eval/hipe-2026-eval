# Release Process

This document describes how to prepare a release for the `hipe-2026-eval`
repository.

This repository is an organizer-side evaluation campaign repository. The release
unit is a tagged repository snapshot that includes:

- evaluation orchestration code under `lib/`;
- the campaign `Makefile`;
- evaluation configuration such as `lib/competition_config.json` and
  `lib/teams.json`;
- documentation such as `README.md`, `GUIDELINES.md`, `SUBMISSIONS.md`, and
  this file;
- reference and system files under `data/` when they are intended to be part of
  the release.

Generated outputs under `results.d/` are derived artifacts. During development
or internal evaluation rounds, archive them on a separate branch when needed.
For the final official release, commit the intended public results explicitly.

## Release Style

Use simple semantic versions for release tags:

- `0.1.0`
- `0.1.1`
- `0.2.0`

Recommended git tag format:

```text
v0.1.0
```

Keep the same version string in:

- the git tag;
- the GitHub release title, if you publish one;
- any release note file or announcement text used for the campaign.

This repository does not currently have package metadata such as
`pyproject.toml`, so there is no package version to update.

## Normal Workflow

1. Prepare release changes on a branch.
2. Review changed evaluation code, config, data, and documentation.
3. Run local verification.
4. Archive generated `results.d/` files on a separate branch if useful.
5. Merge to `main`.
6. Create an annotated tag from the merged commit.
7. Optionally publish a GitHub release.

## Prepare the Release

### 1. Review the Changes

Inspect the diff since the previous release:

```bash
git log <previous-tag>..HEAD --oneline
git diff <previous-tag>..HEAD --stat
git diff <previous-tag>..HEAD --name-status
```

Pay particular attention to:

- `lib/`
- `Makefile`
- `README.md`
- `GUIDELINES.md`
- `SUBMISSIONS.md`
- `data/reference/`
- `data/systems/`
- `lib/competition_config.json`
- `lib/teams.json`

For a release that changes scoring, ranking, diagnostics, or result rendering,
review the relevant generated outputs under `results.d/` before deciding
whether they should remain untracked, be archived, or be committed for final
publication.

### 2. Review Data Inputs

Confirm the reference files use canonical flat names under `data/reference/`,
for example:

```text
HIPE-2026-v1.0-impresso-test-de.jsonl
HIPE-2026-v1.0-impresso-test-en.jsonl
HIPE-2026-v1.0-impresso-test-fr.jsonl
HIPE-2026-v1.0-surprise-test-fr.jsonl
```

Confirm submissions under `data/systems/` follow the expected naming convention:

```text
teamN_<reference-stem>_runX.jsonl
```

Reserved organizer baselines may use:

```text
random_<reference-stem>_run1.jsonl
baseline_<reference-stem>_run1.jsonl
```

Each run should have a matching `*-info.json` file whenever possible.

### 3. Review Documentation

Update documentation when the release changes:

- Makefile targets or variables;
- generated output layout under `results.d/`;
- submission loading instructions;
- reference or system filename conventions;
- efficiency metadata requirements;
- ranking formulas;
- diagnostics output formats.

In practice, review at least:

- `README.md`
- `GUIDELINES.md`
- `SUBMISSIONS.md`
- `PLAN.md`
- `AGENT.md`

## Local Verification

Use the project `venv/` and invoke Makefile targets with `remake`.

Recommended release checks:

```bash
python3 -m py_compile lib/*.py
remake validate-reference
remake validate-submissions
remake validate-info
remake eval-full
```

`eval-full` should generate:

```text
results.d/per-run/
results.d/system-rankings/
results.d/diagnostics/
HIPE_2026_evaluation_results.md
```

If you changed Makefile wiring, check target dependency behavior:

```bash
remake results-md
remake diagnostics
```

These targets should pull in the earlier stages they require.

If you only want to inspect commands without running them:

```bash
remake -n eval-full
```

## Handling Generated Results

`results.d/` contains derived artifacts:

- per-run JSON scores;
- ranking TSV files;
- document-level diagnostics;
- diagnostic metrics JSON files.

During intermediate rounds, do not commit `results.d/` to `main` unless the
campaign policy explicitly calls for it. If a generated result snapshot should
be preserved before final publication, create or update an archive branch.

Example archive workflow:

```bash
git switch -c archive/results-YYYY-MM-DD
git add results.d HIPE_2026_evaluation_results.md
git commit -m "Archive evaluation results YYYY-MM-DD"
git push origin archive/results-YYYY-MM-DD
git switch -
```

If updating an existing archive branch, use normal non-destructive git workflow:

```bash
git switch archive/results-YYYY-MM-DD
git pull --ff-only
git add results.d HIPE_2026_evaluation_results.md
git commit -m "Update archived evaluation results YYYY-MM-DD"
git push origin archive/results-YYYY-MM-DD
git switch -
```

For the final official version, commit only the intended public `results.d/`
snapshot and generated report to the release branch after verifying that the
outputs correspond exactly to the official input data and accepted submissions.

## Release Checklist

Before tagging, confirm all of the following:

- working tree contains only intentional changes;
- `README.md` reflects current targets, defaults, and output paths;
- `SUBMISSIONS.md` matches the accepted submission naming and metadata rules;
- `lib/teams.json` contains the intended public team labels;
- `lib/competition_config.json` contains the intended evaluation cells;
- `python3 -m py_compile lib/*.py` passes;
- `remake eval-full` passes;
- generated report links point to files under `results.d/diagnostics/`;
- intermediate `results.d/` snapshots have been archived if needed;
- final public `results.d/` artifacts are committed only when intended.

Useful commands:

```bash
git status --short
git diff --stat origin/main..HEAD
git log --oneline origin/main..HEAD
```

## Tagging

After the release branch is merged to `main`, sync your local branch and create
an annotated tag:

```bash
git checkout main
git pull --ff-only
git tag -a v0.1.0 -m "Release 0.1.0"
git push origin v0.1.0
```

Use the actual release version instead of `0.1.0`.

## GitHub Release

The tagged commit is the actual repository release snapshot.

A GitHub release is optional. If you publish one, use:

- tag: `vX.Y.Z`;
- title: `Release X.Y.Z`;
- body: a concise summary of the released evaluation code, configuration, data
  status, and whether official `results.d/` artifacts are included.

The `gh` tool is convenient but not required:

```bash
gh release create v0.1.0 --title "Release 0.1.0" --notes-file RELEASE_NOTES.md
```

If the release already exists, inspect before editing:

```bash
gh release view v0.1.0
```
