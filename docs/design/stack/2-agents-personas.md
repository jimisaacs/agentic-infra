# Layer 2: Agents, Personas, and Workflow Commands

## What This Layer Teaches

How to structure multi-agent review systems, persona-driven delivery, and composable workflow commands on top of a core infra baseline.

## Why This Layer Exists

The core layer gives agents rules and guardrails. This layer gives them **roles, voice, and orchestration**. The separation matters because:

- Review agents with defined roles (architecture, security, migration, evidence) catch different classes of issues than a single general-purpose agent.
- Personas make review output memorable and distinctive without changing what gets reviewed or how strictly.
- Workflow commands (`/swarm`, `/review`, `/challenge`, `/tighten`) give users composable entry points instead of requiring them to write detailed prompts every time.
- The swarm roster model separates **authority** (who can approve what) from **delivery** (how the feedback sounds).

## Talking Points

### Agents as role definitions, not code

The `.cursor/agents/` directory contains 7 markdown files, not Python scripts. Each one defines a reviewer's scope, what it looks for, and what it reports. The agent runtime is the editor (Cursor) -- the definitions are prompts, not programs. This makes them easy to audit, customize, and version-control.

### The persona separation principle

Personas (`.genai/personas/`) are strictly optional delivery wrappers. A persona changes how feedback is phrased -- not what gets reviewed, not what severity means, not what evidence is required. This is an intentional design constraint: persona delivery never overrides reviewer role, authority, evidence requirements, or safety rules.

### Swarm roster: authority vs delivery

The swarm roster (`.genai/swarm-roster/`) defines the role model that orchestrators use to select, compose, and scale review agents. It separates:

- **Role**: what the agent reviews (architecture, security, etc.)
- **Stage**: when it runs in a pipeline (review, fix, verify)
- **Authority**: what it can approve or block
- **Trigger**: what change signals activate it

### Commands as composable workflows

The 22 slash commands in `.cursor/commands/` are not just shortcuts -- they're compositional workflow building blocks. `/swarm` decomposes multi-intent prompts into pipelines. `/review` runs the review kernel. `/challenge` stress-tests assumptions. These compose: `/swarm fix and challenge` runs a review, fixes findings, then launches an adversarial challenge.

## What's In This Layer

| Path | Purpose |
|------|---------|
| `.cursor/agents/` | 7 reviewer definitions: architecture, security, migration, evidence, performance, reliability, onboarding |
| `.cursor/commands/` | 22 workflow commands including swarm, review, challenge, tighten, debug, handoff |
| `.genai/swarm-roster/` | Role model (model.md), default roster (defaults.md), index (README.md) |
| `.genai/personas/` | Catalog, role affinities, quickref, 15 persona records |
| `.cursor/skills/template-maintenance/` | Template maintenance skill doc |
| `.cursor/active-areas.md` | Parallel-work visibility file |
| `.genai/learnings-index.md`, `.genai/learnings.md` | Accumulated learnings index and log |

## What's Deliberately Missing

- **MCP server** (`scripts/project_context/`) -- added in layer 3
- **Persistent storage** (LanceDB) -- added in layer 4
- **Vector search** (embeddings) -- added in layer 5

## Try This Layer

```bash
git checkout stack/2-agents-personas
./dev help
./dev verify
```

## Questions This Layer Should Answer

1. How do you structure review agents so they complement rather than duplicate each other?
2. What's the right boundary between agent authority (role) and agent personality (persona)?
3. How do workflow commands compose into multi-phase pipelines?
4. When should you add a specialist reviewer vs rely on the core review kernel?
5. How do you scale review intensity based on change risk without manual configuration?
