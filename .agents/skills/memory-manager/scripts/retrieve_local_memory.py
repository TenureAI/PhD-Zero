#!/usr/bin/env python3
"""Retrieve local experience memory from project-local memory storage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from memory_store import format_record, load_records, matches_filters, normalize_terms, resolve_memory_root, score_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search local project memory")
    parser.add_argument("--memory-root", default="", help="Explicit path to memory root")
    parser.add_argument("--project-root", default="", help="Project root for inferring .project_local memory")
    parser.add_argument("--project-slug", default="", help="Project slug for inferring memory path")
    parser.add_argument("--query", default="", help="Free-text query")
    parser.add_argument("--type", choices=["episode", "procedure", "insight"], default="")
    parser.add_argument("--task-type", default="")
    parser.add_argument("--project", default="")
    parser.add_argument("--error-signature", default="")
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    memory_root = resolve_memory_root(args.memory_root, args.project_root, args.project_slug)
    if not memory_root.exists():
        payload = {"memory_root": str(memory_root), "results": []}
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 0

    filters = {
        "type": args.type,
        "task_type": args.task_type,
        "project": args.project,
        "error_signature": args.error_signature,
        "tags": args.tag,
    }
    query_terms = normalize_terms(args.query)
    ranked = []
    for record in load_records(memory_root):
        if not matches_filters(record, filters):
            continue
        score, matched_terms = score_record(record, query_terms)
        if score <= 0:
            continue
        ranked.append((score, matched_terms, record))

    ranked.sort(key=lambda item: str(item[2].metadata.get("updated_at", "")), reverse=True)
    ranked.sort(key=lambda item: item[0], reverse=True)
    results = [
        format_record(record, score, matched_terms, memory_root)
        for score, matched_terms, record in ranked[: max(args.limit, 1)]
    ]
    payload = {
        "memory_root": str(memory_root),
        "query": args.query,
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
