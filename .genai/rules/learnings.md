# Learnings

Treat learnings as depth, not always-on context.

If the learnings files are absent on this layer, skip this rule.

Before modifying code in an area:

1. Read `.genai/learnings-index.md` if it exists.
2. Match the relevant domain or two.
3. Open only those section(s) in `.genai/learnings.md` when that file exists.
4. Read the whole file only when the work is truly cross-cutting or you are reorganizing learnings.

This keeps the retrieval cost low while still preserving the project's hard-won gotchas.

When you discover something the next agent needs to know — a non-obvious constraint, a thing you tried that didn't work, a pattern that must be preserved — append it to the matching section in `.genai/learnings.md` when that file exists on this layer. If needed, tighten the wording in `.genai/learnings-index.md` so future agents can find that section faster.

Keep entries concise (1-2 sentences) with enough context to prevent the mistake. If the `/handoff` command exists on this layer, it should prompt for learnings to append. You can also append directly during a session when you hit a gotcha.
