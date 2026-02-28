# Remote Experiment Info Guide

Use this guide to collect the minimum information needed to run an experiment remotely.

Do not send the user a YAML form. Ask concise plain-language questions and build the structured state yourself.

## Question Strategy

Ask only what is missing. Prefer small batches. A good default order is:

1. which codebase or repo should be used
2. whether the run is single-node or multi-node
3. whether the environment needs a proxy
4. whether logging or access depends on a specific system such as WandB, 1DP Login, or another platform key

## Suggested Plain-Language Questions

Use only the questions that are still needed.

### Default Opening Questions

- Which codebase or repo should I run?
- Is this single-node or multi-node?
- Does the remote environment need a proxy?
- Do logs or access depend on something specific such as WandB, 1DP Login, or another system key?

### Only If The User's Answer Requires It

- If multi-node: What is the master node, and how should I discover the other nodes?
- If proxy is needed: What proxy or approved setup should I use?
- If an external platform is involved: Is the required key or login already available?
- If the codebase is ambiguous: Which repo path, branch, or launch script should I use?
- If reading the repo reveals missing information: Ask the smallest follow-up question needed to resolve the actual launch command, config, dependency, or runtime assumption.

## Internal Normalization Targets

After collecting answers, normalize them internally into these buckets:

- codebase
- node mode
- proxy requirement
- external logging or auth requirement
- any follow-up details needed by the chosen setup

The normalized state is for agent use only. Do not require the user to express it in any specific format.

## Interpretation Rules

- If the run is multi-node, require master host and node discovery method before launch.
- If proxy is required, confirm the exact proxy or setup path before launch.
- If logging or access depends on WandB, 1DP Login, or another platform, confirm that the required key or login is available.
- If the run is expensive, perform a smoke validation unless the user explicitly waives it.
