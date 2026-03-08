# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## Default Operating Rules
1. Start each non-trivial research task with `run-governor` to select mode and initialize `run_id` paths.
2. Use `research-workflow` as the default orchestration loop.
3. Use `memory-manager` to maintain working todo state and long-term memory.
4. Trigger `human-checkpoint` using mode-aware policy, always for major safety risks and shared-memory publication.
5. Use `experiment-execution` only for actual run execution.
6. Use `project-context` to collect and persist per-project private runtime context before experiments or report/eval execution.
7. Use `deep-research` for deep external investigation and evidence synthesis, including early-stage project scoping when a user wants to write a research study or paper on a topic.
8. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
9. Prefer small, reversible, verifiable steps over broad speculative changes.
10. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.

## Skill Paths
- `.agents/skills/run-governor`
- `.agents/skills/research-workflow`
- `.agents/skills/memory-manager`
- `.agents/skills/human-checkpoint`
- `.agents/skills/experiment-execution`
- `.agents/skills/deep-research`
- `.agents/skills/project-context`
- `.agents/skills/paper-writing`

## Additional Skills
- `paper-writing`: Progressive-disclosure paper writing skill for CS/AI papers. Use when drafting or revising sections such as abstract, introduction, related work, method, figures, experiments, or rebuttal text. Includes section-specific references plus an arXiv source-fetch workflow for mining LaTeX organization from exemplar papers.
