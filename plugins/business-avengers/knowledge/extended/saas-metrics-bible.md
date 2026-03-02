# SaaS Metrics Bible

## Source Methodologies
This guide synthesizes benchmarks and frameworks from:
- Bessemer Venture Partners — *State of the Cloud* (annual SaaS benchmarks)
- OpenView Partners — SaaS benchmarks report (product-led growth metrics)
- ProfitWell (now Paddle) — pricing and retention research
- David Skok — *For Entrepreneurs* (SaaS metrics fundamentals)
- Rob Walling — *The SaaS Playbook* (bootstrapped SaaS)
- Tomasz Tunguz — SaaS financial benchmarks

---

## Quick Decision Guide (Agent Decision Criteria)

| Metric | Warning Threshold | Action |
|--------|------------------|--------|
| LTV:CAC < 3:1 | Critical | Flag business model viability to CEO; do not proceed without addressing |
| CAC Payback > 18 months | High risk | Reduce CAC or increase ARPU before scaling |
| Gross Margin < 60% | Review | Investigate COGS structure; 70%+ is standard SaaS |
| Monthly Churn > 5% | Critical | Product-market fit may not be established |
| NRR < 90% | Warning | Revenue is shrinking on existing base; retention emergency |
| MRR growth < 10%/month (early) | Concern | Growth engine may not be working |

## Red Flags (Explicitly warn the CEO)
- LTV:CAC < 1:1 → company loses money on every customer; stop scaling until fixed
- Gross Margin < 50% → may not be a software business; review COGS composition
- Single customer > 30% of revenue → dangerous concentration risk
- Burn multiple > 2x → spending $2 to generate $1 of ARR; VC red flag

---

## 1. Core Unit Economics

### LTV : CAC Ratio

**Formula:**
```
LTV = ARPU × Gross Margin % ÷ Monthly Churn Rate
CAC = Total Sales & Marketing Spend ÷ New Customers Acquired (same period)
LTV:CAC Ratio = LTV ÷ CAC
```

**Benchmarks by stage:**

| Stage | LTV:CAC | Interpretation |
|-------|---------|----------------|
| Seed / Pre-PMF | < 1:1 | Expected; focus on finding PMF not scaling |
| Early (< $1M ARR) | 1:1 – 3:1 | Acceptable if improving |
| Growth ($1M–$10M ARR) | > 3:1 | Target minimum; < 3:1 needs attention |
| Scale (> $10M ARR) | > 5:1 | Strong; means channel efficiency |

**What it means:**
- < 1:1 → You lose money on every customer you acquire (stop scaling)
- 3:1 → Industry standard "healthy" threshold
- > 5:1 → Potentially under-investing in growth (could grow faster)

### CAC Payback Period

**Formula:**
```
CAC Payback = CAC ÷ (ARPU × Gross Margin %)
```

**Benchmarks:**

| Model | Healthy | Warning | Critical |
|-------|---------|---------|---------|
| PLG (Product-Led Growth) | < 6 months | 6–12 months | > 18 months |
| Sales-assisted | < 12 months | 12–18 months | > 24 months |
| Enterprise | < 18 months | 18–24 months | > 36 months |

### Gross Margin

**Formula:**
```
Gross Margin % = (Revenue - COGS) ÷ Revenue × 100
COGS includes: hosting, support, payment processing, professional services
```

**SaaS Benchmarks (Bessemer):**

| Type | Target | Warning | Critical |
|------|--------|---------|---------|
| Pure SaaS (no services) | 75–85% | 65–74% | < 60% |
| SaaS + professional services | 60–75% | 50–59% | < 50% |
| Usage-based SaaS | 65–80% | 55–64% | < 55% |

**If Gross Margin < 70%:** Identify which COGS component is high and include a roadmap to 70%+.

---

## 2. Revenue Metrics

### MRR / ARR Construction

```
MRR = Sum of all recurring monthly subscription revenue
ARR = MRR × 12

MRR Components (track separately):
- New MRR:        New customers this month
- Expansion MRR:  Upgrades from existing customers
- Churned MRR:    Lost from cancellations
- Contraction MRR: Downgrades from existing customers
- Reactivation MRR: Returning churned customers

Net New MRR = New MRR + Expansion MRR - Churned MRR - Contraction MRR
```

### Net Revenue Retention (NRR / NDR)

**Formula:**
```
NRR = (Starting MRR + Expansion MRR - Churned MRR - Contraction MRR) ÷ Starting MRR × 100
```

**Benchmarks (OpenView Partners):**

| NRR | Interpretation | Stage Typical |
|-----|---------------|---------------|
| > 130% | Elite (Snowflake, Datadog level) | Enterprise SaaS |
| 110–130% | Excellent | Growth SaaS with expansion |
| 100–110% | Good | Solid retention, some expansion |
| 90–100% | Acceptable early-stage | Pre-PMF acceptable |
| < 90% | Danger | Shrinking revenue on existing base |

**Why NRR > 100% matters:**
If NRR > 100%, revenue grows from existing customers even with zero new sales. This is the foundation of SaaS scalability.

### Churn Rate

**Monthly Churn Benchmarks:**

| Market | Elite | Target | Warning | Critical |
|--------|-------|--------|---------|---------|
| SMB SaaS | < 2% | 2–4% | 4–7% | > 7% |
| Mid-Market | < 1% | 1–2% | 2–4% | > 4% |
| Enterprise | < 0.5% | 0.5–1% | 1–2% | > 2% |

**Annual Churn = 1 - (1 - Monthly Churn)^12**
- 5% monthly = 46% annual (catastrophic)
- 2% monthly = 21% annual (challenging)
- 1% monthly = 11% annual (acceptable)
- 0.5% monthly = 6% annual (good)

---

## 3. Growth Metrics

### MRR Growth Rate Benchmarks (Early Stage)

| ARR Stage | Elite Monthly Growth | Target | Warning |
|-----------|---------------------|--------|---------|
| $0 – $100K | > 20%/month | 15–20% | < 10% |
| $100K – $1M | > 15%/month | 10–15% | < 7% |
| $1M – $10M | > 10%/month | 7–10% | < 5% |
| $10M+ | > 5%/month | 3–5% | < 2% |

### Rule of 40

For mature SaaS (> $1M ARR):
```
Rule of 40 = Revenue Growth Rate (%) + EBITDA Margin (%)
```

| Score | Interpretation |
|-------|---------------|
| > 60 | Elite (Zoom-level) |
| 40–60 | Strong |
| 20–40 | Acceptable |
| < 20 | Concerning for investors |

*Note: Pre-$1M ARR, pure growth matters more than Rule of 40.*

### Burn Multiple

```
Burn Multiple = Net Burn ÷ Net New ARR
```

| Multiple | Investor View | Meaning |
|----------|--------------|---------|
| < 0.5x | Excellent | Very efficient growth |
| 0.5x – 1x | Good | Normal SaaS efficiency |
| 1x – 1.5x | Acceptable | Early stage acceptable |
| 1.5x – 2x | Concerning | Spending a lot to grow |
| > 2x | Red flag | Unsustainable without product changes |

---

## 4. Bootstrapped SaaS Benchmarks (Rob Walling)

For indie makers and bootstrapped founders, different benchmarks apply:

### Pricing Benchmarks (Bootstrap SaaS)

| Target Market | Typical ACV | ARPU/Month | Customer Count for $10K MRR |
|---------------|-------------|------------|----------------------------|
| Individual / Solo | $5 – $30/mo | $15 | 667 customers |
| SMB (small teams) | $30 – $200/mo | $75 | 133 customers |
| Mid-Market | $200 – $1,000/mo | $400 | 25 customers |
| SMB Annual Plans | $300 – $2,000/yr | $100–$165 | 61–100 customers |

**Lesson (Walling):** It's easier to acquire 25 customers at $400/month than 667 customers at $15/month. Price higher than you're comfortable with initially.

### Bootstrapped Milestones

| Milestone | Meaning |
|-----------|---------|
| $1K MRR | Proof of concept — people will pay |
| $10K MRR | Ramen profitable (1 founder) |
| $25K MRR | Solid lifestyle business |
| $50K MRR | Hire first employee |
| $100K MRR | Small but real company |

---

## 5. Financial Projections — Mandatory Standards

### Three-Scenario Framework

Every financial projection must include three scenarios:

```
Best Case  = Base assumptions × 1.5 (50% better than expected)
Base Case  = Current assumptions (most likely outcome)
Worst Case = Base assumptions × 0.5 (50% worse than expected)
```

Each scenario must state the key assumption that changes:
- Best: "CAC is 30% lower due to organic referral momentum"
- Base: "CAC remains at current $X, churn at Y%"
- Worst: "CAC 50% higher due to paid channel saturation, churn 2× base"

### Breakeven Analysis (Mandatory)

```
Breakeven MRR = Fixed Monthly Costs ÷ Gross Margin %

Example:
Fixed costs: $5,000/month (tools, subscriptions, part-time help)
Gross Margin: 75%
Breakeven MRR = $5,000 ÷ 0.75 = $6,667/month

→ At $75 ARPU: need 89 customers to break even
→ At $29 ARPU: need 230 customers to break even
```

**Required output:** State the breakeven MRR and the month in which it's projected to be reached (e.g., "Month 18" or "M+18").

---

## 6. Pricing Structure — Goldilocks Principle

### Three-Tier Design (Mandatory for SaaS)

Every pricing page should use 3 tiers with Goldilocks psychology:

| Tier | Role | Design Rule |
|------|------|-------------|
| Free / Starter | Attract, not monetize | Feature-limited; upsell bait |
| Pro / Core | **Primary revenue tier** | Best value; most prominent visually |
| Business / Enterprise | Anchor the Pro tier | Make Pro look reasonable by comparison |

**The Goldilocks effect:** When customers see three tiers, ~60% choose the middle option.
Design the middle tier as the one you want most customers on.

### Value Metric Selection

Choose ONE value metric that scales with customer success:

| Value Metric | Best For | Anti-Pattern |
|-------------|----------|-------------|
| Per seat / user | Team collaboration tools | Bad if users are "viewers" not active |
| Per usage (API calls, events) | Infrastructure, analytics | Unpredictable revenue |
| Per outcome (emails sent, invoices) | Email tools, billing | Creates friction at high usage |
| Flat monthly | Simple tools, indie | Doesn't scale with value delivered |

**Rule:** If a customer 10×s their usage of your product, do they pay 10× more? If they should, price by usage. If not, price flat.

### Annual vs. Monthly Pricing

Standard practice:
- Annual = 2 months free (16.7% discount) = 10× industry norm
- Offer annual to improve cash flow; target 30–50% of customers on annual

---

## 7. Output Quality Standards

Before saving any financial document, verify:

```
□ LTV:CAC ratio calculated and benchmark comparison stated
□ CAC Payback Period calculated (in months)
□ Gross Margin % stated with COGS breakdown
□ NRR estimated or benchmarked (if no real data, use comparable product)
□ Three scenarios present: Best (×1.5) / Base / Worst (×0.5)
□ Breakeven MRR stated + month projected to reach it (e.g., M+18)
□ Pricing uses 3-tier Goldilocks structure
□ Annual pricing offered at ~2 months free
□ If LTV:CAC < 3:1 → business model viability flag to CEO included
□ If Gross Margin < 70% → explanation and roadmap to 70%+ included
```

---

## 8. Quality Self-Assessment Block (add at top of financial output)

```markdown
---
**Financial Model Quality Check**
- Evidence: [1–3] — [benchmarks sourced from: Bessemer/OpenView/ProfitWell/comparable]
- Specificity: [1–3] — [BEP month stated, 3 scenarios present]
- LTV:CAC: [X:1] — [above/below 3:1 threshold]
- Gross Margin: [X%] — [above/below 70% SaaS benchmark]
- Scenarios: [Best/Base/Worst present: yes/no]
- Unmet criteria: [list or "none"]
---
```
