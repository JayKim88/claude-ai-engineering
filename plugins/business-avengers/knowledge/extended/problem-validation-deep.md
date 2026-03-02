# Problem Validation Deep Guide

## Source Methodologies
This guide synthesizes expert frameworks from:
- Rob Fitzpatrick — *The Mom Test* (customer interview design)
- Clayton Christensen — *Jobs to be Done* (JTBD theory)
- Peter Thiel — *Zero to One* (secrets and monopoly thinking)
- Ash Maurya — *Running Lean* (Lean Canvas validation sequence)
- Steve Blank — *The Four Steps to the Epiphany* (customer discovery)

---

## Quick Decision Guide (Agent Decision Criteria)

| Situation | Threshold | Action |
|-----------|-----------|--------|
| CEO describes solution, not problem | Warning | Redirect to problem discovery — solutions before problems cause premature optimization |
| Problem stated as "many people feel..." | Insufficient | Require: specific person + specific situation + specific frequency/cost |
| Zero existing alternatives named | Suspicious | If no workaround exists, customers may not consider it a problem |
| CEO is sole person with this problem | Risk | Validate with 5+ others before proceeding |
| Revenue hypothesis missing | Incomplete | Idea canvas cannot be approved without WTP estimate |

## Red Flags (Explicitly warn the CEO)
- "Everyone has this problem" → not a validated problem, it's an assumption
- "No competitors" when market is large → likely means no viable monetization discovered yet
- Problem framing includes the solution ("an app that...") → restart problem definition
- Assumption list is empty → all startups fail due to unvalidated assumptions; make them explicit

---

## 1. The Mom Test Framework (Rob Fitzpatrick)

### Core Principle
Most customer interviews are useless because we ask questions that generate false positives.
People are polite — they tell you what you want to hear. The Mom Test fixes this.

### The Three Rules

**Rule 1: Talk about their life, not your idea**
- Wrong: "Do you think this app would be useful?"
- Right: "Walk me through the last time you had to [do the task]."

**Rule 2: Ask about specifics, not hypotheticals**
- Wrong: "Would you pay for a solution to this?"
- Right: "How much are you currently spending to handle this? How many hours per week?"

**Rule 3: Listen, don't pitch**
- Compliments don't count as validation ("That sounds great!" = no data)
- Pain signals that count: money spent, time wasted, workarounds built, emotional frustration

### Good vs. Bad Interview Questions

| Bad Questions (Avoid) | Good Questions (Use) |
|----------------------|---------------------|
| "Do you like our idea?" | "How do you currently handle X?" |
| "Would you use this?" | "When was the last time you did X?" |
| "How much would you pay?" | "What do you spend on this today?" |
| "Do you think X is a problem?" | "Tell me about the last time X happened." |
| "Would this save you time?" | "How much time does X cost you now?" |

### 5 Signals That Validate a Real Problem
1. **Money already being spent** — They pay for a workaround today
2. **Time being wasted** — Quantifiable hours lost per week/month
3. **Emotional frustration** — Unprompted negative language when describing it
4. **Active workarounds** — Spreadsheets, manual processes, duct-tape solutions
5. **Repeated occurrence** — It happens regularly (weekly or more), not once

### 5 Signals That Invalidate (False Positives to Watch)
1. "That sounds like a great idea" — politeness, not validation
2. "I would definitely use that" — hypothetical future behavior, not real
3. "A lot of people have this problem" — vague, not their own experience
4. "You should build X feature" — feature suggestion without pain evidence
5. "I'd pay for that" — without asking how much and seeing resistance

---

## 2. Jobs to Be Done (JTBD) Framework (Christensen)

### Core Concept
People don't "buy products" — they "hire" them to do a job in their life.
Understanding the job reveals why customers switch, churn, or never adopt.

### Three Types of Jobs

**Functional Job** — The practical task to accomplish
- Example: "Get invoices to clients faster"
- Measure: Time, cost, accuracy, reliability

**Emotional Job** — How they want to feel
- Example: "Feel professional and credible to clients"
- Measure: Stress reduction, confidence, pride

**Social Job** — How they want to be perceived by others
- Example: "Look like a serious freelancer, not an amateur"
- Measure: Peer recognition, status signals

### JTBD Statement Format
```
When [situation],
I want to [motivation/goal],
So I can [expected outcome].
```

**Example (bad):** "Users want invoice software."
**Example (good):** "When I finish a project and need to get paid quickly,
I want to send a professional invoice in under 5 minutes,
so I can maintain cash flow without looking disorganized."

### Switching Triggers (Forces of Progress)
Understanding why customers switch from current solution to a new one:

| Push Forces (Away from old) | Pull Forces (Toward new) |
|-----------------------------|--------------------------|
| Frustration with current solution | Attraction to new solution |
| Growing urgency of the problem | Social proof (others using it) |
| Triggering event (job change, scale) | Perceived ease of switching |

**Anxiety Forces (Prevent switching):**
- Learning curve fear
- Data migration risk
- "What if the new product is worse?"

**Habit Forces (Status quo bias):**
- "Good enough" satisfaction
- Team already trained on current tool
- Cost of changing workflows

### JTBD Interview Questions
- "What made you start looking for a solution?"
- "What were you using before? Why did you stop?"
- "What almost stopped you from switching?"
- "After switching, what surprised you — positively or negatively?"

---

## 3. Zero to One — The Secret Test (Peter Thiel)

### The "Secrets" Framework
Thiel argues every great business is built on a secret — a truth others don't see or believe.

**Types of secrets:**
1. **Secrets about nature** — Something true about how the world works that most ignore
2. **Secrets about people** — Something about human behavior/desire that goes unacknowledged

### The Monopoly Question
Good businesses don't compete — they create categories where competition is irrelevant.

Ask: "If we succeed, can we dominate this specific market for 10+ years?"

| Competition Trap | Monopoly Thinking |
|-----------------|-------------------|
| "We're like Uber for X" | "We're the only company doing X for Y" |
| "We're 10% better than competitors" | "We're 10x different — different category" |
| "We have more features" | "Competitors structurally cannot offer what we do" |

### The Timing Question
- Why will this work NOW that it didn't 5 years ago?
- What specific change made this possible today?
- Is this a temporary window or a durable opportunity?

---

## 4. Lean Canvas Validation Sequence (Ash Maurya)

### Priority Order (Most Risky First)
Maurya argues you should validate in this order — start where you're most likely to be wrong:

```
1. Problem         ← Is this a real, painful problem?
2. Customer Segment ← Who has this problem most acutely?
3. Unique Value Prop ← Why us vs. alternatives?
4. Solution        ← Will this solution actually work?
5. Revenue Streams  ← Will they pay enough to make this viable?
6. Channels        ← Can we reach them cost-effectively?
```

### Riskiest Assumption Test (RAT)
Before building anything, identify the single most dangerous assumption and test it cheaply.

```
Riskiest assumption: [State the assumption]
Test method: [Cheapest way to falsify it]
Success metric: [Number that would validate it]
Time box: [Maximum time to run the test]
```

**Example:**
```
Riskiest assumption: "Freelancers will pay $29/month for invoice software"
Test method: Landing page + payment intent form (before building)
Success metric: 50 email signups + 5 payment intent attempts in 2 weeks
Time box: 2 weeks
```

---

## 5. Idea Canvas Quality Standards

### Mandatory Problem Statement Format

```
WEAK: "Many people struggle with invoicing."

STRONG: "US-based freelance designers (est. 2.1M) spend on average
3.2 hours/week manually building invoices in Excel or Google Docs,
costing approximately $160/week in billable time not recovered.
Current workarounds: FreshBooks ($17/mo, too complex), Wave (free but
limited), or manual Excel (most common). Primary pain:
professionalism/branding and payment speed."
```

### Revenue Hypothesis Requirements

The idea canvas must include a WTP (Willingness to Pay) estimate with basis:

```
Format: "Estimated WTP: $X/month"
Basis options (choose one):
  - Comparable product benchmark: "[Product Y] charges $Z for similar value"
  - Cost-of-current-solution: "Current Excel + time costs ~$X/month equivalent"
  - Direct signal: "5 interviewees mentioned they'd pay around $X"
  - Industry benchmark: "B2B SaaS for SMBs typically $X-Y/month"
```

### Assumption Register (Mandatory)

Every idea canvas must list at least 3 core assumptions:

```markdown
## Core Assumptions (Before Validation)

| # | Assumption | Risk Level | Validation Method |
|---|-----------|------------|-------------------|
| 1 | Freelancers spend 3+ hrs/week on invoicing | High | 10 customer interviews |
| 2 | They'll pay $29/month for time savings | High | Landing page test |
| 3 | Stripe integration is the key feature | Medium | Prototype test |
```

---

## 6. Output Checklist (before saving idea-canvas.md)

```
□ Problem describes a specific person in a specific situation (not "many people")
□ Current alternatives listed (minimum 3: workarounds count)
□ Differentiation is structural (not just "better UX")
□ Revenue hypothesis with explicit basis (comparable product, interview, or cost calculation)
□ Minimum 3 assumptions explicitly listed with validation methods
□ JTBD statement written: "When [X], I want [Y], so I can [Z]"
□ Mom Test applied: problem framing contains zero solution language
□ "Why Now" noted if applicable (technology/regulatory/behavioral trigger)
```

---

## 7. Quality Self-Assessment Block (add at top of idea-canvas.md)

```markdown
---
**Idea Canvas Quality Check**
- Depth: [1–3] — [reason: specific situation described vs. vague]
- Evidence: [1–3] — [reason: # interview signals or comparable benchmarks]
- Specificity: [1–3] — [reason: WTP number and basis present]
- Assumptions listed: [X]
- Unmet criteria: [list or "none"]
---
```
