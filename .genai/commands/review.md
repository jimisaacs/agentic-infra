# Review

Review current work for quality. Never run git commands that change anything — read-only only.

## How to run it

Follow the [session QA checklist](_session-qa-checklist.md) for scope determination, risk classification, cross-cutting checks, and per-language file verification.

Then, for each changed file:

1. Read the diff and evaluate correctness, safety, and consistency
2. Check for secrets, tokens, or `.env` content in the diff
3. Run **project checks** (tests, lint, typecheck) as documented in the repo

## Report format

List issues by severity:

- **Critical** — breaks functionality, security hole, data loss risk
- **High** — incorrect behavior, missing parity, stale mocks
- **Medium** — inconsistency, missing docs, suboptimal pattern
- **Low** — style, naming, minor cleanup

**Do not fix anything unless asked.** The default job is the report. The user decides what to act on.
