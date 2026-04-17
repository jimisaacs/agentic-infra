---
id: swarm-roster-defaults
type: roster-defaults
source_of_truth: true
---

# Swarm Roster Defaults

## Universal Default Roster

For a generic software engineering repo, the best default is a small assurance kernel rather than a large fixed cast.

### Core Reviewers

| Role | Why it belongs in the kernel |
|---|---|
| `architecture-reviewer` | Guards invariants, boundaries, dependency direction, and scaling traps |
| `security-reviewer` | Covers trust boundaries, auth, isolation, tokens, and misuse paths |
| `evidence-reviewer` or `correctness-reviewer` | Checks whether behavior is actually proven by tests, fixtures, mocks, and negative cases |
| `propagation-checker` or `integration-reviewer` | Catches schema drift, stale clients, rename fallout, and cross-component mismatch |

### Specialist Roles

| Role | Trigger examples |
|---|---|
| `performance-reviewer` | latency claims, throughput claims, rendering hot paths, allocation-sensitive changes |
| `reliability-reviewer` | rollout safety, retries, queues, observability, alerting, incident-sensitive behavior |
| `onboarding-reviewer` or `docs-reviewer` | docs, rules, setup, templates, handoff surfaces |
| Repo-specific overlays | `api-contract`, `data-schema`, `ui-accessibility`, `mobile-native`, `privacy`, `build-tooling` |

### Reserved Flows And Stages

| Kind | Name | Role in the system |
|---|---|---|
| Reserved flow | `challenge` | adversarial pressure test after initial synthesis |
| Workflow stage | `polish` | hygiene cleanup and low-level consistency |
| Workflow stage | `regress-check` | downstream breakage scan after edits settle |
| Workflow stage | `verify` | gatekeeper checks for tests, lint, typecheck, build |
| Workflow stage | `handoff` | final summary for humans or follow-on agents |

`regress-check` is the stage name; this repo exposes it through the `/regressions` command.

## This Repo's Current Mapping

This repo now maps the universal model onto the following role set:

| Role | Class | Authority | Entry stage | Default scope | Default triggers | Status |
|---|---|---|---|---|---|---|
| `architecture-reviewer` | `core-reviewer` | `report-only` | `review` | `component`, `system`, `plan` | invariants, layering, persistence, shared types | active |
| `security-reviewer` | `core-reviewer` | `report-only` | `review` | `file`, `component`, `system`, `plan` | auth, identity, tokens, trust boundaries | active |
| `migration-checker` | `core-reviewer` | `report-only` | `review` | `file`, `component`, `system`, `plan` | schema changes, renames, config drift, generated types | active repo-specific propagation role |
| `evidence-reviewer` | `core-reviewer` | `report-only` | `review` | `file`, `component`, `system`, `plan` | tests, fixtures, mocks, regression proof, missing verification | active |
| `performance-reviewer` | `specialist-reviewer` | `report-only` | `review` | `file`, `component`, `system`, `plan` | latency, throughput, rendering, benchmark claims | available specialist |
| `reliability-reviewer` | `specialist-reviewer` | `report-only` | `review` | `component`, `system`, `plan`, `incident` | rollout safety, retries, observability, incident surfaces | available specialist |
| `onboarding-reviewer` | `specialist-reviewer` | `report-only` | `review` | `file`, `component`, `system` | docs, rules, setup, navigation, handoff surfaces | active specialist |
| `challenge` | `reserved-flow` | `report-only` | `challenge` | `plan`, `system` | explicit adversarial pressure, "what am I missing?" | active reserved flow |
| `polish` | `workflow-stage` | `fix-capable` | `polish` | `file`, `component` | hygiene, naming, import cleanup, dead code | active stage |
| `regress-check` | `workflow-stage` | `report-only` | `regress-check` | `component`, `system` | downstream breakage concern | active stage |
| `verify` | `workflow-stage` | `gatekeeper` | `verify` | `component`, `system` | checks, tests, lint, typecheck, build | active stage |
| `handoff` | `workflow-stage` | `report-only` | `handoff` | `system`, `plan` | final summarization or transfer | active stage |

## Practical Default

For ordinary code changes in this repo:

1. Start with the core kernel: `architecture-reviewer`, `security-reviewer`, `migration-checker`, `evidence-reviewer`.
2. Add specialists by trigger: `performance-reviewer`, `reliability-reviewer`, `onboarding-reviewer`.
3. Run `challenge` only when the user asks for adversarial pressure or the work is strategically important enough to justify it.
4. Finish with `polish`, `regress-check`, `verify`, and `handoff` as stages instead of treating them as more reviewer personas.
