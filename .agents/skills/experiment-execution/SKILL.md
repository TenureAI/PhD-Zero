---
name: experiment-execution
description: |-
  Execute AI/ML experiments locally or remotely with environment, runtime, and logging controls. Prefer invoking via research-workflow.
  TRIGGER when: user asks to run/launch/start/resume/monitor a training job, evaluation, or benchmark, or a plan is ready for execution, or experiment needs rerun/recovery.
  DO NOT TRIGGER when: research investigation only (use deep-research), planning without execution (use research-plan), or env setup without launch (use project-context).
---

# Experiment Execution

## Mission

Run experiments safely, reproducibly, and mode-aware, with clear run paths and traceable evidence.

## References

Read when needed:

1. `references/experiment-launch-checklist.md`
2. `references/remote-info-template.md`

## Required Inputs

Collect minimum safe inputs:

1. execution target (`local|remote`)
2. local project root
3. runtime project root (required when remote)
4. single-node or multi-node
5. proxy requirement
6. tracker/login requirement

Ask only missing questions.

## Run Path Policy

Use shared run_id from run-governor:

1. control logs and stage reports: `<codex-cwd>/logs/runs/<run_id>/`
2. experiment outputs: `<runtime_project_root>/runs/<run_id>/`
3. project-context snapshots and secrets: `<local_project_root>/.project_local/<project_slug>/`

In local execution, `runtime_project_root` can be equal to `local_project_root`.

## Mode-Aware Interaction

1. `full-auto`: proceed without confirmation unless hard blocker or major safety risk.
2. `moderate`: confirm before high-resource actions.
3. `detailed`: confirm for unclear plans and high-resource actions.

## Smoke Validation Policy

Use smoke validation only when needed:

1. when launch details are incomplete
2. when environment readiness is uncertain
3. when cost/risk of full run is high

If setup is clear and safe, direct execution is allowed.

## Execution Policy

1. Confirm real execution vs dry-run.
2. Confirm required inputs.
3. Inspect scripts/configs/logs as needed.
4. Resolve only blocking gaps.
5. Launch smallest valid step first when uncertainty is high.
6. Record commands, node assignments, log paths, run IDs.
7. If the launched action is long-running, immediately enter watch mode instead of treating launch as completion.
8. After each poll, continue with monitoring, diagnosis, recovery, or result collection; do not default to "job started, come back later."
9. Replan on major failures.

## Watch Mode Policy

Long-running experiment execution is an active responsibility, not a fire-and-forget step.

After launching a long-running job:

1. stay in watch mode by default
2. poll logs, checkpoints, scheduler state, or metrics on a model-chosen cadence
3. after each poll:
   - if `running`, choose the next sleep interval and continue watching
   - if `completed`, inspect outputs and continue validation/analysis
   - if `stalled`, inspect evidence, retrieve memory, and attempt recovery or replan
   - if `failed`, diagnose immediately and attempt the smallest safe recovery
4. ask the user only for hard blockers, major safety/resource approvals, or true decision points
5. only allow explicit fire-and-forget behavior when the user clearly requested it

## Watch-Loop Execution Template

Use this template after each experiment poll:

1. read `status`, `followup_action`, `progress_changed`, and `last_log_tail`
2. branch immediately:
   - `continue-watch` or `wait-and-poll`
     - choose the next sleep interval
     - keep monitoring
   - `collect-results`
     - inspect outputs, metrics, checkpoints, and artifacts
     - continue validation and analysis
   - `diagnose-stall`
     - inspect logs
     - retrieve `procedure` and `episode`
     - attempt the smallest safe recovery
   - `diagnose-failure`
     - inspect failure evidence
     - retrieve memory
     - attempt recovery or replan
   - `replan`
     - update route and continue execution
3. write working state update before the next wait or recovery attempt
4. do not stop at "job is still running" unless fire-and-forget was explicitly requested

## Short Iterative Evaluation Loop

Short local edit-and-evaluate cycles must be handled as an owned execution loop, not as a one-shot task.

When the task is iterative optimization:

1. compile an evaluation ladder:
   - baseline or previous-best reference
   - primary regression set
   - promotion gate for larger evaluation
   - final target evaluation
2. prefer broader representative sets over a few hand-picked cases
3. after each batch:
   - run the current gate set
   - compare score against baseline and best-so-far
   - inspect regressions, not just aggregate score
   - decide `iterate`, `replan`, or `promote-to-next-gate`
4. if the new result is the best-so-far and the user requested preservation, snapshot the relevant prompt/config/code/results before the next risky change
5. if the current gate is unmet, do not stop merely because one iteration completed cleanly
6. only hand back to the user when:
   - compiled targets are met
   - a true hard blocker remains
   - a safety/resource gate requires approval

## Unknown Error Branch

When execution fails with unknown error:

1. local evidence triage (stack, logs, env, recent diffs)
2. retrieve relevant `procedure` and `episode` memory
3. targeted search
4. deep research (debug-investigation) if unresolved
5. apply smallest fix and validate

Retry behavior should be mode-aware and evidence-driven.

## SSH and Remote Policy

1. Choose control mode: direct SSH, SSH+session manager, scheduler, or existing remote agent.
2. Declare remote model: remote-native or local-driver.
3. Use remote profile reuse decision from `run-governor`; if missing, request exactly one confirmation via `human-checkpoint`.
4. Validate connectivity and runtime basics before expensive launch when uncertainty exists.

## Logging and Failure Handling

Record stable paths for:

1. stdout/stderr
2. checkpoints
3. metrics
4. artifacts

On failures, record owner and cleanup plan.
On stalled jobs, record recovery attempt and next watch step.

## Data Analysis Visualization Policy

When the deliverable includes data analysis results:

1. run visualization analysis on the computed metrics/tables before final delivery
2. save report-facing figures under `<codex-cwd>/logs/runs/<run_id>/reports/figures/`
3. keep runtime-generated source figures under `<runtime_project_root>/runs/<run_id>/artifacts/figures/`
4. include figure paths in stage reports and final summary
5. prefer stable filenames such as `<topic>-<metric>.png` or `<topic>-<metric>.svg`

## Stop Conditions

Do not launch full run when required inputs are still unknown and not explicitly waived.

In `full-auto`, continue only if risk is acceptable and no major safety issue exists.
In `full-auto`, if remote profile is complete, reuse it by default unless explicitly overridden.
For iterative optimization tasks, do not stop after a single batch while the active evaluation gate or non-regression guard is still unmet.

## Output Contract

Emit execution state as:

```yaml
run_id: <id>
mode: <full-auto|moderate|detailed>
execution_mode: <local|ssh|ssh+tmux|scheduler|remote-agent>
remote_model: <remote-native|local-driver|n/a>
local_project_root: <path>
runtime_project_root: <path>
output_path: <runtime_project_root>/runs/<run_id>
environment:
  python: <path/version>
  env: <conda/venv/module>
  proxy_needed: <yes|no|unknown>
tracking:
  mode: <wandb|files|mixed|unknown>
  run_id: <id|pending>
node_plan:
  master: <host|n/a>
  workers: <list|pending>
logs:
  stdout: <path>
  artifacts: <path>
analysis_artifacts:
  figures_report_root: <codex-cwd>/logs/runs/<run_id>/reports/figures
  figures_runtime_root: <runtime_project_root>/runs/<run_id>/artifacts/figures
  figures: <list of saved figure paths>
next_action: <smallest safe step>
checkpoint_needed: <yes|no>
goal_status:
  primary_target: <target>
  active_gate: <current threshold or eval set>
  best_so_far: <metric summary>
  done_allowed: <yes|no>
```
