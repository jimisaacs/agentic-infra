# Project Layout

Use this rule when working under `project/`. Repo root owns agent infrastructure and governance; `project/` owns the worked-example product surface.

## Structure

- Default shape: `project/{ecosystem}/{target}/`
- An ecosystem is a runtime, platform, or toolchain boundary.
- A target is a deliverable with its own build, run, or test surface.
- Cross-target shared code lives at `{ecosystem}/shared/`.
- Project-wide contracts, fixtures, or shared schemas live at `project/` root.
- Cross-ecosystem wiring lives under `project/stack/`.

## Navigation

- Start with `project/README.md` for the map.
- Read the narrowest target that matches the task before exploring sibling ecosystems.
- Open `project/stack/` only when the task crosses target boundaries.
- When work crosses back into agent infrastructure, return to the repo-root maps instead of inventing new infra under `project/`.

## Scaffolding

- Prefer extending an existing target when the new work ships through the same runtime and build boundary.
- Add a new target only when the work introduces a distinct executable, deployable, or separately testable surface.
- Add a new ecosystem only when the toolchain or runtime boundary is materially different.
- New runnable targets should include their native entry and build files, plus any wiring needed from `project/README.md`.
- Add `project/stack/` wiring only when the target participates in integrated local runs.

## Drift Control

- Keep `project/README.md` current when ecosystems, targets, or navigation change.
- Do not create ad-hoc top-level directories under `project/`; fit the work into the ecosystem/target model or explicitly revise the model.
- Do not park speculative code here. If a target or ecosystem has no live entrypoint, imports, stack wiring, or roadmap/decision reason to exist, treat it as dead and delete or archive it explicitly.
