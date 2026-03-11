# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## Default Operating Rules
1. Start each non-trivial research task with `run-governor` to select mode and initialize `run_id` paths.
2. Use `research-workflow` as the default orchestration loop.
3. Use `memory-manager` to maintain working todo state and long-term memory.
4. If you modify `memory-manager` or any Memory-related skill, or detect compaction markers in state/context files such as `Compact`, `压缩`, `Summary`, or similar summary/compression techniques, invoke `memory-manager` to read prior Memory before continuing so key context is not dropped.
5. Trigger `human-checkpoint` using mode-aware policy, always for major safety risks and shared-memory publication.
6. Use `experiment-execution` only for actual run execution.
7. Use `project-context` to collect and persist per-project private runtime context before experiments or report/eval execution.
8. Use `deep-research` for deep external investigation and evidence synthesis, including early-stage project scoping when a user wants to write a research study or paper on a topic.
9. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
10. Prefer small, reversible, verifiable steps over broad speculative changes.
11. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.

## Skill Paths
- `.agents/skills/run-governor`
- `.agents/skills/research-workflow`
- `.agents/skills/memory-manager`
- `.agents/skills/human-checkpoint`
- `.agents/skills/experiment-execution`
- `.agents/skills/deep-research`
- `.agents/skills/project-context`
