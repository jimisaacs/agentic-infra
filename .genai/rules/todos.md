# Code TODO Conventions

## Taxonomy

| Marker | When to use | Example |
|--------|-------------|---------|
| `TODO(milestone):` | Work planned for a specific milestone | `TODO(milestone): v2 clipboard feature` |
| `TODO(wire):` | Scaffolded, waiting for another endpoint or feature to land | `TODO(wire): use when /api/accounts endpoint lands` |
| `TODO(cleanup):` | Tech debt, dead code, rough edges — not blocking anything | `TODO(cleanup): extract retry logic into helper` |
| `TODO(general):` | Uncategorized or one-off | `TODO(general): ctx is unused here` |
| `FIXME:` | Broken or incorrect behavior that needs fixing before ship | `FIXME: race condition on concurrent refreshes` |
| `ACCEPTED_RISK(severity/category):` | Known risk, intentionally not addressed — documents the decision | `ACCEPTED_RISK(low/crypto): using nil AAD` |

## Format

```
// TODO(category): <one-line description>
```

- Always a single-line comment. If you need more, write a doc comment or link to a design doc.
- Category is optional but preferred — it makes scanning and filtering useful.
- `ACCEPTED_RISK` uses `severity/category` where severity is `low`, `medium`, or `high`.
- Never `TODO` something you can fix right now. TODOs mark genuine future work or intentional deferral.

## Lifecycle

1. **Add** a TODO when you scaffold something that can't be completed yet, or when you spot future work during a session.
2. **Categorize** — pick the most specific marker. `TODO(wire):` beats `TODO:` when you know what it's waiting for.
3. **Resolve** — delete the comment when the work is done. Don't leave stale TODOs.
4. **Scan** — use `/todos` to audit. Before a milestone, filter by that milestone to see what's outstanding.

## Anti-patterns

- Don't use TODOs as a substitute for issue tracking — they're breadcrumbs, not tickets.
- Don't write `TODO: fix this` — say what needs fixing and why it can't be fixed now.
- Don't leave `FIXME:` comments in merged code without a plan to address them.
