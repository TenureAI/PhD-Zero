# Architecture Figures

## Job

Architecture figures should clarify the method faster than prose can.

## Design Rules

1. show information flow, not decoration
2. keep the reader's path obvious
3. use 3-6 major blocks, not every implementation detail
4. align names with the method section exactly
5. annotate the paper's novel block or changed path

## Recommended Figure Workflow

1. sketch the semantic blocks first
2. decide whether the figure is:
   - pipeline
   - dataflow
   - training loop
   - system deployment
3. draft quickly in code
4. only then polish spacing, color, and labels

## Code-Based Tooling Choices

### TikZ

Use when:

1. the paper is LaTeX-native
2. you need publication-grade vector consistency
3. the diagram is stable enough to justify fine control

Strengths:

1. integrates directly into LaTeX
2. precise typography and alignment
3. easy to keep consistent with paper fonts

### Graphviz

Use when:

1. you need fast iteration on graph structure
2. you want automatic layout before manual polishing
3. the figure is mostly nodes and edges

Strengths:

1. fast text-based editing
2. automatic layout
3. good for dependency and pipeline drafts

### Practical Recommendation

Default pattern:

1. draft with Graphviz or a simple text diagram if structure is unclear
2. finalize in TikZ when the figure is stable and will appear in the paper

## Labeling Rules

1. use noun phrases for blocks
2. use verbs on arrows only when action matters
3. avoid paragraphs inside boxes
4. make repeated flows visually repetitive on purpose

## Figure Review Checklist

1. can a reviewer retell the method from the figure
2. is the novelty visually identifiable
3. can the figure survive grayscale or print
4. does the figure introduce names not used in the text
