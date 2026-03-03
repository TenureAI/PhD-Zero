# Synthesis Patterns Reference

Patterns for forming clear, actionable recommendations from research.

---

## Synthesis Framework

### The Synthesis Flow

```
GATHERED DATA
     │
     ▼
┌─────────────┐
│  PATTERNS   │  What themes emerge?
└─────────────┘
     │
     ▼
┌─────────────┐
│  INSIGHTS   │  What do patterns mean?
└─────────────┘
     │
     ▼
┌─────────────┐
│ TRADE-OFFS  │  What are the costs?
└─────────────┘
     │
     ▼
┌─────────────┐
│ RECOMMENDATION │  What should we do?
└─────────────┘
```

---

## Pattern Recognition

### Finding Patterns

Look for:
- **Convergence**: Multiple sources agree
- **Divergence**: Where sources disagree (and why)
- **Gaps**: What's not being discussed
- **Trends**: Directional movement over time
- **Outliers**: Exceptions that prove or break rules

### Pattern Documentation

```markdown
## Pattern: [Name]

**Observation**: [What you're seeing]
**Frequency**: [How often this appears]
**Sources**: [Which sources show this]
**Significance**: [Why it matters]
**Confidence**: High / Medium / Low
```

### Example

```markdown
## Pattern: Framework Consolidation

**Observation**: Teams are consolidating from multiple UI frameworks to single solutions
**Frequency**: 7 of 10 case studies mention this
**Sources**: Netflix, Airbnb, Stripe engineering blogs
**Significance**: Suggests maintenance burden of multiple frameworks exceeds benefits
**Confidence**: High
```

---

## Forming Insights

### Insight Structure

```markdown
## Insight: [Actionable statement]

**Based on**: [Patterns that support this]
**Implication**: [What this means for us]
**Counter-evidence**: [What might contradict this]
**Confidence**: [Level with reasoning]
```

### Insight Types

| Type | Description | Example |
|------|-------------|---------|
| Confirmatory | Validates existing assumption | "React is indeed the dominant choice" |
| Revelatory | New understanding | "GraphQL has significant cold-start costs" |
| Cautionary | Warns against approach | "Serverless requires rethinking state" |
| Differentiating | Shows distinction | "Pricing models vary 10x at scale" |

### Example

```markdown
## Insight: Early architectural decisions constrain scaling options

**Based on**: 
- Pattern: Teams regret tight coupling after 1M users
- Pattern: Database choice determines scaling strategy
- Case study: Monzo's PostgreSQL journey

**Implication**: We should plan our data architecture for 10x current scale

**Counter-evidence**: 
- YAGNI principle suggests not over-engineering
- Some teams successfully migrated databases

**Confidence**: High - multiple independent sources confirm
```

---

## Trade-off Analysis

### Trade-off Matrix

```markdown
## Trade-off Analysis: [Decision]

| Factor | Option A | Option B | Winner |
|--------|----------|----------|--------|
| Cost (initial) | $5k | $15k | A |
| Cost (at scale) | $50k/mo | $20k/mo | B |
| Time to implement | 2 weeks | 6 weeks | A |
| Maintenance burden | High | Low | B |
| Team expertise | Low | High | B |
| Lock-in risk | High | Low | B |

**Summary**: B wins on long-term factors, A wins on short-term
```

### Trade-off Categories

**Time Trade-offs**:
- Implementation time vs. long-term maintenance
- Time to market vs. technical debt
- Learning curve vs. productivity after learning

**Cost Trade-offs**:
- Initial cost vs. ongoing cost
- Build cost vs. buy cost
- Direct cost vs. opportunity cost

**Quality Trade-offs**:
- Performance vs. simplicity
- Flexibility vs. standardization
- Features vs. reliability

**Risk Trade-offs**:
- Innovation vs. proven solutions
- Control vs. managed services
- Speed vs. safety

---

## Recommendation Patterns

### The SBAR Format

```markdown
## Recommendation: [Title]

**Situation**: [Current state and context]

**Background**: [How we got here, what research showed]

**Assessment**: [Analysis of options]

**Recommendation**: [Clear, actionable proposal]
```

### Recommendation Strength

| Level | Language | Use When |
|-------|----------|----------|
| Strong | "We should..." | High confidence, clear winner |
| Moderate | "Consider..." | Good option but context-dependent |
| Conditional | "If X, then..." | Depends on factors |
| Against | "Avoid..." | Clear evidence against |

### Primary + Contingency Pattern

```markdown
## Recommendation

**Primary**: [Main recommendation]
- When: [Default conditions]
- Why: [Key reasons]

**Contingency**: [Backup recommendation]
- When: [Conditions that trigger this]
- Why: [Reasons for fallback]

**Avoid**: [What not to do]
- Why: [Reasons against]
```

### Example

```markdown
## Recommendation: Database Selection

**Primary**: PostgreSQL on Supabase
- When: Standard requirements, team has SQL experience
- Why: Cost-effective, familiar tooling, good scaling story

**Contingency**: PlanetScale (MySQL)
- When: Need global distribution, MySQL preference
- Why: Better geo-distribution, managed sharding

**Avoid**: Self-managed databases
- Why: Operational burden exceeds benefits at our scale
```

---

## Presenting Trade-offs

### The Honest Assessment

Always include:
1. **What we're gaining**: Clear benefits
2. **What we're giving up**: Real costs
3. **What could go wrong**: Risks
4. **What we don't know**: Uncertainties

### Risk Acknowledgment

```markdown
## Risk Assessment

### Known Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Plan] |
| [Risk 2] | Low | Medium | [Plan] |

### Unknown Risks
- We don't have data on [X] at our scale
- [Technology] hasn't been tested for [use case]

### Assumptions
- We assume [X] will continue to be supported
- We assume our scale will grow to [Y]
```

---

## Synthesis Checklist

### Before Synthesizing
- [ ] All gathered data organized
- [ ] Sources evaluated for quality
- [ ] Comparison matrices complete
- [ ] Gaps in information noted

### During Synthesis
- [ ] Patterns identified and documented
- [ ] Insights derived from patterns
- [ ] Trade-offs explicitly stated
- [ ] Counter-evidence considered

### Recommendation Quality
- [ ] Clear, actionable proposal
- [ ] Rationale documented
- [ ] Alternatives acknowledged
- [ ] Risks and trade-offs stated
- [ ] Confidence level appropriate
- [ ] Follow-up actions defined

---

## Anti-Patterns

### Synthesis Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| Cherry-picking | Only citing supporting evidence | Include counter-evidence |
| False certainty | Overstating confidence | Acknowledge unknowns |
| Analysis paralysis | Endless "need more data" | Decide with available info |
| Anchoring | Over-weighting first finding | Consider all evidence equally |
| Availability bias | Over-weighting recent/memorable info | Systematic review |

### Recommendation Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| "It depends" | No actual recommendation | Make a call, state conditions |
| Hidden assumptions | Unstated prerequisites | Document all assumptions |
| Vague action | "Consider X" | Specific next steps |
| Ignoring constraints | Idealistic recommendation | Address real limitations |
| Sunk cost | Recommending based on prior investment | Evaluate fresh |
