#!/usr/bin/env python3
"""Write a concise working-state delta for a run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from memory_store import read_structured, utc_now, write_structured


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write working-state delta")
    parser.add_argument("--run-root", required=True, help="Path to logs/runs/<run_id>")
    parser.add_argument("--goal", default="")
    parser.add_argument("--stage", default="")
    parser.add_argument("--hypothesis", default="")
    parser.add_argument("--last-action", default="")
    parser.add_argument("--last-observation", default="")
    parser.add_argument("--next-step", default="")
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--active-action-id", action="append", default=[])
    parser.add_argument("--todo-active", action="append", default=[])
    parser.add_argument("--todo-done", action="append", default=[])
    parser.add_argument("--todo-blocked", action="append", default=[])
    return parser


def maybe_set(payload: Dict[str, object], key: str, value: str) -> None:
    if value:
        payload[key] = value


def replace_if_present(payload: Dict[str, object], key: str, values: List[str]) -> None:
    if values:
        payload[key] = values


def main() -> int:
    args = build_parser().parse_args()
    run_root = Path(args.run_root).resolve()
    state_path = run_root / "working" / "state.yaml"
    todo_path = run_root / "working" / "todo.yaml"

    state = read_structured(state_path)
    todo = read_structured(todo_path)

    maybe_set(state, "goal", args.goal)
    maybe_set(state, "stage", args.stage)
    maybe_set(state, "hypothesis", args.hypothesis)
    maybe_set(state, "last_action", args.last_action)
    maybe_set(state, "last_observation", args.last_observation)
    maybe_set(state, "next_step", args.next_step)
    replace_if_present(state, "blockers", args.blocker)
    replace_if_present(state, "evidence_refs", args.evidence_ref)
    replace_if_present(state, "active_action_ids", args.active_action_id)
    state["updated_at"] = utc_now()

    replace_if_present(todo, "todo_active", args.todo_active)
    replace_if_present(todo, "todo_done", args.todo_done)
    replace_if_present(todo, "todo_blocked", args.todo_blocked)
    todo["updated_at"] = utc_now()

    write_structured(state_path, state)
    write_structured(todo_path, todo)

    print(
        json.dumps(
            {
                "run_root": str(run_root),
                "state": state,
                "todo": todo,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
