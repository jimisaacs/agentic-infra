# Swarm review

> **Pipeline context:** Phase 3 of `/tighten`. Usually dispatched from `/swarm` (which selects the core roster plus specialists by trigger). Standalone use: when you want the full four-reviewer kernel report without fixes.

Launch the **core four review agents in parallel** against changes. Each agent has a different lens. Consolidate their findings into one severity-ranked report.

## Scope

**Default to this session's changes.** Identify files you edited or created during this conversation and feed those to the reviewers. When the prompt provides context (e.g., "swarm review the auth refactor"), narrow the file list to match.

Fall back to full `git diff` only if no changes were made this session.

## How to run it

1. Identify session-changed files. Cross-reference with `git diff` and `git status`. If diff is empty (changes already committed), use `git diff HEAD~N` to cover the session's work.

2. Launch **4 parallel subagents** using the Task tool — all in a single message so they run concurrently:

```text
Task(subagent_type="security-reviewer", prompt="Review these changes: [paste diff summary + file list]")
Task(subagent_type="architecture-reviewer", prompt="Review these changes: [paste diff summary + file list]")
Task(subagent_type="migration-checker", prompt="Review these changes: [paste diff summary + file list]")
Task(subagent_type="evidence-reviewer", prompt="Review these changes: [paste diff summary + file list]")
```

3. Each subagent prompt must include:
   - The list of changed files with one-line descriptions
   - The nature of the change (new feature, refactor, bugfix, etc.)
   - "Report findings only — do not make changes"
   - If personas are in use, assign them from `.genai/personas/roles.md` and include the selected capsule sourced from `.genai/personas/records/<id>.md`

4. **Consolidate** all four reports into a single table:

| Finding | Agent | Severity | File | Recommendation |
| ------- | ----- | -------- | ---- | -------------- |

5. Group by severity (Critical → High → Medium → Low → Informational). Deduplicate overlapping findings.

When the diff clearly warrants it, use `/swarm review ...` through the orchestrator so it can add `performance-reviewer`, `reliability-reviewer`, or `onboarding-reviewer` on top of this core kernel.

## When to use

- After completing a feature before calling it done
- When the user says "swarm it", "swarm review", or "cluster swarm"
- Before creating a handoff for another agent
- After a large refactor to catch cross-component drift

## When to scale down

For changes touching fewer than 3 files with no Critical/High risk files, consider `/review` instead — it's lighter and faster.

## Related commands

- `/swarm-fix` — same core four agents but **fixes** everything Medium+ after reviewing
- `/regressions` — narrower: dependency/mock/parity checklist (no expert lenses)
- `/swarm-context` — explore a topic, not review a diff
