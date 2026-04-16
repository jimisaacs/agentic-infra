# Walkthrough: The Agentic Core

You're on `stack/1-core`. Everything from `main` is still here -- the Pulse app, the control plane, the principles. This layer adds the first agentic infrastructure on top.

## What changed

Look at what's new since `main`:

- `AGENTS.md` -- the repo-wide guide that AI agents auto-load. Open it. This is what an agent sees first when it enters the repo.
- `CLAUDE.md` -- the Claude Code entrypoint. Same idea, different editor.
- `.genai/rules/` -- the canonical rule prose. Behavioral rules (CLI policy, delivery style) and language/stack rules (Go, Python, TypeScript, Docker).
- `.cursor/rules/` -- thin wrappers that point Cursor at the `.genai/` rules. The prose lives in one place.
- `.genai/skills/` -- on-demand workflow depth (git, docs). Invoked explicitly, not auto-loaded.
- `.cursor/skills/` -- Cursor wrappers for skills.
- `.claude/hooks/guard.py` -- the shell guard. It enforces a conservative allowlist for commands agents can run. This is trust infrastructure.

## Rules vs skills

Open `.genai/rules/core.md` and `.genai/skills/README.md`. This layer introduces two kinds of agent context:

**Rules** load automatically. Some are always-on (posture, CLI policy). Others activate when the agent touches matching files -- edit a `.go` file and the Go rule loads; touch `project/stack/` and the Docker stack rule loads. The agent doesn't ask for these; they're invisible infrastructure.

**Skills** are on-demand depth. An agent managing the Graphite branch stack invokes the `git` skill. An agent writing a walkthrough invokes the `docs` skill. Skills are for procedural knowledge that doesn't belong in every conversation.

The key insight: rules are infrastructure, not documentation. They're loaded by the editor and shape agent behavior in real time. Skills are expertise you call when you need it.

## The guard

Run `./dev verify` and watch the "Guard behavior" section. It tests that the guard correctly allows controlled git commands and blocks destructive ones. The guard is tested as part of verification -- it's not an afterthought.

## Architecture governance

Open `docs/decisions/README.md`. This layer introduces the ADR/DEC framework: architectural decisions are recorded, not lost in chat. Open `docs/decisions/adr/template.md` to see what a good decision record looks like -- context, alternatives, consequences, and review signals.

## The expanded control plane

`./dev` gained new verification steps: guard behavior checks, JSON syntax, MCP config sanity check (ensures MCP isn't prematurely advertised), and doc contract enforcement. Run `./dev status` to see the expanded view. The control plane grew with the layer -- it verifies what the layer adds.

## What to understand before moving on

- Rules in `.genai/rules/` are the single source of truth. Editor wrappers are pointers, not copies.
- The guard is a trust boundary. It uses a conservative allowlist: read-only git commands plus controlled mutations (add, commit, push, checkout, switch). Destructive operations are blocked.
- Architectural decisions are recorded in `docs/decisions/`, not buried in chat history.
- The control plane verifies a pinned subset of required paths, guard behavior, and doc contracts. Not every file is pinned -- the required-paths list grows with each layer.

## What comes next

Checkout `stack/2-agents-personas`. That branch adds review agents with defined roles, persona-driven delivery, and composable workflow commands. The rules from this layer govern how those agents behave.

```bash
git checkout stack/2-agents-personas
```
