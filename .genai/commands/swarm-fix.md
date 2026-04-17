# Swarm fix

> **Pipeline context:** `/swarm-review` + fix phase combined. Usually dispatched from `/swarm fix`. Standalone use: when you want the core review kernel plus fixes without the full `/tighten` convergence loop.

Like `/swarm-review` but instead of just reporting, **fix everything you can**. This atomic command intentionally launches the full four-reviewer kernel; use `/swarm fix ...` when you want specialist add-ons selected from the roster trigger rules.

## Scope

**Default to this session's changes.** Identify files you edited or created during this conversation. When the prompt provides context (e.g., "swarm fix the dashboard work"), narrow to those files.

Fall back to full diff only if no changes were made this session.

## How to run it

1. Get session-changed files via `git diff --stat` and `git diff --cached --stat`.

2. **Launch the same core four agents as `/swarm-review`** (security, architecture, migration, evidence) — all in a single message. Same prompt structure: changed files, nature of change, "report findings only." If personas are in use, assign them from `.genai/personas/roles.md` and source the selected capsule from `.genai/personas/records/<id>.md`.

3. **Consolidate** into a severity-ranked table.

4. **Fix everything Medium and above.** For each finding:
   - Critical/High: fix immediately
   - Medium: fix if straightforward, flag if it needs a design decision
   - Low: fix if trivial, otherwise note it

5. **Verify:** run **project checks** per the repository docs.

6. **Report what you fixed** using the `/handoff` format.

## How it relates to other swarm commands

- `/swarm-review` = same core four agents, **report only** (no fixes)
- `/swarm-fix` = report + **fix** + verify — use when the user says "swarm it and fix it"
- `/regressions` = narrower dependency/mock/parity checklist — run after `/swarm-fix` if you want extra assurance
- `/swarm fix ...` via the orchestrator = core kernel plus any triggered specialists such as `performance-reviewer`, `reliability-reviewer`, or `onboarding-reviewer`
