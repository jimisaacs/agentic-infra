# Layer 6: Agent Evals

## What This Layer Teaches

How to build a repeatable, provider-agnostic eval harness that validates agent behavior against your repo's own conventions, and how to turn passing eval scenarios into reliable demo material.

## Why This Layer Exists

Earlier layers build agentic infrastructure: rules, agents, MCP, persistence, and retrieval. But none of them answer the question "does a fresh agent actually behave correctly in this repo?" Without measurement, you're trusting vibes.

This layer exists to close that loop:

- Run the same prompt against the same workspace repeatedly and get consistent, scorable results.
- Detect regressions when rules, docs, or tooling change.
- Provide curated, evidence-backed demo scenarios instead of ad hoc improvisation.

## Talking Points

### Evals as a capstone, not a prerequisite

This is the last layer for a reason. You need working infrastructure before you can measure it. Teams that start with evals before they have rules, agents, or a control plane end up testing nothing meaningful. This stack demonstrates the correct ordering: build it, make it durable, then prove it works.

### Local scenarios as source of truth

Scenarios live in `evals/scenarios/` as human-editable JSON files. They are git-tracked, version-controlled, and project-specific. Vendor eval platforms (OpenAI Evals API, Anthropic Evaluation Tool) can be useful for broader prompt evaluation, but they don't natively encode this repo's branch/worktree model, control-plane expectations, or teaching-stack semantics. Keep the truth local; use vendor tools as optional mirrors.

### Provider-agnostic runner interface

The runner protocol in `runners/base.py` defines `run(scenario) -> RunResult`. The Cursor runner invokes `cursor agent -p`; a future Claude runner would invoke `claude -p`. Same scenarios, same scoring, same artifacts. Only the execution path differs.

### Cross-worktree evaluation

The harness lives on `stack/6-evals`, but it evaluates agents against any branch. The `--target` flag points the runner at a different worktree:

```bash
./dev eval run --target /path/to/worktree
```

Scenarios define relative workspace paths; `--target` provides the root. This means the same cold-start scenario can measure agent behavior on `main` (no agent infra) and on `stack/5-rag` (full stack). The delta between those results is itself a teaching signal: it shows what each stack layer actually does for agent orientation.

### Deterministic scoring in v0

Scoring is intentionally lightweight: exit code checks, required/forbidden phrase matching, and regex patterns. No LLM-as-judge, no semantic similarity. This keeps results reproducible and explainable. Richer scoring can be added later without changing the scenario format.

### Demo scripts as downstream of eval

A demo scenario is just an eval scenario tagged `demo`. If it passes the eval harness, you can present it live with confidence. The demo report format (`--format demo`) produces presenter-friendly markdown. This eliminates the gap between "it worked when I tried it" and "it works reliably."

## What's In This Layer

| Path | Purpose |
|------|---------|
| `scripts/agent_eval/__init__.py` | Harness identity and constants |
| `scripts/agent_eval/cli.py` | CLI: run, list, report subcommands |
| `scripts/agent_eval/schema.py` | Scenario dataclass, loader, validation |
| `scripts/agent_eval/scoring.py` | Deterministic scoring against expectations |
| `scripts/agent_eval/reporting.py` | Eval (JSON) and demo (markdown) report generators |
| `scripts/agent_eval/runners/base.py` | Runner protocol defining the adapter contract |
| `scripts/agent_eval/runners/cursor.py` | Cursor CLI runner implementation |
| `evals/README.md` | Eval corpus map: format, usage, artifact policy |
| `evals/scenarios/*.json` | Canonical eval scenarios |
| `walkthrough/6-evals.md` | Human walkthrough for this layer |
| `docs/design/stack/6-evals.md` | This document |

## Try This Layer

```bash
./dev eval list                              # see available scenarios
./dev eval run                               # run all scenarios
./dev eval run cold-start-orientation        # run one specific scenario
./dev eval run --format demo                 # produce a demo-friendly report
./dev eval report                            # show the latest run report
./dev status                                 # see eval status in the control plane
```
