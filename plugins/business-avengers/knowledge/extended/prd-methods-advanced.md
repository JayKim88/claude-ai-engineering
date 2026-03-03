# PRD Methods Advanced Guide

## Source Methodologies
This guide synthesizes expert frameworks from:
- Marty Cagan — *Inspired: How to Create Tech Products Customers Love*
- Ryan Singer — *Shape Up* (Basecamp)
- Jeff Patton — *User Story Mapping*
- Teresa Torres — *Continuous Discovery Habits*

---

## Quick Decision Guide (Agent Decision Criteria)

| Situation | Threshold | Action |
|-----------|-----------|--------|
| PRD written as a feature list, not a problem statement | Insufficient | Rewrite starting from problem + outcome |
| MVP scope > 6 weeks for 1 person | Too large | Cut to v1.1; document deferrals |
| Success metrics are outputs ("launch X"), not outcomes ("users do Y") | Insufficient | Replace with action-based, measurable metrics |
| User stories are tasks ("add payment button"), not value statements | Insufficient | Rewrite as "As [user], I want [action], so that [outcome]" |
| Feature list has no "Will NOT build" section | Incomplete | Explicitly list ≥3 deferred items with rationale |
| PRD has no risk column or uncertainty flagging | Insufficient | Add risks and open questions for each major feature |

---

## 1. Inspired — Four Product Risks (Marty Cagan)

Every feature in the PRD must address four product risks before going to engineering:

### Risk 1: Value Risk
*Will customers buy or choose to use it?*
- Is there evidence users want this specific solution? (not just the problem)
- Can you point to interview signal, survey data, or analogous products?
- **Minimum bar**: At least 1 real user said something like "I'd stop using X if Y offered this"

### Risk 2: Usability Risk
*Can users figure out how to use it?*
- Is the interaction model simple enough that a new user can succeed in under 2 minutes without help?
- **Minimum bar**: The core user flow must be described in the PRD, not left to design

### Risk 3: Feasibility Risk
*Can we build it with our current team and technology?*
- Solo founders: flag any feature requiring technology outside their current stack
- **Minimum bar**: Each Must-Have feature needs a Tech Lead feasibility note

### Risk 4: Business Viability Risk
*Will this solution work for our business?*
- Does it align with the chosen revenue model?
- **Minimum bar**: Each feature's cost-to-build should be estimated relative to expected revenue impact

### Opportunity Assessment (before writing PRD)
Before writing, answer these 10 questions:
1. Exactly what problem will this solve? (value proposition)
2. For whom do we solve this problem? (target market)
3. How big is the opportunity? (market size)
4. What alternatives are out there? (competitive landscape)
5. Why are we best positioned to solve it? (differentiation)
6. Why now? (market window)
7. How will we measure success? (metrics/OKR)
8. What factors are critical to success? (solution requirements)
9. Given the above, what's our recommendation? (go/no-go)
10. Identify assumptions: what must be true for this to work?

---

## 2. Shape Up — Scope & Time Framework (Ryan Singer / Basecamp)

### Core Principle: Fixed Time, Variable Scope
- Traditional: Fixed scope, variable time → chronic delays
- Shape Up: Fixed time (appetite), variable scope → ship on time by cutting scope

### Appetite Sizing
Before writing any PRD, define the appetite:

| Appetite | Description | Solo Founder Equivalent |
|----------|-------------|------------------------|
| **Small Batch** | 1-2 weeks of work | MVP feature you can ship in a week |
| **Big Batch** | Up to 6 weeks | Complete MVP launch |
| **Spike** | 1-2 days | Technical or design experiment |

**Rule**: If a feature doesn't fit the appetite, it's not a prioritization problem — it's a scope problem. Cut the feature, not the deadline.

### Shaping Before Writing PRD
Shaping = pre-work to make a pitch concrete enough to hand off.

**The Fat Marker Sketch (not wireframes):**
- Rough sketches that show the key flows without committing to exact UI
- Fast: 30 minutes per screen, not pixel-perfect
- Purpose: identify "rabbit holes" (endless implementation paths) early

**Breadboarding (for non-visual flows):**
- Show places (screens), affordances (buttons/links), and connection lines
- Purpose: validate the flow logic before design begins

### The Pitch (replaces traditional requirements doc)
A Shape Up pitch has 5 components:
1. **Problem**: the raw problem to solve
2. **Appetite**: how much time we're willing to spend
3. **Solution**: the core elements at a high level (fat marker sketch)
4. **Rabbit holes**: known complexities or unknowns to avoid
5. **No-gos**: things explicitly excluded from scope

### Hill Charts (for tracking, not planning)
Instead of % complete, assess each piece of work:
- **Uphill**: still figuring out the unknowns (discovery phase)
- **Top of hill**: known what to do, execution in progress
- **Downhill**: straightforward execution toward completion

**PRD implication**: For each Must-Have feature, note whether it's uphill (still uncertain) or downhill (well-understood). Uphill features need time-boxed spikes before committing.

---

## 3. User Story Mapping (Jeff Patton)

### Why Flat Backlogs Fail
A flat list of user stories loses the narrative — the "why" behind each task.
Story mapping restores narrative by organizing stories into a 2D structure.

### Story Map Structure

```
Backbone (horizontal axis — User Activities)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Sign Up] → [Create Project] → [Invite Team] → [Ship Product]
    │               │                │               │
[Verify email]  [Name it]      [Send invite]   [Set release]
[Set password]  [Add desc]     [Set role]      [Draft notes]
[Choose plan]   [Add logo]     [Resend]        [Publish]
    │
Release 1 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
[Verify email]  [Name it]      [Send invite]   [Set release]
    │
Release 2 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
[Set password]  [Add desc]     [Set role]      [Draft notes]
```

**How to use in PRD:**
- Write the backbone first (what are the 4-6 major activities a user does?)
- For each activity, list the stories (what specific actions enable that activity?)
- Draw horizontal release lines: what's the minimum needed for MVP?
- Everything above the line = MVP. Everything below = v1.1+

### Walking Skeleton
The minimal end-to-end flow that proves the core value proposition works.
- A walking skeleton is NOT the MVP — it's even smaller
- Purpose: validate the technical architecture and core user journey before adding polish
- Rule: if the walking skeleton doesn't deliver the core "aha moment", revisit the solution

---

## 4. Continuous Discovery Habits (Teresa Torres)

### Opportunity Solution Tree
Instead of jumping to solutions, map the full opportunity space first:

```
Goal (Outcome)
    └── Opportunity 1 (user need / pain / desire)
    │       └── Solution A
    │       └── Solution B
    └── Opportunity 2
    │       └── Solution C
    └── Opportunity 3
            └── Solution D
            └── Solution E
```

**PRD implication**: The PRD should show WHICH opportunity the product is addressing, and WHY this opportunity was chosen over others.

### Assumption Testing (before building)
For each major feature, identify the riskiest assumption and define the cheapest test:

```
Feature: [Feature Name]
Riskiest assumption: [State it]
Test method: [Cheapest falsification — survey, landing page, prototype, interview]
Success signal: [Specific observable outcome that validates it]
Time box: [Maximum 1-2 weeks]
```

**Assumption types to test:**
- Desirability: do users want this? (interviews, landing page)
- Usability: can users use this? (prototype test)
- Feasibility: can we build this? (technical spike)
- Viability: is this worth building? (revenue model check)

---

## 5. PRD Quality Standards

### Problem Statement (mandatory format)

```
WEAK: "Users need better project management"

STRONG: "Freelance designers working on 3+ concurrent client projects spend
2+ hours/week manually sending status updates via email. Clients lose
trust when updates are delayed. Current tools (Basecamp, Notion) are
too heavy — most freelancers use a shared Google Doc that breaks down
at 3+ clients. This causes 20% of projects to result in scope disputes."
```

### Success Metrics — Outcome Over Output

| Wrong (Output) | Right (Outcome) |
|----------------|-----------------|
| "Launch the feature" | "60% of active users use this feature within 30 days" |
| "Add notifications" | "D7 retention increases from 35% to 45%" |
| "Build onboarding" | "Time to first value < 5 min for 70% of new users" |
| "Ship mobile app" | "Mobile DAU ≥ 40% of total DAU within 60 days of launch" |

### "What We Will NOT Build" — Mandatory Section
Every PRD must explicitly list at least 3 deferred items with rationale:

```markdown
## Out of Scope (This Release)

| Feature | Why Deferred | Planned For |
|---------|--------------|-------------|
| [Feature A] | Low signal from user interviews; <20% requested it | v1.2 or never |
| [Feature B] | Requires external API integration — 3 weeks extra; not in appetite | v1.1 post-launch |
| [Feature C] | Nice-to-have; core job doesn't require it | v2.0 |
```

**Purpose**: Prevents scope creep. If stakeholders want deferred items added, they must explicitly change the appetite or delay launch.

### RICE Confidence Gate

| Confidence | Meaning | Action |
|------------|---------|--------|
| >80% | Strong user signal (interviews, data) | Include in Must-Have |
| 50-80% | Some signal, some assumption | Include but flag as "Needs validation" |
| <50% | Mostly assumption | Move to "Uncertain Priority" section; validate before building |

---

## 6. User Persona Quality Standards

### Persona Anti-Patterns (avoid)
- **Demographics-only personas**: "35-year-old female marketing manager" → tells you nothing about behavior
- **Vanity personas**: made-up characters with no research backing
- **Too many personas**: 5+ personas = no clear priority

### JTBD-Based Persona Format (preferred)

```markdown
## Persona: [Name]

**Job Title / Role**: [Real role, not fictional name]
**Situation**: [When and where does this person encounter the problem?]

**Main Job**: [What are they trying to accomplish?]
  - Functional: [practical task]
  - Emotional: [how they want to feel]
  - Social: [how they want to be perceived]

**Current Solution**: [What do they use now? What workarounds?]
**Frustration**: [What specifically fails about current solution?]
**Switching Trigger**: [What would make them look for something new?]

**Validated by**: [Interview count, survey data, or explicit assumption flag]
```

### Minimum Standard
- Primary persona: at least 2 behavioral signals (things they DO, not things they ARE)
- Each persona must link to at least 1 Must-Have feature in the PRD
- Flag any persona built entirely from assumption (no interview/data)

---

## 7. Feature Priority Framework

### MoSCoW + RICE Combined Decision

**Step 1: MoSCoW classification**
- **Must Have**: Without this, MVP fails to deliver the core value proposition
- **Should Have**: Important, but MVP can ship without it (add in first sprint post-launch)
- **Could Have**: Nice-to-have if time allows (defer to v1.1)
- **Won't Have**: Explicitly out of scope (prevents scope creep)

**Step 2: RICE scoring for Must-Have features only**
```
RICE = (Reach × Impact × Confidence) / Effort

Reach: # of users affected per quarter
Impact: 3=massive / 2=high / 1=medium / 0.5=low
Confidence: 80%=validated / 50%=assumed / 20%=speculative
Effort: person-weeks to build
```

**Step 3: Sequence by dependencies**
Some Must-Have features are blockers for others. Map dependencies explicitly.

### Feature Justification (mandatory for each Must-Have)

Every Must-Have feature must include ONE of:
1. **Churn blocker**: "Without X, estimated Y% of users cannot complete the core action"
2. **Value prop blocker**: "Without X, the core value proposition cannot be delivered"
3. **Distribution blocker**: "Without X, users cannot share or invite others (viral loop broken)"
4. **Monetization blocker**: "Without X, payment cannot be collected"

---

## 8. Output Checklist (before saving PRD, user-stories, feature-priority)

```
□ Problem statement describes specific person in specific situation with quantified pain
□ Success metrics are action-based outcomes (not outputs or vanity metrics)
□ MVP scope fits 1 person × 6 weeks (Shape Up appetite)
□ Each Must-Have feature has ONE business justification (churn/blocker/distribution/monetization)
□ "What We Will NOT Build" section exists with ≥3 deferred items and rationale
□ User stories follow: As [specific persona], I want [action], so that [outcome]
□ Each story has Given-When-Then acceptance criteria
□ RICE Confidence <50% features are in a separate "Uncertain Priority" section
□ Four product risks addressed for each Must-Have (Value / Usability / Feasibility / Viability)
□ User personas are JTBD-based (not demographics-only)
□ Feature priority links personas to specific features
□ Open questions and assumptions listed with owners and resolution dates
```
