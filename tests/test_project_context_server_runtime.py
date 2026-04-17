from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"


class ProjectContextServerRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        if not VENV_PYTHON.exists():
            self.skipTest("project-context runtime is not bootstrapped")

    def run_runtime(self, script: str) -> dict[str, object]:
        proc = subprocess.run(
            [str(VENV_PYTHON), "-c", script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        return json.loads(proc.stdout)

    def test_fetch_allowlisted_file_returns_contract_fields(self) -> None:
        payload = self.run_runtime(
            """
from pathlib import Path
from scripts.project_context.cli import rebuild_index
from scripts.project_context.server import fetch
import json

repo_root = Path(".").resolve()
rebuild_index(repo_root)
payload = fetch(source_path="README.md")
print(json.dumps(payload))
"""
        )
        self.assertTrue(payload["ok"])
        item = payload["items"][0]
        for key in ("source_path", "stable_id", "label", "class", "freshness", "score_rationale", "warnings"):
            self.assertIn(key, item)

    def test_bundle_plan_feature_returns_docs_first_results(self) -> None:
        payload = self.run_runtime(
            """
from pathlib import Path
from scripts.project_context.cli import rebuild_index
from scripts.project_context.server import bundle
import json

repo_root = Path(".").resolve()
rebuild_index(repo_root)
payload = bundle(kind="plan_feature", topic="control plane", limit=3)
print(json.dumps(payload))
"""
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["kind"], "plan_feature")
        self.assertTrue(payload["results"])


if __name__ == "__main__":
    unittest.main()
