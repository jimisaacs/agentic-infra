from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from ..schema import Scenario
from .base import RunResult


class CursorRunner:
    name = "cursor"

    def __init__(self) -> None:
        self._binary = shutil.which("cursor")

    def available(self) -> bool:
        return self._binary is not None

    def build_command(self, scenario: Scenario, workspace_root: str) -> list[str]:
        if self._binary is None:
            raise RuntimeError("cursor CLI not found on PATH")

        workspace = str(Path(workspace_root) / scenario.workspace)
        cmd = [
            self._binary, "agent",
            "-p", scenario.prompt,
            "--workspace", workspace,
            "--output-format", "text",
        ]

        opts = scenario.runner_options
        if opts.sandbox:
            cmd.extend(["--sandbox", opts.sandbox])
        if opts.mode:
            cmd.extend(["--mode", opts.mode])
        if opts.model:
            cmd.extend(["--model", opts.model])
        if opts.force:
            cmd.append("--force")

        return cmd

    def run(self, scenario: Scenario, workspace_root: str) -> RunResult:
        cmd = self.build_command(scenario, workspace_root)
        t0 = time.monotonic()
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        duration = time.monotonic() - t0
        return RunResult(
            scenario_id=scenario.id,
            stdout=proc.stdout,
            stderr=proc.stderr,
            exit_code=proc.returncode,
            duration_seconds=round(duration, 2),
            metadata={"command": cmd},
        )
