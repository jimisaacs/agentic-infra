# Context Efficiency — Progressive Disclosure

Every token in always-on context competes with the user's actual task.

## Retrieval Ladder

**Map → Index → Slice → Depth → Isolation.** Start at the cheapest layer that answers the current question. Escalate only when the cheaper layer isn't decisive. Use isolation (subagents) for broad exploration.

## Core Rules

1. Always-on stays at map level — pointers, not content.
2. Index first — skills index, local `README.md` maps, CLI help, learnings index.
3. Read slices before wholes. Search before read.
4. No duplication across always-on files. One SSOT, many pointers.
5. Large docs need an index or TOC.
6. Prefer executable summaries (interfaces, types, schemas, route tables) over prose.
