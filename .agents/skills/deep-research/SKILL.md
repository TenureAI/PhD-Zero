---
name: deep-research
description: Conduct deep, evidence-first research for complex questions using broad discovery, verification, contradiction checks, and traceable citations. Use for early-stage project scoping when a user wants to write a research study or paper on a topic, and for idea exploration, debugging investigations, design decisions, implementation strategy, and conflict resolution. Adapt the report template by research type while keeping rigorous sourcing and depth.
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

## Default Workflow

Iterate until evidence quality is sufficient:

1. Restate objective and success criteria.
2. Set explicit `As of: YYYY-MM-DD`.
3. Run staged time-window search with Codex WebSearch.
4. Extract claim-level evidence.
5. Verify high-impact claims independently.
6. Run contradiction/counter-evidence checks.
7. Synthesize and produce final report.

## Completion Gate (Mandatory)

Do not output final conclusions until all gate checks pass.

Before synthesis, print:

1. `selected_mode=quick|default-auditable|deep`
2. `mode_reason=`
3. `total_queries=`
4. `frontier_queries=`
5. `recent_queries=`
6. `mid_term_queries=`
7. `classic_queries=`
8. `gate_pass=YES|NO`

Gate thresholds must be evaluated against the selected mode's minimums.

If `gate_pass=NO`, continue searching and do not finalize.

## Query Budget and Depth Rules

Support three depth modes:
Select one mode before search starts and record the reason.

1. `quick`:
   - total: 20-30
   - stage minimums: `frontier >= 6`, `recent >= 6`, `mid-term >= 4`, `classic >= 2`
2. `default-auditable`:
   - total: target 60 (acceptable 50-80)
   - stage minimums: `frontier >= 15`, `recent >= 15`, `mid-term >= 15`, `classic >= 10`
3. `deep`:
   - total: 100-140
   - stage minimums: `frontier >= 28`, `recent >= 24`, `mid-term >= 20`, `classic >= 12`

Mode selection precedence:

1. User override wins if explicitly specified (for example: `mode=quick|default-auditable|deep`).
2. If user does not specify, auto-select using scope and research-intent signals (not risk-first).
   - `quick`: only for simple, single-point, directly verifiable questions (definition checks, yes/no fact checks, one-paper claim verification).
   - `default-auditable`: default for all non-simple research questions with bounded scope.
   - `deep`: prioritize when scope is broad or open-ended, especially for research idea exploration ("can X and Y be combined", "how to design a roadmap", "landscape + recipe + tradeoffs").
3. If ambiguous, do not choose `quick`; choose `default-auditable` or `deep` based on breadth.
4. Practical guardrail: if the task asks for representative works plus training recipes/mechanisms, use `deep` by default.

If any stage minimum for the selected mode is missed, continue searching before synthesis.

## Search Execution Policy (Codex Native)

1. Use Codex WebSearch directly in-session; do not require external browser interaction.
2. Do not depend on external search APIs for baseline operation.
3. Add date hints in queries (`after:`/`before:`) as soft constraints.
4. Apply hard date validation after retrieval using source published date.
5. If source date is unknown, keep with uncertainty label and lower priority.
6. Do not claim deep-research completion without actual WebSearch calls and auditable query logs.

## Staged Time Windows (Paper-Centric)

Use four mandatory evidence stages and record source counts for each:

1. `frontier` (3-6 months)
   - window: `as_of - 180 days` to `as_of`
2. `recent` (within 1 year)
   - window: `as_of - 365 days` to `as_of`
3. `mid-term` (within 2 years)
   - window: `as_of - 730 days` to `as_of`
4. `classic` (older foundations)
   - window: older than `as_of - 730 days`

When discussing "latest" evidence, prioritize `frontier` first, then `recent`.

Allocate budget by stage (must bias to newer windows):

1. `frontier`: 35-45% of total queries
2. `recent`: 30-35% of total queries
3. `mid-term`: 15-20% of total queries
4. `classic`: 10-15% of total queries

## Stage Search Sequence

Per stage, run at least these query families:

1. canonical topic terms
2. synonym/alias expansion
3. counter-evidence and criticism
4. verification queries for high-impact claims

For `frontier` and `recent`, run at least 2 rounds of query expansion before moving on.

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

## Persistence Policy

1. Always output full report in chat.
2. Save exactly one final report file per deep-research run.
3. Default save path under run logs:
   - `<codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md`
4. If save fails, report failure reason and still provide full report in chat.

## Required Output Structure

Include at minimum:

1. As-of Date and Scope
2. Gate Check
3. Executive Synthesis
4. Comprehensive Analysis
5. Type-Specific Section(s)
6. Research Trail Summary
7. Conclusion and Next Step
8. Saved Report Path and Save Status
9. References

Additionally include stage coverage counters:

1. frontier_sources=
2. recent_sources=
3. mid_term_sources=
4. classic_sources=

Also include two auditable tables:

1. Query Log with fields: `query_id`, `stage`, `query_text`, `date_filter`, `hits_used`
2. Source Log with fields: `source_id`, `title`, `url`, `published_date`, `stage`, `primary_or_secondary`
