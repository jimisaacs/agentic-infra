# Decisions

This folder records load-bearing architecture decisions using progressive disclosure:

- `DEC-xxxx` lives in the backlog while a decision is active. Resolved or dropped rows may remain as short closing pointers.
- `ADR-xxxx` records a settled or superseded architectural decision.
- [`../design/README.md`](../design/README.md) (or your project’s design-doc location) holds the deep background when a short record is not enough.

## Read Path

1. Read this file.
2. Read `backlog.md` for open forks or `adr/README.md` to find one relevant ADR.
3. Open [../design/README.md](../design/README.md) and then the linked design docs only if the short record is not enough.

## What Lives Here

| File | Role |
| --- | --- |
| `backlog.md` | Active architectural decisions plus short resolved or dropped pointers |
| `adr/README.md` | ADR index, statuses, and read path |
| `adr/template.md` | Agent-friendly ADR template plus canonical example |
| `adr/ADR-xxxx-*.md` | Settled or superseded architectural decisions |

## Split Of Responsibilities

- `docs/decisions/` explains architectural choices and open forks.
- `docs/design/` holds deeper rationale, reference architecture, and design research.
- [`../ROADMAP.md`](../ROADMAP.md) says when work happens.
- [`../../STATUS.md`](../../STATUS.md) says what works now.
- Protocol docs and schema docs, when a downstream project adds them, define current wire truth.

## For Agents

- Create a `DEC-xxxx` entry only for unresolved, load-bearing architectural choices.
- Create an `ADR-xxxx` when the choice is settled or when a prior ADR is superseded.
- Frame the choice in the current context and operating range before picking a pattern, product, or style.
- Compare like-for-like options at one scope; if the current design is still viable, treat it as an option.
- Prefer citing an existing `DEC` or `ADR` by ID instead of restating the choice.
- Keep tradeoffs, confidence, and unknowns explicit.
- If implementation conflicts with an accepted ADR, do not drift silently: either update the implementation or supersede the ADR.
- For accepted ADRs touching identity, authorization, trust, or tenant isolation, ask the user before superseding.
- Re-evaluate an ADR when scale, constraints, or implementation pressure meaningfully change.

Agent workflow may live in your project’s AI rules (for example `.genai/rules/decision-records.md`).

## Decision Weight Rule

Create a decision record only if the choice affects one or more of:

- System boundaries such as service edges, APIs, or transport
- Identity, authorization, or trust semantics
- Data shape or long-lived storage contracts
- Scaling strategy or performance characteristics
- Cross-component behavior or architectural invariants

Do not create decision records for local refactors, internal naming, obvious implementation choices, or one-off bugs. When unsure, prefer not creating one.

When you do create one, phrase it around the problem and forcing constraint rather than a preferred tool.

## Conflict Rule

If implementation contradicts an accepted ADR:

1. Confirm the contradiction is real, not a misunderstanding.
2. If the ADR is still correct, update the implementation.
3. If the implementation is correct, create a superseding ADR.
4. Never silently diverge from an ADR.

Minor deviations that do not affect the core decision do not require supersession.
For accepted ADRs touching identity, authorization, trust, or tenant isolation, ask the user before superseding.

## Decision Freshness

Accepted ADRs are assumed correct until challenged. Re-evaluate them when:

- System scale or usage changes significantly
- New constraints or capabilities emerge
- Supporting evidence or measurements are old enough that you would want to reproduce them before relying on them again
- Implementation repeatedly strains against the decision

Re-evaluation should end with either reaffirming the ADR or creating a superseding ADR.
