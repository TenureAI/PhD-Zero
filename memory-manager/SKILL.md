---
name: memory-manager
description: Manage long-term AI R&D memory through retrieval, controlled writeback, promotion, and shared export candidates. Use when a task needs prior similar cases, run-state persistence, lessons learned, SOP extraction, cross-task insight consolidation, or publishing to open-research-memory. Trigger when requests mention memory, episodes, procedures, insights, run logs, memory_manager, experience reuse, or open-research-memory sharing.
---

# Memory Manager

## Mission
Build compounding capability by turning execution traces into reusable memory.

## Load References
Load these files before writing or promoting memory records:
1. `references/memory-layout.md`
2. `references/memory-templates.md`
3. `references/sqlite-schema.sql`

## Memory Types
Manage these layers:
1. `working`: run-scoped volatile state and action logs.
2. `episode`: concrete case records with context, attempts, outcomes, and evidence.
3. `procedure`: reusable SOP extracted from repeated successful episodes.
4. `insight`: cross-task abstractions with scope, boundaries, and confidence.
5. `persona`: behavior config only; do not mix with empirical memory.

## Retrieval Policy
Retrieve aggressively and early:
1. Query by `project`, `task_type`, and `error_signature` first.
2. Add `tags` and full-text matching when exact filters miss.
3. Return top candidates with relevance reason and applicability boundary.
4. Prefer `active` procedure and insight over draft when confidence is comparable.
5. Flag stale entries when `last_used_at` is old and confidence is low.

## Writeback Policy
Write conservatively:
1. Update `working` after each major state transition.
2. Write an `episode` at milestone completion, major failure, route pivot, or human intervention.
3. Draft a `procedure` only after repeated successful pattern (target: 2-3 episodes).
4. Draft an `insight` only after cross-task recurring pattern with evidence links.
5. Store evidence pointers, not only narrative summaries.

## Working Freshness Rules
Treat stale `working` state as an execution risk:
1. Refresh `working` after every plan change, tool call batch, or error diagnosis result.
2. Run a periodic `working` review at least every 15 minutes during active runs.
3. Force a `working` review before long training, expensive actions, or human checkpoints.
4. Force a `working` review after any unexpected failure or interruption.
5. If `working` is stale or inconsistent, pause new actions until it is repaired.

## Working Review Checklist
Validate these fields on each review:
1. `goal`: current run objective is still valid.
2. `hypothesis`: active assumption and its confidence.
3. `last_action` and `last_observation`: latest action-evidence pair is complete.
4. `next_step`: smallest executable step is unambiguous.
5. `blockers`: active blockers and owner (agent or human).
6. `evidence_refs`: links to logs, files, metrics, and command outputs.

## Recovery on Context Drift
If the run appears confused or repetitive:
1. Rebuild `working` from `action_log.jsonl` and `observations.jsonl`.
2. Re-run targeted retrieval with `project`, `task_type`, and `error_signature`.
3. Re-issue a compact state summary before continuing execution.

## Promotion Policy
Promote strictly:
1. `procedure draft -> active` only after successful reuse and stable boundary conditions.
2. `insight draft -> active` only after multi-episode support and no unresolved contradictions.
3. Require human review for safety-critical, expensive, or shared-memory-bound items.
4. Deprecate entries when new evidence conflicts and confidence drops.

## Shared Export Policy
Export only high-value items:
1. `verified` episodes with transferable lessons.
2. `active` procedures with clear prerequisites.
3. `active` insights with explicit evidence links and failure boundaries.
4. Never export `working` state or noisy drafts.

## Shared Repository Contract
When exporting shared memory:
1. Target repository: `https://github.com/recursive-forge/open-research-memory`.
2. Default local clone path: `<workspace>/open-research-memory`.
3. Use pull-based flow only: local export -> branch (`codex/*`) -> PR -> review -> merge.
4. Do not push directly to `main`.
5. Read and follow the canonical docs in that repository: `README.md`, `CONTRIBUTING.md`, `schemas/`, `templates/`, and `.github/pull_request_template.md`.
6. Enforce schema compatibility and required sections (`Context`, `Reproduce`, `Evidence`, `Failure Boundary`).
7. Include reproducibility details and evidence pointers so other contributors can reuse safely.
8. Trigger `human-checkpoint` before publishing shared exports when confidence is low or impact is high.

## Shared Publish Steps
When a record is ready for sharing:
1. Export candidate files into `shared_export/` in the local project.
2. Copy or transform candidates into the correct folders under `open-research-memory/`.
3. Run repository validation (`python3 scripts/validate_records.py`).
4. Commit on a `codex/*` branch with clear record scope.
5. Open PR and request review; merge only after checks pass.

## Shared Memory Consumption
When `open-research-memory` is already cloned locally, use it as an external evidence source:
1. Pull latest changes from the shared repository before retrieval.
2. Search shared records by `type`, `status`, `tags`, `task_type`, and error pattern.
3. Prioritize `active`, `verified`, and `trusted` records; treat `draft` as weak hints.
4. Validate applicability boundary and failure boundary before reuse.
5. Convert selected shared records into local candidate context, not immediate truth.
6. After applying a shared record, log outcome in local `episode` and update confidence.
7. If reuse repeatedly succeeds, promote to local `procedure` or `insight` with shared-source links.
8. If shared guidance fails, record counterexample and avoid repeating blindly.

## Shared-to-Local Linking Rule
For every reused shared record:
1. Store source repository path and commit hash in local evidence refs.
2. Link local `episode/procedure/insight` back to the shared record id.
3. Keep local overrides explicit when local environment differs.

## Required Operation Output
Output this structure for every memory operation:
1. `Action`: retrieve, write, promote, deprecate, or export.
2. `Target`: memory id or new record type.
3. `Rationale`: why this action is justified.
4. `Evidence`: supporting logs, metrics, files, or run IDs.
5. `Result`: created, updated, skipped, blocked, or needs checkpoint.
