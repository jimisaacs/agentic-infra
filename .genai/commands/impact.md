# Impact analysis

Before making a change, understand its blast radius. Launch parallel explorers to map every downstream dependency.

## Scope

**Prompt-driven.** The proposed change comes from the surrounding prompt. When used as a verb (e.g., "impact of adding a field to User" or "what would renaming `tenant_id` impact?"), extract the change from that context.

## How to run it

Given a proposed change (from prompt context or explicit description):

1. **Launch 4 parallel explore agents**, each scoped to a different layer:

```
Task(subagent_type="explore", prompt="Search the server/backend tree for usages of [thing]. Return a table: file | usage type | must update? | risk if missed. Focus on direct uses and type references — skip comments.")

Task(subagent_type="explore", prompt="Search the client/web/UI tree for usages of [thing]. Return a table: file | usage type | must update? | risk if missed.")

Task(subagent_type="explore", prompt="Search docs/, schema/, .cursor/ for mentions of [thing]. Return a table: file | must update? | risk if missed.")

Task(subagent_type="explore", prompt="Search mobile/native app directories for usages of [thing]. Return a table: file | usage type | must update? | risk if missed. If the project has no native apps, report 'not applicable' with confirmation from the repo layout.")
```

2. **Consolidate** into an impact map:

| Layer | File | Usage type | Must update? | Risk if missed |
|-------|------|-----------|-------------|----------------|

3. **Flag high-risk items**: interface changes that break mocks, DTO renames that break clients, event or topic changes that break subscribers.

4. Present the impact map to the user **before** making the change. Let them decide scope.

## When to use

- Before renaming anything (fields, topics, files, types)
- Before changing an interface (adding/removing methods)
- Before changing a DTO shape (adding/removing/renaming fields)
- Before changing external contracts (APIs, events, permissions)
- When the user says "what would this affect?" or "what's the blast radius?"

## When to scale down

For changes scoped to a single file with no interface/DTO changes, a single explore agent is sufficient — skip the 4-layer fan-out.
