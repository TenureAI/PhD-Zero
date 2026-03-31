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
3. Use `memory-manager` in `experience-first` mode: reusable `procedure/episode/insight` retrieval comes before relying on `working` state alone.
4. If you modify `memory-manager` or any Memory-related skill, or detect compaction markers in state/context files such as `Compact`, `压缩`, `Summary`, or similar summary/compression techniques, invoke `memory-manager` to read prior Memory before continuing so key context is not dropped.
5. Trigger `human-checkpoint` using mode-aware policy, always for major safety risks and shared-memory publication.
6. Use `experiment-execution` only for actual run execution, and keep ownership after launch for monitoring, diagnosis, recovery, and result collection.
7. Use `project-context` to collect and persist per-project private runtime context before experiments or report/eval execution.
8. Use `deep-research` as the default gateway for external search and deep external investigation, including early-stage project scoping when a user wants to write a research study or paper on a topic, unless the user is explicitly asking for a paper-writing deliverable right now.
9. Use `research-plan` when the user asks for a proposal, roadmap, ablation/evaluation plan, study design, or pre-implementation research decomposition.
10. After open-ended scoping in `deep-research`, hand off findings into `research-plan` by default; skip only if the user explicitly opts out.
11. Use `paper-writing` only when the user explicitly asks for a paper-writing deliverable such as drafting or revising a paper, section, or rebuttal. Do not use it for topic scoping, literature investigation, feasibility analysis, experiment design, or experiment execution.
12. Base conclusions on evidence only (command outputs, metrics, logs, and file diffs).
13. Prefer small, reversible, verifiable steps over broad speculative changes.
14. Follow `REPO_CONVENTIONS.md` for artifact placement and commit hygiene.
15. If a run was initialized before confirmation, stop and run violation recovery: acknowledge, ask whether to keep/clean artifacts, and wait for explicit reconfirmation before continuing.
16. **Mandatory Visualization**: Every report with quantitative results MUST include code-generated visualizations (matplotlib). Always generate figures when writing stage reports or final reports. If the report is complex, invoke `paper-writing` for polished formatting. Under-visualizing is a violation.
17. For long-running work, do not treat launch as completion: persist an action record, enter watch mode, poll on a model-chosen cadence, and continue until success criteria, a true blocker, or a gated approval point is reached.
18. Do not respond with the equivalent of "the job is running, come back later" unless the user explicitly requested fire-and-forget behavior.

## Persistent Optimization Guardrails
1. Interpret `full-auto` as an interruption policy, not a completion policy.
2. If the user says things such as “keep iterating”, “do not stop”, “try many iterations”, “until target”, or gives explicit target metrics like `90%` or `100%`, compile that into `persistent-optimization` behavior.
3. For persistent-optimization tasks, compile the user request into machine-checkable fields before execution:
   - `primary_target`
   - `promotion_gates`
   - `non_regression_guards`
   - `backup_policy`
   - `stop_allowed_only_if`
4. Do not leave stopping conditions as prose only when they can be converted into measurable gates.
5. If the user asks to preserve strong variants, snapshot best-so-far prompts/configs/code/results before higher-risk changes.
6. `full-auto` plus explicit persistence means the agent keeps ownership until one of these is true:
   - compiled hard targets are met
   - a true hard blocker remains after reasonable recovery attempts
   - a major safety/resource gate requires approval
   - the user explicitly changes or stops the objective

## Goal and Done Guardrails
1. At the start of each non-trivial execution loop, refresh the compiled goal state and active promotion gate.
2. `done` is allowed only when all compiled hard gates are satisfied with evidence.
3. If `completion_policy=until-target-or-hard-blocker`, `done` is forbidden while the active promotion gate or hard target remains unmet.
4. A single clean run, a partial fix, or one successful batch is not sufficient reason to stop.
5. If the current promotion gate is met but the final target is not, promote to the next gate instead of stopping.
6. If targets remain unmet and a safe next step exists, default to `iterate`.
7. If repeated attempts plateau or regress materially, default to `replan`.

## Short Iterative Execution Guardrails
1. Apply the same ownership standard to short local edit-evaluate loops as to long-running jobs.
2. For iterative optimization tasks, define an evaluation ladder before broadening scope:
   - baseline or previous-best reference
   - representative regression set
   - promotion gate for larger evaluation
   - final target evaluation
3. Prefer broader representative sets over a few hand-picked cases.
4. After each batch:
   - compare against baseline and best-so-far
   - inspect regressions, not only aggregate score
   - check non-regression guards
   - choose `iterate`, `replan`, or `promote-to-next-gate`
5. Do not stop after a single iteration merely because execution completed cleanly.
6. For prompts like “先用 30 个左右的题目集合测效果，再考虑上 100”, treat the smaller set as a required promotion gate rather than a suggestion.

## Long-Running Execution Guardrails
1. Classify an action as long-running when it is expected to exceed 5 minutes, launches async or remote work, is high-resource, or is likely to outlive the current model turn.
2. Before waiting on a long-running action:
   - persist `actions/<action_id>.yaml`
   - record command, cwd, expected duration, poll interval, log path, success/failure signals, and resume step
   - update working state with the active `action_id`
3. While the current session is active, use a watch loop:
   - model chooses sleep
   - poll the action
   - inspect `status`, `progress_changed`, `followup_action`, and recent logs
   - choose the next sleep or branch into diagnosis/result handling
4. Allowed liveness states are `pending`, `running`, `stalled`, `failed`, `completed`, and `cancelled`.
5. After every poll, keep ownership and branch immediately:
   - `continue-watch` or `wait-and-poll`
   - `collect-results`
   - `diagnose-stall`
   - `diagnose-failure`
   - `replan`
6. At the start of every resumed turn, reconcile active actions before unrelated planning.

## Memory Invocation Guardrails (Experience-First)
1. `memory-manager` is mandatory for non-trivial runs, but retrieval should center on reusable experience, not only `working` state.
2. Mandatory per non-trivial run:
   - one bootstrap `retrieve/init-working` before planning or execution
   - one close-out writeback before task completion
3. Mandatory per turn and per batch:
   - retrieve relevant memory on every new user turn
   - retrieve `procedure` before every execution batch
   - write a concise `working` delta after every execution batch
4. Mandatory trigger-based retrieval:
   - retrieve `episode` on significant failure, repeated attempt, stalled job, or new error signature
   - retrieve `insight` during planning, replanning, contradiction handling, tradeoff analysis, or final answer shaping
   - retrieve `procedure` plus relevant `episode` before high-resource or irreversible actions
   - reread `working` during resume, compaction recovery, long-action reconciliation, and final handoff
5. After long-action polls:
   - on `stalled` or `failed`, retrieve `procedure` plus relevant `episode` before the next fix attempt
   - on `completed`, retrieve `insight` when interpretation or next-step selection is needed
6. If memory is skipped due to duplicate retrieval, freshness, or low yield, record `memory_skip_reason`.

## Deep-Research Re-entry Guardrails
1. On every new user message, re-run skill routing before continuing prior stage actions.
2. If the new message contains research-intent signals, `deep-research` MUST be activated even mid-run.
3. Research-intent signals include (semantic match, Chinese or English):
   - 调研/研究/对比/综述/文献/证据/机制/根因/为什么/可行性/路线图
   - research/investigate/compare/survey/literature/evidence/mechanism/root-cause/why/feasibility/roadmap
4. All external search for non-trivial research runs must route through `deep-research`; do not bypass it with ad hoc search.
5. Every `deep-research` run must begin with a frontier-first scout before final depth selection.
6. Default depth is `default-auditable`; `light` is a downgrade path only after scout and may not be the silent default.
7. Do not claim deep-research completion without actual WebSearch calls and an auditable query trail.
8. If skipping `deep-research`, emit `dr_skip_reason` with concrete evidence freshness info (source date / timestamp), not a generic statement.
9. Cooldown for non-forced deep-research calls:
   - at most once per stage unless objective changed or new contradiction/high-impact uncertainty appears.

## Experiment Watch Guardrails
1. When `experiment-execution` launches a long-running training, evaluation, benchmark, or inference job, it must enter watch mode by default.
2. After each experiment poll:
   - if `running`, choose the next sleep interval and keep monitoring
   - if `completed`, inspect outputs, checkpoints, metrics, and artifacts immediately
   - if `stalled`, inspect evidence, retrieve memory, and attempt the smallest safe recovery or replan
   - if `failed`, diagnose immediately, retrieve memory, and attempt the smallest safe recovery
3. Unknown execution errors should follow this branch:
   - local evidence triage
   - `procedure` and `episode` retrieval
   - targeted search
   - `deep-research` if still unresolved or freshness-sensitive
   - minimal fix validation
4. Only allow fire-and-forget experiment behavior when the user clearly requested it.

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
