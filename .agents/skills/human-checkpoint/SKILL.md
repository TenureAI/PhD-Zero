---
name: human-checkpoint
description: |-
  Escalate critical decisions to a human with options, tradeoffs, and recommendation.
  TRIGGER when: major safety risk, high irreversible impact, large GPU spend, destructive data ops, shared-memory publication, or hard blockers requiring human approval.
  DO NOT TRIGGER when: routine confirmations handled by run-governor, or low-stakes reversible actions.
---

# Human Checkpoint

## Mission

Request human decisions only at meaningful risk or decision points, using executable options.

## Interaction Channel Policy

For checkpoints that require user input, choose interaction channel in this order:

1. In `moderate` or `detailed`, prefer built-in user-question tool (`request_user_input`) for all required user interactions.
2. If the built-in tool is unavailable in the current runtime, degrade to concise plain-text questions in chat.
3. In `full-auto`, avoid non-essential questions and trigger checkpoints only by mode policy.
4. Never silently skip a required checkpoint because the preferred channel is unavailable.

## Mode-Aware Trigger Policy

1. `full-auto`
   - Trigger only for hard blockers or major safety risks.
2. `moderate`
   - Trigger for plan-finalization confirmations.
   - Trigger before high-resource actions.
   - Trigger for major safety risks.
   - Trigger for required intake clarification and parameter confirmations.
   - Trigger for replan confirmations when route changes materially.
3. `detailed`
   - Trigger when path is unclear.
   - Trigger before high-resource actions.
   - Trigger for major safety risks.
   - Trigger for required intake clarification and parameter confirmations.
   - Trigger for replan confirmations when route changes materially.

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

When using `request_user_input`, map the same structure into 1-3 short option-based questions.
When using plain-text fallback, ask one concise direct question at a time.

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
4. Record `interaction_channel=request_user_input|plain-text-fallback`.
5. If fallback is used, record `fallback_reason`.

## Failure Handling

If no human response is available:

1. In `full-auto`, continue with safest reversible path unless major safety risk remains unresolved.
2. In `moderate` or `detailed`, use plain-text fallback if built-in question tool is unavailable.
3. In `moderate` or `detailed`, remain blocked until user response for required checkpoints.
