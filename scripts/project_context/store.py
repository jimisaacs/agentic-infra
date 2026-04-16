from __future__ import annotations

from pathlib import Path

import lancedb

from .corpus import ChunkRecord
from .runtime import RuntimePaths

TABLE_NAME = "docs"


def connect(paths: RuntimePaths):
    paths.db_path.mkdir(parents=True, exist_ok=True)
    return lancedb.connect(paths.db_path)


def replace_chunks(paths: RuntimePaths, chunks: list[ChunkRecord]) -> int:
    db = connect(paths)
    rows = [chunk.to_row() for chunk in chunks]
    db.create_table(TABLE_NAME, data=rows, mode="overwrite")
    return len(rows)


def has_index(paths: RuntimePaths) -> bool:
    try:
        db = connect(paths)
        db.open_table(TABLE_NAME)
        return True
    except Exception:
        return False


def load_rows(paths: RuntimePaths) -> list[dict[str, object]]:
    db = connect(paths)
    table = db.open_table(TABLE_NAME)
    return table.to_arrow().to_pylist()


def row_count(paths: RuntimePaths) -> int:
    if not has_index(paths):
        return 0
    db = connect(paths)
    table = db.open_table(TABLE_NAME)
    return table.count_rows()
