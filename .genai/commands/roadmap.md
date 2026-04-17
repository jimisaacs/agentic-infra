# Roadmap review

Leo calls the team together. Four specialists with different lenses stress-test the roadmap — then Leo synthesizes with strategic clarity and Raph's honesty. We look at what shipped, what's next, where the gaps are, and whether the story still holds. Then we decide together what to change.

**Leo coordinates, the specialists report, you decide.**

## How to run it

1. **Read current state.** Read `docs/ROADMAP.md`, `STATUS.md` (or equivalents), and recent `git log --oneline -10`. Understand what shipped, what's in progress, what's stale.

2. **Read the PM methodology.** If the repo has a PM or product skill under `.cursor/skills/`, load it for the full methodology. Otherwise use this command's structure only.

3. **Launch the product reviewer swarm** (4 parallel agents):

```text
Task(subagent_type="generalPurpose", prompt="As a PM/TPM: Review the roadmap for milestone health, deferral tracking, and product narrative coherence. Apply solid PM methodology. [include roadmap content]")

Task(subagent_type="architecture-reviewer", prompt="Review the roadmap for scale ceilings, infrastructure gaps, and invariant compliance. [include roadmap content]")

Task(subagent_type="generalPurpose", prompt="As a pragmatic staff engineer: timeline reality check, scope honesty, what to cut, what to prioritize. [include roadmap content]")

Task(subagent_type="generalPurpose", prompt="As a product visionary: differentiation check, competitive positioning, missing memorable moments, product narrative gaps. [include roadmap content]")
```

If the roadmap needs a contrarian pass, optionally add Shredder as a 5th reviewer by sourcing the capsule from `.genai/personas/records/shredder.md` and following `/challenge`.

1. **Synthesize.** Consolidate findings into:
   - Milestones that need updating (completed, stale, scope-crept)
   - Gaps (missing milestones, untracked deferrals)
   - Priority adjustments (reorder, merge, split)
   - Product narrative check (is the differentiator on track?)

1. **Update.** Apply changes to `docs/ROADMAP.md` and `STATUS.md` (or equivalents). Run **project checks** if your changes could affect builds (usually unchanged for doc-only edits).

## When to use

- Start of a new planning session
- After completing a milestone
- "What should we work on next?"
- "Is the roadmap still right?"
- "Swarm the roadmap"
- Quarterly review / major direction change

## Variants

- **`/roadmap check`** — read-only review, no updates. Report findings.
- **`/roadmap update`** — review + apply changes to docs.
- **`/roadmap next`** — just answer "what's the most impactful thing to do next?"
- **`/roadmap scale`** — focus on scale ceilings and infrastructure gaps.

## Related commands

- `/whatnow` — quick, opinionated "what should I work on?" (vs roadmap is a comprehensive review)
- `/swarm-plan` — validate a specific plan (vs roadmap reviews the whole direction)
- `/swarm-context` — deep exploration of a topic (vs roadmap is about priorities)
- `/impact` — blast radius of a specific change (vs roadmap is about sequencing)
