#!/usr/bin/env python3
"""Read-only shared memory retrieval helper.

Search a local open-research-memory clone without importing it into project memory.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT_TYPES = {
    "episodes": "episode",
    "procedures": "procedure",
    "insights": "insight",
}


@dataclass
class Record:
    path: Path
    metadata: Dict[str, Any]
    body: str


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


def load_records(repo_root: Path) -> List[Record]:
    records: List[Record] = []
    for folder, expected_type in ROOT_TYPES.items():
        root = repo_root / folder
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


def normalize_terms(text: str) -> List[str]:
    return [term for term in re.split(r"[^a-z0-9_+-]+", text.lower()) if len(term) >= 2]


def matches_filters(record: Record, args: argparse.Namespace) -> bool:
    metadata = record.metadata

    if args.type and metadata.get("type") != args.type:
        return False
    if args.status and str(metadata.get("status", "")).strip() != args.status:
        return False
    if args.task_type and str(metadata.get("task_type", "")).strip() != args.task_type:
        return False
    if args.error_signature:
        error_signature = str(metadata.get("error_signature", "")).lower()
        if args.error_signature.lower() not in error_signature:
            return False
    if args.tag:
        tags = {str(tag).lower() for tag in metadata.get("tags", []) if str(tag).strip()}
        requested = {tag.lower() for tag in args.tag}
        if not requested.issubset(tags):
            return False
    return True


def score_record(record: Record, query_terms: Iterable[str], args: argparse.Namespace) -> Tuple[int, List[str]]:
    metadata = record.metadata
    title = str(metadata.get("title", "")).lower()
    tags = " ".join(str(tag).lower() for tag in metadata.get("tags", []))
    error_signature = str(metadata.get("error_signature", "")).lower()
    project = str(metadata.get("project", "")).lower()
    task_type = str(metadata.get("task_type", "")).lower()
    body = record.body.lower()

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

    if args.type and metadata.get("type") == args.type:
        score += 2
    if args.task_type and metadata.get("task_type") == args.task_type:
        score += 2
    if args.status and metadata.get("status") == args.status:
        score += 1
    if args.tag:
        tags = {str(tag).lower() for tag in metadata.get("tags", [])}
        score += sum(1 for tag in args.tag if tag.lower() in tags)

    if not query_terms:
        score = 1

    return score, sorted(set(matched))


def format_result(record: Record, score: int, matched_terms: List[str], repo_root: Path) -> Dict[str, Any]:
    metadata = record.metadata
    body_preview = " ".join(record.body.split())
    if len(body_preview) > 220:
        body_preview = body_preview[:217] + "..."
    return {
        "id": metadata.get("id", ""),
        "title": metadata.get("title", ""),
        "type": metadata.get("type", ""),
        "status": metadata.get("status", ""),
        "task_type": metadata.get("task_type", ""),
        "project": metadata.get("project", ""),
        "tags": metadata.get("tags", []),
        "error_signature": metadata.get("error_signature", ""),
        "score": score,
        "matched_terms": matched_terms,
        "path": str(record.path.relative_to(repo_root)),
        "preview": body_preview,
        "source": "shared-repo-readonly",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search a local shared memory repo")
    parser.add_argument("--repo-root", required=True, help="Path to local open-research-memory clone")
    parser.add_argument("--query", default="", help="Free-text query")
    parser.add_argument("--type", choices=sorted(set(ROOT_TYPES.values())), help="Record type filter")
    parser.add_argument("--status", default="", help="Status filter")
    parser.add_argument("--task-type", default="", help="Task type filter")
    parser.add_argument("--tag", action="append", default=[], help="Required tag filter; repeatable")
    parser.add_argument("--error-signature", default="", help="Substring match on error_signature")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of matches to return")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        print(f"Shared repo path does not exist: {repo_root}", file=sys.stderr)
        return 2
    if not (repo_root / ".git").exists():
        print(f"Shared repo path is not a git checkout: {repo_root}", file=sys.stderr)
        return 2

    records = [record for record in load_records(repo_root) if matches_filters(record, args)]
    query_terms = normalize_terms(args.query)

    ranked: List[Tuple[int, List[str], Record]] = []
    for record in records:
        score, matched_terms = score_record(record, query_terms, args)
        if score <= 0:
            continue
        ranked.append((score, matched_terms, record))

    ranked.sort(key=lambda item: str(item[2].metadata.get("title", "")).lower())
    ranked.sort(key=lambda item: str(item[2].metadata.get("updated_at", "")), reverse=True)
    ranked.sort(key=lambda item: item[0], reverse=True)
    results = [
        format_result(record, score, matched_terms, repo_root)
        for score, matched_terms, record in ranked[: max(args.limit, 1)]
    ]

    if args.json:
        print(json.dumps({"repo_root": str(repo_root), "results": results}, ensure_ascii=True, indent=2))
        return 0

    print(f"SharedRepo: {repo_root}")
    print(f"Query: {args.query or '<none>'}")
    print(f"Results: {len(results)}")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}. [{result['type']}/{result['status']}] {result['title']} score={result['score']}")
        print(f"   path={result['path']}")
        if result["task_type"]:
            print(f"   task_type={result['task_type']}")
        if result["tags"]:
            print(f"   tags={','.join(result['tags'])}")
        if result["matched_terms"]:
            print(f"   matched_terms={','.join(result['matched_terms'])}")
        if result["preview"]:
            print(f"   preview={result['preview']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
