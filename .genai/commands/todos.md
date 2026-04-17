# TODO scan

Scan the codebase for code TODOs and report them categorized. See your project's todos rule (e.g. `todos.mdc` under `.cursor/rules/`) for the taxonomy if one exists.

## How to run it

1. Search for `TODO|FIXME|ACCEPTED_RISK` across `*.go`, `*.ts`, `*.tsx`, `*.swift`, and other source extensions your project uses.
2. Categorize each hit by marker type: `TODO(milestone)`, `TODO(wire)`, `TODO(cleanup)`, `TODO` (general), `FIXME`, `ACCEPTED_RISK` — or match the project's convention.
3. If the user specified a scope (e.g., "todos for milestone M4", "todos in the web app"), filter accordingly.

## Report format

### Summary

| Category | Count |
|----------|-------|
| `TODO(M4)` | 4 |
| `TODO(wire)` | 7 |
| `TODO(cleanup)` | 2 |
| `TODO` (general) | 5 |
| `FIXME` | 0 |
| `ACCEPTED_RISK` | 6 |
| **Total** | **24** |

### Detail

**Default:** summary table + stale TODOs only. Full per-item listing only when the user asks for it (e.g., "show me all wire todos") or specifies a narrow filter.

### Stale TODO check

Flag TODOs referencing milestones marked complete in `docs/ROADMAP.md` (or equivalent) or features that already exist. Report as **stale**.

## Filtering

The user's prompt narrows scope:

- **By milestone**: "todos for M4" → only `TODO(M4):` entries (or matching tag)
- **By component**: "todos in the web app" → only files under that directory
- **By risk**: "accepted risks" → only `ACCEPTED_RISK` entries
- **Stale only**: "stale todos" → only TODOs referencing completed milestones or landed features

## When to use

- Before starting a milestone — see what's already scaffolded
- During polish passes — find stale TODOs to clean up
- Code review — audit risk acceptance decisions
