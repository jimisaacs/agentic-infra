# AI Infrastructure

Principles for working on the AI infrastructure itself: rules, skills, commands, agent definitions, `AGENTS.md`, `CLAUDE.md`. This rule loads by file glob — it only appears when you're editing these files.

## 1. Token economy

Rules and skills are a token budget. Every always-on line competes with the user's actual task.

- **Map → Index → Depth.** Always-on files stay at map level (pointers, not content). Indexes route to depth. Depth lives in skills and docs that load on demand.
- **Modularize by concern.** One rule per concern. If a rule covers two unrelated topics, split it.
- **Pointers over duplication.** Reference the SSOT; don't copy content across files. When two files say the same thing, one of them is stale.
- **Loading gate.** Before adding guidance, ask: does every chat need this, or only chats touching this domain? Prefer file-scoped (`globs`) or intelligent (`description`) over always-on. See `context-efficiency.md` for the operational retrieval ladder.

## 2. Drift prevention

Rules and skills are the mechanism that prevents architectural drift across agents and sessions. They are load-bearing — not documentation.

- **Encode established patterns.** When a pattern is proven in code (two+ real uses, or a deliberate architectural choice), capture it in the relevant rule or skill. Unencoded patterns drift.
- **Update on conflict.** When an encoded pattern conflicts with how the code actually works, update the rule. Stale rules cause more drift than missing ones.
- **Consistency over local optimization.** A rule that all agents follow consistently beats a "better" pattern that only one agent knows. Prefer incremental rule evolution over wholesale rewrites.
- **Model selection matters.** Fast models follow explicit patterns well but won't infer unstated conventions. Encoding patterns in rules directly improves fast-model output.

## 3. Self-maintenance

The AI infrastructure is a product surface. Apply the same discipline here that we apply to code.

- **SSOT.** `.genai/rules/` is canonical prose; `.cursor/rules/*.mdc` are thin wrappers. Skills are depth. `AGENTS.md` is the map. Don't duplicate across layers.
- **File size limits.** Same thresholds as code (see `maintenance.md`). A 500-line rule is a skill that hasn't been extracted yet.
- **Downstream awareness.** Before changing a rule, consider: which skills reference it? Which agent types load it? Which file globs trigger it? Changes propagate.
- **Regression awareness.** Removing guidance from a rule can re-introduce the drift it was preventing. Delete with the same care as deleting a test.
- **The infra maintains itself.** When working on rules/skills, this rule loads automatically. The infrastructure accounts for its own maintenance — no special invocation needed.
