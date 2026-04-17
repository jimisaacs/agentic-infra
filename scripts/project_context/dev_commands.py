from __future__ import annotations

import os
from pathlib import Path
import subprocess
from typing import Callable

from .runtime import find_runtime_python
from .runtime import hook_status
from .runtime import install_git_hooks
from .runtime import load_runtime_state
from .runtime import project_context_pip
from .runtime import project_context_python
from .runtime import runtime_paths


Printer = Callable[[str], None]


def context_summary(repo_root: Path) -> dict[str, object]:
    paths = runtime_paths(repo_root)
    runtime_python, version = find_runtime_python()
    return {
        "runtime_python": str(runtime_python) if runtime_python else "missing",
        "runtime_python_version": ".".join(str(part) for part in version) if version else "missing",
        "venv_exists": paths.venv_path.exists(),
        "venv_python": str(project_context_python(paths)),
        "state": load_runtime_state(paths) or {},
        "hooks": hook_status(repo_root),
    }


def setup_runtime(repo_root: Path, print_ok: Printer, print_warn: Printer, print_error: Printer) -> int:
    paths = runtime_paths(repo_root)
    runtime_python, version = find_runtime_python()
    if runtime_python is None or version is None:
        print_error("missing compatible Python runtime for project-context (need >= 3.10)")
        print_warn("Set PROJECT_CONTEXT_PYTHON or install python3.10+ to use `./dev setup`.")
        return 1

    venv_python = project_context_python(paths)
    if not venv_python.exists():
        proc = subprocess.run([str(runtime_python), "-m", "venv", str(paths.venv_path)], cwd=repo_root, check=False)
        if proc.returncode != 0:
            print_error("failed to create .venv for project-context")
            return proc.returncode
        print_ok(f"created runtime venv with {runtime_python} ({'.'.join(str(part) for part in version)})")
    else:
        print_ok("runtime venv already exists")

    pip = project_context_pip(paths)
    env = os.environ.copy()
    env.setdefault("PIP_INDEX_URL", "https://pypi.org/simple")
    install_steps = [
        [str(pip), "install", "--disable-pip-version-check", "--upgrade", "pip"],
        [str(pip), "install", "--disable-pip-version-check", "--requirement", str(paths.lock_path)],
    ]
    for command in install_steps:
        proc = subprocess.run(command, cwd=repo_root, env=env, check=False)
        if proc.returncode != 0:
            print_error(f"dependency install failed: {' '.join(command[1:])}")
            return proc.returncode
    print_ok("project-context dependencies installed")

    installed_hooks = install_git_hooks(repo_root)
    print_ok(f"installed git hooks: {', '.join(installed_hooks)}")

    rebuild_result = run_context_cli(repo_root, ["rebuild"], print_error)
    if rebuild_result != 0:
        return rebuild_result
    smoke_result = run_context_cli(repo_root, ["smoke"], print_error)
    if smoke_result != 0:
        return smoke_result
    print_ok("project-context runtime ready")
    return 0


def run_context_cli(repo_root: Path, subcommand: list[str], print_error: Printer) -> int:
    paths = runtime_paths(repo_root)
    python = project_context_python(paths)
    if not python.exists():
        print_error("project-context runtime is not set up; run `./dev setup` first")
        return 1
    command = [str(python), "-m", "scripts.project_context.cli", "--repo-root", str(repo_root), *subcommand]
    proc = subprocess.run(command, cwd=repo_root, check=False)
    return proc.returncode
