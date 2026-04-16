from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional

from .runtime import RuntimePaths

EMBEDDING_DIM = 384
CACHE_FILE = "embedding_cache.json"


def _load_cache(paths: RuntimePaths) -> dict[str, list[float]]:
    cache_path = paths.runtime_root / CACHE_FILE
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(paths: RuntimePaths, cache: dict[str, list[float]]) -> None:
    cache_path = paths.runtime_root / CACHE_FILE
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache), encoding="utf-8")


def _content_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _get_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except ImportError:
        return None


def embed_text(text: str, model=None) -> list[float]:
    if model is None:
        model = _get_model()
    if model is None:
        return _deterministic_fallback(text)
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_texts(texts: list[str], model=None) -> list[list[float]]:
    if model is None:
        model = _get_model()
    if model is None:
        return [_deterministic_fallback(t) for t in texts]
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [e.tolist() for e in embeddings]


def embed_chunks(
    chunks: list[dict[str, object]],
    paths: RuntimePaths,
    force: bool = False,
) -> list[dict[str, object]]:
    cache = _load_cache(paths)
    model = _get_model()
    texts_to_embed: list[tuple[int, str]] = []

    for i, chunk in enumerate(chunks):
        text = str(chunk.get("text", ""))
        key = _content_key(text)
        if not force and key in cache:
            chunk["vector"] = cache[key]
        else:
            texts_to_embed.append((i, text))

    if texts_to_embed:
        batch_texts = [t for _, t in texts_to_embed]
        batch_vectors = embed_texts(batch_texts, model=model)
        for (i, text), vector in zip(texts_to_embed, batch_vectors):
            key = _content_key(text)
            cache[key] = vector
            chunks[i]["vector"] = vector

    _save_cache(paths, cache)
    return chunks


def _deterministic_fallback(text: str) -> list[float]:
    h = hashlib.sha256(text.encode("utf-8")).digest()
    raw = [((b % 200) - 100) / 100.0 for b in h]
    while len(raw) < EMBEDDING_DIM:
        h = hashlib.sha256(h).digest()
        raw.extend([((b % 200) - 100) / 100.0 for b in h])
    vec = raw[:EMBEDDING_DIM]
    norm = max(sum(v * v for v in vec) ** 0.5, 1e-9)
    return [v / norm for v in vec]
