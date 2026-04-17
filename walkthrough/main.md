# Walkthrough: The Human Baseline

You're on `main`. This is where every project starts -- a well-organized human project before any AI tooling enters the picture.

## What you're looking at

A working multi-ecosystem app ("Pulse") with a Go backend, a React frontend, Docker Compose wiring, and a Python control plane that ties it all together. No editor plugins, no agent rules, no AI infrastructure. Just a clean project that a human can clone, verify, and run.

## Where to start

Run `./dev help`. This is the single control plane -- every operation goes through it. If something isn't reachable from `./dev`, it doesn't exist yet.

Then run `./dev doctor`. It tells you what's installed and what's missing.

## The control plane

Open the `dev` script. It's a single Python file that handles:

- **Verification** (`./dev verify`) -- path checks, syntax, tests, markdown links, doc contracts, format drift, and a Docker-based web build. One command, pass/fail.
- **Formatting** (`./dev fmt`) -- trailing whitespace and EOF normalization. Simple and predictable.
- **Stack lifecycle** (`./dev stack up/down/logs/status`) -- Docker Compose wrappers that build and run the worked-example app.
- **Status** (`./dev status`) -- what's present, what's running, what's missing.

Notice what it does with the terminal: color and Unicode are gated behind `NO_COLOR`, `CLICOLOR_FORCE`, `TERM`, and `isatty()`. Signals are handled. Child processes are tracked and cleaned up. This isn't a throwaway script -- it's the contract.

## The principles

Open `docs/PRINCIPLES.md`. These 18 principles are the documented bar for the repo. The worked-example app doesn't instantiate every one end-to-end, but the principles govern how the repo grows. "Containerized stacks" is why `./dev verify` uses Docker. "Control plane is the contract" is why everything routes through `./dev`. "Self-documenting" is why you're reading this file.

Then open `docs/CONVENTIONS.md`. This is how code is written: naming, error handling, API patterns, dependency direction, testing approach. The `.editorconfig` at the repo root encodes the formatting subset that editors can enforce automatically.

## The worked-example app

Open `project/README.md`. The layout is ecosystem/target:

- `project/go/shared/` -- a health-check library
- `project/go/app/` -- an HTTP server that uses it
- `project/go/cli/` -- a CLI that uses it
- `project/web/` -- a React SPA that calls the server
- `project/stack/` -- Docker Compose + nginx that wires them together

Run `./dev stack up` and visit http://localhost:3000. Enter a URL. You'll see the Pulse app check its health and report status, latency, and errors. The Go server does the checking; the React app renders the results.

Run `./dev stack down` when you're done.

## What to understand before moving on

- The `./dev` control plane is the interface. Contributors don't need tribal knowledge.
- Verification needs Python and Docker. No local Go or Node.js required.
- Principles and conventions are documented, not implied.
- The worked-example app is real -- it builds, runs, and does something useful.

## What comes next

Checkout `stack/1-core`. That branch adds the first agentic layer: rules for AI agents, guardrails, an expanded control plane, and architecture governance. Everything you see on `main` is still there -- the agentic layer builds on top, it doesn't replace.

```bash
git checkout stack/1-core
```
