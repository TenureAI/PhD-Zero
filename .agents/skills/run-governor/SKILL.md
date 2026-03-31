---
name: run-governor
description: |-
  Govern run-level execution policy: mode selection, durable run tracking, long-action watch/resume policy, stage reporting, and safety allowances.
  TRIGGER when: starting a non-trivial research task (set mode + run_id), switching local/remote target, creating a new run, or mode-aware policy decisions needed.
  DO NOT TRIGGER when: trivial single-step tasks, pure info queries, or run already initialized with no policy change needed.
---

# Run Governor

## Mission

Set and enforce run-level execution policy so research runs stay consistent, auditable, durable across long waits, and mode-aware.

## Mode Selection Policy

At the start of a research run, ask the user to choose one mode:

1. `full-auto`
   - Minimize user interruptions.
   - Ask only for hard blockers or major safety risks.
   - Keep ownership until compiled success criteria are met, or a true blocker/safety gate requires interruption.
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
6. While confirmation is pending, read-only intake, code inspection, and evidence gathering are allowed; creating run artifacts or launching jobs is not.

## Persistent Completion Policy

When the user expresses persistence or target-seeking intent, compile it into run policy rather than treating it as stylistic wording.

Trigger phrases include examples such as:

1. "keep iterating"
2. "do not stop"
3. "until target"
4. "try many iterations"
5. "optimize until it works"
6. "reach 90%/100%" or similar target metrics

Required policy fields:

1. `execution_intent`: `single-pass|persistent-optimization`
2. `completion_policy`: `normal|until-target-or-hard-blocker`
3. `done_guard`: `normal|forbid_done_if_target_unmet`
4. `promotion_gates`: ordered thresholds such as "pass 30-case regression before 100-case sweep"
5. `non_regression_guards`: conditions that must not degrade materially
6. `backup_policy`: when to snapshot best-so-far prompts/configs/code/results

Rules:

1. `full-auto` controls interruption frequency; it does not weaken persistence requirements.
2. If user intent is `persistent-optimization`, one edit/test cycle is never sufficient reason to stop.
3. In `full-auto` plus `persistent-optimization`, remain in the execution loop until one of these is true:
   - compiled hard targets are met
   - a true hard blocker remains after reasonable recovery attempts
   - a major safety/resource gate requires approval
   - the user explicitly stops or changes the objective
4. If the target is aspirational but measurable, store both the stretch target and the current promotion gate.
5. If the user asked to preserve strong variants, snapshot best-so-far artifacts before higher-risk changes.

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
2. While blocked, do not create `run_id`, run directories, manifests, policy files, working files, reports, runtime snapshots, or background watchers.
3. `moderate` is only a recommendation label and cannot be applied unless user-confirmed.
4. For `moderate` or `detailed`, ask via built-in question tool first; if unavailable, use plain-text fallback.
5. If user asks to proceed without specifying values, ask a direct clarification question and remain blocked.
6. Confirmation collection must be mediated by `human-checkpoint`.
7. Any assumption for mode/target is non-compliant, even when likely.

## Memory Bootstrap Gate

Before transitioning from initialization to execution workflow:

1. Set `memory_policy=experience-first-continuous` unless user explicitly overrides.
2. Ensure one `memory-manager` bootstrap operation is complete:
   - `retrieve` or `init-working` for current project/task context.
3. If bootstrap is missing, mark status `blocked-awaiting-memory-bootstrap`.
4. This gate enforces bootstrap plus retrieval policy declaration; ongoing retrieval cadence is enforced by `research-workflow` and `memory-manager`.

## Durable Execution Policy

Treat long waits as first-class runtime state, not as something the model should silently "keep waiting" for.

Classify an action as `long_action` when any is true:

1. expected duration is over 5 minutes
2. action launches training, evaluation, inference batches, indexing, or remote jobs
3. action uses `sleep`, async polling, or scheduler submission
4. action is high-resource (`L2` or `L3`)
5. action likely outlives the current model turn

For every `long_action`, do all of the following before waiting:

1. create an action record under `actions/<action_id>.yaml`
2. persist:
   - `action_id`
   - `status`
   - `kind`
   - `command`
   - `cwd`
   - `expected_duration_seconds`
   - `poll_interval_seconds`
   - `launch_time`
   - `last_heartbeat`
   - `next_poll_at`
   - `success_signal`
   - `failure_signal`
   - `resume_step`
3. if the command is launched locally, capture `pid` and log path
4. immediately enter `watch mode`
   - if the current session remains active, use a poll loop (`model chooses sleep -> watch/poll -> inspect state -> model chooses next sleep`)
   - if the action may outlive the current turn, start an external watch loop or automation before ending the turn
5. never mark a `long_action` done without an explicit poll/reconcile step
6. choose an initial poll interval, but keep control with the model
   - scripts may store the chosen interval and suggested next poll time
   - scripts must not become the primary owner of polling strategy
   - the model may shorten or lengthen the next sleep after each poll
7. keep ownership after launch
   - launching a job is not sufficient completion
   - after every poll, the agent must continue with monitoring, diagnosis, recovery, result collection, or replan
   - do not hand the task back to the user only because the job is long-running

Allowed liveness states:

1. `pending`
2. `running`
3. `stalled`
4. `failed`
5. `completed`
6. `cancelled`

## Active Run Registry

Maintain these durable records in `<codex-cwd>/logs/runs/<run_id>/`:

1. `actions/index.json`
   - list of active and historical `action_id`s
   - last sweep time
2. `actions/<action_id>.yaml`
   - one persisted record per long action
3. `actions/watch.log`
   - optional watcher loop output

Registry rules:

1. scan the registry before each new planning cycle
2. if `next_poll_at <= now`, reconcile action state before planning unrelated work
3. do not assume a long-running command completed only because chat output paused
4. if a process ended without a success or failure signal, mark `stalled` and inspect before continuing
5. treat `next_poll_at` as the model-provided wake-up hint for watchers; do not busy-wait
6. do not treat a `running` record as a reason to stop work; it is a reason to stay in watch mode

## Resume Gate

At the start of every resumed run or fresh model turn:

1. read active run metadata and the latest `working/state.yaml`
2. reconcile all `pending|running|stalled` actions
3. update each action with fresh liveness evidence
4. restore the next safe step from `resume_step` or `working.next_step`
5. immediately branch into watch continuation, result collection, diagnosis, or replan based on reconciled action state
6. only continue unrelated planning after active-action handling is complete or explicitly delegated

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
   - execution intent and completion policy
   - compiled target gates and non-regression guards
   - done guard and backup policy
   - high-resource heuristic bands
   - safety policy notes
   - per-run action allowances
   - watch policy
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
   - objective, current phase, hypothesis, blockers, next step, active action ids
4. `working/todo.yaml`
   - `todo_active`, `todo_done`, `todo_blocked`
5. `actions/index.json`
   - active action registry
6. `actions/<action_id>.yaml`
   - durable long-action state
7. `reports/index.md`
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

Before any `L2` or `L3` action:

1. run targeted memory retrieval for relevant procedures and episodes
2. create a long-action record if the job will not finish immediately
3. persist a watch plan and a model-selected poll interval
4. in `moderate` and `detailed`, confirm before launch
5. in `full-auto`, proceed unless major safety risk is present
6. after launch, remain responsible for monitoring and post-poll handling until a true blocker or completion condition exists

## Stage Reporting Contract

At each stage completion:

1. Save one stage report file under `reports/`.
2. Update `reports/index.md` status and timestamp.
3. In chat, provide a detailed stage summary plus report path.
4. Do not require user reply just because a stage report was emitted.
5. Include active long-action status when the stage depends on background work.

## Required Output for Run-Governor Operations

For each run-governor action, emit:

1. `Run`: run_id and active mode
2. `Action`: initialize, switch-mode, update-policy, new-topic-check, resume, watch-update, or stage-report
3. `Decision`: what was chosen and why
4. `Execution`: local/remote choice and reuse decision
5. `Paths`: affected control/output/context paths
6. `Completion`: execution intent, completion policy, done guard, and active promotion gate
7. `Next`: next actionable step
8. `Confirmation`: `user_confirmed_mode`, `user_confirmed_execution_target`, and whether initialization is permitted (`YES|NO`)
9. `Compliance`: `gate_status=pass|blocked`, with blocked reason when applicable
10. `Interaction`: `interaction_transport` and optional `fallback_reason`
11. `Memory`: `memory_policy` and `memory_bootstrap_done=YES|NO`
12. `Liveness`: active action count, newly launched action ids, and whether reconciliation is clean (`YES|NO`)
13. `Watch`: `watch_mode=session-loop|external-loop|none` and next poll time when applicable
14. `Polling`: current interval, next poll time, and whether the model revised the interval this cycle
15. `Followup`: `continue-watch|collect-results|diagnose-stall|diagnose-failure|replan|checkpoint`

## Violation Recovery Policy

If initialization occurred before required confirmation:

1. Immediately acknowledge non-compliance.
2. Ask whether to keep or clean the created artifacts.
3. Do not continue execution until user re-confirms `mode` and `execution_target`.
4. Record the incident and recovery choice in the next stage report.

If a long action was launched without a persisted action record:

1. Stop normal planning.
2. Reconstruct and persist the missing action record immediately.
3. Reconcile log, pid, and latest output before continuing.
4. Record the recovery step in the next stage report.
