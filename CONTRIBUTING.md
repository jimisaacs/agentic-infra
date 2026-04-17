# Contributing

This branch is the human-first baseline for the repo. Keep it small, truthful, and easy to operate without any editor-specific or agent-specific infrastructure.

## Local Loop

Prerequisites: `python3`, `git`, and `docker`. Project tools such as `go`, `node`, and `npm` are optional and only needed for host-native development (`./dev stack dev`).

1. Run `./dev doctor` once on a new machine.
2. Run `./dev setup` if you want the clone-local pre-commit hook installed.
3. Make the smallest correct change.
4. Run `./dev fmt` after edits.
5. Run `./dev verify` before calling the work done.

## What To Keep True

- `README.md` and `project/README.md` stay map-level and easy to read cold.
- `./dev` is the default way to verify, format, and inspect the baseline.
- `./dev verify` requires `python3`, `git`, and `docker`. Most checks run on the host; the web build uses Docker.
- `.githooks/pre-commit` stays helpful for humans rather than encoding editor-specific behavior.
- `./dev setup` remains the tracked way to install that hook for the current clone.
- `docs/PRINCIPLES.md` and `docs/CONVENTIONS.md` are the engineering foundation -- update them when philosophy changes.

## When You Change The Baseline

- The control plane changed: update `dev`, `README.md`, `CONTRIBUTING.md`, `.githooks/pre-commit`, and the affected tests.
- The worked-example app layout changed: update `project/README.md` and any top-level docs that point into `project/`.
- The branch story changed: update `README.md` so `main` still reads as the human baseline and later layers still read as additive upgrades.
- Principles or conventions changed: update `docs/PRINCIPLES.md` or `docs/CONVENTIONS.md` and ensure consistency with the control plane.
