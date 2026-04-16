# Layer 1: Core Infrastructure

## What This Layer Teaches

How to evolve a well-organized human project into an agent-ready repo without pretending the human baseline never existed. This is the first agentic layer on top of `main`.

## Why This Layer Exists

`main` already gives you a tidy human project, a worked-example `project/` tree, and a human control plane. This layer exists to add the first agentic upgrade around that baseline:

- Agents need clear rules to follow. Without them, they hallucinate conventions.
- The baseline control plane (`./dev`) becomes more useful once it can verify agent-facing docs, guardrails, and shell policy.
- Hook-based guardrails prevent agents from running destructive commands before you've built trust.
- Architectural governance (ADRs) ensures load-bearing decisions are recorded, not lost in chat history.

## Talking Points

### Rules as infrastructure, not documentation

The `.genai/rules/` directory is the single source of truth for agent behavior. Editor-specific wrappers (`.cursor/rules/*.mdc`) are thin references, not copies. This means you can support multiple editors (Cursor, Claude Code, etc.) without maintaining parallel rule sets.

### The control plane pattern

`./dev` already exists on `main` as the human control plane. This layer refines it for agent use by adding rule-aware verification, shell-guard checks, and AI-friendly helpers without replacing the human baseline.

### Worktrees as execution surfaces

This layer also introduces the worktree operating model. Worktrees let humans and agents edit and run one stack branch in isolation without turning the home checkout into a branch-hopping workspace. The home checkout remains the Graphite control plane for `gt sync`, `gt restack`, and `gt submit`.

### Guard-first safety

The guard (`.claude/hooks/guard.py`) uses a conservative allowlist for shell commands. It permits read-only git commands and controlled mutations (`git add`, `git commit`, `git push`) while blocking destructive operations (`git reset --hard`, force-push, branch deletion). This is a trust model, not a limitation -- downstream projects can adjust the allowlist as they build confidence in their agent workflows.

### Progressive disclosure starts here

This layer deliberately excludes review agents, personas, MCP servers, and RAG. Not because they're unimportant, but because they're not prerequisites. A team can start from the human baseline on `main`, then move to `stack/1-core` when they want the first agent-facing upgrade.

## What This Layer Adds

| Path | Purpose |
| ---- | ------- |
| `.genai/rules/` | Canonical rule prose covering CLI policy, context efficiency, delivery, maintenance, and more |
| `.cursor/rules/` | Thin Cursor wrappers (`.mdc` files) that `@`-reference the SSOT rules |
| `.cursor/worktrees.json` | Minimal setup hook for isolated worktrees |
| `./dev` | Agent-facing refinement of the baseline control plane |
| `.claude/hooks/` | Guard (command allowlist), format-on-edit, git hook logic |
| `.snip/` | AI-friendly shell output filters |
| `docs/decisions/` | ADR/DEC governance framework + ADR-0001 |
| `docs/design/` | Architecture docs including this stack guide |
| `AGENTS.md`, `CLAUDE.md`, `STATUS.md` | Agent-facing maps and branch-level operating guidance |

## What's Deliberately Missing

- **Review agents** (`.cursor/agents/`) -- added in layer 2
- **Workflow commands** (`.cursor/commands/`) -- added in layer 2
- **Persona catalog** (`.genai/personas/`) -- added in layer 2
- **MCP server** (`scripts/project_context/`) -- added in layer 3
- **Persistent storage** (LanceDB) -- added in layer 4
- **Vector search** (embeddings) -- added in layer 5

## Try This Layer

```bash
git checkout stack/1-core
./dev help
./dev verify
./dev doctor
```

If you work across the stack, create a worktree for isolated edits and keep your home checkout for later `gt restack` and `gt submit`.

## Questions This Layer Should Answer

1. How do I structure rules so they work across multiple AI editors?
2. What does a minimal, honest control plane look like?
3. How do I give agents guardrails without making them useless?
4. When should I create an ADR vs just making the change?
5. What's the smallest set of files an agent needs to orient itself in a new repo?
