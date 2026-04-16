# Decision Backlog

Open architectural decisions live here while they are active...

## Statuses

- open, researching, ready, resolved, dropped

| ID | Status | Decision | Trigger / deadline | Options / tension | Links / resolution |
|---|---|---|---|---|---|
| DEC-0001 | resolved | Select the initial local derived-memory backend for `project-context` | Resolved when the repo shipped the first runnable local MCP-backed memory implementation | LanceDB chosen for this repo's docs-first v1; broader downstream backend policy remains revisitable | [git-derived memory](../design/git-derived-memory.md), [ADR-0001](adr/ADR-0001-git-derived-agent-memory.md), [ADR-0002](adr/ADR-0002-project-context-mcp.md), [ADR-0003](adr/ADR-0003-lancedb-for-project-context-v1.md) |
| DEC-0002 | researching | Define the trust boundary between local `project-context` and shared platform MCPs | Before introducing any shared retrieval, reranking, or policy-backed remote plane | Local-first with optional delegation versus tighter shared control plane; balance offline operation, privacy, auth, and authority ranking | [shared platform MCP](../design/shared-platform-mcp.md), [project-context MCP](../design/project-context-mcp.md) |
