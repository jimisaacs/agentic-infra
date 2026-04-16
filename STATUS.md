# Status

This file models a lightweight status doc for a teaching-first project.

## Current State

- Core path exists: `README.md`, `AGENTS.md`, `CLAUDE.md`, and `./dev` should be enough to understand and operate the template.
- Verification is real: `./dev verify` checks required paths, Python syntax, guard behavior, unit tests, JSON config parsing, markdown links, doc-contract promises, and formatting drift.
- Rules are SSOT: `.genai/rules/` is the canonical source of truth for rule prose; `.cursor/rules/*.mdc` are thin wrappers.
- The worked-example app under `project/` is explicitly mapped, with layout guidance in `project/README.md` and `project-layout` rule coverage for agents.

## What Works Now

- A downstream project can copy this template and start from one control-plane entrypoint.
- The top-level docs point at real files instead of placeholder paths.
- The guard enforces a conservative shell allowlist for agent safety.

## What To Customize Downstream

- Replace the project description, stack, layout, invariants, and commands in `AGENTS.md`.
- Replace the placeholder roadmap and status language with product-specific truth once the template lands in a real repo.
