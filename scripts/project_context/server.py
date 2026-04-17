from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

from . import SERVER_NAME
from . import V1_BUNDLES
from .corpus import filter_rows_by_id
from .corpus import filter_rows_by_source
from .corpus import matching_decisions
from .corpus import rank_rows
from .corpus import chunk_warnings
from .runtime import classify_relative_path
from .runtime import content_hash
from .runtime import hook_status
from .runtime import load_runtime_state
from .runtime import resolve_allowlisted_path
from .runtime import runtime_paths
from .store import has_index
from .store import load_rows

REPO_ROOT = Path(__file__).resolve().parents[2]
PATHS = runtime_paths(REPO_ROOT)
mcp = FastMCP(SERVER_NAME)


def index_unavailable() -> dict[str, object]:
    return {
        "ok": False,
        "error": "project-context index is not built yet",
        "hint": "Run `./dev setup` or `./dev context rebuild` first.",
    }


def resolve_allowlisted_file(source_path: str) -> Path | None:
    resolved = resolve_allowlisted_path(source_path, REPO_ROOT)
    if resolved is None:
        return None
    return resolved[0]


@mcp.tool
def status() -> dict[str, object]:
    state = load_runtime_state(PATHS)
    return {
        "ok": True,
        "server": SERVER_NAME,
        "repo_root": str(REPO_ROOT),
        "index_present": has_index(PATHS),
        "state": state or {},
        "hooks": hook_status(REPO_ROOT),
        "deferrals": [
            "changes",
            "symbols",
            "mcp_resources",
            "mcp_prompts",
            "shared_platform_mcp",
        ],
    }


@mcp.tool
def rebuild() -> dict[str, object]:
    from .cli import rebuild_index

    return rebuild_index(REPO_ROOT)


@mcp.tool
def search(query: str, limit: int = 8) -> dict[str, object]:
    if not has_index(PATHS):
        return index_unavailable()
    rows = load_rows(PATHS)
    results = rank_rows(rows, query, limit)
    return {
        "ok": True,
        "query": query,
        "results": results,
        "result_count": len(results),
    }


@mcp.tool
def fetch(stable_id: str = "", source_path: str = "") -> dict[str, object]:
    if bool(stable_id) == bool(source_path):
        return {"ok": False, "error": "Provide exactly one of `stable_id` or `source_path`."}

    if has_index(PATHS):
        rows = load_rows(PATHS)
        if stable_id:
            matched = filter_rows_by_id(rows, stable_id)
            if matched:
                return {"ok": True, "mode": "indexed_chunk", "item": matched}
        if source_path:
            matched_rows = filter_rows_by_source(rows, source_path)
            if matched_rows:
                return {"ok": True, "mode": "indexed_file", "items": matched_rows}

    if source_path:
        resolved = resolve_allowlisted_path(source_path, REPO_ROOT)
        if resolved is None:
            return {"ok": False, "error": "Path is not in the allowlisted docs-first corpus."}
        file_path, relative = resolved
        text = file_path.read_text(encoding="utf-8")
        return {
            "ok": True,
            "mode": "allowlisted_file",
            "items": [
                {
                    "source_path": relative,
                    "stable_id": f"{relative}::document",
                    "label": file_path.name,
                    "class": classify_relative_path(relative),
                    "text": text,
                    "freshness": content_hash(text),
                    "score_rationale": {},
                    "warnings": chunk_warnings(relative, text),
                }
            ],
        }

    return {"ok": False, "error": "No indexed chunk found for the requested stable_id."}


@mcp.tool
def decisions(query: str = "") -> dict[str, object]:
    matches = matching_decisions(REPO_ROOT, query or None)
    return {
        "ok": True,
        "query": query,
        "backlog": matches["backlog"],
        "adrs": matches["adrs"],
    }


@mcp.tool
def bundle(kind: str, topic: str = "", limit: int = 5) -> dict[str, object]:
    if kind not in V1_BUNDLES:
        return {"ok": False, "error": f"Unsupported bundle kind: {kind}"}

    if kind == "onboarding":
        documents = [
            fetch(source_path="README.md"),
            fetch(source_path="AGENTS.md"),
            fetch(source_path="CLAUDE.md"),
            fetch(source_path="STATUS.md"),
            fetch(source_path="docs/ROADMAP.md"),
        ]
        return {
            "ok": True,
            "kind": kind,
            "documents": documents,
            "decisions": decisions(),
        }

    if not topic:
        return {"ok": False, "error": f"`topic` is required for bundle kind `{kind}`."}

    search_results = search(topic, limit=limit)
    if not search_results.get("ok", False):
        return search_results
    decision_results = decisions(topic)
    return {
        "ok": True,
        "kind": kind,
        "topic": topic,
        "notes": "Docs-first v1 bundle: maps, decisions, learnings, and design context only.",
        "results": search_results.get("results", []),
        "decisions": {
            "backlog": decision_results.get("backlog", []),
            "adrs": decision_results.get("adrs", []),
        },
    }


if __name__ == "__main__":
    mcp.run()
