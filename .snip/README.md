# Snip Examples

This directory is a small teaching example for AI-friendly shell filtering.

It is intentionally optional: the template should still work without upstream `snip` installed, but `./dev snip ...` gives teams one obvious place to plug compact shell-output filters into their agent workflow.

## Included Examples

- `git-status.yaml` — compact `git status` output for agent turns
- `git-log.yaml` — compact recent history for fast context
- `dev-verify.yaml` — compact `./dev verify` summaries while preserving failures

## Setup

1. Install upstream [`snip`](https://github.com/edouard-claude/snip).
1. Point your local snip config at this repo's `.snip/` directory. A minimal example:

```toml
[filters]
dir = [
    "~/.config/snip/filters",
    "${env.PWD}/.snip",
]
```

1. Run commands through the wrapper:

```bash
./dev snip git status
./dev snip git log
./dev snip ./dev verify
```

Git commands passed through `./dev snip ...` still obey the repo's conservative git allowlist. Read-only inspection commands stay convenient; mutating git commands are blocked.

## Design Rules

- Passing commands should become shorter, not noisier.
- Failing commands must preserve the lines that make the problem actionable.
- Explicit flags should still let a user bypass compact defaults when raw output is needed.
