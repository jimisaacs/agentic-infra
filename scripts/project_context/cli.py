from __future__ import annotations

import argparse
import json
from pathlib import Path

from .corpus import build_corpus
from .corpus import rank_rows
from .runtime import hook_status
from .runtime import load_runtime_state
from .runtime import runtime_paths
from .runtime import save_runtime_state
from .store import has_index
from .store import load_rows
from .store import replace_chunks


def rebuild_index(repo_root: Path) -> dict[str, object]:
    paths = runtime_paths(repo_root)
    chunks, warnings = build_corpus(repo_root)
    chunk_count = replace_chunks(paths, chunks)
    payload = {
        "indexed_at": chunks[0].indexed_at if chunks else "",
        "chunk_count": chunk_count,
        "corpus_paths": sorted({chunk.source_path for chunk in chunks}),
        "warning_count": len(warnings),
        "warnings": warnings,
    }
    save_runtime_state(paths, payload)
    return {"ok": True, **payload}


def print_json(payload: dict[str, object]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok", False) else 1


def cmd_rebuild(args: argparse.Namespace) -> int:
    return print_json(rebuild_index(Path(args.repo_root).resolve()))


def cmd_search(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    paths = runtime_paths(repo_root)
    if not has_index(paths):
        return print_json(
            {
                "ok": False,
                "error": "index is missing",
                "hint": "Run `./dev setup` or `./dev context rebuild` first.",
            }
        )
    rows = load_rows(paths)
    return print_json(
        {
            "ok": True,
            "query": args.query,
            "results": rank_rows(rows, args.query, args.limit),
        }
    )


def cmd_status(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    paths = runtime_paths(repo_root)
    return print_json(
        {
            "ok": True,
            "server": "project-context",
            "repo_root": str(repo_root),
            "state": load_runtime_state(paths) or {},
            "index_present": has_index(paths),
            "hooks": hook_status(repo_root),
            "deferrals": [
                "changes",
                "symbols",
                "mcp_resources",
                "mcp_prompts",
                "shared_platform_mcp",
            ],
        }
    )


def cmd_smoke(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    paths = runtime_paths(repo_root)
    if not has_index(paths):
        rebuild_index(repo_root)
    rows = load_rows(paths)
    results = rank_rows(rows, "control plane", 3)
    if not results:
        return print_json(
            {
                "ok": False,
                "error": "smoke query returned no results",
                "hint": "Expected docs-first corpus results for `control plane`.",
            }
        )
    return print_json(
        {
            "ok": True,
            "query": "control plane",
            "top_result": results[0],
            "result_count": len(results),
        }
    )


def cmd_serve(_args: argparse.Namespace) -> int:
    from .server import mcp

    mcp.run()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="project-context")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    subparsers = parser.add_subparsers(dest="command", required=True)

    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild the docs-first local index")
    rebuild_parser.set_defaults(func=cmd_rebuild)

    search_parser = subparsers.add_parser("search", help="Search the docs-first local index")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)
    search_parser.set_defaults(func=cmd_search)

    status_parser = subparsers.add_parser("status", help="Report local project-context status")
    status_parser.set_defaults(func=cmd_status)

    smoke_parser = subparsers.add_parser("smoke", help="Run a minimal runtime smoke check")
    smoke_parser.set_defaults(func=cmd_smoke)

    serve_parser = subparsers.add_parser("serve", help="Serve the local FastMCP server over stdio")
    serve_parser.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
