---
name: paper-writing
description: |-
  Write CS/AI papers with progressive disclosure. Prefer invoking via research-workflow.
  TRIGGER when: user explicitly asks to draft/write/revise a paper, paper section (abstract, intro, related work, method, experiments, conclusion), rebuttal, or LaTeX content.
  DO NOT TRIGGER when: user mentions papers but needs research/investigation (use deep-research), experiment planning (use research-plan), or experiment execution (use experiment-execution).
---

# Paper Writing

## Mission

Provide a section-aware paper-writing workflow that is:

1. evidence-first
2. progressively disclosed
3. LaTeX- and structure-friendly
4. optimized for CS and AI papers

Do not load all writing guidance at once. Start here, then open only the reference file needed for the current section.

## Activation Gate

Activate this skill only when the user explicitly asks for paper-writing output.

Use this skill for:

1. drafting a paper or a named paper section
2. revising existing paper prose
3. writing rebuttal text
4. turning existing claims, evidence, and results into paper-ready prose

Do not use this skill for:

1. topic scoping
2. literature investigation without a writing deliverable
3. feasibility analysis
4. experiment design
5. experiment execution
6. deciding whether a project is paper-worthy

## Default Workflow

1. identify paper type and draft stage
2. load `references/workflow.md`
3. load only the section file needed right now
4. if related-work style mining is needed, load `references/arxiv-source-workflow.md`
5. use `scripts/fetch_arxiv_source.py` to inspect exemplar paper sources
6. write only what is supported by actual evidence, experiments, and citations

## Loading Map

Open these references on demand:

1. `references/source-index.md`
   - external sources and what each one informs
2. `references/workflow.md`
   - overall writing order, collaboration rules, and section contracts
3. `references/abstract.md`
   - abstract structure and compression rules
4. `references/introduction.md`
   - problem framing, gap, contributions, and section logic
5. `references/related-work.md`
   - literature grouping, synthesis, comparison writing, and citation density
6. `references/arxiv-source-workflow.md`
   - how to download and inspect arXiv LaTeX sources
7. `references/method.md`
   - method narrative, notation, pipeline order, and algorithm exposition
8. `references/architecture-figures.md`
   - architecture drawing heuristics and code-based tooling
9. `references/experiments.md`
   - evaluation logic, ablations, robustness, and error analysis
10. `references/tables-and-layout.md`
   - result tables, layout, appendix splitting, and figure-table coordination

## Writing Rules

1. Write from claims backward:
   - claim
   - evidence
   - section role
   - prose
2. Prefer synthesis over surface summary.
3. One paragraph should usually do one job.
4. Keep novelty claims proportional to the real delta.
5. For figures and tables, prefer code-generated assets that can be regenerated.
6. For related work, inspect representative arXiv source when organization matters.

## Scripts

1. `scripts/fetch_arxiv_source.py`
   - download and unpack an arXiv source bundle
   - list candidate main `.tex` files and section fragments
   - useful for `Related Work`, `Method`, and layout mining
