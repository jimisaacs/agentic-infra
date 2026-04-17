# Git-Derived Memory

This document defines the memory model, indexing lifecycle, and workflow rules for the derived-memory layer.

## Memory model

| Layer | What it is | Examples | Authority |
| --- | --- | --- | --- |
| `Canonical` | Human-authored repo truth | code, config, rules, skills, learnings, ADRs, DECs | Highest |
| `Curated` | Fast routing surfaces | repo maps, README guides, indexes, ownership docs | High |
| `Derived` | Generated retrieval artifacts | chunks, embeddings, FTS, symbol tables, summaries | Support only |
| `Ephemeral` | Session and task state | branch/diff context, active work, transient notes | Temporary |
| `Shared` | Optional org/platform help | standards, templates, cross-project data, remote reranking | Contextual |

Agents may query any layer, but answers and actions should cite canonical sources whenever possible.

## Implementation status

Implemented in this repo's v1:

- docs-first allowlist corpus rooted in repo maps, rules, skills, learnings, decisions, and design docs
- explicit denylist for common secret-bearing or unsafe paths
- repo-local derived-memory storage under `.project-context/`, outside git
- full rebuild via `./dev context rebuild` and runtime smoke via `./dev context smoke`

Deferred past v1:

- incremental refresh
- code-symbol indexing
- history-aware retrieval beyond doc freshness
- shared semantic artifacts or transport

## Git-derived memory principle

Git remains the canonical ledger and provenance model.

That means:

- canonical content originates in git-tracked files
- derived memory is built from that content and keyed back to source paths and content identity
- generated retrieval artifacts do not become the source of truth just because they are easier to query
- history-aware retrieval should use Git as the record of sequence, authorship, and change intent

This design leaves room for git-shareable semantic artifacts later, but those artifacts remain secondary to canonical repo sources.

## Indexing lifecycle

### Setup

Project setup should build or hydrate the local derived-memory layer automatically, or at least offer one obvious command that does so.

### Initial corpus

The first phase should prefer high-signal repo knowledge:

- `README.md`
- `AGENTS.md`
- `.genai/rules/`
- `.cursor/skills/`
- `.cursor/learnings*`
- `docs/decisions/`
- selected repo maps and setup docs

Code indexing can follow once the docs-first path is working well.

### Incremental refresh

Refresh should be incremental when possible:

- detect changed files by hash or Git object identity
- update affected chunks and metadata only
- keep a visible freshness signal for each result
- expose rebuild state through the local MCP `status` and `rebuild` verbs

### Storage boundary

Derived artifacts should live outside Git by default. They are local cache, not authored content.

Examples:

- user cache directory
- local data directory under project control
- a project-local hidden path explicitly ignored from version control

This repo's v1 implementation uses the last option: `.project-context/`.

If a team later chooses to share hydrated semantic artifacts through Git or another transport, that should be treated as an optimization layer, not a replacement for local derivation.

## Local backend bias

The current preferred default for the first local implementation is LanceDB because it is embedded, local-first, and version-aware.

This is a planning bias, not a settled invariant. The storage backend remains an open implementation fork until the corresponding decision record is resolved.

Competing candidates include:

- SQLite plus lexical search and vector extension
- Postgres plus `pgvector`
- a dedicated remote vector store such as Qdrant

The choice should be driven by local ergonomics, provenance support, incremental update behavior, and simplicity for downstream projects.

## Chunking and retrieval

Recommended chunking strategy:

- Markdown by heading and subheading
- decision records by canonical sections
- code by symbol or syntax-aware unit
- history summaries by commit or change cluster when added

Recommended retrieval strategy:

- lexical retrieval plus vector retrieval, not vector-only retrieval
- explicit provenance in every result
- warnings for archived, superseded, or stale material
- preference for curated and canonical surfaces when they answer the question directly

## Workflow integration

Derived memory exists to improve agent workflows, not to create a second documentation system.

Expected uses:

- planning bundles that assemble maps, decisions, learnings, and recent changes
- review bundles that combine diffs, affected areas, tests, lints, and relevant ADRs
- debug bundles that surface ownership, failure evidence, and recent history
- onboarding bundles that explain the first verification path and core maps

Workflow commands should call the local MCP when curated routing is not enough. They should not duplicate the same logic in many places.

## Governance rules

- Update canonical docs when the truth changes.
- Regenerate derived memory when canonical inputs change.
- Record open architectural forks as DECs before they become implicit implementation choices.
- Record settled, load-bearing memory or MCP choices as ADRs.
- Prefer links to decision records and design docs instead of restating the same rationale in many files.

## Links

- [agentic-project-infra.md](agentic-project-infra.md)
- [project-context-mcp.md](project-context-mcp.md)
- [shared-platform-mcp.md](shared-platform-mcp.md)
- [../decisions/adr/ADR-0001-git-derived-agent-memory.md](../decisions/adr/ADR-0001-git-derived-agent-memory.md)
- [../decisions/backlog.md](../decisions/backlog.md)
