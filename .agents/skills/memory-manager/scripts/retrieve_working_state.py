#!/usr/bin/env python3
"""Read durable working state for a run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from memory_store import read_structured


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read working state for a run")
    parser.add_argument("--run-root", required=True, help="Path to logs/runs/<run_id>")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_root = Path(args.run_root).resolve()
    payload = {
        "run_root": str(run_root),
        "state": read_structured(run_root / "working" / "state.yaml"),
        "todo": read_structured(run_root / "working" / "todo.yaml"),
    }
    actions_root = run_root / "actions"
    if actions_root.exists():
        payload["active_actions"] = sorted(path.name for path in actions_root.glob("*.yaml"))
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
