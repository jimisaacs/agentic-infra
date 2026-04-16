from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = REPO_ROOT / ".claude" / "hooks" / "guard.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


guard = load_module(GUARD_PATH, "template_guard")


class GuardTests(unittest.TestCase):
    def test_extract_command_from_json(self) -> None:
        raw = '{"tool_input": {"command": "git status"}}'
        self.assertEqual(guard.extract_command(raw), "git status")

    def test_extract_command_fallback_from_raw_string(self) -> None:
        raw = '"command": "git log --oneline -1"'
        self.assertEqual(guard.extract_command(raw), "git log --oneline -1")

    def test_extract_command_invalid_payload_returns_none(self) -> None:
        self.assertIsNone(guard.extract_command("{not-json"))

    def test_evaluate_command_allows_status(self) -> None:
        self.assertEqual(guard.evaluate_command("git status"), 0)

    def test_evaluate_command_blocks_compound_shell(self) -> None:
        self.assertEqual(guard.evaluate_command("git status && git commit -m test"), 2)

    def test_evaluate_command_blocks_repo_hop(self) -> None:
        self.assertEqual(guard.evaluate_command("git -C /tmp status"), 2)


if __name__ == "__main__":
    unittest.main()
