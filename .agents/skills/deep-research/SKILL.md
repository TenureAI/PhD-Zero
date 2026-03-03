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
3. Search broadly across high-signal sources.
4. Extract claim-level evidence.
5. Verify high-impact claims independently.
6. Run contradiction/counter-evidence checks.
7. Synthesize and produce final report.

## Recency and Search Breadth

For evolving topics:

1. Prioritize newest 3-6 months first.
2. Expand to 24 months, then foundational references.
3. Log search pivots and coverage counters.
4. If recent evidence is weak, state the gap explicitly.

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

1. Output full report in chat.
2. Save exactly one final report file per deep-research run.
3. Default save path under run logs:
   - `<codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md`
4. If save fails, report failure reason and still provide full report in chat.

## Required Output Structure

Include at minimum:

1. As-of Date and Scope
2. Executive Synthesis
3. Comprehensive Analysis
4. Type-Specific Section(s)
5. Research Trail Summary
6. Conclusion and Next Step
7. Saved Report Path and Save Status
8. References
