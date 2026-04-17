# Session QA Checklist

Shared reference for session-scoped quality commands. Not a slash command — referenced by `/review`, `/polish`, and `/regressions`.

## Pre-flight

Before starting QA, read `.cursor/learnings-index.md` if present, match the domains you changed, then open only those sections in `.cursor/learnings.md` for known gotchas.

## Scope determination

Default to this session's changes. Check files you edited or created during this conversation.

If no session changes, fall back to git diff:

- `git diff --name-only` + `git diff --cached --name-only`
- If empty: `git log --oneline -5` then `git diff --name-only HEAD~N`

Prompt context narrows scope further — if a specific area is named, focus there.

## Risk classification

Classify touched files by **role**, not by fixed paths (paths vary by repo):

| Risk | What to look for | Why |
| --- | --- | --- |
| **Critical** | Core interfaces, auth/authorization, shared contracts, transport boundaries | Changes here break many callers or security |
| **High** | Business logic, API handlers, wire/DTO layers, real-time or event dispatch | Behavior and compatibility risk |
| **Medium** | UI state, persistence adapters, integration glue | Consumer-side or localized breakage |
| **Low** | Styles, copy, standalone docs, local tooling | Visual or doc drift |

## Cross-cutting checks

Run these for any Critical/High files in scope (adapt names to your project):

- **Mock / test doubles**: Interface or contract changes → sync mocks, fakes, and contract tests
- **Multi-channel parity**: If the stack exposes the same capability over more than one path (e.g. HTTP + RPC), verify handlers stay aligned
- **Shared types**: Server/model changes → verify client type definitions and codegen stay in sync
- **Events / topics**: If subjects, channels, or permissions changed → verify publishers, subscribers, and permission/config docs
- **State management**: Store or cache shape changes → verify components or services reading that state
- **Doc freshness**: Update protocol/API docs and status notes when behavior changes

## Per-language file checks

- **Compiled services** — Builds? Tests? Authorization on sensitive paths? Errors wrapped, not leaked?
- **Client/UI code** — Types correct? State patterns consistent? Dispatch/subscription code updated if events changed?
- **Styles** — No unintended outer margins on leaf components? Design tokens used consistently?
- **Docs / rules / skills** — Cross-references correct? Links work?

## Verification gate

Run the project's standard checks (tests, lint, typecheck — however the repo documents them). If there is no script, run **project checks** the way `CONTRIBUTING` or `README` specifies.

For this template, that means `./dev verify`.

The following cursor rule files may be relevant when present:

- Project-specific AI/agent rules under `.cursor/rules/` or `.genai/rules/`

Consider those rules if they affect your changes.
