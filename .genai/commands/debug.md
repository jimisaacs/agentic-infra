# Debug

Follow the project's documented control plane and local environment story. In this template, start with `./dev doctor`, `./dev status`, `./dev fmt`, and `./dev verify`. If the failure involves the local self-query runtime, use `./dev setup`, `./dev context status`, and `./dev context smoke`.

## Scope

**Prompt-driven.** When the prompt describes a specific failure (e.g., "debug the unit test failure" or "debug why the dev stack won't start"), focus on that failure. Otherwise, start broad with **environment status** (however your project exposes it: compose status, process list, health endpoint, etc.).

## Steps

1. **Check what's running** — Start with the basics your repo documents (containers, local servers, required services).

1. **Read the logs** — If tests or the dev stack failed, capture logs from the relevant service or test runner.

1. **Classify the failure**:

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Compile error | Missing import, type mismatch, unimplemented interface | Fix the code, re-run project checks |
| Unit/integration test failure | Logic bug, stale mock, missing test double method | Read output; fix mock or logic |
| Typecheck error | Type error in app or client code | Fix at the reported location |
| Linter / formatter failure | Style or lint drift | Run the project's format/fix command, then project checks |
| Service won't start | Config issue, port conflict, missing dependency | Check status; restart stack cleanly |
| Local MCP/runtime not ready | Missing bootstrap, missing index, or stale runtime | Run `./dev setup`, then `./dev context status` and `./dev context smoke` |
| Message broker / RPC "no responders" | Service not registered or wrong address | Check registration and connection config in logs |
| Connection refused | Backend or dependency not ready | Wait for health; restart stack |

1. **Capture context** — Before investigating further, gather evidence: recent log lines, status output, exact command and exit code.

If a specific test failed, re-run it in isolation and capture the output.

Save error messages and stack traces verbatim — you'll reference them later.

1. **If the primary CLI or entry script fails** — Verify it runs at all (`./dev help` or the repo's equivalent). If the binary or script is stale, rebuild or reinstall per project docs.

1. **If you need to inspect a runtime environment** — Use the project's supported shell/exec into container workflow for debugging only.

## Narrowing down

1. **Minimal reproduction** — After identifying the area, isolate to the smallest reproducible case:

- If it's a test failure: can you reproduce with just that test file? Check if the failure is consistent or flaky.
- If it's runtime: what's the smallest request or flow that triggers it? Strip away unrelated setup.
- If it's a startup failure: does a clean restart reproduce it?

1. **Bisection** — When the cause isn't obvious from the error:

- Check recent changes to the affected area:

```bash
git log --oneline -10 -- <affected-file-or-directory>
git diff HEAD~5 -- <affected-file-or-directory>
```

- Narrow to the specific change that introduced the failure. Look at the diff for the affected file — what changed recently that could cause this symptom?

## Escalation

1. **When to stop debugging alone:**

- If the issue spans multiple components — escalate to `/swarm-context` on the affected area for multi-perspective analysis.
- If the issue involves auth, tokens, or sensitive data — use your project's security skill or guide if available.
- If you've spent more than 3 investigation cycles without progress — summarize what you know, what you tried, and what you ruled out. Ask the user before going deeper.

## Closing protocol

1. **Before reporting resolution:**

- Verify the fix passes targeted tests and **project checks**.
- Check for regressions: run `/regressions` scoped to the files you changed during the fix.
- Report to the user with this structure:
  - **What failed**: the symptom and where it occurred
  - **Root cause**: what was actually wrong
  - **Fix applied**: what you changed (files and nature of change)
  - **Verification**: test and check results
