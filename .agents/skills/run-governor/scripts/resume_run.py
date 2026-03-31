#!/usr/bin/env python3
"""Reconcile active long-running actions and summarize resume state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from state_io import ACTIVE_ACTION_STATES, action_due, load_action, load_index, load_working_state, reconcile_action, save_action, save_index, utc_now


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resume a durable research run")
    parser.add_argument("--run-root", required=True, help="Path to logs/runs/<run_id>")
    parser.add_argument("--tail-lines", type=int, default=20)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_root = Path(args.run_root).resolve()
    index = load_index(run_root)
    active: List[Dict[str, Any]] = []

    for action_id in index.get("action_ids", []):
        payload = load_action(run_root, action_id)
        if str(payload.get("status", "")) in ACTIVE_ACTION_STATES or action_due(payload):
            payload, summary = reconcile_action(payload, tail_lines=max(args.tail_lines, 0))
            save_action(run_root, payload)
            active.append(summary)

    index["last_sweep_at"] = utc_now()
    save_index(run_root, index)
    working = load_working_state(run_root)
    print(
        json.dumps(
            {
                "run_root": str(run_root),
                "active_actions": active,
                "working_state": working.get("state", {}),
                "working_todo": working.get("todo", {}),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
