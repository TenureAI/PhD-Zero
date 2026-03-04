# Experiment Launch Checklist

Use before real launches. Keep it minimal and mode-aware.

## Required First Checks

1. execution target (`local|remote`)
2. local project root and runtime project root resolved
3. if remote, confirm whether to reuse stored project-context remote profile
4. single-node vs multi-node
5. proxy needed?
6. tracker/login dependency?
7. active `run_id` and output path `<runtime_project_root>/runs/<run_id>`

## Conditional Checks

### Remote target

- runtime host reachable
- runtime project root exists or can be created
- remote profile reuse decision recorded

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
