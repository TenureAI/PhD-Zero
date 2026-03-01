# Evidence Schema

Use claim-level evidence records during deep research. Keep structure flexible by `research_type`.

## Source Record

```json
{
  "source_id": "S1",
  "title": "Source title",
  "url": "https://...",
  "canonical_url": "https://...",
  "source_type": "official_doc|paper|standard|dataset|issue|analysis",
  "source_tier": "tier1|tier2|tier3",
  "research_type": "idea-exploration|debug-investigation|design-decision|implementation-strategy|conflict-resolution",
  "published_date": "YYYY-MM-DD or unknown",
  "accessed_date": "YYYY-MM-DD",
  "credibility_notes": "reliability and limits",
  "benchmark_name": "optional",
  "benchmark_priority_label": "核心基准|补充基准|探索基准|n/a"
}
```

## Claim Record

```json
{
  "claim_id": "C1",
  "claim_text": "normalized claim",
  "source_ids": ["S1", "S3"],
  "verification_status": "corroborated|single-source|conflicted|uncertain",
  "confidence": "high|medium|low",
  "reasoning_note": "how evidence supports claim",
  "failure_boundary": "where claim may stop holding",
  "counterfactual_note": "optional",
  "last_checked_at": "ISO-8601"
}
```

## Debug-Investigation Extension (Optional)

```json
{
  "error_signature": "runtime error summary",
  "reproduction_context": "env/input/trigger",
  "fix_candidate": "candidate action",
  "validation_result": "passed|failed|partial"
}
```

## Pivot Record

```json
{
  "pivot_id": "P1",
  "trigger": "weak evidence|stale results|conflict|low relevance",
  "from": "old strategy",
  "to": "new strategy",
  "result": "new evidence obtained",
  "timestamp": "ISO-8601"
}
```

## Minimum Standard

1. At least one claim record per major conclusion.
2. Mark unresolved conflicts explicitly.
3. Keep citation mapping complete and valid.
4. Prefer tier1/tier2 support for core conclusions.
