# Memory Layout (v0)

Use this directory layout in a workspace:

```text
workspace/
  AGENTS.md
  config/
    persona.yaml
  .agent/
    memory.db
    runs/
      run_<id>/
        working_state.json
        action_log.jsonl
        observations.jsonl
  memory/
    episodes/
      2026/
    procedures/
      draft/
      active/
      deprecated/
    insights/
      draft/
      active/
      deprecated/
  shared_export/
```

## Notes
1. Store narrative memory records as markdown with frontmatter.
2. Store indexing and lifecycle state in SQLite (`.agent/memory.db`).
3. Keep run-scoped logs under `.agent/runs/` and do not export them directly.
