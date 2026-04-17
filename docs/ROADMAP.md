# Roadmap

This file models a lightweight roadmap for a project that adopts the template.

## Milestone 1 — Truthful Baseline

- Ship one obvious control plane (`./dev`) for verify, fmt, doctor, status, and snip.
- Make the top-level doc graph truthful.
- Keep the first-read path small enough for a live demo or first-day onboarding.

## Milestone 2 — Local Self-Query Runtime

- Ship and maintain a docs-first local `project-context` MCP via `./dev setup`.
- Keep `./dev verify` bootstrap-independent while using `./dev context smoke` for runtime readiness.
- Store derived memory outside git and keep canonical docs authoritative.

## Milestone 3 — Advanced Review Delivery

- Keep swarm orchestration, reviewer specialization, persona routing, and challenge flows available.
- Ensure those surfaces are explicitly optional for teams that want a simpler operating model.

## Milestone 4 — Agent Evals and Demo

- Ship a repeatable agent-eval harness via `./dev eval` with local scenario truth.
- Provide cold-start, worktree-awareness, and control-plane verification scenarios as seed corpus.
- Turn passing eval scenarios into curated demo material with presenter-friendly reports.
- Keep the harness provider-agnostic; add a Claude runner adapter as a follow-on.

## Milestone 5 — Downstream Specialization

- Add language rules, domain skills, and project-specific invariants.
- Replace template placeholders with real verification, status, roadmap, and protocol docs.
- Extend the control plane only when a project can name a stable capability it genuinely needs.
