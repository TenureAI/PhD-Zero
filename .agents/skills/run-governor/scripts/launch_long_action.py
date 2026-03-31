#!/usr/bin/env python3
"""Launch a long-running action and persist durable state."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from state_io import ensure_run_layout, next_poll_timestamp, save_action, utc_now


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch and register a long-running action")
    parser.add_argument("--run-root", required=True, help="Path to logs/runs/<run_id>")
    parser.add_argument("--action-id", default="", help="Stable action id; auto-generated if omitted")
    parser.add_argument("--kind", default="long_action", help="Action kind label")
    parser.add_argument("--shell-command", default="", help="Command to launch via shell")
    parser.add_argument("--cwd", default="", help="Working directory for launch")
    parser.add_argument("--expected-duration-seconds", type=int, default=600)
    parser.add_argument("--poll-interval-seconds", type=int, default=120)
    parser.add_argument("--success-signal", default="", help="Substring indicating success in logs")
    parser.add_argument("--failure-signal", default="", help="Substring indicating failure in logs")
    parser.add_argument("--resume-step", default="", help="Suggested resume step after polling")
    parser.add_argument("--log-path", default="", help="Optional explicit log path")
    parser.add_argument("--no-launch", action="store_true", help="Persist only; do not launch a command")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_root = Path(args.run_root).resolve()
    actions_root, _ = ensure_run_layout(run_root)

    timestamp = utc_now().replace(":", "").replace("-", "").replace("+00:00", "Z")
    action_id = args.action_id.strip() or f"act_{timestamp.lower()}"
    cwd = str(Path(args.cwd).resolve()) if args.cwd else os.getcwd()
    log_path = Path(args.log_path).resolve() if args.log_path else (actions_root / f"{action_id}.log")

    record = {
        "action_id": action_id,
        "status": "pending",
        "kind": args.kind,
        "command": args.shell_command,
        "cwd": cwd,
        "expected_duration_seconds": max(args.expected_duration_seconds, 1),
        "poll_interval_seconds": max(args.poll_interval_seconds, 1),
        "launch_time": utc_now(),
        "last_heartbeat": "",
        "last_poll_at": "",
        "next_poll_at": next_poll_timestamp(max(args.poll_interval_seconds, 1)),
        "success_signal": args.success_signal,
        "failure_signal": args.failure_signal,
        "resume_step": args.resume_step,
        "log_path": str(log_path),
        "pid": None,
    }

    if args.shell_command and not args.no_launch:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            process = subprocess.Popen(
                args.shell_command,
                shell=True,
                cwd=cwd,
                stdout=handle,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                executable=os.environ.get("SHELL") or "/bin/sh",
            )
        record["pid"] = process.pid
        record["status"] = "running"
        record["last_heartbeat"] = utc_now()

    save_action(run_root, record)
    print(
        json.dumps(
            {
                "run_root": str(run_root),
                "action_id": action_id,
                "status": record["status"],
                "pid": record["pid"],
                "poll_interval_seconds": record["poll_interval_seconds"],
                "next_poll_at": record["next_poll_at"],
                "log_path": record["log_path"],
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
