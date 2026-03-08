# Experiments

## Job

Experiments should answer whether the paper's claims hold.

## Default Order

1. setup and implementation details
2. main results
3. ablations
4. sensitivity or robustness
5. qualitative or error analysis

## Core Principle

Every experiment must map to a claim.

Before writing a subsection, identify:

1. claim being tested
2. baseline needed
3. metric that decides success or failure

## Main Results Section

1. start with the primary benchmark or setting
2. compare against the strongest relevant baselines
3. explain the pattern before diving into every number

## Ablations

1. remove or vary one component at a time
2. explain what the ablation isolates
3. do not present ablations as a random checklist

## Robustness / Sensitivity

Use when the paper claims:

1. generalization
2. stability
3. low-resource effectiveness
4. scale behavior

## Error Analysis

Use error analysis when:

1. the method claims interpretability
2. failure modes are central to the paper
3. aggregate metrics hide behavior differences

## Writing Rules

1. explain the evaluation logic, not just the metric names
2. separate implementation detail from result interpretation
3. highlight negative or null results when informative
4. say when a baseline is omitted and why
