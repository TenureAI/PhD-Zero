# Remote Experiment Info Guide

Collect only missing information. Ask plain-language questions.

## Default Questions

1. Which repo/project path should be used?
2. Is this single-node or multi-node?
3. Does remote execution need a proxy?
4. Do logs or access depend on systems like WandB/1DP/other platform?

## Follow-Ups Only If Needed

- SSH target and auth details
- remote working directory
- session strategy (direct/tmux/scheduler)
- node topology details

## Interpretation Rules

1. If multi-node, require master and worker discovery details.
2. If proxy is needed, require concrete setup before full run.
3. If credentials are required, confirm availability.
4. If uncertainty remains, prefer smoke validation before full launch.
