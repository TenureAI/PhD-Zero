---
name: research-plan
description: Build detailed, execution-ready research plans for AI/ML projects, papers, and experiment proposals. Use when the user wants a research proposal, experiment roadmap, study design, ablation plan, or pre-implementation planning with explicit experiments, core research questions, innovation points, codebase requirements, files, datasets, risks, and expected outcomes.
---

# Research Plan

## Mission

Turn an early-stage research idea into a concrete, execution-ready plan with clear experiments, implementation prerequisites, and expected results.

## When To Use

Use this skill when the user asks for any of the following:

1. A research plan or proposal.
2. A project plan before implementation.
3. A paper idea breakdown into experiments.
4. An ablation or evaluation roadmap.
5. A study design for an AI/ML or general CS research project.

## Non-Negotiable Output Sections

Every final plan must include all sections below. Do not omit a section just because the user did not mention it.

1. `Problem Definition`
   - What problem is being solved?
   - Why does it matter?
   - What exact question will the study answer?
2. `Research Focus`
   - State the core research points.
   - Separate primary question, secondary questions, and boundary conditions.
3. `Innovation Points`
   - List specific novelty claims.
   - Compare against likely baselines or common approaches.
   - Distinguish true novelty from engineering cleanup.
4. `Experiment Plan`
   - Enumerate the exact experiments to run.
   - Include baseline, main experiment, ablation, robustness, and error-analysis experiments when relevant.
   - For each experiment: hypothesis, setup, variables, metrics, and success signal.
5. `How To Do It`
   - `Code Base`: what kind of repository or framework is needed.
   - `Related Files`: config, prompts, manifests, training scripts, eval scripts, data cards, annotation guides, checkpoint metadata, report templates, and logs.
   - `Datasets`: required datasets, splits, licenses, collection method, cleaning, and augmentation if needed.
6. `Expected Results`
   - What outcomes are expected qualitatively and quantitatively.
   - What negative or null outcomes are still informative.
7. `Risk And Fallback`
   - Technical risks, data risks, evaluation risks, and fallback routes.
8. `Deliverables`
   - What artifacts should exist at the end.

## Default Planning Workflow

Follow this order unless the user explicitly asks for a lighter output:

1. Restate the research objective in one sentence.
2. Identify task type:
   - `modeling`
   - `data-centric`
   - `systems`
   - `human-in-the-loop`
   - `system-evaluation`
3. Identify the primary unit of progress:
   - accuracy or quality gain
   - efficiency or cost reduction
   - robustness improvement
   - usability or workflow improvement
   - scientific understanding
4. Form 1-3 core hypotheses.
5. Design the minimum baseline set.
6. Design the main experiment set.
7. Design ablations to isolate the claimed contribution.
8. Design stress tests or out-of-domain checks where relevant.
9. Specify the implementation foundation.
10. Specify expected outcomes and decision rules.

## Experiment Design Rules

Do not produce vague items such as "run some experiments" or "evaluate performance."

Each experiment block should specify:

1. `Name`
2. `Purpose`
3. `Hypothesis`
4. `Independent Variables`
5. `Controlled Factors`
6. `Datasets / Data Splits`
7. `Metrics`
8. `Implementation Notes`
9. `Expected Outcome`

Use this experiment stack by default:

1. `Baseline`
   - Reproduce a standard or strong practical baseline.
2. `Main Method`
   - Evaluate the proposed idea end to end.
3. `Ablations`
   - Remove or vary each key component one at a time.
4. `Sensitivity`
   - Check scale, hyperparameter, prompt, or data sensitivity.
5. `Robustness`
   - Check domain shift, input perturbation, user variation, or annotation mismatch.
6. `Error Analysis`
   - Identify where the method fails and why.

## How To Write Research Focus

Research focus should be written as concrete questions, not generic themes.

Good:

1. "Does retrieval-augmented planning improve tool-use success on long-horizon tasks without increasing latency too much?"
2. "Which component contributes most: task decomposition, memory retrieval, or verifier feedback?"

Weak:

1. "Study agent planning."
2. "Improve model performance."

## How To Write Innovation Points

Innovation points must be defensible. Use this test:

1. `Method novelty`: a genuinely new mechanism, training strategy, architecture, or data construction method.
2. `Evaluation novelty`: a benchmark, protocol, or measurement setup that reveals something existing work misses.
3. `System novelty`: a workflow or tooling contribution that materially changes what can be studied.

Do not call something innovative if it is only:

1. More tuning.
2. More data without a justification.
3. Routine engineering migration.

If novelty is weak, say so directly and reframe it as:

1. strong empirical study
2. practical system paper
3. careful benchmark or evaluation study

## How To Write "How To Do It"

Always make this section operational.

### Code Base

Specify:

1. Main language and framework.
2. Training and inference entry points.
3. Config system.
4. Evaluation pipeline.
5. Reproducibility requirements.

Examples:

1. `PyTorch + Hugging Face + Hydra` for training-heavy model work.
2. `PyTorch Lightning` when multi-stage training orchestration matters.
3. An existing project-specific codebase when reproduction fidelity matters more than flexibility.

### Related Files

Mention the concrete file classes the repo should contain:

1. `train.py` or stage-specific training scripts
2. `eval.py` and metric wrappers
3. dataset manifests and split files
4. model configs
5. prompt templates if LLMs are involved
6. inference scripts
7. experiment registry or run sheet
8. annotation instructions
9. result summary tables
10. failure case logs

### Datasets

Always specify:

1. Primary dataset
2. Validation and test split policy
3. External or robustness datasets
4. Licensing or access constraints
5. Data cleaning and filtering

If the user has not chosen datasets, propose candidates and explain tradeoffs.

### Additional Experiment Variants

If the plan needs broader coverage, specify extra experiment variants such as:

1. domain shift or out-of-domain evaluation
2. noisy or low-resource settings
3. scale or hyperparameter sensitivity
4. user group or input-type variation
5. inference-time cost or latency constraints

## Expected Results Rules

Expected results must be specific enough to judge success.

Include:

1. `Best-case outcome`
2. `Expected practical outcome`
3. `Failure-case interpretation`

Prefer ranges or decision thresholds over vague claims.

Examples:

1. "Expected 3-7% relative improvement on the primary success metric, with neutral or slightly improved performance on the stable benchmark split."
2. "A null result would suggest the proposed component adds complexity without improving the key bottleneck it was meant to address."

## Output Format

By default, structure the final plan in this order:

1. Title
2. Objective
3. Research Focus
4. Innovation Points
5. Experiment Plan
6. How To Do It
7. Expected Results
8. Risks And Fallbacks
9. Deliverables

Use tables when they make experiment plans easier to scan.

## Required Quality Bar

Before finalizing, check:

1. Are the experiments concrete enough to run?
2. Are the research points framed as questions?
3. Are innovation claims defended against obvious baseline objections?
4. Are codebase, files, and datasets all specified?
5. Are expected results measurable?
6. Are failure cases still informative?

If any answer is no, refine before responding.

## Reference

When drafting the plan, use [references/research-plan-template.md](references/research-plan-template.md) as the default skeleton and checklist.
