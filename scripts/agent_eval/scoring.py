from __future__ import annotations

import re
from dataclasses import dataclass, field

from .runners.base import RunResult
from .schema import Expectations


@dataclass
class ScoreResult:
    scenario_id: str
    passed: bool
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def failures(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed]


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def score(run: RunResult, expectations: Expectations) -> ScoreResult:
    checks: list[CheckResult] = []
    output = run.stdout

    checks.append(CheckResult(
        name="exit_code",
        passed=run.exit_code == expectations.exit_code,
        detail=f"expected {expectations.exit_code}, got {run.exit_code}",
    ))

    for phrase in expectations.required_phrases:
        found = phrase.lower() in output.lower()
        checks.append(CheckResult(
            name=f"required_phrase:{phrase}",
            passed=found,
            detail="" if found else f"not found in output",
        ))

    for phrase in expectations.forbidden_phrases:
        found = phrase.lower() in output.lower()
        checks.append(CheckResult(
            name=f"forbidden_phrase:{phrase}",
            passed=not found,
            detail="" if not found else f"found in output",
        ))

    for pattern in expectations.required_patterns:
        matched = bool(re.search(pattern, output, re.IGNORECASE))
        checks.append(CheckResult(
            name=f"required_pattern:{pattern}",
            passed=matched,
            detail="" if matched else "pattern not matched",
        ))

    for pattern in expectations.forbidden_patterns:
        matched = bool(re.search(pattern, output, re.IGNORECASE))
        checks.append(CheckResult(
            name=f"forbidden_pattern:{pattern}",
            passed=not matched,
            detail="" if not matched else "pattern matched",
        ))

    return ScoreResult(
        scenario_id=run.scenario_id,
        passed=all(c.passed for c in checks),
        checks=checks,
    )
