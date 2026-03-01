---
name: human-checkpoint
description: Escalate critical AI R&D decisions to a human with concise options, tradeoffs, and a recommended default. Use when the path is uncertain, action cost is high, impact is high, or risk of irreversible changes is significant. Trigger when requests mention approval, confirmation, checkpoint, risky change, expensive run, protocol change, or human_checkpoint.
---

# Human Checkpoint

## Mission
Request human decisions only at truly important points, with structured options and explicit consequences.

## Trigger Conditions
Trigger a checkpoint when any condition holds:
1. Path ambiguity: low evidence, conflicting signals, or multiple plausible routes with different outcomes.
2. High resource cost: long training, large sweeps, paid API spikes, or heavy compute occupancy.
3. High result impact: benchmark protocol changes, core hyperparameter policy changes, or strategic pivots.
4. High-risk writes: destructive file edits, shared resource mutation, remote publish, or shared-memory export.

## Do Not Trigger
Skip checkpoint for low-cost, reversible, and routine actions with clear evidence.

## Request Format
Send a concise decision request with this structure:
1. `Decision Needed`: one sentence.
2. `Context`: current state and key evidence.
3. `Options`: 2-3 mutually exclusive choices with tradeoffs.
4. `Recommendation`: default option and why.
5. `If Approved`: immediate next action.
6. `If Rejected`: fallback path.

## Option Design Rules
1. Make options executable now; avoid abstract framing.
2. Make tradeoffs explicit in cost, risk, and expected learning value.
3. Put the recommended option first.
4. Keep the request short enough for fast human response.

## After Decision
1. Execute only the approved option.
2. Record decision rationale and outcome into memory as evidence.
3. Re-evaluate whether another checkpoint is needed before the next high-impact action.

## Failure Handling
If no human response is available in time:
1. Choose the safest reversible path.
2. Avoid high-cost or high-risk actions.
3. Report blocked status with pending decision details.
