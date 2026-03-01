# Experiment Launch Checklist

Use before real launches. Keep it minimal and mode-aware.

## Required First Checks

1. repo/project path
2. single-node vs multi-node
3. proxy needed?
4. tracker/login dependency?
5. active `run_id` and output path `<project-root>/runs/<run_id>`

## Conditional Checks

### Multi-node

- master host and port
- worker discovery source
- launcher type

### Proxy required

- proxy setup path/value
- worker-node applicability

### External tracker/login

- platform
- project/workspace name
- credential availability

## Smoke Rule

Run smoke only when information is incomplete or environment readiness is uncertain.

## Launch Record

Record:

- exact launch command
- run_id and output path
- node mode and assignment
- proxy state
- tracker run id (if any)
- primary logs path
