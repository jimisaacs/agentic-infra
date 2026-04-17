# Walkthrough: The MCP Server

You're on `stack/3-mcp`. The rules, agents, and workflow commands from layers 1-2 are all in place. This layer adds something new: the project's own context surface.

## The problem this solves

Agents already have code search -- the editor provides it. What they lack is structured access to the *why*: architectural decisions, design rationale, conventions, governance docs. This layer builds a project-controlled MCP server that exposes curated, ranked documentation to agents.

## What to look at

Open `scripts/project_context/server.py`. This is a FastMCP server with six tools: `status`, `rebuild`, `search`, `fetch`, `decisions`, and `bundle`. The runtime spans seven modules under `scripts/project_context/`.

Open `scripts/project_context/corpus.py`. This is where markdown files get chunked by heading, scored, and ranked. The ranking is lexical (keyword overlap) -- no embeddings yet. That comes in layer 5.

Open `scripts/project_context/store.py`. This is an in-memory list. Chunks go in, queries come out. It will be replaced by LanceDB in layer 4. The interface stays the same.

## Try it

```bash
./dev setup           # bootstrap the runtime (creates .venv, installs deps)
./dev context smoke   # verify the MCP server works
./dev context search "control plane"
```

## The control plane grew again

`./dev` gained `setup` (bootstraps the MCP runtime) and `context` (serve, rebuild, search, status, smoke). The pattern is the same as layers 0-1: each layer adds capabilities to the same control plane.

## The key insight

The MCP server indexes docs, not code. Design docs, decision records, rules, conventions -- the governance and architectural context that agents need to make good decisions. Code search is already solved by the editor. This fills the gap the editor can't.

## What to understand before moving on

- The MCP server is project-controlled. The project decides what context agents see.
- The in-memory backend is intentionally minimal. Persistence comes next.
- Lexical search works well enough to prove the pattern. Semantic search comes in layer 5.
- `./dev setup` is the bootstrap. `./dev context serve` starts the server.

## What comes next

Checkout `stack/4-persistence`. That branch replaces the in-memory store with LanceDB -- same interface, persistent data, no external server required.

```bash
git checkout stack/4-persistence
```
