from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from .runners.base import RunResult
from .scoring import ScoreResult


def _serialize(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return obj


def eval_report(results: list[tuple[RunResult, ScoreResult]]) -> dict[str, Any]:
    """Produce a JSON-serializable eval summary."""
    scenarios = []
    for run, score in results:
        scenarios.append({
            "scenario_id": run.scenario_id,
            "passed": score.passed,
            "exit_code": run.exit_code,
            "duration_seconds": run.duration_seconds,
            "checks": [
                {"name": c.name, "passed": c.passed, "detail": c.detail}
                for c in score.checks
            ],
            "failure_count": len(score.failures),
        })
    passed = sum(1 for s in scenarios if s["passed"])
    total = len(scenarios)
    return {
        "ok": passed == total,
        "passed": passed,
        "total": total,
        "scenarios": scenarios,
    }


def demo_report(results: list[tuple[RunResult, ScoreResult]]) -> str:
    """Produce a human-readable markdown report for demo walkthroughs."""
    lines: list[str] = []
    lines.append("# Agent Eval Report")
    lines.append("")

    passed = sum(1 for _, s in results if s.passed)
    total = len(results)
    lines.append(f"**Result: {passed}/{total} scenarios passed**")
    lines.append("")

    lines.append("| Scenario | Status | Duration | Failures |")
    lines.append("|----------|--------|----------|----------|")
    for run, score in results:
        status = "PASS" if score.passed else "FAIL"
        failures = ", ".join(c.name for c in score.failures) or "-"
        lines.append(f"| {run.scenario_id} | {status} | {run.duration_seconds}s | {failures} |")

    lines.append("")
    for run, score in results:
        if not score.failures:
            continue
        lines.append(f"## {run.scenario_id}")
        lines.append("")
        for check in score.failures:
            lines.append(f"- **{check.name}**: {check.detail}")
        lines.append("")

    return "\n".join(lines)


def format_report(results: list[tuple[RunResult, ScoreResult]], mode: str = "eval") -> str:
    if mode == "demo":
        return demo_report(results)
    return json.dumps(eval_report(results), indent=2)
