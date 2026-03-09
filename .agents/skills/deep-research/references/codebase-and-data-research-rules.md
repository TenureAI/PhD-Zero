# Codebase And Data Research Rules

Use this reference when the research topic has an implementation, benchmark, reproduction, or planning component.

## 1. Goal

Convert vague "look at the repo/data" work into a traceable evidence pass:

1. identify the most relevant code bases
2. identify the most relevant datasets or workloads
3. determine whether the target plan should align with prior work or intentionally deviate
4. record evidence and uncertainty explicitly

## 2. Codebase Search Order

Search in this order unless the user gives a stricter constraint:

1. local target repo or currently checked out project
2. official implementation linked by the paper, project page, or organization
3. author-maintained GitHub repositories
4. widely used third-party reproductions only if official code is missing or incomplete

Do not treat random GitHub repos as equivalent evidence to official implementations.

## 3. Codebase Search Rules

For each high-relevance method or paper, check whether an open-source code base exists.

Minimum checks:

1. repository URL
2. owner type: official org, author, or third party
3. activity signals: last commit date, issues, stars only as a weak signal
4. reproducibility signals: environment file, training script, eval script, config examples, checkpoints, README completeness
5. scope match: full training, inference only, eval only, or partial reproduction
6. license and usage constraints

If the work is highly relevant and no code is open-sourced, record that absence explicitly instead of silently skipping it.

## 4. What To Extract From A Relevant Repo

When a code base is relevant, extract only the implementation facts needed for reasoning:

1. entry points for training, evaluation, and inference
2. config system and major knobs
3. data manifest or preprocessing path
4. benchmark or metric implementation
5. dependency and runtime assumptions
6. checkpoint availability
7. any mismatch between the paper claim and the released code

Prefer concrete file paths, script names, and config names over generic summaries.

## 5. Dataset And Workload Search Rules

For each candidate dataset, workload, trace, or benchmark, record:

1. what prior work used it
2. whether it is the main comparison target in the literature
3. task definition and label space
4. train/validation/test split policy
5. scale, domain, and freshness
6. license, access, and usage restrictions
7. known contamination, leakage, or annotation-quality concerns
8. preprocessing conventions used by the most relevant prior work

Do not choose datasets only because they are easy to download.

## 6. Dataset Alignment Decision Rule

Default rule:

1. if the task claims improvement over prior work, align first with the datasets or workloads used by the strongest relevant baselines
2. if the literature has no stable comparison set, propose a primary benchmark set and explain why
3. if the target project serves a different domain or product requirement, keep one literature-aligned benchmark and add one target-domain benchmark

You must state which of the following applies:

1. `fully aligned with prior work`
2. `partially aligned with one added domain-specific benchmark`
3. `intentionally different from prior work`

If intentionally different, explain what comparability is lost and what practical validity is gained.

## 7. Comparison Set Construction

When planning evaluations, define the comparison set in this order:

1. strongest official or canonical baseline from the literature
2. strongest practical open-source baseline that can actually be run
3. target-project incumbent or current production baseline when applicable
4. ablations of the proposed method

If the canonical baseline cannot be reproduced, say why and choose the closest defensible substitute.

## 8. Evidence Quality Rules

Treat evidence tiers in this order:

1. paper plus official repo plus released configs or checkpoints
2. paper plus author repo
3. paper only
4. third-party reproduction
5. blog posts, tweets, or issue comments as weak supporting evidence only

Do not present tier 4 or 5 evidence as if it were definitive.

## 9. Required Output When This Reference Applies

Include a compact `Codebase and Data Audit` block in the research output:

1. target repo inspected or not
2. related official repos found or not
3. strongest runnable baseline repo
4. dataset/workload alignment choice
5. main reproducibility risks
6. unresolved gaps

## 10. Failure And Gap Handling

If repository or dataset evidence is incomplete:

1. say what was searched
2. say what was not found
3. state whether the gap changes the recommendation materially
4. provide the least risky fallback
