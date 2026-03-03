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
- query_budget_frontier=
- query_budget_recent=
- query_budget_mid_term=
- query_budget_classic=
- frontier_sources=
- recent_sources=
- mid_term_sources=
- classic_sources=

## Conclusion and Next Step

- final conclusion
- residual uncertainty
- smallest next action

## Saved Report

- Save status: saved/failed
- Saved path: <codex-cwd>/logs/runs/<run_id>/reports/deep-research-<slug>.md

## References
<span id="ref-s1">[S1]</span> Title. Published: YYYY-MM-DD. Accessed: YYYY-MM-DD. URL
```

Rules:
1. Keep `[[S#]](#ref-s#)` mapping valid.
2. Keep sections single-instance (no duplicate headings).
3. Omit irrelevant modules instead of forcing low-value content.
4. Match output language to user language.
