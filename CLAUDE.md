# Claude Code

`AGENTS.md` is auto-loaded — treat it as the repo map. Rules live in `.genai/rules/`. Skills live under `.genai/skills/`. Workflow commands live under `.genai/commands/` as an advanced workflow layer.

## Rules

Read these rules before starting work on any task:

- [.genai/rules/core.md](.genai/rules/core.md) — operating model, skills navigation
- [.genai/rules/cli.md](.genai/rules/cli.md) — execution model, CLI policy, git guard
- [.genai/rules/delivery.md](.genai/rules/delivery.md) — output rules, brevity, open items
- [.genai/rules/tight-work.md](.genai/rules/tight-work.md) — quality tiers, regression checklist
- [.genai/rules/context-efficiency.md](.genai/rules/context-efficiency.md) — progressive disclosure

Load these when relevant (match by task type, not always):

- [.genai/rules/maintenance.md](.genai/rules/maintenance.md) — when finishing changes
- [.genai/rules/decision-records.md](.genai/rules/decision-records.md) — when changing boundaries/architecture
- [.genai/rules/project-layout.md](.genai/rules/project-layout.md) — when working in `project/` or changing the example app layout
- [.genai/rules/persona.md](.genai/rules/persona.md) — when doing review delivery

## Language and stack rules (auto-load)

These load automatically when you touch matching files -- no invocation needed:

- `.genai/rules/python.md` — activates on `*.py`, `dev`, `.githooks/*`
- `.genai/rules/go.md` — activates on `*.go`, `project/go/**`
- `.genai/rules/typescript.md` — activates on `*.ts`, `*.tsx`, `project/web/**`
- `.genai/rules/stack.md` — activates on `project/stack/**`, `Dockerfile`, `compose.yml`

## Skills (on-demand depth)

Invoke when the task requires workflow depth beyond what rules provide. See [skills index](.genai/skills/README.md).

- `.genai/skills/git/` — Graphite stacking, worktree coordination, stack navigation
- `.genai/skills/docs/` — doc hierarchy, walkthrough authoring, ADR workflow
- `.genai/skills/template-maintenance/` — changing template rules, commands, top-level docs

## Agents and commands

Review agent definitions live in `.genai/agents/` (SSOT) with Cursor wrappers in `.cursor/agents/`. Workflow commands live in `.genai/commands/` with Cursor wrappers in `.cursor/commands/`.

## First Moves

1. Read `README.md` if you need the repo map in plain English.
2. Run `./dev doctor` on a new machine.
3. Run `./dev verify` before calling template work complete.
4. Run `./dev setup` when you need the local docs-first `project-context` runtime or want the repo-managed Git hook wrappers installed for this clone.

Hook scripts in this repo enforce a conservative git allowlist. Keep shell commands simple; do not assume every read-only `git` form is permitted.

Use `./dev context status` and `./dev context smoke` when debugging the local self-query runtime or its bootstrap path.

## On-Demand Context

Read these only when the task requires them:

- [STATUS.md](STATUS.md) — what works now
- [docs/ROADMAP.md](docs/ROADMAP.md) — what should happen next
- [docs/decisions/README.md](docs/decisions/README.md) — open `DEC` forks and settled `ADR` choices
- [docs/design/README.md](docs/design/README.md) — deeper architecture and rationale
- [.genai/learnings-index.md](.genai/learnings-index.md) — choose a domain, then open only that section in `.genai/learnings.md`
- [.genai/skills/README.md](.genai/skills/README.md) — skill index for on-demand depth

Read these advanced overlays only when working on review delivery or swarm behavior:

- [.genai/swarm-roster/README.md](.genai/swarm-roster/README.md)
- [.genai/personas/README.md](.genai/personas/README.md)
