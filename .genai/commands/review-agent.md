# Review agent

The user runs parallel agents. When they paste another agent's summary or diff and say "review their work" or "review and fix", do a thorough adversarial review.

## Scope

**Prompt-driven.** The target is another agent's work — identified by pasted summary, diff, or prompt context (e.g., "review the work from the previous session on API handlers"). Focus on the files and changes described, not the entire repo.

## How to run it

1. **Don't trust the summary.** Read every file the other agent claims to have changed. Verify the changes are actually there and correct.

2. **Launch 5 parallel checks**. Review agents may adopt personas from the central catalog when your project uses them. Use `.genai/personas/roles.md` for selection and source the selected capsule from `.genai/personas/records/<id>.md`.

```text
Task(subagent_type="explore", prompt="Check these files for completeness: [list]. Verify: interfaces have all implementations, mocks are in sync, tests compile, no duplicate function definitions.")

Task(subagent_type="security-reviewer", prompt="Review these changes for auth, isolation, and trust-boundary issues: [list with descriptions]")

Task(subagent_type="architecture-reviewer", prompt="Review these changes for API/contract consistency, layering, and whether public surfaces match internal behavior: [list with descriptions]")

Task(subagent_type="migration-checker", prompt="Review these changes for propagation completeness. Did every rename, schema change, generated type, config key, and doc reference update consistently across layers? [list with descriptions]")

Task(subagent_type="evidence-reviewer", prompt="Review these changes for proof of correctness. Which behaviors are directly covered by tests, fixtures, mocks, or verification, and what changed behavior is still unsupported? [list with descriptions]")
```

1. **Check what the other agent missed** — things they should have done but didn't:
   - Did they update contract/schema docs when changing external behavior?
   - Did they update client types or codegen when models changed?
   - Did they cover all transport or API paths the architecture expects?
   - Did they update test doubles and integration tests?
   - Did they check for regressions in their own work?

2. **Fix issues you find** — don't just report. The user said "review and fix."

3. **Report concisely**:
   - Fixed: [file — one-line description] per item
   - Questionable (needs user decision): [file — question]
   - Don't list things you left alone — the user only needs to know what changed and what needs their input.

## When to use

- When the user pastes another agent's work summary
- When the user says "review their work", "review and fix", "go behind that agent"
- When the user shows a diff from another chat and wants verification
