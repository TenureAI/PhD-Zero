---
name: experiment-execution
description: Execute AI/ML experiments locally or remotely with explicit environment, runtime, node, and logging controls. Use when the task requires actual launch, monitoring, rerun, or recovery of experiments, and align interaction/confirmation behavior with the active run mode.
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

1. repo/project path
2. single-node or multi-node
3. proxy requirement
4. tracker/login requirement

Ask only missing questions.

## Run Path Policy

Use shared run_id from run-governor:

1. control logs and stage reports: `<codex-cwd>/logs/runs/<run_id>/`
2. experiment outputs: `<project-root>/runs/<run_id>/`

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
7. Replan on major failures.

## Unknown Error Branch

When execution fails with unknown error:

1. local evidence triage (stack, logs, env, recent diffs)
2. optional memory retrieval if likely useful
3. targeted search
4. deep research (debug-investigation) if unresolved
5. apply smallest fix and validate

Retry behavior should be mode-aware and evidence-driven.

## SSH and Remote Policy

1. Choose control mode: direct SSH, SSH+session manager, scheduler, or existing remote agent.
2. Declare remote model: remote-native or local-driver.
3. Validate connectivity and runtime basics before expensive launch when uncertainty exists.

## Logging and Failure Handling

Record stable paths for:

1. stdout/stderr
2. checkpoints
3. metrics
4. artifacts

On failures, record owner and cleanup plan.

## Stop Conditions

Do not launch full run when required inputs are still unknown and not explicitly waived.

In `full-auto`, continue only if risk is acceptable and no major safety issue exists.

## Output Contract

Emit execution state as:

```yaml
run_id: <id>
mode: <full-auto|moderate|detailed>
execution_mode: <local|ssh|ssh+tmux|scheduler|remote-agent>
remote_model: <remote-native|local-driver|n/a>
repo_path: <path>
output_path: <project-root>/runs/<run_id>
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
next_action: <smallest safe step>
checkpoint_needed: <yes|no>
```
