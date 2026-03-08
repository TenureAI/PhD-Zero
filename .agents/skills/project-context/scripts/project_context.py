#!/usr/bin/env python3
"""Project context bootstrap and preflight helper.

Stores per-project runtime context under:
  .project_local/<project_slug>/
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import platform
import shutil
import subprocess
import sys
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

SCHEMA_VERSION = 3

DEFAULT_SHARED_MEMORY_URL = "https://github.com/TenureAI/open-research-memory"
DEFAULT_SHARED_MEMORY_BRANCH = "main"
DEFAULT_SHARED_MEMORY_MODE = "readonly-source"
DEFAULT_SHARED_MEMORY_SYNC_POLICY = "minimal"

TASK_REQUIRED_FIELDS = {
    "generic": ["execution.execution_target", "execution.local_project_root"],
    "report": ["project.name", "execution.execution_target", "execution.local_project_root"],
    "sft": [
        "cluster.name",
        "cluster.scheduler",
        "cluster.queue",
        "execution.execution_target",
        "execution.local_project_root",
        "execution.runtime_project_root",
    ],
    "rl": [
        "cluster.name",
        "cluster.scheduler",
        "cluster.queue",
        "cluster.gpu_type",
        "execution.execution_target",
        "execution.local_project_root",
        "execution.runtime_project_root",
    ],
    "eval": [
        "cluster.name",
        "execution.execution_target",
        "execution.local_project_root",
        "execution.runtime_project_root",
    ],
}

SECRET_DEFAULTS = ["api.endpoint", "api.key", "network.proxy", "auth.ssh_jump_host"]

PROMPTS = {
    "project.name": "Project name",
    "execution.execution_target": "Execution target (local/remote)",
    "execution.local_project_root": "Local project root path",
    "execution.runtime_project_root": "Runtime project root path",
    "execution.runtime_output_root": "Runtime output root path",
    "execution.runtime_host": "Runtime host",
    "execution.workspace_root": "Workspace root path",
    "memory.shared_repo.path": "Local shared memory repo path",
    "memory.shared_repo.url": "Shared memory repo URL",
    "memory.shared_repo.branch": "Shared memory branch",
    "cluster.name": "Cluster name",
    "cluster.scheduler": "Scheduler (e.g. slurm/k8s/ray/local)",
    "cluster.queue": "Cluster queue/partition",
    "cluster.gpu_type": "GPU type (e.g. H100/A100/4090)",
    "api.endpoint": "API endpoint URL",
    "api.key": "API key",
    "network.proxy": "Proxy URL/path",
    "auth.ssh_jump_host": "SSH jump host",
}


@dataclass
class ProjectPaths:
    root: Path
    slug: str

    @property
    def private_root(self) -> Path:
        return self.root / ".project_local"

    @property
    def project_root(self) -> Path:
        return self.private_root / self.slug

    @property
    def context_path(self) -> Path:
        return self.project_root / "context.json"

    @property
    def secrets_path(self) -> Path:
        return self.project_root / "secrets.json"

    def snapshot_path(self, run_id: str) -> Path:
        return self.project_root / "runs" / run_id / "runtime_snapshot.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    out = []
    for ch in value.strip().lower():
        if ch.isalnum() or ch in {"-", "_"}:
            out.append(ch)
        elif ch in {" ", "/", "."}:
            out.append("-")
    slug = "".join(out).strip("-")
    return slug or "project"


def nested_get(data: Dict[str, Any], dotted_key: str) -> Any:
    cur: Any = data
    for key in dotted_key.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def nested_set(data: Dict[str, Any], dotted_key: str, value: Any) -> None:
    cur = data
    keys = dotted_key.split(".")
    for key in keys[:-1]:
        nxt = cur.get(key)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[key] = nxt
        cur = nxt
    cur[keys[-1]] = value


def deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(dst.get(key), dict):
            deep_merge(dst[key], value)
        else:
            dst[key] = value
    return dst


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: Dict[str, Any], mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=True, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)
    os.chmod(path, mode)


def ensure_private_layout(paths: ProjectPaths) -> None:
    for directory in [paths.private_root, paths.project_root]:
        directory.mkdir(parents=True, exist_ok=True)
        os.chmod(directory, 0o700)


def ensure_gitignore_rule(project_root: Path) -> bool:
    gitignore = project_root / ".gitignore"
    rule = ".project_local/"
    existing = []
    if gitignore.exists():
        with gitignore.open("r", encoding="utf-8") as f:
            existing = f.read().splitlines()
    normalized = {line.strip() for line in existing}
    if rule in normalized or ".project_local" in normalized:
        return False

    if existing and existing[-1].strip() != "":
        existing.append("")
    existing.append(rule)
    payload = "\n".join(existing) + "\n"
    with gitignore.open("w", encoding="utf-8") as f:
        f.write(payload)
    return True


def cmd_output(parts: List[str]) -> str:
    if not shutil.which(parts[0]):
        return ""
    try:
        output = subprocess.check_output(parts, stderr=subprocess.DEVNULL, text=True, timeout=2)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return ""
    return output.strip()


def normalize_context_layout(context: Dict[str, Any], project_root: Path) -> List[str]:
    updated: List[str] = []
    resolved_root = str(project_root.resolve())

    def set_if_missing(key: str, value: str) -> None:
        if value in ("", None):
            return
        if nested_get(context, key) in (None, ""):
            nested_set(context, key, value)
            updated.append(key)

    workspace_root = nested_get(context, "execution.workspace_root")
    local_root = nested_get(context, "execution.local_project_root")
    if workspace_root and (local_root in (None, "") or str(local_root) == resolved_root):
        if str(local_root) != str(workspace_root):
            nested_set(context, "execution.local_project_root", str(workspace_root))
            updated.append("execution.local_project_root")

    set_if_missing("execution.local_project_root", resolved_root)

    target = nested_get(context, "execution.execution_target")
    if isinstance(target, str):
        normalized = target.strip().lower()
        if normalized != target:
            nested_set(context, "execution.execution_target", normalized)
            updated.append("execution.execution_target")
        target = normalized
    if target not in {"local", "remote"}:
        nested_set(context, "execution.execution_target", "local")
        updated.append("execution.execution_target")

    local_root = nested_get(context, "execution.local_project_root")
    runtime_root = nested_get(context, "execution.runtime_project_root")
    target = nested_get(context, "execution.execution_target")
    if target == "local" and runtime_root in (None, "") and local_root not in (None, ""):
        nested_set(context, "execution.runtime_project_root", str(local_root))
        updated.append("execution.runtime_project_root")

    local_root = nested_get(context, "execution.local_project_root")
    set_if_missing("execution.workspace_root", str(local_root))

    runtime_root = nested_get(context, "execution.runtime_project_root")
    runtime_output_root = nested_get(context, "execution.runtime_output_root")
    if runtime_root not in (None, "") and runtime_output_root in (None, ""):
        nested_set(context, "execution.runtime_output_root", str(Path(str(runtime_root)) / "runs"))
        updated.append("execution.runtime_output_root")

    def normalize_bool(key: str, default: bool) -> None:
        value = nested_get(context, key)
        if value in (None, ""):
            nested_set(context, key, default)
            updated.append(key)
            return
        if isinstance(value, bool):
            return
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "y", "on"}:
                nested_set(context, key, True)
                updated.append(key)
            elif lowered in {"0", "false", "no", "n", "off"}:
                nested_set(context, key, False)
                updated.append(key)

    set_if_missing("memory.shared_repo.url", DEFAULT_SHARED_MEMORY_URL)
    set_if_missing("memory.shared_repo.branch", DEFAULT_SHARED_MEMORY_BRANCH)
    set_if_missing("memory.shared_repo.mode", DEFAULT_SHARED_MEMORY_MODE)
    set_if_missing("memory.shared_repo.sync_policy", DEFAULT_SHARED_MEMORY_SYNC_POLICY)
    normalize_bool("memory.shared_repo.enabled", False)
    normalize_bool("memory.shared_repo.auto_clone_if_missing", False)

    shared_path = nested_get(context, "memory.shared_repo.path")
    if isinstance(shared_path, str):
        normalized_path = shared_path.strip()
        if normalized_path != shared_path:
            nested_set(context, "memory.shared_repo.path", normalized_path)
            updated.append("memory.shared_repo.path")
        shared_path = normalized_path
    if shared_path not in (None, "") and nested_get(context, "memory.shared_repo.enabled") is False:
        nested_set(context, "memory.shared_repo.enabled", True)
        updated.append("memory.shared_repo.enabled")

    return updated


def detect_context(project_slug: str, project_root: Path) -> Dict[str, Any]:
    context: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "slug": project_slug,
            "name": project_slug,
        },
        "system": {
            "hostname": platform.node() or os.environ.get("HOSTNAME", ""),
            "username": getpass.getuser(),
        },
        "execution": {
            "python_path": sys.executable,
            "local_project_root": str(project_root.resolve()),
        },
        "memory": {
            "shared_repo": {
                "enabled": False,
                "url": DEFAULT_SHARED_MEMORY_URL,
                "branch": DEFAULT_SHARED_MEMORY_BRANCH,
                "mode": DEFAULT_SHARED_MEMORY_MODE,
                "sync_policy": DEFAULT_SHARED_MEMORY_SYNC_POLICY,
                "auto_clone_if_missing": False,
            }
        },
    }

    conda_env = os.environ.get("CONDA_DEFAULT_ENV", "")
    if conda_env:
        nested_set(context, "execution.conda_env", conda_env)
    venv = os.environ.get("VIRTUAL_ENV", "")
    if venv:
        nested_set(context, "execution.venv", venv)

    cuda_visible = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    if cuda_visible:
        nested_set(context, "cluster.cuda_visible_devices", cuda_visible)

    hostname = cmd_output(["hostname"])
    if hostname and not nested_get(context, "system.hostname"):
        nested_set(context, "system.hostname", hostname)

    return context


def detect_secrets() -> Dict[str, Any]:
    secrets: Dict[str, Any] = {"schema_version": SCHEMA_VERSION}
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        nested_set(secrets, "network.proxy", proxy)
    endpoint = os.environ.get("OPENAI_BASE_URL") or os.environ.get("API_ENDPOINT")
    if endpoint:
        nested_set(secrets, "api.endpoint", endpoint)
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY")
    if key:
        nested_set(secrets, "api.key", key)
    return secrets


def collect_missing(
    payload: Dict[str, Any],
    required_fields: Iterable[str],
    non_interactive: bool,
    secret_mode: bool,
) -> Tuple[List[str], List[str]]:
    added: List[str] = []
    missing: List[str] = []
    for key in required_fields:
        existing = nested_get(payload, key)
        if existing not in (None, ""):
            continue
        if non_interactive:
            missing.append(key)
            continue
        prompt = PROMPTS.get(key, f"Value for {key}")
        if secret_mode:
            value = getpass.getpass(prompt + ": ")
        else:
            value = input(prompt + ": ").strip()
        if value:
            nested_set(payload, key, value)
            added.append(key)
        else:
            missing.append(key)
    return added, missing


def redact_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    redacted = deepcopy(payload)

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                kl = k.lower()
                if any(tag in kl for tag in ["key", "token", "secret", "password"]):
                    out[k] = "***"
                else:
                    out[k] = walk(v)
            return out
        if isinstance(node, list):
            return [walk(x) for x in node]
        return node

    return walk(redacted)


def parse_kv_pairs(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid --set/--secret format: {pair}. Use key.path=value")
        k, v = pair.split("=", 1)
        key = k.strip()
        if not key:
            raise ValueError(f"Invalid empty key in pair: {pair}")
        out[key] = v.strip()
    return out


def apply_overrides(payload: Dict[str, Any], overrides: Dict[str, str]) -> List[str]:
    updated: List[str] = []
    for key, value in overrides.items():
        if value:
            nested_set(payload, key, value)
            updated.append(key)
    return updated


def conditional_required_fields(context: Dict[str, Any]) -> List[str]:
    target = nested_get(context, "execution.execution_target")
    if target == "remote":
        return ["execution.runtime_project_root", "execution.runtime_host"]
    return []


def preflight(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    project_slug = args.project_slug or slugify(project_root.name)
    paths = ProjectPaths(root=project_root, slug=project_slug)
    ensure_private_layout(paths)
    gitignore_updated = ensure_gitignore_rule(project_root)

    context = deep_merge(detect_context(project_slug, project_root), read_json(paths.context_path))
    secrets = deep_merge(detect_secrets(), read_json(paths.secrets_path))

    context_overrides = parse_kv_pairs(args.set or [])
    secret_overrides = parse_kv_pairs(args.secret or [])

    updated_context = apply_overrides(context, context_overrides)
    updated_secrets = apply_overrides(secrets, secret_overrides)
    updated_context.extend(normalize_context_layout(context, project_root))

    required_context = list(TASK_REQUIRED_FIELDS[args.task_type]) + list(args.require)
    for key in conditional_required_fields(context):
        if key not in required_context:
            required_context.append(key)

    required_secrets = list(args.require_secret)
    # If the task appears remote/cluster heavy, keep default secret keys ready.
    if args.task_type in {"sft", "rl", "eval"}:
        for key in SECRET_DEFAULTS:
            if key not in required_secrets:
                required_secrets.append(key)

    added_ctx, missing_ctx = collect_missing(
        context,
        required_context,
        non_interactive=args.non_interactive,
        secret_mode=False,
    )
    added_sec, missing_sec = collect_missing(
        secrets,
        required_secrets,
        non_interactive=args.non_interactive,
        secret_mode=True,
    )
    updated_context.extend(normalize_context_layout(context, project_root))

    context["schema_version"] = SCHEMA_VERSION
    context["updated_at"] = utc_now()
    secrets["schema_version"] = SCHEMA_VERSION
    secrets["updated_at"] = utc_now()

    write_json(paths.context_path, context, 0o600)
    write_json(paths.secrets_path, secrets, 0o600)

    snapshot_path = ""
    if args.run_id:
        snapshot = {
            "schema_version": SCHEMA_VERSION,
            "run_id": args.run_id,
            "task_type": args.task_type,
            "context": context,
            "secrets_redacted": redact_payload(secrets),
            "created_at": utc_now(),
        }
        spath = paths.snapshot_path(args.run_id)
        write_json(spath, snapshot, 0o600)
        if spath.parent.parent.exists():
            os.chmod(spath.parent.parent, 0o700)
        os.chmod(spath.parent, 0o700)
        snapshot_path = str(spath)

    print(f"Project: root={project_root} slug={project_slug}")
    print("Action: preflight")
    print(
        "State: "
        + json.dumps(
            {
                "task_type": args.task_type,
                "updated_context_fields": sorted(set(updated_context + added_ctx)),
                "updated_secret_fields": sorted(set(updated_secrets + added_sec)),
                "gitignore_updated": gitignore_updated,
            },
            ensure_ascii=True,
        )
    )
    print(
        "Paths: "
        + json.dumps(
            {
                "context": str(paths.context_path),
                "secrets": str(paths.secrets_path),
                "snapshot": snapshot_path,
                "local_project_root": str(nested_get(context, "execution.local_project_root") or ""),
                "runtime_project_root": str(nested_get(context, "execution.runtime_project_root") or ""),
                "runtime_output_root": str(nested_get(context, "execution.runtime_output_root") or ""),
                "shared_memory_repo_path": str(nested_get(context, "memory.shared_repo.path") or ""),
                "shared_memory_repo_url": str(nested_get(context, "memory.shared_repo.url") or ""),
            },
            ensure_ascii=True,
        )
    )
    print(
        "Missing: "
        + json.dumps(
            {
                "context": missing_ctx,
                "secrets": missing_sec,
            },
            ensure_ascii=True,
        )
    )

    return 2 if (missing_ctx or missing_sec) else 0


def show(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    project_slug = args.project_slug or slugify(project_root.name)
    paths = ProjectPaths(root=project_root, slug=project_slug)

    context = read_json(paths.context_path)
    secrets = read_json(paths.secrets_path)
    print(f"Project: root={project_root} slug={project_slug}")
    print("Action: show")
    print("Context:")
    print(json.dumps(context, ensure_ascii=True, indent=2, sort_keys=True))
    print("Secrets(redacted):")
    print(json.dumps(redact_payload(secrets), ensure_ascii=True, indent=2, sort_keys=True))
    return 0


def snapshot(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    project_slug = args.project_slug or slugify(project_root.name)
    paths = ProjectPaths(root=project_root, slug=project_slug)

    if not args.run_id:
        raise ValueError("--run-id is required for snapshot")

    context = read_json(paths.context_path)
    secrets = read_json(paths.secrets_path)
    if not context and not secrets:
        print("No context found. Run preflight first.", file=sys.stderr)
        return 2

    payload = {
        "schema_version": SCHEMA_VERSION,
        "run_id": args.run_id,
        "task_type": args.task_type,
        "context": context,
        "secrets_redacted": redact_payload(secrets),
        "created_at": utc_now(),
    }
    out = paths.snapshot_path(args.run_id)
    write_json(out, payload, 0o600)
    if out.parent.parent.exists():
        os.chmod(out.parent.parent, 0o700)
    os.chmod(out.parent, 0o700)

    print(f"Project: root={project_root} slug={project_slug}")
    print("Action: snapshot")
    print(f"Paths: {json.dumps({'snapshot': str(out)}, ensure_ascii=True)}")
    return 0


def migrate_layout(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    private_root = project_root / ".project_local"
    legacy_root = private_root / "projects"
    if not legacy_root.exists():
        print(f"No legacy layout found at {legacy_root}")
        return 0

    migrated: List[str] = []
    skipped: List[str] = []
    failed: List[str] = []

    for item in sorted(legacy_root.iterdir()):
        if not item.is_dir():
            continue
        target = private_root / item.name
        if target.exists():
            if args.force:
                try:
                    shutil.rmtree(target)
                except OSError as exc:
                    failed.append(f"{item.name}: cannot remove existing target ({exc})")
                    continue
            else:
                skipped.append(f"{item.name}: target exists")
                continue
        try:
            os.replace(item, target)
            os.chmod(target, 0o700)
            migrated.append(item.name)
        except OSError as exc:
            failed.append(f"{item.name}: {exc}")

    if args.clean_empty:
        try:
            remaining = [x for x in legacy_root.iterdir()]
            if not remaining:
                legacy_root.rmdir()
        except OSError:
            pass

    print(f"Project: root={project_root}")
    print("Action: migrate-layout")
    print("State: " + json.dumps({"migrated": migrated, "skipped": skipped, "failed": failed}, ensure_ascii=True))
    print(
        "Paths: "
        + json.dumps(
            {"legacy_root": str(legacy_root), "new_root": str(private_root)},
            ensure_ascii=True,
        )
    )
    if failed:
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project context bootstrap helper")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument("--project-root", default=".", help="Project root path")
        p.add_argument("--project-slug", default="", help="Project slug override")

    p_pre = sub.add_parser("preflight", help="Collect and persist missing context/secrets")
    add_common_flags(p_pre)
    p_pre.add_argument(
        "--task-type",
        default="generic",
        choices=sorted(TASK_REQUIRED_FIELDS.keys()),
        help="Current task type",
    )
    p_pre.add_argument("--run-id", default="", help="Run id for optional snapshot output")
    p_pre.add_argument(
        "--non-interactive",
        action="store_true",
        help="Do not prompt; return non-zero when required fields are missing",
    )
    p_pre.add_argument(
        "--require",
        action="append",
        default=[],
        help="Additional required context key (dot notation). Repeatable.",
    )
    p_pre.add_argument(
        "--require-secret",
        action="append",
        default=[],
        help="Additional required secret key (dot notation). Repeatable.",
    )
    p_pre.add_argument(
        "--set",
        action="append",
        default=[],
        help="Set context field key.path=value before validation. Repeatable.",
    )
    p_pre.add_argument(
        "--secret",
        action="append",
        default=[],
        help="Set secret field key.path=value before validation. Repeatable.",
    )

    p_show = sub.add_parser("show", help="Show current context and redacted secrets")
    add_common_flags(p_show)

    p_snap = sub.add_parser("snapshot", help="Write a run snapshot from stored files")
    add_common_flags(p_snap)
    p_snap.add_argument("--run-id", required=True, help="Run id")
    p_snap.add_argument(
        "--task-type",
        default="generic",
        choices=sorted(TASK_REQUIRED_FIELDS.keys()),
        help="Task type to annotate snapshot",
    )

    p_migrate = sub.add_parser(
        "migrate-layout",
        help="Migrate legacy .project_local/projects/<slug> layout to .project_local/<slug>",
    )
    p_migrate.add_argument("--project-root", default=".", help="Project root path")
    p_migrate.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing .project_local/<slug> directories when conflicts occur",
    )
    p_migrate.add_argument(
        "--clean-empty",
        action="store_true",
        help="Remove empty legacy .project_local/projects directory after migration",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "preflight":
        return preflight(args)
    if args.command == "show":
        return show(args)
    if args.command == "snapshot":
        return snapshot(args)
    if args.command == "migrate-layout":
        return migrate_layout(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
