# ADR template

## Blank template

Copy the front matter and sections below into `ADR-xxxx-short-slug.md`.

```markdown
---
id: ADR-xxxx
status: accepted
date: YYYY-MM-DD
tags: []
decision: One-line decision statement
supersedes: []
superseded_by: []
---

# ADR-xxxx Short title

## Decision statement

## Context

## Decision

## Alternatives considered

## Consequences

## Review signals

## Links

```

---

Section expectations:

- `Context` captures the operating range, relevant constraints, and non-goals that make the decision necessary now.
- `Decision` states what is chosen and the scope it covers.
- `Alternatives considered` compares like-for-like options and includes the status quo when it is still a real option.
- `Consequences` records tradeoffs, confidence, and near-term costs.
- `Review signals` names what would make the ADR worth reopening.

## Canonical example (generic)

The following is a complete, minimal ADR illustrating the expected shape and tone.

---

```markdown
---
id: ADR-0001
status: accepted
date: 2026-04-14
tags: [storage, persistence]
decision: Use PostgreSQL as the primary data store
supersedes: []
superseded_by: []
---

# ADR-0001 Use PostgreSQL as the primary data store

## Decision statement

Use PostgreSQL as the system of record for relational data: users, domain entities, and transactional workflows.

## Context

- Need ACID semantics and expressive querying for core business data.
- Current operating range is one regional deployment, moderate write volume, and a small ops surface that can support one primary with read replicas as a future option.
- Non-goals for this decision: offline-first sync and high-write append-only analytics storage.
- Team has operational experience with Postgres and standard backup/replication tooling.

## Decision

Standardize on PostgreSQL for the primary application database. Use migrations for schema changes; access data through the repository layer (or equivalent), not ad hoc SQL from application features. This ADR covers the system-of-record choice, not analytics or cache stores.

## Alternatives considered

- **Stay on SQLite longer:** simplest operationally for small installs; rejected because expected multi-tenant concurrency and online migration pressure exceed its comfortable operating range for this system.
- **MySQL / MariaDB:** viable relational option; not selected because the team's operating experience and surrounding tooling are stronger around Postgres.
- **Document-first store (e.g. MongoDB):** flexible schema but weaker fit for relational integrity and transactional workflows in this domain.

## Consequences

- Accept operational focus on backups, replication, and connection pooling.
- Schema changes require migration discipline and compatibility strategies for rolling deploys.
- Local and CI environments should run Postgres (or a compatible test double) to avoid drift.
- Confidence is medium-high for the current workload; multi-region writes remain an unresolved future constraint.

## Review signals

- Revisit if sustained write volume or regional topology exceeds a single primary with replicas.
- Revisit if domain requirements shift toward mostly document or append-only access patterns.
- Revisit if operating burden outweighs the relational benefits for the team.

## Links

- Status doc (operational readiness)
- Protocol doc (API contracts if applicable)
- Benchmark or spike notes that informed the choice
```
