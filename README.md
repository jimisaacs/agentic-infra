# Agentic Infrastructure

A teaching-first starter kit that begins as a well-oiled human project and then evolves, branch by branch, into agentic infrastructure.

## Human Baseline

`main` is the human-first baseline:

- `project/` is the worked-example multi-ecosystem app surface.
- `./dev` is the human control plane for formatting, verification, lifecycle, and status.
- `docs/` holds the engineering [principles](docs/PRINCIPLES.md) and [conventions](docs/CONVENTIONS.md).
- `.githooks/` provides a lightweight local hook wrapper for baseline verification.

## Quick Start

```bash
./dev help
./dev doctor
./dev setup         # install the clone-local pre-commit hook
./dev verify
./dev fmt
./dev status
./dev stack up         # build and start (dev mode: file watcher)
./dev stack up --prod  # build and start (prod mode: one-shot build)
./dev stack reset      # remove all containers, images, and volumes
```

After `./dev stack up`, Pulse is at **http://localhost:3000**.

## Project Pattern

Use this repo as a pattern for a tidy human project before you add editor- or agent-specific infrastructure:

- Start with [project/README.md](project/README.md) for the ecosystem/target layout.
- Read [docs/PRINCIPLES.md](docs/PRINCIPLES.md) for the engineering philosophy.
- Read [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for coding standards.
- Read [docs/guides/development.md](docs/guides/development.md) for the development workflow.
- Use `./dev` to verify and inspect the baseline.
- Run `./dev setup` if you want the tracked `.githooks/pre-commit` wrapper installed for this clone.
- Use `git worktree` when you want isolated editing or execution without turning one checkout into a branch-hopping workspace.

## Stack

Later branches add the agentic layers:

| Branch | What it adds |
| ------ | ------------ |
| `stack/1-core` | Agentic rules, guardrails, and the first agent-facing `./dev` refinements |
| `stack/2-agents-personas` | Review agents, workflow commands, swarm roster, persona catalog |
| `stack/3-mcp` | Docs-first MCP server with in-memory backend |
| `stack/4-persistence` | LanceDB persistence replacing in-memory backend |
| `stack/5-rag` | Vector embeddings and semantic search |
| `stack/6-evals` | Agent eval harness and demo scenarios |
