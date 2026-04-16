#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def extract_file_path(raw: str) -> str:
    try:
        payload = json.loads(raw)
    except Exception:
        return ""

    candidates = [
        payload.get("tool_input", {}).get("file_path"),
        payload.get("tool_input", {}).get("path"),
        payload.get("file_path"),
        payload.get("path"),
    ]
    for value in candidates:
        if isinstance(value, str):
            return value
    return ""


def main() -> int:
    raw = sys.stdin.read()
    file_path = extract_file_path(raw)
    if not file_path:
        return 0

    target = Path(file_path)
    if not target.exists() or not target.is_file():
        return 0

    try:
        subprocess.run(
            [str(REPO_ROOT / "dev"), "fmt", str(target)],
            cwd=REPO_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception:
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
