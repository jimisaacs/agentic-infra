# Verify

Prefer the project's control plane when it exists. In this template, start with `./dev verify`.

## Scope

**Project checks** usually run the full gate — they may not be file-scoped. But the **doc/hygiene checks** (steps below) should focus on files you changed in this session. When the prompt provides context (e.g., "verify after the API refactor"), focus the manual review on those files.

## Steps

1. **Full gate** — Always start here:

Run the project's documented verification path. For this template, that means `./dev verify`.

If your session changed the local `project-context` runtime, `.cursor/mcp.json`, or the Git hook wrappers, also run `./dev context smoke`.

1. **Documentation** — When behavior, APIs, or conventions changed, update the minimal set your project expects:
   - Component or service status notes (e.g. `STATUS.md` or equivalent)
   - Agent/contributor guide if conventions shifted
   - Protocol or API docs for endpoints, schemas, or contracts
   - Roadmap or changelog for milestone progress
   - Relevant `.cursor/skills/**/SKILL.md` if patterns moved

1. **Final hygiene** — Scan the diff mentally or with search:
   - No `ACCEPTED_RISK` (or equivalent) without a short, concrete justification
   - No hardcoded secrets, tokens, or production URLs
   - No local data dirs or generated secrets staged for commit

## Verification checklist

- [ ] Project checks pass
- [ ] Runtime smoke passes when the local `project-context` surface changed
- [ ] Docs/skills updated when contracts or status changed
- [ ] Diff free of empty risk markers, secrets, and data dirs
