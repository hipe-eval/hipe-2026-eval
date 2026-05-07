"""Shared helpers for the HIPE-2026 evaluation campaign."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUBMISSION_RE = re.compile(r"^((?:team\d+)|dummy)_(.+)_run([1-3])\.jsonl$")
INFO_RE = re.compile(r"^((?:team\d+)|dummy)_(.+)_run([1-3])-info\.json$")
REFERENCE_RE = re.compile(r"^HIPE-2026-.+-(?P<dataset>[^-]+)-(?P<split>[^-]+)-(?P<language>[^-]+)\.jsonl$")


@dataclass(frozen=True)
class SubmissionName:
    team: str
    reference_stem: str
    run: str
    filename: str

    @property
    def reference_filename(self) -> str:
        return f"{self.reference_stem}.jsonl"

    @property
    def info_filename(self) -> str:
        stem = self.filename.removesuffix(".jsonl")
        return f"{stem}-info.json"


@dataclass(frozen=True)
class ReferenceCell:
    dataset: str
    split: str
    language: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def parse_submission_filename(path_or_name: Path | str) -> SubmissionName:
    name = Path(path_or_name).name
    match = SUBMISSION_RE.match(name)
    if not match:
        raise ValueError(
            f"Invalid submission filename '{name}'. Expected teamN_<reference-stem>_runX.jsonl or dummy_<reference-stem>_runX.jsonl with X in 1..3."
        )
    team, reference_stem, run_number = match.groups()
    return SubmissionName(
        team=team,
        reference_stem=reference_stem,
        run=f"run{run_number}",
        filename=name,
    )


def parse_reference_filename(path_or_name: Path | str) -> ReferenceCell:
    name = Path(path_or_name).name
    match = REFERENCE_RE.match(name)
    if not match:
        raise ValueError(f"Invalid HIPE reference filename '{name}'.")
    return ReferenceCell(
        dataset=match.group("dataset"),
        split=match.group("split"),
        language=match.group("language"),
    )


def load_competition_config(path: Path) -> dict[str, Any]:
    return load_json(path)


def find_cell_for_reference(config: dict[str, Any], reference_filename: str) -> dict[str, Any] | None:
    cell = parse_reference_filename(reference_filename)
    for configured in config.get("cells", []):
        if (
            configured.get("dataset") == cell.dataset
            and configured.get("split") == cell.split
            and configured.get("language") == cell.language
        ):
            return configured
    return None


def read_info_file(info_path: Path) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    empty = {
        "info_file": info_path.name,
        "hipe_parameter_count": None,
        "team_parameter_count": None,
        "hipe_model_size": None,
        "team_model_size": None,
        "info_missing": True,
    }

    if not info_path.exists():
        warnings.append(f"Missing info file: {info_path.name}")
        return empty, warnings

    data = load_json(info_path)
    if not isinstance(data, dict):
        raise ValueError(f"{info_path.name} must contain a JSON object.")

    required = [
        "hipe_parameter_count",
        "team_parameter_count",
        "hipe_model_size",
        "team_model_size",
    ]
    for key in required:
        if key not in data:
            raise ValueError(f"{info_path.name} is missing required key '{key}'.")

    for key in ["hipe_parameter_count", "hipe_model_size"]:
        if not isinstance(data[key], (int, float)) or isinstance(data[key], bool):
            raise ValueError(f"{info_path.name} key '{key}' must be numeric.")

    return {
        "info_file": info_path.name,
        "hipe_parameter_count": data["hipe_parameter_count"],
        "team_parameter_count": data["team_parameter_count"],
        "hipe_model_size": data["hipe_model_size"],
        "team_model_size": data["team_model_size"],
        "info_missing": False,
    }, warnings


def competition_ranks(rows: list[dict[str, Any]], key: str, *, higher_is_better: bool) -> dict[tuple[str, str], int]:
    """Return competition ranks keyed by (team, run), with missing values ranked last."""
    total = len(rows)
    present = [row for row in rows if row.get(key) is not None]
    present.sort(key=lambda row: row[key], reverse=higher_is_better)

    ranks: dict[tuple[str, str], int] = {}
    previous_value = object()
    previous_rank = 0
    for index, row in enumerate(present, start=1):
        value = row[key]
        if value == previous_value:
            rank = previous_rank
        else:
            rank = index
            previous_value = value
            previous_rank = rank
        ranks[(row["team"], row["run"])] = rank

    for row in rows:
        ranks.setdefault((row["team"], row["run"]), total)

    return ranks


def tsv_escape(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\t", " ").replace("\n", " ")
