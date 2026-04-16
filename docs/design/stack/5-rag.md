# Layer 5: Vector RAG

## What This Layer Teaches

How to add vector embeddings and semantic search to an existing docs-first MCP server, creating a hybrid retrieval system that combines keyword matching with meaning-based similarity.

## Why This Layer Exists

Lexical search (layer 3) finds documents that contain the exact words you searched for. Semantic search finds documents that are *about* what you searched for, even when different words are used. Combining both gives the best retrieval quality:

- "How do agents get context?" matches docs about MCP, progressive disclosure, and the project-context server -- even if they don't contain the word "context" in every chunk.
- Lexical search still wins for exact identifiers, file paths, and specific terms.
- Hybrid scoring blends both signals, weighting each by confidence.

## Talking Points

### Embeddings as a late addition, not a prerequisite

This layer demonstrates that you don't need embeddings to build a useful retrieval system. Layers 3 and 4 delivered a working MCP server with lexical search. Vector search is an *enhancement*, not a foundation. This ordering matters for teaching: it prevents the common mistake of over-engineering the first version.

### The embedding model choice

The default model is `all-MiniLM-L6-v2` from sentence-transformers:

- 384 dimensions (small, fast)
- Good quality for English documentation
- Runs locally, no API keys needed
- ~80MB download on first use

A deterministic hash-based fallback exists for environments where sentence-transformers isn't installed. It produces stable but semantically meaningless vectors -- useful for testing the pipeline without the ML dependency.

### Embedding cache

Embeddings are cached by content hash in `embedding_cache.json`. Unchanged chunks skip re-embedding on rebuild. This makes incremental updates fast even with a local model.

### LanceDB native vector search

Layer 4 chose LanceDB partly for this moment. LanceDB supports vector similarity search natively -- no additional index server needed. The `vector_search` function in `store.py` calls `table.search(query_vector)` directly. The upgrade from "chunk table store" to "vector database" is one function call.

### Hybrid retrieval strategy

The search tool supports three modes:

| Mode | How it works |
|------|-------------|
| `lexical` | Keyword overlap scoring (same as layer 3) |
| `semantic` | Vector similarity via LanceDB |
| `hybrid` | Runs both, normalizes scores, blends with configurable weight |

Hybrid is the default. The blend weight can be tuned per project -- documentation-heavy repos may favor semantic, code-heavy repos may favor lexical.

## What's In This Layer

| Path | Purpose |
|------|---------|
| `scripts/project_context/embeddings.py` | Embedding generation, caching, batch processing, deterministic fallback |
| `scripts/project_context/store.py` | Extended with `vector_search` and `replace_chunks_with_vectors` |
| `docs/design/stack/5-rag.md` | This document |

## Try This Layer

```bash
git checkout stack/5-rag
./dev setup
./dev context rebuild
./dev context search "how do agents get context"
```

## Questions This Layer Should Answer

1. When does semantic search add value over lexical search for project docs?
2. What's the right embedding model for a local-first development tool?
3. How do you cache embeddings efficiently for incremental rebuilds?
4. What's a good hybrid scoring strategy for blending lexical and semantic results?
5. How does the choice of LanceDB in layer 4 pay off when adding vector search?
