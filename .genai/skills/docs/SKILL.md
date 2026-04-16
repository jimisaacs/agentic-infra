# Documentation

This repo treats documentation as infrastructure (P9: self-documenting). Docs are part of the product, verified by the control plane, and maintained as part of every change. This skill covers the doc architecture and authoring patterns.

## Quick Reference

| I need to... | Read |
|---|---|
| Understand the doc hierarchy | Map → index → depth |
| Know when to update docs | Update triggers |
| Record an architecture decision | Decision records |
| Write or update a walkthrough | Walkthroughs |

## Map → index → depth

The doc architecture follows the `context-efficiency` rule: maps first, then indexes, then depth.

**Maps** (always-loaded, kept small):
- `README.md` -- repo-level orientation
- `AGENTS.md` -- agent-facing guide
- `CLAUDE.md` -- Claude Code entrypoint
- `STATUS.md` -- what works now

**Indexes** (loaded on demand):
- `docs/decisions/README.md` -- decision record index
- `docs/design/README.md` -- design doc index
- `.genai/skills/README.md` -- skills index
- `.genai/learnings-index.md` -- learnings domain index

**Depth** (loaded only when the task touches that area):
- Individual ADRs, design docs, skill files, rule files

Keep maps short and scannable. Depth lives behind indexes. See the `maintenance` rule for SSOT policy and update protocol.

## Update triggers

When you finish a change, check whether these docs need updating. See the `maintenance` rule for the full protocol.

| What changed | Update |
|---|---|
| Control plane (`./dev`) | `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` |
| Project layout | `project/README.md`, `project-layout` rule |
| Architecture or trust boundary | `docs/decisions/` (ADR or DEC entry) |
| Teaching story | `STATUS.md`, `docs/ROADMAP.md`, walkthrough |
| Principles or conventions | `docs/PRINCIPLES.md` or `docs/CONVENTIONS.md` |

`./dev verify` enforces doc contracts -- if a doc promises something that's missing, verify catches it.

## Decision records

Use the `decision-records` rule for the full workflow. Summary:

- **DEC-xxxx**: open architectural fork (tracked in `docs/decisions/backlog.md`)
- **ADR-xxxx**: settled decision (in `docs/decisions/adr/`)
- Create a record when the choice affects boundaries, auth, data contracts, scaling, or invariants
- Don't create one for routine implementation choices

## Walkthroughs

Each stack branch has a walkthrough under `walkthrough/`. Walkthroughs are teaching docs that explain what the branch adds and why.

Pattern:
- State what branch you're on and what changed
- Explain the teaching point (why this is a separate layer)
- Point to specific files to open
- End with "what to understand before moving on" and a navigation pointer

Every claim in a walkthrough must be verifiable against the actual branch content. Forward references to later layers are navigation aids only -- don't describe features as if they exist.

## Anti-patterns

- Don't let maps grow into depth docs -- maps stay short, depth lives behind indexes
- Don't duplicate content between maps -- one canonical home per fact (SSOT)
- Don't describe features that don't exist on the current branch
- Don't skip doc updates when changing the control plane or architecture
- Don't write walkthroughs that can't be verified by reading the code
