# Git Workflow

This repo uses a stacked branch model via Graphite, with a conservative guard that enforces P5 (earned trust). This skill covers the workflow depth beyond what the `cli` and `worktrees` rules define as policy.

## Quick Reference

| I need to... | Read |
|---|---|
| Understand allowed commands | Guard policy (see `cli` rule) |
| Navigate the teaching stack | Stack navigation |
| Work with Graphite | Graphite workflow |
| Use worktrees | Worktree model |

## Stack navigation

The repo uses stacked branches: `main` → `stack/1-core` → `stack/2-agents-personas` → ... → `stack/6-evals`. Each branch builds on its parent and adds one teaching concern. No branch removes content from its parent (P16: additive layering).

```bash
gt log                    # see the full stack
gt checkout stack/3-mcp   # switch to a branch
gt restack                # rebase the stack after changes to a lower branch
```

When you change a lower branch, you must restack to propagate those changes upward. Conflicts during restack are resolved branch by branch.

## Graphite workflow

Graphite (`gt`) manages the stacked PR workflow. The `cli` rule defines what's allowed; this skill covers the patterns.

**Creating work:**
```bash
gt create -m "description"    # create a new branch on the stack
gt modify --commit             # amend or squash into current branch
```

**Syncing and shipping:**
```bash
gt sync                       # fetch and update from remote
gt restack                    # rebase all branches in the stack
gt submit                     # push and create/update PRs
```

Keep `gt sync`, `gt restack`, and `gt submit` in the home checkout. If you use worktrees, edit and commit from the worktree, but manage the stack from home.

## Worktree model

Worktrees let you edit one branch in isolation without branch-hopping in your main checkout. See the `worktrees` rule for the full model.

Key pattern: one worktree per branch you're actively editing. The home checkout stays on whatever branch you're managing the stack from.

```bash
git worktree add ../wt-3-mcp stack/3-mcp    # create a worktree
# edit and commit in the worktree
# gt restack and gt submit from home
```

## Guard constraints

The guard (`.claude/hooks/guard.py`) enforces the git allowlist defined in the `cli` rule. It inspects `git` invocations only -- `gt` commands and non-git shell commands pass through.

If a git command is blocked, check the `cli` rule for the allowlist. If you need a command that's not allowed, ask -- the guard is a trust boundary, not a permanent restriction.

## Anti-patterns

- Don't force-push, rebase, or reset `main`
- Don't delete branches without explicit instruction
- Don't use compound shell commands around git (`&&`, `||`, `;`, `|`)
- Don't use repo-hopping flags (`-C`, `--git-dir`, `--work-tree`)
- Don't manage the stack (restack, submit) from a worktree -- use the home checkout
