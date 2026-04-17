# Pulse

`project/` is the worked-example product surface in this repo. Repo root owns the human docs and control plane; this directory owns the example app code and delivery surfaces.

## Read Path

1. Start here for the ecosystem and target map.
2. Open the narrowest `{ecosystem}/{target}/` that matches the task.
3. Open `stack/` only for cross-target wiring such as Docker Compose, reverse proxies, or local integration.
4. Return to the repo-root docs and `./dev` when the task crosses back into repo-level control or maintenance.

## Structure

```text
project/{ecosystem}/{target}/
```

Every directory under `project/` is an **ecosystem** -- a platform, runtime, or toolchain. Each ecosystem contains one or more **targets** -- deliverables with their own build configuration.

| Ecosystem | Targets | Toolchain |
| --------- | ------- | --------- |
| `go/` | `shared/`, `cli/`, `app/` | Go modules |
| `web/` | _(single target)_ | Vite + TypeScript |
| `stack/` | `go/`, `web/` | Docker Compose |

## Navigation

- `go/shared/` owns Go code reused by both the CLI and API targets.
- `go/cli/` owns the command-line deliverable.
- `go/app/` owns the API deliverable.
- `web/` owns the browser UI.
- `stack/` owns cross-ecosystem local wiring.

## Sharing

Shared code follows the same pattern -- it is just another target within its ecosystem:

- **Project-wide** contracts live at this root (e.g. an OpenAPI spec)
- **Ecosystem-wide** shared code lives at `{ecosystem}/shared/` and is imported by sibling targets
- **Target-local** internals stay inside their own target directory

## Adding new work

- Prefer extending an existing target when the new work ships through the same runtime and build boundary.
- Add a new target when the work needs its own build, run, test, or deployment surface.
- Add a new ecosystem when the toolchain or runtime boundary is materially different.
- Update this file whenever ecosystems, targets, or navigation change.

## Retirement

Treat a target or ecosystem as dead when it no longer has a live entrypoint, imports, stack wiring, or a roadmap/decision reason to exist. Delete it or archive it explicitly; do not leave zombie directories in `project/`.

## Quick Start

### Via the control plane (from repo root)

```bash
./dev stack up          # build and start (dev mode: watches for changes)
./dev stack up --prod   # build and start (prod mode: one-shot build)
# Pulse:  http://localhost:3000

./dev stack dev         # host-native: Go server + Vite watch build (requires Go + Node)
# Pulse:  http://localhost:8080

./dev stack down        # stop the Docker stack
./dev stack reset       # remove all containers, images, and volumes
```

### Direct (from `project/`)

```bash
# Go CLI
cd go/cli && go run . check https://example.com

# Go server (API only)
cd go/app && go run .
# http://localhost:8080/api/check?target=https://example.com

# Go server (API + UI)
cd web && npm install && npm run build
cd ../go/app && go run . -static ../../web/dist
# http://localhost:8080
```
