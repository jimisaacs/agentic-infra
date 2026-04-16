# Maintenance

## 1. Single source of truth

Every piece of information lives in one place. Other locations point to it. `.genai/rules/` is canonical for rule prose; `.cursor/rules/*.mdc` are thin wrappers. AGENTS.md is the overview; skills are depth. Don't repeat skill-level detail in AGENTS.md.

## 2. No derived metadata in rules

Don't encode values in agent-facing docs that change as a side effect of normal work. If there's no mechanism keeping it accurate, it will drift silently and become misinformation that agents trust. Examples: exact line counts, file counts, specific line numbers, version strings copied from a lockfile, counts of implementations. Instead, state the decision or the name — things that only change when someone intentionally changes them.

**Test:** "Will editing the code this doc describes also invalidate something written in this doc?" If yes, remove it.

## 3. File size discipline

| Language | Warning | Split trigger |
| ---------- | --------- | -------------- |
| Go | > 500 lines | > 800 lines |
| TypeScript | > 400 lines | > 600 lines |
| CSS | > 300 lines | > 500 lines |
| Swift | > 500 lines | > 800 lines |
| Python | > 400 lines | > 600 lines |

## 4. Deferred code doesn't live in trunk

If a feature is tagged as future work with zero references, delete it. Git preserves intent. Rebuild when the milestone starts.

## 5. Update protocol

Customize this for your project's doc surface:

Code → run checks. API/wire → protocol docs. Feature → status doc. Milestone → roadmap. Architecture fork or changed forcing context → decision backlog. Settled decision or meaningful re-evaluation outcome → ADR. Gotcha → learnings file. Convention → AGENTS.md.

## 6. Doc classification

**Normative** (must match code): protocol docs, status, AGENTS.md, skills. **Governance** (decision discipline, not wire truth): decision backlog, ADRs. **Narrative** (design intent): vision docs, design papers. Update normative on every relevant change; update governance when architectural choices open, settle, or need re-evaluation; update narrative when direction changes.

## 6.1 Decision freshness

Accepted ADRs are assumed correct until challenged. Re-evaluate them when scale changes materially, new constraints or capabilities appear, implementation repeatedly strains against the choice, or the evidence behind the choice is old enough that you would want to reproduce it before relying on it again. Re-evaluation ends with either reaffirming the ADR or creating a superseding ADR.

## 7. Progressive-disclosure structure

Large or high-churn directories should have a small `README.md` map. The map should say:

- what the folder owns
- which files to read first for common tasks
- which surfaces are generated or mechanical
- which deeper docs or skills to open next

When an always-on file starts collecting tables, command catalogs, or long checklists, move that depth behind a pointer. Maps stay small; indexes route; depth explains.
