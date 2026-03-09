# Research Plan Template

Use this template when producing a detailed research plan.

## 1. Problem Definition

- Research topic:
- Target problem:
- Why it matters:
- Main success criterion:

## 2. Research Focus

- Primary question:
- Secondary question 1:
- Secondary question 2:
- Boundary / exclusion:

## 3. Innovation Points

- Innovation 1:
  - Why it is new:
  - Which baseline it improves upon:
- Innovation 2:
  - Why it is new:
  - Which baseline it improves upon:

## 4. Experiment Plan

For each experiment, fill:

| Experiment | Purpose | Hypothesis | Variables | Data / Scope | Metrics | Expected Outcome |
|---|---|---|---|---|---|---|
| Baseline |  |  |  |  |  |  |
| Main method |  |  |  |  |  |  |
| Ablation A |  |  |  |  |  |  |
| Ablation B |  |  |  |  |  |  |
| Robustness |  |  |  |  |  |  |
| Error analysis |  |  |  |  |  |  |

## 5. How To Do It

### Code Base

- Language / framework:
- Existing repo to reuse:
- Codebase strategy label (`extend current repo` / `reuse official repo` / `port ideas into target repo` / `build minimal new repo`):
- Comparison repos considered:
- Strongest runnable baseline repo:
- Experiment or execution entry points:
- Evaluation entry points:
- Config system:
- Reproducibility notes:

### Related Files

- Experiment scripts:
- Evaluation scripts:
- Data manifests / workload definitions:
- Config files:
- Execution / evaluation scripts:
- Request templates if applicable:
- Annotation guides:
- Result tables / notebooks:

### Data / Workloads / Inputs

- Primary data source / workload / benchmark:
- Dataset/workload strategy label (`aligned with prior work` / `aligned plus target-domain extension` / `new benchmark strategy`):
- Which related works use the chosen data:
- Validation / comparison scope:
- Robustness input:
- License / access:
- Preprocessing / normalization:
- Comparability risks:

### Additional Experiment Variants

Use this only when the research plan needs extra coverage beyond the core baseline/main/ablation setup.

| Variant | What changes | Why it matters | Metric impact to watch |
|---|---|---|---|
| Domain shift |  |  |  |
| Low-resource setting |  |  |  |
| Noisy input |  |  |  |
| Scale sensitivity |  |  |  |
| Latency or cost constraint |  |  |  |

## 6. Expected Results

- Best-case outcome:
- Expected practical outcome:
- Negative / null result interpretation:
- Decision rule for success:

## 7. Risks And Fallbacks

- Data risk:
- Modeling risk:
- Evaluation risk:
- Execution risk:
- Fallback path:

## 8. Deliverables

- Written research plan
- Experiment tracking sheet
- Reproducible code path
- Result summary table
- Final analysis memo
