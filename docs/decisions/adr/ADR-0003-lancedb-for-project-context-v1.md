---
id: ADR-0003
status: accepted
date: 2026-04-15
tags: [storage, retrieval, v1]
decision: Use LanceDB as the local derived-memory backend for this repo's docs-first `project-context` v1 implementation.
supersedes: []
superseded_by: []
---

# ADR-0003 LanceDB For Project-Context V1

## Decision statement

Use LanceDB as the local derived-memory backend for this repo's docs-first `project-context` v1 implementation.

## Context

- The repo needed a real local backend to ship the first runnable `project-context` MCP rather than only design docs.
- ADR-0001 keeps derived memory non-canonical, so the storage backend can vary without redefining source-of-truth semantics.
- The architecture left the backend choice open until implementation pressure forced an actual v1.

## Decision

Adopt LanceDB for this repo's v1 docs-first index and search storage. Treat that as an implementation choice for this repo and this phase, not a permanent downstream template invariant.

## Alternatives considered

- **SQLite-based local storage:** simpler dependency story, but weaker fit for the intended semantic-search growth path.
- **Postgres plus `pgvector`:** heavier bootstrap and not local-first enough for the template's v1.
- **Remote vector store such as Qdrant:** conflicts with the local-first v1 boundary.

## Consequences

- `./dev setup` needs a Python 3.10+ runtime and the LanceDB dependency stack.
- Derived-memory artifacts remain outside git under `.project-context/`.
- Future phases may revisit the backend if ergonomics, performance, or downstream portability demand it.

## Links

- [Git-derived memory](../../design/git-derived-memory.md)
- [Project-context MCP](../../design/project-context-mcp.md)
- [DEC-0001](../backlog.md)
