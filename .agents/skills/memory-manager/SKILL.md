---
name: memory-manager
description: Manage long-term AI R&D memory with retrieval, writeback, promotion, and shared export candidates. Use when preserving run state, maintaining working todo lists, reusing prior debugging/research knowledge, recording outcomes, or preparing post-task shared-memory publication.
---

# Memory Manager

## Mission

Build compounding capability by turning execution traces into reusable, evidence-linked memory.

## Load References

Load these files before writing or promoting records:

1. `references/memory-layout.md`
2. `references/memory-templates.md`
3. `references/sqlite-schema.sql`

## Memory Types

Manage these layers:

1. `working`: run-scoped current state and todo tracking.
2. `episode`: concrete run case record.
3. `procedure`: reusable SOP from repeated success.
4. `insight`: cross-task abstraction with boundaries.
5. `persona`: behavior config only.

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
9. `todo_active`
10. `todo_done`
11. `todo_blocked`

Todo granularity should be task-level (small stages/subtasks), not command-level.

## Retrieval Policy

Retrieve early when useful, but do not block execution:

1. Query by `project`, `task_type`, `error_signature` first.
2. Upgrade retrieval from optional to mandatory before continuing when either of these triggers is present:
   - you are modifying `memory-manager` or another Memory-related skill/instruction
   - a status, state, or context file contains compaction markers such as `Compact`, `压缩`, `Summary`, or similar summary/compression techniques
3. In mandatory-retrieval cases, read prior Memory first and treat the result as required context recovery rather than a best-effort lookup.
4. Add tags and FTS when exact filters miss.
5. Prefer `active` procedures/insights when confidence is similar.
6. Flag stale entries with low confidence.
7. If retrieval is low-yield and task is time-sensitive, continue with search/deep research directly only when the mandatory-retrieval triggers are absent.

## Writeback Policy

Write conservatively and continuously:

1. Update `working` on each meaningful state transition.
2. Write `episode` at milestones, major failure, replan, or human intervention.
3. Create `procedure` draft after repeated successful pattern.
4. Create `insight` draft after cross-task recurring evidence.
5. Store evidence pointers, not narrative only.

## Error-Resolution Memory

For significant errors, capture:

1. `error_signature`
2. reproduction condition
3. attempted fixes
4. observed outcomes
5. final fix (if any)
6. unresolved hypotheses

## Working Freshness Rules

Treat stale working state as risk:

1. Refresh after plan changes, tool-call batches, or diagnosis updates.
2. Review at least every 15 minutes in active execution.
3. Force review before high-resource actions.
4. Force review after interruptions or unexpected failures.

## Recovery on Context Drift

If execution becomes repetitive or confused:

1. Rebuild working state from action and observation logs.
2. Run targeted retrieval by project/task/error signature.
3. If drift followed a compaction step or summary-style recovery, read prior Memory before publishing or trusting a compact state summary.
4. Publish compact state summary before continuing.

## Compaction Recovery Policy

When context may have been compressed:

1. Inspect available status/state/context files for markers such as `Compact`, `压缩`, `Summary`, or equivalent summary/compression techniques.
2. If any marker is present, call `memory-manager` to read prior Memory before editing instructions, planning next actions, or resuming execution.
3. If prior Memory cannot be read, treat that as an active blocker because key context may be missing.
4. Record the compaction trigger and retrieval result in working state or the next stage report.

## Promotion Policy

Promote only with evidence:

1. `procedure draft -> active` after successful reuse and stable boundaries.
2. `insight draft -> active` after multi-episode support.
3. Require human review for safety-critical or expensive procedures.
4. Deprecate entries when contradictions accumulate.

## Shared Export Policy

Treat shared export as post-task work:

1. Do not export during main task execution.
2. Export only verified/high-value records.
3. Never export noisy `working` state.
4. Require `human-checkpoint` before publishing.

## Shared Repository Contract

When exporting:

1. Target `https://github.com/recursive-forge/open-research-memory`.
2. Use pull-based flow: local export -> `codex/*` branch -> PR -> review -> merge.
3. Never push directly to `main`.
4. Enforce schema and required sections.

## Required Operation Output

For each memory operation, emit:

1. `Run`
2. `Action` (retrieve/write/promote/deprecate/export)
3. `Target`
4. `Rationale`
5. `Evidence`
6. `Result`
