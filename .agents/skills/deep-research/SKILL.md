---
name: deep-research
description: |-
  Deep evidence-first research with broad discovery, verification, and traceable citations. Prefer invoking via research-workflow.
  TRIGGER when (MANDATORY — you MUST invoke this skill, no exceptions): user message contains ANY of these keywords or synonyms — 调研/研究/对比/综述/文献/证据/机制/根因/为什么/可行性/路线图/分析/探索, or research/investigate/compare/survey/literature/evidence/mechanism/root-cause/why/feasibility/roadmap/analyze/explore — or asks to verify claims, analyze tradeoffs, scope a new topic, or conduct literature review. Also use this skill as the default gateway for external search. Skipping when keywords match is a routing violation.
  DO NOT TRIGGER when: user asks for paper-writing output (use paper-writing), experiment launch (use experiment-execution), or plan-only without evidence (use research-plan).
---

# Deep Research

## Mission

Produce a deeply researched, evidence-grounded answer with clear provenance and actionable conclusions, and act as the default gateway for external search in research runs.

## Search Routing Gate (Mandatory)

All external search during non-trivial research runs must enter through `deep-research`.

Rules:

1. do not bypass `deep-research` with ad hoc direct search when fresh outside evidence is needed
2. `deep-research` may choose a lighter or deeper execution depth internally, but it may not silently skip actual search
3. every `deep-research` run must perform real WebSearch calls and keep an auditable query trail
4. if search is skipped because existing evidence is already fresh enough, emit `dr_skip_reason` with explicit date windows and source counts

## Research Type Selection

Choose a primary `research_type` early:

1. `idea-exploration`
2. `debug-investigation`
3. `design-decision`
4. `implementation-strategy`
5. `conflict-resolution`

If templates do not fit exactly, adapt structure freely but keep depth, verification, and citations.

## Intake Checkpoint Gate (Mandatory Before Search)

Before selecting depth or running any WebSearch queries:

1. confirm `intake_checkpoint_complete=YES`
2. intake must at least define: objective/scope, constraints, and expected deliverable format
3. route missing-information requests through `human-checkpoint`
4. in `moderate` or `detailed`, prefer built-in user-question tool (`request_user_input`)
5. if built-in tool is unavailable, degrade to concise plain-text questions
6. if intake is incomplete, remain in clarification phase and do not run search, decomposition, or synthesis

## Frontier-First Scout (Mandatory)

Every `deep-research` run must begin with a `frontier-first scout` before final depth selection.

Scout requirements:

1. run at least 6-10 queries total
2. cover at least:
   - `bleeding-edge` topic queries
   - `frontier` topic queries
   - one verification query family
   - one counter-evidence or criticism query family
3. capture representative freshness, source quality, and contradiction density
4. use scout evidence to choose final depth

Scout rules:

1. scout is mandatory even when a lighter depth is later selected
2. scout counts toward total query budget
3. scout may justify upgrading to `deep` or downgrading to `light`
4. scout may not justify "no search"

## Default Workflow

Iterate until evidence quality is sufficient:

1. confirm intake checkpoint is complete
2. restate objective and success criteria
3. set explicit `As of: YYYY-MM-DD`
4. run the mandatory frontier-first scout
5. select execution depth
6. run staged time-window search with Codex WebSearch
7. extract claim-level evidence
8. build key-work cards when the topic is paper-centric
9. verify high-impact claims independently
10. run contradiction/counter-evidence checks
11. synthesize and produce final report

When the topic has implementation, benchmark, reproduction, or planning implications, also apply [references/codebase-and-data-research-rules.md](references/codebase-and-data-research-rules.md).

## Re-entry Policy (Mid-Run)

When called during an ongoing run:

1. treat invocation as valid and do not require starting a new run by default
2. recompute objective delta versus current stage plan
3. if objective changed materially, reset research focus and run fresh query batches
4. if objective is similar, perform incremental deep research using existing evidence as baseline
5. if skipped due to sufficient evidence freshness, emit `dr_skip_reason` with explicit date windows and source counts

## Scoping-to-Planning Handoff Policy

When deep research is used for open-ended scoping (`idea-exploration`), hand off findings to `research-plan` as the required default next step. Skip only if the user explicitly opts out.

Handoff expectations:

1. preserve core hypotheses, constraints, and evidence-backed tradeoffs
2. identify recommended direction and at least one fallback direction
3. convert conclusions into executable planning inputs (experiments, implementation prerequisites, data/workload requirements, risks)

## Completion Gate (Mandatory)

Do not output final conclusions until all gate checks pass.

Before synthesis, print:

1. `intake_checkpoint_complete=YES|NO`
2. `intake_channel=request_user_input|plain-text-fallback|none`
3. `search_entry=deep-research`
4. `frontier_first_scout=YES|NO`
5. `selected_depth=light|default-auditable|deep`
6. `depth_reason=`
7. `dr_degrade_reason=`
8. `total_queries=`
9. `scout_queries=`
10. `bleeding_edge_queries=`
11. `frontier_queries=`
12. `recent_queries=`
13. `mid_term_queries=`
14. `classic_queries=`
15. `degrade_used=YES|NO`
16. `gate_pass=YES|NO`

If `degrade_used=YES`, also print:

1. `degrade_from=`
2. `degrade_to=`
3. `degrade_gap=`
4. `degrade_queries_run=`
5. `degrade_reason=`

If `gate_pass=NO`, continue searching and do not finalize.

## Search Depth Rules

Support three execution depths:

1. `light`
   - only for narrow, low-ambiguity verification after scout
   - total: 12-24 queries
   - stage minimums: `bleeding-edge >= 3`, `frontier >= 3`, `recent >= 2`, `mid-term >= 1`, `classic >= 1`
2. `default-auditable`
   - default for bounded but non-trivial research questions
   - total: target 50-80 queries
   - stage minimums: `bleeding-edge >= 12`, `frontier >= 10`, `recent >= 10`, `mid-term >= 8`, `classic >= 6`
3. `deep`
   - use for broad or open-ended exploration, roadmap design, deep comparisons, or high-uncertainty topics
   - total: 100-140 queries
   - stage minimums: `bleeding-edge >= 28`, `frontier >= 22`, `recent >= 20`, `mid-term >= 16`, `classic >= 10`

Selection rules:

1. user override wins if explicitly specified
2. if the user does not specify, default to `default-auditable`
3. select `deep` when scope is broad, open-ended, contradiction-heavy, or asks for landscape plus recipe or mechanism analysis
4. `light` is not a default mode
5. `light` is allowed only when scout confirms the task is narrow, directly verifiable, and low-ambiguity
6. if ambiguous, do not choose `light`
7. if the prompt mentions 2 or more research-intent terms, do not choose `light` unless the user explicitly forces it

## Depth Sanity Check (Mandatory Before Full Search)

Print this mini-check immediately after selecting depth:

1. `depth_candidate=`
2. `light_disqualifiers_hit=`
3. `open_ended_exploration=YES|NO`
4. `paper_centric=YES|NO`
5. `depth_sanity_pass=YES|NO`

Rules:

1. if `light_disqualifiers_hit` is non-empty and `depth_candidate=light`, set `depth_sanity_pass=NO` and reselect before more search
2. if `open_ended_exploration=YES` and user did not explicitly force `light`, do not use `light`
3. if `paper_centric=YES` and the user asks for mechanisms/recipes/comparisons, do not use `light`

## Search Execution Policy (Codex Native)

1. use Codex WebSearch directly in-session; do not require external browser interaction
2. do not depend on external search APIs for baseline operation
3. treat date text in query strings as recall hints only; do not rely on parser-specific `after:`/`before:` behavior for final stage assignment
4. use date-window targeting during retrieval, then assign stage by published-date validation
5. compute `days_from_as_of` for each source and map to exactly one stage using the stage boundary rules below
6. if source date is unknown, keep with uncertainty label and lower priority
7. do not claim deep-research completion without actual WebSearch calls and auditable query logs
8. prioritize `bleeding-edge`, then `frontier`, then `recent` whenever the user cares about the latest or fastest-moving evidence

## Staged Time Windows

Use five mandatory evidence stages and record source counts for each.
Define `days_from_as_of = as_of_date - published_date` (integer days). Stages are mutually exclusive:

1. `bleeding-edge` (0-90 days): `0 <= days_from_as_of <= 90`
2. `frontier` (91-180 days): `91 <= days_from_as_of <= 180`
3. `recent` (181-365 days): `181 <= days_from_as_of <= 365`
4. `mid-term` (366-730 days): `366 <= days_from_as_of <= 730`
5. `classic` (>730 days): `days_from_as_of > 730`

Freshness floor:

1. `bleeding-edge + frontier >= 35%` for normal runs
2. `bleeding-edge + frontier + recent >= 60%` for all finalized runs

## Stage Search Sequence

Per stage, run at least these query families:

1. canonical topic terms
2. synonym or alias expansion
3. counter-evidence and criticism
4. verification queries for high-impact claims

Use dynamic query-family expansion:

1. build seed terms from user question terms and canonical topic terms
2. expand with aliases discovered from high-confidence retrieved sources
3. do not hard-code universal mandatory method keywords for all topics

Minimum rounds by depth:

1. `light`: `bleeding-edge/frontier/recent >= 1`, `mid-term/classic >= 1`
2. `default-auditable`: `bleeding-edge/frontier/recent >= 3`, `mid-term >= 2`, `classic >= 1`
3. `deep`: `bleeding-edge/frontier/recent >= 4`, `mid-term >= 3`, `classic >= 2`

## Stage Deficit Degrade Policy

If a stage minimum is not met, allow controlled degradation only after an exhaustion pass.

Exhaustion pass minimums per deficit stage:

1. `light`: at least 6 additional stage-targeted queries
2. `default-auditable`: at least 18 additional stage-targeted queries
3. `deep`: at least 32 additional stage-targeted queries

Degrade rules:

1. only adjacent fallback is allowed: `bleeding-edge -> frontier`, `frontier -> recent`, `recent -> mid-term`
2. at most one degrade hop per stage
3. borrowed amount cannot exceed 50% of the deficit stage minimum
4. even after degradation, keep `bleeding-edge + frontier >= 30%` and `bleeding-edge + frontier + recent >= 60%`

## Memory and Search Policy

1. global memory bootstrap is mandatory for non-trivial runs
2. before heavy search batches, use the current memory snapshot or retrieve relevant `insight`/`procedure` memory when it can reduce redundant search or contradiction cost
3. when scout or full search uncovers a repeated issue already covered by memory, incorporate that memory explicitly rather than rediscovering it silently
4. use search directly and aggressively when the topic is new, urgent, or time-sensitive
5. if a lighter depth is chosen, report why `default-auditable` was not needed

## Type-Aware Reporting Requirements

Always include:

1. objective and scope
2. evidence-based conclusions
3. contradictions and uncertainties
4. anchored citations
5. research trail summary
6. saved report path

Type-specific emphasis:

1. `debug-investigation`
   - include error signature, reproduction context, fix candidates, validation outcomes
2. `design-decision`
   - compare alternatives, constraints, and cost/risk tradeoffs
3. `implementation-strategy`
   - include staged rollout options and operational prerequisites
4. `conflict-resolution`
   - focus on disputed claims, source reliability tiers, and resolution rationale
5. `idea-exploration`
   - include landscape, mechanisms, opportunities, and boundaries

## Representative Works Deep-Dive Policy

Trigger this policy when user asks for any of:

1. important works, representative papers, state of the art, or research landscape
2. method comparison across papers
3. roadmap or recipe requests grounded in prior work

When triggered, include a dedicated `Key Works Deep Dive` section and meet minimum coverage:

1. `light`: 3-5 key works
2. `default-auditable`: 6-10 key works
3. `deep`: 10-15 key works

For each key work, provide:

1. problem addressed
2. method or training objective
3. setup and data regime
4. headline results and where they hold
5. limitations or failure boundary
6. why the work matters to the user's question
7. primary citation

## Evidence and Citation Policy

1. cite in text as `[[S#]](#ref-s#)`
2. keep references anchored with published and accessed dates
3. distinguish fact, inference, and uncertainty
4. prefer canonical primary sources
5. do not rely on weak secondary sources for core conclusions

## Quality Gate

Finalize only when:

1. major claims are verified or clearly marked uncertain
2. contradictions are addressed or left as explicit open issues
3. citations are complete and internally consistent
4. report depth matches task type
5. language matches user language
6. if paper-centric policy is triggered, key-work count meets selected depth minimum
7. every finalized search run recorded scout plus full-query totals
8. if degradation is used, exhaustion minimums and freshness floor are explicitly satisfied and reported
9. the selected depth passed `Depth Sanity Check`

## Persistence Policy

1. always output full report in chat
2. save exactly one final report file per deep-research run
3. default save path under run logs:
   - `<codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md`
