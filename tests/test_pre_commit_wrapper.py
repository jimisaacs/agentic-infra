from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = REPO_ROOT / ".githooks" / "pre-commit"


def load_extensionless_module(path: Path, module_name: str):
    loader = importlib.machinery.SourceFileLoader(module_name, str(path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


pre_commit_hook = load_extensionless_module(HOOK_PATH, "baseline_pre_commit_hook")


class PreCommitWrapperTests(unittest.TestCase):
    def test_main_invokes_dev_verify_via_python(self) -> None:
        calls: list[tuple[list[str], dict[str, object]]] = []

        def fake_run(args: list[str], **kwargs: object) -> SimpleNamespace:
            calls.append((args, kwargs))
            if args == ["git", "rev-parse", "--show-toplevel"]:
                return SimpleNamespace(returncode=0, stdout=f"{REPO_ROOT}\n")
            return SimpleNamespace(returncode=7)

        with patch.object(pre_commit_hook.subprocess, "run", side_effect=fake_run):
            self.assertEqual(pre_commit_hook.main(), 7)

        self.assertEqual(len(calls), 2)
        self.assertEqual(
            calls[1][0],
            [pre_commit_hook.sys.executable, str(REPO_ROOT / "dev"), "verify"],
        )
        self.assertEqual(calls[1][1]["cwd"], REPO_ROOT)
        self.assertFalse(calls[1][1]["check"])


if __name__ == "__main__":
    unittest.main()
