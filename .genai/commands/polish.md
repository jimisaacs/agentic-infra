# Polish pass

> **Pipeline context:** Phase 1 of `/tighten`. Also composable via `/swarm`. Standalone use: when you want just the hygiene pass without the full review pipeline.

The user asks for this after the main work is done. "One more pass for polish and hygiene."

## How to run it

Follow the [session QA checklist](_session-qa-checklist.md) for scope determination, risk classification, and cross-cutting checks. Then apply the hygiene and polish buckets below to every file in scope.

### Code hygiene
- Remove dead code, unused imports, stale comments
- Consistent error wrapping and propagation (language-idiomatic)
- No raw internal errors leaking to callers at trust boundaries
- Empty collections serialized consistently (no accidental null vs empty mismatches)
- Typed constants for enums, not bare strings where the codebase uses that pattern

### UI polish (if client/UI changed)
- Alignment and spacing consistent with the **design system tokens** (CSS variables, theme, or component library as defined by the project)
- No outer margins on leaf components when the parent owns spacing via `gap` or layout
- Status and semantic colors use the project's token or variant names
- Form robustness: keyboard submit, focus management, error states
- Responsive layout doesn't break at reasonable widths

## Verification

Run **project checks** (tests, lint, typecheck) per the repository docs.

## Output

Short summary: what you fixed (severity-sorted, one line each) and what you flagged for the user. No narration. If you found nothing, say so in one line.

## Related commands

- `/checkpoint` — run after each polish pass to track convergence (findings decreasing → converged)
- `/regressions` — deeper regression analysis if polish uncovered structural issues
