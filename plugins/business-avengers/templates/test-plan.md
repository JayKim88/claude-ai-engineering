# Test Plan: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Date:** {{DATE}}
**QA Lead:** {{QA_LEAD}}

---

## Test Strategy

{{TEST_STRATEGY_OVERVIEW}}

**Testing Pyramid:**
- Unit Tests: {{UNIT_TEST_PERCENTAGE}}%
- Integration Tests: {{INTEGRATION_TEST_PERCENTAGE}}%
- E2E Tests: {{E2E_TEST_PERCENTAGE}}%

---

## Test Types

### Unit Testing

**Framework:** {{UNIT_TEST_FRAMEWORK}}
**Coverage Target:** {{UNIT_COVERAGE_TARGET}}%
**Scope:** {{UNIT_SCOPE}}

**Example:**
```javascript
{{UNIT_TEST_EXAMPLE}}
```

---

### Integration Testing

**Framework:** {{INTEGRATION_TEST_FRAMEWORK}}
**Coverage Target:** {{INTEGRATION_COVERAGE_TARGET}}%
**Scope:** {{INTEGRATION_SCOPE}}

---

### End-to-End Testing

**Framework:** {{E2E_TEST_FRAMEWORK}}
**Coverage Target:** {{E2E_COVERAGE_TARGET}}%
**Scope:** {{E2E_SCOPE}}

---

## Test Coverage Goals

| Component | Unit | Integration | E2E | Priority |
|-----------|------|-------------|-----|----------|
| {{COMP_1}} | {{COMP_1_UNIT}}% | {{COMP_1_INT}}% | {{COMP_1_E2E}}% | {{COMP_1_PRIORITY}} |
| {{COMP_2}} | {{COMP_2_UNIT}}% | {{COMP_2_INT}}% | {{COMP_2_E2E}}% | {{COMP_2_PRIORITY}} |
| {{COMP_3}} | {{COMP_3_UNIT}}% | {{COMP_3_INT}}% | {{COMP_3_E2E}}% | {{COMP_3_PRIORITY}} |
| {{COMP_4}} | {{COMP_4_UNIT}}% | {{COMP_4_INT}}% | {{COMP_4_E2E}}% | {{COMP_4_PRIORITY}} |

---

## Critical Paths

### Path 1: {{CRITICAL_PATH_1}}

**Steps:**
1. {{PATH_1_STEP_1}}
2. {{PATH_1_STEP_2}}
3. {{PATH_1_STEP_3}}

**Expected Result:** {{PATH_1_EXPECTED}}

---

### Path 2: {{CRITICAL_PATH_2}}

**Steps:**
1. {{PATH_2_STEP_1}}
2. {{PATH_2_STEP_2}}
3. {{PATH_2_STEP_3}}

**Expected Result:** {{PATH_2_EXPECTED}}

---

## Test Environment

**Environment URL:** {{TEST_ENV_URL}}
**Test Data:** {{TEST_DATA_SOURCE}}
**Tools:** {{TEST_TOOLS}}

---

## Tools & Frameworks

| Tool | Type | Purpose | Version |
|------|------|---------|---------|
| {{TOOL_1}} | {{TOOL_1_TYPE}} | {{TOOL_1_PURPOSE}} | {{TOOL_1_VER}} |
| {{TOOL_2}} | {{TOOL_2_TYPE}} | {{TOOL_2_PURPOSE}} | {{TOOL_2_VER}} |
| {{TOOL_3}} | {{TOOL_3_TYPE}} | {{TOOL_3_PURPOSE}} | {{TOOL_3_VER}} |

---

## Test Data Strategy

**Data Generation:** {{DATA_GENERATION_METHOD}}
**Data Reset:** {{DATA_RESET_METHOD}}
**Sensitive Data:** {{SENSITIVE_DATA_HANDLING}}
