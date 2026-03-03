# Research Types Reference

Detailed guidance for each deep-research type.

---

## Technology Evaluation

**Purpose**: Compare frameworks, libraries, or services for a specific use case.

**Duration**: 2-3 days

**When to Use**:
- Selecting a new framework or library
- Migrating from one technology to another
- Evaluating build-vs-buy decisions

### Evaluation Framework

```markdown
## Technology Evaluation: [Topic]

### Requirements Mapping
| Requirement | Weight | [Option A] | [Option B] | [Option C] |
|-------------|--------|------------|------------|------------|
| [Req 1]     | 30%    | [Score]    | [Score]    | [Score]    |
| [Req 2]     | 25%    | [Score]    | [Score]    | [Score]    |

### Integration Assessment
- Existing stack compatibility
- Migration effort estimate
- Learning curve for team

### Total Cost Analysis
- Licensing/subscription costs
- Implementation effort
- Ongoing maintenance
- Hidden costs (scaling, support tiers)

### Risk Assessment
- Vendor stability
- Community health
- Lock-in concerns
- Long-term viability
```

### Key Questions
1. How does each option meet our specific requirements?
2. What's the integration complexity with our stack?
3. What are total costs over 1, 3, 5 years?
4. What's the migration path if we need to switch?

### Output
- Weighted comparison matrix
- Cost projection
- Integration assessment
- Risk analysis
- Clear recommendation with rationale

---

## Competitive Analysis

**Purpose**: Understand how others solve similar problems.

**Duration**: 1-2 days

**When to Use**:
- Designing new features
- Understanding market patterns
- Finding inspiration from solutions at scale

### Analysis Framework

```markdown
## Competitive Analysis: [Problem Domain]

### Competitors Analyzed
1. [Company A] - [why relevant]
2. [Company B] - [why relevant]
3. [Company C] - [why relevant]

### Feature Comparison
| Feature | Our Current | [Comp A] | [Comp B] | [Comp C] |
|---------|-------------|----------|----------|----------|
| [F1]    | [status]    | [impl]   | [impl]   | [impl]   |

### Patterns Identified
- Common approach: [description]
- Differentiators: [what varies]
- Emerging trends: [what's new]

### Insights
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]

### Recommendations
- [What we should adopt]
- [What we should avoid]
- [What we should differentiate on]
```

### Key Questions
1. Who's doing this well at scale?
2. What patterns are common across solutions?
3. Where do competitors differ?
4. What can we learn from their choices?

### Output
- Competitor overview
- Feature comparison matrix
- Pattern synthesis
- Actionable insights

---

## Architecture Exploration

**Purpose**: Design patterns for complex requirements.

**Duration**: 2-4 days

**When to Use**:
- Designing new systems
- Planning major refactors
- Solving complex technical challenges

### Exploration Framework

```markdown
## Architecture Exploration: [Challenge]

### Problem Definition
- Current state
- Desired state
- Constraints
- Quality attributes (scalability, reliability, etc.)

### Options Identified

#### Option A: [Name]
**Description**: [Brief overview]
**Pros**: [List]
**Cons**: [List]
**When appropriate**: [Conditions]

#### Option B: [Name]
**Description**: [Brief overview]
**Pros**: [List]
**Cons**: [List]
**When appropriate**: [Conditions]

### Trade-off Analysis
| Attribute | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Scalability | [Rating] | [Rating] | [Rating] |
| Complexity | [Rating] | [Rating] | [Rating] |
| Cost | [Rating] | [Rating] | [Rating] |

### Case Studies
- [Company X used Option A because...]
- [Company Y migrated from B to C because...]

### Recommendation
[Selected approach with detailed rationale]
```

### Key Questions
1. What are the quality attributes that matter most?
2. What patterns have proven successful for similar challenges?
3. What are the trade-offs between options?
4. How will this evolve over time?

### Output
- Options analysis
- Trade-off matrix
- Case study references
- Architecture decision record (ADR)

---

## Best Practices Research

**Purpose**: Consolidate industry standards for a domain.

**Duration**: 1-2 days

**When to Use**:
- Establishing team standards
- Improving existing practices
- Onboarding documentation

### Research Framework

```markdown
## Best Practices: [Domain]

### Sources Consulted
- [Official guides]
- [Industry leaders]
- [Community consensus]

### Core Principles
1. [Principle 1]: [explanation]
2. [Principle 2]: [explanation]

### Recommended Practices

#### [Category 1]
- **Do**: [practice]
- **Avoid**: [anti-pattern]
- **Rationale**: [why]

#### [Category 2]
- **Do**: [practice]
- **Avoid**: [anti-pattern]
- **Rationale**: [why]

### Implementation Guide
[Step-by-step adoption path]

### Exceptions
[When practices may not apply]
```

### Key Questions
1. What do authoritative sources recommend?
2. What's the community consensus?
3. What are common anti-patterns?
4. How do we adapt to our context?

### Output
- Consolidated best practices
- Anti-patterns to avoid
- Implementation guidelines
- Context-specific adaptations

---

## Vendor Evaluation

**Purpose**: SaaS/tool selection with procurement focus.

**Duration**: 2-3 days

**When to Use**:
- Selecting third-party services
- Procurement decisions
- Compliance-sensitive selections

### Evaluation Framework

```markdown
## Vendor Evaluation: [Category]

### Evaluation Criteria
| Criterion | Weight | Min. Threshold |
|-----------|--------|----------------|
| Features  | 25%    | [minimum]      |
| Price     | 20%    | [budget]       |
| Security  | 20%    | [requirements] |
| Support   | 15%    | [SLA needs]    |
| Integration | 20%  | [requirements] |

### Vendors Evaluated
1. [Vendor A] - [tier/focus]
2. [Vendor B] - [tier/focus]
3. [Vendor C] - [tier/focus]

### Detailed Scoring
| Criterion | [Vendor A] | [Vendor B] | [Vendor C] |
|-----------|------------|------------|------------|
| Features  | [score]    | [score]    | [score]    |
| Price     | [score]    | [score]    | [score]    |
| **Total** | [weighted] | [weighted] | [weighted] |

### Pricing Analysis
| Tier/Scale | [A] | [B] | [C] |
|------------|-----|-----|-----|
| 10k users  | $   | $   | $   |
| 100k users | $   | $   | $   |
| 1M users   | $   | $   | $   |

### Security & Compliance
- SOC 2 Type II: [status per vendor]
- GDPR compliance: [status per vendor]
- Data residency: [options per vendor]

### Recommendation
[Primary and backup recommendations with rationale]
```

### Key Questions
1. What are our hard requirements?
2. How do vendors compare on weighted criteria?
3. What are total costs at our scale?
4. What's the vendor's trajectory?

### Output
- Vendor scorecard
- Pricing projection
- Security assessment
- Contract recommendations
