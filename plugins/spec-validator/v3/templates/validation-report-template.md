# Spec Validation Report

> **Generated**: [TIMESTAMP]
> **Mode**: [VALIDATION_MODE]
> **Spec**: [SPEC_PATH]
> **Checklist**: [CHECKLIST_PATH]

---

## Executive Summary

**Overall Score**: [OVERALL_SCORE]/100 (**Grade [GRADE]**)

[GRADE_DESCRIPTION]

[PREVIOUS_SCORE_SECTION - Include if has_previous_validation is true:
**Previous Score**: [PREVIOUS_SCORE]/100 ([SCORE_DELTA])
**Trend**: [TREND_INDICATOR] [TREND_LABEL]
]

**Validation Mode**: [VALIDATION_MODE]
- **Duration**: ~[ESTIMATED_DURATION]
- **Dimensions Evaluated**: [DIMENSIONS_EVALUATED]

---

## Dimension Scores

| Dimension | Score | Max | Percentage | Status |
|-----------|-------|-----|------------|--------|
| Implementation Completeness | [COMPLETENESS_SCORE] | [COMPLETENESS_MAX] | [COMPLETENESS_PERCENTAGE]% | [COMPLETENESS_STATUS] |
| Implementation Quality | [QUALITY_SCORE] | [QUALITY_MAX] | [QUALITY_PERCENTAGE]% | [QUALITY_STATUS] |
| Spec Adherence | [ADHERENCE_SCORE] | [ADHERENCE_MAX] | [ADHERENCE_PERCENTAGE]% | [ADHERENCE_STATUS] |
| Progress Transparency | [TRANSPARENCY_SCORE] | [TRANSPARENCY_MAX] | [TRANSPARENCY_PERCENTAGE]% | [TRANSPARENCY_STATUS] |
| **Total** | **[OVERALL_SCORE]** | **[TOTAL_MAX]** | **[OVERALL_PERCENTAGE]%** | **[OVERALL_STATUS]** |

### Dimension Breakdown

#### 1. Implementation Completeness ([COMPLETENESS_SCORE]/[COMPLETENESS_MAX] points)

| Category | Completed | Total | Percentage | Points | Max Points |
|----------|-----------|-------|------------|--------|------------|
| Functional Requirements | [FR_COMPLETED] | [FR_TOTAL] | [FR_PERCENTAGE]% | [FR_POINTS] | [FR_MAX_POINTS] |
| - High Priority | [FR_HIGH_COMPLETED] | [FR_HIGH_TOTAL] | [FR_HIGH_PERCENTAGE]% | - | - |
| - Medium Priority | [FR_MEDIUM_COMPLETED] | [FR_MEDIUM_TOTAL] | [FR_MEDIUM_PERCENTAGE]% | - | - |
| - Low Priority | [FR_LOW_COMPLETED] | [FR_LOW_TOTAL] | [FR_LOW_PERCENTAGE]% | - | - |
| Non-Functional Requirements | [NFR_COMPLETED] | [NFR_TOTAL] | [NFR_PERCENTAGE]% | [NFR_POINTS] | [NFR_MAX_POINTS] |
| Data Models | [MODELS_COMPLETED] | [MODELS_TOTAL] | [MODELS_PERCENTAGE]% | [MODELS_POINTS] | [MODELS_MAX_POINTS] |
| API Endpoints | [APIS_COMPLETED] | [APIS_TOTAL] | [APIS_PERCENTAGE]% | [APIS_POINTS] | [APIS_MAX_POINTS] |

#### 2. Implementation Quality ([QUALITY_SCORE]/[QUALITY_MAX] points)

| Category | Score | Max Points | Details |
|----------|-------|------------|---------|
| Test Coverage | [TEST_COVERAGE_SCORE] | [TEST_COVERAGE_MAX] | [TESTS_COMPLETED]/[REQUIREMENTS_TOTAL] requirements tested ([TEST_PERCENTAGE]%) |
| Edge Case Coverage | [EDGE_CASE_SCORE] | [EDGE_CASE_MAX] | [EDGE_CASES_HANDLED]/[EDGE_CASES_TOTAL] edge cases handled ([EDGE_CASE_PERCENTAGE]%) |
| Implementation Notes | [NOTES_SCORE] | [NOTES_MAX] | [ITEMS_WITH_NOTES]/[TOTAL_ITEMS] items documented ([NOTES_PERCENTAGE]%) |

#### 3. Spec Adherence ([ADHERENCE_SCORE]/[ADHERENCE_MAX] points)

| Category | Score | Max Points | Details |
|----------|-------|------------|---------|
| Synchronization | [SYNC_SCORE] | [SYNC_MAX] | [ORPHANED_COUNT] orphaned, [MISSING_COUNT] missing items |
| Priority Accuracy | [PRIORITY_SCORE] | [PRIORITY_MAX] | [PRIORITY_MISMATCHES] priority mismatches |
| Structure Compliance | [STRUCTURE_SCORE] | [STRUCTURE_MAX] | YAML structure [STRUCTURE_STATUS] |

#### 4. Progress Transparency ([TRANSPARENCY_SCORE]/[TRANSPARENCY_MAX] points)

| Category | Score | Max Points | Details |
|----------|-------|------------|---------|
| Status Hygiene | [STATUS_HYGIENE_SCORE] | [STATUS_HYGIENE_MAX] | [ITEMS_WITH_VALID_STATUS]/[TOTAL_ITEMS] items have valid status |
| Blocker Documentation | [BLOCKER_SCORE] | [BLOCKER_MAX] | [BLOCKED_WITH_REASONS]/[BLOCKED_TOTAL] blockers documented |
| Implementation Notes | [TRANSPARENCY_NOTES_SCORE] | [TRANSPARENCY_NOTES_MAX] | [ITEMS_WITH_MEANINGFUL_NOTES]/[TOTAL_ITEMS] items have meaningful notes |
| Validation History | [HISTORY_SCORE] | [HISTORY_MAX] | [HISTORY_ENTRIES] validation entries |

---

## Requirements Status

### Functional Requirements

| ID | Title | Priority | Status | Test Status | Completion Date | Notes |
|----|-------|----------|--------|-------------|-----------------|-------|
[FUNCTIONAL_REQUIREMENTS_TABLE_ROWS]

### Non-Functional Requirements

| ID | Title | Status | Test Status | Completion Date | Notes |
|----|-------|--------|-------------|-----------------|-------|
[NON_FUNCTIONAL_REQUIREMENTS_TABLE_ROWS]

### Data Models

| Model | Status | Implementation Notes |
|-------|--------|---------------------|
[DATA_MODELS_TABLE_ROWS]

### API Endpoints

| Method | Path | Status | Implementation Notes |
|--------|------|--------|---------------------|
[API_ENDPOINTS_TABLE_ROWS]

---

## Issues by Severity

### Critical Issues ([CRITICAL_COUNT])

[CRITICAL_ISSUES_SECTION - If has_critical_issues:
For each critical issue, format as:
#### [NUMBER]. [TITLE]

**Category**: [CATEGORY]
**Item**: [ITEM_ID]

**Description**: [DESCRIPTION]

**Impact**: [IMPACT]

**Fix**: [FIX_ACTION]

**File**: [FILE_LOCATION]

---
Otherwise:
No critical issues found.
]

### Important Issues ([IMPORTANT_COUNT])

[IMPORTANT_ISSUES_SECTION - If has_important_issues:
For each important issue, format as:
#### [NUMBER]. [TITLE]

**Category**: [CATEGORY]
**Item**: [ITEM_ID]

**Description**: [DESCRIPTION]

**Impact**: [IMPACT]

**Fix**: [FIX_ACTION]

---
Otherwise:
No important issues found.
]

### Minor Issues ([MINOR_COUNT])

[MINOR_ISSUES_SECTION - If has_minor_issues:
For each minor issue, format as:
- **[ITEM_ID]**: [DESCRIPTION] ([FIX_ACTION])
Otherwise:
No minor issues found.
]

---

## Next Steps

### Immediate Actions (Address Critical Issues)

[CRITICAL_NEXT_STEPS_LIST]

### Short-Term Actions (Address Important Issues)

[IMPORTANT_NEXT_STEPS_LIST]

### Long-Term Improvements (Address Minor Issues)

[MINOR_NEXT_STEPS_LIST]

### Recommended Focus Areas

1. **[FOCUS_AREA_1]**: [FOCUS_AREA_1_DESCRIPTION]
2. **[FOCUS_AREA_2]**: [FOCUS_AREA_2_DESCRIPTION]
3. **[FOCUS_AREA_3]**: [FOCUS_AREA_3_DESCRIPTION]

---

## Validation History

[VALIDATION_HISTORY_SECTION - If has_validation_history:

### Score Trend

| Date | Score | Grade | Mode | Δ Score | Trend |
|------|-------|-------|------|---------|-------|
[VALIDATION_HISTORY_TABLE_ROWS]

### Dimension Trends

| Dimension | Current | Previous | Δ | Trend |
|-----------|---------|----------|---|-------|
| Completeness | [COMPLETENESS_CURRENT] | [COMPLETENESS_PREVIOUS] | [COMPLETENESS_DELTA] | [COMPLETENESS_TREND] |
| Quality | [QUALITY_CURRENT] | [QUALITY_PREVIOUS] | [QUALITY_DELTA] | [QUALITY_TREND] |
| Adherence | [ADHERENCE_CURRENT] | [ADHERENCE_PREVIOUS] | [ADHERENCE_DELTA] | [ADHERENCE_TREND] |
| Transparency | [TRANSPARENCY_CURRENT] | [TRANSPARENCY_PREVIOUS] | [TRANSPARENCY_DELTA] | [TRANSPARENCY_TREND] |

### Progress Chart

```
Score: 0    10   20   30   40   50   60   70   80   90   100
       |----|----|----|----|----|----|----|----|----|----|
       [SCORE_CHART]
```

Otherwise:

This is the first validation. No history available yet.

Run validations periodically to track progress over time.
]

---

## Configuration Summary

**Dimension Weights**:
- Implementation Completeness: [COMPLETENESS_WEIGHT]%
- Implementation Quality: [QUALITY_WEIGHT]%
- Spec Adherence: [ADHERENCE_WEIGHT]%
- Progress Transparency: [TRANSPARENCY_WEIGHT]%

**Priority Weights** (for FRs):
- High Priority: [HIGH_PRIORITY_WEIGHT]x
- Medium Priority: [MEDIUM_PRIORITY_WEIGHT]x
- Low Priority: [LOW_PRIORITY_WEIGHT]x

**Issue Severity Thresholds**:
- Critical: [CRITICAL_THRESHOLD_DESCRIPTION]
- Important: [IMPORTANT_THRESHOLD_DESCRIPTION]
- Minor: [MINOR_THRESHOLD_DESCRIPTION]

**Validation Mode Settings**:
- Mode: [VALIDATION_MODE]
- Estimated Duration: [ESTIMATED_DURATION]
- Dimensions Evaluated: [DIMENSIONS_EVALUATED]

---

## Appendix

### Spec Parsing Summary

- **Functional Requirements Found**: [FR_TOTAL]
- **Non-Functional Requirements Found**: [NFR_TOTAL]
- **Data Models Found**: [MODELS_TOTAL]
- **API Endpoints Found**: [APIS_TOTAL]
- **Edge Cases Found**: [EDGE_CASES_TOTAL]

### Checklist Validation Summary

- **Total Items in Checklist**: [CHECKLIST_TOTAL_ITEMS]
- **Orphaned Items** (in checklist but not in spec): [ORPHANED_COUNT]
- **Missing Items** (in spec but not in checklist): [MISSING_COUNT]
- **Synchronization Accuracy**: [SYNC_PERCENTAGE]%

### File Information

- **Spec File**: [SPEC_PATH]
- **Spec File Size**: [SPEC_FILE_SIZE]
- **Checklist File**: [CHECKLIST_PATH]
- **Checklist File Size**: [CHECKLIST_FILE_SIZE]
- **Report Generated**: [REPORT_PATH]

### Tool Versions

- **Spec Validator Version**: [VALIDATOR_VERSION]
- **Config Version**: [CONFIG_VERSION]
- **Template Version**: [TEMPLATE_VERSION]

---

**End of Report**

Generated by **spec-validator** plugin v[VALIDATOR_VERSION]

For questions or issues, see: [DOCUMENTATION_URL]

---

## Template Usage Instructions

This template uses [PLACEHOLDER] format for variable substitution.

To populate this template:
1. Read this template file using Read tool
2. Replace each [PLACEHOLDER] with actual values from your validation data
3. For conditional sections (marked with "If condition:"), include/exclude based on condition
4. For table rows sections (ending in _TABLE_ROWS), generate rows and replace the placeholder
5. Write the populated content using Write tool

Example placeholder replacements:
- [TIMESTAMP] → "2026-02-13 14:30:00"
- [OVERALL_SCORE] → "85"
- [GRADE] → "B"
- [COMPLETENESS_SCORE] → "34"

For table row placeholders, generate markdown table rows:
- [FUNCTIONAL_REQUIREMENTS_TABLE_ROWS] → Multiple rows like:
  | FR-1 | User Auth | high | completed | completed | 2026-02-10 | JWT tokens |
  | FR-2 | Profile | medium | in_progress | not_started | - | In development |

For list placeholders, generate markdown list items:
- [CRITICAL_NEXT_STEPS_LIST] → Multiple items like:
  - [ ] Implement FR-3 (high priority)
  - [ ] Fix synchronization errors in checklist
