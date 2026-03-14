# AI R&D Workspace

This workspace is for AI research and development tasks (reproduction, debugging, evaluation, training, and experiment planning).

## ⚠ Mandatory Skill Routing — MUST follow, violations are NOT acceptable

**Every non-trivial task MUST go through the skill pipeline via the `Skill` tool. Do NOT answer research questions, run experiments, or write papers by generating freeform text without first invoking the corresponding skill.**

### Routing Order (execute top-down, stop at the first matching rule)

1. **`research-workflow`** (PRIMARY ORCHESTRATOR) — invoke FIRST for any non-trivial task. All downstream skills below should be invoked FROM WITHIN research-workflow, not standalone.
2. **`deep-research`** — MANDATORY when user message contains ANY research-intent keyword:
   - Chinese: 调研/研究/对比/综述/文献/证据/机制/根因/为什么/可行性/路线图/分析/探索
   - English: research/investigate/compare/survey/literature/evidence/mechanism/root-cause/why/feasibility/roadmap/analyze/explore
   - **If ANY keyword matches → you MUST invoke `deep-research`. No exceptions. Skipping is a routing violation.**
3. **`experiment-execution`** — when user asks to run/launch/start/resume/monitor an experiment.
4. **`research-plan`** — when user asks for a proposal, roadmap, ablation plan, or study design.
5. **`paper-writing`** — ONLY when user explicitly asks to draft/write/revise a paper or section.
6. **`project-context`** — when environment setup or runtime fields are needed before execution.
7. **`run-governor`** — at run start to set mode + run_id.
8. **`memory-manager`** — bootstrap at run start, writeback at task end, trigger-based in between.
9. **`human-checkpoint`** — for safety risks, high-resource approvals, or hard blockers.

### Self-Check Before Every Reply

Before producing any substantive response, you MUST run this mental checklist:
1. Is this task non-trivial? → If yes, did I invoke `research-workflow`? If not, invoke it NOW.
2. Does the user message contain any research-intent keyword from rule 2? → If yes, did I invoke `deep-research`? If not, invoke it NOW.
3. Am I about to answer a research question with freeform text instead of skill output? → STOP. Invoke the skill first.

**Over-triggering is acceptable. Under-triggering is a violation.**

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
