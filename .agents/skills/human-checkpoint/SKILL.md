---
name: human-checkpoint
description: Escalate critical AI R&D decisions to a human with concise options, tradeoffs, and recommendation. Use for major safety risks, hard blockers, high-resource approvals in non-full-auto modes, shared-memory publication, or any decision with high irreversible impact.
---

# Human Checkpoint

## Mission

Request human decisions only at meaningful risk or decision points, using executable options.

## Mode-Aware Trigger Policy

1. `full-auto`
   - Trigger only for hard blockers or major safety risks.
2. `moderate`
   - Trigger for plan-finalization confirmations.
   - Trigger before high-resource actions.
   - Trigger for major safety risks.
3. `detailed`
   - Trigger when path is unclear.
   - Trigger before high-resource actions.
   - Trigger for major safety risks.

Always trigger for shared-memory publication.

## Major Safety Risk Examples

Treat these as major risks:

1. potential large-scale file deletion
2. likely secret leakage
3. destructive remote/shared resource mutation
4. actions with clear financial or operational damage potential

In all modes, checkpoint is required for major risks.

## Request Format

Use this structure:

1. `Decision Needed`
2. `Context`
3. `Options`
4. `Recommendation`
5. `If Approved`
6. `If Rejected`

## Required Option Set for Risky Actions

Provide these options unless user already gave explicit policy:

1. allow once
2. allow same action type for this run
3. disallow and stop
4. user-defined handling

If option 2 is chosen, record it in run policy for this run only.

## Option Design Rules

1. Keep options executable now.
2. State tradeoffs in cost, risk, and learning value.
3. Put recommended option first when appropriate.
4. Keep request short and clear.

## After Decision

1. Execute only approved behavior.
2. Record rationale and outcome in memory/logs.
3. Re-check if another checkpoint is needed before next high-impact action.

## Failure Handling

If no human response is available:

1. In `full-auto`, continue with safest reversible path unless major safety risk remains unresolved.
2. In `moderate` or `detailed`, remain blocked until user response for required checkpoints.
