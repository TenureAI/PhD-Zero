---
name: memory-manager
description: |-
  Manage long-term AI R&D memory: retrieval, writeback, promotion, and shared export.
  TRIGGER when: run bootstrap, each new user turn, each execution batch, significant failure, replan, high-resource action, long-action resume, final report handoff, or compaction markers detected (Compact/压缩/Summary).
  DO NOT TRIGGER when: the exact same retrieval was just performed, freshness is still valid, and no new objective/stage/error signal appeared.
---

# Memory Manager

## Mission

Build compounding capability by turning execution traces into reusable, evidence-linked memory, with retrieval centered on prior experience rather than only current working state.

## Load References

Load these files before writing or promoting records:

1. `references/memory-layout.md`
2. `references/memory-templates.md`
3. `references/sqlite-schema.sql`

## Memory Types

Manage these layers:

1. `working`
   - run-scoped continuity state
   - resume after compaction, interruption, or long waits
2. `episode`
   - concrete run case records
   - useful for similar errors, repeated attempts, and local history
3. `procedure`
   - highest-priority execution memory
   - default retrieval layer before acting
4. `insight`
   - cross-task abstraction, tradeoffs, boundaries, and contradiction handling
5. `persona`
   - behavior config only

## Working Memory Contract

`working` must include:

1. `goal`
2. `stage`
3. `hypothesis`
4. `last_action`
5. `last_observation`
6. `next_step`
7. `blockers`
8. `evidence_refs`
9. `active_action_ids`
10. `todo_active`
11. `todo_done`
12. `todo_blocked`

Todo granularity should be task-level (small stages/subtasks), not command-level.

## Experience-First Retrieval Policy

Prior experience retrieval is the default. `working` is important for continuity, but it is not the only retrieval path and should not crowd out reusable experience.

Mandatory retrieval triggers:

1. every new user turn
2. every execution batch before acting
3. every replan
4. every significant failure or new error signature
5. every high-resource or irreversible action
6. every long-action resume or post-poll decision
7. before final answer or report handoff
8. when modifying `memory-manager` or another Memory-related skill/instruction
9. when compaction markers such as `Compact`, `压缩`, or `Summary` appear

Default retrieval order:

1. `procedure`
   - mandatory before every execution batch
2. `episode`
   - mandatory when a similar failure, repeated attempt, or same task type is present
3. `insight`
   - mandatory during planning, tradeoff analysis, contradiction handling, or final answer shaping
4. `working`
   - mandatory for resume, compaction recovery, long-action reconciliation, and final handoff

Query strategy:

1. query by `project`, `task_type`, `error_signature`, and stage first
2. add tags and FTS when exact filters miss
3. prefer `active` procedures/insights when confidence is similar
4. prefer recent local episodes over shared memory unless local retrieval is clearly low-yield
5. if retrieval is low-yield, keep going, but record `memory_skip_reason` or `memory_low_yield_reason`

## Shared Retrieval Policy

Treat shared memory as an optional read-only source, not as project-local memory.

1. Query project-local memory first.
2. If local retrieval is low-yield, query the user-configured shared repo from `project-context`.
3. Resolve the local shared repo path from `memory.shared_repo.path`; if missing, ask the user where the repo should live and persist it through `project-context`.
4. Use read-only retrieval against the local shared repo checkout; do not mirror shared records into `.project_local` by default.
5. Avoid syncing the shared repo on every run or stage.
6. Sync only when:
   - the shared repo checkout is missing and the user approved clone/bootstrap
   - a retrieval gap remains and the local shared repo is suspected stale
   - immediately before exporting shared memory
7. Treat hits as `external/shared` evidence until they are validated in the current project.
8. Do not rewrite shared records into local `episode/procedure/insight` as if they were observed locally unless the current run reproduced them.

## Writeback Policy

Write conservatively, but more frequently than before:

1. write a concise `working` delta after every execution batch
2. write a concise `working` delta after every long-action poll cycle that changes status or next step
3. write `episode` at milestones, major failure, replan, or human intervention
4. create `procedure` draft after repeated successful pattern or validated recovery workflow
5. create `insight` draft after cross-task recurring evidence
6. store evidence pointers, not narrative only
7. when a completed long-running action produces results that affect later decisions, record the result summary before leaving watch mode

## Error-Resolution Memory

For significant errors, capture:

1. `error_signature`
2. reproduction condition
3. attempted fixes
4. observed outcomes
5. final fix (if any)
6. unresolved hypotheses
7. retrieved procedures/episodes that influenced the fix

## Working Freshness Rules

Treat stale continuity state as risk:

1. refresh after plan changes, tool-call batches, or diagnosis updates
2. refresh after long-action polls that change status
3. review at least every 15 minutes in active execution
4. force review before high-resource actions
5. force review after interruptions or unexpected failures

## Invocation Schedule (Experience-First, Frequent but Targeted)

1. Mandatory once-per-run operations:
   - bootstrap `retrieve/init-working` after intake and before planning/execution
   - close-out writeback before final task completion
2. Mandatory per-turn operations:
   - retrieve relevant experience on every new user turn
3. Mandatory per-batch operations:
   - retrieve `procedure` before every execution batch
   - write `working` delta after every execution batch
4. Mandatory trigger-based operations:
   - retrieve `episode` on problem, failure, repeated attempt, or new error signature
   - retrieve `insight` on planning/replanning/tradeoff/final answer
   - retrieve `procedure` plus `episode` before high-resource actions
   - reread `working` during resume, compaction recovery, long-action reconciliation, and final handoff
   - retrieve `procedure` plus `episode` immediately after stalled or failed poll outcomes
   - retrieve `insight` after completed poll outcomes when interpretation or next-step selection is needed
5. Cooldown:
   - skip only duplicate retrievals when objective, stage, and error signature are unchanged and the same hit set is still fresh
   - cooldown does not suppress a new-trigger retrieval
6. When skipped, log `memory_skip_reason` for auditability.

## Post-Compression Recovery (Required)

When memory is auto-compressed/summarized:

1. immediately run a `working` reread before the next execution step
2. rebuild `working` fields from recent evidence:
   - latest stage report
   - latest action/observation logs
   - latest todo diff (`todo_active/todo_done/todo_blocked`)
   - active long-action records
3. publish a compact post-compression state snapshot and continue only after snapshot is consistent

## Layered Retrieval Timing

Use layer-specific timing to keep retrieval frequent but useful:

1. `procedure` retrieve:
   - before every execution batch
   - before high-resource or irreversible actions
   - after stalled or failed background jobs
2. `episode` retrieve:
   - at run start for same project/task_type
   - at replan or major failure
   - when repeated failure indicates recent local history may help
3. `insight` retrieve:
   - during planning/replanning for hypothesis shaping
   - when evidence conflicts or root cause is unclear
   - before final report/answer to run boundary checks
4. `working` retrieve:
   - bootstrap
   - resume/reconcile
   - after memory compression
   - before final handoff
5. `persona` retrieve:
   - once at run start
   - on interaction mode switch or explicit user preference change
   - before final user-facing delivery

## Recovery on Context Drift

If execution becomes repetitive or confused:

1. rebuild working state from action and observation logs
2. run targeted retrieval by project/task/error signature
3. if drift followed compaction or summary-style recovery, read prior Memory before publishing or trusting a compact state summary
4. publish compact state summary before continuing

## Compaction Recovery Policy

When context may have been compressed:

1. inspect available status/state/context files for markers such as `Compact`, `压缩`, `Summary`, or equivalent summary/compression techniques
2. if any marker is present, call `memory-manager` to read prior Memory before editing instructions, planning next actions, or resuming execution
3. if prior Memory cannot be read, treat that as an active blocker because key context may be missing
4. record the compaction trigger and retrieval result in working state or the next stage report

## Promotion Policy

Promote only with evidence:

1. `procedure draft -> active` after successful reuse and stable boundaries
2. `insight draft -> active` after multi-episode support
3. require human review for safety-critical or expensive procedures
4. deprecate entries when contradictions accumulate

## Shared Export Policy

Treat shared export as post-task work:

1. do not export during main task execution
2. export only verified/high-value records
3. never export noisy `working` state
4. require `human-checkpoint` before publishing
5. sync the shared repo before export so dedupe/conflict checks run against the latest branch tip

## Shared Repository Contract

When exporting:

1. target `https://github.com/TenureAI/open-research-memory`
2. use pull-based flow: local export -> `codex/*` branch -> PR -> review -> merge
3. never push directly to `main`
4. enforce schema and required sections

## Shared Retrieval Helper

Use the helper script for lightweight read-only search of a local shared repo checkout:

```bash
python3 .agents/skills/memory-manager/scripts/shared_memory_retrieval.py \
  --repo-root /path/to/open-research-memory \
  --query "cuda out of memory" \
  --type procedure \
  --task-type debug \
  --limit 5
```

## Required Operation Output

For each memory operation, emit:

1. `Run`
2. `Action` (`retrieve|write|promote|deprecate|export`)
3. `Target`
4. `Layers`
5. `Rationale`
6. `Query`
7. `Hits`
8. `Working Update`
9. `memory_skip_reason` when applicable
