# Market Research Advanced Guide

## Source Methodologies
This guide synthesizes expert frameworks from:
- Sequoia Capital — Company Building (Why Now framework)
- Geoffrey Moore — *Crossing the Chasm* (Beachhead / Bowling Alley strategy)
- Steve Blank — *The Four Steps to the Epiphany* (Customer development)
- Clayton Christensen — *The Innovator's Dilemma* (Disruption patterns)
- CB Insights / Gartner / Forrester — Market sizing methodology

---

## Quick Decision Guide (Agent Decision Criteria)

| Situation | Threshold | Action |
|-----------|-----------|--------|
| TAM < $500M | Small market | Recommend niche positioning or redefine market scope |
| CAGR < 8% | Stagnant growth | Competitive moat required; market share capture strategy |
| 10+ competitors + mature market | Red Ocean | Differentiation must be structural, not incremental |
| No competitors found | Caution | Either no market exists, or no one has monetized it — investigate why |
| No "Why Now" identified | Warning | Cannot explain why this wasn't solved in 10 years — flag to CEO |

## Red Flags (Explicitly warn the CEO about these)
- TAM figures without source URLs → label as "unverified estimate"
- Cannot articulate "Why Now" → recommend Beachhead strategy review
- Beachhead market > 10,000 reachable customers → flag as "entire market, not a beachhead"
- Market sizing without competitive analysis → SOM estimate is unreliable without competition data

---

## 1. The "Why Now" Framework (Sequoia Capital)

Every market analysis must answer: **"Why is this market opening NOW?"**

### Three Categories of "Why Now"

**1. Technology Shift**
- New technology makes previously impossible or prohibitively expensive things feasible
- Diagnostic question: "Could this product have been built 2 years ago? Why not?"
- Examples: iPhone → mobile apps (2007), LLM APIs → AI-native tools (2023+), cloud cost reduction → SaaS era

**2. Regulatory Shift**
- New legislation opens or closes markets
- Diagnostic question: "Has a regulatory change in the last 2 years affected this market?"
- Examples: GDPR enforcement → compliance tools boom, Open Banking API mandates → fintech innovation

**3. Behavioral Shift**
- A large-scale event changes what customers accept or expect
- Diagnostic question: "What are customers accepting now that they previously refused?"
- Examples: COVID-19 → remote work tools explosion, accelerated adoption of digital payments

### Writing "Why Now" — Good vs. Bad

```
Good: "LLM inference costs dropped 90% since 2022, making it economically viable
       for a solo founder to ship AI-powered features at under $X/month operational
       cost. 18 months ago, this was not feasible for an indie product."

Bad: "AI is trending and many people are interested in AI."
```

### When "Why Now" is Missing
If the market has existed for 10+ years without a clear winner and you cannot articulate a "Why Now" trigger:
- This likely indicates a structural problem with the market
- Flag to CEO: "Why has this not been solved in 10 years?" as an explicit risk signal

---

## 2. Beachhead Market Strategy (Crossing the Chasm — Geoffrey Moore)

### The Bowling Alley Principle
Knock down the lead pin (beachhead) and the rest fall in sequence. In business: achieve dominant share in a narrow initial market, then expand naturally into adjacent segments.

### 5 Criteria for a Valid Beachhead

**Criterion 1: Do They Have Budget? (Budget Authority)**
- Does the decision-maker directly control the purchase budget?
- How long is the buying cycle? (< 3 months is ideal for early-stage B2B)

**Criterion 2: Do They Talk to Each Other? (Word-of-Mouth Network)**
- Is there a community where members know and refer each other?
- If one person adopts, does it naturally spread to 10 more?
- Signals: Active LinkedIn group, Slack community, industry conference

**Criterion 3: Are They in Enough Pain? (Pain Urgency)**
- How much are they currently spending to solve this problem?
- Are they using workarounds (spreadsheets, manual processes)?
- "Finally!" reaction vs. "Nice to have" reaction

**Criterion 4: Can We Win Here? (Winnable)**
- Can we achieve #1 in this segment?
- Are incumbents focused elsewhere and leaving this segment underserved?
- Does our differentiation shine brightest for this specific segment?

**Criterion 5: Is There an Expansion Path? (Leverage)**
- After winning the beachhead, what adjacent markets open up naturally?
- Is there a clear 2-3 step expansion sequence?

### Beachhead Size Guidelines

| Size | Verdict | Reason |
|------|---------|--------|
| < 100 reachable customers | Too small | Research ROI is not justified |
| 100 – 1,000 | Goldilocks | Can know names and faces; focused domination |
| 1,000 – 10,000 | Borderline | Possible but requires tight focus management |
| > 10,000 | Not a beachhead | Equivalent to targeting "the whole market" |

### Example Transformation

```
Bad:  "Target the small business (SMB) market."
      → SMB = millions of companies. Not a beachhead.

Good: "US-based boutique interior design studios, 5–20 employees,
       New York and Los Angeles (approx. 3,000 studios nationwide)"
      → Specific, reachable, has a community (ASID), identifiable pain
```

---

## 3. TAM / SAM / SOM Sizing Standards

### External Source Requirements (Mandatory)

TAM figures must include at least 2 sources from the following:

**Tier 1 Sources (Highest credibility)**
- Gartner Market Databook
- Forrester Research
- IDC (International Data Corporation)
- McKinsey Global Institute
- Statista (paid reports)

**Tier 2 Sources (High credibility)**
- Grand View Research
- MarketsandMarkets
- Allied Market Research
- Bloomberg Intelligence
- CB Insights (sector-specific)

**Acceptable but requires Tier 1 cross-validation**
- Industry association publications
- Market size figures cited in company IR filings
- Reputable media citations (WSJ, FT, TechCrunch)

**Required citation format**
```
- TAM: $12.4B (Gartner, "Cloud Security Market Forecast 2024–2028", March 2024)
- URL: https://www.gartner.com/...
```

### Top-Down vs. Bottom-Up Consistency Check

If results differ by more than 50%, analyze which method is flawed and state why.
```
Top-down:   Global $50B × US share 40% × target segment 15% = $3B SAM
Bottom-up:  50,000 target firms × $60,000 ACV = $3B SAM ✓
→ Both methods align. TAM estimate is reliable.
```

### SOM Estimation Standards

**Year 1 SOM**: 0.1% – 1% of SAM
- Early-stage startup benchmark: 10 – 200 customers
- "Number of customers you can realistically reach directly"

**Year 3 SOM**: 1% – 10% of SAM
- Median comparable B2B SaaS at Year 3: 2–5% of SAM
- Median comparable B2C SaaS at Year 3: 0.5–2% of SAM

**SOM Sanity Check (Mandatory)**
```
Back-calculate from Year 3 SOM target:
- Target revenue:  $XM
- Average Contract Value (ACV): $Y
- Required customers: $XM ÷ $Y = Z customers

→ Is acquiring Z customers in 3 years realistic?
  Z customers ÷ 36 months = N new customers/month required.
  Can the sales/marketing budget support this?
```

---

## 4. Market Growth Classification

| CAGR | Classification | Strategic Implication |
|------|---------------|----------------------|
| > 25% | High growth | Land-grab speed is the strategy; execution pace is everything |
| 15–25% | Growth | Both differentiation and execution speed matter equally |
| 8–15% | Stable growth | Differentiation and profitability outweigh speed |
| 5–8% | Low growth | Must capture share from incumbents; moat required |
| < 5% | Stagnant/Mature | Niche-only strategy or reconsider market entry |

---

## 5. Advanced Competitive Analysis

### Christensen's Disruption Positioning

Classify where your product sits in one of three positions:

**1. Low-End Disruption**
- Target customers who are over-served by existing products
- "Good enough" product at a significantly lower price
- Example: Google Docs vs. Microsoft Office

**2. New-Market Disruption**
- Create new customers from non-consumers who couldn't use existing solutions
- Simplicity and accessibility are the core value drivers
- Example: Canva vs. Adobe Photoshop (targeting non-designers)

**3. Sustained Innovation**
- Better product for existing customers
- Not disruptive — incremental improvement
- High competition intensity; strong differentiation required

### Mandatory Competitive Profile (per competitor)

For each direct competitor (minimum 3), include:
1. **Price** (public pricing or estimated with reasoning)
2. **Core differentiation** (what they claim as their #1 advantage)
3. **Actual weakness** (sourced from reviews — not opinion)
4. **Customer segment** (who they actually serve, not who they say they target)
5. **Recent changes** (last 12 months: funding, new features, pricing changes)

**Sources for real weaknesses** (use WebSearch):
- G2, Capterra, Trustpilot — filter for 1–2 star reviews, extract common complaints
- Hacker News "Ask HN: What do you use for X?" threads
- Reddit r/[industry] community discussions

---

## 6. Output Checklist (before saving market-analysis.md)

```
□ TAM figures include at least 2 external source URLs (Tier 1/2)
□ "Why Now" section present — one of the three triggers (tech/regulatory/behavioral) named explicitly
□ Beachhead market is concretely defined: [Country], [Job/Industry], [Size] — ~X reachable customers
□ Beachhead size is within 100–10,000 range (flag if outside)
□ SOM Year 3 includes back-calculation: Target $XM ÷ ACV $Y = Z customers ÷ 36 months = N/month
□ Minimum 3 direct competitors with price + real weakness (review-sourced) + segment
□ CAGR has source attribution
□ Christensen disruption type explicitly labeled (low-end / new-market / sustained)
```

---

## 7. Quality Self-Assessment Block (add at top of output before saving)

```markdown
---
**Market Research Quality Check**
- Evidence: [1–3] — [reason: X external sources included]
- Specificity: [1–3] — [reason: Beachhead defined as X-person market]
- Why Now: [present/missing] — [category: technology/regulatory/behavioral]
- TAM External Sources: [X sources]
- Unmet criteria: [list items or "none"]
---
```
