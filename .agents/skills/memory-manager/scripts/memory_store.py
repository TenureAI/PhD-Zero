#!/usr/bin/env python3
"""Helpers for local memory retrieval and working-state persistence."""

from __future__ import annotations

import ast
import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT_FOLDERS = {
    "episodes": "episode",
    "procedures": "procedure",
    "insights": "insight",
}


@dataclass
class Record:
    path: Path
    metadata: Dict[str, Any]
    body: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_scalar(value: str) -> Any:
    if not value:
        return ""
    if value[0] in {'"', "'"} and value[-1] == value[0]:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value
        return parsed if isinstance(parsed, list) else value
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    lines = text.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, text
    metadata: Dict[str, Any] = {}
    for line in lines[1:end_idx]:
        if not line.strip() or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(raw_value.strip())
    body = "\n".join(lines[end_idx + 1 :]).strip()
    return metadata, body


def normalize_terms(text: str) -> List[str]:
    return [term for term in re.split(r"[^a-z0-9_+-]+", text.lower()) if len(term) >= 2]


def read_structured(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError:
            raise RuntimeError(f"Structured file is not JSON and PyYAML is unavailable: {path}")
        payload = yaml.safe_load(text)
        return payload if isinstance(payload, dict) else {}


def write_structured(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)


def resolve_memory_root(memory_root: str, project_root: str, project_slug: str) -> Path:
    if memory_root:
        return Path(memory_root).resolve()
    root = Path(project_root).resolve()
    if not project_slug:
        project_local = root / ".project_local"
        if project_local.exists():
            children = [child for child in project_local.iterdir() if child.is_dir()]
            if len(children) == 1:
                project_slug = children[0].name
    if not project_slug:
        raise ValueError("Unable to resolve project slug; pass --memory-root or --project-slug")
    return root / ".project_local" / project_slug / "memory"


def load_records(memory_root: Path) -> List[Record]:
    records: List[Record] = []
    for folder, expected_type in ROOT_FOLDERS.items():
        root = memory_root / folder
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(text)
            if not metadata:
                continue
            declared_type = str(metadata.get("type", "")).strip()
            if declared_type and declared_type != expected_type:
                continue
            metadata.setdefault("type", expected_type)
            metadata.setdefault("tags", [])
            records.append(Record(path=path, metadata=metadata, body=body))
    return records


def matches_filters(record: Record, filters: Dict[str, Any]) -> bool:
    metadata = record.metadata
    record_type = str(metadata.get("type", "")).strip()
    if filters.get("type") and record_type != filters["type"]:
        return False
    if filters.get("task_type") and str(metadata.get("task_type", "")).strip() != filters["task_type"]:
        return False
    if filters.get("project") and str(metadata.get("project", "")).strip() != filters["project"]:
        return False
    if filters.get("error_signature"):
        if filters["error_signature"].lower() not in str(metadata.get("error_signature", "")).lower():
            return False
    tags = {str(tag).lower() for tag in metadata.get("tags", []) if str(tag).strip()}
    requested_tags = {str(tag).lower() for tag in filters.get("tags", [])}
    if requested_tags and not requested_tags.issubset(tags):
        return False
    return True


def score_record(record: Record, query_terms: Iterable[str]) -> Tuple[int, List[str]]:
    metadata = record.metadata
    title = str(metadata.get("title", "")).lower()
    tags = " ".join(str(tag).lower() for tag in metadata.get("tags", []))
    error_signature = str(metadata.get("error_signature", "")).lower()
    project = str(metadata.get("project", "")).lower()
    task_type = str(metadata.get("task_type", "")).lower()
    body = record.body.lower()
    record_type = str(metadata.get("type", "")).lower()
    status = str(metadata.get("status", "")).lower()

    score = 0
    matched: List[str] = []
    for term in query_terms:
        term_score = 0
        if term in title:
            term_score += 4
        if term in tags:
            term_score += 3
        if term in error_signature:
            term_score += 3
        if term in project or term in task_type:
            term_score += 2
        if term in body:
            term_score += 1
        if term_score:
            matched.append(term)
            score += term_score

    if record_type == "procedure":
        score += 3
    elif record_type == "episode":
        score += 2
    elif record_type == "insight":
        score += 1

    if status == "active":
        score += 2
    elif status == "draft":
        score += 1

    if not list(query_terms):
        score = max(score, 1)

    return score, sorted(set(matched))


def format_record(record: Record, score: int, matched_terms: List[str], memory_root: Path) -> Dict[str, Any]:
    body_preview = " ".join(record.body.split())
    if len(body_preview) > 220:
        body_preview = body_preview[:217] + "..."
    return {
        "id": record.metadata.get("id", ""),
        "title": record.metadata.get("title", ""),
        "type": record.metadata.get("type", ""),
        "status": record.metadata.get("status", ""),
        "task_type": record.metadata.get("task_type", ""),
        "project": record.metadata.get("project", ""),
        "tags": record.metadata.get("tags", []),
        "error_signature": record.metadata.get("error_signature", ""),
        "score": score,
        "matched_terms": matched_terms,
        "path": str(record.path.relative_to(memory_root)),
        "preview": body_preview,
        "source": "project-local-memory",
    }
