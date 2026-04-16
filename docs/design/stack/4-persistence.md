# Layer 4: LanceDB Persistence

## What This Layer Teaches

How to replace an in-memory backend with an embedded database for persistent, fast chunk storage -- without adding operational complexity.

## Why This Layer Exists

The in-memory store from layer 3 works but loses data on every process restart. For a development tool that agents use repeatedly, this means re-indexing every time the MCP server starts. LanceDB solves this:

- **Embedded**: no external server to run or manage. It's a library, not a service.
- **Columnar**: Apache Arrow under the hood, so scanning and filtering is fast.
- **Vector-ready**: the same table can later hold embedding vectors alongside text, making the upgrade to semantic search (layer 5) incremental.

The separation from layer 3 is deliberate: it demonstrates that the MCP server's architecture doesn't depend on its storage backend. The in-memory version and the LanceDB version share the same interface.

## Talking Points

### The storage abstraction pattern

Layer 3's `store.py` exposed four functions: `replace_chunks`, `has_index`, `load_rows`, `row_count`. This layer replaces the implementation but keeps the interface identical. Any consumer of `store.py` (the server, the CLI, tests) works unchanged. This is a practical example of the dependency inversion principle in a teaching context.

### Why LanceDB over SQLite, DuckDB, or a JSON file

- **SQLite**: good for relational data, awkward for columnar chunk storage, no native vector support.
- **DuckDB**: excellent for analytics, heavier than needed for a chunk index.
- **JSON file**: simple but slow for large indexes, no query optimization.
- **LanceDB**: columnar (fast scans), embedded (no server), native vector search support (layer 5 upgrade path), Arrow-native (efficient serialization).

ADR-0003 records this decision.

### What persistence enables

With persistence, `./dev setup` builds the index once. Subsequent `./dev context serve` calls start instantly with the existing index. `./dev context rebuild` refreshes when docs change. This makes the MCP server practical for daily use, not just demos.

## What's In This Layer

| Path | Purpose |
|------|---------|
| `scripts/project_context/store.py` | LanceDB implementation replacing the in-memory backend |
| `pyproject.toml` | Python package metadata with `lancedb` + `fastmcp` deps |
| `requirements-project-context.lock` | Pinned dependency lock for reproducible installs |
| `docs/decisions/adr/ADR-0003` | Decision record: why LanceDB for v1 |
| `examples/language-rules/` | Language-specific rule examples (CSS, Go, TypeScript) for downstream adoption |

## What's Deliberately Missing

- **Vector embeddings and semantic search** -- added in layer 5

## Try This Layer

```bash
git checkout stack/4-persistence
./dev setup
./dev context rebuild
./dev context search "control plane"
```

## Questions This Layer Should Answer

1. When does an in-memory store stop being enough and persistence become necessary?
2. What makes LanceDB a good fit for this use case vs other embedded databases?
3. How do you design a storage interface so the backend can be swapped without changing consumers?
4. What does a good ADR look like for a storage technology choice?
5. How does `./dev setup` change when persistent state enters the picture?
