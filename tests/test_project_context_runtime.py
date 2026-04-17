from __future__ import annotations

import importlib
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

runtime = importlib.import_module("scripts.project_context.runtime")


class ProjectContextRuntimeTests(unittest.TestCase):
    def test_allowlist_and_denylist_rules(self) -> None:
        self.assertTrue(runtime.is_allowlisted_relative("README.md"))
        self.assertTrue(runtime.is_allowlisted_relative("docs/design/README.md"))
        self.assertFalse(runtime.is_allowlisted_relative(".env"))
        self.assertTrue(runtime.is_denylisted_relative(".env"))

    def test_classify_relative_path(self) -> None:
        self.assertEqual(runtime.classify_relative_path("README.md"), "curated")
        self.assertEqual(runtime.classify_relative_path("docs/design/README.md"), "narrative")
        self.assertEqual(runtime.classify_relative_path(".genai/rules/core.md"), "canonical")

    def test_normalize_repo_relative_preserves_dotted_prefixes(self) -> None:
        self.assertEqual(runtime.normalize_repo_relative(".cursor/learnings.md"), ".cursor/learnings.md")
        self.assertEqual(runtime.normalize_repo_relative("./README.md"), "README.md")

    def test_hook_status_detects_current_wrapper(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            source = repo_root / ".githooks" / "pre-commit"
            installed_hooks_dir = repo_root / "installed-hooks"
            target = installed_hooks_dir / "pre-commit"
            source.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            source.write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            status = runtime.hook_status(repo_root, installed_hooks_dir=installed_hooks_dir)
            self.assertTrue(status["pre-commit"]["installed"])
            self.assertTrue(status["pre-commit"]["current"])

    def test_resolve_allowlisted_path_blocks_traversal_to_denylisted_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
            repo_root = Path(tmp_dir)
            (repo_root / "docs" / "design").mkdir(parents=True)
            target = repo_root / ".env"
            target.write_text("SECRET=1\n", encoding="utf-8")
            resolved = runtime.resolve_allowlisted_path("docs/design/../../../.env", repo_root)
            self.assertIsNone(resolved)


if __name__ == "__main__":
    unittest.main()
