# Spec Validator - Installation and Testing Guide

Complete guide for installing, configuring, and testing the spec-validator plugin.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Verification](#verification)
4. [Configuration](#configuration)
5. [First Validation](#first-validation)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Uninstallation](#uninstallation)

---

## Prerequisites

### Required

- **Claude CLI**: Version 0.5.0 or higher with plugin support
- **Node.js**: Version 14.0 or higher
- **npm**: Version 6.0 or higher
- **Git**: For version control (recommended)

### Recommended

- **YAML Linter**: `yamllint` for validating checklist files
  ```bash
  # macOS
  brew install yamllint

  # Linux
  pip install yamllint
  ```

- **Markdown Linter**: `markdownlint` for spec document validation
  ```bash
  npm install -g markdownlint-cli
  ```

### Check Prerequisites

```bash
# Check Claude CLI version
claude --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git
git --version
```

**Expected Output**:
```
claude version 0.5.0 or higher
node version v14.0.0 or higher
npm version 6.0.0 or higher
git version 2.x.x
```

---

## Installation

### Method 1: Install from Source (Recommended)

1. **Navigate to plugins directory**:
   ```bash
   cd /Users/jaykim/Documents/Projects/claude-ai-engineering/plugins
   ```

2. **Copy plugin files**:
   ```bash
   # If installing from tempo directory
   cp -r ../tempo/competitive-agents/spec-validator/agent-b/v1 spec-validator

   # Or if downloading from repository
   git clone https://github.com/JayKim88/claude-ai-engineering.git
   cd claude-ai-engineering/plugins
   ```

3. **Verify directory structure**:
   ```bash
   cd spec-validator
   ls -la
   ```

   **Expected output**:
   ```
   .claude-plugin/
   skills/
   commands/
   templates/
   docs/
   README.md
   CLAUDE.md
   ```

4. **Link the plugin**:
   ```bash
   cd /Users/jaykim/Documents/Projects/claude-ai-engineering
   npm run link
   ```

   **Expected output**:
   ```
   Linking plugins...
   ✓ Linked skill: spec-validator
   ✓ Linked command: /validate
   ✓ Plugin installation complete
   ```

5. **Verify installation**:
   ```bash
   claude plugins list
   ```

   **Expected output** (should include):
   ```
   spec-validator (v1.0.0) - Validate implementation against specifications
   ```

### Method 2: Install from Package (Future)

```bash
# Once published to npm registry
npm install -g @claude-plugins/spec-validator

# Link to Claude
claude plugin install spec-validator
```

---

## Verification

### Step 1: Check Plugin Registration

```bash
# List all installed plugins
claude plugins list

# Check if spec-validator is registered
claude plugins list | grep spec-validator
```

**Expected**: `spec-validator` appears in the list

### Step 2: Verify Skill Registration

```bash
# List all skills
claude skills list

# Check if spec-validator skill is registered
claude skills list | grep spec-validator
```

**Expected**: `spec-validator` skill appears in the list

### Step 3: Verify Command Registration

```bash
# List all commands
claude commands list

# Check if /validate command is registered
claude commands list | grep validate
```

**Expected**: `/validate` command appears in the list

### Step 4: Test Trigger Phrases

Open Claude CLI and try:
```
validate spec implementation
```

**Expected**: Skill activates and asks for spec path

### Step 5: Test Slash Command

Open Claude CLI and try:
```
/validate
```

**Expected**: Command executes and asks for spec path

---

## Configuration

### Default Configuration

The plugin comes with sensible defaults in `skills/spec-validator/config.yaml`.

**To view default config**:
```bash
cat plugins/spec-validator/skills/spec-validator/config.yaml
```

### Customizing Configuration

1. **Copy default config** (to preserve original):
   ```bash
   cp plugins/spec-validator/skills/spec-validator/config.yaml \
      plugins/spec-validator/skills/spec-validator/config.custom.yaml
   ```

2. **Edit custom config**:
   ```bash
   vim plugins/spec-validator/skills/spec-validator/config.yaml
   ```

3. **Common customizations**:

   **Adjust dimension weights**:
   ```yaml
   dimensions:
     implementation_completeness:
       total_weight: 50  # Increase from 40 to emphasize completeness
     implementation_quality:
       total_weight: 20  # Decrease from 25
   ```

   **Adjust grade thresholds**:
   ```yaml
   grades:
     A:
       min_score: 95  # Raise from 90 for stricter grading
   ```

   **Add custom parsing patterns**:
   ```yaml
   parsing:
     functional_requirements:
       patterns:
         - regex: '##\s+REQ-(\d+)[:：]\s*(.+)'  # Support REQ-X format
           capture_groups:
             id: 1
             title: 2
   ```

4. **Validate custom config**:
   ```bash
   yamllint plugins/spec-validator/skills/spec-validator/config.yaml
   ```

   **Expected**: No errors

5. **Test with custom config**:
   ```bash
   # Config is loaded automatically on next validation
   /validate --spec test-spec.md
   ```

---

## First Validation

### Create a Test Spec

1. **Create test directory**:
   ```bash
   mkdir -p ~/spec-validator-test
   cd ~/spec-validator-test
   ```

2. **Create test spec** (`test-spec.md`):
   ```markdown
   # Test Feature Specification

   ## FR-1: User Registration (Priority: High)
   Users must be able to register with email and password.

   ## FR-2: User Login (Priority: High)
   Users must be able to login with email and password.

   ## FR-3: Password Reset (Priority: Medium)
   Users can request password reset via email.

   ## NFR-1: Security
   Passwords must be hashed using bcrypt with cost factor 12.

   ## NFR-2: Performance
   API response time must be under 200ms for 95th percentile.

   ## Technical Design

   ### User Model
   - id: UUID
   - email: String
   - password_hash: String
   - created_at: Timestamp

   ## API Endpoints

   - POST /api/auth/register
   - POST /api/auth/login
   - POST /api/auth/reset-password

   ## Edge Cases

   1. Handle duplicate email registration attempts
   2. Handle invalid password format
   3. Handle expired password reset tokens
   ```

3. **Save the file**:
   ```bash
   cat > test-spec.md << 'EOF'
   [paste the content above]
   EOF
   ```

### Generate Checklist

1. **Run validation** (will offer to generate checklist):
   ```bash
   claude
   ```

2. **Type in Claude CLI**:
   ```
   /validate --spec ~/spec-validator-test/test-spec.md
   ```

3. **Expected interaction**:
   ```
   Checklist not found at ~/spec-validator-test/.spec-checklist.yaml

   Would you like to:
   1) Generate template from spec
   2) Specify different path
   3) Exit

   Choice:
   ```

4. **Choose option 1**:
   ```
   1
   ```

5. **Expected output**:
   ```
   Generating checklist template from spec...
   ✓ Found 3 functional requirements
   ✓ Found 2 non-functional requirements
   ✓ Found 1 data model
   ✓ Found 3 API endpoints
   ✓ Found 3 edge cases

   Template saved to: ~/spec-validator-test/.spec-checklist.yaml

   Please update the checklist with implementation status and re-run validation.
   ```

### Update Checklist

1. **Open checklist**:
   ```bash
   vim ~/spec-validator-test/.spec-checklist.yaml
   ```

2. **Update status** (simulate partial implementation):
   ```yaml
   functional_requirements:
     - id: "FR-1"
       title: "User Registration"
       priority: "high"
       status: "completed"  # Changed from not_started
       test_status: "completed"  # Changed from not_started
       implementation_notes: "Implemented in auth/register.py"
       completed_date: "2026-02-13"

     - id: "FR-2"
       title: "User Login"
       priority: "high"
       status: "completed"  # Changed from not_started
       test_status: "in_progress"  # Changed from not_started
       implementation_notes: "Implemented in auth/login.py. Tests incomplete."

     - id: "FR-3"
       title: "Password Reset"
       priority: "medium"
       status: "not_started"  # Keep as not_started
   ```

3. **Save and exit**

### Run First Validation

1. **Run validation**:
   ```
   /validate --spec ~/spec-validator-test/test-spec.md
   ```

2. **Expected output**:
   ```
   === Spec Validation Report ===

   Overall Score: 68/100 (Grade D - Needs work)

   Dimension Scores:
     Implementation Completeness: 26/40 (65%)
     Implementation Quality: 12/25 (48%)
     Spec Adherence: 20/20 (100%)
     Progress Transparency: 10/15 (67%)

   Requirements Status:
     FRs: 2/3 completed (67%)
       High Priority: 2/2 (100%)
       Medium Priority: 0/1 (0%)
     NFRs: 0/2 completed (0%)

   Critical Issues: 0
   Important Issues: 3
     - FR-2: Marked completed but tests not finished
     - NFR-1: Not started
     - NFR-2: Not started

   Minor Issues: 2
     - FR-3: Missing implementation notes
     - 3 edge cases not tracked in checklist

   Report saved to: ~/spec-validator-test/validation-report-20260213-100000.md
   ```

3. **Review the report**:
   ```bash
   cat ~/spec-validator-test/validation-report-*.md
   ```

### Iterate and Improve

1. **Fix an important issue** (complete NFR-1):
   ```yaml
   non_functional_requirements:
     - id: "NFR-1"
       title: "Security"
       status: "completed"
       test_status: "completed"
       implementation_notes: "Using bcrypt with cost factor 12"
       completed_date: "2026-02-13"
   ```

2. **Re-validate**:
   ```
   /validate
   ```

3. **Expected**: Score improves (e.g., from 68 to 74)

4. **Continue iterating** until score >= 90

---

## Testing

### Unit Tests

Create a test suite to verify plugin functionality.

**Test File**: `test-validation.sh`

```bash
#!/bin/bash

# Spec Validator Plugin Test Suite

echo "=== Spec Validator Test Suite ==="

# Test 1: Plugin Installation
echo "Test 1: Checking plugin installation..."
if claude plugins list | grep -q "spec-validator"; then
    echo "✓ Plugin installed"
else
    echo "✗ Plugin not found"
    exit 1
fi

# Test 2: Config File Exists
echo "Test 2: Checking config file..."
if [ -f "plugins/spec-validator/skills/spec-validator/config.yaml" ]; then
    echo "✓ Config file exists"
else
    echo "✗ Config file missing"
    exit 1
fi

# Test 3: Templates Exist
echo "Test 3: Checking templates..."
for template in validation-report-template.md checklist-template.yaml fix-guide.md; do
    if [ -f "plugins/spec-validator/templates/$template" ]; then
        echo "✓ Template $template exists"
    else
        echo "✗ Template $template missing"
        exit 1
    fi
done

# Test 4: YAML Validation
echo "Test 4: Validating config YAML..."
if yamllint plugins/spec-validator/skills/spec-validator/config.yaml; then
    echo "✓ Config YAML valid"
else
    echo "✗ Config YAML invalid"
    exit 1
fi

# Test 5: Test Spec Validation
echo "Test 5: Running test validation..."
# This would require Claude CLI interaction, skipping for now
echo "⊘ Interactive test skipped"

echo ""
echo "=== Test Suite Complete ==="
echo "4/5 tests passed"
```

**Run Tests**:
```bash
chmod +x test-validation.sh
./test-validation.sh
```

### Integration Tests

**Test Checklist**:

- [ ] Install plugin via `npm run link`
- [ ] Verify plugin appears in `claude plugins list`
- [ ] Trigger skill with "validate spec implementation"
- [ ] Trigger command with `/validate`
- [ ] Generate checklist template from spec
- [ ] Validate with full mode
- [ ] Validate with quick mode
- [ ] Validate with requirements-only mode
- [ ] Handle missing spec file gracefully
- [ ] Handle invalid YAML gracefully
- [ ] Detect orphaned checklist items
- [ ] Detect missing checklist items
- [ ] Calculate weighted FR scores correctly
- [ ] Generate readable markdown report
- [ ] Update validation history in checklist
- [ ] Calculate score delta from previous validation
- [ ] Assign correct letter grade

### Regression Tests

**Create Baseline**:
```bash
# Run validation on test spec
/validate --spec test-spec.md > baseline-output.txt

# Save baseline score
grep "Overall Score" baseline-output.txt > baseline-score.txt
```

**Verify After Changes**:
```bash
# Run validation again
/validate --spec test-spec.md > current-output.txt

# Compare scores
diff baseline-score.txt <(grep "Overall Score" current-output.txt)
```

**Expected**: No differences if spec and checklist unchanged

---

## Troubleshooting

### Issue: Plugin Not Found

**Symptom**: `claude plugins list` doesn't show spec-validator

**Solutions**:
1. **Re-link plugin**:
   ```bash
   cd /Users/jaykim/Documents/Projects/claude-ai-engineering
   npm run link
   ```

2. **Check plugin.json**:
   ```bash
   cat plugins/spec-validator/.claude-plugin/plugin.json
   ```
   Verify it's valid JSON with `name: "spec-validator"`

3. **Check Claude config**:
   ```bash
   cat ~/.claude/config.yaml
   ```
   Verify `plugins_path` points to correct directory

### Issue: Trigger Phrase Not Working

**Symptom**: Typing "validate spec implementation" doesn't activate skill

**Solutions**:
1. **Check SKILL.md description**:
   ```bash
   head -n 10 plugins/spec-validator/skills/spec-validator/SKILL.md
   ```
   Verify trigger phrases are in description frontmatter

2. **Restart Claude CLI**:
   ```bash
   claude restart
   ```

3. **Try exact trigger phrase**:
   ```
   validate spec implementation
   ```
   (not "validate the spec" or other variations)

### Issue: Config Not Loading

**Symptom**: Validation uses hardcoded defaults instead of custom config

**Solutions**:
1. **Verify config path**:
   ```bash
   ls -la plugins/spec-validator/skills/spec-validator/config.yaml
   ```

2. **Check YAML syntax**:
   ```bash
   yamllint plugins/spec-validator/skills/spec-validator/config.yaml
   ```

3. **Check file permissions**:
   ```bash
   chmod 644 plugins/spec-validator/skills/spec-validator/config.yaml
   ```

### Issue: Report Not Generating

**Symptom**: Validation completes but no report file created

**Solutions**:
1. **Check output directory permissions**:
   ```bash
   ls -la ~/spec-validator-test/
   chmod 755 ~/spec-validator-test/
   ```

2. **Specify output path explicitly**:
   ```
   /validate --output ~/validation-report.md
   ```

3. **Check disk space**:
   ```bash
   df -h
   ```

### Issue: Parsing Misses Requirements

**Symptom**: Validation report shows 0 FRs found in spec

**Solutions**:
1. **Verify spec format**:
   ```bash
   grep "FR-" test-spec.md
   ```
   Ensure requirements use `FR-X` format

2. **Check parsing patterns** in config.yaml:
   ```yaml
   parsing:
     functional_requirements:
       patterns:
         - regex: '##\s+FR-(\d+)[:：]\s*(.+)'
   ```

3. **Add custom patterns** for your spec format

### Issue: Validation Takes Too Long

**Symptom**: Validation hangs or takes >60 seconds

**Solutions**:
1. **Check spec file size**:
   ```bash
   ls -lh test-spec.md
   ```
   If >10 MB, consider splitting into modules

2. **Use quick mode**:
   ```
   /validate quick
   ```

3. **Increase timeout** in config.yaml:
   ```yaml
   performance:
     parsing_timeout_seconds: 60
   ```

---

## Uninstallation

### Remove Plugin

1. **Unlink plugin**:
   ```bash
   cd /Users/jaykim/Documents/Projects/claude-ai-engineering
   npm run unlink spec-validator
   ```

2. **Delete plugin directory**:
   ```bash
   rm -rf plugins/spec-validator
   ```

3. **Verify removal**:
   ```bash
   claude plugins list
   ```
   **Expected**: spec-validator not in list

### Clean Up Test Files

```bash
rm -rf ~/spec-validator-test
```

---

## Next Steps

After successful installation:

1. **Read README.md**: Comprehensive user documentation
2. **Review examples**: See `README.md` Examples section
3. **Try with real spec**: Use spec-interview to create a spec, then validate
4. **Customize config**: Adjust weights and thresholds for your needs
5. **Integrate into workflow**: Add validation to CI/CD pipeline

---

## Getting Help

If you encounter issues not covered here:

1. **Check fix-guide.md**: Step-by-step solutions for common issues
2. **Review SKILL.md**: Error handling table for specific scenarios
3. **Consult CLAUDE.md**: Architecture and development guide
4. **Open an issue**: Include spec, checklist, error output, and steps to reproduce

---

**Last Updated**: 2026-02-13
**Plugin Version**: 1.0.0
**Author**: Jay Kim
