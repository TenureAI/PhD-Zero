# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## Default Operating Rules
1. Use `research-workflow` as the default execution loop for all non-trivial tasks.
2. Use `memory-manager` for memory retrieval, writeback, promotion, and shared export candidates.
3. Trigger `human-checkpoint` before high-cost, high-impact, or high-risk actions.
4. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
5. Prefer small, reversible, verifiable steps over broad speculative changes.
6. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.

## Skill Paths
- `.agents/skills/research-workflow`
- `.agents/skills/memory-manager`
- `.agents/skills/human-checkpoint`
- `.agents/skills/experiment-execution`
