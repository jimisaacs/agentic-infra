from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
FMT_HOOK_PATH = REPO_ROOT / ".claude" / "hooks" / "fmt-on-edit.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


fmt_hook = load_module(FMT_HOOK_PATH, "template_fmt_hook")


class FmtOnEditTests(unittest.TestCase):
    def test_extract_file_path_from_tool_input(self) -> None:
        raw = '{"tool_input": {"file_path": "/tmp/example.py"}}'
        self.assertEqual(fmt_hook.extract_file_path(raw), "/tmp/example.py")

    def test_extract_file_path_from_top_level_path(self) -> None:
        raw = '{"path": "/tmp/example.py"}'
        self.assertEqual(fmt_hook.extract_file_path(raw), "/tmp/example.py")

    def test_extract_file_path_invalid_payload_returns_empty_string(self) -> None:
        self.assertEqual(fmt_hook.extract_file_path("{bad-json"), "")


if __name__ == "__main__":
    unittest.main()
