# Shared Platform MCP

This document defines the optional shared/org MCP plane that complements, but does not replace, the local `project-context` MCP.

## Purpose

The shared platform plane exists to reduce repeated effort across many agentic projects.

It can provide:

- paved-road bootstrap for new repos
- standards and architectural defaults
- reusable templates for rules, skills, MCP servers, and verification patterns
- cross-project or org-wide knowledge that does not belong in a single repo
- remote services such as reranking, policy lookup, or observability metadata

## Non-goals

The shared platform plane should not:

- become the only way a project can explain itself
- replace repo-local canonical truth
- require network access for routine local work
- hide trust boundaries between local facts and remote guidance

## Responsibilities

### 1. Bootstrap

Help a new repo adopt a strong baseline:

- repo structure recommendations
- initial MCP and control-plane scaffolding
- starter rules, skills, decisions, and verification patterns

### 2. Standards

Provide shared best practices that are bigger than a single repo:

- naming and layout conventions
- safe default MCP contracts
- verification and rollout expectations
- guidance for when to promote a choice into DEC or ADR form

### 3. Cross-project intelligence

Offer optional context that a single repo cannot author alone:

- platform docs
- cross-repo patterns
- known architectural precedents
- reusable migration and review heuristics

### 4. Optional services

Supply remote capabilities only when they help materially:

- reranking
- remote retrieval over approved corpora
- policy enforcement or standards lookup
- observability or fleet-level metadata

## Trust boundary

The local repo remains authoritative for its own truth.

The shared plane can advise, enrich, or rank, but it should not silently override:

- canonical repo files
- local decisions and invariants
- local setup and verification state

Any time the shared plane influences a local answer, the local MCP should preserve that provenance clearly.

## Rollout model

Recommended order:

1. local `project-context` MCP first
2. shared bootstrap and standards second
3. shared retrieval or reranking only when local value is already proven

This sequence keeps the project operable in a standalone mode and prevents platform dependency from outrunning local correctness.

## Open questions

The shared plane still has load-bearing open questions around:

- trust and auth boundaries
- privacy and corpus eligibility
- what can be cached or mirrored locally
- how much remote policy should shape local answers

Those forks should stay in the decision backlog until the platform work is actually forced.

## Links

- [agentic-project-infra.md](agentic-project-infra.md)
- [project-context-mcp.md](project-context-mcp.md)
- [git-derived-memory.md](git-derived-memory.md)
- [../decisions/backlog.md](../decisions/backlog.md)
