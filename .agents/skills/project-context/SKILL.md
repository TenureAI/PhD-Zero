---
name: project-context
description: |-
  Initialize and maintain per-project runtime context (env, secrets, snapshots). Prefer invoking via research-workflow.
  TRIGGER when: new run needs env setup, preflight before experiment/eval, runtime fields missing (paths, API keys, GPU config, proxy), run snapshot needed, or shared-memory needs project config.
  DO NOT TRIGGER when: pure research (use deep-research), plan-only (use research-plan), or env already fully resolved.
---

# Project Context

## Mission

Provide a reusable, private-by-default context layer for each project so environment information is collected once, reused across runs, and safely isolated from git history.

Scope boundary:

1. manages runtime context and secrets only
2. does not store heavy experiment artifacts (checkpoints, dataset caches, large logs)
3. stores per-project shared-memory source configuration, but not shared-memory records

## Trigger

Use this skill when any of these are needed:

1. first-time project environment bootstrap
2. preflight checks before experiment/report/eval execution
3. missing runtime fields during task execution
4. per-run context snapshot for reproducibility
5. first use of shared-memory retrieval or export for a project

## Private Directory Contract

Store all local runtime state under project root:

- `<project-root>/.project_local/<project_slug>/context.json`
- `<project-root>/.project_local/<project_slug>/secrets.json`
- `<project-root>/.project_local/<project_slug>/runs/<run_id>/runtime_snapshot.json`

Rules:

1. `.project_local/` must be in `.gitignore`.
2. `context.json` is non-sensitive.
3. `secrets.json` is sensitive and must never be logged verbatim.
4. If multiple projects share one orchestration repo, isolate by `project_slug`.
5. Initialize `.gitignore` if missing and append `.project_local/` if absent.

## Incremental Collection Policy

Do not ask for all fields at once.

1. infer task type (`report|sft|rl|eval|generic`)
2. load existing `context.json` + `secrets.json`
3. auto-detect non-sensitive environment values where possible
4. if execution target is `remote`, consume reuse decision from `run-governor` first; ask only if decision is missing
5. ask only for missing required fields for the current task
6. during execution, allow blocker-only delta prompts (e.g. missing API URL/key)
7. persist immediately for reuse
8. when shared-memory retrieval/export is needed, ask the user where the local shared-memory repo should live if `memory.shared_repo.path` is missing

If new missing fields appear later, run preflight again and collect only deltas.

## Security Policy

1. set `<project-root>/.project_local` and subdirectories to `0700`
2. set `secrets.json` to `0600`
3. redact sensitive keys in all CLI output (`***`)
4. never place secret content in stage reports or commit messages

## Run Integration

Recommended order in research execution:

1. `run-governor` collects and confirms mode + `local|remote` target
2. `run-governor` initializes `run_id`
3. `project-context` preflight resolves runtime context and consumes remote reuse decision
4. `experiment-execution` runs with resolved context
5. `project-context` snapshot writes run-scoped frozen context
6. shared-memory retrieval/export reuses `memory.shared_repo.*` from `context.json`

## Script

Use helper script:

- `scripts/project_context.py`

Examples:

```bash
python3 .agents/skills/project-context/scripts/project_context.py preflight \
  --project-root . \
  --project-slug my-sft-project \
  --task-type sft \
  --run-id 20260303_130000-my-sft-project
```

```bash
python3 .agents/skills/project-context/scripts/project_context.py preflight \
  --project-root . \
  --project-slug my-sft-project \
  --task-type generic \
  --require memory.shared_repo.path
```

```bash
python3 .agents/skills/project-context/scripts/project_context.py show \
  --project-root . \
  --project-slug my-sft-project
```

```bash
python3 .agents/skills/project-context/scripts/project_context.py migrate-layout \
  --project-root . \
  --clean-empty
```

## Required Output for Operations

For each operation, emit:

1. `Project`: root and slug
2. `Action`: preflight/show/snapshot
3. `State`: loaded + newly collected fields
4. `Paths`: local/context/secrets/snapshot/runtime/shared-memory paths
5. `Missing`: unresolved required fields (if any)
