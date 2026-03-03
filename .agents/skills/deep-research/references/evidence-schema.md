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
  "time_stage": "bleeding-edge|frontier|recent|mid-term|classic|unknown",
  "days_from_as_of": "integer or unknown",
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

## Key Work Record (Paper-Centric Optional)

```json
{
  "work_id": "W1",
  "work_title": "Paper title",
  "source_id": "S3",
  "method_family": "SFT|RLHF|DPO|ORPO|GRPO|hybrid|other",
  "supervision_signal": "demonstrations|pairwise preference|scalar reward|verifier|mixed",
  "optimization_type": "offline|on-policy|off-policy|mixed",
  "main_gain": "what improved and in which setting",
  "known_risk": "instability|overfit|reward hacking|forgetting|other",
  "best_use_case": "where this method is most suitable",
  "why_relevant_to_user": "one-line linkage to user question"
}
```

## Degrade Record (Optional)

```json
{
  "stage": "bleeding-edge|frontier|recent|mid-term|classic",
  "required_min": 12,
  "achieved_before_degrade": 10,
  "additional_queries_run": 18,
  "fallback_stage": "frontier|recent|mid-term|none",
  "borrowed_count": 2,
  "reason": "window-level source scarcity after exhaustion pass"
}
```

## Minimum Standard

1. At least one claim record per major conclusion.
2. Mark unresolved conflicts explicitly.
3. Keep citation mapping complete and valid.
4. Prefer tier1/tier2 support for core conclusions.
5. For paper-centric topics, include key work records for each deep-dive work.
6. If degradation is used, include degrade record(s) for each degraded stage.
