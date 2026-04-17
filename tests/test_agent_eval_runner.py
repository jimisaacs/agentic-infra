from __future__ import annotations

import unittest

from scripts.agent_eval.runners.cursor import CursorRunner
from scripts.agent_eval.schema import RunnerOptions, Scenario


class CursorRunnerCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CursorRunner()
        if not self.runner.available():
            self.runner._binary = "/usr/local/bin/cursor"

    def _make_scenario(self, **overrides) -> Scenario:
        defaults = {
            "id": "test",
            "description": "test scenario",
            "prompt": "describe this repo",
            "workspace": ".",
            "runner": "cursor",
            "runner_options": RunnerOptions(),
        }
        defaults.update(overrides)
        return Scenario(**defaults)

    def test_basic_command(self) -> None:
        s = self._make_scenario()
        cmd = self.runner.build_command(s, "/repo")
        self.assertIn("agent", cmd)
        self.assertIn("-p", cmd)
        self.assertIn("describe this repo", cmd)
        self.assertIn("--workspace", cmd)
        self.assertIn("--output-format", cmd)

    def test_sandbox_option(self) -> None:
        s = self._make_scenario(runner_options=RunnerOptions(sandbox="disabled"))
        cmd = self.runner.build_command(s, "/repo")
        idx = cmd.index("--sandbox")
        self.assertEqual(cmd[idx + 1], "disabled")

    def test_mode_option(self) -> None:
        s = self._make_scenario(runner_options=RunnerOptions(mode="plan"))
        cmd = self.runner.build_command(s, "/repo")
        idx = cmd.index("--mode")
        self.assertEqual(cmd[idx + 1], "plan")

    def test_model_option(self) -> None:
        s = self._make_scenario(runner_options=RunnerOptions(model="gpt-5"))
        cmd = self.runner.build_command(s, "/repo")
        idx = cmd.index("--model")
        self.assertEqual(cmd[idx + 1], "gpt-5")

    def test_force_option(self) -> None:
        s = self._make_scenario(runner_options=RunnerOptions(force=True))
        cmd = self.runner.build_command(s, "/repo")
        self.assertIn("--force", cmd)

    def test_no_force_by_default(self) -> None:
        s = self._make_scenario()
        cmd = self.runner.build_command(s, "/repo")
        self.assertNotIn("--force", cmd)

    def test_workspace_path_resolution(self) -> None:
        s = self._make_scenario(workspace="project/web")
        cmd = self.runner.build_command(s, "/repo")
        idx = cmd.index("--workspace")
        self.assertIn("project/web", cmd[idx + 1])


if __name__ == "__main__":
    unittest.main()
