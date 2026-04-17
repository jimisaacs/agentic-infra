# Development Guide

How to develop in this repo. The control plane (`./dev`) is the single interface for all development operations.

## Prerequisites

- **Required:** Python 3, Git, and Docker. These are what `./dev verify` and `./dev stack` need.
- **For host-native development:** Go and Node.js/npm. Optional -- useful for `./dev stack dev` (Go server + Vite watch build on host) but never required for verification.

Run `./dev doctor` to check what's available.

## First-Time Setup

```bash
git clone <repo-url>
cd <repo>
./dev doctor        # check prerequisites
./dev setup         # install the clone-local pre-commit hook
./dev verify        # confirm the baseline passes
```

## Quality Gate

```bash
./dev verify        # full verification: paths, syntax, tests, links, docs, format
./dev fmt           # normalize trailing whitespace and EOF newlines
./dev fmt --check   # report drift without fixing
```

`./dev verify` is the single command that tells you whether the work is shippable. Run it before calling any work done. The pre-commit hook runs it automatically if you've installed it via `./dev setup`.

Verification uses Docker to build the web app inside a container. No local Node.js or npm needed -- the container handles dependencies and compilation.

## Running the Worked-Example App

### Container stack (Docker required)

```bash
./dev stack up         # build and start (dev mode: file watcher rebuilds on change)
./dev stack up --prod  # build and start (prod mode: one-shot build, no watcher)
./dev stack status     # check running containers
./dev stack logs       # stream container logs (Ctrl-C to stop)
./dev stack down       # stop the stack
./dev stack reset      # remove all containers, images, and volumes
```

After `./dev stack up`, the app is available at **http://localhost:3000** (nginx serves the UI and proxies `/api/` to the internal API).

### Host-native development (Go + Node required)

```bash
./dev stack dev     # start Go server + Vite watch build
```

This builds the web assets, starts a file watcher for rebuilds, and runs the Go server on port 8080 serving both the API and the UI. Edit `project/web/src/` and refresh the browser to see changes.

## Worktrees

Use `git worktree` when you want isolated editing or execution without turning one checkout into a branch-hopping workspace.

Worktrees are optional tools, not the default model. Most development happens in the main checkout. The Docker stack maps port 3000 to the host; host-native development (`./dev stack dev`) uses port 8080. If you run stacks in multiple worktrees simultaneously, you'll need to adjust ports via Compose overrides.

## What Not to Do

- **Don't skip verification.** If you run multiple worktrees, verify each one independently.
- **Don't skip verification.** `./dev verify` is the trust boundary. Work that doesn't pass it isn't done.
- **Don't modify generated files by hand.** If a file is generated (build output, lock files from a tool), regenerate it through the proper command.
- **Don't scatter scripts.** If a development operation isn't reachable through `./dev`, it should be. Add it to the control plane rather than creating a separate script.
