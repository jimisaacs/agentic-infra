---
id: ADR-0002
status: accepted
date: 2026-04-15
tags: [mcp, retrieval, workflow]
decision: Provide a built-in local project-context MCP as the primary self-query interface, with shared platform MCP services remaining optional overlays.
supersedes: []
superseded_by: []
---

# ADR-0002 Project-Context MCP

## Decision statement

Provide a built-in local project-context MCP as the primary self-query interface, with shared platform MCP services remaining optional overlays.

## Context

- Agents need a low-token, structured way to ask a project about its own maps, decisions, evidence, and related files.
- Raw file search alone is not enough for fast recall, while a shared remote plane should not be required for ordinary local work.
- The project wants one strong self-query surface instead of many partially-overlapping ad hoc mechanisms.

## Decision

Standardize on a built-in local `project-context` MCP that exposes task-shaped verbs such as search, fetch, bundle, decisions, status, and rebuild in v1, with `changes` and `symbols` reserved for later phases. Allow a shared platform MCP to enrich local answers with templates, standards, reranking, or cross-project context, but keep the local plane operable on its own.

## Alternatives considered

- **No built-in MCP:** keeps the repo simpler, but forces agents to reconstruct the same context manually in every session.
- **Shared platform MCP as the primary interface:** centralizes behavior, but creates offline, trust, and rollout coupling too early.
- **One generic ask-anything endpoint:** flexible, but weaker for schema clarity, provenance, and composable workflow tooling.

## Consequences

- Projects need a small local setup and index lifecycle to support the MCP well.
- The MCP contract becomes part of the architecture that downstream templates should implement.
- Shared platform capabilities can evolve independently as additive services.

## Links

- [Project-context MCP](../../design/project-context-mcp.md)
- [Shared platform MCP](../../design/shared-platform-mcp.md)
- [Best-in-class agentic project infra](../../design/agentic-project-infra.md)
- [DEC-0002](../backlog.md)
