# Data Metrics and Analytics Guide

## Overview

This guide covers essential data analytics frameworks, key metrics, and measurement strategies for digital businesses. Learn how to track, analyze, and optimize your product's performance.

---

## 1. AARRR Metrics (Pirate Metrics)

### Framework Overview

Dave McClure's AARRR framework divides the customer lifecycle into five stages:

```
Acquisition → Activation → Retention → Revenue → Referral
```

Each stage has specific metrics to track and optimize.

### Acquisition Metrics

**Definition:** How users discover and arrive at your product.

#### Key Metrics

| Metric | Formula | What It Means | Target |
|--------|---------|---------------|--------|
| Traffic Sources | N/A | Where users come from | Diversified |
| Cost Per Click (CPC) | Ad spend / Clicks | Cost to get someone to click | <$2 (varies by industry) |
| Click-Through Rate (CTR) | Clicks / Impressions | % who click your ad | 1-3% (search), 0.5-1% (display) |
| Cost Per Acquisition (CAC) | Marketing spend / New customers | Cost to acquire a customer | <1/3 of LTV |
| CAC by Channel | Channel spend / Customers from channel | Which channels are most efficient | Varies |

#### Tracking Setup

**Google Analytics 4 (GA4):**
```javascript
// Install GA4
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>

// Track custom events
gtag('event', 'page_view', {
  page_title: 'Homepage',
  page_location: window.location.href
});
```

**UTM Parameters for Campaign Tracking:**
```
https://yoursite.com?utm_source=twitter&utm_medium=social&utm_campaign=launch&utm_content=variant_a

Parameters:
- utm_source: Where traffic comes from (twitter, google, newsletter)
- utm_medium: Marketing medium (social, email, cpc, organic)
- utm_campaign: Campaign name (launch, black_friday, webinar_signup)
- utm_content: Specific link/ad (variant_a, hero_button, footer_link)
```

#### Channel Performance Analysis

```
Example Monthly Acquisition Data:

Channel          | Users | Customers | CAC    | Notes
-----------------|-------|-----------|--------|------------------
Organic Search   | 5,000 | 100       | $0     | Best long-term
Google Ads       | 2,000 | 60        | $50    | Expensive but qualified
Facebook Ads     | 3,000 | 45        | $40    | Lower intent
Content/Blog     | 1,500 | 30        | $10    | High ROI
Email (existing) | 1,000 | 80        | $5     | Best conversion
Referral         | 800   | 40        | $0     | Viral growth

Analysis:
- Email has best conversion (8%)
- Organic search has most volume (scale potential)
- Google Ads is expensive but works (optimize)
- Referral shows product-market fit (encourage sharing)
```

### Activation Metrics

**Definition:** Users experience the core value of your product (the "Aha moment").

#### Key Metrics

| Metric | Formula | What It Means | Target |
|--------|---------|---------------|--------|
| Activation Rate | Users who reached "Aha" / Total signups | % who experience core value | >40% |
| Time to Value | Time from signup to "Aha moment" | How fast users get value | <24 hours |
| Onboarding Completion | Users who finish onboarding / Signups | % completing setup | >60% |
| Feature Adoption | Users using feature / Active users | % using key features | >30% |

#### Defining Your "Aha Moment"

**Process:**
1. Identify retained vs churned users
2. Analyze actions they took in first week
3. Find patterns that correlate with retention
4. Test hypothesis: Does driving users to this action increase retention?

**Examples by Product Type:**

| Product | Aha Moment |
|---------|------------|
| Facebook | Add 7 friends in 10 days |
| Dropbox | Save file on one device, access on another |
| Slack | Send 2,000 team messages |
| Airbnb | Complete a booking |
| Twitter | Follow 30 accounts |
| LinkedIn | Get endorsed or make 1 connection |

**Your Product's Aha Moment Framework:**
```
[User] completes [action] within [timeframe]

Example (Project Management Tool):
"User creates first project and adds 3 tasks within 7 days"

How to find it:
1. Segment users by retention (30-day retention ≥50% = retained)
2. Cohort analysis: What did retained users do in first 7 days?
3. Statistical correlation: Which actions predict retention?
4. A/B test: Drive users to suspected Aha moment, measure impact
```

#### Tracking Activation

**PostHog Example:**
```javascript
// Initialize PostHog
posthog.init('YOUR_API_KEY', {api_host: 'https://app.posthog.com'})

// Track activation events
posthog.capture('user_signed_up', {
  method: 'google',
  timestamp: new Date()
})

posthog.capture('project_created', {
  project_name: 'First Project',
  task_count: 3
})

posthog.capture('aha_moment_reached', {
  days_since_signup: 2,
  actions_completed: ['project_created', 'tasks_added', 'team_invited']
})
```

**Funnel Analysis:**
```
Activation Funnel:

Sign Up (100%) → Create Profile (80%) → Add First Project (50%) → Add 3 Tasks (30%) → Invite Team (20%)

Drop-off points:
- 50% drop before creating project (improve onboarding)
- 20% drop between project and tasks (show task templates)
- 10% drop at team invite (explain collaboration value)

Optimization priorities:
1. Get more users to create first project (biggest drop)
2. Template library to make task creation easier
3. Contextual prompt to invite team when project has 3+ tasks
```

### Retention Metrics

**Definition:** Users continue to use your product over time.

#### Key Metrics

| Metric | Formula | What It Means | Target (varies by product) |
|--------|---------|---------------|---------------------------|
| Day 1 Retention | Users active on Day 1 / Signups | % who come back next day | 40-70% |
| Day 7 Retention | Users active on Day 7 / Signups | % active after 1 week | 20-40% |
| Day 30 Retention | Users active on Day 30 / Signups | % active after 1 month | 10-30% |
| Monthly Active Users (MAU) | Unique users in 30 days | Total active user base | Growing |
| Churn Rate | Users who left / Total users | % leaving each period | <5% monthly (SaaS) |

#### Cohort Retention Analysis

**What It Is:** Track groups of users who signed up in the same time period and see how their retention changes over time.

**Example Cohort Table:**

```
Cohort    | Month 0 | Month 1 | Month 2 | Month 3 | Month 6
----------|---------|---------|---------|---------|--------
Jan 2026  | 100%    | 45%     | 38%     | 35%     | 30%
Feb 2026  | 100%    | 50%     | 42%     | 38%     | -
Mar 2026  | 100%    | 55%     | 48%     | -       | -

Insights:
- Retention improving over time (newer cohorts retain better)
- Curve flattens around Month 3 (30-38% become "retained")
- Product improvements (Feb launch) increased retention
```

**Retention Curve Types:**

```
Ideal (Flattening):
100% ┐
     │╲___________
 40% │
     │
  0% └──────────────→
     0  1  3  6 months
(Users find long-term value)

Bad (Declining):
100% ┐
     │╲
 40% │ ╲
     │  ╲________
  0% └──────────────→
     0  1  3  6 months
(No sticky value, eventual 0%)

Great (Smiling):
100% ┐
     │╲   ╱
 40% │ ╲ ╱
     │  ╲╱
  0% └──────────────→
     0  1  3  6 months
(Network effects kick in)
```

#### Churn Analysis

**Types of Churn:**

**1. Voluntary Churn:**
- User actively cancels subscription
- User stops using product
- User deletes account

**2. Involuntary Churn:**
- Payment failure
- Expired credit card
- Insufficient funds

**Churn Rate Calculations:**

```
Monthly Churn Rate = (Customers lost this month / Customers at start of month) × 100

Example:
Start of month: 1,000 customers
Lost: 50 customers
Churn rate: (50 / 1,000) × 100 = 5%

Revenue Churn = (MRR lost / MRR at start of month) × 100

Example:
Start MRR: $50,000
Lost MRR: $2,000
New MRR from expansions: $3,000
Net Revenue Churn: ($2,000 - $3,000) / $50,000 = -2% (negative churn = good!)
```

**Churn Cohort Analysis:**

```
Why did users churn?

Reason                  | % of Churned Users | Action
------------------------|-------------------|------------------
Didn't see value        | 35%               | Improve onboarding
Too expensive           | 25%               | Review pricing, add cheaper tier
Missing features        | 20%               | Prioritize feature requests
Found alternative       | 10%               | Competitive analysis
Technical issues        | 5%                | Improve reliability
Other                   | 5%                | Survey for insights
```

**Preventing Churn:**

```
Early Warning Signals:

High Risk (50%+ chance of churn):
- No login for 14+ days
- No usage of core feature in 30 days
- Support tickets unresolved for 7+ days
- Downgraded from paid to free
- Multiple failed payments

Medium Risk (20-50% chance):
- Login frequency decreasing (weekly → monthly)
- Single feature user (not experiencing full value)
- No team members invited (solo user in team product)

Intervention Tactics:
1. Automated email: "We noticed you haven't logged in..."
2. In-app message: "Need help getting started?"
3. Personal outreach from founder/CSM for high-value accounts
4. Offer training/onboarding session
5. Feature education: "Have you tried [feature]?"
6. Win-back discount: "Come back for 20% off 3 months"
```

### Revenue Metrics

**Definition:** How you make money from users.

#### Key Metrics

| Metric | Formula | What It Means | Target |
|--------|---------|---------------|--------|
| Monthly Recurring Revenue (MRR) | Sum of all monthly subscriptions | Predictable monthly income | Growing 10-20% MoM |
| Annual Recurring Revenue (ARR) | MRR × 12 | Annualized revenue | $1M+ for Series A |
| Average Revenue Per User (ARPU) | Total revenue / Total users | Revenue per user | Increasing over time |
| Customer Lifetime Value (LTV) | ARPU × (1 / Churn rate) | Total revenue from a customer | 3-5x CAC |
| LTV:CAC Ratio | LTV / CAC | Return on acquisition investment | >3:1 |

#### MRR Breakdown

**Components of MRR:**

```
MRR Movement:

Starting MRR (Month 1):        $10,000

New MRR (new customers):       + $2,000
Expansion MRR (upgrades):      + $500
Reactivation MRR (win-backs):  + $200
------------------------------------------
Gross New MRR:                 + $2,700

Churned MRR (cancellations):   - $800
Contraction MRR (downgrades):  - $200
------------------------------------------
Gross Churn MRR:               - $1,000

Net New MRR:                   + $1,700

Ending MRR (Month 2):          $11,700

Growth Rate:                   17%
```

**MRR Goals by Stage:**

| Stage | MRR | Growth Rate | Focus |
|-------|-----|-------------|-------|
| Pre-seed | $1K-10K | 20%+ MoM | Find PMF, high growth |
| Seed | $10K-50K | 15-20% MoM | Repeatable acquisition |
| Series A | $100K+ | 10-15% MoM | Scale revenue |
| Series B | $1M+ | 5-10% MoM | Profitability + growth |

#### Customer Lifetime Value (LTV)

**Simple LTV Calculation:**
```
LTV = ARPU / Churn Rate

Example:
ARPU = $50/month
Monthly churn = 5% (0.05)
LTV = $50 / 0.05 = $1,000

Meaning: Average customer pays $1,000 over their lifetime
```

**Detailed LTV Calculation:**
```
LTV = (ARPU × Gross Margin) / Churn Rate

Example:
ARPU = $50/month
Gross margin = 80% (costs to serve customer)
Monthly churn = 5%
LTV = ($50 × 0.80) / 0.05 = $800
```

**LTV by Cohort:**
```
Month   | Cohort Jan | Cohort Feb | Cohort Mar
--------|------------|------------|------------
0       | $50        | $50        | $50
1       | $40        | $45        | $48
2       | $35        | $40        | $45
3       | $30        | $38        | -
6       | $25        | -          | -
12      | $20        | -          | -

Total   | $200       | $173       | $143

Observation: Feb cohort retaining better than Jan (product improvements)
```

#### Pricing Tier Performance

```
Tier Performance Analysis:

Plan        | Price  | Customers | MRR      | % of Revenue | Churn
------------|--------|-----------|----------|--------------|-------
Free        | $0     | 5,000     | $0       | 0%           | 15%
Starter     | $29    | 800       | $23,200  | 35%          | 8%
Professional| $99    | 300       | $29,700  | 45%          | 4%
Enterprise  | $399   | 50        | $19,950  | 20%          | 2%

Total       |        | 6,150     | $72,850  | 100%         | 6% avg

Insights:
- Professional tier is sweet spot (45% of revenue, good retention)
- Free users rarely convert (consider gating more features)
- Enterprise has best retention (focus on upsells)
- Starter tier high churn (improve onboarding or value)
```

### Referral Metrics

**Definition:** Users tell others about your product, driving organic growth.

#### Key Metrics

| Metric | Formula | What It Means | Target |
|--------|---------|---------------|--------|
| Viral Coefficient (K) | Invites per user × Conversion rate | Each user brings K new users | >1.0 for viral growth |
| Referral Rate | Users who referred / Total users | % of users who share | 10-30% |
| Invitation Conversion | Signups from invites / Total invites sent | % of invites that convert | 20-40% |
| Cycle Time | Time from user joining to inviting others | Speed of viral loop | <7 days |

#### Viral Coefficient Deep Dive

**Formula:**
```
K = (Number of invites per user) × (Conversion rate of invites)

Example 1: Viral Growth (K > 1.0)
- Average user sends 5 invites
- 25% of invites sign up
- K = 5 × 0.25 = 1.25

Meaning: Each user brings 1.25 new users → exponential growth

Example 2: Sub-Viral (K < 1.0)
- Average user sends 3 invites
- 15% of invites sign up
- K = 3 × 0.15 = 0.45

Meaning: Each user brings 0.45 new users → growth requires other channels

Example 3: Optimizing K
Current: K = 0.45 (3 invites × 15% conversion)

Increase invites to 5:
K = 5 × 0.15 = 0.75 (improvement, still sub-viral)

Improve conversion to 25%:
K = 5 × 0.25 = 1.25 (viral!)
```

**Viral Cycle Time Impact:**

```
Scenario A: K = 1.2, Cycle time = 30 days
Month 1: 100 users
Month 2: 120 users (+20)
Month 3: 144 users (+24)
Month 6: 299 users

Scenario B: K = 1.2, Cycle time = 7 days
Week 1: 100 users
Week 2: 120 users
Week 4: 144 users
Month 2: 619 users
Month 6: 23,298 users

Same K, faster cycle time = exponential difference
```

#### Referral Program Design

**Incentive Structures:**

```
Type 1: Double-sided Incentive (Best for growth)
Referrer gets: $10 credit
Referee gets: $10 credit
Example: Dropbox (500MB for both), Uber ($10 for both)

Type 2: Referrer Only
Referrer gets: $20 credit or 1 month free
Referee gets: Nothing
Works when: Product value is obvious

Type 3: Referee Only
Referrer gets: Nothing (altruism)
Referee gets: Discount or trial extension
Works when: Users are evangelists

Type 4: Tiered Rewards
1-5 referrals: $10 each
6-20 referrals: $15 each
20+ referrals: $25 each + Ambassador status
Example: Affiliate programs

Recommended: Double-sided with generous incentive
```

**Built-in Virality (Best Approach):**

```
Product features that naturally invite others:

Collaboration:
- Google Docs: Invite to edit document
- Figma: Share design for feedback
- Slack: Invite team to channel

Content Sharing:
- Loom: Share video link
- Canva: Share design
- Notion: Share page publicly

Network Effects:
- LinkedIn: Value increases with connections
- Marketplace: Buyers bring sellers, vice versa

Implementation:
1. Make sharing core to product value
2. Recipient sees preview/value before signing up
3. Easy signup process (1-click with invite)
4. Immediate value upon joining
```

---

## 2. North Star Metric

### What It Is

The single metric that best captures the core value you deliver to customers. It's the metric you'd choose if you could only track one thing.

### Characteristics of a Good North Star

```
✓ Measures customer value (not vanity)
✓ Leading indicator of revenue
✓ Actionable by the team
✓ Captures product vision
✓ Understandable by everyone
```

### Examples by Product Type

| Product | North Star Metric | Why |
|---------|-------------------|-----|
| Airbnb | Nights Booked | Captures value for hosts & guests |
| Netflix | Hours Watched | Engagement drives retention |
| Slack | Messages Sent | Communication value |
| Facebook | Daily Active Users | Network effect value |
| Medium | Total Time Reading | Content engagement |
| Uber | Rides per Week | Core product usage |
| Spotify | Time Listening | Music streaming value |

### Finding Your North Star

**Framework:**

```
Step 1: What is the core value you provide?
Example (Project Management): "Help teams collaborate on work"

Step 2: How do users experience that value?
- Creating projects
- Assigning tasks
- Completing tasks
- Team communication

Step 3: Which metric best captures that value?
Option A: Projects Created (too early in funnel)
Option B: Tasks Completed (captures actual progress)
Option C: Active Team Members (captures collaboration)

Step 4: Test correlation with revenue
Analyze: Does increase in [metric] predict revenue growth?

Chosen North Star: "Tasks Completed per Team per Week"
- Measures actual value delivery
- Teams completing more tasks = getting value
- Leads to retention and expansion
```

### North Star Dashboard

```
Weekly North Star Review:

Current Week: 15,000 tasks completed
Last Week: 14,200 tasks completed
Growth: +5.6%

Breakdown:
- New teams: 2,000 tasks (13%)
- Existing teams: 13,000 tasks (87%)

By Plan:
- Free: 3,000 tasks
- Starter: 5,000 tasks
- Pro: 6,000 tasks
- Enterprise: 1,000 tasks

Leading Indicators:
- New signups: +12% (future task growth)
- Team invites sent: +8% (collaboration increasing)

Lagging Indicators:
- Retention rate: 65% (stable)
- Revenue: +10% MoM (tracking North Star)
```

---

## 3. Funnel Analysis

### Conversion Funnel Framework

**Definition:** Map the steps users take from awareness to becoming a customer, and measure drop-off at each step.

### Example Funnel: SaaS Product

```
Landing Page → Signup → Email Verification → Onboarding → First Value → Paid Customer

Step 1: Landing Page Visit
- 10,000 visitors/month

Step 2: Signup Started (40%)
- 4,000 started signup
- Drop-off: 6,000 (60%) - Why?
  * Too much friction (too many form fields?)
  * Value prop unclear
  * Trust issues

Step 3: Signup Completed (70% of started)
- 2,800 completed signup
- Drop-off: 1,200 (30%)
  * Email verification not received
  * Gave up during process
  * Privacy concerns

Step 4: Email Verified (85%)
- 2,380 verified email
- Drop-off: 420 (15%)
  * Email in spam
  * Lost interest
  * Verification link expired

Step 5: Onboarding Completed (60%)
- 1,428 finished onboarding
- Drop-off: 952 (40%)
  * Too long/complex
  * Unclear value
  * Distractions

Step 6: Reached "Aha Moment" (50%)
- 714 experienced core value
- Drop-off: 714 (50%)
  * Didn't understand product
  * Couldn't figure out how to use
  * No immediate need

Step 7: Converted to Paid (15% of "Aha")
- 107 became paying customers
- Overall conversion: 1.07%

Total Funnel Conversion: 10,000 visitors → 107 customers = 1.07%
```

### Optimization Priorities

```
Impact = (Current drop-off %) × (Users at that stage) × (Estimated improvement)

Stage 1: Landing → Signup
- Drop-off: 60% (6,000 users)
- Potential improvement: +10% conversion
- Impact: 600 additional signups

Stage 2: Onboarding → Aha
- Drop-off: 50% (1,428 users)
- Potential improvement: +20% conversion
- Impact: 286 additional "Aha" moments

Stage 3: Aha → Paid
- Drop-off: 85% (714 users)
- Potential improvement: +5% conversion
- Impact: 36 additional customers

Prioritize: Stage 2 (onboarding) has highest impact on customers (286 × 15% = 43 customers vs 36 from Stage 3)
```

### A/B Testing Funnels

```
Test: Simplify Signup Form

Control (Old):
- 10 form fields
- Signup conversion: 30%

Variant (New):
- 3 form fields (email, password, name)
- Signup conversion: 45%

Results:
- Improvement: +50% relative, +15% absolute
- Impact: 10,000 visitors × 15% = 1,500 additional signups/month

Projected customers:
1,500 additional signups × 7.6% (signup to customer) = 114 additional customers/month

ROI: Massive (one-time development cost, ongoing revenue increase)
```

---

## 4. A/B Testing Framework

### When to A/B Test

```
✓ Good candidates for testing:
- Signup/onboarding flow
- Pricing page
- Landing page headlines
- CTA button copy/color
- Email subject lines

✗ Don't test (yet):
- Low traffic (<1,000 users/week)
- Core product features (qualitative feedback first)
- Long conversion cycles (test will take months)
```

### Statistical Significance

**Required Sample Size:**

```
Use online calculators (e.g., Optimizely, Evan Miller)

Example:
Current conversion: 2%
Desired improvement: 20% relative (2% → 2.4%)
Confidence level: 95%
Power: 80%

Required sample size: ~19,000 per variant = 38,000 total

Timeline:
If you get 1,000 visitors/week: 38 weeks (too long)
If you get 10,000 visitors/week: 4 weeks (acceptable)
```

**Statistical Significance Calculator:**
```
Variant A: 1,000 visitors, 20 conversions (2%)
Variant B: 1,000 visitors, 30 conversions (3%)

Is 3% significantly better than 2%?

p-value: 0.09 (9%)
Result: NOT statistically significant at 95% confidence (need p < 0.05)

Continue test until p < 0.05 or reach sample size limit
```

### Test Design

```
Hypothesis: "Changing CTA from 'Sign Up' to 'Start Free Trial' will increase conversions because it reduces commitment fear"

Control: "Sign Up" button
Variant: "Start Free Trial" button

Metrics:
- Primary: Signup conversion rate
- Secondary: Email verification rate, activation rate
- Guardrail: Bounce rate (ensure not hurting other metrics)

Test Duration: 2 weeks (or until statistical significance)

Success Criteria:
- Variant achieves >5% absolute improvement
- p-value < 0.05
- No negative impact on guardrail metrics

Result:
Control: 2.0% conversion (1,000/50,000)
Variant: 2.5% conversion (1,300/52,000)
Improvement: +25% relative
p-value: 0.002 (statistically significant)

Decision: Ship variant, expect 250 additional signups/month
```

---

## 5. Cohort Analysis

### What It Is

Group users by a common characteristic (usually signup date) and track their behavior over time.

### Types of Cohorts

**Time-based Cohorts:**
```
- Daily: Users who signed up on same day
- Weekly: Users who signed up in same week
- Monthly: Users who signed up in same month
```

**Behavior-based Cohorts:**
```
- Acquisition channel: SEO, Paid, Referral
- Product tier: Free, Starter, Pro
- User segment: Small business, Enterprise
- Feature usage: Power users, casual users
```

### Retention Cohort Example

```
Monthly Cohort Retention Table:

          | M0    | M1  | M2  | M3  | M6  | M12
----------|-------|-----|-----|-----|-----|-----
Jan 2025  | 100%  | 45% | 35% | 30% | 25% | 20%
Feb 2025  | 100%  | 50% | 40% | 35% | 28% | -
Mar 2025  | 100%  | 55% | 45% | 38% | -   | -
Apr 2025  | 100%  | 60% | 48% | -   | -   | -
May 2025  | 100%  | 62% | -   | -   | -   | -

Insights:
1. Retention improving over time (product getting better)
2. Curve flattens around M3 (~30-38% become long-term users)
3. Recent cohorts retaining better (Apr/May 60%+ at M1)
4. Product changes in March working (retention jump)
```

### Revenue Cohort Analysis

```
Revenue Generated by Cohort:

Cohort    | M0      | M1      | M2      | M3      | M6      | Cumulative
----------|---------|---------|---------|---------|---------|------------
Jan 2025  | $5,000  | $4,000  | $3,500  | $3,200  | $2,800  | $18,500
Feb 2025  | $6,000  | $5,200  | $4,800  | $4,500  | -       | $20,500
Mar 2025  | $7,000  | $6,500  | $6,000  | -       | -       | $19,500

Analysis:
- Feb cohort more valuable than Jan (better targeting or pricing)
- Revenue churn slowing (good retention)
- LTV increasing with each cohort
```

---

## 6. Dashboard Design

### Key Principles

```
1. Hierarchy: Most important metrics at top
2. Context: Show comparison (vs last week, vs goal)
3. Trends: Show direction (up/down, % change)
4. Drill-down: Allow exploring details
5. Real-time: Update frequently (hourly/daily)
6. Accessible: Visible to whole team
```

### Startup Dashboard Template

```
┌─────────────────────────────────────────────────────┐
│ NORTH STAR METRIC                                   │
│ Tasks Completed This Week: 15,234 ↑ 12%            │
└─────────────────────────────────────────────────────┘

┌─────────────── ACQUISITION ──────────────────┐
│ Traffic:           45,230  ↑ 8%              │
│ Signups:           1,234   ↑ 15%             │
│ CAC:               $24     ↓ 5%              │
└───────────────────────────────────────────────┘

┌─────────────── ACTIVATION ───────────────────┐
│ Activation Rate:   42%     ↑ 3%              │
│ Time to Value:     2.3 days ↓ 0.5 days       │
│ Onboarding %:      68%     ↑ 5%              │
└───────────────────────────────────────────────┘

┌─────────────── RETENTION ────────────────────┐
│ MAU:               12,450  ↑ 10%             │
│ Day 30 Retention:  35%     → (flat)          │
│ Churn Rate:        4.2%    ↓ 0.3%            │
└───────────────────────────────────────────────┘

┌─────────────── REVENUE ──────────────────────┐
│ MRR:               $72,850 ↑ 17%             │
│ ARPU:              $58     ↑ 2%              │
│ LTV:CAC:           3.2     ↑ 0.1             │
└───────────────────────────────────────────────┘

┌─────────────── REFERRAL ─────────────────────┐
│ Viral Coeff (K):   0.65    ↑ 0.05            │
│ Referral Rate:     18%     ↑ 2%              │
│ Invite Conv:       28%     → (flat)          │
└───────────────────────────────────────────────┘
```

### Tools for Dashboards

| Tool | Best For | Price | Complexity |
|------|----------|-------|------------|
| Google Sheets | MVP, simple tracking | Free | Low |
| Metabase | Self-serve analytics | Free (self-hosted) | Medium |
| Mixpanel | Product analytics | $28/mo+ | Medium |
| Amplitude | Advanced analytics | Free (10M events) | High |
| PostHog | Open-source product analytics | $0-450/mo | Medium |
| Tableau | Enterprise, complex viz | $70+/user/mo | High |

**Recommended for Startups:** PostHog or Mixpanel (balance of power and ease)

---

## 7. NPS (Net Promoter Score)

### What It Is

Single-question survey that measures customer satisfaction and likelihood to refer.

**The Question:**
"How likely are you to recommend [Product] to a friend or colleague?"
(0-10 scale)

### Scoring

```
Promoters (9-10):
- Love your product
- Will recommend it
- Drive referrals

Passives (7-8):
- Satisfied but not enthusiastic
- Vulnerable to competitors
- Won't actively refer

Detractors (0-6):
- Unhappy customers
- May spread negative word-of-mouth
- High churn risk
```

### NPS Calculation

```
NPS = % Promoters - % Detractors

Example:
Survey responses: 100 people
Promoters (9-10): 60 people
Passives (7-8): 25 people
Detractors (0-6): 15 people

NPS = 60% - 15% = 45

Interpretation:
- >70: Excellent (world-class)
- 50-70: Great
- 30-50: Good
- 0-30: Needs improvement
- <0: Major problems
```

### NPS Survey Implementation

**When to Send:**
```
Best timing:
- After user experiences core value (post "Aha moment")
- After significant milestone (30 days active, completed project)
- NOT immediately after signup (no value yet)

Frequency:
- Quarterly for active users
- Post-interaction (after support ticket resolved)
- Avoid survey fatigue (max 1-2x per year per user)
```

**Follow-up Questions:**
```
For Promoters (9-10):
"What do you love most about [Product]?"
→ Use for marketing, case studies, testimonials

For Passives (7-8):
"What would make [Product] a 10 for you?"
→ Feature requests, product roadmap

For Detractors (0-6):
"What disappointed you about [Product]?"
→ Critical feedback, churn prevention
```

### Acting on NPS Data

```
Promoters (9-10):
✓ Ask for testimonial or review
✓ Invite to referral program
✓ Feature as case study
✓ Invite to beta programs

Passives (7-8):
✓ Understand missing features
✓ Engage with content/education
✓ Check in quarterly

Detractors (0-6):
✓ Personal outreach from founder/CSM
✓ Understand root cause
✓ Offer to help resolve issue
✓ Win-back campaign if churned

Aggregate Analysis:
- Track NPS trend over time
- Segment by plan, cohort, channel
- Correlate with churn and LTV
- Set OKRs to improve NPS
```

---

## Summary: Metrics to Track by Stage

### Pre-Product (Idea Stage)
```
□ Customer interviews completed: 20-30
□ Problem validation: 60%+ say it's a major pain
□ Willingness to pay: 40%+ would pay
```

### MVP (Validation Stage)
```
□ Signups: 100-500
□ Activation rate: 30%+
□ Retention (Day 7): 20%+
□ Qualitative feedback: 10+ user interviews
```

### Product-Market Fit (Growth Stage)
```
□ Sean Ellis score: 40%+ "very disappointed"
□ Retention (Day 30): 40%+
□ NPS: 30+
□ Organic growth: 30%+ from referrals
□ MRR: $10K+, growing 15-20% MoM
```

### Scale Stage
```
□ MRR: $100K+
□ LTV:CAC: >3:1
□ CAC payback: <12 months
□ Churn: <5% monthly
□ NPS: 50+
```

**Remember:** Don't track everything. Focus on 5-7 key metrics that drive your business. Over-measurement leads to analysis paralysis.

Track what matters, act on insights, and iterate quickly.
