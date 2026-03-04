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

1. execution target (`local|remote`)
2. local project root
3. runtime project root (required when remote)
4. single-node or multi-node
5. proxy requirement
6. tracker/login requirement

Ask only missing questions.

## Run Path Policy

Use shared run_id from run-governor:

1. control logs and stage reports: `<codex-cwd>/logs/runs/<run_id>/`
2. experiment outputs: `<runtime_project_root>/runs/<run_id>/`
3. project-context snapshots and secrets: `<local_project_root>/.project_local/<project_slug>/`

In local execution, `runtime_project_root` can be equal to `local_project_root`.

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
3. If project-context has remote profile, confirm reuse policy before launch.
4. Validate connectivity and runtime basics before expensive launch when uncertainty exists.

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
In `full-auto`, if remote profile is complete, reuse it by default unless explicitly overridden.

## Output Contract

Emit execution state as:

```yaml
run_id: <id>
mode: <full-auto|moderate|detailed>
execution_mode: <local|ssh|ssh+tmux|scheduler|remote-agent>
remote_model: <remote-native|local-driver|n/a>
local_project_root: <path>
runtime_project_root: <path>
output_path: <runtime_project_root>/runs/<run_id>
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
