# Contributing

This branch adds the first agentic layer on top of the human baseline from `main`. Keep the human project surfaces truthful and the agentic additions clearly additive.

## Local Loop

Prerequisites: `python3`, `git`, and `docker`. For `./dev setup`, you also need a discoverable Python 3.10+ runtime on `PATH` (or via `PROJECT_CONTEXT_PYTHON`). Optional: `snip`. Project tools such as `go`, `node`, and `npm` are only needed for host-native development (`./dev stack dev`).

1. Run `./dev doctor` once on a new machine.
2. Run `./dev setup` if you need the local docs-first `project-context` runtime or want the clone-local Git hook wrappers installed.
3. Make the smallest correct change.
4. Run `./dev fmt` after edits.
5. Run `./dev verify` before calling the work done.
6. If you changed the local MCP/runtime surface, also run `./dev context smoke`.

## What To Keep True

- `README.md`, `AGENTS.md`, and `CLAUDE.md` stay map-level and easy to read cold.
- `.genai/rules/` is the SSOT for rule prose; `.cursor/rules/*.mdc` stay thin wrappers.
- The `./dev` control plane is the default way to verify, format, and inspect the template.
- `./dev verify` requires `python3`, `git`, and `docker`. Most checks run on the host; the web build uses Docker.
- `project/README.md` remains the map for the worked-example app surface.
- `docs/PRINCIPLES.md` and `docs/CONVENTIONS.md` are the engineering foundation -- update them when philosophy changes.

## When You Change The Template

- Rules or agent-facing behavior changed: update `README.md`, `AGENTS.md`, `CLAUDE.md`, and the affected `.genai/rules/*.md`.
- The control plane changed: update `dev`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and the affected tests.
- The worked-example app layout changed: update `project/README.md`, `.genai/rules/project-layout.md`, and any top-level docs that point into `project/`.
- Review delivery or persona routing changed: update `.genai/personas/` and `.genai/swarm-roster/` rather than copying logic into reviewers.
- Architecture or load-bearing workflow changed: update `docs/decisions/` and `docs/design/` as appropriate.
- Principles or conventions changed: update `docs/PRINCIPLES.md` or `docs/CONVENTIONS.md` and ensure consistency with the control plane.
- Teaching story changed: update `STATUS.md` and `docs/ROADMAP.md` so the example remains coherent.
