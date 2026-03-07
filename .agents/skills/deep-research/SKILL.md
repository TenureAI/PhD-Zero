---
name: deep-research
description: Conduct deep, evidence-first research for complex questions using broad discovery, verification, contradiction checks, and traceable citations. Use for idea exploration, debugging investigations, design decisions, implementation strategy, and conflict resolution. Adapt the report template by research type while keeping rigorous sourcing and depth.
---

# Deep Research

## Mission

Produce a deeply researched, evidence-grounded answer with clear provenance and actionable conclusions.

## Research Type Selection

Choose a primary `research_type` early:

1. `idea-exploration`
2. `debug-investigation`
3. `design-decision`
4. `implementation-strategy`
5. `conflict-resolution`

If templates do not fit exactly, adapt structure freely but keep depth, verification, and citations.

## Intake Checkpoint Gate (Mandatory Before Search)

Before selecting mode or running any WebSearch queries:

1. Confirm `intake_checkpoint_complete=YES`.
2. Intake must at least define: objective/scope, constraints, and expected deliverable format.
3. Route missing-information requests through `human-checkpoint`.
4. In `moderate` or `detailed`, prefer built-in user-question tool (`request_user_input`).
5. If built-in tool is unavailable, degrade to concise plain-text questions.
6. If intake is incomplete, remain in clarification phase and do not run search, decomposition, or synthesis.

## Default Workflow

Iterate until evidence quality is sufficient:

1. Confirm intake checkpoint is complete.
2. Restate objective and success criteria.
3. Set explicit `As of: YYYY-MM-DD`.
4. Run staged time-window search with Codex WebSearch.
5. Extract claim-level evidence.
6. Build key-work cards when the topic is paper-centric.
7. Verify high-impact claims independently.
8. Run contradiction/counter-evidence checks.
9. Synthesize and produce final report.

## Scoping-to-Planning Handoff Policy

When deep research is used for open-ended scoping (`idea-exploration`), hand off findings to `research-plan` as the required default next step. Skip only if the user explicitly opts out.

Handoff expectations:

1. Preserve core hypotheses, constraints, and evidence-backed tradeoffs.
2. Identify recommended direction and at least one fallback direction.
3. Convert conclusions into executable planning inputs (experiments, implementation prerequisites, data/workload requirements, risks).

## Completion Gate (Mandatory)

Do not output final conclusions until all gate checks pass.

Before synthesis, print:

1. `intake_checkpoint_complete=YES|NO`
2. `intake_channel=request_user_input|plain-text-fallback|none`
3. `selected_mode=quick|default-auditable|deep`
4. `mode_reason=`
5. `total_queries=`
6. `bleeding_edge_queries=`
7. `frontier_queries=`
8. `recent_queries=`
9. `mid_term_queries=`
10. `classic_queries=`
11. `degrade_used=YES|NO`
12. `gate_pass=YES|NO`

If `degrade_used=YES`, also print:

1. `degrade_from=`
2. `degrade_to=`
3. `degrade_gap=`
4. `degrade_queries_run=`
5. `degrade_reason=`

Gate thresholds must be evaluated against the selected mode's minimums.

If `gate_pass=NO`, continue searching and do not finalize.

## Query Budget and Depth Rules

Support three depth modes:
Select one mode before search starts and record the reason.

1. `quick`:
   - total: 20-30
   - stage minimums: `bleeding-edge >= 5`, `frontier >= 4`, `recent >= 4`, `mid-term >= 3`, `classic >= 2`
2. `default-auditable`:
   - total: target 60 (acceptable 50-80)
   - stage minimums: `bleeding-edge >= 12`, `frontier >= 10`, `recent >= 10`, `mid-term >= 8`, `classic >= 6`
3. `deep`:
   - total: 100-140
   - stage minimums: `bleeding-edge >= 28`, `frontier >= 22`, `recent >= 20`, `mid-term >= 16`, `classic >= 10`

Mode selection precedence:

1. User override wins if explicitly specified (for example: `mode=quick|default-auditable|deep`).
2. If user does not specify, auto-select using scope and research-intent signals (not risk-first).
   - `quick`: only for simple, single-point, directly verifiable questions (definition checks, yes/no fact checks, one-paper claim verification).
   - `default-auditable`: default for all non-simple research questions with bounded scope.
   - `deep`: prioritize when scope is broad or open-ended, especially for research idea exploration ("can X and Y be combined", "how to design a roadmap", "landscape + recipe + tradeoffs").
3. If ambiguous, do not choose `quick`; choose `default-auditable` or `deep` based on breadth.
4. Practical guardrail: if the task asks for representative works plus training recipes/mechanisms, use `deep` by default.
5. `quick` hard disqualifiers (if any item is true, `quick` is forbidden):
   - user asks for research/landscape/survey/roadmap/recipe/mechanism comparison
   - user asks whether two methods can be combined and how to do it
   - paper-centric deep-dive policy is triggered
   - task requires contradiction analysis instead of a single factual verification
6. Mandatory auto-selection algorithm when user does not specify mode:
   - step A: check `quick` hard disqualifiers; if any true, candidate mode must be `default-auditable` or `deep`
   - step B: if request is open-ended idea exploration (for example "can X and Y be combined", "give landscape + recipe + tradeoffs"), select `deep`
   - step C: otherwise select `default-auditable`
7. Language robustness rule: map intent by semantics, not language surface. Treat equivalent Chinese and English phrases (for example "研究"/"research", "调研"/"investigate", "综述"/"survey", "路线图"/"roadmap", "可不可以结合"/"can X and Y be combined", "怎么做"/"how to implement") as identical depth signals.

If any stage minimum for the selected mode is missed, continue searching before synthesis.

## Mode Sanity Check (Mandatory Before Search)

Print this mini-check immediately after selecting mode:

1. `mode_candidate=`
2. `quick_disqualifiers_hit=`
3. `open_ended_exploration=YES|NO`
4. `paper_centric=YES|NO`
5. `mode_sanity_pass=YES|NO`

Rules:

1. If `quick_disqualifiers_hit` is non-empty and `mode_candidate=quick`, set `mode_sanity_pass=NO` and reselect mode before any query.
2. If `open_ended_exploration=YES` and user did not explicitly force `quick`, do not use `quick`.
3. If `paper_centric=YES` and user asks for mechanisms/recipes/comparisons, do not use `quick`.

## Mode Regression Examples (Use as Tie-Breakers)

1. Prompt: "验证论文 X 的某个具体结论是否成立" / "Verify whether claim X in paper Y holds" -> expected `quick`
2. Prompt: "帮我调研 A 方法和 B 方法的差异与适用边界" / "Compare method A vs B and their boundaries" -> expected `default-auditable`
3. Prompt: "用 deep research 研究 SFT 和 RL 能不能结合，给训练路线" / "Use deep research to study whether SFT and RL can be combined and propose a recipe" -> expected `deep`
4. Prompt: "给出这个方向的重要论文和方法演进，并提供落地 recipe" / "Provide key papers, method evolution, and an implementation recipe" -> expected `deep`
5. Prompt: "最近 3 个月某模型价格是否变动" / "Did this model's price change in the last 3 months?" -> expected `quick`
6. Prompt: "写一份该技术路线的文献综述（含反证）" / "Write a literature review with contradictions/counter-evidence" -> expected `default-auditable` or `deep` (prefer `deep` when open-ended)
7. Multilingual intent-trigger rule: if 2+ intent terms appear, never `quick`.
   - Chinese terms: "研究", "调研", "综述", "路线图", "机制", "对比", "可不可以结合", "怎么做"
   - English terms: "research", "investigate", "survey", "landscape", "roadmap", "mechanism", "compare", "can be combined", "how to implement"

## Search Execution Policy (Codex Native)

1. Use Codex WebSearch directly in-session; do not require external browser interaction.
2. Do not depend on external search APIs for baseline operation.
3. Treat date text in query strings as recall hints only; do not rely on parser-specific `after:`/`before:` behavior for final stage assignment.
4. Use date-window targeting during retrieval (for example recency filters and window-scoped query batches), then assign stage by automatic published-date validation.
5. Compute `days_from_as_of` for each source and map to exactly one stage using the stage boundary rules below.
6. If source date is unknown, keep with uncertainty label and lower priority.
7. Do not claim deep-research completion without actual WebSearch calls and auditable query logs.

## Staged Time Windows (Paper-Centric)

Use five mandatory evidence stages and record source counts for each.
Define `days_from_as_of = as_of_date - published_date` (integer days). Stages are mutually exclusive:

1. `bleeding-edge` (0-90 days): `0 <= days_from_as_of <= 90`
2. `frontier` (91-180 days): `91 <= days_from_as_of <= 180`
3. `recent` (181-365 days): `181 <= days_from_as_of <= 365`
4. `mid-term` (366-730 days): `366 <= days_from_as_of <= 730`
5. `classic` (>730 days): `days_from_as_of > 730`

When discussing "latest" evidence, prioritize `bleeding-edge`, then `frontier`, then `recent`.

Allocate budget by stage (must bias to newer windows):

1. `bleeding-edge`: 15-25% of total queries
2. `frontier`: 12-22% of total queries
3. `recent`: 16-26% of total queries
4. `mid-term`: 12-22% of total queries
5. `classic`: 8-15% of total queries

Freshness floor:

1. `bleeding-edge + frontier >= 35%` (normal)
2. `bleeding-edge + frontier + recent >= 60%` (normal and degraded)

## Stage Search Sequence

Per stage, run at least these query families:

1. canonical topic terms
2. synonym/alias expansion
3. counter-evidence and criticism
4. verification queries for high-impact claims

Use dynamic query-family expansion:

1. Build seed terms from user question terms and canonical topic terms.
2. Expand with method aliases discovered from high-confidence retrieved sources.
3. Do not hard-code universal mandatory method keywords for all topics.

Round definitions:

1. A round is one expansion pass for a stage and may add 1-3 queries per stage.
2. Query-family coverage is checked at stage completion, not required in every single round.

Minimum rounds by mode:

1. `quick`: `bleeding-edge/frontier/recent >= 2` rounds, `mid-term/classic >= 1` round
2. `default-auditable`: `bleeding-edge/frontier/recent >= 3` rounds, `mid-term >= 2` rounds, `classic >= 1` round
3. `deep`: `bleeding-edge/frontier/recent >= 4` rounds, `mid-term >= 3` rounds, `classic >= 2` rounds

## Stage Deficit Degrade Policy (Allowed with Exhaustion)

If a stage minimum is not met, allow controlled degradation only after an exhaustion pass.

Exhaustion pass minimums (per deficit stage):

1. `quick`: at least 8 additional stage-targeted queries
2. `default-auditable`: at least 18 additional stage-targeted queries
3. `deep`: at least 32 additional stage-targeted queries
4. The additional queries must cover all four query families and at least one extra expansion round beyond mode minimum.

Degrade rules:

1. Only adjacent fallback is allowed: `bleeding-edge -> frontier`, `frontier -> recent`, `recent -> mid-term`.
2. At most one degrade hop per stage.
3. Borrowed amount cannot exceed 50% of the deficit stage minimum.
4. Even after degradation, keep `bleeding-edge + frontier >= 30%` and `bleeding-edge + frontier + recent >= 60%`.

## Memory and Search Policy

1. Memory lookup is optional and situational.
2. Use memory when likely to reduce repeated search effort.
3. Use search/deep research directly when topic is new, urgent, or time-sensitive.
4. If memory is skipped, note reason in report trail.

## Type-Aware Reporting Requirements

Always include:

1. objective and scope
2. evidence-based conclusions
3. contradictions/uncertainties
4. anchored citations
5. research trail summary
6. saved report path

Type-specific emphasis:

1. `debug-investigation`
   - include error signature, reproduction context, fix candidates, validation outcomes
   - benchmark/matrix sections are optional unless directly relevant
2. `design-decision`
   - compare alternatives, constraints, cost/risk tradeoffs
3. `implementation-strategy`
   - include staged rollout options and operational prerequisites
4. `conflict-resolution`
   - focus on disputed claims, source reliability tiers, and resolution rationale
5. `idea-exploration`
   - include landscape, mechanisms, opportunities, and boundaries

## Representative Works Deep-Dive Policy (Mandatory for Paper-Centric Topics)

Trigger this policy when user asks for any of:

1. "important works", "representative papers", "state of the art", "research landscape"
2. method comparison across papers (for example: SFT vs RLHF vs DPO)
3. roadmap/recipe requests grounded in prior work

When triggered, include a dedicated `Key Works Deep Dive` section and meet minimum coverage:

1. `quick`: 3-5 key works
2. `default-auditable`: 6-10 key works
3. `deep`: 10-15 key works

For each key work, provide all required fields:

1. problem addressed (1-2 lines)
2. method/training objective (with concrete loss/optimization framing if available)
3. setup and data regime (what supervision/reward signal is used)
4. headline results and where they hold
5. limitations or failure boundary
6. why this work matters to the user's question
7. citation(s), with primary source required for every key work

Depth constraints:

1. Do not list papers as one-line bullets only.
2. Keep at least two works with explicit contradiction or negative evidence discussion.
3. Prefer tables for side-by-side comparison, then add short narrative synthesis.

## Evidence and Citation Policy

1. Cite in text as `[[S#]](#ref-s#)`.
2. Keep references anchored with published and accessed dates.
3. Distinguish fact, inference, and uncertainty.
4. Prefer canonical primary sources.
5. Do not rely on weak secondary sources for core conclusions.

## Quality Gate

Finalize only when:

1. major claims are verified or clearly marked uncertain
2. contradictions are addressed or left as explicit open issues
3. citations are complete and internally consistent
4. report depth matches task type
5. language matches user language
6. if paper-centric policy is triggered, key-work count meets selected mode minimum
7. if paper-centric policy is triggered, each key work has required fields and a primary citation
8. if degradation is used, exhaustion minimums and freshness floor are explicitly satisfied and reported
9. mode choice passed `Mode Sanity Check`; if not, rerun with corrected mode before finalizing

## Persistence Policy

1. Always output full report in chat.
2. Save exactly one final report file per deep-research run.
3. Default save path under run logs:
   - `<codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md`
4. If save fails, report failure reason and still provide full report in chat.

## Required Output Structure

Include at minimum:

1. As-of Date and Scope
2. Intake Checkpoint Status
3. Gate Check
4. Executive Synthesis
5. Comprehensive Analysis
6. Key Works Deep Dive (when paper-centric policy is triggered)
7. Type-Specific Section(s)
8. Research Trail Summary
9. Conclusion and Next Step
10. Saved Report Path and Save Status
11. References

Additionally include stage coverage counters:

1. bleeding_edge_sources=
2. frontier_sources=
3. recent_sources=
4. mid_term_sources=
5. classic_sources=

Also include two auditable tables:

1. Query Log with fields: `query_id`, `stage`, `query_text`, `date_filter`, `hits_used`
2. Source Log with fields: `source_id`, `title`, `url`, `published_date`, `stage`, `primary_or_secondary`

If paper-centric policy is triggered, include a third auditable table:

3. Key Works Matrix with fields: `work_id`, `method_family`, `supervision_signal`, `optimization_type`, `main_gain`, `known_risk`, `best_use_case`

If degradation is used, include a fourth auditable table:

4. Degrade Log with fields: `stage`, `required_min`, `achieved_before_degrade`, `additional_queries_run`, `fallback_stage`, `borrowed_count`, `reason`
