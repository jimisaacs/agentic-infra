# Walkthrough: Vector RAG

You're on `stack/5-rag`. The MCP server has a persistent LanceDB backend from layer 4. This layer adds the final piece: vector embeddings and semantic search.

## What changed

Open `scripts/project_context/embeddings.py`. This generates vector embeddings for each documentation chunk using `sentence-transformers` (default model: `all-MiniLM-L6-v2`). Embeddings are cached by content hash -- unchanged chunks skip re-embedding on rebuild.

Open `scripts/project_context/store.py` again. Compare it to layer 4. It gained `vector_search` and `replace_chunks_with_vectors`. LanceDB supports native vector similarity search -- no separate index server needed. The upgrade from "chunk table" to "vector database" is one function call.

## Why this is layer 5 and not layer 1

This is the teaching point of the whole stack. You don't need embeddings to build a useful retrieval system. Layers 3 and 4 delivered a working MCP server with lexical search. Semantic search is an enhancement, not a foundation.

Starting with embeddings is a common mistake. It adds ML dependencies, model downloads, and computational cost before you've proven the basic retrieval pipeline works. This stack demonstrates the correct ordering: make it work, make it persistent, then make it smart.

## Hybrid search

The search tool now supports three modes:

- **lexical** -- keyword overlap, same as layer 3
- **semantic** -- vector similarity via LanceDB
- **hybrid** (default) -- runs both, normalizes scores, blends with configurable weight

## Try it

```bash
./dev setup
./dev context rebuild   # generates embeddings (first run downloads ~80MB model)
./dev context search "how do agents get oriented in a new repo"
```

Compare the results to a purely lexical query. Semantic search finds docs that are *about* the topic even when they use different words.

## The full picture

You've now walked through layers 1-5 of the stack:

| Layer | What it adds | Walkthrough |
|-------|-------------|-------------|
| `main` | Human baseline: app, control plane, principles | `walkthrough/main.md` |
| `stack/1-core` | Agentic rules, guardrails, governance | `walkthrough/1-core.md` |
| `stack/2-agents-personas` | Review agents, personas, workflow commands | `walkthrough/2-agents-personas.md` |
| `stack/3-mcp` | Docs-first MCP server, in-memory backend | `walkthrough/3-mcp.md` |
| `stack/4-persistence` | LanceDB persistence | `walkthrough/4-persistence.md` |
| `stack/5-rag` | Vector embeddings, semantic search | `walkthrough/5-rag.md` |

Each layer builds on the previous one. No layer removes content from its parent. The stack is both a teaching tool and a working system.

## What to take away

- Start with the simplest thing that works. Add complexity only when the simpler version proves its value.
- The control plane (`./dev`) grew with every layer but never lost backward compatibility.
- Architecture decisions are recorded, not implied. Each major choice has an ADR.
- Rules, agents, and personas are infrastructure, not code. They're versioned, audited, and testable.
- The project governs its own context surface. It doesn't rely on the editor to understand its architecture.
