# Stack Architecture

This repo uses a Graphite-managed stacked branch model. Each branch builds additively on the previous one, teaching one layer of agentic infrastructure at a time.

## Layers

| Branch | Layer | What it adds | Doc |
| ------ | ----- | ------------ | --- |
| `main` | Human baseline | `project/`, human `./dev`, `.githooks/`, and human-facing docs | -- |
| `stack/1-core` | Agentic core | Rules, guardrails, worktree guidance, and the first agent-facing `./dev` refinements | [1-core.md](1-core.md) |
| `stack/2-agents-personas` | Agents + personas | Review agents, workflow commands, swarm roster, persona catalog | [2-agents-personas.md](2-agents-personas.md) |
| `stack/3-mcp` | MCP server | Docs-first MCP runtime with in-memory backend | [3-mcp.md](3-mcp.md) |
| `stack/4-persistence` | LanceDB persistence | Replaces in-memory backend with embedded database | [4-persistence.md](4-persistence.md) |
| `stack/5-rag` | Vector RAG | Embedding generation, hybrid lexical+semantic search | [5-rag.md](5-rag.md) |

## Design Principles

- **Additive layering**: each branch = everything below + one concern. No branch removes content from its parent.
- **Progressive disclosure**: a newcomer can start at `stack/1-core` and get value without loading the full stack.
- **Standalone layers**: each branch should be a coherent, working repo at its layer of capability.
- **Teaching-first**: the stack exists to demonstrate how agentic infrastructure composes, not just to organize code.

## Workflow

Start on `main` to see the human baseline. Move to `stack/1-core` when you want the first agentic upgrade layer. Use worktrees when you want isolated execution without turning one checkout into a branch-hopping workspace.

```text
# home checkout
gt checkout stack/5-rag
git worktree add ../worktrees/core stack/1-core

# in the worktree
./dev verify
gt modify -c -m "description"
git push

# back in the home checkout
gt restack --branch stack/1-core --upstack
gt submit
```

Notes:

- Worktrees are valid for isolated editing, testing, committing, and pushing.
- Keep one home checkout for `gt sync`, `gt restack`, `gt submit`, and broad stack navigation.
- If a branch is already checked out in another worktree, `gt checkout <branch>` from the home checkout will fail.
