# Codebase And Data Research Rules

Use this reference when the plan depends on an implementation foundation, benchmark choice, or reproduction strategy.

## 1. Goal

Turn "code base and dataset requirements" into explicit planning decisions:

1. which repo to build on
2. which related repos to compare against
3. which datasets or workloads to align with
4. what reproducibility risks are accepted

## 2. Codebase Selection Order

Choose the implementation foundation in this order unless the user overrides it:

1. the current target repo when it already matches the project objective
2. official code linked by the key paper or project page
3. author-maintained GitHub repositories
4. strong third-party reproductions only when official code is missing or unusable

State which repo is the primary foundation and why it wins on relevance, maintainability, and reproducibility.

## 3. Codebase Audit Checklist

For each primary or comparison repo, check:

1. owner type: official org, author, or third party
2. repository scope: full training, inference only, eval only, or partial
3. entry points for training, evaluation, and inference
4. config system and experiment launch pattern
5. dataset manifests and preprocessing scripts
6. metric implementation and benchmark coverage
7. environment reproducibility: lock files, Docker, conda, or install docs
8. checkpoint availability
9. license constraints
10. maintenance signals such as last meaningful commit

Do not name a repo in the plan without explaining whether it is actually runnable for the target objective.

## 4. GitHub Search Rule

For every highly relevant prior work, check whether there is an open-source repository.

Record at least:

1. repo URL
2. owner
3. official or unofficial status
4. what part of the paper it covers
5. whether it is suitable as a baseline, implementation reference, or both

If no public repo exists for an important work, say so explicitly.

## 5. Dataset And Workload Alignment Rule

Default planning rule:

1. align first with the datasets or workloads used by the strongest relevant prior work
2. if the target deployment domain differs, keep one literature-aligned benchmark and add one target-domain benchmark
3. if prior work is fragmented, define a benchmark set that covers the main comparison axis and explain the tradeoff

Do not choose datasets only because they are convenient.

## 6. Dataset Audit Checklist

For each chosen dataset, workload, trace, or benchmark, specify:

1. which related works use it
2. task definition and label space
3. split policy
4. scale and domain coverage
5. freshness or temporal boundary when relevant
6. license and access restrictions
7. preprocessing and normalization conventions
8. contamination, leakage, or quality risks

## 7. Planning Decision Labels

Every plan must label dataset/workload strategy as one of:

1. `aligned with prior work`
2. `aligned plus target-domain extension`
3. `new benchmark strategy`

Every plan must label codebase strategy as one of:

1. `extend current repo`
2. `reuse official repo`
3. `port ideas into target repo`
4. `build minimal new repo`

## 8. Required Plan Content

When this reference applies, the plan must make these items explicit:

1. primary implementation repo
2. comparison repos considered and why they were rejected or kept
3. strongest runnable baseline
4. dataset/workload alignment choice
5. benchmark comparability risks
6. reproducibility blockers and fallback path
