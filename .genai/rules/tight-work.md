# Tight Work

Quality isn't a phase after the build — it's part of the work. When you finish the main task, tighten it before presenting it as done. No user prompt needed. Scale effort to scope.

## Scope classification

Customize this risk matrix for your project:

| Risk | File patterns | Why |
|------|-------------|------|
| Critical | Core interfaces, auth, service layer | Changes here break everything |
| High | Business logic, transport, API handlers | Wire format and behavior |
| Medium | Stores, UI pages, persistence implementations | Consumer-side |
| Low | CSS, docs, skills, rules | Style and documentation |

## Tiers

**Tier 1 — Trivial** (1-2 files, Low risk): Format, self-review diff, run checks.

**Tier 2 — Normal** (3-9 files, or Medium+ risk): Tier 1 + polish inline (dead code, unused imports, error wrapping) + regression checklist + rebuild if needed + run checks + brief summary.

**Tier 3 — Significant** (10+ files, cross-cutting, interface/DTO/auth changes): Tier 2 + launch explore agents on Critical/High files to verify downstream callers + fix findings + re-check + summary with regression table.

## Regression checklist (Tier 2+)

For each changed file: What existing behavior depends on this? Changed an exported symbol → search all callers. Changed a DTO/wire format → check client types, models, docs, mocks. Changed an interface → verify every implementation and mock. Changed auth → test all access paths. Changed store shape → check every consumer.

## What tight work is NOT

Not scope expansion. Tight work polishes what you built — no new abstractions, API generalization, or rewrites. That's **Refine**, not redesign.
