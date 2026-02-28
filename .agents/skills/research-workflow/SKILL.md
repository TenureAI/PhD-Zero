---
name: research-workflow
description: Run an evidence-driven AI R&D execution loop from task intake to reflection and consolidation. Use when handling research tasks such as repo, paper, issue, and documentation analysis, baseline reproduction, training/evaluation debugging, experiment planning, and iterative delivery. Trigger when requests mention research workflow, research_workflow, baseline reproduction, model debugging, literature scan, or next-step experiment decisions.
---

# Research Workflow

## Mission
Drive AI R&D tasks with small, testable, evidence-first steps.

## Default Loop
Execute this loop every cycle:
1. Intake task.
2. Understand current state.
3. Search broadly for relevant evidence (repo files, papers, issues, docs, logs, prior runs).
4. Plan minimal next step.
5. Recall relevant memory before expensive or irreversible actions.
6. Act.
7. Observe outputs and artifacts.
8. Reason from evidence.
9. Evaluate against success criteria.
10. Decide: continue, done, checkpoint, or reflect.

## Stage Rules
1. Define explicit success criteria before non-trivial actions.
2. Prefer the lowest-cost step that can falsify the current hypothesis.
3. Record commands, file changes, metrics, and errors as evidence.
4. Start with broad evidence collection before committing to a path.
5. Re-check memory before long training, broad experiment sweeps, or protocol changes.
6. Trigger `human-checkpoint` when uncertainty, cost, impact, or risk is high.
7. End each major phase with a state summary and next decision.

## Search and Evidence Collection
Collect context widely before major decisions:
1. Inspect local codebase, configs, scripts, logs, and experiment artifacts.
2. Read related papers, official docs, issues, benchmark protocols, and shared memory repositories when available.
3. Compare multiple sources when claims conflict.
4. Prefer primary sources over secondary summaries.
5. Summarize collected evidence into concrete hypotheses and next actions.

## Decision Policy
Use this decision order:
1. `done`: success criteria satisfied with evidence.
2. `checkpoint`: high-cost, high-impact, or high-risk action requires human confirmation.
3. `iterate`: another low-cost step is available.
4. `blocked`: no reliable next step; request targeted human input.

## Evidence Standard
Treat claims as valid only when backed by one of:
1. Reproducible command output.
2. Measurable metric change.
3. File diff linked to behavior change.
4. Cross-check against prior memory with matching context.

## Required Cycle Output
Emit this structure at the end of each cycle:
1. `State`: what is currently true.
2. `Evidence`: what was observed.
3. `Next Step`: smallest validated action.
4. `Memory Need`: none, retrieve, or writeback.
5. `Checkpoint Need`: yes or no, with reason.
6. `Shared Candidate`: yes or no, with why.
