# Layer 3: MCP Server

## What This Layer Teaches

How to build a docs-first MCP (Model Context Protocol) server that gives agents structured access to project knowledge -- without requiring a database, embeddings, or external services.

## Why This Layer Exists

Agents are only as good as the context they receive. Most AI coding tools rely on file search and semantic indexing provided by the editor. This layer adds a **project-controlled** context surface: an MCP server that the project itself defines, runs, and governs.

The key insight: the project is the authority on its own structure. An MCP server lets the project expose curated, ranked, up-to-date context rather than relying on the editor's general-purpose indexer.

## Talking Points

### Docs-first, not code-first

The MCP server indexes markdown documentation, design docs, decision records, and rules -- not source code. This is deliberate. Agents already have good code search (the editor provides it). What they lack is structured access to the *why* behind the code: architectural decisions, design rationale, conventions, and governance.

### In-memory backend as the starting point

This layer uses a simple in-memory store (`store.py`) instead of a database. The chunks live in a Python list. This is intentionally minimal:

- Minimal dependencies (FastMCP plus standard library)
- No install/setup friction beyond `./dev setup`
- The same interface (`replace_chunks`, `load_rows`, `has_index`, `row_count`) that the persistent layer will use

The trade-off: data doesn't survive process restarts. The next layer (persistence) solves this.

### Lexical search, not vector search

The search implementation (`corpus.rank_rows`) uses keyword overlap scoring, not embeddings. This is the honest starting point: it works, it's fast, it requires no ML models, and it's easy to understand and debug. Vector search is added in layer 5.

### The MCP tool surface

The server exposes six tools through FastMCP:

| Tool | What it does |
|------|-------------|
| `status` | Runtime state, index health, hook status |
| `rebuild` | Rebuild the chunk index from source docs |
| `search` | Lexical search across indexed chunks |
| `fetch` | Retrieve a specific document or chunk by path |
| `decisions` | Query ADR/DEC governance records |
| `bundle` | Package multiple related chunks for context |

### Control plane integration

`./dev context serve` starts the MCP server. `./dev context rebuild` builds the index. `./dev context search` runs queries from the CLI. The control plane is the same one from layer 1 -- the MCP just adds subcommands to it.

## What's In This Layer

| Path | Purpose |
|------|---------|
| `scripts/project_context/server.py` | FastMCP server exposing 6 tools |
| `scripts/project_context/corpus.py` | Markdown chunking, heading extraction, lexical ranking |
| `scripts/project_context/store.py` | In-memory chunk storage (replaced by LanceDB in layer 4) |
| `scripts/project_context/runtime.py` | Path allowlists, state management, corpus iteration |
| `scripts/project_context/cli.py` | CLI for rebuild, search, status, smoke, serve |
| `scripts/project_context/dev_commands.py` | Bridge between `./dev` and the context runtime |
| `docs/design/project-context-mcp.md` | MCP architecture and data flow |
| `docs/design/git-derived-memory.md` | Git-derived memory model |
| `docs/decisions/adr/ADR-0002` | Decision record for the MCP approach |

## What's Deliberately Missing

- **LanceDB persistence** (`lancedb` dep, persistent `store.py`) -- added in layer 4
- **Vector embeddings and semantic search** -- added in layer 5

## Try This Layer

```bash
git checkout stack/3-mcp
./dev setup
./dev context smoke
./dev context search "control plane"
```

## Questions This Layer Should Answer

1. Why build a project-specific MCP server instead of relying on editor-provided search?
2. What's the right granularity for doc chunks (headings? paragraphs? files?)?
3. How does lexical search compare to vector search for project documentation?
4. What's the minimum viable MCP tool surface for agent orientation?
5. How do you integrate an MCP server into an existing control plane without adding complexity?
