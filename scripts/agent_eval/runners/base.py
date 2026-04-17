from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from ..schema import Scenario


@dataclass
class RunResult:
    scenario_id: str
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    metadata: dict[str, Any] = field(default_factory=dict)


class Runner(Protocol):
    """Protocol that all runner adapters must implement."""

    name: str

    def run(self, scenario: Scenario, workspace_root: str) -> RunResult:
        """Execute a scenario and return the result."""
        ...
