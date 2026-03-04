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

<runtime_project_root>/runs/<run_id>/
  logs/
  checkpoints/
  artifacts/
  metrics/

<local_project_root>/.project_local/<project_slug>/
  context.json
  secrets.json
  runs/<run_id>/runtime_snapshot.json
```

Notes:
1. Keep control records and stage reports under Codex logs.
2. Keep heavy experiment outputs under runtime project run directories.
3. Keep run_id consistent across control, runtime output, and snapshot paths.
4. In local execution, `runtime_project_root` can equal `local_project_root`.
5. In remote execution, `runtime_project_root` should be remote and explicit.
