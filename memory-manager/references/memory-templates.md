# Memory Templates (v0)

Use markdown with YAML frontmatter for each long-term memory record.

## Episode Template

```markdown
---
id: ep_<timestamp>_<slug>
type: episode
status: active
title: "<short title>"
project: "<project>"
task_type: "<reproduce|debug|eval|train|plan>"
tags: ["tag1", "tag2"]
error_signature: "<optional>"
source_run_id: "run_<id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
human_verified: false
confidence: 0.60
---

## Problem
Describe the task and context.

## Attempts
List attempted actions in order.

## Outcome
Describe result and measured metrics.

## Effective Method
Describe what worked and why.

## Lesson Learned
State transfer-friendly takeaways.

## Evidence
Link files, logs, commands, and metric snapshots.
```

## Procedure Template

```markdown
---
id: proc_<timestamp>_<slug>
type: procedure
status: draft
title: "<short title>"
project: "<optional>"
task_type: "<task category>"
tags: ["tag1", "tag2"]
source_run_id: "run_<id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
human_verified: false
confidence: 0.70
---

## Scope
Define where this procedure applies.

## Preconditions
List required environment and assumptions.

## Workflow
Provide ordered steps.

## Branches and Checks
Describe decision branches and checkpoints.

## Stop and Escalate Conditions
Describe when to stop and call human checkpoint.

## Evidence Links
List supporting episode IDs.
```

## Insight Template

```markdown
---
id: ins_<timestamp>_<slug>
type: insight
status: draft
title: "<short title>"
project: "<optional or cross-project>"
task_type: "<optional>"
tags: ["tag1", "tag2"]
source_run_id: "run_<id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
human_verified: false
confidence: 0.55
---

## Insight Statement
State the abstract pattern clearly.

## Supporting Evidence
Reference episode/procedure IDs and observed metrics.

## Applicability Boundary
Define where the insight should be used.

## Counterexamples
List known failure cases or contradictions.

## Next Validation
Describe how to test and increase confidence.
```
