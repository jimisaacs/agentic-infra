# Regressions

> **Pipeline context:** Phase 2 of `/tighten`. Also composable via `/swarm`. Standalone use: when you want just the dependency breakage scan.

The owner's #1 frustration is agents introducing regressions. This command systematically checks changed files for downstream breakage.

## How to run it

Follow the [session QA checklist](_session-qa-checklist.md) for scope determination, risk classification, and cross-cutting checks.

Then, for each Critical/High file, launch a targeted explore agent:

```
Task(subagent_type="explore", prompt="File [path] was modified. Find the top downstream dependencies of the changed symbols. Return a table: dependency | status (in sync / stale) | issue. Max 10 rows — focus on highest-risk dependencies.")
```

Launch these in parallel for all Critical/High files in scope.

## Report format

Report as a table:

| File changed | Downstream dependency | Status | Issue |
|-------------|----------------------|--------|-------|
| `internal/contracts/repos.go` | `testutil/mocks.go` | In sync | -- |
| `internal/contracts/repos.go` | `service_test.go` | **STALE** | Missing `NewMethod` stub |

## When to use

- After any non-trivial code change, before calling it done
- When the user says "did you break anything?" or "check for regressions"
- Before creating a handoff — the next agent shouldn't inherit your regressions

## When to scale down

For single-file changes to Low/Medium risk files, a manual grep for references is sufficient — skip the explore agent fan-out.

## Related commands

- `/swarm-review` — broader: the core four reviewer kernel (security, architecture, migration, evidence) vs this dependency/parity checklist
- `/impact` — **before** making a change (blast radius); this is **after** (did it break?)
