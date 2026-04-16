# Agent skills (index)

Skills are **on-demand workflow depth** -- invoked explicitly when a task requires deep procedural knowledge. They complement rules, which load automatically based on file context.

**When to use a skill vs rely on rules:**
- An agent editing `project/go/app/main.go` gets the `go` rule automatically (glob-scoped). No skill needed.
- An agent managing Graphite stacks across worktrees invokes the `git` skill for workflow depth beyond what the `cli` and `worktrees` rules define.
- An agent writing a walkthrough invokes the `docs` skill for the authoring pattern and doc hierarchy.

## Available skills

| Skill | Invoke when | What it covers |
| --- | --- | --- |
| `git` | Navigating the teaching stack, using Graphite, coordinating worktrees | Stack model, `gt` workflow, worktree patterns, guard constraints |
| `docs` | Writing or updating docs, walkthroughs, ADRs | Doc hierarchy (map → index → depth), update triggers, walkthrough pattern, decision records |
| `template-maintenance` | Changing the template itself (rules, commands, top-level docs). Available from the agents-personas layer. | Cold-start path, SSOT invariants, `./dev` loop |

## What's handled by rules instead

Language and stack conventions load automatically via glob-scoped rules -- you don't need to invoke a skill:

| Rule | Activates when | File |
| --- | --- | --- |
| `python` | Touching `*.py`, `dev`, `.githooks/*` | `.genai/rules/python.md` |
| `go` | Touching `*.go`, `project/go/**` | `.genai/rules/go.md` |
| `typescript` | Touching `*.ts`, `*.tsx`, `project/web/**` | `.genai/rules/typescript.md` |
| `stack` | Touching `project/stack/**`, `Dockerfile`, `compose.yml` | `.genai/rules/stack.md` |

## Skill chaining

Most tasks need at most one skill. Common patterns:

- **Code change in Go**: just edit -- the `go` rule loads automatically
- **Managing the branch stack**: invoke `git` skill
- **Writing a walkthrough**: invoke `docs` skill
- **Changing the template**: invoke `template-maintenance` (layer 2+)
- **Architecture decision**: invoke `docs` skill → decision records section

See also: **[AGENTS.md](../../AGENTS.md)** for the repo map and **[rules index](../../.cursor/rules/README.md)** for how rules load.
