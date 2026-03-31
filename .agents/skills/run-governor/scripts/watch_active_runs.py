#!/usr/bin/env python3
"""Background watcher for active durable run actions."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from state_io import ACTIVE_ACTION_STATES, action_due, load_action, load_index, parse_iso, reconcile_action, save_action, save_index, utc_now


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Watch active durable run actions")
    parser.add_argument("--logs-root", default="", help="Path to logs/runs root")
    parser.add_argument("--run-root", default="", help="Optional specific run root")
    parser.add_argument("--sleep-seconds", type=int, default=120, help="Loop interval when not using --once")
    parser.add_argument("--tail-lines", type=int, default=20)
    parser.add_argument("--once", action="store_true", help="Run one sweep and exit")
    return parser


def iter_run_roots(args: argparse.Namespace) -> List[Path]:
    if args.run_root:
        return [Path(args.run_root).resolve()]
    logs_root = Path(args.logs_root).resolve()
    if not logs_root.exists():
        return []
    return sorted(path for path in logs_root.iterdir() if path.is_dir())


def sweep_run(run_root: Path, tail_lines: int) -> Dict[str, object]:
    index = load_index(run_root)
    updates = []
    now = datetime.now(timezone.utc)
    for action_id in index.get("action_ids", []):
        payload = load_action(run_root, action_id)
        if str(payload.get("status", "")) not in ACTIVE_ACTION_STATES and not action_due(payload, now):
            continue
        if not action_due(payload, now):
            continue
        payload, summary = reconcile_action(payload, tail_lines=tail_lines)
        save_action(run_root, payload)
        updates.append(summary)
    index["last_sweep_at"] = utc_now()
    save_index(run_root, index)
    return {
        "run_root": str(run_root),
        "updates": updates,
    }


def compute_global_sleep_seconds(run_roots: List[Path], fallback_seconds: int) -> int:
    now = datetime.now(timezone.utc)
    next_due_seconds: List[int] = []
    for run_root in run_roots:
        index = load_index(run_root)
        for action_id in index.get("action_ids", []):
            payload = load_action(run_root, action_id)
            status = str(payload.get("status", ""))
            if status not in ACTIVE_ACTION_STATES:
                continue
            next_poll_at = str(payload.get("next_poll_at", "")).strip()
            if not next_poll_at:
                next_due_seconds.append(1)
                continue
            delta = int((parse_iso(next_poll_at) - now).total_seconds())
            next_due_seconds.append(max(delta, 1))
    if not next_due_seconds:
        return fallback_seconds
    return max(1, min(fallback_seconds, min(next_due_seconds)))


def main() -> int:
    args = build_parser().parse_args()
    sleep_seconds = max(args.sleep_seconds, 1)

    while True:
        run_roots = iter_run_roots(args)
        summaries = [sweep_run(run_root, max(args.tail_lines, 0)) for run_root in run_roots]
        print(json.dumps({"timestamp": utc_now(), "runs": summaries}, ensure_ascii=True, indent=2))
        if args.once:
            return 0
        time.sleep(compute_global_sleep_seconds(run_roots, sleep_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
