from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
from typing import Iterable

MIN_RUNTIME_PYTHON = (3, 10)
PREFERRED_RUNTIME_CANDIDATES = [
    "python3.13",
    "python3.12",
    "python3.11",
    "python3.10",
]
RUNTIME_DIRNAME = ".project-context"
DB_DIRNAME = "lancedb"
STATE_FILENAME = "state.json"
LOCK_FILENAME = "requirements-project-context.lock"
HOOK_WRAPPER_PATHS = {"pre-commit": ".githooks/pre-commit"}
ALLOWLIST_FILES = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "STATUS.md",
    "docs/ROADMAP.md",
    ".cursor/learnings-index.md",
    ".cursor/learnings.md",
}
ALLOWLIST_PREFIXES = (
    ".genai/rules/",
    ".cursor/skills/",
    "docs/decisions/",
    "docs/design/",
)
DENYLIST_EXACT = {
    ".env",
    ".env.local",
    ".envrc",
}
DENYLIST_PREFIXES = (
    ".git/",
    ".venv/",
    ".project-context/",
    ".tmp-project-context-lock/",
    ".cache/",
    ".local/",
)
DENYLIST_SUFFIXES = (
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".crt",
)
CLASS_PREFIXES = {
    "canonical": (
        ".genai/rules/",
        ".cursor/skills/",
        ".cursor/learnings.md",
        "docs/decisions/",
        "STATUS.md",
    ),
    "curated": (
        "README.md",
        "AGENTS.md",
        "CLAUDE.md",
        "CONTRIBUTING.md",
        "docs/ROADMAP.md",
        ".cursor/learnings-index.md",
    ),
    "narrative": ("docs/design/",),
}


@dataclass(frozen=True)
class RuntimePaths:
    repo_root: Path
    venv_path: Path
    runtime_root: Path
    db_path: Path
    state_path: Path
    lock_path: Path


def runtime_paths(repo_root: Path) -> RuntimePaths:
    runtime_root = repo_root / RUNTIME_DIRNAME
    return RuntimePaths(
        repo_root=repo_root,
        venv_path=repo_root / ".venv",
        runtime_root=runtime_root,
        db_path=runtime_root / DB_DIRNAME,
        state_path=runtime_root / STATE_FILENAME,
        lock_path=repo_root / LOCK_FILENAME,
    )


def project_context_python(paths: RuntimePaths) -> Path:
    return paths.venv_path / "bin" / "python"


def project_context_pip(paths: RuntimePaths) -> Path:
    return paths.venv_path / "bin" / "pip"


def ensure_runtime_dirs(paths: RuntimePaths) -> None:
    paths.runtime_root.mkdir(parents=True, exist_ok=True)
    paths.db_path.mkdir(parents=True, exist_ok=True)


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def is_denylisted_relative(relative_path: str) -> bool:
    lowered = relative_path.lower()
    if lowered in DENYLIST_EXACT:
        return True
    if any(lowered.startswith(prefix) for prefix in DENYLIST_PREFIXES):
        return True
    if any(lowered.endswith(suffix) for suffix in DENYLIST_SUFFIXES):
        return True
    return False


def is_allowlisted_relative(relative_path: str) -> bool:
    if relative_path in ALLOWLIST_FILES:
        return True
    return any(relative_path.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)


def classify_relative_path(relative_path: str) -> str:
    for class_name, prefixes in CLASS_PREFIXES.items():
        if any(relative_path == prefix or relative_path.startswith(prefix) for prefix in prefixes):
            return class_name
    return "derived"


def is_corpus_path(path: Path, repo_root: Path) -> bool:
    try:
        relative = repo_relative(path, repo_root)
    except ValueError:
        return False
    if is_denylisted_relative(relative):
        return False
    return is_allowlisted_relative(relative)


def iter_corpus_paths(repo_root: Path) -> Iterable[Path]:
    for relative in sorted(ALLOWLIST_FILES):
        path = repo_root / relative
        if path.exists() and path.is_file() and is_corpus_path(path, repo_root):
            yield path
    for prefix in ALLOWLIST_PREFIXES:
        root = repo_root / prefix
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and is_corpus_path(path, repo_root):
                yield path


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_repo_relative(value: str) -> str:
    normalized = Path(value).as_posix()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def resolve_allowlisted_path(source_path: str, repo_root: Path) -> tuple[Path, str] | None:
    normalized = normalize_repo_relative(source_path)
    candidate = (repo_root / normalized).resolve()
    try:
        relative = repo_relative(candidate, repo_root)
    except ValueError:
        return None
    if is_denylisted_relative(relative):
        return None
    if not is_allowlisted_relative(relative):
        return None
    if not candidate.exists() or not candidate.is_file():
        return None
    return candidate, relative


def find_runtime_python() -> tuple[Path | None, tuple[int, int, int] | None]:
    env_override = os.environ.get("PROJECT_CONTEXT_PYTHON")
    candidates = []
    if env_override:
        candidates.append(env_override)
    candidates.extend(PREFERRED_RUNTIME_CANDIDATES)

    seen: set[str] = set()
    for raw in candidates:
        resolved = shutil.which(raw) or raw
        if resolved in seen:
            continue
        seen.add(resolved)
        candidate = Path(resolved)
        if not candidate.exists():
            continue
        version = read_python_version(candidate)
        if version and version >= MIN_RUNTIME_PYTHON:
            return candidate, version
    return None, None


def read_python_version(python_path: Path) -> tuple[int, int, int] | None:
    proc = subprocess.run(
        [str(python_path), "-c", "import sys; print('.'.join(str(v) for v in sys.version_info[:3]))"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    parts = proc.stdout.strip().split(".")
    if len(parts) != 3:
        return None
    try:
        return tuple(int(part) for part in parts)  # type: ignore[return-value]
    except ValueError:
        return None


def hook_status(
    repo_root: Path,
    installed_hooks_dir: Path | None = None,
) -> dict[str, dict[str, object]]:
    status: dict[str, dict[str, object]] = {}
    git_hooks_dir = installed_hooks_dir or git_dir(repo_root) / "hooks"
    for hook_name, relative_source in HOOK_WRAPPER_PATHS.items():
        source = repo_root / relative_source
        target = git_hooks_dir / hook_name
        installed = target.exists()
        current = installed and files_match(source, target)
        executable = installed and os.access(target, os.X_OK)
        status[hook_name] = {
            "source_path": relative_source,
            "installed": installed,
            "current": current,
            "executable": executable,
        }
    return status


def files_match(left: Path, right: Path) -> bool:
    if not left.exists() or not right.exists():
        return False
    return left.read_bytes() == right.read_bytes()


def install_git_hooks(repo_root: Path) -> list[str]:
    git_hooks_dir = git_dir(repo_root) / "hooks"
    git_hooks_dir.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for hook_name, relative_source in HOOK_WRAPPER_PATHS.items():
        source = repo_root / relative_source
        target = git_hooks_dir / hook_name
        if target.exists() and not files_match(source, target):
            backup = target.with_name(f"{hook_name}.agentic-infra.bak")
            if not backup.exists():
                backup.write_bytes(target.read_bytes())
        target.write_bytes(source.read_bytes())
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        installed.append(hook_name)
    return installed


def load_runtime_state(paths: RuntimePaths) -> dict[str, object] | None:
    if not paths.state_path.exists():
        return None
    try:
        return json.loads(paths.state_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_runtime_state(paths: RuntimePaths, payload: dict[str, object]) -> None:
    ensure_runtime_dirs(paths)
    paths.state_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_dir(repo_root: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return repo_root / ".git"
    raw = proc.stdout.strip()
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = (repo_root / candidate).resolve()
    return candidate
