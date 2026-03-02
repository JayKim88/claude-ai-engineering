# Growth Engineering Knowledge Base

Expert growth frameworks for Phase 10 (Growth Execution).
Source: Sean Ellis (Hacking Growth), Andrew Chen (The Cold Start Problem),
Reforge curriculum, Nir Eyal (Hooked), Casey Winters (growth loop theory).

---

## 1. Product-Market Fit Signal

### Sean Ellis PMF Test
Survey active users (used product in last 2 weeks) with one question:
> "How would you feel if you could no longer use [product]?"

| Response | Score | Interpretation |
|----------|-------|----------------|
| Very disappointed | Count as PMF signal | Core metric |
| Somewhat disappointed | Neutral | |
| Not disappointed | Churn risk | |
| Already stopped using | Lost customer | |

**PMF threshold: ≥40% answer "Very disappointed"**
- <25%: No PMF — do not scale yet. Fix retention first.
- 25–39%: Weak PMF — identify what the 40%+ segment looks like; narrow ICP
- ≥40%: PMF signal — safe to begin scaling acquisition

**Segmentation rule:** If overall score is 32% but a specific segment scores 55%, you have PMF — just in a narrower niche than you thought.

### Retention Curve Test (Reforge)
Plot cohort retention curve over 8–12 weeks.

```
Retention %
100 │╲
 80 │  ╲
 60 │    ╲___
 40 │        ╲____
 20 │              ╲____
  0 └──────────────────────→ Week
   W0 W1  W2  W3  W4  W5  W8

Patterns:
  └── DEATH CURVE: retention → 0% — NO PMF
  └── ASYMPTOTIC: levels off at 15–40% — PMF signal
  └── SMILE CURVE: retention dips then recovers — PMF + engagement cycle
```

**Asymptotic floor benchmarks:**
- Consumer social apps: 15–25% D30 retention
- Consumer productivity: 25–40% D30
- B2B SaaS: 70–90% M6 retention (monthly churn benchmark: <2%)

---

## 2. North Star Metric Framework

### What is the NSM?
One metric that captures the value delivered to users AND predicts long-term revenue.

**NSM selection criteria:**
1. Captures value delivery (not just revenue or signups)
2. Measurable and movable by the team
3. Leading indicator of long-term retention
4. Simple enough to rally the whole team

**NSM examples by business type:**

| Business Type | North Star Metric | Why |
|---------------|------------------|-----|
| Communication tool | Messages sent per week | Value = communication |
| Project management | Projects completed | Value = completion |
| Analytics SaaS | Dashboards viewed per week | Value = insight consumption |
| Marketplace | Successful transactions | Value = match-making |
| Content platform | Minutes of content consumed | Value = engagement |
| Developer tool | API calls per week | Value = integration depth |

**Input Metrics → NSM (work backwards):**
```
NSM: "Weekly active users who complete 1+ project"
  ├── Acquisition: new signups/week
  ├── Activation: % who create first project within 7 days
  ├── Engagement: % who return and complete a project
  └── Expansion: avg projects per active user
```

**Anti-patterns (bad NSMs):**
- Revenue (lagging; can game with discounts)
- Signups (vanity; doesn't indicate value delivery)
- Page views (can inflate via poor UX)
- App opens (doesn't indicate value)

---

## 3. Growth Loops (Andrew Chen / Reforge)

### Growth Loops vs. AARRR Funnel
AARRR is a linear funnel. Growth Loops are compounding systems where output becomes input.

```
AARRR (linear — diminishing):
Acquisition → Activation → Retention → Revenue → Referral
Each stage loses users; growth slows as top-of-funnel cost rises.

Growth Loop (compounding):
User does valuable thing → Product becomes more valuable → Attracts more users → repeat
```

### The 4 Core Growth Loop Types

**1. Viral Loop (Content/Sharing)**
```
User creates content → Shares publicly → New user discovers → Signs up → Creates content
```
Examples: Canva (shares designs), Loom (shares videos), Notion (shares pages)
K-factor formula: K = (invites sent per user) × (conversion rate)
K > 1 = exponential growth; K < 1 = supplemental channel only

**2. Paid Growth Loop**
```
User pays → Revenue → Spend on ads → New user acquired → User pays
```
Viable when: LTV:CAC > 3:1, CAC payback < 12 months
Not a loop if: margins are negative — you're just buying growth

**3. Content SEO Loop**
```
User-generated content → Indexed by Google → Organic traffic → New users → UGC
```
Examples: Glassdoor, Yelp, Stack Overflow
Build time: 6–18 months; compounding accelerates after month 12

**4. Product/PLG Loop**
```
User invites colleague → Colleague joins → Team uses together → Network effect → More invites
```
Examples: Slack, Figma, Notion teams
Requires: inherent collaboration value; sharing features baked into product

### Loop Selection Guide

| If you have... | Best loop |
|----------------|-----------|
| Naturally shareable output (reports, designs, results) | Viral/Content loop |
| Strong SEO opportunity (problem-aware users search) | SEO Content loop |
| Team/collaboration product | PLG viral loop |
| High LTV B2B | Paid loop (if CAC economics work) |
| API / integration use case | Developer distribution loop |

---

## 4. Activation Engineering — The Aha Moment

### What is the Aha Moment?
The specific action where a user first experiences the core value. Activation = user reaches Aha Moment.

**Finding the Aha Moment (data method):**
1. Define 3–5 candidate "power user actions"
2. Compare D30 retention rates between users who did vs. didn't do each action in first 7 days
3. The action with highest retention delta = Aha Moment

**Examples:**
| Product | Aha Moment |
|---------|-----------|
| Slack | Send 2,000 messages as a team |
| Dropbox | Put 1 file in Dropbox folder |
| Facebook | 7 friends in 10 days |
| Twitter | Follow 30 accounts |
| Airbnb | Complete first booking |

### Activation Funnel Optimization

```
Signup → Onboarding → First value action → Habit formation
  │           │               │                  │
  ▼           ▼               ▼                  ▼
Drop-off:   Drop-off:     Drop-off:          Drop-off:
form too    too long/     confusing/         no habit
complex     no guidance   no quick win       trigger
```

**Activation rate benchmarks:**
- Weak: < 20% complete onboarding
- Average: 20–40%
- Good: 40–60%
- Excellent: > 60%

**Activation optimization tactics:**
1. Remove friction: reduce signup form to email + password only
2. Progressive onboarding: 3-step checklist, not 10-step wizard
3. Time-to-value: user sees value in <5 minutes
4. Aha Moment shortcut: guide user directly to the core action
5. Empty state design: never show a blank screen; pre-populate with example data

---

## 5. Retention Engineering

### Retention Curve Analysis
Plot M1, M3, M6, M12 retention for each acquisition cohort.

**Retention benchmarks (SaaS):**

| Metric | Bad | OK | Good | Elite |
|--------|-----|-----|------|-------|
| M1 retention | <40% | 40–60% | 60–80% | >80% |
| M3 retention | <25% | 25–45% | 45–65% | >65% |
| M6 retention | <20% | 20–40% | 40–60% | >60% |
| Annual churn | >25% | 15–25% | 5–15% | <5% |

**Churn analysis framework — 5 root causes:**
1. Didn't reach Aha Moment (fix onboarding)
2. Value not habitual — only occasional use (fix engagement loop)
3. Job changed / company changed (unavoidable; segment out)
4. Competitor poached (check competitive analysis)
5. Budget cut (price point issue; check LTV tier)

### The Hook Model (Nir Eyal)

```
Trigger → Action → Variable Reward → Investment → Trigger (next cycle)
```

**Four elements:**

| Element | Purpose | Examples |
|---------|---------|---------|
| External Trigger | Bring user back | Email, push notification, SMS |
| Internal Trigger | Habit-forming association | FOMO, boredom, anxiety about missing info |
| Action | Simplest behavior in anticipation of reward | 1-click, minimal effort |
| Variable Reward | Unpredictable; maintains desire | Social validation, new content, achievement |
| Investment | User stores value; raises switching cost | Profile data, content creation, customization |

**Investment examples that drive retention:**
- Saved templates / configurations
- Uploaded data / history
- Built integrations
- Trained preferences (recommendations engine)
- Social connections / followers built

---

## 6. Growth Experiment Prioritization

### ICE vs. RICE vs. BRASS

| Framework | Components | Best for |
|-----------|-----------|---------|
| ICE | Impact × Confidence × Ease | Quick prioritization; early-stage |
| RICE | Reach × Impact × Confidence ÷ Effort | More rigorous; growth team |
| BRASS | Bets, Risk, Alignment, Spread, Size | Portfolio approach; complex experiments |

### ICE Scoring Guide

**Impact (1–10):** How much will this move the NSM?
- 9–10: Major funnel improvement (e.g., signup flow redesign)
- 6–8: Moderate improvement (e.g., email copy A/B)
- 1–5: Minor improvement (e.g., button color)

**Confidence (1–10):** How sure are we it will work?
- 9–10: Backed by user research + competitor evidence
- 6–8: Strong intuition, some data
- 1–5: Hunch, no evidence

**Ease (1–10):** How easy to implement? (inverse of effort)
- 9–10: 1 hour, no code
- 6–8: 1–3 days dev
- 1–5: 1+ week dev

**ICE Score = (I + C + E) / 3** — Run in order of score.

### Experiment Velocity Standard
- Run ≥2 experiments per week (growth team)
- Each experiment needs: hypothesis, metric, success threshold, duration, sample size
- Duration: minimum 2 weeks; stop early only if >95% confidence threshold hit
- Document: winner/loser AND learning — both have value

---

## 7. Growth Output Quality Standards (Phase 10)

**Growth plan must address all 5 AARRR stages with specific tactics:**

| Stage | Weak output | Strong output |
|-------|------------|---------------|
| Acquisition | "Use SEO and social" | "3 pillar SEO posts targeting [keyword cluster, 500 visits/mo], launching Week 2" |
| Activation | "Improve onboarding" | "Reduce onboarding steps from 7 to 3; guide users to Aha Moment (first X) within 5 mins" |
| Retention | "Send re-engagement emails" | "D7 win-back sequence: 3-email series if no login; segment by last action" |
| Revenue | "Increase conversions" | "Upgrade prompt at 3 trigger points: feature gate hit, 80% quota used, 30-day mark" |
| Referral | "Add referral program" | "Referral prompt at moment of success (after first X), 2-sided incentive: $Y credit each" |

**Growth Plan Checklist (Phase 10):**
- [ ] PMF score stated or retention curve described (evidence of signal before scaling)
- [ ] North Star Metric defined (not revenue, not signups)
- [ ] Input metrics listed (3–5 metrics that drive NSM)
- [ ] Primary growth loop identified (viral / SEO / paid / PLG) with rationale
- [ ] Aha Moment defined: specific action + target timeframe
- [ ] Activation rate target stated with baseline
- [ ] Retention curve target by M1, M3 with specific tactics to move it
- [ ] ≥3 ICE-scored experiments proposed for first 90 days
- [ ] D7 / D30 retention metrics tracked in measurement plan

**Self-Assessment Block (add at top of growth output before saving):**
```markdown
---
**Growth Plan Quality Check**
- Depth: [1–3] — [specific loop design vs. generic channel list]
- Evidence: [1–3] — [PMF signal stated, retention benchmarks compared]
- Specificity: [1–3] — [Aha Moment named, NSM defined, ICE scores present]
- Growth loop type: [viral/SEO/paid/PLG] — [rationale stated]
- NSM: [defined/missing]
- PMF signal: [confirmed/unclear/no signal yet]
- Unmet criteria: [list or "none"]
---
```
