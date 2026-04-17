# Conventions

Coding and project conventions. These are the defaults -- override per-ecosystem when the ecosystem has a stronger standard.

## Formatting

Formatting is encoded in `.editorconfig` at the repo root. Editors that respect `.editorconfig` will apply these rules automatically.

| Language | Indent | Width |
|----------|--------|-------|
| Go | tabs | 4 |
| Python | spaces | 4 |
| TypeScript, JavaScript, JSON, HTML, CSS | spaces | 2 |
| YAML | spaces | 2 |
| Markdown | spaces | 2 |

All files use LF line endings, UTF-8 encoding, and a final newline.

`./dev fmt` strips trailing whitespace and normalizes EOF newlines. It does not enforce indentation style -- that is the editor's responsibility via `.editorconfig`. These are complementary: `.editorconfig` governs how you write, `./dev fmt` catches what slipped through.

## Naming

| Context | Convention |
|---------|-----------|
| JSON fields | `snake_case` |
| Go types and functions | Standard Go conventions (`PascalCase` exported, `camelCase` unexported) |
| Go enums | Typed constants with a clear prefix (`StatusUp`, `StatusDown`) |
| URL paths | Kebab-case for multi-word segments (`/login-code`, `/quiet-hours`) |
| File names | Lowercase with hyphens or underscores per ecosystem convention |

## Error Handling

- Use sentinel errors for known conditions (`ErrNotFound`, `ErrForbidden`).
- Wrap errors with context using constructors (`BadRequest("missing field: %s", name)`).
- Never swallow errors silently. If you handle an error, log it or return it.
- Distinguish between client errors (4xx -- the request is wrong) and server errors (5xx -- the system is wrong).

## API Patterns

**Response envelope.** Prefer a consistent response shape for larger services:

```json
{"status": 200, "data": { ... }}
{"status": 400, "error": "missing required field: target"}
```

Small handlers (like the Pulse demo) may return simpler shapes; adopt the envelope when endpoints grow beyond a single resource.

**State transitions use named verbs, not PATCH.** Instead of `PATCH /resource/{id}` with a status field, use `POST /resource/{id}/archive`, `POST /resource/{id}/done`. Each verb is a distinct action with its own auth, audit, and response shape.

**Resource naming.** Plural nouns for collections (`/entries`, `/members`). Singular for singletons (`/config`, `/clearance`). Kebab-case for multi-word resources.

**Destructive operations.** Require a confirmation field in the request body, not a query parameter. This keeps confirmation tokens out of proxy logs and browser history.

## Dependency Direction

Core domain logic lives in one package. It never imports transport, storage, or infrastructure packages. Transport handlers and storage adapters import core. If you find core importing a transport type, the dependency is inverted -- fix it.

```
core/          <-- domain logic, interfaces, types
transport/     --> imports core
storage/       --> imports core
```

## Storage

- Repositories depend on interfaces, never concrete implementations.
- Separate durable storage (databases) from ephemeral storage (caches, KV).
- Compile-time interface checks: `var _ core.MyRepo = (*postgres.MyRepo)(nil)`.
- Migrations are embedded and run at startup. No external migration tool required.

## Testing

- Use the standard library's test framework. No assertion libraries, no mock frameworks.
- Service tests wire all mock repos and test domain logic directly.
- Transport tests use `httptest` and verify the full request/response cycle.
- Mock interfaces live in a test utilities package, not scattered across test files.

## Mutation Side-Effects

Every mutation (create, update, delete) should consider three side-effects:

| Side-effect | Purpose |
|-------------|---------|
| Event publication | Real-time consumers (dashboards, agents) see the change |
| Audit logging | Security trail -- who did what, when, through which door |
| Cache invalidation | Downstream caches regenerate on next access |

Not every mutation needs all three. But consider each explicitly -- missing a side-effect causes silent gaps that are hard to diagnose later.

## Documentation

- Map-level docs (`README.md`, `CONTRIBUTING.md`) stay short and easy to read cold.
- Depth lives behind indexes -- link to it, don't inline it.
- Update docs when direction changes. A doc that describes last month's architecture is actively harmful.
- The control plane (`./dev`) is the executable documentation. If a doc says "run X" and `./dev` doesn't support X, the doc is wrong.
