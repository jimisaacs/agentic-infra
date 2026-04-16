# TypeScript Conventions (Example)

> This is an example language-specific rule. Copy to `.genai/rules/typescript.md` and customize for your project.
> Add a corresponding `.cursor/rules/typescript.mdc` wrapper with `globs: ["**/*.ts", "**/*.tsx"]`.

## State Management

- One store per domain. Select narrowly — don't destructure the whole store.
- Never mutate store state outside store actions.

## API Calls

- Always use your API client — never raw `fetch()`.
- Error handling: use a typed error helper — never `(e as Error).message`.

## Component Patterns

```tsx
const handleAction = async () => {
  try {
    await api<ResponseType>('/endpoint', { method: 'POST', body: JSON.stringify({}) });
    toast('Done', 'success');
  } catch (e: unknown) {
    toast(toError(e).message, 'error');
  }
};
```

## IO Boundaries

Anywhere untyped data enters the system — HTTP responses, WebSocket events, localStorage, URL params — is a type boundary. Untyped data enters, typed data leaves.

- Define a type for every IO shape.
- Nothing typed `any` should leak past an IO boundary into application code.

## Type Discrimination

Prefer narrowing over workarounds. Never use `as` casts or `any` to sidestep union types.

## Anti-Patterns

- Don't use `dangerouslySetInnerHTML`.
- Don't call `fetch()` directly — use your API client.
- Don't hardcode magic strings — use typed constants.
