# Project-Context MCP

This document defines the built-in local MCP that lets an agentic project answer questions about itself quickly, with provenance and low token cost.

## Purpose

The `project-context` MCP is the repo's primary self-query interface.

It should help an agent answer questions like:

- What is this area and where should I read first?
- What decisions constrain this work?
- What changed recently and what might regress?
- Which files, symbols, or docs are most relevant to this task?
- What evidence says this understanding is current?

It should not replace the canonical files themselves. It should route to them, retrieve from them, and package them efficiently.

## Implementation status

Implemented in this repo's v1:

- bootstrap via `./dev setup`
- local stdio registration through `.cursor/mcp.json` using `./dev context serve`
- docs-first index over the allowlisted corpus
- tools: `search`, `fetch`, `bundle`, `decisions`, `status`, `rebuild`
- bundle shapes: `onboarding`, `understand_component`, `plan_feature`

Deferred past v1:

- MCP resources
- MCP prompts
- `changes`
- `symbols`
- `review_change` and `debug_area` bundles
- shared-platform delegation

## Availability

- The local server should be available after project setup.
- It should work offline against the current clone.
- It should not require a shared platform service for normal repo work.

## Capability surface

The lists below describe the long-term surface area. V1 implements only the subset called out in **Implementation status** above.

### Tools

- `search`: docs-first retrieval in v1, with broader hybrid retrieval over docs, code, decisions, learnings, and optional change summaries as the long-term target
- `fetch`: retrieve a canonical document, file slice, or cited chunk by path or stable identifier
- `bundle`: assemble task-shaped context for common workflows
- `decisions`: surface relevant DEC and ADR records with status awareness
- `changes`: summarize recent diffs, touched areas, and likely blast radius
- `symbols`: resolve modules, symbols, owners, and related files when code indexing exists
- `status`: report index freshness, corpus coverage, ignored paths, and rebuild health
- `rebuild`: rebuild or incrementally refresh local derived memory

### Resources

The server should expose a small set of stable resources that downstream tooling can read directly:

- `repo://map` - repo map and first-read path
- `repo://decisions/open` - active DEC backlog view
- `repo://decisions/adr-index` - ADR index and statuses
- `repo://learnings/index` - learnings domains and routing
- `repo://status/index` - setup, verification, and other current-state pointers when present
- `repo://active-areas` - current parallel-work visibility when present

### Prompts

If prompts are implemented, they should be task-shaped and thin:

- `understand_component`
- `plan_change`
- `review_change`
- `debug_area`
- `onboard_agent`

Prompts should route to tools and resources above rather than duplicating architectural truth inside prompt text.

## Result contract

Every tool result should preserve enough structure for an agent to reason about trust and freshness.

Required properties:

- `source_path`
- `stable_id`
- `label` such as heading, symbol, or section name
- `class` such as `canonical`, `curated`, `derived`, or `narrative`
- `freshness` such as content hash or indexed timestamp
- `score_rationale` for ranked results
- `warnings` when a result is archived, superseded, lower-authority, or stale

Recommended properties:

- `decision_status` for DEC and ADR records
- `owners` or ownership hints when the repo has them
- `related_paths`
- `evidence_refs` to diffs, tests, lints, or verification surfaces

## Query policy

The server should follow the same retrieval ladder as the repo itself:

1. Prefer curated routing when a direct map or index answers the question.
2. Use hybrid retrieval when the question is broad, fuzzy, or cross-cutting.
3. Prefer canonical sources over narrative or derived matches when both answer the same question.
4. Return citations that let the agent read the source directly.

The server should never hide when it is returning a summary, a cached derivative, or a lower-authority result.

## Task-shaped bundles

`bundle` exists because many agent questions are not just search queries.

Recommended initial bundle shapes:

- `onboarding`: repo map, key read paths, current decisions, and first verification path
- `plan_feature`: relevant maps, decisions, learnings, touched symbols, and recent related changes
- `review_change`: change summary, affected areas, relevant ADRs, tests, lints, and likely regression surfaces
- `debug_area`: ownership, recent related changes, failure surfaces, tests, and relevant decisions
- `understand_component`: local map, symbols, key files, decisions, and adjacent evidence

In the current v1 implementation, `plan_feature` is docs-first only: maps, decisions, learnings, and design context. It does not promise code symbols or rich change evidence yet.

Bundles should remain compositional. They are thin orchestrations across existing tools and resources, not separate sources of truth.

## Relationship to the shared platform plane

The local `project-context` MCP is required. A shared platform MCP is optional.

The local server may delegate selected work to a shared platform surface for:

- reranking
- template bootstrap assistance
- cross-project search
- policy or standards lookup
- observability or remote metadata

But the local server should still produce a coherent answer when the shared plane is unavailable.

## Non-goals

- replacing Git or becoming the repo's canonical data store
- hiding source provenance behind a single opaque "ask anything" endpoint
- forcing every project to use a remote service before local work can begin

## Links

- [agentic-project-infra.md](agentic-project-infra.md)
- [git-derived-memory.md](git-derived-memory.md)
- [shared-platform-mcp.md](shared-platform-mcp.md)
- [../decisions/adr/ADR-0002-project-context-mcp.md](../decisions/adr/ADR-0002-project-context-mcp.md)
