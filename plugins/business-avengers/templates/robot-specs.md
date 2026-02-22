# Robot Specifications: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Last Updated:** {{LAST_UPDATED}}
**Owner:** {{OWNER_NAME}}
**Infrastructure:** {{INFRASTRUCTURE_PLATFORM}}

---

## Robot Registry

<!-- Central index of all automation robots -->

| Robot ID | Name | Purpose | Schedule | Status | Last Run | Success Rate |
|----------|------|---------|----------|--------|----------|--------------|
| {{ROBOT_1_ID}} | {{ROBOT_1_NAME}} | {{ROBOT_1_PURPOSE}} | {{ROBOT_1_SCHEDULE}} | {{ROBOT_1_STATUS}} | {{ROBOT_1_LAST_RUN}} | {{ROBOT_1_SUCCESS_RATE}} |
| {{ROBOT_2_ID}} | {{ROBOT_2_NAME}} | {{ROBOT_2_PURPOSE}} | {{ROBOT_2_SCHEDULE}} | {{ROBOT_2_STATUS}} | {{ROBOT_2_LAST_RUN}} | {{ROBOT_2_SUCCESS_RATE}} |
| {{ROBOT_3_ID}} | {{ROBOT_3_NAME}} | {{ROBOT_3_PURPOSE}} | {{ROBOT_3_SCHEDULE}} | {{ROBOT_3_STATUS}} | {{ROBOT_3_LAST_RUN}} | {{ROBOT_3_SUCCESS_RATE}} |
| {{ROBOT_4_ID}} | {{ROBOT_4_NAME}} | {{ROBOT_4_PURPOSE}} | {{ROBOT_4_SCHEDULE}} | {{ROBOT_4_STATUS}} | {{ROBOT_4_LAST_RUN}} | {{ROBOT_4_SUCCESS_RATE}} |
| {{ROBOT_5_ID}} | {{ROBOT_5_NAME}} | {{ROBOT_5_PURPOSE}} | {{ROBOT_5_SCHEDULE}} | {{ROBOT_5_STATUS}} | {{ROBOT_5_LAST_RUN}} | {{ROBOT_5_SUCCESS_RATE}} |
| {{ROBOT_6_ID}} | {{ROBOT_6_NAME}} | {{ROBOT_6_PURPOSE}} | {{ROBOT_6_SCHEDULE}} | {{ROBOT_6_STATUS}} | {{ROBOT_6_LAST_RUN}} | {{ROBOT_6_SUCCESS_RATE}} |
| {{ROBOT_7_ID}} | {{ROBOT_7_NAME}} | {{ROBOT_7_PURPOSE}} | {{ROBOT_7_SCHEDULE}} | {{ROBOT_7_STATUS}} | {{ROBOT_7_LAST_RUN}} | {{ROBOT_7_SUCCESS_RATE}} |
| {{ROBOT_8_ID}} | {{ROBOT_8_NAME}} | {{ROBOT_8_PURPOSE}} | {{ROBOT_8_SCHEDULE}} | {{ROBOT_8_STATUS}} | {{ROBOT_8_LAST_RUN}} | {{ROBOT_8_SUCCESS_RATE}} |

**Status Legend:**
- **Active**: Running on schedule
- **Paused**: Temporarily disabled
- **Failed**: Last run failed, needs attention
- **Maintenance**: Being updated/debugged

---

## Robot 1: {{R1_NAME}}

### Purpose & Trigger

**Purpose:**
{{R1_PURPOSE_DETAILED}}

**Trigger Type:**
{{R1_TRIGGER_TYPE}}

**Trigger Conditions:**
{{R1_TRIGGER_CONDITIONS}}

### Input Sources

**Primary Data Source:**
- **Type:** {{R1_INPUT_1_TYPE}}
- **Location:** {{R1_INPUT_1_LOCATION}}
- **Authentication:** {{R1_INPUT_1_AUTH}}
- **Format:** {{R1_INPUT_1_FORMAT}}

**Secondary Data Source:**
- **Type:** {{R1_INPUT_2_TYPE}}
- **Location:** {{R1_INPUT_2_LOCATION}}
- **Authentication:** {{R1_INPUT_2_AUTH}}
- **Format:** {{R1_INPUT_2_FORMAT}}

**Additional Inputs:**
{{R1_ADDITIONAL_INPUTS}}

### Processing Logic

**Step 1: {{R1_STEP_1_NAME}}**
{{R1_STEP_1_DESCRIPTION}}

**Step 2: {{R1_STEP_2_NAME}}**
{{R1_STEP_2_DESCRIPTION}}

**Step 3: {{R1_STEP_3_NAME}}**
{{R1_STEP_3_DESCRIPTION}}

**Step 4: {{R1_STEP_4_NAME}}**
{{R1_STEP_4_DESCRIPTION}}

**Step 5: {{R1_STEP_5_NAME}}**
{{R1_STEP_5_DESCRIPTION}}

**Conditional Logic:**
```
If {{R1_CONDITION_1}}:
    {{R1_ACTION_1}}
Else if {{R1_CONDITION_2}}:
    {{R1_ACTION_2}}
Else:
    {{R1_ACTION_3}}
```

### Output/Actions

**Primary Output:**
- **Action Type:** {{R1_OUTPUT_1_TYPE}}
- **Destination:** {{R1_OUTPUT_1_DESTINATION}}
- **Format:** {{R1_OUTPUT_1_FORMAT}}

**Secondary Output:**
- **Action Type:** {{R1_OUTPUT_2_TYPE}}
- **Destination:** {{R1_OUTPUT_2_DESTINATION}}
- **Format:** {{R1_OUTPUT_2_FORMAT}}

**Success Notification:**
{{R1_SUCCESS_NOTIFICATION}}

### Schedule

**Cron Expression:**
```
{{R1_CRON_EXPRESSION}}
```

**Human-Readable:**
{{R1_SCHEDULE_HUMAN}}

**Timezone:**
{{R1_TIMEZONE}}

**Expected Execution Time:**
{{R1_EXPECTED_DURATION}}

### Error Handling

**Retry Logic:**
- **Max Retries:** {{R1_MAX_RETRIES}}
- **Retry Delay:** {{R1_RETRY_DELAY}}
- **Exponential Backoff:** {{R1_EXPONENTIAL_BACKOFF}}

**Fallback Actions:**
{{R1_FALLBACK_ACTIONS}}

**Alert on Failure:**
- **Channel:** {{R1_ALERT_CHANNEL}}
- **Recipients:** {{R1_ALERT_RECIPIENTS}}
- **Alert Threshold:** {{R1_ALERT_THRESHOLD}}

**Known Error Scenarios:**
| Error Type | Cause | Recovery Action |
|-----------|-------|----------------|
| {{R1_ERROR_1}} | {{R1_ERROR_1_CAUSE}} | {{R1_ERROR_1_RECOVERY}} |
| {{R1_ERROR_2}} | {{R1_ERROR_2_CAUSE}} | {{R1_ERROR_2_RECOVERY}} |
| {{R1_ERROR_3}} | {{R1_ERROR_3_CAUSE}} | {{R1_ERROR_3_RECOVERY}} |

### Monitoring

**Health Check:**
- **Endpoint:** {{R1_HEALTH_CHECK_ENDPOINT}}
- **Expected Response:** {{R1_HEALTH_CHECK_EXPECTED}}
- **Check Frequency:** {{R1_HEALTH_CHECK_FREQUENCY}}

**Output Validation:**
{{R1_OUTPUT_VALIDATION}}

**Performance Metrics:**
- Execution time (target: < {{R1_PERF_TARGET}})
- Success rate (target: > {{R1_SUCCESS_TARGET}}%)
- Error rate (target: < {{R1_ERROR_TARGET}}%)

**Dashboard Link:**
{{R1_DASHBOARD_LINK}}

---

## Robot 2: {{R2_NAME}}

### Purpose & Trigger

**Purpose:**
{{R2_PURPOSE_DETAILED}}

**Trigger Type:**
{{R2_TRIGGER_TYPE}}

**Trigger Conditions:**
{{R2_TRIGGER_CONDITIONS}}

### Input Sources

**Primary Data Source:**
- **Type:** {{R2_INPUT_1_TYPE}}
- **Location:** {{R2_INPUT_1_LOCATION}}
- **Authentication:** {{R2_INPUT_1_AUTH}}
- **Format:** {{R2_INPUT_1_FORMAT}}

**Secondary Data Source:**
- **Type:** {{R2_INPUT_2_TYPE}}
- **Location:** {{R2_INPUT_2_LOCATION}}
- **Authentication:** {{R2_INPUT_2_AUTH}}
- **Format:** {{R2_INPUT_2_FORMAT}}

**Additional Inputs:**
{{R2_ADDITIONAL_INPUTS}}

### Processing Logic

**Step 1: {{R2_STEP_1_NAME}}**
{{R2_STEP_1_DESCRIPTION}}

**Step 2: {{R2_STEP_2_NAME}}**
{{R2_STEP_2_DESCRIPTION}}

**Step 3: {{R2_STEP_3_NAME}}**
{{R2_STEP_3_DESCRIPTION}}

**Step 4: {{R2_STEP_4_NAME}}**
{{R2_STEP_4_DESCRIPTION}}

**Step 5: {{R2_STEP_5_NAME}}**
{{R2_STEP_5_DESCRIPTION}}

**Conditional Logic:**
```
If {{R2_CONDITION_1}}:
    {{R2_ACTION_1}}
Else if {{R2_CONDITION_2}}:
    {{R2_ACTION_2}}
Else:
    {{R2_ACTION_3}}
```

### Output/Actions

**Primary Output:**
- **Action Type:** {{R2_OUTPUT_1_TYPE}}
- **Destination:** {{R2_OUTPUT_1_DESTINATION}}
- **Format:** {{R2_OUTPUT_1_FORMAT}}

**Secondary Output:**
- **Action Type:** {{R2_OUTPUT_2_TYPE}}
- **Destination:** {{R2_OUTPUT_2_DESTINATION}}
- **Format:** {{R2_OUTPUT_2_FORMAT}}

**Success Notification:**
{{R2_SUCCESS_NOTIFICATION}}

### Schedule

**Cron Expression:**
```
{{R2_CRON_EXPRESSION}}
```

**Human-Readable:**
{{R2_SCHEDULE_HUMAN}}

**Timezone:**
{{R2_TIMEZONE}}

**Expected Execution Time:**
{{R2_EXPECTED_DURATION}}

### Error Handling

**Retry Logic:**
- **Max Retries:** {{R2_MAX_RETRIES}}
- **Retry Delay:** {{R2_RETRY_DELAY}}
- **Exponential Backoff:** {{R2_EXPONENTIAL_BACKOFF}}

**Fallback Actions:**
{{R2_FALLBACK_ACTIONS}}

**Alert on Failure:**
- **Channel:** {{R2_ALERT_CHANNEL}}
- **Recipients:** {{R2_ALERT_RECIPIENTS}}
- **Alert Threshold:** {{R2_ALERT_THRESHOLD}}

**Known Error Scenarios:**
| Error Type | Cause | Recovery Action |
|-----------|-------|----------------|
| {{R2_ERROR_1}} | {{R2_ERROR_1_CAUSE}} | {{R2_ERROR_1_RECOVERY}} |
| {{R2_ERROR_2}} | {{R2_ERROR_2_CAUSE}} | {{R2_ERROR_2_RECOVERY}} |
| {{R2_ERROR_3}} | {{R2_ERROR_3_CAUSE}} | {{R2_ERROR_3_RECOVERY}} |

### Monitoring

**Health Check:**
- **Endpoint:** {{R2_HEALTH_CHECK_ENDPOINT}}
- **Expected Response:** {{R2_HEALTH_CHECK_EXPECTED}}
- **Check Frequency:** {{R2_HEALTH_CHECK_FREQUENCY}}

**Output Validation:**
{{R2_OUTPUT_VALIDATION}}

**Performance Metrics:**
- Execution time (target: < {{R2_PERF_TARGET}})
- Success rate (target: > {{R2_SUCCESS_TARGET}}%)
- Error rate (target: < {{R2_ERROR_TARGET}}%)

**Dashboard Link:**
{{R2_DASHBOARD_LINK}}

---

## Robot 3: {{R3_NAME}}

### Purpose & Trigger

**Purpose:**
{{R3_PURPOSE_DETAILED}}

**Trigger Type:**
{{R3_TRIGGER_TYPE}}

**Trigger Conditions:**
{{R3_TRIGGER_CONDITIONS}}

### Input Sources

**Primary Data Source:**
- **Type:** {{R3_INPUT_1_TYPE}}
- **Location:** {{R3_INPUT_1_LOCATION}}
- **Authentication:** {{R3_INPUT_1_AUTH}}
- **Format:** {{R3_INPUT_1_FORMAT}}

**Secondary Data Source:**
- **Type:** {{R3_INPUT_2_TYPE}}
- **Location:** {{R3_INPUT_2_LOCATION}}
- **Authentication:** {{R3_INPUT_2_AUTH}}
- **Format:** {{R3_INPUT_2_FORMAT}}

### Processing Logic

**Step 1: {{R3_STEP_1_NAME}}**
{{R3_STEP_1_DESCRIPTION}}

**Step 2: {{R3_STEP_2_NAME}}**
{{R3_STEP_2_DESCRIPTION}}

**Step 3: {{R3_STEP_3_NAME}}**
{{R3_STEP_3_DESCRIPTION}}

**Step 4: {{R3_STEP_4_NAME}}**
{{R3_STEP_4_DESCRIPTION}}

### Output/Actions

**Primary Output:**
- **Action Type:** {{R3_OUTPUT_1_TYPE}}
- **Destination:** {{R3_OUTPUT_1_DESTINATION}}
- **Format:** {{R3_OUTPUT_1_FORMAT}}

### Schedule

**Cron Expression:**
```
{{R3_CRON_EXPRESSION}}
```

**Human-Readable:**
{{R3_SCHEDULE_HUMAN}}

### Error Handling

**Retry Logic:**
- **Max Retries:** {{R3_MAX_RETRIES}}
- **Retry Delay:** {{R3_RETRY_DELAY}}

**Alert on Failure:**
- **Channel:** {{R3_ALERT_CHANNEL}}
- **Recipients:** {{R3_ALERT_RECIPIENTS}}

### Monitoring

**Health Check:**
- **Endpoint:** {{R3_HEALTH_CHECK_ENDPOINT}}
- **Expected Response:** {{R3_HEALTH_CHECK_EXPECTED}}

**Performance Metrics:**
- Execution time (target: < {{R3_PERF_TARGET}})
- Success rate (target: > {{R3_SUCCESS_TARGET}}%)

---

## Dependencies

### External APIs

| API Name | Purpose | Authentication Method | Rate Limits | Fallback |
|----------|---------|----------------------|-------------|----------|
| {{API_1}} | {{API_1_PURPOSE}} | {{API_1_AUTH}} | {{API_1_LIMITS}} | {{API_1_FALLBACK}} |
| {{API_2}} | {{API_2_PURPOSE}} | {{API_2_AUTH}} | {{API_2_LIMITS}} | {{API_2_FALLBACK}} |
| {{API_3}} | {{API_3_PURPOSE}} | {{API_3_AUTH}} | {{API_3_LIMITS}} | {{API_3_FALLBACK}} |
| {{API_4}} | {{API_4_PURPOSE}} | {{API_4_AUTH}} | {{API_4_LIMITS}} | {{API_4_FALLBACK}} |

### Credentials & Secrets

**Secrets Manager:**
{{SECRETS_MANAGER_PLATFORM}}

**Required Secrets:**
- {{SECRET_1}}
- {{SECRET_2}}
- {{SECRET_3}}
- {{SECRET_4}}
- {{SECRET_5}}

**Rotation Policy:**
{{SECRET_ROTATION_POLICY}}

### External Services

| Service Name | Purpose | Criticality | Uptime SLA | Contact |
|--------------|---------|-------------|-----------|---------|
| {{SERVICE_1}} | {{SERVICE_1_PURPOSE}} | {{SERVICE_1_CRITICAL}} | {{SERVICE_1_SLA}} | {{SERVICE_1_CONTACT}} |
| {{SERVICE_2}} | {{SERVICE_2_PURPOSE}} | {{SERVICE_2_CRITICAL}} | {{SERVICE_2_SLA}} | {{SERVICE_2_CONTACT}} |
| {{SERVICE_3}} | {{SERVICE_3_PURPOSE}} | {{SERVICE_3_CRITICAL}} | {{SERVICE_3_SLA}} | {{SERVICE_3_CONTACT}} |

---

## Deployment

### Infrastructure

**Hosting Platform:**
{{HOSTING_PLATFORM}}

**Server Specifications:**
- **CPU:** {{SERVER_CPU}}
- **RAM:** {{SERVER_RAM}}
- **Storage:** {{SERVER_STORAGE}}
- **Region:** {{SERVER_REGION}}

**Operating System:**
{{SERVER_OS}}

**Runtime Environment:**
{{RUNTIME_ENVIRONMENT}}

### Code Repository

**Repository URL:**
{{REPO_URL}}

**Branch Strategy:**
- **Production:** {{PROD_BRANCH}}
- **Staging:** {{STAGING_BRANCH}}
- **Development:** {{DEV_BRANCH}}

**Deployment Method:**
{{DEPLOYMENT_METHOD}}

### Environment Variables

```bash
# Required environment variables
{{ENV_VAR_1}}={{ENV_VAR_1_VALUE}}
{{ENV_VAR_2}}={{ENV_VAR_2_VALUE}}
{{ENV_VAR_3}}={{ENV_VAR_3_VALUE}}
{{ENV_VAR_4}}={{ENV_VAR_4_VALUE}}
{{ENV_VAR_5}}={{ENV_VAR_5_VALUE}}
```

### Deployment Checklist

- [ ] Code pushed to repository
- [ ] Environment variables configured
- [ ] Secrets uploaded to secrets manager
- [ ] Dependencies installed
- [ ] Database migrations run (if applicable)
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Alerts configured
- [ ] Documentation updated
- [ ] Rollback plan tested

---

## Maintenance

### Regular Maintenance Tasks

**Weekly:**
- [ ] {{WEEKLY_TASK_1}}
- [ ] {{WEEKLY_TASK_2}}
- [ ] {{WEEKLY_TASK_3}}

**Monthly:**
- [ ] {{MONTHLY_TASK_1}}
- [ ] {{MONTHLY_TASK_2}}
- [ ] {{MONTHLY_TASK_3}}

**Quarterly:**
- [ ] {{QUARTERLY_TASK_1}}
- [ ] {{QUARTERLY_TASK_2}}
- [ ] {{QUARTERLY_TASK_3}}

### Update Procedures

**Updating a Robot:**
1. {{UPDATE_STEP_1}}
2. {{UPDATE_STEP_2}}
3. {{UPDATE_STEP_3}}
4. {{UPDATE_STEP_4}}
5. {{UPDATE_STEP_5}}

**Rollback Procedure:**
1. {{ROLLBACK_STEP_1}}
2. {{ROLLBACK_STEP_2}}
3. {{ROLLBACK_STEP_3}}

### Incident Response

**On Robot Failure:**
1. {{INCIDENT_STEP_1}}
2. {{INCIDENT_STEP_2}}
3. {{INCIDENT_STEP_3}}
4. {{INCIDENT_STEP_4}}

**Escalation Path:**
- **Level 1:** {{ESCALATION_L1}} (auto-fix attempt)
- **Level 2:** {{ESCALATION_L2}} (contractor notified)
- **Level 3:** {{ESCALATION_L3}} (owner SMS alert)
