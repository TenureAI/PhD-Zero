# Run Layout

Use this layout for each research run.

```text
<codex-cwd>/logs/runs/<run_id>/
  run_policy.yaml
  run_manifest.yaml
  working/
    state.yaml
    todo.yaml
  reports/
    index.md
    stage-01-<slug>.md
    stage-02-<slug>.md
    ...

<project-root>/runs/<run_id>/
  logs/
  checkpoints/
  artifacts/
  metrics/
```

Notes:
1. Keep control records and stage reports under Codex logs.
2. Keep heavy experiment outputs under project run directories.
3. Keep run_id consistent across all paths.
