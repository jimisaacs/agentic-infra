# Checkpoint

Captures the current working state so you (and the user) know what's solid before continuing. Use this to structure the "one more pass" loop — if a checkpoint produces zero findings, the work is done.

## When to use

- After completing a feature, before starting polish passes
- Between polish passes, to know if you've converged
- Before starting a new phase of work that could introduce regressions
- When the user says "checkpoint", "save state", "what's working now"

## How to run it

### 1. Capture current state

```bash
git diff --stat
git diff --cached --stat
```

### 2. Run verification (if applicable)

If you touched compiled code or scripts covered by CI:

Run **project checks** per the repository docs.

If you only touched docs, rules, skills, or commands — skip this step when checks don't apply to those files.

### 3. Assess what's solid

For each area you've touched, classify:

| Area | Status | Notes |
|------|--------|-------|
| [component] | **Solid** / **Fragile** / **Incomplete** | [one-line detail] |

- **Solid**: Verified working, tests pass, no known issues
- **Fragile**: Works but has edge cases, missing error handling, or untested paths
- **Incomplete**: Partially implemented, known gaps

### 4. Report findings from this pass

If this is a polish checkpoint (not the first one), compare against the previous checkpoint:

```
Checkpoint #N:
- Project checks: PASS / FAIL (detail if fail)
- Findings this pass: [count]
- Fixes applied: [list]
- Remaining: [list or "none — converged"]
```

### 5. Convergence signal

If this pass produced **zero findings** (nothing to fix, nothing to flag):

> **Converged.** No findings this pass. The work is solid. Ready for commit or handoff.

Tell the user explicitly. Don't manufacture findings to seem thorough — if it's clean, it's clean.

## Checkpointing across passes

The user's typical rhythm is: build → checkpoint → polish → checkpoint → polish → checkpoint (converged). Each checkpoint should be clearly numbered so both you and the user can see the trajectory. Decreasing findings per pass = healthy convergence. Steady or increasing findings = something is structurally wrong.

## Related commands

- `/polish` — the work between checkpoints
- `/regressions` — deeper regression analysis (use when checkpoint reveals fragile areas)
- `/verify` — full verification gate (checkpoint is lighter)
