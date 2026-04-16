# Delivery

**This rule governs all agent output.** When other rules (regression-gate, commands, skills) prescribe thoroughness, that thoroughness is *internal work* — the response to the user stays governed by this rule.

## Finish what you start

Don't leave partial work with caveats. If a change needs 3 files updated, update all 3. If you discover something broken while working, fix it or explicitly don't — never "note: this might need attention."

## Open items block

If you genuinely can't finish something (blocked on user input, outside scope), put it in one block at the very bottom:

```
**Open items**
- [ ] [thing] — [why it's open, what's needed]
```

No block = no loose ends. No "everything looks good!" filler.

## Say less

- Don't narrate what you're about to do, then do it, then summarize what you did. Just do it.
- Don't explain obvious code changes.
- Don't pad with context the user already knows.
- One sentence where one sentence works. Nothing where nothing is needed.

**Hard rule:** if your response is longer than ~15 lines of prose (excluding code blocks and tool output), you are probably saying too much. Cut.

## Exhaustive output only on request

Commands like `/todos`, `/impact`, `/handoff` may produce longer structured output — that's their job. But the *default* for coding turns, polish passes, and general chat is short. When in doubt, shorter.
