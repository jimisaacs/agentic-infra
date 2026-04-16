# Cursor project rules

This folder follows **[Cursor → Rules](https://cursor.com/docs/context/rules)** (project rules: version-controlled, scoped).

## How rules load

| Kind | Frontmatter | When it applies |
| ------ | ---------------- | ----------------- |
| Always | `alwaysApply: true` | Every Agent chat |
| By file | `globs: [...]` | Files matching patterns are in context |
| Intelligent | `description: "..."` + `alwaysApply: false` | Agent decides from the description |
| Manual | (no globs; optional description) | When `@`-mentioned in chat |

Use **`.md` or `.mdc`**. **`.mdc`** supports YAML frontmatter (`description`, `globs`, `alwaysApply`).

**Best practices** (from Cursor docs): keep each rule under ~500 lines; split by domain; **reference files with `@path`** instead of copying code; keep always-on rules at **map/index** depth, not full checklists; prefer small index files over resolving large docs into every chat.

| File | Role |
| ------ | ------ |
| `core.mdc` | Always — operating model, posture, skills/rules navigation |
| `cli.mdc` | Always — execution model + CLI policy |
| `tight-work.mdc` | Always — what "done" means: tiered polish + regression checklist |
| `delivery.mdc` | Always — output rules: finish things, be brief, open items block |
| `learnings.mdc` | Always — read learnings index, then the relevant section |
| `context-efficiency.mdc` | Always — progressive disclosure: minimize always-on token cost |
| `active-areas.mdc` | Intelligent — check for parallel agent conflicts (loads when modifying 3+ files) |
| `misdirected.mdc` | Intelligent — wrong-chat / vague asks: restate scope (loads when instructions seem out of scope) |
| `maintenance.mdc` | Intelligent — file size discipline, SSOT, update protocol (loads when finishing changes) |
| `decision-records.mdc` | Intelligent — ADR workflow for load-bearing architecture changes |
| `worktrees.mdc` | Intelligent — worktree execution model, home-checkout Graphite flow, port offsets |
| `python.mdc` | By file (`*.py`, `dev`, `.githooks/*`) — Python conventions for control plane and runtime |
| `go.mdc` | By file (`*.go`, `project/go/**`) — Go conventions for the Pulse app |
| `typescript.mdc` | By file (`*.ts`, `*.tsx`, `project/web/**`) — TypeScript/React conventions |
| `stack.mdc` | By file (`project/stack/**`, `Dockerfile`, `compose.yml`, `nginx.conf`) — Docker Compose architecture |
| `project-layout.mdc` | By file (`project/**`) — workspace layout, scaffolding, navigation, retirement |
| `ai-infra.mdc` | By file (`.cursor/`, `.claude/`, `.genai/`, `AGENTS.md`, `CLAUDE.md`) — self-maintenance |
| `todos.mdc` | By file (source files) — TODO taxonomy, format, lifecycle |
| `persona.mdc` | Manual — canonical review persona catalog and routing guidance |

**Repo-wide agent guide**: [`AGENTS.md`](../../AGENTS.md) (plain markdown; complements these rules).

**Plans**: [`.cursor/plans/README.md`](../plans/README.md).
