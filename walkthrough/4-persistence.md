# Walkthrough: LanceDB Persistence

You're on `stack/4-persistence`. The MCP server from layer 3 is working but loses its index every time the process restarts. This layer fixes that.

## What changed

Open `scripts/project_context/store.py` and compare it mentally to layer 3. The interface is the same four functions: `replace_chunks`, `has_index`, `load_rows`, `row_count`. The implementation is different -- it writes to a LanceDB table instead of a Python list.

This is the dependency inversion principle in practice: the server, CLI, and tests don't know or care that the backend changed.

## Why LanceDB

Open `docs/decisions/adr/ADR-0003-lancedb-for-project-context-v1.md`. This is the decision record. It explains why LanceDB over SQLite, Postgres+pgvector, or a remote vector store. The short version: embedded (no server), local-first, and vector-ready (layer 5 upgrade path).

## What persistence enables

Run `./dev setup` once. It builds the index and writes it to disk. After that, `./dev context serve` starts instantly -- no re-indexing. `./dev context rebuild` refreshes when docs change. This makes the MCP server practical for daily use.

## Try it

```bash
./dev setup
./dev context status    # shows index state, chunk count, indexed timestamp
./dev context search "architectural decisions"
```

## What to understand before moving on

- The store interface didn't change. Only the implementation did. Consumers are untouched.
- LanceDB is an embedded library, not a service. No Docker, no ports, no management.
- The ADR explains the choice. This is what good architecture governance looks like in practice.
- `./dev setup` is now meaningful -- it bootstraps persistent state.

## What comes next

Checkout `stack/5-rag`. That branch adds vector embeddings and semantic search -- LanceDB's native vector support makes this a natural extension.

```bash
git checkout stack/5-rag
```
