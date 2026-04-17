from __future__ import annotations

import importlib
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

corpus = importlib.import_module("scripts.project_context.corpus")


class ProjectContextCorpusTests(unittest.TestCase):
    def test_split_sections_builds_heading_path_labels(self) -> None:
        sections = corpus.split_sections(
            "README.md",
            textwrap.dedent(
                """
                # Title

                Intro.

                ## Setup

                Details.
                """
            ).strip(),
        )
        self.assertEqual(sections[0]["label"], "Title")
        self.assertEqual(sections[1]["label"], "Title > Setup")

    def test_build_corpus_indexes_allowlisted_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            (repo_root / "README.md").write_text("# Repo\n\n## Intro\n\nHello.\n", encoding="utf-8")
            (repo_root / "docs" / "design").mkdir(parents=True)
            (repo_root / "docs" / "design" / "README.md").write_text("# Design\n\nBody.\n", encoding="utf-8")
            chunks, warnings = corpus.build_corpus(repo_root)
            self.assertFalse(warnings)
            self.assertTrue(any(chunk.source_path == "README.md" for chunk in chunks))
            self.assertTrue(any(chunk.class_name == "narrative" for chunk in chunks))

    def test_matching_decisions_reads_backlog_and_adr_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            decisions_root = repo_root / "docs" / "decisions"
            (decisions_root / "adr").mkdir(parents=True)
            (decisions_root / "backlog.md").write_text(
                "| ID | Status | Decision | Trigger / deadline | Options / tension | Links / resolution |\n"
                "|---|---|---|---|---|---|\n"
                "| DEC-0001 | researching | Pick storage | before build | LanceDB vs SQLite | link |\n",
                encoding="utf-8",
            )
            (decisions_root / "adr" / "ADR-0001-storage.md").write_text(
                textwrap.dedent(
                    """
                    ---
                    id: ADR-0001
                    status: accepted
                    decision: Use git-derived memory
                    ---

                    # ADR-0001
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            matches = corpus.matching_decisions(repo_root, "storage")
            self.assertEqual(matches["backlog"][0]["id"], "DEC-0001")
            self.assertEqual(matches["adrs"][0]["id"], "ADR-0001")


if __name__ == "__main__":
    unittest.main()
