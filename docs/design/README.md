# Design Docs

This directory holds the upstream architecture and product thesis for the system used to build this template.

The template should implement the stable conclusions from these docs. It should not copy the full rationale, research trail, or open forks into downstream projects.

## Read Path

1. Read [agentic-project-infra.md](agentic-project-infra.md) for the reference architecture and artifact strategy.
2. Read [stack/README.md](stack/README.md) for the layered branch guide and per-layer teaching story.
3. Use [../decisions/backlog.md](../decisions/backlog.md) for open load-bearing forks and [../decisions/adr/README.md](../decisions/adr/README.md) for settled decisions.

## What Lives Here

| File | Role |
| ---- | ---- |
| `agentic-project-infra.md` | Reference architecture, principles, invariants, and template relationship |
| `stack/README.md` | Layered branch guide for the teaching stack |

## Boundaries

- `docs/design/` explains the deep architecture and why this system should work this way.
- `docs/decisions/` records compact open forks and settled choices.
- `README.md`, `AGENTS.md`, and `CLAUDE.md` stay map-level and point here when depth is needed.
