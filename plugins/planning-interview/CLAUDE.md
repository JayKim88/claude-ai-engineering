# CLAUDE.md - Developer Guide

> Technical documentation for developers, maintainers, and contributors

## Table of Contents

1. [Architecture](#architecture)
2. [Testing Checklist](#testing-checklist)
3. [Customization Guide](#customization-guide)
4. [Question Design Philosophy](#question-design-philosophy)
5. [Template Customization](#template-customization)
6. [Debugging Tips](#debugging-tips)

---

## Architecture

### Design Philosophy

The planning-interview plugin follows **single-skill, multi-mode** architecture:

- **Single skill**: One SKILL.md handles all interview logic
- **Multi-mode**: Branching logic adapts behavior (Solo/Startup/Team)
- **Template-driven**: Output uses static templates with dynamic placeholder filling
- **Stateful**: Session object maintains state across AskUserQuestion rounds
- **Pragmatic scoring**: 1-5 completeness scale drives adaptive follow-ups (Alpha's contribution)

### Core Components

```
┌─────────────────────────────────────────────────┐
│              Plugin Entry Point                  │
│           (.claude-plugin/plugin.json)           │
└──────────────┬──────────────────────────────────┘
               │ Trigger Detection
               ▼
┌─────────────────────────────────────────────────┐
│              SKILL.md Algorithm                  │
│  ┌──────────────────────────────────────────┐  │
│  │ Step 1: Trigger Detection                 │  │
│  │ Step 2: Session Initialization            │  │
│  │ Step 3: Context Detection (3 questions)   │  │
│  │ Step 4: Mode Confirmation                 │  │
│  │ Step 5: Interview Rounds (adaptive)       │  │
│  │   Step 5.4: Completeness Scoring (1-5)    │  │
│  │   Step 5.5: Session Management (Team)     │  │
│  │ Step 6: Optional Helpers (MoSCoW, etc.)   │  │
│  │ Step 7: Completion Detection              │  │
│  │ Step 8: Template Selection & Validation   │  │
│  │ Step 9: Generate PRD                      │  │
│  │ Step 10: Save to File                     │  │
│  │ Step 11: Error Handling                   │  │
│  └──────────────────────────────────────────┘  │
└──────────────┬──────────────────────────────────┘
               │ Template Selection
               ▼
┌─────────────────────────────────────────────────┐
│                  Templates                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │lean-     │  │product-  │  │full-prd  │     │
│  │canvas.md │  │brief.md  │  │.md       │     │
│  │(23 plc)  │  │(35 plc)  │  │(50+ plc) │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → Trigger detected
2. **Context Gathering** → 3 questions determine mode
3. **Interview Loop** → N rounds of AskUserQuestion (N by mode)
4. **Answer Scoring** → 1-5 completeness score per answer (drives follow-ups)
5. **Answer Storage** → All responses in session.answers
6. **Validation** → Check for missing data
7. **Template Loading** → Select appropriate template
8. **Placeholder Filling** → Map session.answers to placeholders
9. **File Write** → Save PRD to filesystem

### State Management

**Session Object:**

```javascript
{
  mode: "Solo" | "Startup" | "Team",
  answers: {
    problem_and_goals: "...",
    solution_and_strategy: "...",
    users_and_market: "...",
    constraints_and_priorities: "...",
    success_metrics: "...",
    moscow_prioritization: {...}
  },
  current_round: 0,
  max_rounds: 3-4 | 5-6 | 8-9,
  completeness_score: {  // Alpha's 1-5 scoring
    problem_and_goals: 5,
    solution_and_strategy: 3,
    users_and_market: 4,
    // ...
  },
  template_type: "lean-canvas" | "product-brief" | "full-prd",
  project_name: "...",
  start_time: 1739577600000,
  language: "en" | "ko",
  quick_mode: false
}
```

---

## Testing Checklist

### Core Functionality Tests (1-5)

**Test 1: Solo Mode End-to-End**

- **Input**: "planning interview" → answer context for Solo mode
- **Expected**:
  - 3 context questions
  - Solo mode recommended
  - 3-4 interview rounds
  - Lean Canvas generated (10 sections)
  - File saved as `lean-canvas-{project}-{date}.md`
- **Validation**:
  - All 10 sections present
  - No `[TODO]` if all questions answered well
  - Completeness scores tracked (check session state)

**Test 2: Startup Mode End-to-End**

- **Input**: "PRD for B2B SaaS analytics platform" (Quick Mode)
- **Expected**:
  - Quick Mode auto-selects Startup
  - 5-6 interview rounds
  - Product Brief (12 sections)
  - File saved as `product-brief-{project}-{date}.md`

**Test 3: Team Mode End-to-End**

- **Input**: "기획해줘" (Korean) → answer for Team mode
- **Expected**:
  - Context questions in Korean
  - Team mode (8-9 rounds)
  - Session save offered after round 3, 6
  - Full PRD (13 sections) with Korean headers

**Test 4: Completeness Scoring & Follow-ups**

- **Input**: Provide vague answers (< 10 words, generic terms)
- **Expected**:
  - Completeness score < 3 triggers follow-up
  - Follow-up from same category
  - After follow-up, score updates
  - If still < 3, accept and mark `[TODO]`
- **Validation**:
  - Check `session.completeness_score` values
  - Verify follow-up logic (1 follow-up per low score)

**Test 5: File Saving**

- **Input**: Complete Solo mode, choose save options
- **Expected**:
  - Default filename option works
  - Custom path option works
  - Preview first option shows content
- **Validation**:
  - File exists at specified location
  - Filename format: `{mode}-{project-slug}-{YYYYMMDD}.md`

---

### Edge Case Tests (6-10)

**Test 6: Quick Mode Bypass**

- **Input**: "Lean Canvas for mobile recipe app"
- **Expected**:
  - Skips context questions
  - Auto-selects Solo mode
  - Jumps to interview rounds

**Test 7: Template File Missing Fallback**

- **Setup**: Delete `templates/lean-canvas.md`
- **Input**: Complete Solo mode interview
- **Expected**:
  - Error handler uses embedded default
  - Warning: "Template file not found"
  - PRD still generates

**Test 8: "I Don't Know" Handling**

- **Input**: Answer 2-3 questions with "I don't know"
- **Expected**:
  - Accepts "I don't know" without follow-up loop
  - Marks `[TODO: Research needed - {topic}]`
  - PRD generated with clear gaps

**Test 9: Mid-Interview Mode Switching**

- **Input**: Start Solo, after 2 rounds say "Actually, switch to Team mode"
- **Expected**:
  - Confirms mode switch
  - Preserves first 2 rounds
  - Adjusts max_rounds
  - Final PRD uses Team template with all answers

**Test 10: Session Resume**

- **Input**: Team mode, complete 3 rounds, choose "Save and resume"
- **In new conversation**: "continue planning interview"
- **Expected**:
  - Finds most recent draft file
  - Loads session JSON
  - Continues from round 4
  - Final PRD includes all answers

---

## Customization Guide

### Adding New Question Categories

**Use Case:** Add "Technical Feasibility" category to Team mode

**Steps:**

1. **Update question allocation table in SKILL.md Step 5:**

```markdown
| Category | Solo | Startup | Team |
|----------|------|---------|------|
| ... existing ... |
| Technical Feasibility | 0 | 0 | 1 |
```

2. **Add question example in Step 5.3:**

```markdown
**Round X: Technical Feasibility**

\`\`\`
AskUserQuestion(
  "What are the key technical constraints or dependencies? Are there any technical risks?",
  allow_freeform=true
)
\`\`\`
```

3. **Update template:** Add section to `templates/full-prd.md`

4. **Test:** Run Test 3 (Team mode) and verify new section

---

### Adjusting Completeness Scoring Thresholds

**Use Case:** Your users are technical and provide short but precise answers. Current threshold (word_count < 10) triggers too many false positives.

**Steps:**

1. **Edit SKILL.md Step 5.4:**

```pseudocode
// OLD
if word_count(answer) < 10:
  score = min(score, 2)

// NEW
if word_count(answer) < 5:  // Only flag very short
  score = min(score, 2)
```

2. **Add technical term whitelist:**

```pseudocode
technical_terms = ["API", "CLI", "SaaS", "MVP", "KPI"]
if contains_technical_terms(answer, technical_terms):
  score = min(score + 1, 5)  // Bonus for technical specificity
```

3. **Test:** Run Test 4 with short technical answers (e.g., "REST API for B2B SaaS, OAuth 2.0, 99.9% SLA")

---

### Modifying Round Counts

**Use Case:** Solo mode feels too short, want 5-6 rounds instead of 3-4

**Steps:**

1. **Update SKILL.md Step 5 allocation table:**

Change Solo column to sum to 5-6 rounds

2. **Add more question examples in Step 5.1**

3. **Update README.md comparison table:**

```markdown
| **Duration** | 20-25 min (was 15-20) |
| **Interview Rounds** | 5-6 rounds (was 3-4) |
```

4. **Test:** Run Test 1 and verify 5-6 rounds executed

---

## Question Design Philosophy

### Good vs Bad Questions

**Good Questions:**

1. **Specific and actionable**
   - Good: "Who is your primary target user? Be specific about their role, company size, and current workflow."
   - Bad: "Who is your target user?"

2. **Encourage concrete examples**
   - Good: "What problem does this solve? Describe a time when your target user faced this issue."
   - Bad: "What problem does this solve?"

3. **Request quantification**
   - Good: "What's your North Star metric? What quantitative target would prove product-market fit (e.g., '1000 MAU with 40% retention')?"
   - Bad: "How will you measure success?"

4. **Avoid yes/no questions**
   - Good: "What's the total addressable market size? How many potential customers exist?"
   - Bad: "Is there a market for this?"

5. **Focus on WHY, not HOW**
   - Good: "What technical constraints might limit delivery? (e.g., legacy systems, compliance, scalability)"
   - Bad: "What tech stack will you use?" (That's spec-interview)

---

## Template Customization

### Adding Company Branding

**Use Case:** Want all PRDs to include company logo and branding

**Steps:**

1. **Edit template header in `templates/product-brief.md`:**

```markdown
![YourCompany Logo](https://yourcompany.com/logo.png)

# {PROJECT_NAME} - Product Brief

**Company:** YourCompany, Inc.
...
```

2. **Add footer:**

```markdown
**YourCompany Product Management Office**
*For questions, contact: product@yourcompany.com*
```

3. **Test:** Generate Product Brief and verify branding

---

### Creating New Templates

**Use Case:** Want "Feature Spec" template for mid-sized features

**Steps:**

1. **Create `templates/feature-spec.md`:**

```markdown
# {PROJECT_NAME} - Feature Specification

## 1. Overview
{OVERVIEW}

## 2. User Story
{USER_STORY}

## 3. Requirements
{REQUIREMENTS}

## 4. Success Metrics
{SUCCESS_METRICS}
```

2. **Add "Feature" mode to SKILL.md Step 4**

3. **Define question allocation** (e.g., 3-4 rounds, 20 min)

4. **Update template selection in Step 8**

5. **Test:** Trigger Feature mode and verify template used

---

## Debugging Tips

### Enable Verbose Logging

Add to SKILL.md Step 2:

```pseudocode
session.debug_mode = true

if session.debug_mode:
  log("Session:", session)
  log("Current round:", session.current_round)
  log("Completeness scores:", session.completeness_score)
```

### Inspect Session State

Ask Claude: "Show me the current session state"

```json
{
  "mode": "Startup",
  "current_round": 3,
  "completeness_score": {
    "problem_and_goals": 5,
    "solution_and_strategy": 3,
    "users_and_market": 4
  },
  "answers": { ... }
}
```

### Common Issues

| Issue | Likely Cause | Debug Steps |
|-------|--------------|-------------|
| No trigger detected | Typo in trigger phrase | Check exact spelling, try Quick Mode |
| Wrong mode selected | Context scoring logic | Review Step 3 answers, check rubric |
| Template not filled | Placeholder mapping incorrect | Inspect `session.answers` keys vs `{PLACEHOLDERS}` |
| Too many follow-ups | Scoring threshold too strict | Review Step 5.4 heuristics, lower threshold |
| Session resume fails | JSON corrupted | Check draft file footer, validate JSON |

---

## Contributing

### Development Workflow

1. Fork repository
2. Create branch: `git checkout -b feature/new-category`
3. Make changes: Edit SKILL.md, templates, or README
4. Test: Run Tests 1-3 minimum (all modes end-to-end)
5. Update docs: Sync CLAUDE.md, README.md
6. Commit: `git commit -m "feat: add technical feasibility category"`
7. Push: `git push origin feature/new-category`
8. Pull Request: Submit with test results

### Review Checklist

- [ ] All tests pass (minimum Tests 1-3)
- [ ] No breaking changes to templates
- [ ] README.md updated if user-facing change
- [ ] CLAUDE.md updated if internal logic change
- [ ] Examples still render correctly
- [ ] Commit messages follow conventional commits

---

## Versioning

**Semantic Versioning:**

- **Major (2.0.0)**: Breaking changes to algorithm or templates
- **Minor (1.1.0)**: New features (mode, helper, language)
- **Patch (1.0.1)**: Bug fixes, docs, heuristic tuning

**Upgrade Path:**

1. Update `version` in plugin.json and SKILL.md
2. Add changelog section to README.md
3. Tag commit: `git tag v1.1.0`
4. Release notes: What's new, breaking changes, migration guide

---

## Support

- **Issues**: https://github.com/your-org/claude-plugins/issues
- **Discussions**: https://github.com/your-org/claude-plugins/discussions

---

**Last Updated:** 2026-02-15
**Version:** 1.0.0 (Fused Implementation)