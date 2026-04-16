# Contributing

This branch adds the first agentic layer on top of the human baseline from `main`. Keep the human project surfaces truthful and the agentic additions clearly additive.

## Local Loop

Prerequisites: `python3`, `git`, and `docker`. Optional: `snip`. Project tools such as `go`, `node`, and `npm` are only needed for host-native development (`./dev stack dev`).

1. Run `./dev doctor` once on a new machine.
2. Make the smallest correct change.
3. Run `./dev fmt` after edits.
4. Run `./dev verify` before calling the work done.

## What To Keep True

- `README.md`, `AGENTS.md`, and `CLAUDE.md` stay map-level and easy to read cold.
- `.genai/rules/` is the SSOT for rule prose; `.cursor/rules/*.mdc` stay thin wrappers.
- The `./dev` control plane is the default way to verify, format, and inspect the template.
- `./dev verify` requires `python3`, `git`, and `docker`. Most checks run on the host; the web build uses Docker.
- `project/README.md` remains the map for the worked-example app surface.
- `docs/PRINCIPLES.md` and `docs/CONVENTIONS.md` are the engineering foundation -- update them when philosophy changes.

## When You Change The Template

- Rules or command behavior changed: update `README.md`, `AGENTS.md`, and any affected `.genai/rules/*.md`.
- The control plane changed: update `dev`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and any doc-contract expectations encoded in `./dev verify`.
- The worked-example app layout changed: update `project/README.md`, `.genai/rules/project-layout.md`, and any top-level map entries that point into `project/`.
- Architecture or load-bearing workflow changed: update `docs/decisions/` and `docs/design/` as appropriate.
- Principles or conventions changed: update `docs/PRINCIPLES.md` or `docs/CONVENTIONS.md` and ensure consistency with the control plane.
- Teaching story changed: update `STATUS.md` and `docs/ROADMAP.md` so the example remains coherent.
