from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
import re
from pathlib import Path
from typing import Iterable

from .runtime import classify_relative_path
from .runtime import content_hash
from .runtime import iter_corpus_paths
from .runtime import normalize_repo_relative
from .runtime import repo_relative

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
TOKEN_RE = re.compile(r"[A-Za-z0-9_.:/-]+")


@dataclass(frozen=True)
class ChunkRecord:
    stable_id: str
    source_path: str
    label: str
    class_name: str
    text: str
    freshness: str
    indexed_at: str
    warnings: list[str]
    score_rationale: dict[str, object]

    def to_row(self) -> dict[str, object]:
        row = asdict(self)
        row["class"] = row.pop("class_name")
        row["warnings"] = list(self.warnings)
        return row


def build_corpus(repo_root: Path) -> tuple[list[ChunkRecord], list[str]]:
    indexed_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    warnings: list[str] = []
    chunks: list[ChunkRecord] = []
    for path in iter_corpus_paths(repo_root):
        chunks.extend(chunk_markdown_file(path, repo_root, indexed_at))
    warnings.extend(warning for chunk in chunks for warning in chunk.warnings)
    return chunks, sorted(set(warnings))


def chunk_markdown_file(path: Path, repo_root: Path, indexed_at: str) -> list[ChunkRecord]:
    relative = repo_relative(path, repo_root)
    text = path.read_text(encoding="utf-8")
    file_hash = content_hash(text)
    class_name = classify_relative_path(relative)
    warnings = chunk_warnings(relative, text)
    sections = split_sections(relative, text)
    return [
        ChunkRecord(
            stable_id=f"{relative}::{slugify(section['anchor'])}",
            source_path=relative,
            label=section["label"],
            class_name=class_name,
            text=section["text"],
            freshness=file_hash,
            indexed_at=indexed_at,
            warnings=list(warnings),
            score_rationale={},
        )
        for section in sections
    ]


def split_sections(relative_path: str, text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))

    if not headings:
        label = Path(relative_path).name
        body = text.strip() or label
        return [{"anchor": "document", "label": label, "text": body}]

    sections: list[dict[str, str]] = []
    stack: list[tuple[int, str]] = []
    for idx, (line_index, level, title) in enumerate(headings):
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        next_index = len(lines)
        for future_index in range(idx + 1, len(headings)):
            candidate_line, candidate_level, _ = headings[future_index]
            if candidate_level <= level:
                next_index = candidate_line
                break
        section_lines = lines[line_index:next_index]
        label = " > ".join(entry[1] for entry in stack)
        anchor = stack[-1][1]
        section_text = "\n".join(section_lines).strip()
        if section_text:
            sections.append({"anchor": anchor, "label": label, "text": section_text})
    return sections


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "section"


def chunk_warnings(relative_path: str, text: str) -> list[str]:
    warnings: list[str] = []
    if relative_path.startswith("docs/decisions/adr/") and "status: superseded" in text:
        warnings.append("superseded-adr")
    if relative_path == "docs/decisions/backlog.md":
        warnings.extend(backlog_status_warnings(text))
    return warnings


def backlog_status_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for line in text.splitlines():
        if not line.startswith("| DEC-"):
            continue
        parts = [part.strip() for part in line.split("|")[1:-1]]
        if len(parts) < 2:
            continue
        status = parts[1]
        if status in {"resolved", "dropped"}:
            warnings.append(f"backlog-{status}")
    return warnings


def rank_rows(rows: Iterable[dict[str, object]], query: str, limit: int) -> list[dict[str, object]]:
    terms = [term.lower() for term in TOKEN_RE.findall(query)]
    if not terms:
        return []

    ranked: list[dict[str, object]] = []
    for row in rows:
        source_path = str(row["source_path"])
        label = str(row["label"])
        text = str(row["text"])
        class_name = str(row["class"])
        haystacks = [source_path.lower(), label.lower(), text.lower()]
        label_hits = sum(term in haystacks[1] for term in terms)
        path_hits = sum(term in haystacks[0] for term in terms)
        text_hits = sum(term in haystacks[2] for term in terms)
        score = float(path_hits * 4 + label_hits * 3 + text_hits)
        if class_name in {"canonical", "curated"}:
            score += 1.5
        if class_name == "narrative":
            score -= 0.5
        if score <= 0:
            continue

        item = dict(row)
        item["score"] = round(score, 3)
        item["score_rationale"] = {
            "path_hits": path_hits,
            "label_hits": label_hits,
            "text_hits": text_hits,
            "class_boost": class_name if class_name in {"canonical", "curated"} else "none",
        }
        ranked.append(item)

    ranked.sort(key=lambda item: (-float(item["score"]), str(item["source_path"]), str(item["label"])))
    return ranked[:limit]


def filter_rows_by_source(rows: Iterable[dict[str, object]], source_path: str) -> list[dict[str, object]]:
    normalized = normalize_repo_relative(source_path)
    matched = [dict(row) for row in rows if str(row["source_path"]) == normalized]
    matched.sort(key=lambda row: str(row["stable_id"]))
    return matched


def filter_rows_by_id(rows: Iterable[dict[str, object]], stable_id: str) -> dict[str, object] | None:
    for row in rows:
        if str(row["stable_id"]) == stable_id:
            return dict(row)
    return None


def backlog_entries(repo_root: Path) -> list[dict[str, str]]:
    backlog_path = repo_root / "docs/decisions/backlog.md"
    if not backlog_path.exists():
        return []
    entries: list[dict[str, str]] = []
    for line in backlog_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| DEC-"):
            continue
        parts = [part.strip() for part in line.split("|")[1:-1]]
        if len(parts) < 6:
            continue
        entries.append(
            {
                "id": parts[0],
                "status": parts[1],
                "decision": parts[2],
                "trigger": parts[3],
                "tension": parts[4],
                "links": parts[5],
            }
        )
    return entries


def adr_entries(repo_root: Path) -> list[dict[str, str]]:
    adr_root = repo_root / "docs/decisions/adr"
    entries: list[dict[str, str]] = []
    if not adr_root.exists():
        return entries
    for path in sorted(adr_root.glob("ADR-*.md")):
        text = path.read_text(encoding="utf-8")
        front_matter = parse_front_matter(text)
        entries.append(
            {
                "id": str(front_matter.get("id", path.stem)),
                "status": str(front_matter.get("status", "unknown")),
                "decision": str(front_matter.get("decision", path.stem)),
                "path": repo_relative(path, repo_root),
            }
        )
    return entries


def parse_front_matter(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}
    payload: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        payload[key.strip()] = value.strip().strip('"')
    return payload


def decision_matches(entry: dict[str, str], query: str) -> bool:
    haystack = " ".join(entry.values()).lower()
    return all(term.lower() in haystack for term in TOKEN_RE.findall(query))


def matching_decisions(repo_root: Path, query: str | None) -> dict[str, list[dict[str, str]]]:
    backlog = backlog_entries(repo_root)
    adrs = adr_entries(repo_root)
    if not query:
        return {"backlog": backlog, "adrs": adrs}
    return {
        "backlog": [entry for entry in backlog if decision_matches(entry, query)],
        "adrs": [entry for entry in adrs if decision_matches(entry, query)],
    }
