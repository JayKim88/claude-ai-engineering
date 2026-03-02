# Automation & Scale Knowledge Base

Expert automation frameworks for Phase 11 (Automation Audit & Autonomous Org Design).
Source: Pieter Levels (MAKE), Rob Walling (SaaS Playbook), Mike Michalowicz (Clockwork),
Zapier / n8n automation patterns.

---

## 1. Automation ROI Framework

### When to Automate (Decision Matrix)

**Formula:** Automation ROI = (Time saved per week × hourly value × 52) ÷ Build cost

**Threshold:** Automate if payback period < 8 weeks.

**Automation priority score:**
```
Priority = (Frequency × Time × Error Risk × Scale Impact) ÷ Build Effort

Where:
- Frequency: Daily=5, Weekly=3, Monthly=1
- Time: Hours saved per occurrence (decimal)
- Error Risk: Manual errors likely? High=3, Medium=2, Low=1
- Scale Impact: Gets worse at scale? High=3, Medium=2, Low=1
- Build Effort: Days to build (denominator — higher = lower priority)
```

**Example prioritization:**
| Task | Freq | Time | Error | Scale | Effort | Score |
|------|------|------|-------|-------|--------|-------|
| Daily backup | 5 | 0.1h | 3 | 3 | 0.5d | 9.0 |
| Invoice generation | 3 | 0.5h | 3 | 3 | 1d | 13.5 |
| Support auto-reply | 5 | 0.25h | 1 | 3 | 1d | 11.25 |
| Report generation | 3 | 2h | 2 | 2 | 2d | 6.0 |

### Automation vs. Hire Decision Matrix

| Situation | Automate | Hire Contractor | Hire FTE |
|-----------|----------|----------------|---------|
| Repetitive, rule-based, predictable | ✓ | | |
| Requires judgment, context, relationships | | ✓ | |
| Volume growing 10%+ monthly | ✓ | Temporary bridge | |
| Strategic, intellectual, creative | | | ✓ |
| One-time project with clear deliverable | | ✓ | |
| Core business function, competitive moat | | | ✓ |

---

## 2. The Bus Test (Mike Michalowicz)

**Definition:** Can the business run for 4 weeks without the founder?

**Bus Test Score:** Count YES answers (target: ≥8/10)

| # | Question | Pass |
|---|----------|------|
| 1 | All processes documented in step-by-step SOPs? | |
| 2 | Revenue-generating tasks can be completed by someone else? | |
| 3 | Customer support can be handled without founder? | |
| 4 | Tech systems have access shared with ≥1 person or documented? | |
| 5 | Financial operations (billing, payroll) run without founder? | |
| 6 | Marketing/content publishing can continue without founder? | |
| 7 | Key vendor/supplier relationships have backup contact? | |
| 8 | Monitoring and alerts go to non-founder on-call? | |
| 9 | On-call escalation path defined for outages? | |
| 10 | Business does not depend on founder's unique skill? | |

**Score interpretation:**
- 0–4: Founder dependency — high risk; prioritize documentation and delegation
- 5–7: Partial autonomy — can take 1-week vacations
- 8–10: Autonomous business — can take 4-week vacations; ready for acquisition

---

## 3. Automation Stack (Indie Maker)

### Tier 1: No-Code Automation (start here)
| Tool | Best for | Connections |
|------|----------|------------|
| Zapier | Simple 2-step workflows, SaaS-to-SaaS | 5,000+ apps |
| Make (Integromat) | Complex multi-step flows | 1,000+ apps |
| n8n | Self-hosted, developer-friendly, free | Open source |

### Tier 2: Cron Jobs & Scripts
For time-based, predictable tasks:
```python
# Example: Daily automated report
@cron("0 9 * * *")  # 9 AM daily
async def daily_digest():
    metrics = await get_yesterday_metrics()
    await send_email(to=OWNER_EMAIL, subject="Daily Digest", body=metrics)
    await post_to_slack(channel="#alerts", message=metrics.summary)
```

### Tier 3: Webhooks & Event-Driven
For reactive, trigger-based automation:
```
Stripe payment.succeeded webhook →
  → Create customer record in DB
  → Send welcome email (Resend)
  → Post to #new-customers Slack
  → Start 7-day onboarding sequence
  → Update MRR dashboard (internal)
```

### Automation Reliability Standards
- Every automation needs a failure notification path (email or Slack)
- Critical automations (billing, auth) need rollback procedures
- Log all automation runs with timestamp, input, output, status
- Test automations weekly with synthetic events (dead canary detection)

---

## 4. Monitoring & Alerting (3-Tier System)

### Tier 1: Uptime Monitoring (UptimeRobot or Betterstack)
- Check every 5 minutes
- Alert on: HTTP status ≠ 200, response time > 5s
- Notification: SMS + email to founder; Slack #alerts

### Tier 2: Error Rate Monitoring (Sentry)
- Alert on: Error spike > 3× baseline in 15 minutes
- Alert on: New error type (first occurrence)
- Weekly digest of top 5 errors by volume

### Tier 3: Business Metric Monitoring
| Metric | Alert threshold | Channel |
|--------|-----------------|---------|
| MRR drop | > 10% month-over-month | Email |
| Churn spike | > 2× monthly average in 7 days | Slack + Email |
| Signup rate drop | < 50% of 7-day average | Slack |
| Failed payments | > 5 in 24 hours | Email |
| Error rate | > 1% of requests | PagerDuty / SMS |

---

## 5. Autonomous Organization Design (MAKE)

### Three-Layer Org Structure
```
Layer 1: Robots (Automation)
  → Handles: repetitive, rule-based, predictable tasks
  → Tools: Zapier, cron jobs, webhooks, Stripe automations
  → Example: Email sequences, invoice generation, backups

Layer 2: Contractors (Humans on Demand)
  → Handles: judgment-required, output-based, time-limited tasks
  → Structure: clear deliverables, async communication, no supervision needed
  → Example: Customer support (Lemon.io), Content writing, Bug fixes

Layer 3: Founder (Strategic)
  → Handles: product direction, key relationships, pivots, fundraising
  → Target: max 20 hours/week on operations; rest on strategy
```

### Contractor Management Standards
**Before hiring:**
- Written SOP for every task they'll do (so you can evaluate quality)
- Clear deliverables with acceptance criteria
- Trial project: 2–4 hours paid, evaluate output quality

**Communication:**
- Async-first (Loom for context, Notion for SOPs, Linear/Trello for tasks)
- Weekly async check-in via Loom (5 min video > 30 min meeting)
- Escalation path defined: what decisions can contractor make vs. escalate?

**Contractor vs. FTE guideline:**
- < 20 hours/week per task: always contractor
- 20–40 hours/week, < 12 months: contractor
- > 40 hours/week, ongoing, strategic: FTE

---

## 6. Automation Quality Standards (Phase 11)

**Automation Audit Checklist:**
- [ ] All repetitive tasks catalogued with time-per-occurrence
- [ ] Automation ROI calculated for top 10 tasks (payback period)
- [ ] Bus Test score calculated (target ≥8/10)
- [ ] Critical automations have failure notifications
- [ ] Automation stack specified: no-code tools + cron jobs + webhooks
- [ ] Monitoring setup: 3-tier system implemented or planned
- [ ] Contractor vs. automation decision made for each non-automated task
- [ ] Autonomous org design: 3-layer structure documented

**Self-Assessment Block (add at top of automation output before saving):**
```markdown
---
**Automation Quality Check**
- Depth: [1–3] — [ROI calculated per task vs. generic list]
- Evidence: [1–3] — [Bus Test scored, time estimates provided]
- Specificity: [1–3] — [specific tools named, webhook events specified]
- Bus Test score: [X/10] — [target ≥8]
- Monitoring: [3-tier: complete/partial/missing]
- Unmet criteria: [list or "none"]
---
```
