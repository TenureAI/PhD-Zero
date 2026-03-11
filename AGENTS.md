# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## Default Operating Rules
1. Start each non-trivial research task with `run-governor`, but do not initialize `run_id` paths before explicit user confirmation of both `mode` and execution target (`local|remote`).
2. Use `research-workflow` as the default orchestration loop.
3. Use `memory-manager` to maintain working todo state and long-term memory.
4. If you modify `memory-manager` or any Memory-related skill, or detect compaction markers in state/context files such as `Compact`, `压缩`, `Summary`, or similar summary/compression techniques, invoke `memory-manager` to read prior Memory before continuing so key context is not dropped.
5. Trigger `human-checkpoint` using mode-aware policy, always for major safety risks and shared-memory publication.
6. Use `experiment-execution` only for actual run execution.
7. Use `project-context` to collect and persist per-project private runtime context before experiments or report/eval execution.
8. Use `deep-research` for deep external investigation and evidence synthesis, including early-stage project scoping when a user wants to write a research study or paper on a topic, unless the user is explicitly asking for a paper-writing deliverable right now.
9. Use `research-plan` when the user asks for a proposal, roadmap, ablation/evaluation plan, study design, or pre-implementation research decomposition.
10. After open-ended scoping in `deep-research`, hand off findings into `research-plan` by default; skip only if the user explicitly opts out.
11. Use `paper-writing` only when the user explicitly asks for a paper-writing deliverable such as drafting or revising a paper, section, or rebuttal. Do not use it for topic scoping, literature investigation, feasibility analysis, experiment design, or experiment execution.
12. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
13. Prefer small, reversible, verifiable steps over broad speculative changes.
14. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.
15. If a run was initialized before confirmation, stop and run violation recovery: acknowledge, ask whether to keep/clean artifacts, and wait for explicit reconfirmation before continuing.

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

## Paper-Writing Trigger Guardrails
1. Activate `paper-writing` only when the user explicitly asks for a paper-writing output.
2. Valid triggers include drafting or revising a paper, a named paper section, or rebuttal text.
3. Do not activate `paper-writing` just because the request mentions papers, literature, comparisons, or related work if the actual need is still research, planning, or experiments.
4. If the user has not explicitly asked for paper-writing output, prefer `deep-research`, `research-plan`, or `experiment-execution` according to the current stage.

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
