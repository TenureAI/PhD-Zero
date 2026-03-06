---
name: research-plan
description: Build detailed, execution-ready research plans for CS projects, papers, and experiment proposals. Use when the user wants a research proposal, experiment roadmap, study design, ablation plan, or pre-implementation planning with explicit experiments, core research questions, innovation points, codebase requirements, files, data or workload requirements, risks, and expected outcomes.
---

# Research Plan

## Mission

Turn an early-stage research idea into a concrete, execution-ready plan with clear experiments, implementation prerequisites, and expected results.

## Interaction Policy

Once the user has chosen a direction, stop asking frequent clarification questions unless a missing detail would materially change the plan.

Default behavior after direction is fixed:

1. Infer reasonable assumptions.
2. Write the full detailed plan in one pass.
3. Ask follow-up questions only for hard blockers or high-risk ambiguity.

Do not turn normal planning into a back-and-forth questionnaire.

## Delivery Policy

Separate the full planning artifact from the chat summary.

1. The full plan should still be detailed and complete.
2. In the CLI chat, do not dump the entire long report unless the user explicitly asks for it.
3. In the CLI chat, provide a concise summary focused on:
   - key innovation points
   - experiment plan
   - code base and file requirements
   - data or workload requirements
   - expected results
   - major risks
4. Keep progress updates short while drafting.

## When To Use

Use this skill when the user asks for any of the following:

1. A research plan or proposal.
2. A project plan before implementation.
3. A paper idea breakdown into experiments.
4. An ablation or evaluation roadmap.
5. A study design for a general CS research project.

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
   - `Related Files`: configs, manifests, experiment scripts, evaluation scripts, request templates when needed, documentation, metadata, report templates, and logs.
   - `Data / Workloads / Inputs`: required datasets, workloads, traces, corpora, benchmarks, or input sources; plus split policy, access constraints, and preprocessing if needed.
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
   - `algorithmic`
   - `systems`
   - `data or benchmarking`
   - `human-computer interaction`
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
6. `Data / Workloads / Evaluation Scope`
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
   - Check scale, configuration, workload, or data sensitivity.
5. `Robustness`
   - Check domain shift, input perturbation, user variation, or annotation mismatch.
6. `Error Analysis`
   - Identify where the method fails and why.

## How To Write Research Focus

Research focus should be written as concrete questions, not generic themes.

Good:

1. "Does the proposed indexing strategy reduce query latency under high-concurrency workloads without hurting recall?"
2. "Which component contributes most: cache policy, partitioning scheme, or request scheduling?"

Weak:

1. "Study system performance."
2. "Improve performance."

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
2. Experiment and execution entry points.
3. Config system.
4. Evaluation pipeline.
5. Reproducibility requirements.

Examples:

1. A language and framework already established in the target project.
2. A reproducible config system for experiments and evaluation.
3. An existing project-specific codebase when reproduction fidelity matters more than flexibility.

### Related Files

Mention the concrete file classes the repo should contain:

1. `run_experiment.py` or stage-specific experiment scripts
2. `eval.py` and metric wrappers
3. data manifests, workload definitions, or split files
4. system or experiment configs
5. experiment configs or request templates if applicable
6. execution or evaluation scripts
7. experiment registry or run sheet
8. annotation instructions
9. result summary tables
10. failure case logs

### Data / Workloads / Inputs

Always specify:

1. Primary data source, workload, benchmark, trace, or corpus
2. Validation, comparison, or test scope
3. External or robustness inputs
4. Licensing, access, or collection constraints
5. Preprocessing, filtering, or normalization

If the user has not chosen the evaluation inputs, propose candidates and explain tradeoffs.

### Additional Experiment Variants

If the plan needs broader coverage, specify extra experiment variants such as:

1. domain shift or out-of-domain evaluation
2. noisy or low-resource settings
3. scale or configuration sensitivity
4. user group or input-type variation
5. execution-time cost or latency constraints

## Expected Results Rules

Expected results must be specific enough to judge success.

Include:

1. `Best-case outcome`
2. `Expected practical outcome`
3. `Failure-case interpretation`

Prefer ranges or decision thresholds over vague claims.

Examples:

1. "Expected 3-7% relative improvement on the primary success metric, with neutral or slightly improved performance on the stable reference workload."
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

When returning results to the user in chat, summarize the plan instead of pasting the full long-form document unless the user explicitly requests the full text.

## Required Quality Bar

Before finalizing, check:

1. Are the experiments concrete enough to run?
2. Are the research points framed as questions?
3. Are innovation claims defended against obvious baseline objections?
4. Are codebase, files, and data or workload requirements all specified?
5. Are expected results measurable?
6. Are failure cases still informative?

If any answer is no, refine before responding.

## Reference

When drafting the plan, use [references/research-plan-template.md](references/research-plan-template.md) as the default skeleton and checklist.
