from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunnerOptions:
    mode: str | None = None
    model: str | None = None
    sandbox: str = "enabled"
    force: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RunnerOptions:
        return cls(
            mode=data.get("mode"),
            model=data.get("model"),
            sandbox=data.get("sandbox", "enabled"),
            force=data.get("force", False),
        )


@dataclass
class Expectations:
    exit_code: int = 0
    required_phrases: list[str] = field(default_factory=list)
    forbidden_phrases: list[str] = field(default_factory=list)
    required_patterns: list[str] = field(default_factory=list)
    forbidden_patterns: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Expectations:
        return cls(
            exit_code=data.get("exit_code", 0),
            required_phrases=data.get("required_phrases", []),
            forbidden_phrases=data.get("forbidden_phrases", []),
            required_patterns=data.get("required_patterns", []),
            forbidden_patterns=data.get("forbidden_patterns", []),
        )


@dataclass
class Scenario:
    id: str
    description: str
    prompt: str
    workspace: str = "."
    branch: str | None = None
    runner: str = "cursor"
    runner_options: RunnerOptions = field(default_factory=RunnerOptions)
    expectations: Expectations = field(default_factory=Expectations)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Scenario:
        return cls(
            id=data["id"],
            description=data["description"],
            prompt=data["prompt"],
            workspace=data.get("workspace", "."),
            branch=data.get("branch"),
            runner=data.get("runner", "cursor"),
            runner_options=RunnerOptions.from_dict(data.get("runner_options", {})),
            expectations=Expectations.from_dict(data.get("expectations", {})),
            tags=data.get("tags", []),
        )


def validate_scenario(data: dict[str, Any]) -> list[str]:
    """Return a list of validation errors, empty if valid."""
    errors: list[str] = []
    for required in ("id", "description", "prompt"):
        if required not in data:
            errors.append(f"missing required field: {required}")
    if "id" in data and not isinstance(data["id"], str):
        errors.append("field 'id' must be a string")
    if "runner" in data and data["runner"] not in ("cursor", "claude"):
        errors.append(f"unsupported runner: {data['runner']}")
    if "expectations" in data:
        exp = data["expectations"]
        if not isinstance(exp, dict):
            errors.append("field 'expectations' must be an object")
        elif "exit_code" in exp and not isinstance(exp["exit_code"], int):
            errors.append("expectations.exit_code must be an integer")
    return errors


def load_scenario(path: Path) -> Scenario:
    """Load and validate a single scenario file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_scenario(data)
    if errors:
        raise ValueError(f"invalid scenario {path.name}: {'; '.join(errors)}")
    return Scenario.from_dict(data)


def load_scenarios(scenarios_dir: Path, tags: list[str] | None = None) -> list[Scenario]:
    """Load all scenarios from a directory, optionally filtered by tags."""
    if not scenarios_dir.is_dir():
        return []
    scenarios = []
    for path in sorted(scenarios_dir.glob("*.json")):
        scenario = load_scenario(path)
        if tags and not any(t in scenario.tags for t in tags):
            continue
        scenarios.append(scenario)
    return scenarios
