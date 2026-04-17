from __future__ import annotations

from .corpus import ChunkRecord
from .runtime import RuntimePaths

_STORE: list[dict[str, object]] = []


def replace_chunks(paths: RuntimePaths, chunks: list[ChunkRecord]) -> int:
    global _STORE
    _STORE = [chunk.to_row() for chunk in chunks]
    return len(_STORE)


def has_index(paths: RuntimePaths) -> bool:
    return len(_STORE) > 0


def load_rows(paths: RuntimePaths) -> list[dict[str, object]]:
    return list(_STORE)


def row_count(paths: RuntimePaths) -> int:
    return len(_STORE)
