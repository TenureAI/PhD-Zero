---
name: experiment-execution
description: Execute AI/ML experiments locally or on remote infrastructure with explicit environment, orchestration, logging, and node-management requirements. Use when the user wants to run training, evaluation, fine-tuning, benchmarking, long-running scripts, remote jobs, cluster launches, tmux sessions, SSH execution, distributed jobs, log collection, or experiment reruns. Trigger only when the task is about actually executing experiments rather than only planning or editing code.
---

# Experiment Execution

## Mission
Run experiments safely and reproducibly, especially on remote machines and multi-node environments.

Use this skill only when the task involves actual execution: launching scripts, preparing runtime environments, scheduling jobs, attaching to sessions, monitoring progress, or collecting logs.

## References
Read these only when needed:

- `references/experiment-launch-checklist.md`
  Read before a real launch, rerun, or distributed execution. Use it as a minimal preflight checklist, not a full questionnaire.
- `references/remote-info-template.md`
  Read when remote host, node, proxy, credential, tracker, or logging information is incomplete. Use it to drive a short interview with the user. Do not ask the user to fill YAML or any other structured format manually. Ask concise plain-language questions, then normalize the answers yourself.

## Required Inputs
Before execution, collect only the minimum safe inputs:

1. Which codebase or repo should be used.
2. Whether the execution is single-node or multi-node.
3. Whether a proxy is required in the remote environment.
4. Whether logging or authentication depends on a specific system such as WandB, 1DP Login, or another internal platform.

Only ask follow-up questions when one of these answers implies more detail is required.

## Information Collection Style
Do not ask the user to complete forms, YAML, JSON, or long questionnaires.

Instead:

1. ask only the missing questions
2. use plain language
3. start with 3 to 4 high-value questions at most
4. summarize the answers back into an internal structured state
5. continue execution once the minimum safe information is available

If the user gives partial or messy information, extract what is usable and only ask for the gaps that block safe execution.

## Default First Questions
Unless the user already provided them, start from these:

1. Which codebase or repo should I run?
2. Is this single-node or multi-node?
3. Does the remote environment need a proxy?
4. Do logs or access depend on something specific such as WandB, 1DP Login, or another platform key?

## Execution Policy
Follow this order:

1. Confirm whether the user wants real execution or only a dry-run plan.
2. Confirm the codebase, node mode, proxy requirement, and any external logging or auth dependency.
3. Inspect existing run scripts, launch wrappers, and prior logs only as needed.
4. Ask deeper follow-up questions only when the chosen setup requires them.
5. After inspecting the target codebase, continue asking targeted follow-up questions if the repository reveals missing launch details, unclear dependencies, or ambiguous runtime assumptions.
6. Prefer the smallest validation step first: connectivity test, env check, one-process smoke run, or one-node dry run.
7. Trigger `human-checkpoint` before expensive launches, distributed training, destructive cleanup, or secret/proxy changes.
8. Record all launch commands, node assignments, log locations, and experiment IDs as evidence.

## 1. SSH And Remote Execution

### 1.1 Choose the Control Mode
Classify the execution path into one of these modes:

1. Direct SSH command execution
   Use when the task is simple, short-lived, or easy to retry.
2. SSH plus tmux or screen session
   Use for long-running jobs that need reattachment and manual monitoring.
3. Scheduler or platform wrapper
   Use when the environment depends on Slurm, Kubernetes, Ray, internal launchers, or similar orchestration.
4. Preinstalled remote agent environment
   Use only when a remote agent environment already exists on the machine and can operate there directly. This is optional, not required.

Do not assume these modes are interchangeable. The difference matters for path resolution, environment loading, persistence, observability, and failure recovery.

### 1.2 Decide Between Two Remote Models
Treat these as different operating models:

1. Remote-native model
   A remote agent environment is already available on the machine. Work happens on the server itself.
2. Local-driver model
   Codex runs locally and every action is sent through SSH commands to the remote machine.

For each run, make the model explicit before proceeding, but do not assume a remote agent environment exists.

### 1.3 Remote Access Details
Do not collect all remote details upfront. Confirm only what is needed for the chosen path.

Typical follow-ups are:

- SSH target: host, port, username, and jump host if needed
- auth method: key path, agent forwarding, or other approved method
- working directory on remote host
- shell init behavior: `.bashrc`, `.zshrc`, conda activation, module load, etc.
- persistent session strategy: none, tmux, screen, nohup, scheduler
- file transfer path if code or configs must be synced

### 1.4 Minimal Remote Validation
Use a low-cost validation sequence first:

1. verify connectivity
2. print hostname, user, and working directory
3. inspect GPU and CUDA visibility if relevant
4. verify Python or launcher binary
5. run a tiny smoke command before the real launch

## 2. Development And Experiment Conventions

### 2.1 Repository Hygiene
When execution requires repo changes or temporary scripts:

- keep reusable execution logic in the repo
- keep task-specific notes under `docs/`
- keep local runtime state and scratch outputs under `workspace/` or `WORKSPACE/`
- do not mix one-off experiment artifacts into reusable skill directories
- prefer checked-in launch scripts for stable workflows; prefer ignored temporary scripts for one-off debugging

Follow `REPO_CONVENTIONS.md` if this repository is the control repo.

### 2.2 Experiment Recording
Do not assume a logging platform. First ask whether a specific tracking or login system is required.

Common options:

1. tracker-backed
   Example: WandB or another experiment platform.
2. file-backed
   Example: structured log files, JSON metrics, TensorBoard event files, local summaries.
3. mixed
   External tracker plus local logs and artifacts.

For tracker-backed or platform-backed runs, confirm only the required details:

- project or workspace name
- run naming convention
- required API key or login state
- whether offline mode is acceptable
- artifact upload expectations

If credentials are required, the user must provide or confirm them. This includes systems such as WandB, 1DP Login, or other internal platforms. Do not invent or silently reuse secrets.

### 2.3 Proxy And Network Rules
Proxy is a top-level early question because it can block almost everything else.

If proxy is needed, then determine the exact setup:

- whether HTTP or HTTPS proxy is required
- whether package mirrors are required
- whether outbound access is restricted on worker nodes
- whether tracker endpoints are reachable from the remote environment

If proxy configuration is needed, ask the user for the exact settings or the approved setup path.

## 3. User, Node, And Log Information

### 3.1 Multi-Stage Or Multi-Node Inputs
Ask for these only when the run is multi-node or multi-stage:

- master node hostname or address
- port requirements
- world size, node rank, and GPU count per node
- job launcher style: torchrun, deepspeed, accelerate, slurm, mpi, custom wrapper
- per-node workspace path consistency

### 3.2 Discovering Other Nodes
When the cluster topology is not fully specified, gather it from the available source of truth:

1. scheduler allocation output
2. hostfile
3. cluster environment variables
4. existing launch scripts
5. user-provided node inventory

Do not hardcode node lists without evidence.

### 3.3 Logging And Failure Handling
Keep logging questions minimal unless the user asks for a stricter protocol. Default to a discoverable stdout log path and expand only if needed.

If more detail is needed, define:

- primary log file path
- stderr handling
- checkpoint path
- metrics path
- retry or resume strategy
- who owns cleanup of failed runs

Prefer log locations that are stable and discoverable. If a session manager is used, record its session name.

## Output Contract
When this skill is used, structure the execution state like this:

```yaml
execution_mode: <local|ssh|ssh+tmux|scheduler|remote-agent>
remote_model: <remote-native|local-driver|n/a>
repo_path: <path>
environment:
  python: <path or version>
  env: <conda/venv/module>
  proxy_needed: <yes|no|unknown>
tracking:
  mode: <wandb|files|mixed|unknown>
  run_id: <id or pending>
node_plan:
  master: <host or n/a>
  workers: <list or pending>
logs:
  stdout: <path>
  artifacts: <path>
next_action: <smallest safe next step>
checkpoint_needed: <yes|no>
```

## Stop Conditions
Do not launch the full experiment until the following are clear or explicitly waived by the user:

- codebase to run
- single-node vs multi-node
- proxy requirement if relevant
- tracker or login credential strategy if relevant

If any of these are missing, ask targeted questions instead of guessing.
