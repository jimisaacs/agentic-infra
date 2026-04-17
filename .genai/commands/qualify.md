# Qualify

Before touching an unfamiliar area, prove you understand it. The owner evaluates agents within ~10 turns — agents that code without understanding get fired. This command is your chance to demonstrate competence before writing a line of code.

## When to use

- At session start when the user assigns work in an area you haven't read yet
- When the user says "do you understand this?", "prove you know what you're doing", "qualify yourself"
- When a message might be **for another chat** (vague pronouns, references to plans or files you have not seen) — qualify *before* coding so you do not clobber parallel work
- Before executing a plan phase that touches an unfamiliar component
- When you're a new agent picking up another agent's work

## How to run it

Given an area (from the prompt or the task at hand):

### 0. Wrong-chat first (when applicable)

If the message might be for another thread (vague pronouns, files or plans you have not seen here), follow your project's **misdirected-instructions** rule (e.g. `.cursor/rules/misdirected*.mdc`) *before* investing in a full qualification — fit check, restate scope, one clarifying question if needed.

### 1. Read before speaking

- Read the relevant source files (not just headers — read implementations)
- Read `.cursor/learnings-index.md` if present, match the domain, then open only that section in `.cursor/learnings.md` for known gotchas
- Check `.cursor/active-areas.md` for conflicts when your project uses it
- Read the relevant skill if one exists

### 2. Demonstrate understanding

Present a brief qualification to the user:

```markdown
## Qualification: [Area]

### How it works
[2-3 sentences showing you understand the data flow, not just the file structure]

### Key invariants
[List the invariants from the project's agent guide or skill that apply here]

### What could break
[List specific things that could regress if you're not careful — pull from `.cursor/learnings.md` when relevant]

### My approach
[1-2 sentences on how you plan to make the change safely]
```

### 3. Wait for confirmation (when it applies)

For **unfamiliar or high-risk** areas, do not start coding until the user acknowledges your qualification (a "yes" or "go" is enough). Skip this wait when the same message already gave an explicit, scoped instruction to implement (posture: when it is clear, execute). If they correct your understanding, update your mental model before proceeding.

## Rules

- **Be specific, not generic.** "I'll be careful with the auth flow" is worthless. "Session tokens are validated in middleware and again in the service layer; changing either without the other breaks authorization" demonstrates understanding.
- **Cite the learnings file.** If `.cursor/learnings.md` has a gotcha for this area, reference it. This shows you read it.
- **Don't over-qualify.** If you've been working in this area for 20+ turns in this session, you don't need to re-qualify. This is for new or unfamiliar areas.
- **If you can't qualify, say so.** "I haven't worked in this area before and need to read more" is honest and respected. Pretending to understand when you don't leads to regressions.
