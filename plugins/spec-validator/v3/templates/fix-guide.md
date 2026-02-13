# Spec Validation Fix Guide

This guide provides step-by-step instructions for fixing common validation issues identified in spec validation reports.

---

## Critical Issues

### Issue: Missing High-Priority Functional Requirements

**Problem**: High-priority FRs are not implemented or not tracked in the checklist.

**Why It Matters**: High-priority requirements are critical for MVP and block other features.

**Fix Steps**:
1. Review the validation report to identify missing high-priority FRs
2. For each missing FR:
   - If not started: Add to checklist with `status: not_started` and add to sprint backlog
   - If implemented but not tracked: Update checklist to `status: completed` and add implementation notes
   - If partially done: Mark as `status: in_progress` and document what's remaining
3. Re-validate to confirm the issue is resolved

**Example Fix**:
```yaml
functional_requirements:
  - id: "FR-1"
    title: "User authentication with email and password"
    priority: "high"
    status: "in_progress"  # Updated from not_started
    test_status: "not_started"
    implementation_notes: "Login endpoint implemented. Still need password reset flow."
    blockers: ""
    completed_date: null
```

---

### Issue: Orphaned Checklist Items

**Problem**: Items exist in the checklist but not in the spec document.

**Why It Matters**: Indicates the checklist is out of sync with the spec, leading to tracking drift.

**Fix Steps**:
1. Review the orphaned items list in the validation report
2. For each orphaned item:
   - **Option A**: If the spec is outdated, update the spec to include this requirement
   - **Option B**: If the item is no longer needed, remove it from the checklist
   - **Option C**: If the item belongs to a different spec, move it to the correct checklist
3. Document the decision in a comment
4. Re-validate to ensure sync score improves

**Example Fix**:
```yaml
# BEFORE (orphaned)
functional_requirements:
  - id: "FR-99"
    title: "Feature that was removed from spec"
    status: "not_started"

# AFTER (removed because no longer in spec)
# Removed FR-99 as it was deprecated in spec v2.0
```

---

### Issue: Invalid YAML Structure

**Problem**: Checklist YAML has syntax errors or missing required sections.

**Why It Matters**: Parser cannot read the checklist, validation cannot proceed.

**Fix Steps**:
1. Note the specific YAML error from the validation report (line number, column)
2. Open the checklist file and navigate to the error location
3. Common issues:
   - Indentation errors (use spaces, not tabs; 2-space indents)
   - Missing colons after keys
   - Unclosed quotes
   - Invalid YAML characters in values
4. Use an online YAML validator or IDE YAML plugin to verify syntax
5. Ensure all required sections are present:
   - `metadata`
   - `functional_requirements`
   - `non_functional_requirements`
6. Re-validate to confirm parsing succeeds

**Example Fix**:
```yaml
# BEFORE (invalid)
functional_requirements:
- id: FR-1
  title: Missing quotes and colon in status
  status not_started

# AFTER (valid)
functional_requirements:
  - id: "FR-1"
    title: "Missing quotes and colon in status"
    status: "not_started"
```

---

### Issue: Synchronization Error (>10% items out of sync)

**Problem**: Large mismatch between spec and checklist items.

**Why It Matters**: Suggests major drift between planning and tracking, undermining validation accuracy.

**Fix Steps**:
1. Regenerate the checklist template from the current spec:
   ```
   /validate --spec spec.md  # Will offer to generate template
   ```
2. Compare the new template with your existing checklist
3. Merge manually:
   - Copy implementation status and notes from old checklist
   - Use structure from new template
   - Mark new items as `not_started`
   - Remove orphaned items
4. Update `metadata.last_updated` and `metadata.checklist_version`
5. Re-validate to confirm sync

**Example Merge**:
```yaml
# OLD CHECKLIST (has status/notes)
  - id: "FR-1"
    status: "completed"
    implementation_notes: "Done using JWT"

# NEW TEMPLATE (has correct structure from spec)
  - id: "FR-1"
    title: "User authentication"
    priority: "high"

# MERGED
  - id: "FR-1"
    title: "User authentication"
    priority: "high"
    status: "completed"
    implementation_notes: "Done using JWT"
```

---

## Important Issues

### Issue: Missing Medium-Priority Functional Requirements

**Problem**: Medium-priority FRs are incomplete.

**Why It Matters**: Important features that improve user experience or system capability.

**Fix Steps**:
1. Prioritize missing medium-priority FRs in your backlog
2. For each FR:
   - Add to sprint plan if resources available
   - Mark as `in_progress` when work begins
   - Update `implementation_notes` with progress details
3. Consider if any can be downgraded to low priority (discuss with stakeholders)
4. Re-validate after completing a few medium-priority FRs

---

### Issue: Untested Completed Items

**Problem**: Items marked `status: completed` but `test_status: not_started` or `in_progress`.

**Why It Matters**: Claiming completion without tests leads to undetected bugs and regressions.

**Fix Steps**:
1. Review the untested completed items list
2. For each item:
   - If tests exist but weren't tracked: Update `test_status` to reflect reality
   - If no tests: Write tests before claiming completion
   - Update test breakdown (unit/integration/e2e) if applicable
3. Make it a policy: "Completed" means "tested"
4. Re-validate to improve quality score

**Example Fix**:
```yaml
# BEFORE (completed but untested)
  - id: "FR-3"
    status: "completed"
    test_status: "not_started"

# AFTER (tests added)
  - id: "FR-3"
    status: "completed"
    test_status: "completed"
    implementation_notes: "Implemented in auth.py"
    tests:
      unit: "completed"
      integration: "completed"
      e2e: "in_progress"
```

---

### Issue: Missing Non-Functional Requirements

**Problem**: NFRs from the spec are not implemented or tracked.

**Why It Matters**: NFRs affect system quality, performance, and reliability.

**Fix Steps**:
1. Review missing NFRs in the validation report
2. Assess impact and priority (some NFRs are critical, others can wait)
3. For each missing NFR:
   - Add to checklist if not present
   - Update status based on current state
   - Add measurement criteria in implementation notes
4. Consider automated monitoring for NFRs (response time, uptime, etc.)
5. Re-validate

**Example Fix**:
```yaml
non_functional_requirements:
  - id: "NFR-1"
    title: "API response time under 200ms for 95th percentile"
    status: "in_progress"
    test_status: "in_progress"
    implementation_notes: "Currently at 250ms. Added database indexing, reduced by 50ms. Next: add caching."
    blockers: "Need Redis setup in staging environment"
    completed_date: null
```

---

### Issue: Priority Mismatches

**Problem**: Spec says an FR is high priority, but checklist says medium or low (or vice versa).

**Why It Matters**: Misaligned priorities lead to incorrect weighting in scoring.

**Fix Steps**:
1. Review priority mismatch list in validation report
2. For each mismatch:
   - Check the spec for the correct priority
   - Update the checklist to match
   - If the spec is wrong, update the spec and document the change
3. Ensure consistency: Always treat spec as source of truth
4. Re-validate to improve adherence score

**Example Fix**:
```yaml
# SPEC says: FR-2: User Profile Management (Priority: High)

# BEFORE (mismatched)
  - id: "FR-2"
    title: "User Profile Management"
    priority: "medium"  # Wrong

# AFTER (corrected)
  - id: "FR-2"
    title: "User Profile Management"
    priority: "high"  # Matches spec
```

---

### Issue: Blocked Without Reason

**Problem**: Items have `status: blocked` but `blockers` field is empty or vague.

**Why It Matters**: Team cannot help unblock if they don't know what's blocking progress.

**Fix Steps**:
1. Review blocked items in validation report
2. For each blocked item:
   - Document specific blocker (dependency, missing resource, technical issue)
   - Include who/what can unblock (person, team, decision)
   - Add target unblock date if known
3. Escalate blockers to team leads or stakeholders
4. Re-validate to improve transparency score

**Example Fix**:
```yaml
# BEFORE (blocked but unclear)
  - id: "FR-5"
    status: "blocked"
    blockers: "issues"

# AFTER (clear blocker)
  - id: "FR-5"
    status: "blocked"
    blockers: "Waiting on API key from third-party vendor (Stripe). Requested 2026-02-10. Expected by 2026-02-15. Contact: vendor-support@stripe.com"
    implementation_notes: "Implementation ready, just need credentials to test integration."
```

---

## Minor Issues

### Issue: Missing Low-Priority Functional Requirements

**Problem**: Low-priority FRs are incomplete.

**Why It Matters**: Nice-to-have features, not critical for MVP.

**Fix Steps**:
1. Review low-priority FRs in backlog
2. Decide whether to:
   - Defer to next release
   - Implement if time permits
   - Remove from spec if no longer needed
3. Update checklist status to reflect decision
4. Re-validate

---

### Issue: Incomplete Implementation Notes

**Problem**: Many items lack meaningful implementation notes.

**Why It Matters**: Notes provide context for future developers and help with maintenance.

**Fix Steps**:
1. Go through implemented items
2. Add notes covering:
   - Key implementation decisions
   - Technologies/libraries used
   - File locations
   - Known limitations or workarounds
3. Keep notes concise but informative
4. Re-validate to improve transparency score

**Example Fix**:
```yaml
# BEFORE (no notes)
  - id: "FR-7"
    status: "completed"
    implementation_notes: ""

# AFTER (informative notes)
  - id: "FR-7"
    status: "completed"
    implementation_notes: "Implemented using WebSocket (socket.io) for real-time updates. Connection management in src/websocket.ts. Falls back to polling if WebSocket unavailable. Max 100 concurrent connections per server."
```

---

### Issue: Missing Validation History

**Problem**: No validation history tracked in checklist.

**Why It Matters**: History shows progress trends and accountability.

**Fix Steps**:
1. Run your first validation (this will create the history section)
2. Run periodic validations to build trend data
3. Aim for upward trend in scores
4. Use history to demonstrate progress in standups/reviews
5. Re-validate regularly

**Example History**:
```yaml
validation_history:
  - date: "2026-02-13T10:30:00Z"
    score: 75
    grade: "C"
    dimensions:
      completeness: 28
      quality: 18
      adherence: 17
      transparency: 12
    mode: "full"
    validator_version: "1.0.0"
```

---

## General Best Practices

### 1. Validate Early and Often

- Run quick validations daily or after major features
- Run full validations before sprint reviews or releases
- Track score trends, aim for continuous improvement

### 2. Keep Spec and Checklist in Sync

- Update checklist immediately when spec changes
- If you implement something not in the spec, add it to the spec first
- Use spec as single source of truth

### 3. Meaningful Status Updates

- Don't mark items as "completed" until fully tested
- Use "in_progress" to show active work
- Document blockers immediately when they occur
- Update notes as you implement, not after the fact

### 4. Prioritize Critical Issues First

- Fix Critical issues before Important issues
- Fix Important issues before Minor issues
- Re-validate after each fix batch to track improvement

### 5. Use Validation Modes Strategically

- **full**: Before releases, sprint reviews
- **quick**: Daily standup checks
- **requirements-only**: Sprint progress tracking

### 6. Set Score Targets

- MVP: Aim for score >= 70 (Grade C)
- Release: Aim for score >= 90 (Grade A)
- Production: Maintain score >= 85 (Grade B)

### 7. Review Validation Reports as a Team

- Share validation reports in standups
- Discuss trends (improving vs. declining)
- Celebrate when score reaches new milestones
- Use reports to identify where to focus effort

---

## Troubleshooting

### Validation won't run

1. Check spec file path is correct
2. Verify spec file is not empty
3. Ensure checklist is valid YAML (use online validator)
4. Check file permissions (read/write access)

### Scores seem wrong

1. Review config.yaml to verify weights
2. Check if correct validation mode was used
3. Ensure priorities in checklist match spec
4. Verify status values are valid (completed/in_progress/not_started/blocked)

### Checklist won't update

1. Check file write permissions
2. Ensure checklist is not open in another program
3. Verify YAML structure is valid before update
4. Check validation report for errors

### History not tracking

1. Verify `validation_history` section exists in checklist
2. Check that validation completed successfully (no errors)
3. Ensure file write succeeded (check validation output)
4. Manually add history section if missing

---

## Example: Full Fix Workflow

**Scenario**: Validation report shows score of 65/100 (Grade D)

**Critical Issues**:
- 2 high-priority FRs not started
- 5 orphaned checklist items

**Important Issues**:
- 8 completed items with no tests
- 3 blocked items without blocker explanations

**Minor Issues**:
- 15 items missing implementation notes

**Fix Steps**:

1. **Fix Critical Issues First**:
   ```bash
   # Add the 2 high-priority FRs to sprint backlog
   # Update checklist status to "in_progress" for both
   # Remove the 5 orphaned items from checklist
   # Re-validate: /validate quick
   # Expected score: ~72/100 (Grade C)
   ```

2. **Fix Important Issues**:
   ```bash
   # Write tests for the 8 completed items
   # Update test_status to "completed"
   # Document blockers for the 3 blocked items
   # Re-validate: /validate
   # Expected score: ~82/100 (Grade B)
   ```

3. **Fix Minor Issues** (if time permits):
   ```bash
   # Add implementation notes to the 15 items
   # Re-validate: /validate
   # Expected score: ~86/100 (Grade B)
   ```

4. **Finish High-Priority FRs**:
   ```bash
   # Complete the 2 high-priority FRs
   # Update status to "completed" with tests
   # Re-validate: /validate
   # Expected score: ~93/100 (Grade A)
   ```

**Result**: Improved from Grade D to Grade A in 4 iterations, ready to ship!

---

## Need Help?

If you encounter issues not covered in this guide:
1. Check the validation report for specific error messages
2. Review the SKILL.md error handling table
3. Consult the config.yaml for customization options
4. Open an issue with reproduction steps

---

**Last Updated**: 2026-02-13
**Plugin Version**: 1.0.0
