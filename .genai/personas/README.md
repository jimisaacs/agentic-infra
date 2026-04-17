---
id: persona-index
type: persona-index
audience: [agents, humans]
---

# Persona Catalog

> Curated index for catalog-driven review personas and reserved swarm voices.

Use this directory as a progressive-disclosure entrypoint. Start here, then load only the next cheapest file you need.

This layer is optional for downstream teams. It exists here because the template doubles as a richer reference model, not because every adopting project needs themed review delivery.

## Read Path

1. [`catalog.md`](catalog.md) - compact canonical roster metadata.
2. [`roles.md`](roles.md) - routing rules, affinities, and slot-machine behavior.
3. [`records/<id>.md`](records/) - the chosen persona's depth record.
4. [`quickref.md`](quickref.md) - shallow fallback for direct launches or tight context windows.

## Core Files

- [`catalog.md`](catalog.md): canonical table of persona ids, scopes, tags, and record paths.
- [`roles.md`](roles.md): role-to-persona affinity rules, uniqueness constraints, and prompt-capsule contract.
- [`quickref.md`](quickref.md): derived fallback cache for review agents launched without explicit assignment.

`persona capsule` means the minimal injected fields (`id`, `name`, `voice`, `strengths`, `avoid`, `signoff_style`) rather than the full persona record.

## Review Personas

- [`raphael`](records/raphael.md): aggressive thoroughness and zero patience for sloppy follow-through.
- [`splinter`](records/splinter.md): calm architectural wisdom and principled critique.
- [`michelangelo`](records/michelangelo.md): upbeat delivery with real sharpness underneath.
- [`velma`](records/velma.md): evidence-first sleuthing and contradiction hunting.
- [`donatello`](records/donatello.md): systems-brain engineering and design-constraint rigor.
- [`egon`](records/egon.md): deadpan science, risk isolation, and precise technical diagnosis.
- [`shaggy`](records/shaggy.md): nervous discovery, good for first-day confusion and hidden gotchas.
- [`inspector-gadget`](records/inspector-gadget.md): propagation checking through exhaustive stumble-and-find passes.
- [`penny`](records/penny.md): methodical correctness and quiet competence.
- [`krang`](records/krang.md): theatrical flaw-hunting without sacrificing accuracy.
- [`dick-dastardly`](records/dick-dastardly.md): scheming adversarial energy for devious failure modes.
- [`slimer`](records/slimer.md): chaotic enthusiasm for onboarding and docs delight.

## Reserved Personas

- [`leo`](records/leo.md): reserved for PM and roadmap contexts.
- [`donnie`](records/donnie.md): reserved for engineering lead contexts.
- [`shredder`](records/shredder.md): reserved adversary persona for `/challenge` and similar contrarian flows.

## Optional

- For the role/stage/authority roster model that sits above personas, see [`.genai/swarm-roster/README.md`](../swarm-roster/README.md).
- Do not inject this whole directory into a prompt. Read the index, then the routing rules, then only the selected record.
- Treat `quickref.md` as a cache. `catalog.md`, `roles.md`, and the individual records are authoritative.
