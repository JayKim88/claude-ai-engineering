# Pricing Strategies Knowledge Base

## Overview

Pricing is one of the most critical decisions for any business. This guide covers proven pricing frameworks, methodologies, and strategies to help you price your product optimally.

---

## Core Pricing Frameworks

### 1. Value-Based Pricing

#### Definition
Set prices based on the perceived value to the customer, not your costs. Price captures the value you create.

#### When to Use
- Unique product with clear differentiation
- Measurable ROI for customers
- Strong brand or market position
- B2B products with quantifiable savings

#### Methodology

**Step 1: Identify Customer Segments**
```
Segment A: Small businesses (1-10 employees)
- Pain: Manual data entry takes 10 hours/week
- Value: Time saved = $200/week

Segment B: Mid-market (50-200 employees)
- Pain: Coordination issues across teams
- Value: Efficiency gain = $2,000/week
```

**Step 2: Quantify Economic Value**
```
Economic Value Formula:
Total Customer Value = Reference Value + Differentiation Value

Example (Project Management Tool):
Reference Value: $50/user/month (competitors)
Differentiation Value:
- Time saved: 5 hours/month × $50/hour = $250
- Error reduction: $100/month in prevented mistakes
Total Value: $400/month per user

Price Capture: Set price at 30-50% of total value = $120-200/month
```

**Step 3: Willingness-to-Pay Analysis**

| Method | How It Works | When to Use |
|--------|--------------|-------------|
| Van Westendorp | Ask 4 price questions (too cheap, bargain, expensive, too expensive) | Pre-launch, survey-based |
| Conjoint Analysis | Test feature bundles at different prices | Complex products, multiple features |
| A/B Testing | Test different prices with real customers | Live product, sufficient traffic |
| Customer Interviews | Direct conversations about budget | B2B, enterprise sales |

**Van Westendorp Survey Questions:**
1. At what price would this product be too expensive? (never buy)
2. At what price would this product be expensive? (think twice)
3. At what price would this product be a bargain? (great deal)
4. At what price would this product be too cheap? (question quality)

#### Pricing Examples

**B2B SaaS Example:**
```
Customer saves $10,000/month using your tool
Industry standard: capture 20-30% of value created
Your price: $2,000-3,000/month

Justification in sales pitch:
"Our tool saves you $10,000/month. For just $2,500/month,
you net $7,500 in savings. That's a 300% ROI."
```

**Consumer Product Example:**
```
Premium coffee subscription:
Reference: Starbucks coffee = $5/cup × 20 cups/month = $100
Your value: Specialty beans + convenience + sustainability
Differentiation value: $30/month
Price: $79/month (60% of reference + differentiation value)
```

#### Pros
- Maximizes revenue and profit
- Aligns price with customer success
- Defensible against cost-based competition
- Allows premium positioning

#### Cons
- Requires deep customer understanding
- Difficult to quantify some value
- May leave money on table if too conservative
- Needs continuous validation

#### Key Metrics
- **Value-to-Price Ratio**: Customer value / price (target: 3:1 to 10:1)
- **Price Sensitivity**: % change in demand per % change in price
- **Willingness to Pay Distribution**: Price range analysis
- **Feature Value Attribution**: Which features drive price

---

### 2. Competition-Based Pricing

#### Definition
Set prices relative to competitors. Position as premium, at-market, or value option.

#### Competitive Positioning Matrix

```
                Premium (1.5-3x)
                      |
                      |
    Value ----------------------------- At-Market
   (0.5-0.8x)         |                   (0.9-1.1x)
                      |
                 Penetration
                 (0.3-0.6x)
```

#### Positioning Strategies

**Premium Pricing (Above Market)**
- Price: 1.5-3x competitor average
- Justification: Superior quality, brand, service
- Examples: Apple, Salesforce
- Risk: Must deliver exceptional value

**At-Market Pricing (Match Competitors)**
- Price: ±10% of market average
- Justification: Similar features, compete on brand/service
- Examples: Most SaaS tools
- Risk: Commoditization, price wars

**Value Pricing (Below Premium, Above Budget)**
- Price: 70-90% of market leader
- Justification: Good quality, better price
- Examples: Notion vs. Confluence
- Risk: Perceived as "budget" option

**Penetration Pricing (Significantly Below Market)**
- Price: 30-60% of competitors
- Justification: Gain market share, disrupt
- Examples: Zoom (initially), Robinhood
- Risk: Unsustainable, race to bottom

#### Competitive Analysis Framework

**Step 1: Map Competitor Pricing**
| Competitor | Plan | Price/User/Month | Features | Target Segment |
|------------|------|------------------|----------|----------------|
| Leader A | Pro | $25 | Full suite | Enterprise |
| Leader B | Plus | $20 | Most features | Mid-market |
| Challenger C | Growth | $15 | Core features | Small business |
| Budget D | Basic | $8 | Limited | Individuals |

**Step 2: Feature Comparison**
```
Feature Parity Analysis:
Your Product vs Competitor A:
- Core features: 100% match
- Advanced features: 80% match
- Integrations: 90% match
- Support: 100% match

Justified Price Range: $20-25/user/month (80-100% of Leader A)
```

**Step 3: Choose Your Position**
```
Decision Factors:
- Brand strength: Weak → Price lower
- Feature completeness: 80% → Price at 80-90% of leader
- Market share goal: High → Price lower initially
- Margin requirements: High → Price higher

Position Selected: Value (85% of leader) = $21/user/month
```

#### Pricing Examples

**Direct Competitor Matching:**
```
Market Research Results:
- Competitor A: $99/month (market leader, 40% share)
- Competitor B: $79/month (challenger, 30% share)
- Competitor C: $49/month (budget option, 15% share)

Your Strategy: Position between A and B
Price: $89/month
Messaging: "90% of the features at 90% of the price"
```

**Feature-Differentiated Pricing:**
```
If you have unique features:
- Base features: Match competitor ($50/month)
- Your unique features: Add 30-50% premium
- Final price: $65-75/month

Messaging: "Everything Competitor X has, plus [unique feature]"
```

#### Pros
- Quick to implement (just research competitors)
- Reduces pricing risk
- Easier to justify to customers
- Market validation built-in

#### Cons
- Ignores your unique value proposition
- Can lead to commoditization
- Doesn't account for cost structure differences
- May not maximize revenue

#### Key Metrics
- **Price Position Index**: Your price / average competitor price
- **Feature Parity Score**: % of leader's features you have
- **Win Rate vs Competitors**: Competitive deal win %
- **Price as Objection Rate**: How often price blocks sales

---

### 3. Cost-Plus Pricing

#### Definition
Calculate your costs and add a markup percentage to ensure profitability.

#### Cost Components

**Direct Costs (Variable):**
- Product/inventory costs
- Transaction fees (Stripe, etc.)
- Shipping/delivery
- Direct labor
- Customer-specific costs

**Indirect Costs (Fixed):**
- Salaries (product, engineering, support)
- Infrastructure (servers, tools, software)
- Marketing and sales
- Office/overhead
- Legal and accounting

#### Markup Calculation

**Standard Markup Formula:**
```
Selling Price = Cost / (1 - Desired Margin %)

Example:
Cost per unit: $30
Desired gross margin: 40%
Selling Price = $30 / (1 - 0.40) = $30 / 0.60 = $50

Verification:
Revenue: $50
Cost: $30
Profit: $20
Margin: $20 / $50 = 40% ✓
```

**Industry-Standard Margins:**

| Industry | Typical Gross Margin | Markup Formula |
|----------|---------------------|----------------|
| SaaS | 70-90% | Cost / 0.1-0.3 |
| E-commerce | 30-50% | Cost / 0.5-0.7 |
| Physical Products | 40-60% | Cost / 0.4-0.6 |
| Services | 40-70% | Cost / 0.3-0.6 |
| Marketplaces | 60-80% (net) | Variable |
| Digital Products | 90-95% | Cost / 0.05-0.1 |

#### Full Cost Analysis Example

**SaaS Product (100 customers):**
```
Monthly Costs:
Infrastructure: $500
- Hosting: $200
- Tools (Stripe, analytics): $300

Salaries (allocated): $15,000
- Engineering (50%): $10,000
- Support (25%): $2,500
- Sales/Marketing (25%): $2,500

Overhead: $1,000
- Legal, accounting: $500
- Office, misc: $500

Total Monthly Cost: $16,500
Cost per Customer: $16,500 / 100 = $165

Target Gross Margin: 70%
Required Price: $165 / 0.30 = $550 per customer/month

Sanity Check:
Revenue (100 × $550): $55,000
Costs: $16,500
Gross Profit: $38,500
Margin: 70% ✓
```

**E-commerce Product:**
```
Per-Unit Costs:
Product cost (COGS): $20
Shipping: $5
Transaction fees (3%): Will calculate after
Packaging: $2

Subtotal Variable Costs: $27

Desired Margin: 50%
Initial Price Estimate: $27 / 0.50 = $54

Add Transaction Fees (3%): $54 / 0.97 = $55.67
Round to: $59

Final Check:
Selling Price: $59
Transaction Fee (3%): $1.77
Net Revenue: $57.23
COGS: $27
Gross Profit: $30.23
Margin: 52.8% ✓
```

#### Tiered Markup Strategy

**Volume-Based Markup:**
```
Low Volume (1-10 units): 100% markup (2x cost)
- Higher handling costs, lower efficiency
- Price: Cost × 2

Medium Volume (11-100 units): 60% markup (1.6x cost)
- Standard operations
- Price: Cost × 1.6

High Volume (100+ units): 40% markup (1.4x cost)
- Economies of scale
- Price: Cost × 1.4
```

#### Pros
- Guarantees profitability
- Simple to calculate and explain
- Ensures all costs are covered
- Easy to adjust as costs change

#### Cons
- Ignores customer willingness to pay
- May price too high or too low
- Doesn't account for competitive dynamics
- Can miss revenue opportunities

#### Key Metrics
- **Gross Margin**: (Revenue - COGS) / Revenue
- **Contribution Margin**: (Revenue - Variable Costs) / Revenue
- **Break-Even Volume**: Fixed Costs / (Price - Variable Cost)
- **Target Margin Achievement**: Actual vs target margin %

---

### 4. Penetration Pricing

#### Definition
Set artificially low prices initially to gain market share quickly, then raise prices once established.

#### When to Use
- Entering crowded, competitive market
- Strong network effects (need critical mass)
- Can achieve economies of scale quickly
- Have funding to sustain losses
- Goal is market dominance, not immediate profit

#### Strategy Framework

**Phase 1: Entry (Months 1-6)**
```
Pricing: 40-60% below market rate
Goal: Acquire 1,000+ customers
Example: Market rate $100/mo → You charge $50/mo
Expected Margin: Negative (acceptable short-term)
```

**Phase 2: Growth (Months 7-18)**
```
Pricing: 70-80% of market rate
Goal: Reach 5,000+ customers, achieve product-market fit
Example: Raise to $75/mo
Communicate: "Early adopter pricing ending, locking in current customers"
Expected Margin: Break-even to slightly positive
```

**Phase 3: Maturity (Months 19+)**
```
Pricing: Match or exceed market rate
Goal: Optimize for profitability
Example: Raise to $100-120/mo
Grandfathering: Keep early customers at $75 or give 20% lifetime discount
Expected Margin: Target margins achieved
```

#### Pricing Examples

**SaaS Market Entry:**
```
Market Leader: $50/user/month
Your Penetration Price: $20/user/month (60% discount)

Year 1 Plan:
- Acquire 500 customers @ $20 = $10,000 MRR
- Monthly costs: $15,000
- Monthly loss: $5,000 (funded by investment)

Year 2 Plan:
- Raise to $35/user/month for new customers
- Grandfather existing at $25/user/month
- Grow to 1,500 customers (mix of $25 and $35)
- MRR: ~$45,000
- Monthly costs: $30,000
- Monthly profit: $15,000
```

**Marketplace Launch:**
```
Standard marketplace take rate: 15-20%
Your penetration rate: 0% for first 6 months

Rationale: Need liquidity on both sides
- Attract sellers with free listing
- Attract buyers with inventory
- GMV growth > revenue in early days

Month 7+: Introduce 5% take rate
Month 13+: Increase to 10% take rate
Month 19+: Match market at 15-20% take rate
```

#### Customer Communication

**Price Lock Guarantee:**
```
"Lock in $29/month for life as an early adopter.
After [date], new customers pay $49/month."

Creates urgency and rewards early customers.
```

**Grandfather Clause:**
```
Email to existing customers:
"Thanks for being an early supporter. While we're raising
prices to $99/month for new customers, you'll stay at
$49/month as long as you remain a customer."
```

**Transparent Price Increases:**
```
"We're growing! To continue improving the product and
providing great support, we're adjusting pricing:

- Current customers: $49 → $69 (in 60 days)
- New customers: $99 (starting today)

You can lock in $49 for another 12 months by switching
to annual billing before [date]."
```

#### Risks and Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| Burn rate too high | Set max customer acquisition before raising prices |
| Cheap price anchoring | Communicate it's "early adopter" pricing from day 1 |
| Customer churn on increase | Grandfather early customers or give loyalty discounts |
| Competitors match low price | Differentiate on features, not just price |
| Can't raise prices later | Build in value continuously to justify increases |

#### Pros
- Rapid customer acquisition
- Builds market share quickly
- Tests product-market fit fast
- Creates network effects
- Disrupts incumbents

#### Cons
- Requires funding to sustain losses
- Risk of being stuck at low price
- Attracts price-sensitive customers
- May damage brand (perceived as cheap)
- Competitors may match

#### Key Metrics
- **Customer Acquisition Rate**: New customers per month
- **Market Share Growth**: % of market captured
- **Burn Rate**: Monthly cash consumed
- **Conversion on Price Increase**: % of customers who stay
- **Time to Profitability**: Months until positive margin

---

### 5. Skimming Pricing

#### Definition
Launch at premium price to maximize profit from early adopters, then gradually lower price to reach broader market.

#### When to Use
- First-to-market with innovative product
- Strong brand or reputation
- Limited competition initially
- High R&D costs to recoup
- Inelastic demand from early adopters

#### Price Descent Strategy

**Phase 1: Launch (Premium Tier)**
```
Price: 2-3x eventual target price
Target: Innovators and early adopters (2.5% of market)
Duration: 6-12 months
Goal: Maximize margin, recoup development costs

Example: New productivity tool
Launch price: $299/month
Positioning: "Premium tool for cutting-edge teams"
```

**Phase 2: Expansion (Standard Tier)**
```
Price: 1.5-2x eventual target price
Target: Early majority (13.5% of market)
Duration: 12-24 months
Goal: Maintain healthy margins while growing

Price: $199/month
Positioning: "Industry-leading solution"
Keep $299 tier as "Enterprise" with added features
```

**Phase 3: Growth (Value Tier)**
```
Price: Target price (1x)
Target: Mass market (early + late majority)
Duration: Ongoing
Goal: Market penetration while maintaining profitability

Price: $99/month
Positioning: "Professional-grade tool, accessible pricing"
Maintain higher tiers with added value
```

#### Pricing Examples

**Tech Product Launch:**
```
Year 1 (Early Adopter Phase):
- Single tier: $499/month
- Target: 100 customers = $49,900 MRR
- Focus: Premium features, white-glove support

Year 2 (Expansion Phase):
- Premium: $499/month (add features to maintain value)
- Professional: $299/month (original feature set)
- Target: 500 customers (mix) = ~$180,000 MRR

Year 3 (Mass Market Phase):
- Enterprise: $699/month (new premium tier)
- Professional: $299/month
- Standard: $149/month (new entry tier)
- Target: 2,000 customers = ~$400,000 MRR
```

**Physical Product (Tech Hardware):**
```
Launch:
- Price: $999 (limited quantity)
- Market: Tech enthusiasts, early adopters

6 Months:
- Price: $799 (increased production volume)
- Market: Mainstream tech users

12 Months:
- Price: $599 (economies of scale)
- Market: Mass market
- Introduce "Pro" version at $999 for new early adopters
```

#### Tier Evolution Strategy

**Maintain Premium Positioning:**
```
Don't just lower prices - add tiers and evolve:

Launch (Month 0):
└─ Premium: $500

Month 12:
├─ Premium: $500 (add features to justify)
└─ Standard: $300 (original feature set)

Month 24:
├─ Enterprise: $800 (new premium tier)
├─ Premium: $500 (enhanced)
└─ Standard: $300
```

#### Communication Strategy

**Early Adopter Messaging:**
```
"Be among the first to experience [product].
Limited availability at launch price of $499.

As an early customer, you'll receive:
- Priority feature requests
- Dedicated onboarding
- Price lock guarantee
- Beta access to new features"
```

**Price Reduction Announcement:**
```
"Thanks to your support, we've grown and can now offer
[product] to more teams.

New pricing:
- Professional: $299/month (new tier)
- Enterprise: $499/month (you're here)

As a thank you, you'll receive:
- [New enterprise feature]
- [Added benefit]
- Your $499 rate is locked in"
```

#### Pros
- Maximizes early revenue
- Recovers R&D costs quickly
- Creates perception of premium product
- Targets less price-sensitive customers first
- Allows iterative pricing strategy

#### Cons
- Limits initial market size
- May miss fast-growth opportunity
- Early adopters may resent later price drops
- Requires truly differentiated product
- Competitive risk if others enter at lower price

#### Key Metrics
- **Price Premium Index**: Your price / market average
- **Revenue per Customer**: Higher early, validates skimming
- **Market Penetration by Price Tier**: % of TAM reached
- **Customer Lifetime by Tier**: Do early customers stay?
- **Brand Perception**: Premium vs value perception tracking

---

## 6. Psychological Pricing

#### Definition
Use psychological principles to influence customer perception and purchasing behavior.

#### Core Principles

**Charm Pricing (Ending in 9)**
```
Research: $99 outperforms $100 by 5-20% in sales
Mechanism: Left-digit effect (brain anchors on "9" vs "10")

When to use:
✓ Consumer products
✓ B2C SaaS
✓ Price-sensitive markets

When NOT to use:
✗ Premium/luxury positioning
✗ Enterprise B2B
✗ Professional services
```

**Prestige Pricing (Round Numbers)**
```
Research: $100 outperforms $99 for luxury goods
Mechanism: Round numbers feel more premium, easier to process

Examples:
- Premium SaaS: $500/month (not $499)
- Luxury goods: $1,000 (not $999)
- Consulting: $10,000 project (not $9,999)
```

#### Anchoring Effects

**Price Anchoring Strategy:**
```
Technique: Show expensive option first to make others seem reasonable

Example Pricing Page (order matters):

1. Enterprise: $999/month (anchor - rarely purchased)
   ↓ Makes $299 feel reasonable
2. Professional: $299/month (target tier)
   ↓ Makes $99 feel like a bargain
3. Basic: $99/month (entry tier)

Reverse order would make $299 feel expensive.
```

**Comparison Anchoring:**
```
Method: Show what customer would pay without your product

Example:
"Hiring a full-time designer: $80,000/year
Our unlimited design service: $3,000/year

You save: $77,000/year (96% savings)"

The $80k anchors the value, making $3k feel like a steal.
```

#### Decoy Pricing

**Definition:** Add a strategically-priced option to make target option look better.

**Classic Decoy Example:**
```
Before (2 options - customers split 50/50):
├─ Basic: $10/month
└─ Pro: $30/month

After (add decoy - 70% choose Pro):
├─ Basic: $10/month
├─ Standard: $28/month (decoy - intentionally poor value)
└─ Pro: $30/month (target - looks great vs Standard)

Mechanism: Pro is only $2 more than Standard but much better value
```

**Application in SaaS:**
```
Starter: $29/month
- 5 projects
- 1 user
- Email support

Professional: $89/month (decoy)
- 25 projects
- 5 users
- Email support
- Basic analytics

Business: $99/month (target)
- Unlimited projects
- Unlimited users
- Priority support
- Advanced analytics
- Integrations
- Custom branding

Business is only $10 more than Professional but unlocks
everything, making it the obvious choice.
```

#### Bundle Pricing Psychology

**Good-Better-Best Framework:**
```
Good: $50/month
- Core features
- ~20% of customers choose

Better: $100/month (2x price, 4x features)
- Everything in Good
- Advanced features
- ~60% of customers choose (target)

Best: $200/month (2x price, 2x features vs Better)
- Everything in Better
- Premium features
- ~20% of customers choose

Middle option captures majority through compromise effect.
```

#### Pricing Format Psychology

**Annual vs Monthly Display:**
```
Option A (emphasize savings):
"$9/month (billed annually at $108)
Save $36 vs monthly billing"

Option B (reduce sticker shock):
"$108/year (just $9/month)
One payment, 12 months of access"

Option A for price-sensitive, Option B for commitment-hesitant
```

**Per-Unit Pricing:**
```
Option A: "$99/month"
- Feels expensive for individual

Option B: "$99/month for team of 10 = $9.90/person"
- Feels affordable when divided

B2B SaaS: Always show per-user cost breakdown
```

#### Price-Quality Perception

**Price as Signal:**
```
Low Price → May signal:
- Lower quality
- Less support
- Budget option
- Limited features

High Price → May signal:
- Premium quality
- Better support
- Professional option
- Full features

Match price to intended perception
```

#### Scarcity and Urgency

**Limited-Time Pricing:**
```
"Early Bird: $499 (expires in 3 days)
Regular Price: $699 (after launch)"

Psychology: Fear of missing out (FOMO)
Increases conversion by 20-40%
```

**Limited Quantity:**
```
"Only 50 spots available at $99/month
Next tier: $149/month"

Creates urgency through scarcity
Works well for cohort-based products, new launches
```

#### Pricing Presentation Best Practices

**Do:**
- Show annual savings clearly
- Use decoy pricing intentionally
- Display most popular option prominently
- Keep pricing page simple (max 4 tiers)
- A/B test pricing displays

**Don't:**
- Use charm pricing for premium products
- Hide fees or surprise customers
- Make pricing overly complex
- Change prices frequently without notice
- Use fake scarcity (erodes trust)

#### Common Psychological Biases to Leverage

| Bias | How to Use | Example |
|------|------------|---------|
| Anchoring | Show high price first | $999 tier before $99 tier |
| Loss Aversion | Frame as avoiding loss | "Don't lose $10k/year to inefficiency" |
| Social Proof | Show popular option | "Most Popular" badge |
| Reciprocity | Give before asking | Free trial before paid |
| Scarcity | Limited availability | "Only 5 spots left" |
| Default Effect | Pre-select preferred tier | Annual billing selected by default |

#### Testing Psychological Pricing

**A/B Test Ideas:**
```
Test 1: $99 vs $100
Hypothesis: Charm pricing increases conversion

Test 2: Annual shown first vs monthly shown first
Hypothesis: Annual-first increases annual subscriptions

Test 3: 3 tiers vs 4 tiers (with decoy)
Hypothesis: Decoy pushes to higher tier

Test 4: "Most Popular" badge on middle tier
Hypothesis: Social proof increases middle tier selection
```

#### Pros
- Can increase conversion by 10-40%
- No cost to implement
- Backed by behavioral research
- Easy to test and iterate

#### Cons
- Can feel manipulative if overdone
- Cultural differences in effectiveness
- May not work for all products
- Risk of appearing unprofessional

---

## 7. Tiered Pricing (Good-Better-Best)

#### Definition
Offer 3-4 pricing tiers to serve different customer segments and capture more value.

#### Optimal Tier Structure

**Three-Tier Framework (Recommended):**
```
Basic/Starter (20% adoption):
- Entry point for price-sensitive customers
- Core features only
- Self-serve support
- Goal: Land customers, upsell later

Professional/Growth (60% adoption - TARGET):
- Sweet spot for most customers
- Most features included
- Standard support
- Goal: Maximize revenue

Enterprise/Premium (20% adoption):
- Premium features
- White-glove support
- Custom integrations
- Goal: Maximize ARPU, serve large customers
```

**Four-Tier Framework (Advanced):**
```
Free (60% of users, 0% revenue):
- Lead generation
- Network effects
- Freemium model

Starter (30% of paid, 15% revenue):
- Entry paid tier
- Basic features

Professional (60% of paid, 60% revenue - TARGET):
- Main tier
- Full features

Enterprise (10% of paid, 25% revenue):
- Premium tier
- Custom solutions
```

#### Feature Allocation Strategy

**Feature Differentiation Matrix:**

| Feature Type | Free | Starter | Professional | Enterprise |
|--------------|------|---------|--------------|------------|
| Core Value | ✓ Limited | ✓ | ✓ | ✓ |
| Advanced Features | ✗ | ✗ | ✓ | ✓ |
| Collaboration | ✗ | Limited | ✓ | ✓ |
| Integrations | ✗ | 3 | 10 | Unlimited |
| Support | Community | Email | Priority | Dedicated |
| Customization | ✗ | ✗ | Limited | ✓ |
| Security/Compliance | Basic | Basic | Advanced | Enterprise |
| Analytics | Basic | Basic | Advanced | Custom |

**Good-Better-Best Pricing Ratios:**
```
Good: $X (baseline)
Better: $3-4X (best value - target tier)
Best: $8-12X (premium)

Example:
Basic: $25/month
Professional: $99/month (4x - target)
Enterprise: $299/month (12x)

Why this ratio works:
- 3-4x jump feels justified with feature adds
- 8-12x jump appeals to different segment (enterprises)
```

#### Real-World Tiered Pricing Examples

**Example 1: Project Management SaaS**
```
Basic: $10/user/month (up to 10 users)
- Unlimited projects
- 10GB storage
- Email support
- Core features

Professional: $20/user/month
- Everything in Basic
- 100GB storage per user
- Priority support
- Advanced reporting
- Integrations
- Timeline view
- 👑 Most Popular

Enterprise: Custom pricing
- Everything in Professional
- Unlimited storage
- Dedicated support
- SSO/SAML
- Advanced security
- Custom onboarding
- SLA guarantee
```

**Example 2: Marketing Tool**
```
Starter: $49/month
- Up to 1,000 contacts
- 10,000 emails/month
- Basic templates
- Email support

Growth: $149/month ⭐
- Up to 10,000 contacts
- 100,000 emails/month
- Premium templates
- A/B testing
- Automation
- Priority support
- Analytics

Pro: $299/month
- Up to 50,000 contacts
- Unlimited emails
- Everything in Growth
- Advanced segmentation
- Multi-user accounts
- API access
- Phone support
```

#### Capacity-Based Tiering

**Usage-Based Tiers:**
```
Tier 1: $29/month (up to 10,000 API calls)
Tier 2: $99/month (up to 100,000 API calls)
Tier 3: $299/month (up to 500,000 API calls)
Enterprise: Custom (500k+ API calls)

Per-unit economics:
Tier 1: $0.0029 per call
Tier 2: $0.00099 per call (better value)
Tier 3: $0.000598 per call (best value)

Encourages upgrades as usage grows naturally.
```

#### Tier Naming Strategy

**Professional Naming:**
- Starter / Professional / Enterprise
- Basic / Pro / Premium
- Individual / Team / Business

**Creative Naming (if brand-appropriate):**
- Free / Grow / Scale / Enterprise
- Hobbyist / Creator / Professional / Studio
- Bronze / Silver / Gold / Platinum

**Avoid:**
- Too many tiers (max 4)
- Confusing names (what's difference between "Pro" and "Professional"?)
- Negative framing ("Limited" tier vs "Starter" tier)

#### Migration and Upsell Strategy

**Upgrade Triggers:**
```
Built-in upsell moments:
- User hits usage limit: "Upgrade to continue"
- User tries premium feature: "Unlock with Professional"
- Team grows: "Add team members with Team plan"
- Integration needed: "Available on Pro and above"

Proactive outreach:
- 80% of limit: "You're growing! Consider upgrading"
- High engagement: "Power users love our Pro plan"
- Multiple team members on Basic: "Team plan saves you money"
```

**Smooth Upgrade Path:**
```
Prorated upgrade immediately:
"Upgrade now to Professional for just $12.50
(prorated from your $10 Basic plan)"

vs

Confusing upgrade experience:
"Upgrade to Professional. You'll be charged $99 on your next billing date."
```

#### Common Tiering Mistakes

**Mistake 1: Too Many Tiers**
```
Bad (6 tiers):
Free / Lite / Basic / Pro / Premium / Enterprise
→ Decision paralysis, confusing differentiation

Good (3 tiers):
Starter / Professional / Enterprise
→ Clear choices, obvious upgrade path
```

**Mistake 2: Wrong Feature Gating**
```
Bad:
- Basic tier too limited (can't see value)
- Pro tier has everything (no reason for Enterprise)

Good:
- Basic: Enough to see value, but limitations drive upgrade
- Pro: Full-featured for most users
- Enterprise: Special needs (security, scale, support)
```

**Mistake 3: Poor Value Progression**
```
Bad (linear value):
Basic: 10 features for $10
Pro: 20 features for $20
→ No incentive to upgrade

Good (exponential value):
Basic: 10 features for $10
Pro: 30 features for $20 (3x features for 2x price)
→ Pro feels like a great deal
```

#### Pros
- Captures different customer segments
- Natural upsell path
- Maximizes revenue per customer
- Serves both small and large customers

#### Cons
- Complex to design and maintain
- Can confuse customers if poorly executed
- Requires ongoing optimization
- Feature allocation decisions are hard

#### Key Metrics
- **Tier Distribution**: % customers in each tier
- **Upgrade Rate**: % moving to higher tier per month
- **Downgrade Rate**: % moving to lower tier per month
- **Revenue Mix**: % of revenue from each tier
- **ARPU by Tier**: Average revenue per user in each tier

---

## Pricing Decision Framework

### Step-by-Step Pricing Process

**Step 1: Understand Your Costs (1-2 days)**
```
Calculate:
- COGS (Cost of Goods Sold)
- CAC (Customer Acquisition Cost)
- Support costs per customer
- Infrastructure costs
- Fully-loaded cost per customer

Minimum Viable Price = Total Cost per Customer / 0.7
(Ensures 30% minimum margin)
```

**Step 2: Research the Market (3-5 days)**
```
Analyze:
- Top 5 competitors' pricing
- Their tier structure
- Feature comparison
- Market positioning
- Average deal size in your category

Competitive Price Range = [Lowest competitor, Highest competitor]
```

**Step 3: Quantify Customer Value (1-2 weeks)**
```
Interview 10-20 target customers:
- What problem does this solve?
- What's the cost of the problem?
- What alternatives are they using?
- What would they pay?
- What's too expensive?

Value-Based Price Range = [30% of value created, 50% of value created]
```

**Step 4: Synthesize Pricing Range (1 day)**
```
Overlay three ranges:
- Cost-Plus: $X (minimum)
- Competitive: $Y to $Z
- Value-Based: $A to $B

Sweet Spot: Where competitive and value-based overlap

Example:
Cost-Plus minimum: $50
Competitive range: $80-150
Value-Based range: $100-200
→ Sweet Spot: $100-150
```

**Step 5: Choose Initial Price (1 day)**
```
Within sweet spot, choose based on strategy:

Market Entry (Penetration):
→ Low end of range ($100)

Balanced Growth:
→ Mid range ($125)

Premium Positioning (Skimming):
→ High end of range ($150)

Default recommendation: Start at mid-high ($135)
- Easier to lower than raise
- Test willingness to pay
- Can always discount
```

**Step 6: Structure Tiers (2-3 days)**
```
If using tiered pricing:

Tier 1 (Starter): 50-70% of main tier price
- $75-95 (let's choose $79)

Tier 2 (Professional - TARGET): Sweet spot price
- $135

Tier 3 (Enterprise): 2-3x professional tier
- $299-399 (let's choose $299)

Allocate features across tiers based on customer research
```

**Step 7: Test and Iterate (Ongoing)**
```
Week 1-4: Launch at chosen price
- Track conversion rate
- Note objections
- Monitor competitor changes

Month 2-3: A/B test if sufficient traffic
- Test +/- 20% price variation
- Test different tier structures
- Test messaging

Month 4+: Optimize based on data
- Adjust price if needed
- Refine feature allocation
- Consider new tiers or pricing models
```

---

## Pricing Page Best Practices

### Layout and Structure

**Optimal Pricing Page Structure:**
```
1. Headline: "Simple, transparent pricing"
2. Toggle: Annual/Monthly (show annual savings)
3. Tier Cards: 3-4 tiers side-by-side
4. Feature Comparison: Table below cards
5. FAQ: Common pricing questions
6. Social Proof: "Join 10,000+ companies"
7. CTA: "Start free trial" or "Get started"
```

### Tier Card Design

**Effective Tier Card:**
```
[TIER NAME]
Most Popular ⭐ (if applicable)

$99/month
or $79/month billed annually (Save $240)

[Primary CTA Button]
"Start 14-day trial"

Key Features:
✓ Unlimited projects
✓ 10 team members
✓ Priority support
✓ Advanced analytics
✓ 50+ integrations

[Secondary CTA]
"View all features"
```

### Comparison Table

**Feature Comparison Best Practices:**
```
Category-based feature list:

Core Features:
├─ Projects: Basic (10) | Pro (Unlimited) | Enterprise (Unlimited)
├─ Storage: Basic (10GB) | Pro (100GB) | Enterprise (Unlimited)
└─ Users: Basic (1) | Pro (10) | Enterprise (Unlimited)

Advanced Features:
├─ Analytics: Basic (✗) | Pro (✓) | Enterprise (Advanced)
├─ API Access: Basic (✗) | Pro (✓) | Enterprise (✓)
└─ Custom Branding: Basic (✗) | Pro (✗) | Enterprise (✓)

Support:
├─ Response Time: Basic (48h) | Pro (24h) | Enterprise (4h)
└─ Support Type: Basic (Email) | Pro (Priority) | Enterprise (Dedicated)

Max 15-20 features in comparison table (don't overwhelm)
```

### Persuasion Elements

**Trust Builders:**
- "No credit card required" for trials
- "Cancel anytime" for subscriptions
- "30-day money-back guarantee"
- Security badges (SOC 2, GDPR, etc.)
- Customer logos ("Trusted by...")
- Testimonials about value

**Urgency Creators:**
- "Limited time: Save 30% on annual plans"
- "Early bird pricing ends [date]"
- "Join 100+ teams who signed up this week"

---

## Common Pricing Mistakes and Fixes

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| Pricing too low initially | Hard to raise, anchors value | Start 20% higher than comfortable, discount if needed |
| Too many tiers | Decision paralysis | Max 4 tiers (ideally 3) |
| Features in wrong tiers | Blocks conversion or prevents upsells | Test feature allocation, move based on data |
| No annual plan | Miss easy revenue boost | Offer annual at 15-20% discount vs monthly |
| Frequent price changes | Erodes trust | Change max 1-2x per year |
| Hidden fees | Customers feel tricked | Transparent all-in pricing |
| Competitor obsession | Race to bottom | Focus on value, differentiate |
| One-size-fits-all | Leave money on table | Tier pricing for different segments |
| Not testing | Guessing optimal price | A/B test when possible |
| Neglecting price communication | Confusion, objections | Clear messaging about value |

---

## Summary: Quick Reference

**Choosing Your Primary Strategy:**

| Situation | Best Strategy | Expected Margin |
|-----------|---------------|-----------------|
| Unique value prop, B2B | Value-Based | High (60-80%) |
| Competitive market | Competition-Based | Medium (30-50%) |
| Need profitability guarantee | Cost-Plus | Target (varies) |
| Entering crowded market | Penetration | Low initially |
| First-to-market innovation | Skimming | Very High (70-90%) |
| Consumer product | Psychological + Tiered | Medium (40-60%) |

**Quick Wins:**
1. Add annual billing (instant 15-20% revenue boost)
2. Implement 3-tier pricing (capture more segments)
3. Use charm pricing ($99 vs $100) for B2C
4. Add "Most Popular" badge to target tier
5. Test showing annual pricing first

Most businesses should use a combination: tiered pricing structure with value-based pricing, influenced by competitive positioning and psychological principles.
