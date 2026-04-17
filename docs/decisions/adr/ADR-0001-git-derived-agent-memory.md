---
id: ADR-0001
status: accepted
date: 2026-04-15
tags: [memory, git, provenance]
decision: Derive agent memory from git-tracked canonical sources and never treat generated retrieval artifacts as canonical.
supersedes: []
superseded_by: []
---

# ADR-0001 Git-Derived Agent Memory

## Decision statement

Derive agent memory from git-tracked canonical sources and never treat generated retrieval artifacts as canonical.

## Context

- The project wants fast agent recall, semantic retrieval, and task-shaped context without replacing human-authored docs and code.
- Similarity search is useful, but it can surface stale or lower-authority material if provenance is weak.
- Git already provides the source ledger for authorship, review, and change history.

## Decision

Keep code, config, docs, rules, skills, learnings, and decision records as the canonical repo truth. Build embeddings, lexical indexes, symbol maps, summaries, and other retrieval artifacts as derived memory keyed back to those sources. Agents should cite canonical files whenever possible.

## Alternatives considered

- **Vector database as a primary memory ledger:** faster to query directly, but weakens provenance and risks drifting away from reviewable repo truth.
- **Raw markdown and code only with no derived memory:** simpler, but does not provide the fast recall and fuzzy retrieval expected from a best-in-class agentic project.
- **Shared remote memory as the first source of truth:** useful for org-wide intelligence, but too dependent on network and trust boundaries for the local project core.

## Consequences

- The system needs indexing, freshness, and rebuild mechanics.
- Storage backends can change without redefining canonical truth.
- Git history remains available as the provenance and change-intent layer for memory features.

## Links

- [Git-derived memory](../../design/git-derived-memory.md)
- [Best-in-class agentic project infra](../../design/agentic-project-infra.md)
- [DEC-0001](../backlog.md)
