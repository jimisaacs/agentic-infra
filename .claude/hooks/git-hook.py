#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def repo_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return Path(proc.stdout.strip()).resolve()


def run_pre_commit(root: Path) -> int:
    proc = subprocess.run([str(root / "dev"), "verify"], cwd=root, check=False)
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if not args:
        print("expected hook name", file=sys.stderr)
        return 2
    root = repo_root()
    hook_name = args[0]
    if hook_name == "pre-commit":
        return run_pre_commit(root)
    print(f"unsupported hook: {hook_name}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
