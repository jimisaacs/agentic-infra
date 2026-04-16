# Decision Records

Use this rule when architectural work is in scope: invariants, boundaries, identity/auth/trust semantics, transport, scaling path, long-lived data contracts, or edits under `docs/decisions/`.

## 1. Read path

Use progressive disclosure:

1. Read `docs/decisions/README.md`
2. Read `docs/decisions/backlog.md` for open forks or `docs/decisions/adr/README.md` to find one relevant ADR
3. Open linked design material only if the short decision record is not enough

Do not load the whole decisions directory by default.

## 2. Decision types

- **`DEC-xxxx`** — active architectural decision in `docs/decisions/backlog.md`
- **`ADR-xxxx`** — settled or superseded architectural decision in `docs/decisions/adr/`

Use `DEC` while the choice is active. Use `ADR` once the choice is settled. If nothing load-bearing is being decided, use neither.

## 3. Decision Weight Rule

Create a `DEC` or `ADR` only if the choice affects one or more of:

- System boundaries such as service edges, APIs, or transport
- Identity, authorization, or trust semantics
- Data shape or long-lived storage contracts
- Scaling strategy or performance characteristics
- Cross-component behavior or architectural invariants

Do not create decision records for:

- Local refactors or internal structure
- Naming changes unless they affect external contracts
- Obvious implementation choices with no meaningful alternatives
- One-off fixes or bugs

When unsure, prefer not creating a decision record.

## 4. Create a DEC

Create a new `DEC-xxxx` entry only when:

- No existing `DEC` or `ADR` already covers the choice
- The decision is unresolved
- You can state what event forces the decision

Every backlog row should stay compact and include:

- Stable ID
- Status
- One-line decision title that names the fork, not the favored answer
- `Trigger / deadline`
- Short options or tension, phrased at one scope and abstraction level
- Links to the roadmap, status, design docs, or ADR that matter

Ground rules:

- Start from the current context and forcing constraint; if the current design is still viable, treat it as an option.
- Use precedent, market defaults, and anecdotes as inputs to compare, not as the decision itself.
- If one row mixes system-wide structure with a local implementation or product choice, split it into separate decision work.

If you cannot state a forcing trigger or deadline, the item is probably not ready for the backlog.

## 5. Write an ADR

Use `docs/decisions/adr/template.md`.

Rules:

- One ADR records one settled architectural decision
- Use the fixed field order from the template
- Keep the decision statement to one line
- `Context` should name the operating range, relevant constraints, and non-goals that make the decision necessary now
- Keep `Context`, `Alternatives considered`, `Consequences`, and `Review signals` terse
- Compare like-for-like alternatives; include keeping the current design when it is still a real option
- Keep structural/style choices separate from local implementation or product/vendor selection unless the choice is inseparable
- Make tradeoffs, confidence, and unresolved unknowns explicit; distinguish measured evidence from judgment
- Link to current benchmarks, incidents, spikes, or design docs when they materially support the choice
- Link out to design docs for deep rationale instead of expanding the ADR
- Popularity, defaults, and single-project anecdotes can suggest options, but they do not close the ADR
- Use `accepted` or `superseded` for ADR status

If an ADR needs multiple unrelated rationales or compares options at different abstraction levels, split it.

When a `DEC` is resolved, mark the backlog row resolved, link the resulting ADR, and keep the row terse. If the backlog starts getting noisy, prune old resolved rows after source docs point at the ADR.

## 6. Conflict Rule

If implementation contradicts an accepted ADR:

1. Confirm the contradiction is real, not a misunderstanding
2. If the ADR is still correct, update the implementation
3. If the implementation is correct, create a new ADR that supersedes the old one
4. Never silently diverge from an ADR

Minor deviations that do not affect the core decision do not require supersession.

For accepted ADRs that touch identity, authorization, trust, or account isolation, ask the user before superseding.

## 7. Decision Freshness

Accepted ADRs are assumed correct until challenged, but re-evaluate them when:

- System scale or usage changes significantly
- New constraints or capabilities emerge
- Supporting evidence or measurements are old enough that you would want to reproduce them before relying on them again
- Implementation repeatedly strains against the decision

When reusing older measurements, benchmarks, or vendor guidance, confirm that they still match the current versions, scale, and operating conditions.

Re-evaluation should end with either reaffirming the existing ADR or creating a superseding ADR.

## 8. Reference over repetition

- Cite `DEC-xxxx` or `ADR-xxxx` in plans, handoffs, reviews, roadmap notes, and design docs when architecture is relevant
- Prefer linking to a decision record instead of restating the same rationale
- If the architecture changes, create a superseding ADR rather than rewriting history inside the old ADR

## 9. Boundaries

Customize these for your project:

- Roadmap answers **when**
- Status doc answers **what works now**
- Protocol/schema docs answer **what the system does today**
- `docs/decisions/` answers **why this architecture was chosen** or **which architectural fork is still open**
