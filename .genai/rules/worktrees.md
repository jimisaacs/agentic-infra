# Worktrees

Rules for the Graphite + worktree execution model.

## Tool Responsibilities

| Tool | Owns | When to use |
| --- | --- | --- |
| **Graphite (`gt`)** | Stack relationships, rebasing, PR submission, sync | Home-checkout stack management |
| **Git worktrees** | Additional checkouts for isolated editing and execution | Long-running work, parallel changes, dependency isolation |
| **Cursor `/worktree`** | Editor-native UX for opening isolated worktrees | Spinning up an isolated checkout from Cursor |
| **Home checkout** | Stack control plane | `gt sync`, `gt restack`, `gt submit`, broad branch navigation |

## Workflow

Keep one home checkout as the stack control plane. Use worktrees when you want isolated editing or execution without day-to-day branch switching in the home checkout.

```text
# home checkout
gt checkout stack/5-rag
git worktree add ../worktrees/core stack/1-core

# in the worktree
./dev verify
gt modify -c -m "description"
git push

# back in the home checkout
gt restack --branch stack/1-core --upstack
gt submit
```

## Rules

- **Worktrees are valid for isolated execution on stack branches.** Edit, test, commit, and push from the worktree that owns the branch.
- **Keep one home checkout for Graphite stack management.** Run `gt sync`, `gt restack`, and `gt submit` there.
- **Do not rely on `gt checkout <branch>` once that branch is occupied by another worktree.** Branch occupancy is a real limitation; target restacks from the home checkout instead.
- **Do not treat one worktree per stack branch as the canonical model.** Additional worktrees are optional tools, not the stack itself.
- **Cursor `/worktree` and Git worktrees are related but not identical.** Use repo rules and Graphite commands as the source of truth for stack operations.
- **Don't assume the default branch or default ports.** Always check the environment.

## Environment Isolation

Cursor worktrees use `.cursor/worktrees.json` for setup. The current config is intentionally minimal: it copies `.env` from the root worktree if it exists. Add heavier bootstrap steps there only when the project genuinely needs them.

Default ports apply only to the main working tree. Worktrees should use offset ports to avoid conflicts.

## Graphite MCP

The GT MCP server is registered in `.cursor/mcp.json`. This allows agents to create stacked PRs through the MCP protocol when instructed.
