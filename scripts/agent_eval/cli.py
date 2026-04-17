from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from . import ARTIFACTS_DIR, SCENARIOS_DIR
from .reporting import format_report
from .runners.base import RunResult
from .runners.claude import ClaudeRunner
from .runners.cursor import CursorRunner
from .schema import load_scenario, load_scenarios
from .scoring import ScoreResult, score


def _resolve_scenarios_dir(repo_root: Path) -> Path:
    return repo_root / SCENARIOS_DIR


def _resolve_artifacts_dir(repo_root: Path) -> Path:
    return repo_root / ARTIFACTS_DIR


def _get_runner(name: str) -> CursorRunner | ClaudeRunner:
    if name == "cursor":
        runner = CursorRunner()
        if not runner.available():
            print("error: cursor CLI not found on PATH", file=sys.stderr)
            raise SystemExit(1)
        return runner
    if name == "claude":
        runner = ClaudeRunner()
        if not runner.available():
            print("error: claude CLI not found on PATH", file=sys.stderr)
            raise SystemExit(1)
        return runner
    print(f"error: unsupported runner: {name}", file=sys.stderr)
    raise SystemExit(1)


def _write_artifact(artifacts_dir: Path, run_id: str, scenario_id: str, filename: str, content: str) -> Path:
    dest = artifacts_dir / run_id / scenario_id
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / filename
    path.write_text(content, encoding="utf-8")
    return path


def cmd_run(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    scenarios_dir = _resolve_scenarios_dir(repo_root)
    artifacts_dir = _resolve_artifacts_dir(repo_root)

    if args.scenario_ids:
        scenarios = []
        for sid in args.scenario_ids:
            path = scenarios_dir / f"{sid}.json"
            if not path.exists():
                print(f"error: scenario not found: {sid}", file=sys.stderr)
                return 1
            scenarios.append(load_scenario(path))
    else:
        tag_filter = args.tags.split(",") if args.tags else None
        scenarios = load_scenarios(scenarios_dir, tags=tag_filter)

    if not scenarios:
        print("no scenarios found")
        return 0

    target_root = Path(args.target).resolve() if args.target else repo_root
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    results: list[tuple[RunResult, ScoreResult]] = []

    if target_root != repo_root:
        print(f"target: {target_root}")

    for scenario in scenarios:
        print(f"running: {scenario.id} ...", end=" ", flush=True)
        runner = _get_runner(scenario.runner)
        run_result = runner.run(scenario, str(target_root))
        score_result = score(run_result, scenario.expectations)
        results.append((run_result, score_result))

        _write_artifact(artifacts_dir, run_id, scenario.id, "stdout.txt", run_result.stdout)
        _write_artifact(artifacts_dir, run_id, scenario.id, "stderr.txt", run_result.stderr)
        _write_artifact(artifacts_dir, run_id, scenario.id, "meta.json", json.dumps({
            "scenario_id": scenario.id,
            "exit_code": run_result.exit_code,
            "duration_seconds": run_result.duration_seconds,
            "passed": score_result.passed,
            "command": run_result.metadata.get("command", []),
            "target": str(target_root),
        }, indent=2))

        status = "PASS" if score_result.passed else "FAIL"
        print(f"{status} ({run_result.duration_seconds}s)")

    report = format_report(results, mode=args.format)
    report_path = _write_artifact(artifacts_dir, run_id, "", f"report.{'md' if args.format == 'demo' else 'json'}", report)

    print(f"\nrun: {run_id}")
    print(f"report: {report_path}")
    print(report)

    passed = sum(1 for _, s in results if s.passed)
    return 0 if passed == len(results) else 1


def cmd_list(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    scenarios_dir = _resolve_scenarios_dir(repo_root)
    tag_filter = args.tags.split(",") if args.tags else None
    scenarios = load_scenarios(scenarios_dir, tags=tag_filter)
    if not scenarios:
        print("no scenarios found")
        return 0
    print(f"{'ID':<30} {'RUNNER':<10} {'TAGS':<30} DESCRIPTION")
    for s in scenarios:
        tags = ", ".join(s.tags) if s.tags else "-"
        print(f"{s.id:<30} {s.runner:<10} {tags:<30} {s.description}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    artifacts_dir = _resolve_artifacts_dir(repo_root)
    if args.run_id:
        run_dir = artifacts_dir / args.run_id
    else:
        runs = sorted(artifacts_dir.iterdir()) if artifacts_dir.is_dir() else []
        runs = [r for r in runs if r.is_dir()]
        if not runs:
            print("no runs found")
            return 0
        run_dir = runs[-1]

    for ext in ("json", "md"):
        report_path = run_dir / f"report.{ext}"
        if report_path.exists():
            print(report_path.read_text(encoding="utf-8"))
            return 0
    print(f"no report found in {run_dir}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-eval")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run eval scenarios")
    run_parser.add_argument("scenario_ids", nargs="*", help="Specific scenario IDs to run (default: all)")
    run_parser.add_argument("--tags", help="Comma-separated tag filter")
    run_parser.add_argument("--target", help="Workspace root to evaluate against (default: repo root; use for cross-worktree eval)")
    run_parser.add_argument("--format", choices=["eval", "demo"], default="eval", help="Report format")
    run_parser.set_defaults(func=cmd_run)

    list_parser = subparsers.add_parser("list", help="List available scenarios")
    list_parser.add_argument("--tags", help="Comma-separated tag filter")
    list_parser.set_defaults(func=cmd_list)

    report_parser = subparsers.add_parser("report", help="Show results from a previous run")
    report_parser.add_argument("run_id", nargs="?", help="Run ID (default: latest)")
    report_parser.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
