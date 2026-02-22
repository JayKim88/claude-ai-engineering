# Monitoring & Alerting Setup: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Last Updated:** {{LAST_UPDATED}}
**Infrastructure:** {{INFRASTRUCTURE}}
**Owner:** {{OWNER_NAME}}

---

## Monitoring Philosophy

**Core Belief:** Everything breaks eventually. The goal is to detect fast, alert smart, and respond automatically where possible.

**Principles:**
1. **Monitor what matters**: Only alert on things that require action
2. **Expect things to break**: Design for graceful degradation, not perfection
3. **Alert fatigue is real**: Too many alerts = ignored alerts
4. **Automate recovery**: Robot fixes first, human intervention as last resort
5. **Data-driven decisions**: If you can't measure it, you can't improve it

**Alerting Hierarchy:**
- **Level 1 (Auto-Fix):** Robot attempts automated recovery
- **Level 2 (Contractor):** Human intervention required, non-urgent
- **Level 3 (Owner):** Strategic decision or emergency requiring owner attention
- **Level 4 (Emergency):** Business-critical outage, SMS/call owner

---

## Uptime Monitoring

### External Endpoints to Monitor

| Endpoint | Type | Expected Response | Check Frequency | Alert Threshold |
|----------|------|------------------|----------------|----------------|
| {{ENDPOINT_1}} | {{TYPE_1}} | {{RESPONSE_1}} | {{FREQ_1}} | {{THRESHOLD_1}} |
| {{ENDPOINT_2}} | {{TYPE_2}} | {{RESPONSE_2}} | {{FREQ_2}} | {{THRESHOLD_2}} |
| {{ENDPOINT_3}} | {{TYPE_3}} | {{RESPONSE_3}} | {{FREQ_3}} | {{THRESHOLD_3}} |
| {{ENDPOINT_4}} | {{TYPE_4}} | {{RESPONSE_4}} | {{FREQ_4}} | {{THRESHOLD_4}} |
| {{ENDPOINT_5}} | {{TYPE_5}} | {{RESPONSE_5}} | {{FREQ_5}} | {{THRESHOLD_5}} |
| {{ENDPOINT_6}} | {{TYPE_6}} | {{RESPONSE_6}} | {{FREQ_6}} | {{THRESHOLD_6}} |

**Check Types:**
- **HTTP/HTTPS**: Status code, response time, content match
- **API**: JSON response validation, specific field values
- **Database**: Connection test, query execution time
- **DNS**: Resolution time, correct IP
- **SSL/TLS**: Certificate expiration (alert 30 days before)

### Uptime Targets

**Overall Uptime SLA:** {{UPTIME_SLA}}%

**Acceptable Downtime:**
- **Monthly:** {{MONTHLY_DOWNTIME_BUDGET}} minutes
- **Quarterly:** {{QUARTERLY_DOWNTIME_BUDGET}} minutes
- **Annually:** {{ANNUAL_DOWNTIME_BUDGET}} hours

**Planned Maintenance Windows:**
{{MAINTENANCE_WINDOWS}}

### Auto-Recovery Actions

**On Endpoint Failure:**
1. **Retry:** {{RETRY_COUNT}} times with {{RETRY_DELAY}} second delay
2. **If still failing:** {{AUTO_RECOVERY_ACTION_1}}
3. **If recovery fails:** {{AUTO_RECOVERY_ACTION_2}}
4. **Alert contractor** if not recovered within {{CONTRACTOR_ALERT_DELAY}} minutes

**Common Auto-Recovery Scenarios:**
| Failure Type | Auto-Recovery Action | Success Rate | Fallback |
|--------------|---------------------|--------------|----------|
| {{FAILURE_1}} | {{RECOVERY_1}} | {{SUCCESS_1}}% | {{FALLBACK_1}} |
| {{FAILURE_2}} | {{RECOVERY_2}} | {{SUCCESS_2}}% | {{FALLBACK_2}} |
| {{FAILURE_3}} | {{RECOVERY_3}} | {{SUCCESS_3}}% | {{FALLBACK_3}} |
| {{FAILURE_4}} | {{RECOVERY_4}} | {{SUCCESS_4}}% | {{FALLBACK_4}} |

---

## Performance Monitoring

### Application Performance Metrics

| Metric | Target | Warning Threshold | Critical Threshold | Current |
|--------|--------|------------------|-------------------|---------|
| Page Load Time (Homepage) | < {{PAGE_LOAD_TARGET}}ms | > {{PAGE_LOAD_WARNING}}ms | > {{PAGE_LOAD_CRITICAL}}ms | {{PAGE_LOAD_CURRENT}}ms |
| API Response Time (Avg) | < {{API_TARGET}}ms | > {{API_WARNING}}ms | > {{API_CRITICAL}}ms | {{API_CURRENT}}ms |
| API Response Time (P95) | < {{API_P95_TARGET}}ms | > {{API_P95_WARNING}}ms | > {{API_P95_CRITICAL}}ms | {{API_P95_CURRENT}}ms |
| Database Query Time (Avg) | < {{DB_TARGET}}ms | > {{DB_WARNING}}ms | > {{DB_CRITICAL}}ms | {{DB_CURRENT}}ms |
| Time to First Byte (TTFB) | < {{TTFB_TARGET}}ms | > {{TTFB_WARNING}}ms | > {{TTFB_CRITICAL}}ms | {{TTFB_CURRENT}}ms |
| Error Rate | < {{ERROR_TARGET}}% | > {{ERROR_WARNING}}% | > {{ERROR_CRITICAL}}% | {{ERROR_CURRENT}}% |

### Server Metrics

| Metric | Target | Warning | Critical | Auto-Action |
|--------|--------|---------|----------|-------------|
| CPU Usage | < {{CPU_TARGET}}% | > {{CPU_WARNING}}% | > {{CPU_CRITICAL}}% | {{CPU_ACTION}} |
| Memory Usage | < {{MEM_TARGET}}% | > {{MEM_WARNING}}% | > {{MEM_CRITICAL}}% | {{MEM_ACTION}} |
| Disk Usage | < {{DISK_TARGET}}% | > {{DISK_WARNING}}% | > {{DISK_CRITICAL}}% | {{DISK_ACTION}} |
| Network I/O | < {{NETWORK_TARGET}} Mbps | > {{NETWORK_WARNING}} Mbps | > {{NETWORK_CRITICAL}} Mbps | {{NETWORK_ACTION}} |
| Open Connections | < {{CONN_TARGET}} | > {{CONN_WARNING}} | > {{CONN_CRITICAL}} | {{CONN_ACTION}} |

### Performance Optimization Triggers

**Alert Owner When:**
- Average response time increases by >{{RESPONSE_TIME_INCREASE}}% for {{RESPONSE_TIME_DURATION}} consecutive hours
- Error rate exceeds {{ERROR_RATE_THRESHOLD}}% for {{ERROR_DURATION}} minutes
- Server costs increase by >{{COST_INCREASE_THRESHOLD}}% month-over-month without revenue increase
- Database queries exceed {{DB_SLOW_QUERY_THRESHOLD}}ms on >{{DB_SLOW_QUERY_COUNT}} queries/day

---

## Business Logic Monitoring

### Revenue Monitoring

**Daily Revenue Checks:**
- **Expected Daily Revenue Range:** ${{MIN_DAILY_REVENUE}} - ${{MAX_DAILY_REVENUE}}
- **Alert if:** Daily revenue < ${{REVENUE_ALERT_THRESHOLD}} or > ${{REVENUE_SPIKE_THRESHOLD}}
- **Weekly Revenue Target:** ${{WEEKLY_REVENUE_TARGET}}
- **Alert if:** Week-to-date revenue is <{{WTD_REVENUE_THRESHOLD}}% of target by Thursday

**Payment Processing Anomalies:**
- Payment failure rate > {{PAYMENT_FAILURE_THRESHOLD}}% (normal: {{NORMAL_PAYMENT_FAILURE}}%)
- Refund rate > {{REFUND_THRESHOLD}}% (normal: {{NORMAL_REFUND}}%)
- Average transaction value changes by >{{TRANSACTION_VALUE_CHANGE}}% without explanation

### User Activity Monitoring

| Metric | Normal Range | Alert Threshold | Action |
|--------|--------------|----------------|--------|
| Daily Active Users | {{DAU_MIN}} - {{DAU_MAX}} | < {{DAU_ALERT}} or > {{DAU_SPIKE}} | {{DAU_ACTION}} |
| Sign-ups per Day | {{SIGNUP_MIN}} - {{SIGNUP_MAX}} | < {{SIGNUP_ALERT}} | {{SIGNUP_ACTION}} |
| Churn Rate (Monthly) | {{CHURN_MIN}}% - {{CHURN_MAX}}% | > {{CHURN_ALERT}}% | {{CHURN_ACTION}} |
| Conversion Rate | {{CONV_MIN}}% - {{CONV_MAX}}% | < {{CONV_ALERT}}% | {{CONV_ACTION}} |
| Support Tickets/Day | {{TICKET_MIN}} - {{TICKET_MAX}} | > {{TICKET_ALERT}} | {{TICKET_ACTION}} |

### Expected Values Testing

**Automated Sanity Checks:**

```python
# Example: Daily at midnight
def business_logic_checks():
    # Check 1: User count should never decrease dramatically
    assert today_user_count > yesterday_user_count * {{USER_COUNT_MIN_RATIO}}

    # Check 2: Revenue should be within reasonable bounds
    assert {{MIN_DAILY_REVENUE}} <= today_revenue <= {{MAX_DAILY_REVENUE}}

    # Check 3: API usage should match active users
    assert api_calls_today > active_users_today * {{API_CALLS_PER_USER_MIN}}

    # Check 4: Database growth should be predictable
    assert db_growth_today < {{MAX_DB_GROWTH_MB}} MB

    # Check 5: No user should have impossible values
    assert max_user_balance < {{MAX_REASONABLE_BALANCE}}
```

**Alert if Any Check Fails:**
{{BUSINESS_LOGIC_ALERT_PROTOCOL}}

---

## Alert Channels

### Channel Configuration

| Channel | Use Case | Recipients | Noise Level | Response SLA |
|---------|----------|-----------|-------------|--------------|
| SMS | Critical outages only | {{SMS_RECIPIENTS}} | Very Low | Immediate |
| Phone Call | Business-threatening emergencies | {{PHONE_RECIPIENTS}} | Extremely Low | Immediate |
| Email | Important but not urgent | {{EMAIL_RECIPIENTS}} | Medium | {{EMAIL_SLA}} |
| Slack | Warnings and FYI | {{SLACK_CHANNEL}} | High | {{SLACK_SLA}} |
| Dashboard | All metrics (no noise) | Owner/Contractors | N/A | As needed |

### Alert Routing Rules

**SMS Alerts (Level 4: Emergency):**
- {{SMS_RULE_1}}
- {{SMS_RULE_2}}
- {{SMS_RULE_3}}

**Email Alerts (Level 3: Owner):**
- {{EMAIL_RULE_1}}
- {{EMAIL_RULE_2}}
- {{EMAIL_RULE_3}}
- {{EMAIL_RULE_4}}

**Slack Alerts (Level 2: Contractor):**
- {{SLACK_RULE_1}}
- {{SLACK_RULE_2}}
- {{SLACK_RULE_3}}
- {{SLACK_RULE_4}}

**Dashboard Only (Level 1: Auto-Handled):**
- {{DASHBOARD_RULE_1}}
- {{DASHBOARD_RULE_2}}
- {{DASHBOARD_RULE_3}}

### Alert Message Templates

**SMS Template (Critical):**
```
[CRITICAL] {{PROJECT_NAME}}
{{ISSUE_SUMMARY}}
Impact: {{IMPACT_DESCRIPTION}}
Action: {{REQUIRED_ACTION}}
Dashboard: {{DASHBOARD_URL}}
```

**Email Template (Important):**
```
Subject: [{{SEVERITY}}] {{PROJECT_NAME}}: {{ISSUE_TITLE}}

Issue: {{ISSUE_DESCRIPTION}}
Detected: {{DETECTION_TIME}}
Current Status: {{CURRENT_STATUS}}
Impact: {{IMPACT_ASSESSMENT}}

Auto-Recovery Attempted: {{AUTO_RECOVERY_STATUS}}
Recommended Action: {{RECOMMENDED_ACTION}}

Dashboard: {{DASHBOARD_URL}}
Runbook: {{RUNBOOK_URL}}
```

**Slack Template (Warning):**
```
⚠️ {{ISSUE_TITLE}}
📊 Metric: {{METRIC_NAME}} = {{METRIC_VALUE}} (threshold: {{THRESHOLD}})
🕐 Detected: {{DETECTION_TIME}}
🔧 Auto-action: {{AUTO_ACTION}}
📈 Trend: {{TREND_ANALYSIS}}
```

---

## Alert Escalation

### Escalation Levels

**Level 1: Robot Auto-Fix (No Human Alert)**
- **Scope:** {{L1_SCOPE}}
- **Examples:** {{L1_EXAMPLES}}
- **Success Rate:** {{L1_SUCCESS_RATE}}%
- **Average Resolution Time:** {{L1_AVG_TIME}}

**Level 2: Contractor Notification (Slack/Email)**
- **Trigger:** {{L2_TRIGGER}}
- **Response SLA:** {{L2_SLA}}
- **Resolution Authority:** {{L2_AUTHORITY}}
- **Escalate to L3 if:** {{L2_ESCALATION_CRITERIA}}

**Level 3: Owner Alert (Email)**
- **Trigger:** {{L3_TRIGGER}}
- **Response SLA:** {{L3_SLA}}
- **Decision Required:** {{L3_DECISION_TYPE}}
- **Escalate to L4 if:** {{L3_ESCALATION_CRITERIA}}

**Level 4: Owner Emergency (SMS/Call)**
- **Trigger:** {{L4_TRIGGER}}
- **Response SLA:** Immediate
- **Examples:** {{L4_EXAMPLES}}

### Escalation Timing

**Auto-Escalation Rules:**
- L1 → L2: After {{L1_TO_L2_TIME}} minutes of failed auto-recovery
- L2 → L3: After {{L2_TO_L3_TIME}} hours with no contractor resolution
- L3 → L4: After {{L3_TO_L4_TIME}} minutes with no owner response OR if revenue impact exceeds ${{REVENUE_IMPACT_L4}}

**De-escalation:**
- Once resolved, send all-clear notification to same channels
- Post-incident report (for L3/L4) within {{POSTMORTEM_SLA}} hours

---

## Dashboard Design

### Primary Dashboard (Owner View)

**URL:** {{DASHBOARD_URL}}

**Sections:**
1. **Health Overview (Top)**
   - Current uptime status (green/yellow/red)
   - Open alerts count
   - Active users (last 24h)
   - Revenue (last 24h, last 7d, last 30d)

2. **Key Metrics (Middle)**
   - {{DASHBOARD_METRIC_1}}: {{METRIC_1_VISUALIZATION}}
   - {{DASHBOARD_METRIC_2}}: {{METRIC_2_VISUALIZATION}}
   - {{DASHBOARD_METRIC_3}}: {{METRIC_3_VISUALIZATION}}
   - {{DASHBOARD_METRIC_4}}: {{METRIC_4_VISUALIZATION}}
   - {{DASHBOARD_METRIC_5}}: {{METRIC_5_VISUALIZATION}}

3. **Alerts & Incidents (Bottom)**
   - Recent alerts (last 7 days)
   - Incident response times
   - Auto-recovery success rate

**Refresh Frequency:** {{DASHBOARD_REFRESH_FREQUENCY}}

**Mobile Accessible:** {{MOBILE_ACCESSIBLE}}

### Technical Dashboard (Contractor View)

**URL:** {{TECH_DASHBOARD_URL}}

**Sections:**
1. System Performance (CPU, Memory, Disk, Network)
2. Application Performance (Response times, error rates)
3. Database Metrics (Query times, connection pool)
4. External Dependencies Status (APIs, third-party services)
5. Recent Logs (errors, warnings)

**Refresh Frequency:** {{TECH_DASHBOARD_REFRESH}}

### Business Dashboard (High-Level)

**URL:** {{BUSINESS_DASHBOARD_URL}}

**Sections:**
1. Revenue Metrics (MRR, ARR, growth rate)
2. User Metrics (DAU, MAU, churn, LTV)
3. Unit Economics (CAC, LTV/CAC ratio)
4. Conversion Funnel
5. Top Customers

**Refresh Frequency:** {{BUSINESS_DASHBOARD_REFRESH}}

---

## Incident Response Playbook

### Detect

**How Incidents Are Detected:**
1. Automated monitoring alerts ({{DETECT_AUTO_PCT}}% of incidents)
2. Customer reports ({{DETECT_CUSTOMER_PCT}}% of incidents)
3. Contractor proactive checks ({{DETECT_CONTRACTOR_PCT}}% of incidents)

**Alert Contains:**
- Issue description
- Severity level
- Impact assessment
- Auto-recovery status
- Recommended next steps
- Relevant dashboard link

### Assess

**Assessment Checklist (Contractor):**
- [ ] Confirm issue is real (not false positive)
- [ ] Determine scope (how many users affected?)
- [ ] Estimate impact (revenue, reputation, data)
- [ ] Check if auto-recovery is working
- [ ] Identify root cause hypothesis
- [ ] Determine if escalation needed

**Assessment Time Target:** <{{ASSESS_TIME_TARGET}} minutes

### Respond

**Response Framework:**
1. **Acknowledge:** Confirm receipt of alert within {{ACK_SLA}}
2. **Communicate:** Update status page if customer-facing
3. **Mitigate:** Apply immediate fix (even if temporary)
4. **Resolve:** Implement permanent fix
5. **Verify:** Confirm issue is fully resolved
6. **Document:** Log in incident tracker

**Response Time Targets:**
- **Critical:** {{RESPONSE_CRITICAL}} minutes
- **High:** {{RESPONSE_HIGH}} hours
- **Medium:** {{RESPONSE_MEDIUM}} hours
- **Low:** {{RESPONSE_LOW}} hours

### Postmortem

**Required for:** All Level 3 and Level 4 incidents

**Postmortem Template:**
```markdown
# Incident Postmortem: {{INCIDENT_TITLE}}

**Date:** {{INCIDENT_DATE}}
**Duration:** {{INCIDENT_DURATION}}
**Severity:** {{INCIDENT_SEVERITY}}
**Impact:** {{INCIDENT_IMPACT}}

## Timeline
- {{TIMELINE_ENTRY_1}}
- {{TIMELINE_ENTRY_2}}
- {{TIMELINE_ENTRY_3}}

## Root Cause
{{ROOT_CAUSE_ANALYSIS}}

## Resolution
{{RESOLUTION_DESCRIPTION}}

## What Went Well
- {{WENT_WELL_1}}
- {{WENT_WELL_2}}

## What Went Wrong
- {{WENT_WRONG_1}}
- {{WENT_WRONG_2}}

## Action Items
- [ ] {{ACTION_ITEM_1}} (Owner: {{OWNER_1}}, Due: {{DUE_1}})
- [ ] {{ACTION_ITEM_2}} (Owner: {{OWNER_2}}, Due: {{DUE_2}})
- [ ] {{ACTION_ITEM_3}} (Owner: {{OWNER_3}}, Due: {{DUE_3}})
```

**Postmortem SLA:** Within {{POSTMORTEM_SLA}} of incident resolution

---

## Tools Stack

### Recommended Tools

| Category | Tool | Purpose | Cost | Integration |
|----------|------|---------|------|-------------|
| Uptime Monitoring | {{UPTIME_TOOL}} | External endpoint checks | {{UPTIME_COST}} | {{UPTIME_INTEGRATION}} |
| APM | {{APM_TOOL}} | Application performance | {{APM_COST}} | {{APM_INTEGRATION}} |
| Error Tracking | {{ERROR_TOOL}} | Exception logging | {{ERROR_COST}} | {{ERROR_INTEGRATION}} |
| Logs | {{LOG_TOOL}} | Centralized logging | {{LOG_COST}} | {{LOG_INTEGRATION}} |
| Metrics | {{METRICS_TOOL}} | Custom metrics & dashboards | {{METRICS_COST}} | {{METRICS_INTEGRATION}} |
| Alerts | {{ALERT_TOOL}} | Alert routing & escalation | {{ALERT_COST}} | {{ALERT_INTEGRATION}} |
| Status Page | {{STATUS_TOOL}} | Public status communication | {{STATUS_COST}} | {{STATUS_INTEGRATION}} |

**Total Monthly Cost:** {{TOTAL_MONITORING_COST}}

### Current Implementation

**Monitoring Stack:**
- **Uptime:** {{CURRENT_UPTIME_TOOL}}
- **APM:** {{CURRENT_APM_TOOL}}
- **Errors:** {{CURRENT_ERROR_TOOL}}
- **Logs:** {{CURRENT_LOG_TOOL}}
- **Dashboards:** {{CURRENT_DASHBOARD_TOOL}}
- **Alerts:** {{CURRENT_ALERT_TOOL}}

**Integration Points:**
{{INTEGRATION_DESCRIPTION}}

---

## Maintenance & Review

### Weekly Monitoring Review (Contractor)

- [ ] Check false positive rate (<{{FALSE_POSITIVE_TARGET}}% target)
- [ ] Review alert response times
- [ ] Verify all dashboards are working
- [ ] Check auto-recovery success rate
- [ ] Update alert thresholds if needed

### Monthly Monitoring Review (Owner)

- [ ] Review incident frequency and severity trends
- [ ] Assess monitoring coverage (are we missing anything?)
- [ ] Review monitoring costs vs value
- [ ] Update escalation procedures if needed
- [ ] Review and tune alert thresholds

### Quarterly Monitoring Audit

- [ ] Full review of all monitors (are they still relevant?)
- [ ] Test all escalation paths
- [ ] Review postmortems for systemic issues
- [ ] Benchmark against industry standards
- [ ] Plan monitoring improvements for next quarter
