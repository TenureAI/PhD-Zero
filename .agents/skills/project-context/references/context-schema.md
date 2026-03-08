# Project Context Schema (V3)

Context is split into two JSON files under:

- `<project-root>/.project_local/<project_slug>/context.json`
- `<project-root>/.project_local/<project_slug>/secrets.json`

This schema is for runtime context only. Heavy runtime artifacts stay under:

- `<runtime_project_root>/runs/<run_id>/...`

## Non-sensitive (`context.json`)

```json
{
  "schema_version": 3,
  "project": {
    "slug": "vision-sft-v2",
    "name": "vision-sft-v2"
  },
  "system": {
    "hostname": "node-a01",
    "username": "alice"
  },
  "execution": {
    "execution_target": "remote",
    "local_project_root": "/Users/alice/work/vision-sft-v2",
    "runtime_project_root": "/data/projects/vision-sft-v2",
    "runtime_output_root": "/data/projects/vision-sft-v2/runs",
    "runtime_host": "train-gateway-01",
    "python_path": "/opt/conda/bin/python",
    "conda_env": "train",
    "venv": ""
  },
  "cluster": {
    "name": "h100-prod",
    "scheduler": "slurm",
    "queue": "train",
    "gpu_type": "H100"
  },
  "memory": {
    "shared_repo": {
      "enabled": true,
      "path": "/Users/alice/work/open-research-memory",
      "url": "https://github.com/TenureAI/open-research-memory",
      "branch": "main",
      "mode": "readonly-source",
      "sync_policy": "minimal",
      "auto_clone_if_missing": false
    }
  },
  "tracking": {
    "run_notes": ""
  },
  "updated_at": "2026-03-04T09:00:00Z"
}
```

## Sensitive (`secrets.json`)

```json
{
  "schema_version": 3,
  "api": {
    "endpoint": "https://internal-gateway.example.com",
    "key": "<redacted>"
  },
  "network": {
    "proxy": "http://proxy.local:7890"
  },
  "auth": {
    "ssh_jump_host": "jump.internal"
  },
  "updated_at": "2026-03-04T09:00:00Z"
}
```

## Task-Type Required Fields (Default)

For all task types:

- `execution.execution_target`
- `execution.local_project_root`

Task-specific additions:

- `generic`: none
- `report`:
  - `project.name`
- `sft`:
  - `execution.runtime_project_root`
  - `cluster.name`
  - `cluster.scheduler`
  - `cluster.queue`
- `rl`:
  - `execution.runtime_project_root`
  - `cluster.name`
  - `cluster.scheduler`
  - `cluster.queue`
  - `cluster.gpu_type`
- `eval`:
  - `execution.runtime_project_root`
  - `cluster.name`

Conditional rule:

- if `execution.execution_target=remote`, require `execution.runtime_host`

You can append per-run requirements via CLI flags:

- `--require key.path`
- `--require-secret key.path`

## Snapshot Contract

Each run should freeze an immutable runtime snapshot:

- `<project-root>/.project_local/<project_slug>/runs/<run_id>/runtime_snapshot.json`

Snapshot payload:

```json
{
  "schema_version": 3,
  "run_id": "20260304_090000-vision-sft-v2",
  "task_type": "sft",
  "context": {"...": "..."},
  "secrets_redacted": {"...": "***"},
  "created_at": "2026-03-04T09:00:00Z"
}
```

## Shared Memory Source Fields

Store shared-memory source configuration in `context.json` so the user is not re-prompted every run:

- `memory.shared_repo.enabled`
- `memory.shared_repo.path`
- `memory.shared_repo.url`
- `memory.shared_repo.branch`
- `memory.shared_repo.mode`
- `memory.shared_repo.sync_policy`
- `memory.shared_repo.auto_clone_if_missing`

Recommended semantics:

- `mode=readonly-source`
- `sync_policy=minimal`
- ask the user for `memory.shared_repo.path` when shared retrieval/export is first needed
- do not hardcode machine-specific paths into prompts or skills

## Legacy Compatibility

Legacy field:

- `execution.workspace_root`

When present, map to:

- `execution.local_project_root`
- `execution.runtime_project_root` (if missing)

## Legacy Layout Migration

Legacy path:

- `<project-root>/.project_local/projects/<project_slug>/...`

Migrate to new layout:

```bash
python3 .agents/skills/project-context/scripts/project_context.py migrate-layout --project-root . --clean-empty
```
