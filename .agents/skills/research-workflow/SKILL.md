---
name: research-workflow
description: |-
  PRIMARY ORCHESTRATOR — trigger this skill FIRST for any non-trivial AI R&D task. Coordinates run-governor, memory-manager, deep-research, research-plan, project-context, experiment-execution, human-checkpoint, and paper-writing.
  TRIGGER FIRST when: any non-trivial research task begins (analysis, debugging, reproduction, planning, evaluation, training), or context compaction detected (Compact/压缩/Summary). Other skills should be invoked FROM WITHIN this workflow.
  DO NOT TRIGGER when: trivial single-command tasks ("show file", "fix typo"), or pure conversational queries.
---

# Research Workflow

## Mission

Drive AI R&D tasks with small, testable, evidence-first steps while supporting durable long-running execution, aggressive experience retrieval, and DR-first external search.

## Orchestration Order

**CRITICAL: Each step below that names a skill MUST be executed by calling `Skill(skill: "<name>")`. Do NOT simulate or skip the skill — actually invoke it via the Skill tool. Producing output that a skill should produce without invoking that skill is a workflow violation.**

For non-trivial tasks, run this order:

1. **`Skill(skill: "run-governor")`** — Initialize run policy (mode + run_id) and reconcile active long actions before any execution.
2. **`Skill(skill: "project-context")`** — Resolve runtime context before experiment/report/eval execution. MUST call when env setup is needed.
3. Understand user objective and current code/evidence state.
4. **`Skill(skill: "human-checkpoint")`** — Clarify ambiguous requirements. MUST call when intake is incomplete.
5. Complete intake checkpoint before planning or decomposition.
6. **`Skill(skill: "memory-manager")`** — Run bootstrap retrieval and initialize durable working state. MUST call before planning.
7. **`Skill(skill: "deep-research")`** — Use as the default external search gateway whenever outside evidence is needed, and always when research-intent keywords appear.
8. **`Skill(skill: "research-plan")`** — Build execution plan. MUST call for planning-heavy requests or after deep-research scoping.
9. Confirm plan as required by mode.
10. **`Skill(skill: "experiment-execution")`** — Execute experiment. MUST call for any actual run/launch/monitor.
11. Replan on major issues when needed.
12. Emit stage reports and maintain report index.
13. **`Skill(skill: "memory-manager")`** — Close-out writeback. MUST call before task completion.
14. **`Skill(skill: "paper-writing")`** — Write paper deliverable. MUST call only when user explicitly asks for paper output.

## Mode-Aware Interaction Policy

Follow run mode from `run-governor`:

1. `full-auto`
   - Prefer autonomous decisions.
   - Ask user only for hard blockers or major safety risks.
2. `moderate`
   - Confirm finalized plan.
   - Confirm before high-resource actions.
3. `detailed`
   - Ask on unclear path.
   - Ask before high-resource actions.

If user explicitly asks to switch mode, switch immediately.

## User Interaction Routing Policy

Route required user interactions through `human-checkpoint`:

1. In `moderate` or `detailed`, prefer built-in user-question tool (`request_user_input`).
2. If built-in tool is unavailable, degrade to concise plain-text questions.
3. Apply this routing to intake clarification, plan confirmation, replan confirmation, and parameter approvals.
4. Log channel choice as `interaction_channel=request_user_input|plain-text-fallback` and include `fallback_reason` when used.

## Mid-Run Intent Switch Gate (Mandatory)

On each new user message:

1. Re-evaluate objective and skill routing before executing the next pending action.
2. Retrieve relevant memory before new planning or execution continues.
3. If user intent shifts to research/scoping/comparison/root-cause inquiry, call `Skill(skill: "deep-research")` immediately — do NOT answer the research question yourself.
4. Do not continue stale execution plans when the objective changed materially.
5. If `deep-research` is skipped, emit `dr_skip_reason` with freshness evidence (date/timestamp and source coverage), then continue.
6. Cooldown:
   - no more than one non-forced deep-research call per stage.
   - bypass cooldown when objective changed, contradiction appears, or high-impact uncertainty remains unresolved.

## Goal Compilation Gate (Mandatory)

Before planning the first execution batch, translate the user request into machine-checkable success gates. Do not leave stopping conditions as prose only.

Compile at least:

1. `objective_summary`: one-sentence task goal
2. `primary_target`: final target metric or observable end state
3. `promotion_gates`: staged thresholds that must be passed before larger or costlier evaluation
4. `non_regression_guards`: what must not degrade materially
5. `backup_policy`: when to preserve best-so-far variants
6. `stop_allowed_only_if`: exact conditions that permit `done`
7. `hard_blockers`: the small set of conditions that justify asking the user

Examples of required compilation:

1. "keep iterating" or "do not stop" -> `completion_policy=until-target-or-hard-blocker`
2. "target 100% accuracy" -> stretch target plus current promotion gate
3. "use about 30 examples first, then try 100" -> ordered evaluation ladder
4. "do not overfit a few cases" -> non-regression guard on held-out or previously-correct samples
5. "backup strong versions" -> preserve best-so-far artifact before riskier changes

If any of these are measurable but omitted from the compiled goal state, treat that as a workflow defect and repair it before continuing.

## Durable Execution Loop

Repeat this loop until completion:

1. Compile or refresh success criteria, promotion gates, and done guards.
2. Retrieve prior experience:
   - `procedure` retrieval is mandatory before each execution batch
   - add `episode` retrieval when a problem, repeated attempt, or new error signature appears
   - add `insight` retrieval for planning, tradeoffs, or final answer shaping
3. Route external search through `deep-research` when fresh outside evidence is needed.
4. Plan the smallest useful next batch.
5. If the batch contains a `long_action`, persist an action record before waiting.
6. If the batch contains a `long_action`, switch to `watch mode`.
7. Act or poll an active action.
8. Observe outputs or liveness state.
9. If a poll occurred, immediately branch into post-poll handling rather than stopping at a status update.
10. Write working delta.
11. Evaluate result quality, target progress, and non-regression status against the compiled gates.
12. Decide: iterate, replan, checkpoint, or done.

## Short Iterative Optimization Policy

Treat local edit-evaluate loops with the same ownership standard as long-running jobs. They are not "one batch and done" tasks.

For iterative optimization tasks:

1. establish a baseline score before the first risky change when practical
2. define the primary regression set and any promotion gate set before broadening evaluation
3. after each batch:
   - compare against baseline and best-so-far
   - check non-regression guards
   - update which promotion gate is next
4. if a new best result appears and the user requested preservation or the route is high-risk, snapshot the best-so-far variant before proceeding
5. if targets are still unmet and a safe next step exists, default to `iterate`, not `done`
6. if repeated attempts plateau or regress, default to `replan`
7. ask the user only for a true blocker, safety/resource gate, or objective ambiguity that cannot be resolved locally

## Long-Running Action Policy

Treat an action as long-running when it is expected to exceed 5 minutes, launches a remote or async job, or likely outlives the current model turn.

Before launching a long-running action:

1. persist an action record through `run-governor`
2. record:
   - command
   - cwd
   - log path
   - success/failure signals
   - expected duration
   - poll interval
   - resume step
3. update working state with the active `action_id`
4. choose an initial poll interval, but keep the schedule under model control
5. if the action is likely to outlive the current turn, start an external watcher loop before leaving the turn

While the current session remains active:

1. use poll loops rather than blocking waits
2. the loop should be `model chooses sleep -> run watcher/poll -> inspect -> model chooses next sleep -> continue`
3. if no new output appears, classify as `running` or `stalled`, not `done`
4. the model may shorten the interval when there is fresh progress, warning signs, or expected completion is near
5. the model may lengthen the interval when the process is healthy but idle
6. watcher scripts should report status, not own the polling strategy
7. after each poll, update working state and next poll time
8. after each poll, immediately choose one of:
   - continue-watch
   - collect-results
   - diagnose-stall
   - diagnose-failure
   - replan
9. do not hand the task back to the user merely because the job is long-running
10. replan only after explicit lack-of-progress evidence, not because output paused briefly

## Post-Poll Handling Policy

After every long-action poll, the agent must keep ownership of the task and continue from the observed state.

Required branches:

1. `running`
   - if the process is healthy, choose the next sleep interval and continue watch mode
   - if progress appeared, update working state and keep monitoring
2. `completed`
   - inspect outputs, logs, checkpoints, or metrics immediately
   - run downstream validation, analysis, or report generation instead of waiting for the user to come back
3. `stalled`
   - inspect logs and latest outputs
   - retrieve `procedure` and `episode` memory before the next recovery attempt
   - attempt the smallest safe recovery or replan
4. `failed`
   - inspect failure evidence immediately
   - retrieve relevant memory
   - attempt the smallest safe recovery, or replan if needed
5. `checkpoint`
   - ask the user only if a true hard blocker, major safety risk, or explicit decision point remains

Default rule:

1. Never respond with the equivalent of "the job is running, come back later" unless the user explicitly wants fire-and-forget behavior.
2. Long-running work stays inside the watch loop until one of these is true:
   - success criteria are met
   - a hard blocker requires the user
   - a safety/resource gate requires explicit approval
   - an external automation takeover was explicitly established

## Watch-Loop Prompt Template

When running in watch mode, use this template after every poll so followup handling stays consistent instead of ad hoc.

Template:

1. poll the action
2. read:
   - `status`
   - `status_changed`
   - `progress_changed`
   - `followup_action`
   - `last_log_tail`
3. execute the branch for `followup_action`
4. update working delta
5. either choose the next sleep interval or continue into diagnosis/result handling immediately

Branch template:

1. `followup_action=continue-watch`
   - summarize what changed
   - decide the next sleep interval
   - remain in watch mode
2. `followup_action=wait-and-poll`
   - confirm the process is still healthy
   - choose the next sleep interval
   - remain in watch mode
3. `followup_action=collect-results`
   - inspect outputs, checkpoints, logs, metrics, or artifacts immediately
   - validate against success criteria
   - continue to downstream analysis/reporting rather than stopping at "completed"
4. `followup_action=diagnose-stall`
   - inspect logs and latest outputs
   - retrieve `procedure` plus relevant `episode` memory
   - attempt the smallest safe recovery or replan
5. `followup_action=diagnose-failure`
   - inspect failure evidence
   - retrieve relevant memory
   - run the smallest safe recovery path, or replan if needed
6. `followup_action=replan`
   - update hypothesis and next step
   - restart the loop with a new execution batch

Compact prompt form:

```text
Watch loop:
1. Poll the active action.
2. Read status, status_changed, progress_changed, followup_action, and last_log_tail.
3. If followup_action=continue-watch or wait-and-poll, choose the next sleep interval and keep ownership.
4. If followup_action=collect-results, inspect outputs immediately and continue analysis/validation.
5. If followup_action=diagnose-stall or diagnose-failure, inspect evidence, retrieve memory, and attempt the smallest safe recovery.
6. If followup_action=replan, update the route and continue execution.
7. Do not stop at a mere status update, and do not hand the task back to the user unless a true blocker remains.
```

## Search, Memory, and Deep-Research Policy

Use these in combination:

1. `memory-manager` bootstrap is mandatory before planning/execution for non-trivial runs.
2. Every new user turn must retrieve relevant memory before planning continues.
3. Every execution batch must retrieve `procedure` memory before acting.
4. If a problem appears, a new error signature is observed, or repeated attempts are failing, retrieve `episode` memory before the next fix attempt.
5. Before high-resource or irreversible actions, retrieve `procedure` plus relevant `episode` memory.
6. During planning, tradeoff analysis, contradiction resolution, or final answer shaping, retrieve `insight` memory.
7. `working` memory reads are mandatory for resume/reconcile, compaction recovery, long-action resume, and final handoff; they are not the only retrieval path.
8. After every execution batch and every long-action poll cycle, write a concise `working` delta.
9. After every stalled or failed poll result, retrieve `procedure` plus relevant `episode` memory before the next fix attempt.
10. After every completed poll result, inspect outputs and retrieve `insight` memory if interpretation, report writing, or tradeoff analysis is needed.
11. All external search must route through `deep-research`; do not bypass it with ad hoc search.
12. `deep-research` may choose light/default/deep execution depth internally, but it may not silently skip actual search.
13. If project-local memory retrieval is low-yield, shared-memory retrieval may query the configured local shared repo as a read-only source.
14. If memory or DR is skipped, record `memory_skip_reason` or `dr_skip_reason` with concrete evidence.
15. For unknown errors, use this branch:
   - local evidence triage (logs, stack trace, recent changes)
   - local memory retrieval (`procedure`, then `episode`)
   - shared-memory retrieval when reusable SOPs or prior debug cases are likely relevant
   - `deep-research` search if the issue is still unresolved or freshness-sensitive
   - minimal fix validation
16. If compaction is detected, treat missing working reread as a workflow violation and recover before continuing.
17. If deep research was used for open-ended scoping, call `Skill(skill: "research-plan")` to convert findings into an execution-ready plan. Skip only if the user explicitly opts out.

## Replanning Policy

Trigger replan when:

1. major assumption fails
2. repeated attempts show no improvement
3. new evidence changes route significantly
4. resource/risk profile changes
5. a long-running action remains `stalled` across multiple polls
6. post-poll handling repeatedly produces no safe next step

Mode controls whether replan confirmation is required.

## Stage Reporting Policy

At each stage completion or major todo completion:

1. Save stage report under `<codex-cwd>/logs/runs/<run_id>/reports/`.
2. Update `reports/index.md` with status and timestamp.
3. In chat, provide a detailed summary plus report path.
4. Do not block execution only because a stage report was emitted.
5. If the stage depends on background work, include active action ids, latest liveness state, and next poll plan.
6. If the stage delivers data-analysis results, include visualization outputs and saved figure paths (default: `<codex-cwd>/logs/runs/<run_id>/reports/figures/`).

## Mandatory Visualization Policy

**Every report that presents quantitative results MUST include visualizations. This is non-negotiable.**

1. When writing any report (stage report, final report, evaluation summary) that contains numerical results, tables, or comparisons, you MUST generate matplotlib/code-based figures before finalizing the report.
2. At minimum, generate:
   - a ranking/comparison chart when multiple strategies, methods, or configurations are compared
   - a breakdown chart when per-category/per-subject/per-level data is available
   - a trend chart when results vary across an ordered dimension
3. Save all figures to `<codex-cwd>/logs/runs/<run_id>/reports/figures/` and embed them in the report markdown with relative paths.
4. Prefer code-generated assets that can be regenerated. Save the generation script alongside the figures.
5. If the report scope is large or the visualizations need polished formatting, invoke `Skill(skill: "paper-writing")` to handle the report writing and figure integration.
6. If you are unsure whether a report needs visualization, it does. Over-visualizing is acceptable; under-visualizing is a violation.

## Shared Memory Export Gate

Do not export shared memory during core task execution.

1. Complete the primary task first.
2. Treat shared export as a post-task phase.
3. Require `human-checkpoint` before publishing shared memory.
4. Sync the shared repo before opening the export PR.

## Decision Policy

Use this order:

1. `done`: all compiled hard gates are satisfied with evidence.
2. `checkpoint`: decision requires mode-based confirmation or safety gating.
3. `iterate`: target is still unmet and a validated next step exists.
4. `replan`: current route is weak, stale, or repeatedly failing to improve.
5. `blocked`: hard blocker requires user input.

Done guard:

1. If `completion_policy=until-target-or-hard-blocker`, `done` is forbidden while the active promotion gate or hard target remains unmet.
2. A single successful batch, a clean run, or a partial fix is not sufficient for `done`.
3. If the final stretch target is not yet met but the current promotion gate is met, advance to the next gate instead of stopping.

## Evidence Standard

Treat conclusions as valid only when backed by one or more:

1. reproducible command output
2. measurable metric movement
3. file diff tied to behavior change
4. corroborated external source
5. durable liveness evidence for long-running actions

## Required Cycle Output

At end of each cycle, emit:

1. `Run`: run_id, mode, current stage
2. `State`: what is true now
3. `Evidence`: key observations
4. `Todo`: active/done/blocked highlights
5. `Next Step`: smallest safe action
6. `Replan Need`: yes or no, with reason
7. `Checkpoint Need`: yes or no, with reason
8. `Report Path`: stage report path or pending path
9. `Interaction Channel`: `request_user_input|plain-text-fallback|none`
10. `Goal Status`: primary target, active promotion gate, non-regression status, and whether `done` is currently allowed
11. `Memory`: retrieved layers, key hits, and `memory_skip_reason` when relevant
12. `Deep Research`: `dr_used=YES|NO`, depth, and `dr_skip_reason` or downgrade reason
13. `Liveness`: active action ids, current status, next poll time, and current poll interval when background work exists

## Violation Recovery Policy

If user interaction was handled outside required routing in non-`full-auto` modes:

1. Acknowledge non-compliance.
2. Re-run the missed checkpoint using `human-checkpoint` and channel policy.
3. Re-evaluate downstream conclusions that depended on the missed checkpoint.

If a cycle ended while a long-running action had no watch or resume plan:

1. Acknowledge the missing liveness protection.
2. Persist or reconstruct the action record.
3. Establish a poll or watcher plan before resuming normal work.
4. Record the recovery step in the next stage report.
