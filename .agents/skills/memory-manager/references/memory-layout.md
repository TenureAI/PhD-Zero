# Memory Layout (v1)

Use this layout during research execution:

```text
<codex-cwd>/logs/runs/<run_id>/
  working/
    state.yaml
    todo.yaml
  reports/
    index.md
    stage-*.md

<runtime_project_root>/runs/<run_id>/
  logs/
  checkpoints/
  artifacts/

<project-root>/.project_local/<project_slug>/memory/
  episodes/
  procedures/
    draft/
    active/
    deprecated/
  insights/
    draft/
    active/
    deprecated/
  index.db
```

Notes:
1. Keep working state and reports run-scoped.
2. Keep long-term memory in `.project_local/<project_slug>/memory/` plus index metadata in `index.db`.
3. Treat old `memory/` and `.agent/memory.db` layouts as legacy and migrate when touched.
4. Shared memory repos live outside `.project_local` and are treated as read-only retrieval sources, not as run-scoped state.
