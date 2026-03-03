# Source Quality Reference

Guidelines for evaluating and prioritizing research sources.

---

## Source Hierarchy

Sources ranked by reliability and value:

### Tier 1: Primary Sources (Highest Trust)

| Source Type | Examples | Strengths | Watch For |
|-------------|----------|-----------|-----------|
| Official Documentation | API docs, guides | Authoritative, current | May omit limitations |
| Engineering Blogs | Netflix Tech, Stripe Eng | Real-world validation | May be dated |
| Academic Papers | ACM, IEEE | Rigorous methodology | May lack practical context |
| Conference Talks | QCon, Strange Loop | Expert insights | May be promotional |

### Tier 2: Secondary Sources (Good Trust)

| Source Type | Examples | Strengths | Watch For |
|-------------|----------|-----------|-----------|
| GitHub Repos | Sample implementations | Executable proof | Maintenance status |
| Case Studies | Published post-mortems | Real failure modes | Selective reporting |
| Technical Books | O'Reilly, Manning | Comprehensive depth | Currency of info |
| Comparison Articles | ThoughtWorks Radar | Broad perspective | Author bias |

### Tier 3: Community Sources (Verify)

| Source Type | Examples | Strengths | Watch For |
|-------------|----------|-----------|-----------|
| Stack Overflow | Top answers | Practical solutions | Outdated approaches |
| Reddit/HN | r/programming, HN threads | Diverse opinions | Strong opinions |
| Dev.to / Medium | Technical posts | Accessible explanations | Variable quality |
| Tutorials | Blog tutorials | Step-by-step | May not scale |

### Tier 4: Commercial Sources (Skeptical)

| Source Type | Examples | Strengths | Watch For |
|-------------|----------|-----------|-----------|
| Vendor Blogs | Company announcements | Latest features | Marketing spin |
| Analyst Reports | Gartner, Forrester | Market context | Pay-to-play concerns |
| Marketing Pages | Product websites | Feature overviews | Cherry-picked metrics |
| Sponsored Content | Paid blog posts | Easy access | Hidden bias |

---

## Source Evaluation Criteria

Rate sources 1-5 on each criterion:

### Authority
- Who wrote this?
- What's their expertise?
- What's their track record?
- Is the organization credible?

### Currency
- When was this published?
- Is it still maintained?
- Have things changed since?
- Are there more recent sources?

### Evidence
- Are claims supported?
- Is there data or benchmarks?
- Can findings be reproduced?
- Are limitations acknowledged?

### Objectivity
- What's the author's incentive?
- Is it promotional?
- Are alternatives fairly presented?
- Are downsides discussed?

### Relevance
- Does this match our context?
- Is the scale comparable?
- Are constraints similar?
- Is the use case aligned?

---

## Red Flags

### Content Red Flags
- No dates or unclear publication time
- Claims without evidence
- No mention of limitations
- "X is the best" without context
- Outdated dependencies/versions
- Broken links, unmaintained resources

### Source Red Flags
- Anonymous or pseudonymous authors
- Heavy commercial promotion
- SEO-optimized listicles
- Copied content across sites
- Comment sections disabled
- No clear author credentials

### Context Red Flags
- Scale mismatch (startup advice for enterprise)
- Region-specific (may not apply globally)
- Technology-specific (may not transfer)
- Time-specific (may be outdated)

---

## Verification Strategies

### Cross-Reference
```markdown
## Claim: "[Technology X] handles 1M concurrent connections"

Sources supporting:
- Official benchmarks (link) - Tier 1
- Engineering blog post (link) - Tier 1
- Independent benchmark (link) - Tier 2

Sources contradicting:
- GitHub issue about connection limits (link)
- Reddit discussion about scaling problems (link)

Assessment: Claim is valid under specific conditions (see official docs for requirements)
```

### Triangulation
For important claims, find 3+ independent sources:
1. Official documentation
2. Real-world case study
3. Community validation

If sources conflict, document the disagreement.

### Recency Check
```markdown
## Source Evaluation: "[Blog Post Title]"

Published: March 2023
Technology Version: v2.1
Current Version: v4.0

Major Changes Since:
- Breaking API changes in v3.0
- New feature X in v3.5
- Performance improvements in v4.0

Assessment: Core concepts valid, code examples outdated
```

### Scale Validation
```markdown
## Source Context Check

Source Scale:
- "We use X for our 10k user app"

Our Scale:
- Planning for 500k users

Gap Analysis:
- Source may not address scaling concerns
- Need additional sources for high-scale validation
```

---

## Source Documentation

Document sources for traceability:

```markdown
## Source Log

### [Source Title]
- **URL**: [link]
- **Author**: [name, credentials]
- **Published**: [date]
- **Accessed**: [date]
- **Tier**: [1-4]
- **Relevance**: [1-5]
- **Key Points**:
  - [Point 1]
  - [Point 2]
- **Limitations**:
  - [Limitation 1]
- **Related Sources**: [links]
```

---

## Finding Quality Sources

### Search Strategies

**For official information:**
```
site:docs.example.com [topic]
"[product] API reference"
```

**For real-world usage:**
```
"[product] at scale" engineering blog
"[product] case study" production
"migrating from [A] to [B]"
"[product] post-mortem"
```

**For pain points:**
```
site:github.com/[org]/[repo] label:bug "[feature]"
"[product] problems" OR "issues with [product]"
"why we stopped using [product]"
```

**For comparisons:**
```
"[A] vs [B]" -site:versus.com -site:g2.com
"[A] or [B]" site:news.ycombinator.com
"switched from [A] to [B]"
```

### Where to Look

| Need | Go To |
|------|-------|
| Feature details | Official docs, API reference |
| Real usage | Engineering blogs, case studies |
| Problems | GitHub issues, Reddit, HN |
| Benchmarks | Independent tests, academic papers |
| Community health | GitHub pulse, Discord/Slack activity |
| Pricing reality | Pricing pages, Reddit discussions |
| Migration stories | Blog posts, conference talks |
