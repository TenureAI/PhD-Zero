# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## Default Operating Rules
1. Start each non-trivial research task with `run-governor`, but do not initialize `run_id` paths before explicit user confirmation of both `mode` and execution target (`local|remote`).
2. Use `research-workflow` as the default orchestration loop.
3. Use `memory-manager` to maintain working todo state and long-term memory.
4. Trigger `human-checkpoint` using mode-aware policy, always for major safety risks and shared-memory publication.
5. Use `experiment-execution` only for actual run execution.
6. Use `project-context` to collect and persist per-project private runtime context before experiments or report/eval execution.
7. Use `deep-research` for deep external investigation and evidence synthesis, including early-stage project scoping when a user wants to write a research study or paper on a topic.
8. Use `research-plan` when the user asks for a proposal, roadmap, ablation/evaluation plan, study design, or pre-implementation research decomposition.
9. After open-ended scoping in `deep-research`, hand off findings into `research-plan` by default; skip only if the user explicitly opts out.
10. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
11. Prefer small, reversible, verifiable steps over broad speculative changes.
12. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.
13. If a run was initialized before confirmation, stop and run violation recovery: acknowledge, ask whether to keep/clean artifacts, and wait for explicit reconfirmation before continuing.

## Skill Paths
- `.agents/skills/run-governor`
- `.agents/skills/research-workflow`
- `.agents/skills/research-plan`
- `.agents/skills/memory-manager`
- `.agents/skills/human-checkpoint`
- `.agents/skills/experiment-execution`
- `.agents/skills/deep-research`
- `.agents/skills/project-context`
