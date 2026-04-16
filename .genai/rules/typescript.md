# TypeScript / React

React SPA under `project/web/`. Vite build, strict TypeScript, functional components.

## Conventions

- Functional components only, React hooks for state and effects
- Shared interfaces in a dedicated types file -- type names match Go structs
- `fetch()` for API calls -- no HTTP client libraries
- Plain CSS -- no CSS frameworks or modules
- 2-space indent per `.editorconfig`
- Strict TypeScript (`strict: true`)

## Structure

Source under `project/web/src/`. Flat: root component, entry point, types file, components directory. The nginx proxy in `project/stack/` routes `/api/` to the Go server -- use relative paths, don't hardcode API URLs.

## Running

Builds inside Docker. No local Node.js required for `./dev verify`. See `stack` rule for container architecture.

## Anti-patterns

- Don't add state management libraries without an ADR
- Don't add third-party UI component libraries
- Don't scatter type definitions across files
- Don't hardcode API URLs
