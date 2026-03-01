---
name: run-governor
description: Govern run-level execution policy for AI research tasks, including interaction mode selection, run_id creation, directory layout, stage reporting, and per-run safety allowances. Use when starting or switching a research run, defining how often to ask the user, handling high-resource actions, or deciding whether to continue within the same run vs start a new run.
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
3. If mode selection is pending for 30+ minutes, default to `moderate`.
4. After mode is selected, do not auto-continue after confirmation timeouts in non-`full-auto` modes.

## Run Identity and Directories

Use one run identifier:

- `run_id = <YYYYMMDD_HHMMSS>-<query-slug>`

Create and maintain:

1. Control logs and reports:
   - `<codex-cwd>/logs/runs/<run_id>/`
2. Per-project execution outputs:
   - `<project-root>/runs/<run_id>/`

Do not mirror project artifacts back to Codex logs by default.

## Run Files

Maintain these files in `<codex-cwd>/logs/runs/<run_id>/`:

1. `run_policy.yaml`
   - mode
   - high-resource heuristic bands
   - safety policy notes
   - per-run action allowances
2. `run_manifest.yaml`
   - primary project root
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
4. `Paths`: affected control/output paths
5. `Next`: next actionable step
