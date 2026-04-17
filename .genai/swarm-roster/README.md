---
id: swarm-roster-index
type: roster-index
audience: [agents, humans]
---

# Swarm Roster

> Progressive-disclosure entrypoint for the universal swarm-roster model and this repo's default implementation.

Use this directory to answer three questions in order:

1. What are the canonical roster dimensions and contracts?
2. What is the universal best-in-class default roster for a software engineering repo?
3. How does this repo map that universal model onto its current `/swarm` behavior?

## Read Path

1. [`model.md`](model.md) - canonical dimensions, authority levels, scope values, and role contract schema.
2. [`defaults.md`](defaults.md) - universal default roster kernel, specialist overlays, and this repo's current mapping.
3. Relevant reviewer spec under [`.cursor/agents/`](../../.cursor/agents/) - role-specific checklist, prompt contract, and output format.
4. [`.genai/personas/README.md`](../personas/README.md) - delivery voices and persona-routing system.

## Core Files

- [`model.md`](model.md): source of truth for roster terminology and the six design dimensions.
- [`defaults.md`](defaults.md): source of truth for the universal default roster and repo-specific role mapping.
- [`.genai/commands/swarm.md`](../commands/swarm.md): orchestrator behavior that selects roles, stages, and persona capsules.
- [`.genai/personas/roles.md`](../personas/roles.md): routing rules for persona assignment after role selection.

## Invariants

1. `role`, `persona`, `stage`, `authority`, `trigger`, and `scope` stay separate concepts.
2. The default roster is a small assurance kernel, not a giant fixed cast.
3. Specialist roles join by trigger, not by habit.
4. Reserved flows like `challenge` are not reviewer roles.
5. Workflow stages like `polish`, `regress-check`, `verify`, and `handoff` are not personas.
6. Commands should read only the roster material they actually need.

## Notes

- `roster` is broader than `reviewers`. Not everyone in the roster must be a reviewer.
- The persona catalog is orthogonal. It decides delivery voice after the orchestrator chooses a role.
- This directory describes the portable model. Role-specific review mechanics still live in the agent specs.
