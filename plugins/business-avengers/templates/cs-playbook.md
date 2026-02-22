# Customer Success Playbook: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Date:** {{DATE}}
**CS Lead:** {{CS_LEAD}}

---

## CS Philosophy

{{CS_PHILOSOPHY}}

**Mission:** {{CS_MISSION}}

**Core Values:**
1. {{CS_VALUE_1}}
2. {{CS_VALUE_2}}
3. {{CS_VALUE_3}}

---

## Response Time SLAs

| Priority | First Response | Resolution Time | Channels |
|----------|----------------|-----------------|----------|
| Critical | {{CRITICAL_RESPONSE}} | {{CRITICAL_RESOLUTION}} | {{CRITICAL_CHANNELS}} |
| High | {{HIGH_RESPONSE}} | {{HIGH_RESOLUTION}} | {{HIGH_CHANNELS}} |
| Medium | {{MEDIUM_RESPONSE}} | {{MEDIUM_RESOLUTION}} | {{MEDIUM_CHANNELS}} |
| Low | {{LOW_RESPONSE}} | {{LOW_RESOLUTION}} | {{LOW_CHANNELS}} |

---

## Ticket Categories

### Category 1: {{CATEGORY_1}}

**Priority:** {{CAT_1_PRIORITY}}
**Common Issues:**
- {{CAT_1_ISSUE_1}}
- {{CAT_1_ISSUE_2}}
- {{CAT_1_ISSUE_3}}

**Resolution Process:**
{{CAT_1_PROCESS}}

---

### Category 2: {{CATEGORY_2}}

**Priority:** {{CAT_2_PRIORITY}}
**Common Issues:**
- {{CAT_2_ISSUE_1}}
- {{CAT_2_ISSUE_2}}
- {{CAT_2_ISSUE_3}}

**Resolution Process:**
{{CAT_2_PROCESS}}

---

### Category 3: {{CATEGORY_3}}

**Priority:** {{CAT_3_PRIORITY}}
**Common Issues:**
- {{CAT_3_ISSUE_1}}
- {{CAT_3_ISSUE_2}}
- {{CAT_3_ISSUE_3}}

**Resolution Process:**
{{CAT_3_PROCESS}}

---

## Escalation Matrix

| Level | Role | Scenarios | Contact |
|-------|------|-----------|---------|
| L1 | {{L1_ROLE}} | {{L1_SCENARIOS}} | {{L1_CONTACT}} |
| L2 | {{L2_ROLE}} | {{L2_SCENARIOS}} | {{L2_CONTACT}} |
| L3 | {{L3_ROLE}} | {{L3_SCENARIOS}} | {{L3_CONTACT}} |
| Executive | {{L4_ROLE}} | {{L4_SCENARIOS}} | {{L4_CONTACT}} |

---

## FAQ Draft

### Getting Started

**Q: {{FAQ_1_Q}}**
A: {{FAQ_1_A}}

**Q: {{FAQ_2_Q}}**
A: {{FAQ_2_A}}

**Q: {{FAQ_3_Q}}**
A: {{FAQ_3_A}}

### Account Management

**Q: {{FAQ_4_Q}}**
A: {{FAQ_4_A}}

**Q: {{FAQ_5_Q}}**
A: {{FAQ_5_A}}

### Billing

**Q: {{FAQ_6_Q}}**
A: {{FAQ_6_A}}

**Q: {{FAQ_7_Q}}**
A: {{FAQ_7_A}}

### Troubleshooting

**Q: {{FAQ_8_Q}}**
A: {{FAQ_8_A}}

**Q: {{FAQ_9_Q}}**
A: {{FAQ_9_A}}

---

## Common Issues & Solutions

### Issue 1: {{ISSUE_1_NAME}}

**Symptoms:** {{ISSUE_1_SYMPTOMS}}

**Root Cause:** {{ISSUE_1_CAUSE}}

**Solution:**
1. {{ISSUE_1_STEP_1}}
2. {{ISSUE_1_STEP_2}}
3. {{ISSUE_1_STEP_3}}

**Prevention:** {{ISSUE_1_PREVENTION}}

---

### Issue 2: {{ISSUE_2_NAME}}

**Symptoms:** {{ISSUE_2_SYMPTOMS}}

**Root Cause:** {{ISSUE_2_CAUSE}}

**Solution:**
1. {{ISSUE_2_STEP_1}}
2. {{ISSUE_2_STEP_2}}
3. {{ISSUE_2_STEP_3}}

**Prevention:** {{ISSUE_2_PREVENTION}}

---

### Issue 3: {{ISSUE_3_NAME}}

**Symptoms:** {{ISSUE_3_SYMPTOMS}}

**Root Cause:** {{ISSUE_3_CAUSE}}

**Solution:**
1. {{ISSUE_3_STEP_1}}
2. {{ISSUE_3_STEP_2}}
3. {{ISSUE_3_STEP_3}}

**Prevention:** {{ISSUE_3_PREVENTION}}

---

## Feedback Collection

**Collection Methods:**
- {{FEEDBACK_METHOD_1}}
- {{FEEDBACK_METHOD_2}}
- {{FEEDBACK_METHOD_3}}

**Feedback Loop:**
{{FEEDBACK_LOOP_PROCESS}}

---

## CSAT/NPS Plan

**CSAT Survey:**
- Trigger: {{CSAT_TRIGGER}}
- Questions: {{CSAT_QUESTIONS}}
- Target Score: {{CSAT_TARGET}}

**NPS Survey:**
- Frequency: {{NPS_FREQUENCY}}
- Target Score: {{NPS_TARGET}}

**Follow-up Process:**
{{FOLLOWUP_PROCESS}}

---

## Customer Onboarding

**Onboarding Timeline:** {{ONBOARDING_TIMELINE}}

**Steps:**
1. {{ONBOARDING_STEP_1}}
2. {{ONBOARDING_STEP_2}}
3. {{ONBOARDING_STEP_3}}
4. {{ONBOARDING_STEP_4}}

**Success Criteria:**
{{ONBOARDING_SUCCESS}}

---

## Proactive Outreach

**Health Score Monitoring:**
{{HEALTH_SCORE_CRITERIA}}

**At-Risk Customers:**
{{AT_RISK_PROCESS}}

**Expansion Opportunities:**
{{EXPANSION_PROCESS}}

---

## Customer Self-Service Strategy (MAKE Methodology)

<!-- MAKE Principle: Automate customer support. 90%+ of CS requests can be handled by self-service. Scale without hiring. -->

### Self-Service Capabilities

| Action | Self-Service? | Implementation | Priority |
|--------|--------------|----------------|----------|
| Sign up / Create account | Yes | Auth system | Must-have |
| View billing history | Yes | Payment provider portal | Must-have |
| Change subscription plan | Yes | Payment provider portal | Must-have |
| Cancel subscription | Yes | Payment provider portal | Must-have |
| Request refund | Yes | Auto-refund within {{REFUND_WINDOW}} | Must-have |
| Update payment method | Yes | Payment provider portal | Must-have |
| Update profile / settings | Yes | User settings page | Must-have |
| View usage / limits | Yes | Dashboard | Should-have |
| Export personal data | Yes | GDPR compliance | Should-have |
| Delete account | Yes | Account deletion flow | Should-have |

**Estimated CS Reduction:** {{ESTIMATED_CS_REDUCTION}}%

### Remaining Human-Touch CS

| Scenario | Why Human Needed | Resolution SLA |
|----------|-----------------|----------------|
| {{HUMAN_CS_1}} | {{HUMAN_REASON_1}} | {{HUMAN_SLA_1}} |
| {{HUMAN_CS_2}} | {{HUMAN_REASON_2}} | {{HUMAN_SLA_2}} |
| {{HUMAN_CS_3}} | {{HUMAN_REASON_3}} | {{HUMAN_SLA_3}} |

---

## Basic Uptime Monitoring

<!-- Minimal monitoring for Phase 9. Full monitoring setup in Phase 11 (monitoring-setup.md). -->

**Recommended Tool:** UptimeRobot or equivalent (free tier available)

**Minimum Setup:**
- Site health check: Every 5 min → SMS + Email on failure
- API endpoint check: Every 5 min → Email on error rate > 5%
- Performance degradation: Daily digest via Slack/Email
