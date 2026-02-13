# Spec Validator - Development Guide

This document provides comprehensive guidance for developers who want to understand, modify, or extend the spec-validator plugin.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Execution Flow](#execution-flow)
4. [Key Components](#key-components)
5. [Scoring Algorithms](#scoring-algorithms)
6. [Parsing Strategy](#parsing-strategy)
7. [Configuration System](#configuration-system)
8. [Testing Checklist](#testing-checklist)
9. [Extension Points](#extension-points)
10. [Performance Considerations](#performance-considerations)
11. [Future Roadmap](#future-roadmap)

---

## Architecture Overview

### Design Philosophy

The spec-validator follows the **Architect Philosophy**: prioritizing completeness, extensibility, and robustness over simplicity.

**Core Principles**:
1. **Comprehensive structure**: All components present (plugin.json, SKILL.md, README, CLAUDE.md, config, templates, commands)
2. **Exhaustive error handling**: Every step has error scenarios documented and handled
3. **Extensive configuration**: YAML config with tunable parameters for all aspects
4. **Detailed documentation**: 150+ line README, complete SKILL.md with 12 steps, development guide
5. **Template system**: Separate templates for reports, checklists, and fix guides
6. **Quality-focused**: Uses sonnet model for balanced quality and speed

### Pattern: Simple Skill (NOT Multi-Agent)

**Rationale**: Spec validation is a sequential, deterministic process:
1. Parse spec document
2. Read checklist
3. Compare and calculate scores
4. Generate report

There's no benefit to parallelization here. Single spec, single checklist, no ambiguity requiring multiple perspectives.

**Contrast with Multi-Agent**: If we were generating multiple validation strategies or evaluating from different quality frameworks simultaneously, multi-agent would make sense. But validation is a straightforward comparison task.

### Why This Architecture?

- **Predictability**: Users get consistent, repeatable validation results
- **Debuggability**: Linear execution makes issues easy to trace
- **Performance**: No coordination overhead, faster than multi-agent for this use case
- **Simplicity**: Despite comprehensive features, execution flow is straightforward
- **Extensibility**: Easy to add new dimensions or parsing patterns without re-architecting

---

## Directory Structure

```
spec-validator/
├── .claude-plugin/
│   └── plugin.json                      # Plugin metadata (name, version, author)
│
├── skills/
│   └── spec-validator/
│       ├── SKILL.md                     # 12-step execution algorithm
│       └── config.yaml                  # Configuration (weights, patterns, thresholds)
│
├── commands/
│   └── validate/
│       └── validate.md                  # /validate slash command definition
│
├── templates/
│   ├── validation-report-template.md    # Markdown report structure
│   ├── checklist-template.yaml          # YAML checklist structure
│   └── fix-guide.md                     # Issue resolution guide
│
├── README.md                            # User documentation (150+ lines)
└── CLAUDE.md                            # This file (developer guide)
```

### File Purposes

| File | Purpose | Audience |
|------|---------|----------|
| **plugin.json** | Plugin metadata for registration | Plugin system |
| **SKILL.md** | Execution algorithm with 12 steps | Claude (LLM executor) |
| **config.yaml** | Tunable parameters (weights, patterns) | Developers/power users |
| **validate.md** | Slash command definition | Claude (command handler) |
| **validation-report-template.md** | Report structure with placeholders | Report generator |
| **checklist-template.yaml** | Checklist structure with examples | Template generator |
| **fix-guide.md** | Step-by-step issue resolution | End users |
| **README.md** | User documentation and examples | End users |
| **CLAUDE.md** | Development guide and architecture | Developers |

---

## Execution Flow

### High-Level Flow

```
User Invokes Validation
    ↓
Step 1: Initialization (gather paths, mode)
    ↓
Step 2: Load Configuration (weights, patterns)
    ↓
Step 3: Parse Spec (extract FRs, NFRs, models, APIs, edge cases)
    ↓
Step 4: Read & Validate Checklist (YAML validation, sync check)
    ↓
Steps 5-8: Calculate 4 Dimension Scores (in sequence)
    ↓
Step 9: Aggregate Scores (combine, assign grade)
    ↓
Step 10: Generate Issues List (categorize by severity)
    ↓
Step 11: Update Validation History (append to checklist)
    ↓
Step 12: Generate Report (populate template, save file)
    ↓
Display Summary & Report Path
```

### Detailed Step Breakdown

#### Step 1: Initialization and Context Gathering

**Inputs**:
- User request (trigger phrase or /validate command)
- Optional: spec path, checklist path, validation mode

**Process**:
1. Check if spec path provided
   - If yes: Use it
   - If no: Ask user via AskUserQuestion
2. Check if checklist path provided
   - If yes: Use it
   - If no: Default to `.spec-checklist.yaml` in spec directory
3. Check if validation mode provided
   - If yes: Validate (full/quick/requirements-only)
   - If no: Default to `full`
4. Generate session ID (timestamp)

**Outputs**:
- Resolved spec path
- Resolved checklist path
- Validation mode
- Session ID

**Error Handling**:
- Spec path invalid → Ask for correct path
- Mode invalid → Default to `full`, notify user

#### Step 2: Load Configuration

**Inputs**:
- Config file at `skills/spec-validator/config.yaml`

**Process**:
1. Read config file using Read tool
2. Parse YAML
3. Extract:
   - Dimension weights
   - Priority weights
   - Grade thresholds
   - Issue severity mappings
   - Parsing patterns
   - Validation mode settings

**Outputs**:
- Configuration object with all settings

**Error Handling**:
- Config not found → Use hardcoded defaults, log warning
- Config YAML invalid → Use hardcoded defaults, log error
- Missing fields → Use defaults for those fields

**Hardcoded Defaults**:
```python
DEFAULT_CONFIG = {
    "dimensions": {
        "completeness": 40,
        "quality": 25,
        "adherence": 20,
        "transparency": 15
    },
    "priority_weights": {
        "high": 3,
        "medium": 2,
        "low": 1
    }
    # ... etc
}
```

#### Step 3: Parse Specification Document

**Inputs**:
- Spec file path
- Parsing patterns from config

**Process**:
1. Read spec file using Read tool
2. Extract Functional Requirements:
   - Search for `FR-\d+` patterns
   - Extract title, priority, description
   - Default priority to `medium` if not specified
3. Extract Non-Functional Requirements:
   - Search for `NFR-\d+` patterns
   - Extract title, description
4. Extract Data Models:
   - Find "Technical Design" or "Data Models" section
   - Extract model names and fields
5. Extract API Endpoints:
   - Search for `GET|POST|PUT|DELETE /api/...` patterns
   - Extract method, path, description
6. Extract Edge Cases:
   - Find "Edge Cases" section
   - Extract numbered or bulleted items

**Outputs**:
- Structured spec object:
  ```python
  {
      "functional_requirements": [
          {"id": "FR-1", "title": "...", "priority": "high", "description": "..."},
          ...
      ],
      "non_functional_requirements": [...],
      "data_models": [...],
      "api_endpoints": [...],
      "edge_cases": [...]
  }
  ```

**Error Handling**:
- Spec empty → Exit with error
- No FRs found → Log warning, continue
- Section parsing fails → Log error, continue with other sections
- Invalid priority → Default to `medium`

**Parsing Strategy**: Multi-pattern matching (see [Parsing Strategy](#parsing-strategy) section)

#### Step 4: Read and Validate Checklist

**Inputs**:
- Checklist file path
- Spec object from Step 3

**Process**:
1. Read checklist file using Read tool
2. Parse YAML
3. Validate structure:
   - Required sections present (metadata, functional_requirements, non_functional_requirements)
   - Valid status values (completed/in_progress/not_started/blocked)
   - Valid test_status values
4. Synchronization check:
   - Compare checklist items to spec items
   - Identify orphaned items (in checklist but not spec)
   - Identify missing items (in spec but not checklist)
5. Priority verification:
   - Compare FR priorities between spec and checklist
   - Flag mismatches

**Outputs**:
- Parsed checklist object
- Synchronization report:
  ```python
  {
      "orphaned_items": ["FR-99", ...],
      "missing_items": ["FR-5", ...],
      "priority_mismatches": [{"id": "FR-3", "spec": "high", "checklist": "medium"}],
      "sync_percentage": 85.7
  }
  ```
- Validation warnings/errors

**Error Handling**:
- Checklist not found → Offer to generate template, exit or continue
- YAML invalid → Exit with error and syntax details
- Structure invalid → Exit with error and required format
- Out of sync → Flag for Dimension 3 scoring, continue
- Invalid status values → Flag as Important issue, continue but penalize Dimension 4

#### Steps 5-8: Calculate Dimension Scores

**Sequential execution** (not parallel, as each builds on shared data).

See [Scoring Algorithms](#scoring-algorithms) section for detailed formulas.

#### Step 9: Aggregate Scores and Determine Grade

**Inputs**:
- Dimension scores from Steps 5-8
- Validation mode
- Grade thresholds from config

**Process**:
1. Sum dimension scores based on mode:
   - `full`: All 4 dimensions
   - `quick`: Dimensions 1 + 3, rescale to 100
   - `requirements-only`: Dimension 1 only, rescale to 100
2. Assign letter grade based on thresholds:
   - 90-100: A
   - 80-89: B
   - 70-79: C
   - 60-69: D
   - 0-59: F

**Outputs**:
- Overall score (0-100)
- Letter grade (A-F)
- Grade description

#### Step 10: Generate Issues List

**Inputs**:
- All validation findings from Steps 3-8
- Issue severity thresholds from config

**Process**:
1. Categorize findings into Critical/Important/Minor based on config rules
2. For each issue:
   - Generate title
   - Describe impact
   - Provide specific fix action
   - Identify file location
3. Sort by severity, then by priority (high-priority FRs first)

**Outputs**:
- Categorized issue lists
- Next steps checklist

#### Step 11: Update Validation History

**Inputs**:
- Current checklist content
- Validation results from Steps 5-9
- Session metadata

**Process**:
1. Read current checklist
2. Append validation entry to `validation_history` section
3. Calculate score delta if previous history exists
4. Write updated checklist

**Outputs**:
- Updated checklist with new history entry
- Score delta (if applicable)
- Trend indicator (↗ improving, → stable, ↘ declining)

**Error Handling**:
- No previous history → Create history section
- History corrupted → Warn, create new history
- Write fails → Log error, continue to report

#### Step 12: Generate Validation Report

**Inputs**:
- All validation results from Steps 1-11
- Report template from `templates/validation-report-template.md`
- Configuration settings

**Process**:
1. Read report template
2. Populate placeholders with validation data
3. Generate tables, charts, issue lists
4. Write report to file

**Outputs**:
- Markdown validation report file
- Console summary
- Report file path

**Error Handling**:
- Template not found → Use inline template
- Write fails → Display report in console

---

## Key Components

### plugin.json

**Purpose**: Plugin registration metadata

**Structure**:
```json
{
  "name": "spec-validator",
  "version": "1.0.0",
  "description": "...",
  "author": {...},
  "license": "MIT",
  "keywords": [...]
}
```

**Why It Matters**: Enables plugin discovery and installation via `npm run link`.

### SKILL.md

**Purpose**: Execution algorithm for the LLM

**Structure**:
- YAML frontmatter (name, description, version)
- Trigger phrases (English and Korean)
- When to Use section
- Execution Algorithm (12 numbered steps with pseudocode)
- Error Handling table
- Quick Reference

**Why 12 Steps**: Breaks down complex validation into manageable, testable units. Each step has clear inputs, process, outputs, and error handling.

**Pseudocode Format**:
```python
ToolName(
    param="value",
    ...
)
```

This guides the LLM on which tools to invoke and what parameters to use.

### config.yaml

**Purpose**: Centralized configuration for all tunable parameters

**Sections**:
1. **Dimension Weights**: Control how much each dimension contributes to overall score
2. **Priority Weights**: Control how FRs are weighted by priority
3. **Grade Thresholds**: Define score ranges for letter grades
4. **Issue Severity**: Map issue types to Critical/Important/Minor
5. **Validation Modes**: Define mode-specific settings
6. **Parsing Patterns**: Regex patterns for extracting requirements from specs
7. **Checklist Validation Rules**: Schema rules for checklist validation
8. **Report Settings**: Report format and display options
9. **History Settings**: Validation history tracking configuration
10. **Paths**: Default file paths
11. **Feature Flags**: Enable/disable experimental features
12. **Performance Settings**: Limits and timeouts

**Why YAML**: Human-readable, version-controllable, supports comments for documentation.

**Extension Pattern**: To add a new configuration option, add it to config.yaml with a comment explaining its purpose, then reference it in SKILL.md or code.

### Templates

#### validation-report-template.md

**Purpose**: Structure for generated validation reports

**Features**:
- Handlebars-style placeholders: `{{variable_name}}`
- Conditional sections: `{{#if condition}}...{{/if}}`
- Loops: `{{#each items}}...{{/each}}`

**Sections**:
1. Executive Summary (score, grade, trend)
2. Dimension Scores (4 dimension breakdown)
3. Requirements Status (tables for FRs, NFRs, models, APIs)
4. Issues by Severity (Critical/Important/Minor)
5. Next Steps (actionable checklist)
6. Validation History (trends and charts)
7. Configuration Summary (weights, thresholds)
8. Appendix (parsing summary, file info)

**Why Separate Template**: Allows customization of report format without modifying execution logic. Power users can create custom report formats.

#### checklist-template.yaml

**Purpose**: Structure for generating new checklists from specs

**Features**:
- Complete YAML structure with all sections
- Example entries with comments
- Usage instructions in comments

**Generation Process**:
1. Parse spec to extract requirements
2. Populate template with extracted data
3. Initialize all status fields to `not_started`
4. Add metadata (spec path, creation date)
5. Save to `.spec-checklist.yaml`

#### fix-guide.md

**Purpose**: Comprehensive troubleshooting guide for users

**Structure**:
- Critical Issues (with step-by-step fixes)
- Important Issues (with step-by-step fixes)
- Minor Issues (with quick fixes)
- General Best Practices
- Example Workflows
- Troubleshooting FAQ

**Why Separate Guide**: Keeps README focused on usage, provides detailed resolution steps for each issue type.

---

## Scoring Algorithms

### Dimension 1: Implementation Completeness (40 points)

**Formula**:
```python
FR_score = calculate_weighted_fr_score(frs, priority_weights) * 20
NFR_score = (nfr_completed / nfr_total) * 10
Model_score = (models_completed / models_total) * 5
API_score = (apis_completed / apis_total) * 5

Dimension_1 = FR_score + NFR_score + Model_score + API_score
```

**Weighted FR Calculation**:
```python
def calculate_weighted_fr_score(frs, priority_weights):
    weighted_completed = 0
    weighted_total = 0

    for fr in frs:
        weight = priority_weights[fr.priority]  # high=3, medium=2, low=1
        weighted_total += weight

        if fr.status == "completed":
            weighted_completed += weight

    return weighted_completed / weighted_total if weighted_total > 0 else 0
```

**Example**:
- 2 high-priority FRs completed out of 3: (2/3) * 3 = 2
- 4 medium-priority FRs completed out of 5: (4/5) * 2 = 1.6
- 3 low-priority FRs completed out of 4: (3/4) * 1 = 0.75
- Weighted sum: 2 + 1.6 + 0.75 = 4.35
- Weighted total: 3*3 + 5*2 + 4*1 = 9 + 10 + 4 = 23
- Wait, recalculate: high total = 3*3 = 9, medium total = 5*2 = 10, low total = 4*1 = 4
- Total weighted = 9 + 10 + 4 = 23
- Completed weighted: 2*3 + 4*2 + 3*1 = 6 + 8 + 3 = 17
- FR percentage: 17 / 23 = 0.739
- FR score: 0.739 * 20 = 14.78 points

**Edge Cases**:
- If category has 0 items: Skip, don't penalize
- If all items in category completed: Give full points for that category
- If priority missing: Default to `medium` (weight = 2)

### Dimension 2: Implementation Quality (25 points)

**Formula**:
```python
Test_coverage = (requirements_with_tests_completed / total_requirements) * 15
Edge_case_coverage = (edge_cases_handled / total_edge_cases) * 7
Implementation_notes = (items_with_notes / total_items) * 3

Dimension_2 = Test_coverage + Edge_case_coverage + Implementation_notes
```

**Test Coverage Criteria**:
```python
def has_tests_completed(item):
    return item.test_status == "completed"
```

**Notes Quality Criteria**:
```python
def has_meaningful_notes(item):
    return (
        item.implementation_notes is not None and
        len(item.implementation_notes.strip()) > 0
    )
```

**Edge Cases**:
- If no edge cases in spec: Give full 7 points
- If no tests tracked: Score 0 for test coverage
- If notes empty but status completed: Penalize notes score

### Dimension 3: Spec Adherence (20 points)

**Formula**:
```python
Sync_score = (1 - (orphaned_items + missing_items) / total_spec_items) * 12
Priority_accuracy = (correctly_prioritized_frs / total_frs) * 5
Structure_compliance = 3 if valid_structure else 0

Dimension_3 = Sync_score + Priority_accuracy + Structure_compliance
```

**Synchronization Calculation**:
```python
def calculate_sync_score(spec, checklist):
    orphaned = items_in_checklist_not_in_spec(spec, checklist)
    missing = items_in_spec_not_in_checklist(spec, checklist)
    total = len(spec.all_items())

    error_rate = (len(orphaned) + len(missing)) / total if total > 0 else 0
    sync_accuracy = 1 - error_rate

    return sync_accuracy * 12
```

**Priority Accuracy**:
```python
def calculate_priority_accuracy(spec, checklist):
    matches = 0
    total = 0

    for fr in spec.functional_requirements:
        total += 1
        checklist_fr = checklist.find_fr(fr.id)

        if checklist_fr and checklist_fr.priority == fr.priority:
            matches += 1

    return (matches / total) * 5 if total > 0 else 0
```

**Structure Compliance**:
```python
def is_valid_structure(checklist):
    required_sections = ["metadata", "functional_requirements", "non_functional_requirements"]
    return all(section in checklist for section in required_sections)
```

### Dimension 4: Progress Transparency (15 points)

**Formula**:
```python
Status_hygiene = (items_with_valid_status / total_items) * 5
Blocker_documentation = (blocked_with_reasons / total_blocked) * 4
Implementation_notes = (items_with_meaningful_notes / total_items) * 3
Validation_history = calculate_history_score(history) * 3

Dimension_4 = Status_hygiene + Blocker_documentation + Implementation_notes + Validation_history
```

**History Score**:
```python
def calculate_history_score(history):
    if len(history) >= 2:
        return 1.0  # Full 3 points
    elif len(history) == 1:
        return 0.33  # 1 point (encourage starting tracking)
    else:
        return 0  # 0 points
```

**Blocker Documentation**:
```python
def has_blocker_explanation(item):
    return (
        item.status == "blocked" and
        item.blockers is not None and
        len(item.blockers.strip()) > 0
    )
```

---

## Parsing Strategy

### Multi-Pattern Matching

The plugin uses multiple regex patterns to handle different spec formats.

#### Functional Requirements Patterns

**Pattern 1: Header Format**
```regex
##\s+FR-(\d+)[:：]\s*(.+)
```
Matches:
- `## FR-1: User Authentication`
- `## FR-2： 사용자 인증` (Korean colon)

**Pattern 2: Bold Inline Format**
```regex
\*\*FR-(\d+)\*\*[:：]\s*(.+)
```
Matches:
- `**FR-1**: User Authentication`
- `**FR-1**： 사용자 인증`

**Pattern 3: Plain Text Format**
```regex
^FR-(\d+)[:：]\s*(.+)
```
Matches:
- `FR-1: User Authentication` (at start of line)

#### Priority Detection

**High Priority Patterns**:
```python
high_patterns = [
    r'Priority:\s*High',
    r'priority:\s*high',
    r'\(High\)',
    r'\[HIGH\]'
]
```

**Medium Priority Patterns**:
```python
medium_patterns = [
    r'Priority:\s*Medium',
    r'priority:\s*medium',
    r'\(Medium\)',
    r'\[MEDIUM\]'
]
```

**Low Priority Patterns**:
```python
low_patterns = [
    r'Priority:\s*Low',
    r'priority:\s*low',
    r'\(Low\)',
    r'\[LOW\]'
]
```

**Default**: If no priority pattern found, default to `medium`.

#### Data Models Parsing

**Section Detection**:
```python
section_markers = [
    "## Technical Design",
    "## Data Models",
    "### Data Models"
]
```

**Model Extraction**:
1. Find section markers
2. Extract text from marker to next major section
3. Search for model definitions:
   ```regex
   ###\s+(\w+)\s+Model
   ####\s+(\w+)
   ```
4. Extract fields (lines starting with `-` or `*`)

#### API Endpoints Parsing

**Pattern**:
```regex
(GET|POST|PUT|DELETE|PATCH)\s+(/[/\w\-{}:]+)
```

Matches:
- `GET /api/users`
- `POST /api/auth/login`
- `PUT /api/users/{id}`

**Backtick Pattern** (for inline code):
```regex
`(GET|POST|PUT|DELETE|PATCH)\s+([^`]+)`
```

Matches:
- `` `GET /api/users` ``
- `` `POST /api/auth/login` ``

#### Edge Cases Parsing

**Section Detection**:
```python
section_markers = [
    "## Edge Cases",
    "### Edge Cases",
    "## Error Handling"
]
```

**Item Extraction**:
```regex
^\d+\.\s+(.+)      # Numbered list: "1. Handle duplicate emails"
^[-*]\s+(.+)       # Bullet list: "- Handle duplicate emails"
```

### Handling Parsing Failures

**Graceful Degradation**:
1. If section not found, continue with other sections
2. If pattern doesn't match, try next pattern
3. If all patterns fail, log warning and move on
4. Never exit due to parsing failure (only structural failures)

**Example**:
```python
def parse_functional_requirements(spec_text):
    frs = []
    patterns = [pattern1, pattern2, pattern3]

    for pattern in patterns:
        matches = re.findall(pattern, spec_text)
        for match in matches:
            fr = create_fr_from_match(match)
            if fr not in frs:  # Avoid duplicates
                frs.append(fr)

    if len(frs) == 0:
        log_warning("No FRs found in spec. This may indicate parsing issues.")

    return frs
```

---

## Configuration System

### Configuration Hierarchy

1. **Hardcoded Defaults**: Built into SKILL.md as fallback
2. **config.yaml**: User-customizable settings
3. **Runtime Overrides**: Command-line flags (future enhancement)

### Adding New Configuration Options

**Steps**:
1. Add to `config.yaml` with comment:
   ```yaml
   # NEW FEATURE: Custom weighting for edge cases
   edge_case_weight:
     critical: 3
     important: 2
     minor: 1
   ```

2. Update `SKILL.md` Step 2 to read new config:
   ```python
   Read(
       file_path="skills/spec-validator/config.yaml"
   )
   # Extract edge_case_weight from config
   ```

3. Use in scoring algorithm (e.g., Step 6):
   ```python
   Edge_case_score = calculate_weighted_edge_case_score(
       edge_cases,
       config.edge_case_weight
   )
   ```

4. Update `README.md` Configuration section with new option

5. Update `CLAUDE.md` (this file) to document new option

### Configuration Best Practices

- **Always provide defaults**: Don't crash if config missing
- **Validate config values**: Check ranges, types, required fields
- **Document all options**: Comments in YAML, descriptions in README
- **Use descriptive names**: `dimension_weights.completeness` not `dw_c`
- **Group related settings**: Keep all dimension settings together

---

## Testing Checklist

### Pre-Release Testing

**Installation**:
- [ ] `npm run link` succeeds without errors
- [ ] Skill registered (trigger phrase activates)
- [ ] Command registered (`/validate` works)

**Basic Validation**:
- [ ] Parse simple spec with FRs and NFRs
- [ ] Generate checklist template from spec
- [ ] Calculate scores correctly for sample data
- [ ] Generate readable validation report
- [ ] Update validation history in checklist

**Error Handling**:
- [ ] Graceful handling of missing spec file
- [ ] Graceful handling of missing checklist file
- [ ] Error message for invalid YAML syntax
- [ ] Recovery from parsing failures
- [ ] Fallback to defaults when config missing

**Validation Modes**:
- [ ] `full` mode calculates all 4 dimensions
- [ ] `quick` mode skips Quality and Transparency
- [ ] `requirements-only` mode focuses on FRs/NFRs

**Scoring Accuracy**:
- [ ] Priority-weighted FR scoring works correctly
- [ ] Test coverage calculation is accurate
- [ ] Synchronization detection finds orphaned and missing items
- [ ] Grade assignment matches thresholds
- [ ] Score rescaling works for quick/requirements-only modes

**Edge Cases**:
- [ ] Handles spec with no FRs
- [ ] Handles spec with no NFRs
- [ ] Handles empty checklist sections
- [ ] Handles division by zero (0 total items)
- [ ] Handles very large specs (1000+ requirements)

**Integration**:
- [ ] Works with specs from spec-interview plugin
- [ ] Checklist template generates correctly
- [ ] Validation history persists across runs
- [ ] Report files save to correct location

### Test Spec and Checklist

Use these for regression testing:

**test-spec.md**:
```markdown
# Test Specification

## FR-1: Authentication (Priority: High)
User login with email and password.

## FR-2: Profile (Priority: Medium)
User profile page.

## NFR-1: Performance
API response time under 200ms.

## Technical Design
### User Model
- id
- email
- password_hash

## API Endpoints
- POST /api/auth/login
- GET /api/users/{id}

## Edge Cases
1. Handle duplicate email registration
2. Handle invalid password format
```

**test-checklist.yaml**:
```yaml
metadata:
  spec_file: "./test-spec.md"
  project_name: "Test Project"
  created_date: "2026-02-13"

functional_requirements:
  - id: "FR-1"
    title: "Authentication"
    priority: "high"
    status: "completed"
    test_status: "completed"
    implementation_notes: "Done"

  - id: "FR-2"
    title: "Profile"
    priority: "medium"
    status: "not_started"
    test_status: "not_started"

non_functional_requirements:
  - id: "NFR-1"
    title: "Performance"
    status: "in_progress"
    test_status: "not_started"
```

**Expected Results**:
- Completeness: ~50% (1/2 FRs, 0/1 NFRs completed)
- Quality: Low (1/2 tested, no notes)
- Adherence: High (no sync issues)
- Transparency: Low (no history)
- Overall: ~60-65 (Grade D)

---

## Extension Points

### Adding New Dimensions

**Example**: Add "Security" dimension (10 points)

1. **Update config.yaml**:
   ```yaml
   dimensions:
     # ... existing dimensions ...
     security:
       total_weight: 10
       breakdown:
         authentication: 4
         authorization: 3
         encryption: 3
   ```

2. **Add Step 8.5 to SKILL.md**:
   ```markdown
   ### Step 8.5: Calculate Dimension 5 - Security (10 points)

   Assess security implementation.

   **Scoring Algorithm**:
   ```python
   Auth_score = (auth_requirements_completed / auth_requirements_total) * 4
   Authz_score = (authz_requirements_completed / authz_requirements_total) * 3
   Encryption_score = (encryption_requirements_completed / encryption_requirements_total) * 3

   Dimension_5 = Auth_score + Authz_score + Encryption_score
   ```
   ```

3. **Update aggregation in Step 9**:
   ```python
   if mode == "full":
       Overall_score = Dimension_1 + Dimension_2 + Dimension_3 + Dimension_4 + Dimension_5
   ```

4. **Update report template** to include security dimension

5. **Update README** with new dimension documentation

### Adding New Parsing Patterns

**Example**: Support "REQ-1" instead of "FR-1"

1. **Update config.yaml**:
   ```yaml
   parsing:
     functional_requirements:
       patterns:
         # ... existing patterns ...
         - regex: '##\s+REQ-(\d+)[:：]\s*(.+)'
           capture_groups:
             id: 1
             title: 2
   ```

2. **Update SKILL.md Step 3** to use new patterns

3. **Test** with sample spec using REQ-X format

### Adding New Issue Types

**Example**: Detect missing API documentation

1. **Update config.yaml**:
   ```yaml
   issue_severity:
     important:
       # ... existing issues ...
       - missing_api_documentation
   ```

2. **Update SKILL.md Step 10** to check for API docs:
   ```python
   for api in api_endpoints:
       if api.status == "completed" and not api.documentation:
           issues.append({
               "type": "missing_api_documentation",
               "severity": "important",
               "item": api.id,
               "description": "API implemented but lacks documentation"
           })
   ```

3. **Update fix-guide.md** with resolution steps

### Adding New Validation Modes

**Example**: Add "security-only" mode

1. **Update config.yaml**:
   ```yaml
   validation_modes:
     security_only:
       duration_estimate: "20 seconds"
       dimensions: ["security"]
       total_points: 10  # Will be rescaled to 100
       description: "Security requirements validation only"
   ```

2. **Update SKILL.md Step 1** to accept new mode

3. **Update SKILL.md Step 9** to handle rescaling:
   ```python
   elif mode == "security-only":
       Overall_score = Dimension_5  # Rescale to 100
       Overall_score = (Overall_score / 10) * 100
   ```

4. **Update validate.md** command documentation

---

## Performance Considerations

### Bottlenecks

**Spec Parsing** (Step 3):
- Large specs (10+ MB) can take 10-20 seconds to parse
- Multiple regex patterns executed sequentially

**Optimization**:
```python
# Cache parsed spec to avoid re-parsing
# Set max file size limit (default 10MB)
if spec_file_size > config.performance.max_spec_size_mb * 1024 * 1024:
    exit_with_error("Spec file too large")
```

**Checklist Validation** (Step 4):
- YAML parsing is generally fast (<1 second)
- Synchronization check is O(n*m) where n=spec items, m=checklist items

**Optimization**:
```python
# Use hash maps for O(1) lookups
spec_item_ids = set([item.id for item in spec.all_items()])
checklist_item_ids = set([item.id for item in checklist.all_items()])

orphaned = checklist_item_ids - spec_item_ids
missing = spec_item_ids - checklist_item_ids
```

### Scalability Limits

**Current Limits** (from config):
- Max spec size: 10 MB
- Max checklist items: 1000
- Parsing timeout: 30 seconds

**Handling Large Projects**:
1. Split spec into modules (frontend, backend, API, etc.)
2. Validate each module separately
3. Aggregate scores across modules (future feature)

**Memory Usage**:
- Spec and checklist held in memory
- Report template held in memory
- Peak memory: ~50 MB for typical project
- Max memory: ~500 MB for very large project

### Performance Tuning

**Quick Mode** (skip dimensions 2 and 4):
- Reduces validation time from 30s to 10s
- Use for daily checks

**Parsing Optimization**:
```yaml
# In config.yaml
performance:
  parsing_timeout_seconds: 30
  max_regex_matches: 1000  # Stop after 1000 matches per pattern
  enable_parsing_cache: true  # Cache parsed specs
```

---

## Future Roadmap

### Phase 1: Core Enhancements (v1.1)

**1. Code Validation**
- Scan actual codebase to verify implementations exist
- Don't just rely on checklist self-reporting
- Use Grep and Read tools to search for function/class definitions
- Auto-update checklist based on code findings

**2. Auto-Fix**
- Automatically fix minor sync issues
- Add missing items to checklist
- Remove orphaned items (with user confirmation)
- Update priorities to match spec

**3. Git Integration**
- Track validations with git commits
- Add validation score to commit messages
- Show validation score in `git log`
- Prevent commits if score < threshold (configurable)

### Phase 2: Integration & Automation (v1.2)

**4. CI/CD Integration**
- Run validation as part of CI pipeline
- Fail builds if score < threshold
- Generate validation reports in CI artifacts
- Badge showing current validation score

**5. Visual Dashboard**
- Web-based dashboard showing validation trends
- Burndown charts for requirements
- Dimension score over time
- Team leaderboard (if multiple projects)

**6. Multi-Spec Support**
- Validate multiple specs in one run
- Frontend spec + Backend spec + API spec
- Aggregate scores across specs
- Generate combined validation report

### Phase 3: Intelligence & Integration (v2.0)

**7. AI-Assisted Validation**
- Use LLM to scan code and auto-populate checklist status
- Suggest implementation notes based on code analysis
- Predict completion dates based on velocity
- Recommend priority adjustments based on dependencies

**8. Test Coverage Integration**
- Integrate with pytest-cov, Istanbul, JaCoCo
- Use actual coverage data instead of checklist self-reporting
- Fail validation if coverage < threshold
- Generate coverage reports alongside validation reports

**9. Project Management Integration**
- Sync with Jira, Linear, GitHub Projects
- Auto-update checklist from ticket status
- Create tickets for missing requirements
- Link validation report to sprint board

**10. Team Collaboration**
- Slack/Discord notifications on validation completion
- Tag team members in issues
- Commenting system for validation findings
- Shared validation dashboard

### Phase 4: Advanced Features (v2.5+)

**11. Custom Dimensions**
- Allow users to define additional scoring dimensions
- Plugin system for dimension calculators
- Pre-built dimension libraries (accessibility, i18n, performance)

**12. Validation Templates**
- Pre-built templates for common project types
- REST API template
- React app template
- Microservice template
- Mobile app template

**13. Compliance Reporting**
- Generate audit-ready compliance reports
- SOC 2, HIPAA, GDPR compliance checks
- Map requirements to compliance standards
- Automated compliance validation

**14. Regression Detection**
- Alert if score decreases between validations
- Track which dimension regressed
- Identify newly failing requirements
- Auto-create tickets for regressions

---

## Development Workflow

### Making Changes

1. **Branch**: Create feature branch
   ```bash
   git checkout -b feature/add-security-dimension
   ```

2. **Modify Files**:
   - Update `config.yaml` with new settings
   - Update `SKILL.md` with new steps or logic
   - Update templates if output format changes
   - Update `README.md` with user-facing changes
   - Update `CLAUDE.md` (this file) with developer notes

3. **Test**:
   - Run validation on test spec
   - Verify scores are correct
   - Check report format
   - Test error handling

4. **Document**:
   - Add examples to README
   - Update configuration reference
   - Add troubleshooting notes if needed

5. **Commit**:
   ```bash
   git add .
   git commit -m "feat: add security dimension validation"
   ```

6. **PR**: Submit pull request with clear description

### Debugging

**Enable Verbose Logging**:
```yaml
# In config.yaml (future feature)
debug:
  enabled: true
  log_parsing: true
  log_scoring: true
  log_file: "./validation-debug.log"
```

**Manual Testing**:
```bash
# Test parsing
/validate --spec test-spec.md

# Check config loading
cat skills/spec-validator/config.yaml

# Verify YAML syntax
yamllint .spec-checklist.yaml

# Check report generation
cat validation-report-*.md
```

**Common Issues**:
- **Scores seem wrong**: Check config weights, verify status values are valid
- **Parsing misses items**: Add debug logging to Step 3, check regex patterns
- **Report not generated**: Verify template exists, check file write permissions
- **History not updating**: Check YAML structure, verify write succeeded

---

## Conclusion

The spec-validator plugin is designed to be comprehensive, extensible, and production-ready. Following the Architect philosophy, it prioritizes completeness and robustness while maintaining a clear, linear execution flow.

**Key Takeaways**:
1. **Simple Skill Architecture**: Sequential validation is more appropriate than multi-agent for this use case
2. **Extensive Configuration**: YAML config provides flexibility without code changes
3. **Template System**: Separates structure from logic for easy customization
4. **Comprehensive Error Handling**: Every step has failure modes documented and handled
5. **Clear Extension Points**: Easy to add dimensions, patterns, modes, or issue types

**For New Contributors**:
- Start with README.md to understand user perspective
- Read SKILL.md to understand execution flow
- Review config.yaml to see all tunable parameters
- Consult this CLAUDE.md for architecture and extension guidance

**Maintenance**:
- Keep all documentation synchronized when making changes
- Test edge cases thoroughly (empty specs, invalid YAML, sync errors)
- Preserve backwards compatibility when updating scoring algorithms
- Version configuration schema if making breaking changes

**Questions?**
- See fix-guide.md for troubleshooting
- Check README examples for usage patterns
- Review SKILL.md error handling table for specific scenarios
- Open an issue with detailed reproduction steps

---

**Last Updated**: 2026-02-13
**Plugin Version**: 1.0.0
**Author**: Jay Kim
