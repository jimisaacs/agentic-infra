# Agent Evals

Repeatable agent-behavior scenarios for this repo's teaching stack. Scenarios are canonical inputs; run artifacts are derived outputs that stay outside git.

## Quick Start

```bash
./dev eval list                    # see available scenarios
./dev eval run                     # run all scenarios
./dev eval run cold-start-orientation   # run one scenario
./dev eval report                  # show the latest run report
```

## Scenario Format

Each scenario is a JSON file under `evals/scenarios/`. Fields:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Stable identifier matching the filename |
| `description` | yes | What this scenario tests |
| `prompt` | yes | The prompt fed to the agent |
| `workspace` | no | Relative path within the repo (default: `.`) |
| `branch` | no | Expected branch context (reserved; not enforced by the harness yet) |
| `runner` | no | Runner to use: `cursor` (default) or `claude` |
| `runner_options` | no | Runner-specific options (mode, model, sandbox, force) |
| `expectations` | no | Scoring criteria (exit_code, required/forbidden phrases and patterns) |
| `tags` | no | Tags for filtering: `cold-start`, `demo`, `eval`, `stack-*` |

## Scenarios and Demos

Scenarios marked with the `demo` tag are intended for human presentation. A passing demo scenario is one you can confidently show in a live walkthrough. The eval harness validates them the same way it validates any other scenario -- the demo script is downstream of the eval corpus.

## Cross-Worktree Eval

The harness lives on `stack/6-evals`, but you can evaluate agents against any branch by pointing `--target` at a different worktree:

```bash
# from the stack/6-evals checkout
./dev eval run --target /path/to/worktree    # evaluate against another branch's worktree
```

Scenarios define relative workspace paths. The `--target` flag provides the root those paths resolve against. This keeps scenarios portable -- the same scenario can test cold-start behavior on `main` (no agent infra) and on `stack/5-rag` (full stack).

## Run Artifacts

Run artifacts are written to `.tmp-agent-evals/` (gitignored). Each run gets a timestamped directory containing per-scenario stdout, stderr, metadata, and a summary report.

## Report Formats

- `--format eval` (default): JSON summary with per-scenario pass/fail and check details
- `--format demo`: human-readable markdown report
