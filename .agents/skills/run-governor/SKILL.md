---
name: run-governor
description: >-
  Govern run-level execution policy for AI research tasks, including interaction mode selection, run_id creation, directory layout, stage reporting, and per-run safety allowances. Use when starting or switching a research run, defining how often to ask the user, handling high-resource actions, or deciding whether to continue within the same run vs start a new run.
  TRIGGER when starting any non-trivial research task (to set mode and run_id), when switching execution targets (local/remote), when a new run needs to be created, or when stage reporting or mode-aware policy decisions are needed.
  DO NOT TRIGGER for trivial single-step tasks, for pure information queries, or when a run is already initialized and no mode/policy change is needed.
---

# Run Governor

## Mission

Set and enforce run-level execution policy so research runs stay consistent, auditable, and mode-aware.

## Mode Selection Policy

At the start of a research run, ask the user to choose one mode:

1. `full-auto`
   - Minimize user interruptions.
   - Ask only for hard blockers or major safety risks.
2. `moderate` (recommended)
   - Confirm during plan finalization.
   - Confirm before high-resource actions.
3. `detailed`
   - Ask when path is unclear.
   - Ask before high-resource actions.

Additional rules:

1. If the user explicitly asks to switch mode, switch immediately.
2. If the user says "just do it" or equivalent, treat as a temporary switch to `full-auto` behavior.
3. If mode selection is pending, keep the run in `pending-confirmation` and do not initialize run artifacts.
4. Never auto-default mode from timeout. A mode must be explicitly confirmed by the user before initialization.
5. After mode is selected, do not auto-continue after confirmation timeouts in non-`full-auto` modes.

## Interaction Transport Policy

For user confirmations required by run initialization:

1. Route confirmation requests through `human-checkpoint`.
2. In `moderate` or `detailed`, prefer built-in user-question tool (`request_user_input`).
3. If built-in tool is unavailable, degrade to concise plain-text questions.
4. Record the channel as `interaction_transport=request_user_input|plain-text-fallback`.

## Execution Target Bootstrap

During run initialization, decide execution target before planning launch steps:

1. ask whether this run executes on `local` or `remote`
2. if `remote`, load existing remote fields from `project-context`
3. ask user whether to reuse stored remote fields for this run
4. if not reused or incomplete, collect only missing remote-required fields
5. persist the final decision and resolved paths into run manifest and project-context
6. if shared-memory retrieval/export is in scope, persist resolved shared repo metadata from `project-context` into the run manifest

Remote-required fields:

1. `execution.runtime_host`
2. `execution.runtime_project_root`
3. `cluster.scheduler` when scheduler-based launch is selected

Mode rules:

1. `full-auto`: if stored remote fields are complete, reuse by default; ask only on hard blockers.
2. `moderate` and `detailed`: explicitly confirm reuse choice.

## Mandatory Human Confirmation Gate

Before creating any run files or directories, collect and confirm both fields from the user:

1. `user_confirmed_mode` in `{full-auto|moderate|detailed}`
2. `user_confirmed_execution_target` in `{local|remote}`

Hard constraints:

1. If either confirmation is missing, mark status `blocked-awaiting-user-confirmation`.
2. While blocked, do not create `run_id`, run directories, manifests, policy files, working files, reports, or runtime snapshots.
3. `moderate` is only a recommendation label and cannot be applied unless user-confirmed.
4. For `moderate` or `detailed`, ask via built-in question tool first; if unavailable, use plain-text fallback.
5. If user asks to proceed without specifying values, ask a direct clarification question and remain blocked.
6. Confirmation collection must be mediated by `human-checkpoint`.
7. Any assumption for mode/target is non-compliant, even when likely.

## Memory Bootstrap Gate

Before transitioning from initialization to execution workflow:

1. Set `memory_policy=balanced-triggered` unless user explicitly overrides.
2. Ensure one `memory-manager` bootstrap operation is complete:
   - `retrieve` or `init-working` for current project/task context.
3. If bootstrap is missing, mark status `blocked-awaiting-memory-bootstrap`.
4. This gate enforces only the bootstrap, not per-step memory writes.

## Run Identity and Directories

Use one run identifier:

- `run_id = <YYYYMMDD_HHMMSS>-<query-slug>`

Prerequisite:

1. `run_id` creation is allowed only after `user_confirmed_mode` and `user_confirmed_execution_target` are present.

Create and maintain:

1. Control logs and reports:
   - `<codex-cwd>/logs/runs/<run_id>/`
2. Runtime execution outputs:
   - `<runtime_project_root>/runs/<run_id>/`
3. Project context state:
   - `<local_project_root>/.project_local/<project_slug>/`

Do not mirror heavy runtime artifacts back to local logs by default.

## Run Files

Maintain these files in `<codex-cwd>/logs/runs/<run_id>/`:

1. `run_policy.yaml`
   - mode
   - high-resource heuristic bands
   - safety policy notes
   - per-run action allowances
2. `run_manifest.yaml`
   - local project root
   - runtime project root
   - runtime output root
   - execution target (`local|remote`)
   - runtime host (if remote)
   - shared memory repo path/url/branch/sync policy when configured
   - optional additional project roots
   - output directory mapping
3. `working/state.yaml`
   - objective, current phase, hypothesis, blockers, next step
4. `working/todo.yaml`
   - `todo_active`, `todo_done`, `todo_blocked`
5. `reports/index.md`
   - stage list with status (`done|running|blocked`), file paths, and last update time

## Multi-Project and New-Topic Policy

1. Default to one run bound to one primary project.
2. Allow multiple project roots in one run only when they serve the same objective.
3. If a user request appears mostly unrelated to the current objective, ask whether to start a new run.
4. If user clearly states "new project/topic", ask to switch run.

## Safety and Allowance Policy

When a risky action is encountered, provide choices:

1. allow once
2. allow same action type for this run
3. disallow and stop
4. user-defined handling

Treat potential large file deletion as major safety risk.

In `full-auto`, do not interrupt for non-major risks. Continue and record rationale in stage reports.

## High-Resource Heuristic

Use approximate decision bands:

1. `L1` low: typically under 2 GPU-hours and under 20 USD equivalent.
2. `L2` medium: roughly 2-10 GPU-hours or 20-100 USD equivalent.
3. `L3` high: over 10 GPU-hours, over 100 USD equivalent, or long multi-node runs.

In `moderate` and `detailed`, confirm before L2/L3 actions.
In `full-auto`, proceed unless major safety risk is present.

## Stage Reporting Contract

At each stage completion:

1. Save one stage report file under `reports/`.
2. Update `reports/index.md` status and timestamp.
3. In chat, provide a detailed stage summary plus report path.
4. Do not require user reply just because a stage report was emitted.

## Required Output for Run-Governor Operations

For each run-governor action, emit:

1. `Run`: run_id and active mode
2. `Action`: initialize, switch-mode, update-policy, new-topic-check, or stage-report
3. `Decision`: what was chosen and why
4. `Execution`: local/remote choice and reuse decision
5. `Paths`: affected control/output/context paths
6. `Next`: next actionable step
7. `Confirmation`: `user_confirmed_mode`, `user_confirmed_execution_target`, and whether initialization is permitted (`YES|NO`)
8. `Compliance`: `gate_status=pass|blocked`, with blocked reason when applicable
9. `Interaction`: `interaction_transport` and optional `fallback_reason`
10. `Memory`: `memory_policy` and `memory_bootstrap_done=YES|NO`

## Violation Recovery Policy

If initialization occurred before required confirmation:

1. Immediately acknowledge non-compliance.
2. Ask whether to keep or clean the created artifacts.
3. Do not continue execution until user re-confirms `mode` and `execution_target`.
4. Record the incident and recovery choice in the next stage report.
