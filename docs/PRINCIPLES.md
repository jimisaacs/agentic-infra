# Principles

Engineering principles that guide how this project is built and evolved. Product-agnostic -- these apply regardless of the domain the downstream project serves.

## Core

1. **Isolation by default.** Data and concerns are scoped. Sharing is explicit, never ambient. If two things don't need to see each other, they shouldn't be able to.

2. **Local-first.** Data lives on disk, under your control. External services receive only what they need for the current operation -- never a standing copy of your state.

3. **Clear platform boundaries.** Each runtime owns a clear domain. Server-side owns reasoning and data. Client-side owns observation and action. Don't blur the line -- it makes both sides harder to reason about and harder to secure.

4. **Heuristics before inference.** Don't call an LLM or any expensive service for what deterministic rules can decide. Rules are fast, predictable, and auditable. Inference is for the problems rules can't solve.

5. **Earned trust.** Start cautious. Promote to autonomous after proven reliability. This applies to code, to agents, and to new capabilities. Trust is graduated, not granted.

6. **Discretion.** Know when NOT to act. Silence is a valid response. The system that acts on everything is more dangerous than the system that acts on nothing.

7. **Auditable.** Every mutation is logged. If you can't explain what happened and who triggered it, the system failed. Audit trails are not optional infrastructure -- they are the proof that trust is being honored.

8. **Multi-transport.** Data endpoints should work through more than one door when the architecture supports it. If the same operation is reachable via HTTP and message bus, both doors call the same service methods.

9. **Self-documenting.** Update docs when direction changes. Stale docs are worse than no docs -- they actively mislead. The documentation is part of the product, not a side artifact.

10. **Self-hosting development.** Development tooling is a product surface, not disposable infrastructure. The tools that help users should also help developers. Every feature shipped for users makes the dev tooling better. Every dev capability makes the product better. They compound.

11. **Interface-first.** Depend on interfaces, never concrete implementations. Repositories, services, and transport adapters are separated by contract. Swap an implementation without touching callers.

12. **Dependency direction.** Core domain logic never imports infrastructure. Infrastructure adapts to core. If a transport handler or storage adapter needs to change, core should be unaware.

13. **Single control plane.** One CLI entrypoint for verification, formatting, lifecycle, and status. No scattered scripts, no tribal knowledge about which command to run where. `./dev` is the interface.

14. **Containerized stacks.** When the project has a multi-service stack, containers are the default way to run it. Host toolchains are optional for development convenience, never required for verification.

15. **Quality gate.** One command tells you if the work is shippable. The checks it runs depend on the layer: path checks, syntax, tests, doc contracts, formatting, and a Docker-based web build. If you can't run it, you're not done.

16. **Additive layering.** Each layer of capability builds on everything below and adds one concern. No layer removes content from its parent. This applies to stack branches, to architecture, and to features.

17. **Verify-before-ship.** The quality gate is the trust boundary for code. Work that passes verification earns the right to ship. Work that doesn't is not done, no matter how good it looks.

18. **Control plane is the contract.** The `./dev` script is the interface to the project. If a capability isn't reachable through `./dev`, it doesn't exist for new contributors.
