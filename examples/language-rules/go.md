# Go Server Conventions (Example)

> This is an example language-specific rule. Copy to `.genai/rules/go.md` and customize for your project.
> Add a corresponding `.cursor/rules/go.mdc` wrapper with `globs: ["**/*.go"]`.

## Idiomatic Go

### Naming

- Unexported by default — only export what the package contract requires.
- Avoid stutter: `transport.TransportServer` → `transport.Server`.
- No `Get` prefix on getters (`Name()` not `GetName()`).
- Short receiver names, consistent across methods.

### Design

- Accept interfaces, return structs.
- Make the zero value useful.
- Don't panic in library code — return errors.
- Avoid premature abstraction.

### Context & Goroutines

- `context.Context` is always the first parameter, never stored in a struct.
- Goroutine ownership: whoever starts it is responsible for stopping it.

## Formatting & Types

- `gofmt` + tabs. `any` not `interface{}`.
- Typed constants for enums.
- JSON responses: `snake_case`.

## Error Handling

- Define sentinel errors in your core package.
- Never return raw repo errors to callers — wrap with `fmt.Errorf("context: %w", err)`.

## Testing

- stdlib `testing` — hand-rolled mocks or your preferred mock library.
- Integration tests: require env var, skip if unset.

## Anti-Patterns

- Don't skip mocks for new interface methods.
- Don't put domain methods in the wrong file.
- Don't assume existing mocks are complete.
