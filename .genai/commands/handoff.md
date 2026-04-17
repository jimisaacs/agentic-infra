# Handoff to another agent

The user runs multiple agents in parallel. When they say "summarize for another agent" or "hand this off", produce a structured handoff in this format.

## Scope

**Cover this session's changes.** The handoff should describe what *you* did in this conversation — files you edited, decisions you made, issues you found. When the prompt provides context (e.g., "hand off the auth work"), narrow the summary to that subset.

## Temporal anchor

Every handoff must include a temporal header so the receiving agent knows *when* this work happened. Run these commands to gather the data:

```bash
date -Iseconds                    # current wall-clock time
git rev-parse --short HEAD        # current commit SHA
git log --oneline -1              # latest commit summary
```

## Output format

```markdown
## Session: [Short title]
- **Date:** [ISO 8601 timestamp from `date -Iseconds`, e.g. 2026-04-02T14:30:00-07:00]
- **Git HEAD:** [short SHA from `git rev-parse --short HEAD`]
- **Uncommitted changes:** [yes/no — from `git status --short | wc -l`]

### What changed
[List every file modified with a one-line description of the change]

### What works now
[Bullet list of behaviors that are now working]

### What's left / known issues
[Bullet list of incomplete work, known gaps, or things the next agent should check]

### Warnings for the next agent
[Things the next agent MUST NOT do, or things that will break if they're not careful. Be specific and stern.]
- DO NOT [specific action] — it will break [specific thing] because [reason]
- [Area X] is fragile right now because [reason] — test after any change
- [Pattern Y] looks wrong but is intentional because [reason] — don't "fix" it

### What I tried that didn't work
[Negative knowledge — approaches that failed and why. This prevents the next agent from repeating mistakes.]
- Tried [approach] → failed because [reason]
- Considered [alternative] → rejected because [trade-off]

### Regressions to watch for
[Specific behaviors that could break if the next agent isn't careful — this is critical, the user hates regressions]

### Files the reviewing agent should read
[Ranked list of files most relevant to reviewing this work]

### Learnings to append
[New entries for `.cursor/learnings.md` — gotchas discovered in this session that future agents need to know. Append these to the learnings file now.]
```

## Rules

- Full file paths from repo root.
- Always include temporal header.
- If you modified interfaces or shared DTOs, list downstream files that need sync.
- Don't minimize issues — if something is half-done, say so.
- **Omit empty sections** rather than writing "N/A" or "None."
- **Budget: the entire handoff must fit in ~80 lines.** If your session touched many files, group by area instead of listing each file individually. The receiving agent can read files — it needs a map, not a transcript.
- **Append learnings** to `.cursor/learnings.md` if you discovered something new.
