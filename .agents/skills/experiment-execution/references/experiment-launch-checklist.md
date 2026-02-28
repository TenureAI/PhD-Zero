# Experiment Launch Checklist

Use this checklist before any real experiment launch.

Keep it short by default. Do not ask every item unless the run actually requires it.

## Default Checks

Start with these first:

1. Which codebase or repo are we using?
2. Is this single-node or multi-node?
3. Does the environment need a proxy?
4. Does logging or access depend on a specific system such as WandB, 1DP Login, or another platform key?

If these four are clear, continue execution and ask deeper questions only when needed.

## Conditional Follow-Ups

### If Multi-Node

- master host
- master port
- world size or worker count
- how to discover other nodes

### If Proxy Is Required

- proxy address or approved setup path
- whether worker nodes need the same proxy
- whether package downloads or tracker sync depend on it

### If Logging Or Login Uses An External System

- platform name
- project or workspace name if applicable
- whether the required key or login is already available
- any run naming rule if the platform requires it

## Minimal Safe Validation

Before the full launch, do the smallest useful check:

1. connectivity check if remote
2. environment check if activation is required
3. one-step smoke run if the experiment is expensive

## Launch Record

Record these after launch:

- exact launch command
- codebase used
- single-node or multi-node
- whether proxy was enabled
- session name or scheduler job ID if relevant
- tracker or login run ID if relevant
- primary log path
