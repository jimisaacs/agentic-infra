# ADRs

This directory stores settled or superseded architectural decisions.

Use [template.md](template.md) to author a new record. The template includes a canonical minimal example that shows the expected shape and tone.
Backlog vs ADR workflow lives in [../README.md](../README.md).

## Statuses

- `accepted` — the current architectural decision
- `superseded` — replaced by a newer ADR

## Read Path

1. Use the table below to find the relevant ADR.
2. Read that one ADR in full.
3. Open linked design docs only if the ADR is not enough.

## Numbering

Name files `ADR-xxxx-short-slug.md` and add every new ADR back to the index below.

## Index

| ADR | Status | Decision | Tags | Links |
|---|---|---|---|---|
| `ADR-0001` | `accepted` | Derive agent memory from git-tracked canonical sources and never treat generated retrieval artifacts as canonical. | `memory`, `git`, `provenance` | [record](ADR-0001-git-derived-agent-memory.md) |
