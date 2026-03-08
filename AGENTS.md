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

## Memory Invocation Guardrails (Balanced)
1. `memory-manager` is mandatory for non-trivial runs, but only as a control-plane step, not per command.
2. Mandatory calls per non-trivial run:
   - one bootstrap `retrieve/init-working` before planning or execution
   - one close-out writeback before task completion
3. Conditional calls between bootstrap and close-out are trigger-based only:
   - stage change
   - replan
   - significant failure or new error signature
   - before high-resource action
   - before final report/answer handoff
4. Periodic refresh is allowed when either is true:
   - at least 15 minutes since last memory operation
   - at least 3 execution cycles since last memory operation
5. Cooldown rule: do not invoke `memory-manager` more than once in a cycle unless forced by safety/high-resource/failure triggers.
6. If memory is skipped due to cooldown or low delta, record `memory_skip_reason` in the stage report.

## Deep-Research Re-entry Guardrails
1. On every new user message, re-run skill routing before continuing prior stage actions.
2. If the new message contains research-intent signals, `deep-research` MUST be activated even mid-run.
3. Research-intent signals include (semantic match, Chinese or English):
   - 调研/研究/对比/综述/文献/证据/机制/根因/为什么/可行性/路线图
   - research/investigate/compare/survey/literature/evidence/mechanism/root-cause/why/feasibility/roadmap
4. If skipping `deep-research`, emit `dr_skip_reason` with concrete evidence freshness info (source date / timestamp), not a generic statement.
5. Cooldown for non-forced deep-research calls:
   - at most once per stage unless objective changed or new contradiction/high-impact uncertainty appears.

## Skill Paths
- `.agents/skills/run-governor`
- `.agents/skills/research-workflow`
- `.agents/skills/research-plan`
- `.agents/skills/memory-manager`
- `.agents/skills/human-checkpoint`
- `.agents/skills/experiment-execution`
- `.agents/skills/deep-research`
- `.agents/skills/project-context`
- `.agents/skills/paper-writing`

## Additional Skills
- `paper-writing`: Progressive-disclosure paper writing skill for CS/AI papers. Use when drafting or revising sections such as abstract, introduction, related work, method, figures, experiments, or rebuttal text. Includes section-specific references plus an arXiv source-fetch workflow for mining LaTeX organization from exemplar papers.
