# Walkthrough: Agents, Personas, and Workflow Commands

You're on `stack/2-agents-personas`. The rules and guardrails from layer 1 are in place. This layer adds the agents that use them.

## What changed

Open `.cursor/agents/`. There are 7 markdown files -- not Python scripts, not config files. Each one defines a reviewer's scope, focus, and reporting style. These are prompts that the editor runtime loads, not programs you execute.

Open `.genai/personas/`. This is the delivery layer. A persona changes how feedback sounds -- not what gets reviewed or what severity means. Open any record in `records/` and compare it to the agent definition it maps to. The separation is intentional: authority lives in the agent role, personality lives in the persona.

## The swarm model

Open `.genai/swarm-roster/README.md`. The roster separates role (what to review), stage (when to run), authority (what to approve), and trigger (what change activates it). This lets an orchestrator compose review pipelines from parts rather than hardcoding them.

## Workflow commands

Open `.cursor/commands/`. There are 22 slash commands. These aren't shortcuts -- they're composable workflow building blocks. `/swarm` decomposes multi-intent prompts into pipelines. `/review` runs the core review. `/challenge` stress-tests assumptions.

The teaching point: commands compose. `/swarm fix and challenge` runs a review, applies fixes, then launches an adversarial challenge pass. Each command is a markdown file that describes a workflow, not code that implements one.

## What to understand before moving on

- Agents are role definitions, not code. The editor is the runtime.
- Personas are optional delivery wrappers. They never override authority or evidence requirements.
- The swarm roster separates concerns that are usually tangled: who reviews, when they run, and what they can approve.
- Workflow commands are composable. Complex workflows emerge from simple parts.

## What comes next

Checkout `stack/3-mcp`. That branch adds a docs-first MCP server -- the project's own context surface for agents, backed by an in-memory store.

```bash
git checkout stack/3-mcp
```
