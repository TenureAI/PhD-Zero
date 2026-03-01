# Memory Templates (v1)

Use markdown with YAML frontmatter.

## Episode Template

```markdown
---
id: ep_<timestamp>_<slug>
type: episode
status: active
title: "<short title>"
project: "<project>"
task_type: "<reproduce|debug|eval|train|plan|research>"
tags: ["tag1", "tag2"]
error_signature: "<optional>"
source_run_id: "<run_id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
confidence: 0.60
---

## Problem

## Attempts

## Outcome

## Evidence

## Todo Impact
- moved_to_done:
- moved_to_blocked:
```
```

## Procedure Template

```markdown
---
id: proc_<timestamp>_<slug>
type: procedure
status: draft
title: "<short title>"
source_run_id: "<run_id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
confidence: 0.70
---

## Scope

## Preconditions

## Workflow

## Stop/Escalate Conditions

## Supporting Episodes
```

## Insight Template

```markdown
---
id: ins_<timestamp>_<slug>
type: insight
status: draft
title: "<short title>"
source_run_id: "<run_id>"
created_at: "2026-01-01T00:00:00Z"
updated_at: "2026-01-01T00:00:00Z"
confidence: 0.55
---

## Insight Statement

## Supporting Evidence

## Applicability Boundary

## Counterexamples
```
