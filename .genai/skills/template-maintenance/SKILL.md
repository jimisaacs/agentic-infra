# Template Maintenance

Use this skill when you are changing the agentic-infra template itself: rules, commands, top-level docs, hooks, personas, or the `./dev` control plane.

## Goals

- Keep the cold-start path truthful and small.
- Preserve `.genai/rules/` as SSOT.
- Treat advanced layers as optional from the first-read path.

## Default Loop

1. Start with `README.md`, `AGENTS.md`, and `CLAUDE.md`.
2. If the change touches command or toolchain behavior, read `.genai/rules/cli.md` and use `./dev`.
3. If the change touches review delivery, read `.genai/personas/README.md` and `.genai/swarm-roster/README.md` only after the top-level docs are updated.
4. Run `./dev fmt` after edits.
5. Run `./dev verify` before finishing.
6. If the change touches the local `project-context` runtime (layer 3+), `.cursor/mcp.json`, or Git hook wrappers, also run `./dev setup` and `./dev context smoke`.

## Invariants

- `README.md`, `AGENTS.md`, and `CLAUDE.md` stay map-level.
- `./dev` is the one obvious control-plane entrypoint.
- Persona and swarm systems may stay rich, but they must be clearly optional for downstream teams.
- If a doc mentions a path by default, that path should exist in the repo or be explicitly marked optional.
