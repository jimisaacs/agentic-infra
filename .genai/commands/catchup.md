# Catch up

When you're a new agent dropping into an ongoing project, or the user says "catch up", "what just happened", or "swarm the latest" — build a comprehensive understanding of the most recent changes from multiple angles simultaneously.

## Scope

**Commit-scoped, not session-scoped.** This command always looks at the latest commit(s) — it's for catching up, not reviewing your own work. When the prompt narrows scope (e.g., "swarm the latest server changes"), filter the analysis to that subset.

**Scale cap:** If `git diff HEAD~1 --name-only` lists >20 files, don't read all of them. Use `git diff --stat HEAD~1` to identify the top 10 highest-churn files and focus explores on those. Mention skipped files in the brief.

## How to run it

1. **Establish temporal context:**

```bash
date -Iseconds
git log -10 --format='%h %aI %s'
git show --stat HEAD
git diff HEAD~1 --name-only
```

Use `--format='%h %aI %s'` to include ISO 8601 author dates — this tells agents *when* each commit landed, not just what changed. Compare the oldest relevant commit's date to now to determine the gap width.

2. **Launch 4 parallel agents** to analyze the latest commit from different perspectives:

```
Task(subagent_type="explore", prompt="Read the latest commit. What server/backend code changed? Read every modified file in that layer and summarize: what was added, what was refactored, what was removed. Focus on behavior changes, not formatting. Files: [list backend files from diff]")

Task(subagent_type="explore", prompt="Read the latest commit. What client/UI code changed? Read every modified file in that layer and summarize: new components, state/store changes, type changes, API client or event wiring. Files: [list client files from diff]")

Task(subagent_type="explore", prompt="Read the latest commit. What infrastructure changed? Check rules, skills, commands, agents, hooks, CI config, and project docs. Summarize what's new or different for agents working in this project. Files: [list .cursor/, .github/, docs/, infra-related files from diff]")

Task(subagent_type="explore", prompt="Read the latest commit. Are there any regressions, incomplete work, or TODOs left behind? Check for: stale mocks or test doubles, missing paired handlers where the architecture expects symmetry, client types out of sync with server models, broken links in docs. Files: [list all files from diff]")
```

3. **Synthesize** into a session brief:

```markdown
## Temporal context
- **Current time:** [ISO 8601 from `date -Iseconds`]
- **Last commit:** [SHA + date + summary]
- **Gap since last commit:** [human-readable duration, e.g. "14 hours", "3 days"]
- **Commits in window:** [count]

## What just happened
[1-3 sentence summary]

## Server / backend changes
[Bullet list of behavior changes]

## Client / UI changes
[Bullet list of UI and client-integration changes]

## Infrastructure changes
[What's new for agents — rules, commands, skills, CI]

## Open items
[Anything incomplete, risky, or needing follow-up]
```

4. **Present the brief to the user** or use it as your own context to continue working.

## When to use

- At the start of a new session when the user says "catch up" or "what's the latest"
- When the user says "swarm the latest" or "swarm latest context"
- When another agent just made changes and you need to understand them before continuing
- After a big commit to get the lay of the land
