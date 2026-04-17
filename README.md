# Agentic Infrastructure

This branch is the first agentic enhancement layer on top of the human project baseline in `main`. It keeps the same `project/` workspace and human `./dev`, then adds editor-agnostic rules, agent-facing maps, guardrails, AI-friendly shell helpers, and lightweight architecture governance.

## Quick Start

```bash
git checkout stack/1-core
./dev help
./dev doctor
./dev verify
./dev status
./dev stack up         # build and start (dev mode: file watcher)
./dev stack up --prod  # build and start (prod mode: one-shot build)
./dev stack reset      # remove all containers, images, and volumes
```

After `./dev stack up`, Pulse is at **http://localhost:3000**.

## What This Layer Adds

- `AGENTS.md` -- repo-wide agent guide
- `CLAUDE.md` -- Claude Code entrypoint
- `.genai/rules/` -- canonical rule prose (SSOT)
- `.cursor/rules/` -- thin Cursor wrappers around the SSOT rules
- `.claude/hooks/` -- shared guard and format-on-edit hooks
- `.snip/` -- AI-friendly shell output filters
- `docs/decisions/` and `docs/design/` -- governance and architecture depth

## What This Layer Adds

- `AGENTS.md` -- repo-wide agent guide
- `CLAUDE.md` -- Claude Code entrypoint
- `.genai/rules/` -- canonical rule prose (SSOT)
- `.cursor/rules/` -- thin Cursor wrappers around the SSOT rules
- `.claude/hooks/` -- shared guard and format-on-edit hooks
- `.snip/` -- AI-friendly shell output filters
- `docs/decisions/` and `docs/design/` -- governance and architecture depth

## Project Pattern


- Start with [project/README.md](project/README.md) for the ecosystem/target layout.
- Read [docs/PRINCIPLES.md](docs/PRINCIPLES.md) for the engineering philosophy.
- Read [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for coding standards.
- Read [docs/guides/development.md](docs/guides/development.md) for the development workflow.
- Use `./dev` to verify and inspect the template.

## Worked Example

The repo also carries a small `project/` workspace so the infrastructure has something real to govern. Treat repo root as the agent-infra layer and `project/` as the example downstream app surface; start at `project/README.md` only when the task touches that sample app or its layout.

## Advanced Path

For review agents, workflow commands, persona-driven delivery, and swarm orchestration:

- `.genai/commands/` — 22 workflow commands (SSOT); `.cursor/commands/` for Cursor slash commands
- `.genai/agents/` — 7 reviewer definitions; `.cursor/agents/` for Cursor agent launch
- `.genai/personas/` — optional review persona catalog
- `.genai/swarm-roster/` — role model for multi-agent review

## Repo Structure

| Path | Purpose |
| ---- | ------- |
| `.genai/rules/` | Canonical rule prose (SSOT) |
| `.genai/commands/` | Workflow commands (SSOT) |
| `.genai/agents/` | Reviewer definitions (SSOT) |
| `.genai/skills/` | On-demand depth docs (SSOT) |
| `.genai/personas/` | Review persona catalog |
| `.genai/swarm-roster/` | Swarm role model |
| `.cursor/rules/` | Cursor wrappers (`.mdc` frontmatter + `@` references) |
| `.cursor/commands/` | Cursor slash command wrappers |
| `.cursor/agents/` | Cursor agent wrappers |
| `.claude/hooks/` | Guard, format-on-edit, and git hook scripts |
| `.githooks/` | Thin Git hook wrappers |
| `.snip/` | AI-friendly shell output filters |
| `project/` | Worked-example product workspace organized by ecosystem and target; see `project/README.md` |
| `docs/decisions/` | ADR/DEC governance framework |
| `docs/design/` | Architecture docs and stack guide |

## Stack Architecture

This repo uses a stacked branch model. Each branch builds on the previous one, teaching one layer of agentic infrastructure at a time. See [docs/design/stack/README.md](docs/design/stack/README.md) for the full guide.
