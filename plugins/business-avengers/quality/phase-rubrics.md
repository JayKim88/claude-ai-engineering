# Business Avengers Phase Quality Rubrics

## Evaluation System

### 3 Dimensions

| Dimension | Description | 1 (Redo) | 2 (Basic Pass) | 3 (Expert Level) |
|-----------|-------------|----------|----------------|-----------------|
| **Depth** | Actionable detail | Direction only ("build a GTM strategy") | Key decisions present but execution steps unclear | Anyone could execute this tomorrow |
| **Evidence** | Data / source-based | Assumptions only, no sources | Some data but sources unclear | All key figures have source URLs or explicit reasoning |
| **Specificity** | Numbers / names / dates | Abstract ("many users", "fast growth") | Some figures but units/ranges unclear | All key claims include numbers, names, dates |

### Pass Thresholds
- **1**: Redo required — revise the section and re-evaluate
- **2**: Minimum pass — early-stage startup acceptable; proceed to next phase
- **3**: Target level — VC-ready or senior consultant standard

**Goal**: Average Evidence score ≥ 2.5 across all outputs

---

## Phase 0: Ideation — Idea Canvas

### Mandatory Checklist

```
□ Is the problem described as a specific person in a specific situation?
  - BAD: "Many people feel inconvenient"
  - GOOD: "Freelance designers waste ~3 hours/week manually building
           invoices in Excel every time they send a quote to a client"

□ Are 3+ existing alternatives (solutions) named?
  (spreadsheets, Tool A, Tool B, etc.)

□ Is the differentiation "structural"? (something competitors cannot easily copy)
  - BAD: "We are easier to use"
  - GOOD: "We have exclusive access to [specific data source] that would take
           competitors 6+ months to replicate"

□ Is a revenue hypothesis stated?
  - GOOD: "Estimated willingness to pay ~$29/month — based on similar service Y at $35"

□ Are 2+ core assumptions explicitly listed?
  (Naming assumptions before validation clarifies future pivot decisions)

□ Is a JTBD statement written in "When [X] / I want [Y] / So I can [Z]" format?
  - BAD: "Users want a faster invoicing tool"
  - GOOD: "When I finish a project and need to get paid quickly,
           I want to send a professional invoice in under 5 minutes,
           so I can maintain cash flow without looking disorganized to clients"

□ Is a "Why Now" or switching trigger present?
  - What changed recently (technology / behavior / regulation / cost) that makes this timely?
  - If no "Why Now" exists, it must be explicitly flagged as a timing risk
```

### Rubric (Phase 0)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Problem specificity** | "Many people are inconvenienced" | Specific profession's pain | Specific situation + specific action + quantified pain |
| **Differentiation** | "We do it better" | Specific feature advantage | Structural reason competitors cannot replicate |
| **Revenue hypothesis** | None | "Subscription" mentioned | "$X/month, basis: comparable service Y at $Z" |
| **Assumptions stated** | None | < 2 | 2+ with proposed validation method |
| **JTBD quality** | Missing or generic ("users want X") | Functional job stated only | Situation + motivation + outcome, all specific; switching trigger identified |
| **Why Now** | None | General trend mentioned ("AI is growing") | Named technology/behavior/regulatory shift with specific enabling change |

---

## Phase 1: Market Research — Market Analysis

### Mandatory Checklist

```
□ TAM figures include at least 2 external source URLs?
  (Gartner, Forrester, IDC, Statista — Tier 1/2 sources)

□ "Why Now" section present with at least one of the following:
  - Technology shift (new tech makes this possible)
  - Regulatory shift (new law opens or closes the market)
  - Behavioral shift (large event changed consumer acceptance)

□ Beachhead market concretely defined?
  Format: "[Country], [Job/Industry], [Size] — ~X reachable customers"

□ Beachhead size within 100–10,000 customer range?

□ SOM Year 3 includes customer count back-calculation?
  Format: "Target $XM ÷ ACV $Y = Z customers ÷ 36 months = N/month required"

□ CAGR has source attribution?

□ 3+ direct competitors with: price / real weakness (from reviews) / actual segment?
```

### Rubric (Phase 1: Market Analysis)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **TAM evidence** | No sources | 1 source | 2+ Tier 1/2 sources with URLs |
| **Why Now** | None | "AI is trending" level | Specific tech/regulatory/behavioral trigger + timeline |
| **Beachhead** | None | "SMB market" level | Country + job + size + reachable customer count |
| **SOM validation** | None | % figure only | Customer back-calc + monthly acquisition rate required |
| **Competitor weaknesses** | None | "Has weaknesses" | G2/Capterra/Reddit-sourced real user complaints |

### Phase 1 Self-Assessment Block (add at top of output)

```markdown
---
**Market Research Quality Check**
- Evidence: [1–3] — [X external sources included]
- Specificity: [1–3] — [Beachhead: defined as X-person market]
- Why Now: [present/missing] — [category: technology/regulatory/behavioral]
- TAM External Sources: [X]
- Unmet criteria: [list or "none"]
---
```

---

## Phase 2: Product Planning — PRD

### Mandatory Checklist

```
□ Each Must Have feature has a rationale: "Without this, X% of users would churn"
  or "Without this, core value cannot be delivered"

□ MVP scope fits "1 person, 6 weeks" (Shape Up Appetite principle: Fixed time, variable scope)?

□ Success metrics are action-based?
  - BAD: "User growth", "satisfaction improvement"
  - GOOD: "≥ 60% of users complete core action within 7 days of signup"

□ "What we will NOT build" list is explicitly stated?

□ Features with RICE Confidence < 50% are flagged separately?
```

### Rubric (Phase 2)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Feature priority rationale** | None | MoSCoW only | RICE score + churn justification |
| **MVP scope** | Unclear | Feature list only | 6-week / 1-person Appetite stated explicitly |
| **Success metrics** | "Growth" level | KPI list | Action-based + numerical targets |
| **Scope boundary** | None | Partial | "Will not build" list explicitly stated |

---

## Phase 3: Design — Design System & Wireframes

### Mandatory Checklist

```
□ Color system: Primary, Secondary, Semantic (Success/Error/Warning/Info) all defined
□ Typography: Mobile and desktop scale both specified
□ Spacing: 8px grid-based system stated
□ Button states: Default / Hover / Active / Disabled / Loading all defined
□ WCAG 2.1 AA compliance: minimum 4.5:1 contrast ratio
□ Click count to core action stated (target: ≤ 3 clicks)
□ Empty State screen (no data state) included
□ Error State screen (failure state) included
```

### Rubric (Phase 3)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Component completeness** | Colors only | Major components | All states (Default/Hover/Active/Disabled) |
| **Accessibility** | None | "Accessibility considered" | WCAG 2.1 AA explicit + contrast ratio value |
| **UX flow** | Screen list only | Flow diagram | Click count + Empty/Error state included |

---

## Phase 4: Technical Planning — Architecture

### Mandatory Checklist

```
□ Monolith vs. Microservices choice has an explicit rationale?
  (Default: Monolith if MAU < 100K)

□ First-month infrastructure cost estimate included? ($X/month)

□ Database choice has reasoning beyond "preference"?

□ 3+ key technical decisions documented in ADR format?
  Format: Context → Decision → Consequences (Alternatives Considered)

□ 12-Factor App non-compliant items explicitly listed? (technical debt transparency)
```

### Rubric (Phase 4)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Architecture decision rationale** | "We prefer it" level | Pros/cons mentioned | ADR format (Context / Decision / Consequences) |
| **Cost transparency** | None | Rough estimate | $X/month first month + per-service breakdown |
| **Tech debt awareness** | None | "Improve later" | Intentional simplifications listed + resolution timeline |

---

## Phase 5: Development Guide

### Mandatory Checklist

```
□ Setup guide reaches "deployable Hello World" in under 30 minutes?
□ Test coverage targets: MVP ≥ 40%, core business logic ≥ 80%
□ DORA metrics goal: Deployment Frequency ≥ once/week
□ Intentional technical debt register included?
```

### Rubric (Phase 5)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Onboarding speed** | None | Install guide | 30-minute Hello World step-by-step |
| **Test strategy** | "Testing needed" | Types listed | Coverage targets + Test Pyramid ratios |
| **Deployment maturity** | None | CI/CD mentioned | DORA metrics targets stated explicitly |

---

## Phase 6: QA Planning

### Mandatory Checklist

```
□ Test Pyramid ratios stated: Unit 70% : Integration 20% : E2E 10%
□ Critical path tests: payment/cancellation/core conversion flows 100% covered
□ Core Web Vitals targets: LCP < 2.5s, FID < 100ms, CLS < 0.1
□ Pre-launch smoke test list: completable in under 10 minutes
□ Applicable OWASP Top 10 items checked
```

### Rubric (Phase 6)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Test coverage** | "We will test" | Unit/integration/E2E mentioned | Pyramid ratios + coverage targets |
| **Performance targets** | None | "Make it fast" | Core Web Vitals numerical targets |
| **Launch readiness** | None | Checklist present | 10-minute smoke test scenario list |

---

## Phase 7: Launch Strategy — GTM

### Mandatory Checklist

```
□ Bullseye Framework applied: 3 channels selected from 19 with explicit rationale?
□ Launch timeline covers: D-30 / D-14 / D-7 / D-1 / D-Day / D+7?
□ "First 100 users" sourcing plan with specific channels and outreach method?
□ Per-channel kill criteria: "Abandon if metric X is below Y after 7 days"?
□ Product Hunt launch decision made (with readiness checklist)?
```

### Rubric (Phase 7)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Channel strategy** | "Social media" level | 3 channels listed | Bullseye rationale + success/kill criteria |
| **Launch timeline** | None | "D-Day plan" | D-30 through D+7 with specific daily/weekly tasks |
| **First users** | "We will market" | Channels mentioned | "First 100: [specific path]" with names/communities |

---

## Phase 8: Monetization — Pricing & Financial Projections

### Mandatory Checklist

```
□ Unit Economics thresholds met or flagged:
  - LTV:CAC > 3:1 (if not met → recommend business model review to CEO)
  - CAC Payback Period < 12 months

□ Gross Margin: ≥ 70% for SaaS
  (if not met → state reason and roadmap to achieve)

□ Three scenarios included:
  - Best:  Base × 1.5
  - Base:  Current assumptions
  - Worst: Base × 0.5

□ Breakeven MRR and expected month to reach it stated?

□ Pricing page: 3-tier structure using Goldilocks principle?
  (Low tier: feature-limited, High tier: clearly Enterprise, Middle tier: most attractive)
```

### Rubric (Phase 8)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Unit Economics** | No LTV/CAC | Individual figures present | LTV:CAC ratio + Payback Period in months |
| **Scenario analysis** | 1 forecast only | Best/Worst present | 3 scenarios + assumptions per scenario |
| **Breakeven clarity** | "Eventually" | MRR mentioned | Breakeven MRR + expected month (M+X format) |
| **Pricing structure** | None | Prices listed | Goldilocks 3-tier + feature mapping |

---

## Phase 9: Operations

### Mandatory Checklist

```
□ Single North Star Metric selected (multiple = re-select)
□ AARRR measurement tool specified per stage (Mixpanel/PostHog/Amplitude)
□ CS response SLA: Free 48h / Paid 24h / Enterprise 4h
□ "Same question 3 times → FAQ or automate" rule applied?
□ OKR: 1 Objective + ≤ 3 Key Results per quarter
```

### Rubric (Phase 9)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **North Star** | None | Multiple KPIs | 1 metric + measurement method |
| **CS standards** | None | "Reply quickly" | Tier-based SLA (in hours) |
| **OKR** | None | Goals listed | 1 Objective + ≤ 3 KRs + measurement method |

---

## Phase 10: Growth

### Mandatory Checklist

```
□ PMF measurement method stated (Sean Ellis 40% Rule or alternative metric)?
□ Growth Loop defined: "More users → [specific action] → even more users"
□ Only experiments with ICE score ≥ 6 included in priority list?
□ Retention curve targets set: D1 / D7 / D30
  (SaaS reference: target D30 > 40%)
□ Viral Coefficient K > 0.5 plan or alternative stated?
```

### Rubric (Phase 10)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **PMF standard** | None | "PMF achieved" | 40% Rule or alternative metric + current value |
| **Growth Loop** | None | "Viral" mentioned | "A → B → C → more A" — concrete mechanism |
| **Experiment plan** | Ideas listed | Priority order | ICE scores + success criteria per experiment |

---

## Phase 11: Automation

### Mandatory Checklist

```
□ Automation ROI calculated: Time saved (hrs/month) × hourly rate vs. build cost?
□ Bus Factor test: Tasks that would stop without CEO for 7 days — listed?
□ Automation priority: All recurring tasks > 2 hrs/month that can be automated — listed?
□ Tool selection principle: No-code first → Low-code → Custom code?
□ Failure alerts configured for each automation — stated?
```

### Rubric (Phase 11)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **ROI analysis** | None | "Automation is good" | Hours saved × rate vs. build cost formula |
| **Bus Factor** | None | "Needs documentation" | CEO-absent 7-day task halt list |
| **Priority** | Ideas listed | By importance | Monthly hour basis + tool selection rationale |

---

## Phase 12: Scale & Exit

### Mandatory Checklist

```
□ Valuation: ARR × multiple calculation with multiple rationale (NRR, growth rate basis)?
□ Built to Sell checklist applied (5 conditions):
  1. Single focused service (no complex customization)
  2. Operates without CEO retained post-acquisition
  3. Recurring revenue (MRR/ARR) in place
  4. No single customer > 15% of revenue
  5. Service delivery process fully documented
□ Platform comparison table: MicroAcquire / Empire Flippers / Direct negotiation?
□ Earnout negotiation points: 3+?
```

### Rubric (Phase 12)

| Criterion | 1 | 2 | 3 |
|-----------|---|---|---|
| **Valuation** | None | ARR mentioned | ARR × multiple + multiple rationale |
| **Sale readiness** | None | "Can be sold" | Built to Sell 5-condition check + unmet items |
| **Platform strategy** | None | 1 platform mentioned | Comparison table + fit criteria per platform |
