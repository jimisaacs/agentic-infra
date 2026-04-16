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


def replace_chunks_with_vectors(
    paths: RuntimePaths,
    rows: list[dict[str, object]],
) -> int:
    db = connect(paths)
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
    return len(load_rows(paths))


def vector_search(
    paths: RuntimePaths,
    query_vector: list[float],
    limit: int = 10,
) -> list[dict[str, object]]:
    db = connect(paths)
    try:
        table = db.open_table(TABLE_NAME)
    except Exception:
        return []
    try:
        results = (
            table.search(query_vector, vector_column_name="vector")
            .limit(limit)
            .to_arrow()
            .to_pylist()
        )
        return results
    except Exception:
        return []
