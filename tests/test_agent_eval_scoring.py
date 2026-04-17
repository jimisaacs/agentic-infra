from __future__ import annotations

import unittest

from scripts.agent_eval.runners.base import RunResult
from scripts.agent_eval.schema import Expectations
from scripts.agent_eval.scoring import score


def _make_run(stdout: str = "", exit_code: int = 0) -> RunResult:
    return RunResult(
        scenario_id="test",
        stdout=stdout,
        stderr="",
        exit_code=exit_code,
        duration_seconds=1.0,
    )


class ScoringTests(unittest.TestCase):
    def test_pass_on_empty_expectations(self) -> None:
        result = score(_make_run(), Expectations())
        self.assertTrue(result.passed)
        self.assertEqual(len(result.failures), 0)

    def test_exit_code_mismatch(self) -> None:
        result = score(_make_run(exit_code=1), Expectations(exit_code=0))
        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].name, "exit_code")

    def test_required_phrase_present(self) -> None:
        result = score(_make_run(stdout="hello ./dev world"), Expectations(required_phrases=["./dev"]))
        self.assertTrue(result.passed)

    def test_required_phrase_missing(self) -> None:
        result = score(_make_run(stdout="no match here"), Expectations(required_phrases=["./dev"]))
        self.assertFalse(result.passed)

    def test_required_phrase_case_insensitive(self) -> None:
        result = score(_make_run(stdout="See AGENTS.md"), Expectations(required_phrases=["agents.md"]))
        self.assertTrue(result.passed)

    def test_forbidden_phrase_absent(self) -> None:
        result = score(_make_run(stdout="all good"), Expectations(forbidden_phrases=["error"]))
        self.assertTrue(result.passed)

    def test_forbidden_phrase_present(self) -> None:
        result = score(_make_run(stdout="I don't have access"), Expectations(forbidden_phrases=["I don't have access"]))
        self.assertFalse(result.passed)

    def test_required_pattern_matched(self) -> None:
        result = score(_make_run(stdout="use gt sync here"), Expectations(required_patterns=[r"gt (sync|restack)"]))
        self.assertTrue(result.passed)

    def test_required_pattern_not_matched(self) -> None:
        result = score(_make_run(stdout="no graphite commands"), Expectations(required_patterns=[r"gt (sync|restack)"]))
        self.assertFalse(result.passed)

    def test_forbidden_pattern_absent(self) -> None:
        result = score(_make_run(stdout="clean output"), Expectations(forbidden_patterns=[r"error|fatal"]))
        self.assertTrue(result.passed)

    def test_forbidden_pattern_present(self) -> None:
        result = score(_make_run(stdout="fatal: something broke"), Expectations(forbidden_patterns=[r"error|fatal"]))
        self.assertFalse(result.passed)

    def test_multiple_checks(self) -> None:
        result = score(
            _make_run(stdout="./dev verify passed", exit_code=0),
            Expectations(
                exit_code=0,
                required_phrases=["./dev verify"],
                forbidden_phrases=["command not found"],
            ),
        )
        self.assertTrue(result.passed)
        self.assertEqual(len(result.checks), 3)


if __name__ == "__main__":
    unittest.main()
