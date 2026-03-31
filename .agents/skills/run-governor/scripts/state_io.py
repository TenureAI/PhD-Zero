#!/usr/bin/env python3
"""Shared helpers for durable run and long-action state."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


ACTIVE_ACTION_STATES = {"pending", "running", "stalled"}
FINAL_ACTION_STATES = {"failed", "completed", "cancelled"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_iso(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    return datetime.fromisoformat(normalized)


def next_poll_timestamp(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=max(seconds, 1))).replace(microsecond=0).isoformat()


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


def ensure_run_layout(run_root: Path) -> Tuple[Path, Path]:
    actions_root = run_root / "actions"
    working_root = run_root / "working"
    actions_root.mkdir(parents=True, exist_ok=True)
    working_root.mkdir(parents=True, exist_ok=True)
    return actions_root, working_root


def action_file(run_root: Path, action_id: str) -> Path:
    return run_root / "actions" / f"{action_id}.yaml"


def load_index(run_root: Path) -> Dict[str, Any]:
    _, _ = ensure_run_layout(run_root)
    index_path = run_root / "actions" / "index.json"
    payload = read_structured(index_path)
    payload.setdefault("action_ids", [])
    payload.setdefault("last_sweep_at", "")
    return payload


def save_index(run_root: Path, payload: Dict[str, Any]) -> None:
    write_structured(run_root / "actions" / "index.json", payload)


def register_action(run_root: Path, action_id: str) -> None:
    payload = load_index(run_root)
    action_ids = [item for item in payload.get("action_ids", []) if isinstance(item, str)]
    if action_id not in action_ids:
        action_ids.append(action_id)
    payload["action_ids"] = sorted(action_ids)
    save_index(run_root, payload)


def load_action(run_root: Path, action_id: str) -> Dict[str, Any]:
    payload = read_structured(action_file(run_root, action_id))
    if not payload:
        raise FileNotFoundError(f"Missing action record: {action_id}")
    return payload


def save_action(run_root: Path, payload: Dict[str, Any]) -> None:
    action_id = str(payload.get("action_id", "")).strip()
    if not action_id:
        raise ValueError("Action payload missing action_id")
    register_action(run_root, action_id)
    write_structured(action_file(run_root, action_id), payload)


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def tail_text(path: Path, tail_lines: int) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if tail_lines <= 0:
        return ""
    return "\n".join(lines[-tail_lines:])


def signal_hit(text: str, signal_text: str) -> bool:
    return bool(signal_text and signal_text in text)


def followup_action_for_status(status: str, progress_changed: bool) -> str:
    if status == "completed":
        return "collect-results"
    if status == "failed":
        return "diagnose-failure"
    if status == "stalled":
        return "diagnose-stall"
    if progress_changed:
        return "continue-watch"
    return "wait-and-poll"


def reconcile_action(payload: Dict[str, Any], tail_lines: int = 20) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    record = dict(payload)
    now = utc_now()
    previous_status = str(record.get("status", "pending"))
    status = previous_status
    poll_interval_seconds = int(record.get("poll_interval_seconds", 120) or 120)
    previous_log_tail = str(record.get("last_log_tail", ""))
    previous_heartbeat = str(record.get("last_heartbeat", ""))
    log_path = Path(str(record.get("log_path", "")).strip()) if str(record.get("log_path", "")).strip() else None
    log_tail = tail_text(log_path, tail_lines) if log_path else ""
    success_signal = str(record.get("success_signal", "")).strip()
    failure_signal = str(record.get("failure_signal", "")).strip()
    pid = record.get("pid")

    alive = False
    if isinstance(pid, int) and pid > 0:
        alive = pid_alive(pid)

    if signal_hit(log_tail, failure_signal):
        status = "failed"
    elif signal_hit(log_tail, success_signal):
        status = "completed"
    elif alive:
        status = "running"
    elif status in FINAL_ACTION_STATES:
        status = status
    elif pid:
        status = "stalled"

    record["status"] = status
    record["last_poll_at"] = now
    if log_path and log_path.exists():
        record["last_heartbeat"] = datetime.fromtimestamp(log_path.stat().st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat()
    elif alive:
        record["last_heartbeat"] = now

    progress_changed = log_tail != previous_log_tail or str(record.get("last_heartbeat", "")) != previous_heartbeat
    next_interval = int(record.get("poll_interval_seconds", poll_interval_seconds) or poll_interval_seconds)
    record["poll_interval_seconds"] = max(next_interval, 1)
    status_changed = status != previous_status
    followup_action = followup_action_for_status(status, progress_changed)

    if status in ACTIVE_ACTION_STATES:
        record["next_poll_at"] = next_poll_timestamp(record["poll_interval_seconds"])
    else:
        record["next_poll_at"] = ""

    record["last_log_tail"] = log_tail
    summary = {
        "action_id": record.get("action_id", ""),
        "status": status,
        "pid": pid,
        "alive": alive,
        "status_changed": status_changed,
        "progress_changed": progress_changed,
        "followup_action": followup_action,
        "poll_interval_seconds": record["poll_interval_seconds"],
        "next_poll_at": record.get("next_poll_at", ""),
        "log_path": str(log_path) if log_path else "",
        "last_log_tail": log_tail,
    }
    return record, summary


def action_due(payload: Dict[str, Any], now: datetime | None = None) -> bool:
    if str(payload.get("status", "")) not in ACTIVE_ACTION_STATES:
        return False
    next_poll_at = str(payload.get("next_poll_at", "")).strip()
    if not next_poll_at:
        return True
    current = now or datetime.now(timezone.utc)
    return parse_iso(next_poll_at) <= current


def load_working_state(run_root: Path) -> Dict[str, Any]:
    working_state = read_structured(run_root / "working" / "state.yaml")
    todo_state = read_structured(run_root / "working" / "todo.yaml")
    return {
        "state": working_state,
        "todo": todo_state,
    }
