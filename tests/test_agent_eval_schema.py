from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.agent_eval.schema import (
    Expectations,
    RunnerOptions,
    Scenario,
    load_scenario,
    load_scenarios,
    validate_scenario,
)


class ValidateScenarioTests(unittest.TestCase):
    def test_valid_minimal(self) -> None:
        data = {"id": "test", "description": "desc", "prompt": "hello"}
        self.assertEqual(validate_scenario(data), [])

    def test_missing_required_fields(self) -> None:
        errors = validate_scenario({})
        self.assertIn("missing required field: id", errors)
        self.assertIn("missing required field: description", errors)
        self.assertIn("missing required field: prompt", errors)

    def test_invalid_runner(self) -> None:
        data = {"id": "x", "description": "d", "prompt": "p", "runner": "openai"}
        errors = validate_scenario(data)
        self.assertTrue(any("unsupported runner" in e for e in errors))

    def test_valid_runners(self) -> None:
        for runner in ("cursor", "claude"):
            data = {"id": "x", "description": "d", "prompt": "p", "runner": runner}
            self.assertEqual(validate_scenario(data), [])

    def test_invalid_exit_code_type(self) -> None:
        data = {"id": "x", "description": "d", "prompt": "p", "expectations": {"exit_code": "zero"}}
        errors = validate_scenario(data)
        self.assertTrue(any("exit_code" in e for e in errors))


class ScenarioFromDictTests(unittest.TestCase):
    def test_defaults(self) -> None:
        s = Scenario.from_dict({"id": "t", "description": "d", "prompt": "p"})
        self.assertEqual(s.workspace, ".")
        self.assertEqual(s.runner, "cursor")
        self.assertEqual(s.runner_options.sandbox, "enabled")
        self.assertEqual(s.expectations.exit_code, 0)
        self.assertEqual(s.tags, [])

    def test_full_scenario(self) -> None:
        data = {
            "id": "full",
            "description": "full test",
            "prompt": "hello",
            "workspace": "./sub",
            "branch": "stack/1-core",
            "runner": "cursor",
            "runner_options": {"mode": "plan", "model": "gpt-5", "sandbox": "disabled", "force": True},
            "expectations": {
                "exit_code": 1,
                "required_phrases": ["foo"],
                "forbidden_phrases": ["bar"],
                "required_patterns": ["f.o"],
                "forbidden_patterns": ["b.r"],
            },
            "tags": ["demo", "eval"],
        }
        s = Scenario.from_dict(data)
        self.assertEqual(s.branch, "stack/1-core")
        self.assertEqual(s.runner_options.mode, "plan")
        self.assertTrue(s.runner_options.force)
        self.assertEqual(s.expectations.exit_code, 1)
        self.assertEqual(s.expectations.required_phrases, ["foo"])
        self.assertIn("demo", s.tags)


class LoadScenarioTests(unittest.TestCase):
    def test_load_valid_file(self) -> None:
        data = {"id": "file-test", "description": "d", "prompt": "p"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            s = load_scenario(Path(f.name))
        self.assertEqual(s.id, "file-test")

    def test_load_invalid_file_raises(self) -> None:
        data = {"description": "missing id and prompt"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            f.flush()
            with self.assertRaises(ValueError):
                load_scenario(Path(f.name))


class LoadScenariosTests(unittest.TestCase):
    def test_empty_dir(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(load_scenarios(Path(d)), [])

    def test_missing_dir(self) -> None:
        self.assertEqual(load_scenarios(Path("/nonexistent")), [])

    def test_tag_filter(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            dp = Path(d)
            (dp / "a.json").write_text(json.dumps({"id": "a", "description": "d", "prompt": "p", "tags": ["demo"]}))
            (dp / "b.json").write_text(json.dumps({"id": "b", "description": "d", "prompt": "p", "tags": ["eval"]}))
            demos = load_scenarios(dp, tags=["demo"])
            self.assertEqual(len(demos), 1)
            self.assertEqual(demos[0].id, "a")


if __name__ == "__main__":
    unittest.main()
