# Python

Python serves two roles: infrastructure (control plane, hooks, guard -- stdlib only) and runtime (MCP server, eval harness on later layers -- managed dependencies via lockfiles).

## Infrastructure Python (dev, hooks, guard)

Standard library only. No third-party imports. Must run on Python 3.10+ without `pip install`.

- `from __future__ import annotations` in every file
- Type hints: `list[str]`, `dict[str, object]`, `X | None`
- `subprocess.run` with `capture_output=True, check=False` and explicit returncode handling
- Terminal output respects `NO_COLOR`, `CLICOLOR_FORCE`, `TERM`, `isatty()`
- No classes unless the abstraction earns its weight
- Testing: stdlib `unittest` in `tests/` at repo root

The `dev` script is a single-file CLI with `argparse`. Layer detection uses sentinel files (`_has_layerN()`). Each `cmd_*` function is one subcommand returning 0 for success.

The guard (`.claude/hooks/guard.py`) enforces the git allowlist from the `cli` rule. If you change the allowlist, update the corresponding test.

## Runtime Python (scripts/)

Uses managed dependencies via lockfiles. Same conventions as infrastructure (type hints, explicit errors, no global state) but may import third-party packages.

## Anti-patterns

- Don't add third-party imports to `dev` or hooks
- Don't use `os.system` -- use `subprocess.run`
- Don't swallow subprocess errors
- Don't add global state
- Don't skip updating tests when changing infrastructure code
