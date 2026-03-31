#!/usr/bin/env python3
"""Poll a long-running action and refresh durable liveness state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from state_io import load_action, next_poll_timestamp, reconcile_action, save_action


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Poll a long-running action")
    parser.add_argument("--run-root", required=True, help="Path to logs/runs/<run_id>")
    parser.add_argument("--action-id", required=True, help="Action id to poll")
    parser.add_argument("--tail-lines", type=int, default=20, help="Number of log lines to retain")
    parser.add_argument("--poll-interval-seconds", type=int, default=0, help="Optional model-selected interval for the next poll")
    parser.add_argument("--next-poll-seconds", type=int, default=0, help="Optional explicit delay for the next poll")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_root = Path(args.run_root).resolve()
    payload = load_action(run_root, args.action_id)
    if args.poll_interval_seconds > 0:
        payload["poll_interval_seconds"] = max(args.poll_interval_seconds, 1)
    updated, summary = reconcile_action(payload, tail_lines=max(args.tail_lines, 0))
    if args.next_poll_seconds > 0 and str(updated.get("status", "")) in {"pending", "running", "stalled"}:
        updated["poll_interval_seconds"] = max(args.next_poll_seconds, 1)
        updated["next_poll_at"] = next_poll_timestamp(max(args.next_poll_seconds, 1))
        summary["poll_interval_seconds"] = updated["poll_interval_seconds"]
        summary["next_poll_at"] = updated["next_poll_at"]
    save_action(run_root, updated)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
