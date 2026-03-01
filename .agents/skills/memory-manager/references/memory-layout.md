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

<project-root>/runs/<run_id>/
  logs/
  checkpoints/
  artifacts/

memory/
  episodes/
  procedures/
    draft/
    active/
    deprecated/
  insights/
    draft/
    active/
    deprecated/

.agent/
  memory.db
```

Notes:
1. Keep working state and reports run-scoped.
2. Keep long-term memory in `memory/` plus index metadata in `.agent/memory.db`.
