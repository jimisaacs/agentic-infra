# Misdirected Instructions & Wrong Chat

The owner runs multiple agents in parallel. Before modifying files:

1. **Fit check** — Does the ask apply to this repo and *this* session? If it names files or decisions you haven't seen in this thread, stop and ask.
2. **Restate scope** — In 1-3 bullets, state what you believe you're changing. If you can't name concrete files or behaviors, ask.
3. **Conflict check** — Read `.cursor/active-areas.md`. Don't revert or reformat files you didn't touch.
4. **Sensitive areas** — Auth, shared components, infrastructure, and identity-related code need understanding first.

If mid-session the task was misdirected: stop edits, summarize what changed vs what was wanted, offer to revert your session edits only.

**Anti-patterns:** Shipping "something related" when the ask doesn't parse. Treating unrelated git status as yours to fix. Continuing silently after confusion.
