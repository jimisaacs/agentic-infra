# Learnings Index

Scan this file first. Then open only the matching section in `.genai/learnings.md`.

## Domains

- `Auth & Identity` — sessions, tokens, roles, tenant boundaries, transport vs application identity
- `Server` — service layout, repositories, APIs, scaling and concurrency conventions
- `Client/Frontend` — UI architecture, state, routing, real-time data patterns
- `Infrastructure` — containers, CI, build pipelines, deployment, observability
- `Process` — agent workflows, planning vs execution, handoffs, avoiding destructive automation

## Retrieval Pattern

1. Match the task to one or two domains.
2. Search `.genai/learnings.md` for the matching `##` or `###` heading.
3. Read only that section.
4. Append new learnings to the matching domain, then tighten this index if discovery would still be fuzzy.

## Growth Policy

- **Max 15 bullets per domain section.** When a section exceeds 15, archive the oldest or most situation-specific entries to an `### Archived` subsection at the bottom of that domain.
- **Review for staleness** when a milestone ships — remove entries about patterns that no longer exist or have been superseded.
- **Keep entries concise** — 1-2 sentences with enough context to prevent the mistake. If an entry needs a paragraph, it belongs in a rule or skill, not learnings.
