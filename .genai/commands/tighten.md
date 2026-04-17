# Tighten

The full treatment — swarm review, regression check, convergence loop. Everything the agent does automatically when your project defines a **tight-work** rule (if present), plus the swarm layer on top.

Use when:
- You want expert-level review before committing
- A big task just landed and you want assurance beyond automatic hygiene
- You say "tighten it", "tighten the auth work", "one more tighten pass"

## Pipeline

### Phase 1: Polish (direct)

Follow the [polish checklist](polish.md) on session-changed files:
- Dead code, unused imports, stale comments
- Error wrapping and propagation; empty collection handling; typed constants where the codebase uses them
- UI alignment and spacing (if client/UI touched)
- Fix everything you find inline

### Phase 2: Regression check (parallel agents)

Identify Critical/High files from the [session QA checklist](_session-qa-checklist.md) risk matrix. For each, launch an explore agent:

```
Task(subagent_type="explore", prompt="File [path] was modified. Find the top downstream dependencies of the changed symbols. Return a table: dependency | status (in sync / stale) | issue. Max 10 rows — focus on highest-risk dependencies.")
```

Launch all in parallel. Fix any stale dependencies found.

### Phase 3: Adaptive swarm review (parallel agents)

Select review agents using the roster model in `/swarm`. Use the core four-reviewer kernel for substantive changes, then add specialists by trigger. Scale down only for trivial low-risk work.

Each agent prompt includes:
- Changed files with one-line descriptions
- Nature of change (feature, refactor, bugfix)
- "Report findings only — do not make changes"

### Phase 4: Fix Medium+ findings

Consolidate findings from the regression scan and swarm review into a severity-ranked table. Phase 1 polish issues should already be fixed inline. Fix:
- **Critical/High**: immediately
- **Medium**: if straightforward; flag if it needs a design decision
- **Low**: if trivial; otherwise note
- **Informational**: skip

### Phase 5: Verify

Run **project checks** (tests, lint, typecheck) per the repository docs.

### Phase 6: Checkpoint

Report convergence state:

```
Tighten pass:
- Project checks: PASS / FAIL
- Findings from swarm: [count by severity]
- Fixed: [list]
- Remaining: [list or "none — converged"]
```

### Phase 7: Converge (if needed)

If findings remain after fixing, run one more polish + verify loop. Cap at 2 total iterations — if it hasn't converged by then, report what's left as open items.

### Phase 8: Final report

If converged:
> **Tight.** No remaining findings. Project checks pass.

If not converged, list open items per your project's delivery rule (if any).

## Scaling

| Scope | Approach |
|-------|----------|
| Trivial (1-2 files, Low risk) | Skip `/tighten` — automatic tight-work + local review may be sufficient |
| Normal (3-10 files) | Core four-reviewer kernel plus specialists by trigger |
| Large (10+ files, cross-cutting) | Core kernel plus every relevant specialist |

## Related commands

- **Tight-work rule** (when present) — the automatic version agents do without being asked (polish + regressions + verify)
- `/swarm-review` — report only (no fix)
- `/swarm-fix` — review + fix (no convergence loop)
- `/polish` — just the hygiene pass
- `/regressions` — just the dependency check
