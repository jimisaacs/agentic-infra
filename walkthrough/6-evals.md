# Walkthrough: Agent Evals

You're on `stack/6-evals`. The full agentic stack is in place -- rules, agents, MCP server, persistence, and hybrid search. This layer adds the final piece: repeatable agent-behavior evaluation and curated demo scenarios.

## What changed

Open `scripts/agent_eval/`. This is a lightweight eval harness that runs agent scenarios through `cursor agent -p` and scores the output against expected signals. No vendor eval platform required -- scenarios are local JSON files, scoring is deterministic, and run artifacts stay outside git.

Open `evals/scenarios/`. Each JSON file defines one scenario: a prompt, a runner, expectations (required phrases, forbidden phrases, regex patterns, exit code), and tags. The format is human-editable and provider-agnostic.

Open `evals/README.md`. This is the map for the eval corpus -- format reference, quick start, and the relationship between eval scenarios and demo scripts.

## Why this is layer 6

Every earlier layer adds capability. This one proves the capability works:

- Layer 1 introduced rules and verification. Layer 6 verifies that a fresh agent actually follows those rules.
- Layer 2 introduced workflow commands. Layer 6 checks that an agent discovers and uses them.
- Layers 3-5 built a self-query surface. Layer 6 validates that agents orient correctly without hand-holding.

Starting with evals would have been premature -- you need something worth evaluating first. The correct ordering is: build the infrastructure, prove it works, then turn the proof into demos.

## The harness

The eval harness has three parts:

- **Runners** execute scenarios. The `v0` runner invokes `cursor agent -p` with workspace, sandbox, and model options. The runner interface (`runners/base.py`) is a protocol -- adding a Claude adapter later means implementing one class, not restructuring the harness.
- **Scoring** checks the output against expectations. Exit code, required phrases, forbidden phrases, and regex patterns. Lightweight and deterministic -- no LLM-as-judge.
- **Reporting** produces either a JSON eval summary or a human-readable markdown report. The demo report is presenter-friendly.

## Try it

```bash
./dev eval list                              # see available scenarios
./dev eval run                               # run all scenarios
./dev eval run cold-start-orientation        # run one scenario
./dev eval run --format demo                 # produce a demo-friendly report
./dev eval report                            # show the latest run report
```

## Cross-worktree eval

The harness lives here on `stack/6-evals`, but you can evaluate agents against any branch. Point `--target` at a worktree checked out to a different branch:

```bash
./dev eval run --target /path/to/worktree    # evaluate against another branch's worktree
```

This is the intended workflow. The same cold-start scenario can test whether an agent orients correctly on `main` (no agent infrastructure at all) versus `stack/5-rag` (full stack with retrieval). The scenarios stay the same -- only the target workspace changes.

## The full picture

You've now walked through the entire stack:

| Layer | What it adds | Walkthrough |
|-------|-------------|-------------|
| `main` | Human baseline: app, control plane, principles | `walkthrough/main.md` |
| `stack/1-core` | Agentic rules, guardrails, governance | `walkthrough/1-core.md` |
| `stack/2-agents-personas` | Review agents, personas, workflow commands | `walkthrough/2-agents-personas.md` |
| `stack/3-mcp` | Docs-first MCP server, in-memory backend | `walkthrough/3-mcp.md` |
| `stack/4-persistence` | LanceDB persistence | `walkthrough/4-persistence.md` |
| `stack/5-rag` | Vector embeddings, semantic search | `walkthrough/5-rag.md` |
| `stack/6-evals` | Agent eval harness, demo scenarios | `walkthrough/6-evals.md` |

Each layer builds on the previous one. No layer removes content from its parent. The stack is both a teaching tool and a working system.

## What to take away

- Evals are the proof layer, not an afterthought. If you can't measure agent behavior, you can't improve it.
- Demo scripts are downstream of the eval corpus. Passing scenarios become the basis for live walkthroughs.
- The harness is provider-agnostic. Scenarios are local truth; runners are adapters. Adding Claude or another runner doesn't change the scenarios.
- The control plane (`./dev`) grew again -- `./dev eval` joins `./dev verify`, `./dev context`, and the rest. Same pattern, new capability.
