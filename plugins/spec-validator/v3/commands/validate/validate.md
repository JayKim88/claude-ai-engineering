---
description: Validate implementation code against specification documents using YAML-based checklist and 4-dimension scoring
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# /validate Command

Validates that implementation code matches the specification document using a structured YAML checklist system.

## Syntax

```
/validate [mode] [--spec PATH] [--checklist PATH] [--output PATH]
```

## Parameters

- `mode` (optional): Validation mode
  - `full` - Complete validation (default)
  - `quick` - Fast validation (Completeness + Adherence only)
  - `requirements-only` - FR/NFR progress only

- `--spec PATH` (optional): Path to specification document
  - Default: Will prompt user or search current directory

- `--checklist PATH` (optional): Path to .spec-checklist.yaml
  - Default: Same directory as spec, named `.spec-checklist.yaml`

- `--output PATH` (optional): Path for validation report
  - Default: `{spec_directory}/validation-report-{timestamp}.md`

## Examples

```bash
# Full validation with defaults
/validate

# Quick validation
/validate quick

# Specify paths explicitly
/validate full --spec ./docs/feature-spec.md --checklist ./docs/.spec-checklist.yaml

# Requirements-only mode
/validate requirements-only --spec ./spec.md

# Custom output location
/validate --spec ./spec.md --output ./reports/validation.md
```

## What It Does

1. Parses the specification document to extract:
   - Functional Requirements (FR-1, FR-2, ...)
   - Non-Functional Requirements (NFR-1, NFR-2, ...)
   - Data Models
   - API Endpoints
   - Edge Cases

2. Reads and validates the `.spec-checklist.yaml` file

3. Calculates 4-dimension scores (100-point scale):
   - **Dimension 1 (40 pts)**: Implementation Completeness
   - **Dimension 2 (25 pts)**: Implementation Quality
   - **Dimension 3 (20 pts)**: Spec Adherence
   - **Dimension 4 (15 pts)**: Progress Transparency

4. Generates a comprehensive validation report with:
   - Overall score and grade (A-F)
   - Dimension scores breakdown
   - Requirements status table
   - Issues by severity (Critical/Important/Minor)
   - Next steps checklist
   - Validation history and trends

5. Updates validation history in the checklist file

## Validation Modes

| Mode | Duration | Dimensions | Use Case |
|------|----------|------------|----------|
| **full** | ~30s | All 4 | Complete pre-release validation |
| **quick** | ~10s | 2 | Daily standup checks |
| **requirements-only** | ~15s | 1 | Sprint progress tracking |

## Output

The command produces:
1. **Console summary**: Key findings and overall score
2. **Markdown report**: Detailed validation results saved to file
3. **Updated checklist**: Validation history appended

## Grade Scale

- **90-100 (A)**: Ready to ship
- **80-89 (B)**: Nearly complete
- **70-79 (C)**: Good progress
- **60-69 (D)**: Needs work
- **0-59 (F)**: Significant gaps

## Common Workflows

### Initial Setup
```bash
# 1. Create spec (using spec-interview plugin)
# 2. Generate checklist template
/validate --spec spec.md  # Will offer to generate template if missing

# 3. Start implementation, update checklist as you go
```

### Periodic Validation
```bash
# Quick check during development
/validate quick

# Full validation before sprint review
/validate full
```

### Pre-Release Validation
```bash
# Comprehensive validation
/validate full --spec ./docs/release-spec.md

# Fix issues identified in report
# Re-validate until score >= 90
/validate full
```

## Error Handling

The command handles common issues gracefully:

- **Spec not found**: Prompts for correct path
- **Checklist missing**: Offers to generate template from spec
- **YAML syntax errors**: Shows specific line and error details
- **Out-of-sync checklist**: Flags as Critical issues, continues validation
- **Missing sections**: Uses available data, flags gaps in report

## Integration with spec-interview

This command works seamlessly with specs created by the `spec-interview` plugin:

1. **spec-interview** → Create detailed specification
2. **spec-validator** → Generate checklist template
3. **Developer** → Implement features, update checklist
4. **spec-validator** → Validate periodically
5. **Iterate** until score >= 90

## Related Commands

- Use **spec-interview** skill to create specifications
- Use **project-insight** skill for code quality analysis
- Use **learning-summary** skill to document validation insights

## Configuration

Customize validation behavior by editing:
```
skills/spec-validator/config.yaml
```

Available settings:
- Dimension weights
- Priority weights for FRs
- Issue severity thresholds
- Parsing patterns
- Report format options

## Implementation Notes

When implementing this command execution in Claude Code:

1. **Path Detection Strategy**:
   - Detect plugin installation directory at runtime
   - Use `Bash(command="pwd")` to determine current context
   - Build paths relative to detected plugin root
   - Example: `config_path = skill_directory + "/config.yaml"`

2. **File Path Resolution**:
   - User-provided paths (spec, checklist): Use as absolute paths
   - Plugin files (config, templates): Detect at runtime
   - Output files: Generate relative to spec directory
   - Use Bash tool with `realpath` if needed: `Bash(command="realpath ./spec.md")`

3. **Tool Usage**:
   - Read spec: `Read(file_path=absolute_spec_path)`
   - Read checklist: `Read(file_path=absolute_checklist_path)`
   - Read config: `Read(file_path=detected_config_path)`
   - Read template: `Read(file_path=detected_template_path)`
   - Write report: `Write(file_path=absolute_report_path, content=report_content)`
   - Write checklist: `Write(file_path=absolute_checklist_path, content=updated_checklist)`

4. **User Prompts**:
   - Use AskUserQuestion for missing inputs
   - Format: `AskUserQuestion(question="Clear question with options if applicable")`
   - Parse response and validate before proceeding

5. **Template Population**:
   - Read template using Read tool
   - Replace [PLACEHOLDER] strings with actual values using string replacement
   - For conditional sections, include/exclude based on data availability
   - For table rows, generate complete rows then replace placeholder
   - See SKILL.md Step 12 for detailed substitution algorithm

6. **Error Handling**:
   - Try Read operations, catch file not found
   - Validate YAML syntax after reading
   - Check for required sections before processing
   - Provide clear error messages with next steps

7. **Path Examples**:
   ```python
   # Detect skill directory (do this once at start)
   skill_directory = detect_skill_installation_directory()

   # Build plugin paths
   config_path = skill_directory + "/config.yaml"
   template_directory = skill_directory + "/../../templates"
   template_path = template_directory + "/validation-report-template.md"

   # Use user-provided paths directly
   spec_path = user_provided_spec_path  # Absolute
   checklist_path = user_provided_checklist_path or default_checklist_path

   # Generate output path relative to spec
   spec_directory = get_directory_from_path(spec_path)
   report_path = spec_directory + "/validation-report-" + timestamp + ".md"
   ```
