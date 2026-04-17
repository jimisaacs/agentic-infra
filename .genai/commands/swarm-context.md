# Swarm context

When you need to understand something deeply before acting — "swarm it to understand", "what's the full picture", "explore this" — launch parallel agents to build a comprehensive understanding from multiple angles.

## Scope

**Prompt-driven.** The topic comes from the surrounding prompt. When used as a verb (e.g., "swarm context on the billing module" or "I need context on how notifications work"), extract the topic from that context.

## How to run it

Given a topic, area, or question (from prompt context or explicit description):

1. **Launch 3 parallel explore agents**, each investigating a different facet (adjust directory names to your repo layout):

```
Task(subagent_type="explore", prompt="How does [topic] work in the server/backend? Read the main service and data layers for implementations, data flow, and entry points. Return a summary with file paths.")

Task(subagent_type="explore", prompt="How does [topic] work in the client/UI? Read components, state, and API/event wiring that touch this. Return a summary with file paths.")

Task(subagent_type="explore", prompt="What do the docs say about [topic]? Read the agent guide, protocol/API docs, status notes, and relevant skills. Are docs consistent with the code? Return a summary of what's documented vs what might be stale.")

```

2. **Synthesize** the parallel findings into a single coherent picture:
   - How it works today (server + client + docs)
   - What the docs say vs what the code does
   - Gaps, inconsistencies, or open questions

3. **Present to the user** as a structured brief — not a wall of text. Use tables, diagrams, or bullet points.

## When to use

- When the user asks "how does X work?" about something that spans multiple components
- When the user says "I need the full picture on X" or "swarm context on X"
- Before planning a feature that touches an area you don't fully understand
- When investigating a bug that could span backend, client, or infrastructure
