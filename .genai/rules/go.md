# Go

The worked-example Pulse app under `project/go/`. Standard library only, no third-party dependencies.

## Dependency direction

```
shared/    <-- domain logic, imports nothing outside itself
app/       --> imports shared/
cli/       --> imports shared/
```

Domain package never imports transport or infrastructure. If you find the reverse, the dependency is inverted.

## Conventions

- Typed constants with clear prefixes: `StatusUp`, `StatusDown`, `StatusDegraded`
- JSON tags: `snake_case` (`json:"latency_ms"`), `omitempty` for optional fields
- `http.Client` with explicit timeout -- never the default client
- `http.NewServeMux()` with Go 1.22+ method+path routing
- Set `Content-Type: application/json` explicitly before writing responses
- Transport is thin: parse input, call domain, encode result

## Running

Go runs in Docker for verification. No local Go toolchain required for `./dev verify`. See `stack` rule for container architecture.

## Anti-patterns

- Don't import consumer packages from the domain package
- Don't use `http.Get` or the default client
- Don't forget `Content-Type` headers on JSON responses
- Don't put transport logic in the domain package
