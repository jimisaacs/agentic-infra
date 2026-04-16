# Execution Model + CLI Policy

## Toolchain Policy

Prefer one obvious control plane for local agent work. In this template, that entry point is `./dev`.

Baseline control-plane commands:

- `./dev help`
- `./dev setup`
- `./dev verify`
- `./dev fmt`
- `./dev doctor`
- `./dev status`
- `./dev snip ...`
- `./dev context ...`

Downstream projects may replace `./dev` with another entrypoint, but they should keep the same contract: verification, formatting, environment inspection, and any agent-facing shell helpers should route through one blessed interface.

In this repo, `./dev verify` stays bootstrap-independent. `./dev setup` bootstraps the optional local `project-context` runtime and installs thin Git hook wrappers for the current clone. Grouped `./dev context ...` commands operate that runtime once it exists.

On `stack/1-core`, `./dev setup` and `./dev context ...` are forward-compatible surfaces: the commands exist, but the local `project-context` runtime is not available until layer 3.

## Git — Controlled Mutation via Graphite

Agents may mutate git state through **Graphite (`gt`)** and controlled git commands on stack branches.

### Always allowed (read-only)

- `git status`, `git diff`, `git log`, `git show`, `git blame`
- `git fetch`, `git rev-parse`, `git ls-files`
- `git worktree list`
- conservative branch-listing forms such as `git branch --list` and `git branch --show-current`

### Allowed for stack development

- `gt` commands: `create`, `modify`, `submit`, `sync`, `restack`, `checkout`, `track`, `log`
- `git add`, `git commit`, `git push` on stack branches
- `git checkout`, `git switch` for branch navigation
- `git worktree add`, `git worktree remove`, `git worktree prune`

For worktree-based stack execution:

- Edit, commit, and push from the worktree that owns the branch
- Keep `gt sync`, `gt restack`, `gt submit`, and broad stack navigation in the home checkout
- If a branch is already checked out in another worktree, `gt checkout <branch>` from the home checkout will fail

### Never allowed

- Force-push, rebase, or reset on `main`
- `git reset --hard`, `git clean -fd`, or other destructive operations
- Deleting branches without explicit instruction
- Compound shell commands around git (chaining with `&&`, `||`, `;`, `|`)
- Repo-hopping globals: `-C`, `-c`, `--git-dir`, `--work-tree`

The guard in `.claude/hooks/guard.py` enforces the git allowlist above. It inspects `git` invocations only -- `gt` commands pass through because `gt` is a separate binary. Branch-level policies (e.g. no force-push on `main`) are social conventions enforced by review, not by the guard's lexer.

## Protected Files

Never modify guard scripts, hook configs, or cli rules without explicit consent.
