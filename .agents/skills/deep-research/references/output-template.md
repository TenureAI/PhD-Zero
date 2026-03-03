# Deep Research Output Template

Use this as a base scaffold. Keep rigor, but adapt modules by `research_type`.

```markdown
## As-of Date and Scope

- As of: YYYY-MM-DD
- Research type: <type>
- Scope: included/excluded items

## Executive Synthesis

- 3-6 bullets
- direct conclusion first

## Comprehensive Analysis

### A. Core Findings
Claim-level analysis with citations [[S1]](#ref-s1).

### B. Verification and Counter-Evidence
What was cross-checked, what conflicts remain.

### C. Implications
Operational or decision implications.

## Key Works Deep Dive (Paper-Centric Only)

Include 6-10 works for default-auditable (or mode-based threshold from SKILL.md).

| Work | Problem | Method/Objective | Supervision Signal | Main Gain | Limitation | Why it matters here |
|---|---|---|---|---|---|---|
| InstructGPT [[S1]](#ref-s1) | ... | ... | ... | ... | ... | ... |

Then add short narrative:
- which methods are strongest under which conditions
- where evidence conflicts
- what is still uncertain

## Type-Specific Section

- For `debug-investigation`: error signature, reproduction, fix candidates, validation table.
- For `design-decision`: option comparison table (cost/risk/benefit).
- For `implementation-strategy`: staged rollout and prerequisites.
- For `conflict-resolution`: dispute map and source-tier arbitration.
- For `idea-exploration`: landscape and opportunity boundaries.

## Research Trail Summary

- queries_run=
- sources_opened=
- pivots=
- dropped_sources=
- query_budget_total=
- query_budget_bleeding_edge=
- query_budget_frontier=
- query_budget_recent=
- query_budget_mid_term=
- query_budget_classic=
- bleeding_edge_sources=
- frontier_sources=
- recent_sources=
- mid_term_sources=
- classic_sources=
- key_works_included=
- freshness_coverage_bleeding_frontier=
- freshness_coverage_bleeding_frontier_recent=
- degrade_used=YES|NO
- degrade_from=
- degrade_to=
- degrade_gap=
- degrade_queries_run=
- degrade_reason=

## Conclusion and Next Step

- final conclusion
- residual uncertainty
- smallest next action

## Saved Report

- Save status: saved/failed
- Saved path: <codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md

## References
<span id="ref-s1">[S1]</span> Title. Published: YYYY-MM-DD. Accessed: YYYY-MM-DD. URL

## Degrade Log (Only if degrade_used=YES)

| stage | required_min | achieved_before_degrade | additional_queries_run | fallback_stage | borrowed_count | reason |
|---|---:|---:|---:|---|---:|---|
| bleeding-edge | 12 | 10 | 18 | frontier | 2 | low source volume in window |
```

Rules:
1. Keep `[[S#]](#ref-s#)` mapping valid.
2. Keep sections single-instance (no duplicate headings).
3. Omit irrelevant modules instead of forcing low-value content.
4. Match output language to user language.
5. If topic is paper-centric, do not skip `Key Works Deep Dive`.
6. If degradation is used, include explicit degradation metadata and `Degrade Log`.
