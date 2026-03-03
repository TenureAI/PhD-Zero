# Project Context Schema (V1)

Context is split into two JSON files under:

- `<project-root>/.project_local/<project_slug>/context.json`
- `<project-root>/.project_local/<project_slug>/secrets.json`

## Non-sensitive (`context.json`)

```json
{
  "schema_version": 1,
  "project": {
    "slug": "vision-sft-v2",
    "name": "vision-sft-v2"
  },
  "system": {
    "hostname": "node-a01",
    "username": "alice"
  },
  "execution": {
    "python_path": "/opt/conda/bin/python",
    "conda_env": "train",
    "venv": "",
    "workspace_root": "/data/projects/vision-sft-v2"
  },
  "cluster": {
    "name": "h100-prod",
    "scheduler": "slurm",
    "queue": "train",
    "gpu_type": "H100"
  },
  "tracking": {
    "run_notes": ""
  },
  "updated_at": "2026-03-03T13:00:00Z"
}
```

## Sensitive (`secrets.json`)

```json
{
  "schema_version": 1,
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
  "updated_at": "2026-03-03T13:00:00Z"
}
```

## Task-Type Required Fields (Default)

- `generic`: none
- `report`:
  - `project.name`
  - `execution.workspace_root`
- `sft`:
  - `cluster.name`
  - `cluster.scheduler`
  - `cluster.queue`
  - `execution.workspace_root`
- `rl`:
  - `cluster.name`
  - `cluster.scheduler`
  - `cluster.queue`
  - `cluster.gpu_type`
  - `execution.workspace_root`
- `eval`:
  - `cluster.name`
  - `execution.workspace_root`

You can append per-run requirements via CLI flags:

- `--require key.path`
- `--require-secret key.path`

## Snapshot Contract

Each run should freeze an immutable runtime snapshot:

- `<project-root>/.project_local/<project_slug>/runs/<run_id>/runtime_snapshot.json`

Snapshot payload:

```json
{
  "schema_version": 1,
  "run_id": "20260303_130000-vision-sft-v2",
  "task_type": "sft",
  "context": {"...": "..."},
  "secrets_redacted": {"...": "***"},
  "created_at": "2026-03-03T13:00:00Z"
}
```

## Legacy Layout Migration

Legacy path:

- `<project-root>/.project_local/projects/<project_slug>/...`

Migrate to new layout:

```bash
python .agents/skills/project-context/scripts/project_context.py migrate-layout --project-root . --clean-empty
```
