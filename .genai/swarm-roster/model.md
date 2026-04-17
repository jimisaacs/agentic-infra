---
id: swarm-roster-model
type: roster-model
source_of_truth: true
---

# Swarm Roster Model

The universal best-in-class design is not a fixed cast. It is a model with the right separations.

## Canonical Dimensions

| Dimension | Meaning | Typical values |
|---|---|---|
| `role` | What job is being done | `architecture-reviewer`, `security-reviewer`, `evidence-reviewer`, `challenge` |
| `persona` | How that job is delivered | `splinter`, `penny`, `shredder` |
| `stage` | When it runs in the workflow | `review`, `challenge`, `polish`, `verify`, `handoff` |
| `authority` | What it is allowed to do | `report-only`, `fix-capable`, `gatekeeper` |
| `trigger` | What kinds of changes activate it | auth, schema drift, docs changes, latency claims, rollout risk |
| `scope` | The level it operates on | `file`, `component`, `system`, `plan`, `incident` |

These six dimensions should be explicit in any portable swarm-roster design.

## Canonical Vocabulary

- `swarm roster` - the full cast the orchestrator can draw from.
- `core reviewers` - the default assurance kernel for substantive code changes.
- `specialist roles` - optional reviewer lanes activated by trigger.
- `reserved flows` - named adversarial or strategic passes that are not ordinary reviewers.
- `workflow stages` - the pipeline steps that sequence work across roles.
- `persona catalog` - the delivery-layer source of truth used after role selection.
- `persona capsule` - the minimal selected-persona payload injected into a prompt.

## Authority Levels

| Authority | Meaning | Examples |
|---|---|---|
| `report-only` | Inspect and report findings, but do not change files by default | reviewer agents |
| `fix-capable` | Allowed to make changes inside an execution phase | executor agents, direct fix phases |
| `gatekeeper` | Produces a pass/fail decision or exit condition | `verify`, policy checks, release gates |

Authority belongs to the role contract, not to the persona.

## Scope Levels

| Scope | Use when |
|---|---|
| `file` | Focused implementation review or a single changed surface |
| `component` | A bounded subsystem or module changed together |
| `system` | Multiple layers or a cross-cutting behavior changed |
| `plan` | Reviewing proposed work before implementation |
| `incident` | Debugging, rollback, or reliability-sensitive failure handling |

Roles may support multiple scope levels, but they should name them explicitly.

## Role Contract Schema

Every durable role should define the following metadata somewhere stable, ideally in its spec frontmatter:

| Field | Meaning |
|---|---|
| `name` | Stable role identifier |
| `role_class` | `core-reviewer`, `specialist-reviewer`, `reserved-flow`, `workflow-stage`, or `orchestrator` |
| `authority` | `report-only`, `fix-capable`, or `gatekeeper` |
| `entry_stage` | The stage where the role normally enters the pipeline |
| `default_scope` | List of scope levels the role commonly handles |
| `default_triggers` | List of trigger phrases or change kinds that activate the role |
| `exit_artifact` | The expected output from the role |

## Composition Contract

1. The orchestrator selects roles from the swarm roster based on trigger, scope, and risk.
2. The orchestrator assigns stages independently of persona selection.
3. Persona assignment happens after role selection through the persona catalog.
4. Reserved flows like `challenge` attach after the first substantive synthesis pass.
5. Finishers like `polish`, `regress-check`, `verify`, and `handoff` remain stages, not reviewer roles.

## Default Shape

The best default shape is:

1. A small assurance kernel of high-signal reviewers.
2. Specialist roles that plug in by trigger.
3. A reserved adversarial flow for pressure-testing.
4. Finishing stages that converge quality and communicate outcome.
