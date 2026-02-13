---
name: spec-validator
description: Validates implementation code against specification documents using YAML-based checklists and 4-dimension scoring. Use when user says "validate spec implementation", "check if spec is implemented", "verify spec compliance", "스펙 검증", "구현 확인", "체크리스트 검증", or wants to verify that code matches requirements.
version: 1.0.0
---

# Spec Validator Skill

## Trigger Phrases

**English**:
- "validate spec implementation"
- "check if spec is implemented"
- "verify spec compliance"
- "validate against spec"
- "check spec checklist"
- "how complete is the implementation"
- "spec validation report"

**Korean**:
- "스펙 검증"
- "구현 확인"
- "체크리스트 검증"
- "명세 확인"
- "요구사항 검증"

## When to Use

Use this skill when:
1. You have a spec document and want to verify implementation progress
2. You need to check if a `.spec-checklist.yaml` file is synchronized with the spec
3. You want to generate a scored validation report (100-point scale, 4 dimensions)
4. You need to track validation history and score improvement trends
5. You want actionable feedback on what's missing or incomplete
6. You're in a spec-driven development workflow and need periodic verification

## Path Resolution Strategy

This skill uses a dynamic path detection system to avoid hardcoded absolute paths:

**Step 0: Detect Skill Directory**
```python
# At the start of execution, determine where the skill files are located
# Use Bash tool to find the plugin installation directory
Bash(command="pwd", description="Get current working directory")
# Store result as current_directory

# The skill directory will be relative to the plugin root
# Typical structure: {plugin_root}/skills/spec-validator/
# Config path: {skill_directory}/config.yaml
# Templates path: {plugin_root}/templates/
```

**Throughout Execution**:
- Use user-provided absolute paths for spec and checklist files
- Use detected `skill_directory` for config.yaml
- Use detected `plugin_root` for templates
- Generate output paths relative to spec directory

## Execution Algorithm

### Step 1: Initialization and Context Gathering

**Goal**: Collect required inputs from user or context.

**If spec path NOT provided in user request:**
Use AskUserQuestion tool to gather information:
```
AskUserQuestion(question="Please provide the path to your specification document (e.g., ./docs/spec.md):")
```

**If checklist path NOT provided:**
Default to looking for `.spec-checklist.yaml` in the same directory as the spec file.

**If validation mode NOT provided:**
Default to `full` mode.

**Generate session ID:**
Use current timestamp (format: YYYYMMDD-HHMMSS)

**Detect skill directory:**
```
# Use Bash to detect where this skill is installed
Bash(command="pwd", description="Detect current working directory")
# If in plugin context, skill_directory will be determinable from context
# Otherwise, search for config.yaml in typical plugin paths
```

**Outputs from this step:**
- `spec_path`: Full absolute path to spec document
- `checklist_path`: Full absolute path to checklist (or default location)
- `validation_mode`: "full", "quick", or "requirements-only"
- `session_id`: Timestamp string
- `skill_directory`: Detected path to skill files
- `config_path`: `{skill_directory}/config.yaml`
- `template_directory`: `{skill_directory}/../../templates`

**Branching Logic:**
- If spec path is invalid → Use AskUserQuestion to get correct path
- If validation mode is invalid → Default to "full" and notify user
- Proceed to Step 2

### Step 2: Load Configuration

**Goal**: Read configuration file to get scoring weights and parsing patterns.

**Action**: Use Read tool to load config:
```
Read(file_path=config_path)
```
Where `config_path` was determined in Step 1.

**Parse the YAML content** to extract:
- `dimensions` section (weights for each dimension)
- `priority_weights` (high=3, medium=2, low=1)
- `grades` thresholds (A=90-100, B=80-89, etc.)
- `issue_severity` mappings
- `parsing.functional_requirements.patterns` (regex patterns)
- `validation_modes` settings

**If config file not found or malformed:**
Use these hardcoded defaults:
```yaml
dimensions:
  implementation_completeness: 40
  implementation_quality: 25
  spec_adherence: 20
  progress_transparency: 15
priority_weights:
  high: 3
  medium: 2
  low: 1
  default: 2
```

Output to user: "Warning: Config not found. Using default settings."

**Outputs from this step:**
- `config` object with all settings

**Proceed to Step 3**

### Step 3: Parse Specification Document

**Goal**: Extract FRs, NFRs, models, APIs, and edge cases from spec.

**Action**: Use Read tool:
```
Read(file_path=spec_path)
```

**Parse the spec content** using these strategies:

**For Functional Requirements:**
- Search for patterns like `## FR-1:`, `**FR-2**:`, `FR-3:`
- For each match, extract:
  - ID (e.g., "FR-1")
  - Title (text after the colon)
  - Priority: Search nearby lines for "Priority: High", "(High)", "[HIGH]", etc.
    - If not found, default to "medium"
- Store in list: `functional_requirements = [{"id": "FR-1", "title": "...", "priority": "high"}, ...]`

**For Non-Functional Requirements:**
- Search for patterns like `## NFR-1:`, `**NFR-2**:`, etc.
- Extract ID and title
- Store in list: `non_functional_requirements = [{"id": "NFR-1", "title": "..."}, ...]`

**For Data Models:**
- Find section headers: "## Technical Design", "## Data Models"
- Extract model names from patterns like `### User Model`, `#### Product`
- Store in list: `data_models = [{"name": "User"}, {"name": "Product"}, ...]`

**For API Endpoints:**
- Search for patterns: `GET /api/`, `POST /api/`, etc.
- Also check: `` `GET /api/...` `` (in code blocks)
- Extract method and path
- Store in list: `api_endpoints = [{"method": "GET", "path": "/api/users"}, ...]`

**For Edge Cases:**
- Find section: "## Edge Cases", "### Edge Cases"
- Extract numbered or bulleted items
- Store in list: `edge_cases = [{"id": "EC-1", "description": "..."}, ...]`

**Outputs from this step:**
- `spec_data` object containing:
  - `functional_requirements` (list)
  - `non_functional_requirements` (list)
  - `data_models` (list)
  - `api_endpoints` (list)
  - `edge_cases` (list)

**Branching Logic:**
- If spec file is empty → Output error: "Spec document is empty. Cannot validate." → Exit
- If no FRs found → Log warning: "No functional requirements found. Check spec format." → Continue
- Proceed to Step 4

### Step 4: Read and Validate Checklist

**Goal**: Load checklist and verify structure.

**Action**: Use Read tool:
```
Read(file_path=checklist_path)
```

**If file not found:**
Use AskUserQuestion:
```
AskUserQuestion(question="Checklist not found at [checklist_path]. Would you like to:\n1) Generate template from spec\n2) Specify different path\n3) Exit\n\nEnter choice (1/2/3):")
```
- If choice = 1: Generate template (see template generation logic below), then Exit or Continue
- If choice = 2: Ask for new path, retry
- If choice = 3: Exit

**Parse YAML content:**
Verify these sections exist:
- `metadata`
- `functional_requirements`
- `non_functional_requirements`

**Validate each FR item has:**
- `id` field
- `status` field (value must be: completed, in_progress, not_started, or blocked)
- `test_status` field (value must be: completed, in_progress, or not_started)

**Check synchronization:**
- Create set of all spec item IDs: `spec_ids = {fr.id for fr in spec_data.functional_requirements} + {nfr.id for nfr in spec_data.non_functional_requirements}`
- Create set of all checklist item IDs: `checklist_ids = {item.id for item in checklist.functional_requirements} + {item.id for item in checklist.non_functional_requirements}`
- Find orphaned: `orphaned_items = checklist_ids - spec_ids`
- Find missing: `missing_items = spec_ids - checklist_ids`

**Outputs from this step:**
- `checklist` object with parsed data
- `sync_report`:
  - `orphaned_items` (list)
  - `missing_items` (list)
  - `sync_percentage` (float)

**Branching Logic:**
- If YAML syntax invalid → Output error with line number → Exit
- If structure invalid → Output error with missing sections → Exit
- If out of sync → Flag for dimension 3 scoring → Continue
- Proceed to Step 5

### Step 5: Calculate Dimension 1 - Implementation Completeness (40 points)

**Goal**: Calculate completion score with priority weighting.

**FR Scoring (20 points max):**
```
weighted_completed = 0
weighted_total = 0

for each fr in spec_data.functional_requirements:
    weight = config.priority_weights[fr.priority]  # high=3, medium=2, low=1
    weighted_total += weight

    checklist_fr = find_in_checklist(fr.id)
    if checklist_fr.status == "completed":
        weighted_completed += weight

fr_percentage = weighted_completed / weighted_total if weighted_total > 0 else 0
fr_score = fr_percentage * 20
```

**NFR Scoring (10 points max):**
```
nfr_completed = count(nfr in checklist where status == "completed")
nfr_total = len(spec_data.non_functional_requirements)
nfr_score = (nfr_completed / nfr_total) * 10 if nfr_total > 0 else 10
```

**Model Scoring (5 points max):**
```
models_completed = count(model in checklist where status == "completed")
models_total = len(spec_data.data_models)
model_score = (models_completed / models_total) * 5 if models_total > 0 else 5
```

**API Scoring (5 points max):**
```
apis_completed = count(api in checklist where status == "completed")
apis_total = len(spec_data.api_endpoints)
api_score = (apis_completed / apis_total) * 5 if apis_total > 0 else 5
```

**Total:**
```
dimension_1_score = fr_score + nfr_score + model_score + api_score
```

**Outputs from this step:**
- `dimension_1_score` (0-40)
- `completeness_breakdown` with per-category scores

**Proceed to Step 6**

### Step 6: Calculate Dimension 2 - Implementation Quality (25 points)

**Goal**: Assess quality indicators.

**Test Coverage (15 points max):**
```
requirements_with_tests = count(items in checklist where test_status == "completed")
total_requirements = len(all checklist items with test_status field)
test_coverage_score = (requirements_with_tests / total_requirements) * 15 if total_requirements > 0 else 0
```

**Edge Case Coverage (7 points max):**
```
edge_cases_handled = count(ec in checklist where status == "completed")
edge_cases_total = len(spec_data.edge_cases)
edge_case_score = (edge_cases_handled / edge_cases_total) * 7 if edge_cases_total > 0 else 7
```

**Implementation Notes (3 points max):**
```
items_with_notes = count(items in checklist where implementation_notes is not empty)
total_items = len(all checklist items)
notes_score = (items_with_notes / total_items) * 3
```

**Total:**
```
dimension_2_score = test_coverage_score + edge_case_score + notes_score
```

**Outputs from this step:**
- `dimension_2_score` (0-25)
- `quality_breakdown`

**Proceed to Step 7**

### Step 7: Calculate Dimension 3 - Spec Adherence (20 points)

**Goal**: Verify synchronization.

**Synchronization Score (12 points max):**
```
total_spec_items = len(spec_ids)
error_count = len(orphaned_items) + len(missing_items)
sync_accuracy = 1 - (error_count / total_spec_items) if total_spec_items > 0 else 1
sync_score = sync_accuracy * 12
```

**Priority Accuracy (5 points max):**
```
priority_matches = 0
total_frs = len(spec_data.functional_requirements)

for each fr in spec_data.functional_requirements:
    checklist_fr = find_in_checklist(fr.id)
    if checklist_fr and checklist_fr.priority == fr.priority:
        priority_matches += 1

priority_score = (priority_matches / total_frs) * 5 if total_frs > 0 else 5
```

**Structure Compliance (3 points max):**
```
required_sections = ["metadata", "functional_requirements", "non_functional_requirements"]
has_all_sections = all(section in checklist for section in required_sections)
structure_score = 3 if has_all_sections else 0
```

**Total:**
```
dimension_3_score = sync_score + priority_score + structure_score
```

**Outputs from this step:**
- `dimension_3_score` (0-20)
- `adherence_breakdown`

**Proceed to Step 8**

### Step 8: Calculate Dimension 4 - Progress Transparency (15 points)

**Goal**: Evaluate tracking hygiene.

**Status Hygiene (5 points max):**
```
valid_statuses = ["completed", "in_progress", "not_started", "blocked"]
items_with_valid_status = count(items where status in valid_statuses)
total_items = len(all checklist items)
status_hygiene_score = (items_with_valid_status / total_items) * 5
```

**Blocker Documentation (4 points max):**
```
blocked_items = items where status == "blocked"
blocked_with_reasons = count(blocked_items where blockers field is not empty)
blocker_score = (blocked_with_reasons / len(blocked_items)) * 4 if len(blocked_items) > 0 else 4
```

**Implementation Notes (3 points max):**
```
items_with_meaningful_notes = count(items where len(implementation_notes) > 10)
notes_score = (items_with_meaningful_notes / total_items) * 3
```

**Validation History (3 points max):**
```
history_entries = len(checklist.validation_history) if hasattr(checklist, 'validation_history') else 0
if history_entries >= 2:
    history_score = 3
elif history_entries == 1:
    history_score = 1
else:
    history_score = 0
```

**Total:**
```
dimension_4_score = status_hygiene_score + blocker_score + notes_score + history_score
```

**Outputs from this step:**
- `dimension_4_score` (0-15)
- `transparency_breakdown`

**Proceed to Step 9**

### Step 9: Aggregate Scores and Determine Grade

**Goal**: Calculate overall score and assign grade.

**Score aggregation based on mode:**
```
if validation_mode == "full":
    overall_score = dimension_1_score + dimension_2_score + dimension_3_score + dimension_4_score
elif validation_mode == "quick":
    raw_score = dimension_1_score + dimension_3_score  # max 60
    overall_score = (raw_score / 60) * 100
elif validation_mode == "requirements-only":
    raw_score = dimension_1_score  # max 40
    overall_score = (raw_score / 40) * 100
```

**Grade assignment:**
```
if overall_score >= 90:
    grade = "A"
    label = "Ready to ship"
elif overall_score >= 80:
    grade = "B"
    label = "Nearly complete"
elif overall_score >= 70:
    grade = "C"
    label = "Good progress"
elif overall_score >= 60:
    grade = "D"
    label = "Needs work"
else:
    grade = "F"
    label = "Significant gaps"
```

**Outputs from this step:**
- `overall_score` (0-100)
- `grade` (A-F)
- `grade_label` (string)

**Proceed to Step 10**

### Step 10: Generate Issues List

**Goal**: Categorize all findings.

**Critical Issues** (from config.issue_severity.critical):
- Missing high-priority FRs (where status != "completed")
- Orphaned checklist items (in checklist but not in spec)
- Invalid YAML structure
- Synchronization errors (>10% items out of sync)

**Important Issues** (from config.issue_severity.important):
- Missing medium-priority FRs
- Completed items without tests (status="completed" but test_status!="completed")
- Missing NFRs
- Priority mismatches between spec and checklist
- Blocked items without blocker explanations

**Minor Issues** (from config.issue_severity.minor):
- Missing low-priority FRs
- Incomplete implementation notes
- Missing validation history

**For each issue, create:**
```
{
  "title": "FR-X not completed",
  "category": "Functional Requirement",
  "item_id": "FR-X",
  "description": "High-priority requirement not implemented",
  "impact": "Blocks core functionality",
  "fix_action": "Implement FR-X in [relevant file]",
  "file_location": checklist_path
}
```

**Outputs from this step:**
- `critical_issues` (list)
- `important_issues` (list)
- `minor_issues` (list)
- `next_steps` (list of actions)

**Proceed to Step 11**

### Step 11: Update Validation History

**Goal**: Append validation entry to checklist.

**Action**: Use Read tool to get current checklist:
```
Read(file_path=checklist_path)
```

**Create history entry:**
```
new_entry = {
  "date": current_timestamp_ISO8601,
  "score": overall_score,
  "grade": grade,
  "dimensions": {
    "completeness": dimension_1_score,
    "quality": dimension_2_score,
    "adherence": dimension_3_score,
    "transparency": dimension_4_score
  },
  "mode": validation_mode,
  "validator_version": "1.0.0"
}
```

**Append to checklist YAML:**
If `validation_history` section exists, append to it.
If not, create new section.

**Calculate delta if previous history exists:**
```
if len(validation_history) > 1:
    score_delta = overall_score - validation_history[-2].score
    if score_delta > 0:
        trend = "↗ Improving"
    elif score_delta < 0:
        trend = "↘ Declining"
    else:
        trend = "→ Stable"
```

**Action**: Use Write tool to save updated checklist:
```
Write(file_path=checklist_path, content=updated_checklist_yaml)
```

**Outputs from this step:**
- Updated checklist file
- `score_delta` (if applicable)
- `trend` (if applicable)

**Branching Logic:**
- If write fails → Log error: "Could not update validation history" → Continue to Step 12

**Proceed to Step 12**

### Step 12: Generate Validation Report

**Goal**: Create comprehensive Markdown report.

**Detect template path:**
```
template_path = template_directory + "/validation-report-template.md"
```

**Action**: Use Read tool to load template:
```
Read(file_path=template_path)
```

**Template Substitution Algorithm:**

The template uses `[PLACEHOLDER]` format. To populate:

**Step 12.1: Read Template**
```
template_content = Read(file_path=template_path)
```

**Step 12.2: Prepare All Replacement Values**
Create a dictionary mapping placeholders to actual values:
```python
replacements = {
  "[TIMESTAMP]": current_timestamp,
  "[VALIDATION_MODE]": validation_mode,
  "[SPEC_PATH]": spec_path,
  "[CHECKLIST_PATH]": checklist_path,
  "[OVERALL_SCORE]": str(overall_score),
  "[GRADE]": grade,
  "[GRADE_DESCRIPTION]": grade_label,
  "[COMPLETENESS_SCORE]": str(dimension_1_score),
  "[COMPLETENESS_MAX]": "40",
  "[COMPLETENESS_PERCENTAGE]": str(int(dimension_1_score / 40 * 100)),
  # ... continue for all placeholders
}
```

**Step 12.3: Handle Table Row Placeholders**
For placeholders ending in `_TABLE_ROWS`, generate markdown table rows:
```python
# Example: Functional Requirements Table
fr_rows = []
for fr in functional_requirements:
    row = f"| {fr.id} | {fr.title} | {fr.priority} | {fr.status} | {fr.test_status} | {fr.completed_date or '-'} | {fr.implementation_notes or '-'} |"
    fr_rows.append(row)

replacements["[FUNCTIONAL_REQUIREMENTS_TABLE_ROWS]"] = "\n".join(fr_rows)
```

**Step 12.4: Handle Conditional Sections**
For sections marked with `[SECTION_NAME - If condition:]`, check condition and include/exclude:
```python
# Example: Previous Score Section
if has_previous_validation:
    previous_section = f"**Previous Score**: {previous_score}/100 ({score_delta})\n**Trend**: {trend_indicator} {trend_label}"
    # Keep the section
else:
    # Remove the entire conditional section from template
    # Find the section between markers and delete it
```

**Step 12.5: Perform String Replacement**
```python
report_content = template_content

# Replace all simple placeholders
for placeholder, value in replacements.items():
    report_content = report_content.replace(placeholder, value)

# Remove any remaining conditional markers
# (If a conditional section was kept, remove its markers)
```

**Step 12.6: Validate Report Content**
Verify that:
- No `[PLACEHOLDER]` strings remain (except in usage instructions section)
- All tables have consistent column counts
- All scores are numeric and in valid ranges

**Generate report filename:**
```
report_filename = f"validation-report-{session_id}.md"
report_path = spec_directory + "/" + report_filename
```
Where `spec_directory` is the directory containing the spec file.

**Action**: Use Write tool to save report:
```
Write(file_path=report_path, content=report_content)
```

**Output to user:**
```
=== Spec Validation Complete ===

Overall Score: [overall_score]/100 (Grade [grade])
[grade_label]

Critical Issues: [critical_count]
Important Issues: [important_count]
Minor Issues: [minor_count]

Full report saved to: [report_path]
Validation history updated in checklist.
```

**Branching Logic:**
- If template not found → Use inline template structure → Continue
- If write fails → Output report to console instead → Continue

**End of execution**

## Error Handling

| Scenario | Detection | Response |
|----------|-----------|----------|
| **Spec document not found** | Step 1: File path validation | Use AskUserQuestion: "Spec document not found at [path]. Please provide a valid spec file path:" |
| **Spec document empty** | Step 3: Content validation after Read | Output error: "Spec document is empty. Cannot validate against an empty specification." → Exit |
| **Checklist not found** | Step 4: File path validation | Use AskUserQuestion: "Checklist not found. Would you like to: 1) Generate template from spec, 2) Specify different path, 3) Exit?" |
| **Checklist YAML invalid** | Step 4: YAML parsing | Output error: "Checklist YAML syntax invalid. Please fix the YAML syntax and try again." → Exit |
| **Checklist structure invalid** | Step 4: Schema validation | Output error: "Checklist structure invalid. Missing required sections: [list]. See templates/checklist-template.yaml for correct format." → Exit |
| **Out-of-sync checklist** | Step 7: Synchronization check | Continue validation but flag as Critical issues in Step 10. Deduct points in Dimension 3. Include orphaned and missing items in report. |
| **No FRs in spec** | Step 3: FR extraction | Log warning: "No functional requirements found in spec. This may indicate parsing issues or an incomplete spec." → Continue with scoring |
| **All requirements completed** | Step 5: Completion calculation | Output: "Congratulations! All requirements are marked complete. Score: [score]/100." → Still run quality checks in Dimensions 2-4. |
| **Config file not found** | Step 2: File read | Use hardcoded defaults. Log warning: "Config not found, using defaults." |
| **Invalid validation mode** | Step 1: Mode validation | Default to 'full' mode. Output: "Invalid mode '[mode]'. Using 'full' mode. Valid modes: full, quick, requirements-only." |
| **History update fails** | Step 11: File write | Log error: "Could not update validation history: [error]. Report generation will continue." → Continue |
| **Report generation fails** | Step 12: File write | Output: "Could not write report to file: [error]. Displaying in console instead." → Display full report in console |
| **Division by zero** | Steps 5-8: Score calculation | If denominator is 0 (e.g., no FRs), skip that category. Give full points for that subcategory. |

## Quick Reference

### Command Usage

```bash
# Full validation (default)
validate spec implementation

# Quick validation (Completeness + Adherence only)
validate spec implementation in quick mode

# Requirements-only (FR/NFR progress only)
validate requirements only

# Specify paths explicitly
validate spec at /path/to/spec.md with checklist /path/to/.spec-checklist.yaml

# Korean
스펙 검증
```

### Validation Modes

| Mode | Duration | Dimensions | Use Case |
|------|----------|------------|----------|
| **full** | ~30s | All 4 (100 pts) | Complete validation before releases |
| **quick** | ~10s | 2 (Completeness + Adherence) | Daily standup checks |
| **requirements-only** | ~15s | 1 (FR/NFR progress) | Sprint progress tracking |

### Scoring Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Implementation Completeness** | 40 pts | FRs (20), NFRs (10), Models (5), APIs (5) with priority weighting |
| **Implementation Quality** | 25 pts | Test coverage (15), Edge cases (7), Notes (3) |
| **Spec Adherence** | 20 pts | Sync (12), Priority accuracy (5), Structure (3) |
| **Progress Transparency** | 15 pts | Status hygiene (5), Blocker docs (4), Notes (3), History (3) |

### Grade Scale

- **90-100 (A)**: Ready to ship. High confidence in completeness.
- **80-89 (B)**: Nearly complete. Minor gaps, generally ready.
- **70-79 (C)**: Good progress. Significant work done, but notable gaps.
- **60-69 (D)**: Needs work. More incomplete than complete.
- **0-59 (F)**: Significant gaps. Major requirements missing.

### Typical Workflow

1. **Create spec** with spec-interview plugin
2. **Generate checklist**: `generate checklist from spec.md`
3. **Implement features**, update checklist after each completion
4. **Validate periodically**: Every sprint or before releases
5. **Fix issues** identified in validation report
6. **Re-validate** until score >= 90
7. **Ship** with confidence

### File Locations

- Spec document: Anywhere (user provides path)
- Checklist: Same directory as spec, named `.spec-checklist.yaml`
- Config: Detected at `{skill_directory}/config.yaml`
- Report: `{spec_directory}/validation-report-{timestamp}.md`
- Templates: Detected at `{plugin_root}/templates/`
