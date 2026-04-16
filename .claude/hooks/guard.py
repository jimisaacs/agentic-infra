#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shlex
import sys

COMMAND_FALLBACK_PATTERNS = (
    re.compile(r'"command"\s*:\s*"([^"]*)"'),
    re.compile(r'"tool_input"\s*:\s*"([^"]*)"'),
)


def decode_json_string(value: str) -> str:
    try:
        return json.loads(f'"{value}"')
    except Exception:
        return value


def extract_command(raw: str) -> str | None:
    try:
        payload = json.loads(raw)
    except Exception:
        payload = None

    if isinstance(payload, dict):
        tool_input = payload.get("tool_input")
        candidates = [
            tool_input.get("command") if isinstance(tool_input, dict) else None,
            tool_input if isinstance(tool_input, str) else None,
            payload.get("command"),
        ]
        for value in candidates:
            if isinstance(value, str):
                return value

    for pattern in COMMAND_FALLBACK_PATTERNS:
        match = pattern.search(raw)
        if match:
            return decode_json_string(match.group(1))

    return None


def contains_compound_shell(command: str) -> bool:
    return any(token in command for token in ("&&", "||", ";", "|", "$(", "`", "\n"))


def allow_branch_listing(args: list[str]) -> bool:
    allowed_exact = {
        "--list",
        "-l",
        "--all",
        "-a",
        "--remotes",
        "-r",
        "--show-current",
        "--verbose",
        "-v",
        "--color",
        "--no-color",
        "--omit-empty",
    }
    allowed_prefixes = (
        "--sort=",
        "--column=",
        "--format=",
        "--contains=",
        "--no-contains=",
        "--merged=",
        "--no-merged=",
        "--points-at=",
    )
    return all(arg in allowed_exact or arg.startswith(allowed_prefixes) for arg in args)


def allow_worktree(args: list[str]) -> bool:
    if not args:
        return False
    if args[0] == "list":
        return all(arg in {"-v", "--verbose", "--porcelain"} for arg in args[1:])
    if args[0] in {"add", "remove", "prune"}:
        return True
    return False


def evaluate_command(command: str) -> int:
    if not command or command == "null":
        return 0

    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return 2 if "git" in command else 0

    git_index = -1
    for idx, token in enumerate(words):
        if token == "git" or os.path.basename(token) == "git":
            git_index = idx
            break
    if git_index < 0:
        return 0

    if contains_compound_shell(command):
        return 2

    subcmd = ""
    subcmd_index = -1
    i = git_index + 1
    while i < len(words):
        word = words[i]
        if word.startswith("-"):
            if word in {"-C", "--git-dir", "--work-tree", "-c"} or word.startswith(("--git-dir=", "--work-tree=")):
                return 2
            i += 1
            continue
        subcmd = word
        subcmd_index = i
        break

    if not subcmd:
        return 0

    remaining = words[subcmd_index + 1 :]
    if "--no-index" in remaining:
        return 2

    if subcmd in {"status", "diff", "log", "show", "blame", "fetch", "rev-parse", "ls-files"}:
        return 0
    if subcmd == "branch":
        return 0 if allow_branch_listing(remaining) else 2
    if subcmd == "worktree":
        return 0 if allow_worktree(remaining) else 2
    if subcmd in {"add", "commit", "push", "checkout", "switch", "rm"}:
        return 0
    return 2


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    command = extract_command(raw)
    if command is None:
        return 2
    return evaluate_command(command)


if __name__ == "__main__":
    raise SystemExit(main())
