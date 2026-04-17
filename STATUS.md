# Status

This file models a lightweight status doc for a teaching-first project.

## Current State

- Core path exists: `README.md`, `AGENTS.md`, `CLAUDE.md`, and `./dev` should be enough to understand and operate the template.
- Verification is real: `./dev verify` checks required paths, Python syntax, guard behavior, unit tests, JSON config parsing, markdown links, doc-contract promises, and formatting drift.
- Rules are SSOT: `.genai/rules/` is the canonical source of truth for rule prose; `.cursor/rules/*.mdc` are thin wrappers.
- The worked-example app under `project/` is explicitly mapped, with layout guidance in `project/README.md` and `project-layout` rule coverage for agents.
- SSOT pattern extended: `.genai/commands/`, `.genai/agents/`, `.genai/skills/`, `.genai/learnings*.md` are canonical; `.cursor/` versions are thin wrappers.
- Advanced layers stay available: personas, swarm roster docs, specialist reviewers, and workflow commands remain in the repo but should not be required reading for day-one use.

- Local self-query is real: `./dev setup` bootstraps a docs-first `project-context` runtime and `./dev context ...` exposes status, rebuild, search, smoke, and serve operations.

- Agent eval harness is real: `./dev eval` runs repeatable agent-behavior scenarios, scores output against expected signals, and produces eval or demo reports. Scenarios live under `evals/scenarios/` as canonical local truth.

## What Works Now

- A downstream project can copy this template and start from one control-plane entrypoint.
- The top-level docs point at real files instead of placeholder paths.
- The guard enforces a conservative shell allowlist for agent safety.
- Cursor can register a local `project-context` MCP through `.cursor/mcp.json` once the runtime is bootstrapped.
- Claude Code can register the same MCP through `.claude/mcp.json`.
- The local MCP currently exposes a thin docs-first tool surface: `search`, `fetch`, `bundle`, `decisions`, `status`, and `rebuild`.
- The docs-first index is stored under `.project-context/`, outside git, and remains non-canonical derived memory.
- Review delivery has a richer persona/swarm system without forcing it into the first-read path.
- The agent eval harness runs cold-start scenarios via `cursor agent -p` and scores them deterministically. Run artifacts are derived and gitignored.

## What To Customize Downstream

- Replace the project description, stack, layout, invariants, and commands in `AGENTS.md`.
- Decide whether the advanced review-persona and swarm-roster layers are valuable for your team or should stay dormant.
- Replace the placeholder roadmap and status language with product-specific truth once the template lands in a real repo.
