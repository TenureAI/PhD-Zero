---
name: research-workflow
description: Run a mode-aware, evidence-driven AI R&D workflow from intake to completion for research tasks such as code/paper analysis, debugging, reproduction, planning, and iterative delivery. Use when a non-trivial research task needs structured phases, stage reporting, replanning control, and integration with run-governor, research-plan, memory-manager, deep-research, human-checkpoint, and experiment-execution.
---

# Research Workflow

## Mission

Drive AI R&D tasks with small, testable, evidence-first steps while respecting the selected interaction mode.

## Orchestration Order

For non-trivial tasks, run this order:

1. Initialize run policy with `run-governor`.
2. Resolve runtime context with `project-context` before experiment/report/eval execution.
3. Resolve shared-memory source config from `project-context` when shared retrieval or export may be needed.
4. Understand user objective and current code/evidence state.
5. Clarify ambiguous requirements through `human-checkpoint`.
6. Complete intake checkpoint before planning or decomposition.
7. Run one `memory-manager` bootstrap (`retrieve/init-working`).
8. Run deep research when needed.
9. Build an execution plan (use `research-plan` for planning-heavy requests).
10. Confirm plan as required by mode.
11. Execute with trigger-based working-memory updates.
12. Replan on major issues when needed.
13. Emit stage reports and maintain report index.
14. Close task, write memory close-out, then optionally publish shared memory.

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
2. If user intent shifts to research/scoping/comparison/root-cause inquiry, activate `deep-research` immediately.
3. Do not continue stale execution plans when the objective changed materially.
4. If `deep-research` is skipped, emit `dr_skip_reason` with freshness evidence (date/timestamp and source coverage), then continue.
5. Cooldown:
   - no more than one non-forced deep-research call per stage.
   - bypass cooldown when objective changed, contradiction appears, or high-impact uncertainty remains unresolved.

## Default Execution Loop

Repeat this loop until completion:

1. Update success criteria.
2. Collect or refresh evidence.
3. Plan the smallest useful next action.
4. Refresh working todo state only when memory trigger conditions are met.
5. Act.
6. Observe outputs.
7. Evaluate result quality and risk.
8. Decide: iterate, replan, checkpoint, or done.

## Search, Memory, and Deep-Research Policy

Use these in combination:

1. `memory-manager` bootstrap is mandatory before planning/execution for non-trivial runs.
2. Between bootstrap and close-out, memory operations are trigger-based and non-aggressive.
3. Trigger memory operation when one of the following occurs:
   - stage transition
   - replan
   - significant error or new error signature
   - memory auto-compression/summarization completed
   - before high-resource action
   - before final answer/report handoff
4. Periodic `working` memory refresh is required when either holds:
   - at least 15 minutes since last memory operation
   - at least 3 execution cycles since last memory operation
5. Command-gap fallback: if 5 consecutive commands/actions finish without a memory update, force one concise `working` refresh.
6. Cooldown: no more than one non-forced memory operation per cycle.
7. Avoid per-command memory writes; batch observations into one delta update.
8. Use search/deep research directly when topic is time-sensitive, new, or currently blocked.
9. If project-local memory retrieval is low-yield, shared-memory retrieval may query the configured local shared repo as a read-only source.
10. Do not sync the shared repo on every cycle; prefer the current local checkout and sync only on explicit gap handling or before export.
11. For open-ended research/scoping requests, run deep research before giving decomposition or roadmap recommendations.
11.1 For mid-run new research requests, run deep research re-entry before further execution.
12. For unknown errors, use this branch:
   - local evidence triage (logs, stack trace, recent changes)
   - shared-memory retrieval when reusable SOPs or prior debug cases are likely relevant
   - targeted search
   - deep research (debug-investigation) if still unresolved
   - minimal fix validation
13. If skipping memory due to cooldown or low-value delta, record reason in the stage report.
14. If intake information is missing, trigger `human-checkpoint` before deep research or planning.
15. If deep research was used for open-ended scoping, hand off to `research-plan` to convert findings into an execution-ready plan. Skip only if the user explicitly opts out.

## Replanning Policy

Trigger replan when:

1. Major assumption fails.
2. Repeated attempts show no improvement.
3. New evidence changes route significantly.
4. Resource/risk profile changes.

Mode controls whether replan confirmation is required.

## Stage Reporting Policy

At each stage completion or major todo completion:

1. Save stage report under `<codex-cwd>/logs/runs/<run_id>/reports/`.
2. Update `reports/index.md` with status and timestamp.
3. In chat, provide a detailed summary plus report path.
4. Do not block execution only because a stage report was emitted.

## Shared Memory Export Gate

Do not export shared memory during core task execution.

1. Complete the primary task first.
2. Treat shared export as a post-task phase.
3. Require `human-checkpoint` before publishing shared memory.
4. Sync the shared repo before opening the export PR.

## Decision Policy

Use this order:

1. `done`: success criteria met with evidence.
2. `checkpoint`: decision requires mode-based confirmation or safety gating.
3. `iterate`: validated small next step exists.
4. `replan`: current route is weak or stale.
5. `blocked`: hard blocker requires user input.

## Evidence Standard

Treat conclusions as valid only when backed by one or more:

1. Reproducible command output.
2. Measurable metric movement.
3. File diff tied to behavior change.
4. Corroborated external source.

## Required Cycle Output

At end of each cycle, emit:

1. `Run`: run_id, mode, current stage.
2. `State`: what is true now.
3. `Evidence`: key observations.
4. `Todo`: active/done/blocked highlights.
5. `Next Step`: smallest safe action.
6. `Replan Need`: yes or no, with reason.
7. `Checkpoint Need`: yes or no, with reason.
8. `Report Path`: stage report path or pending path.
9. `Interaction Channel`: `request_user_input|plain-text-fallback|none`.

## Violation Recovery Policy

If user interaction was handled outside required routing in non-`full-auto` modes:

1. Acknowledge non-compliance.
2. Re-run the missed checkpoint using `human-checkpoint` and channel policy.
3. Re-evaluate downstream conclusions that depended on the missed checkpoint.
