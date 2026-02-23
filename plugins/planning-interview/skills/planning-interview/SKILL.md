---
name: planning-interview
description: Conducts adaptive product planning interviews to generate comprehensive PRDs (Lean Canvas, Product Brief, or Full PRD) based on user context
version: 1.0.0
author: Fused Implementation (Alpha + Beta)
model: claude-opus-4-6
fallback_model: claude-sonnet-4-5
---

# Planning Interview Skill

## Purpose

Transform vague product ideas into actionable PRDs through context-aware, business-focused interviews. Adapts question depth and template complexity based on user type (Solo Builder / Startup Founder / Product Manager).

## Model Selection

- **Recommended**: `claude-opus-4-6` - Nuanced follow-up questions, business insight synthesis, subtle vague answer detection
- **Acceptable**: `claude-sonnet-4-5` - Faster interviews, may miss some subtle vagueness patterns
- **Use Opus for**: Team mode (requires deep strategic thinking), users with complex business models
- **Use Sonnet for**: Solo mode (quick iterations), technically-focused users who provide concrete answers

## Algorithm

### Step 1: Trigger Detection

Detect trigger phrases to initiate planning interview:

**English triggers:**
- "planning interview"
- "PRD" or "product requirements"
- "product planning"
- "help me plan [product/feature]"
- "create a PRD for [X]"

**Korean triggers:**
- "기획해줘" or "기획 도와줘"
- "제품 기획 도와줘"
- "PRD 만들어줘"

**Quick Mode triggers** (auto-select mode, skip context detection):
- "PRD for B2B SaaS" → Startup mode
- "Lean Canvas for mobile app" → Solo mode
- "Full PRD for enterprise" → Team mode

Upon detection, proceed to Step 2.

---

### Step 2: Initialize Session

Create session state to track interview progress:

```
session = {
  mode: null,              // Solo / Startup / Team (determined in Step 4)
  answers: {},             // Store all user responses by category
  current_round: 0,        // Track interview progress
  max_rounds: null,        // Set based on mode (3-4 / 5-6 / 8-9)
  completeness_score: {},  // Track answer quality per category (1-5 scale)
  template_type: null,     // lean-canvas / product-brief / full-prd
  project_name: null,      // Derived from user input
  start_time: timestamp,   // Run `date '+%Y-%m-%d %H:%M'` to get exact time. Never estimate.
  language: detect_from_trigger(), // 'en' or 'ko'
  quick_mode: false        // true if triggered via Quick Mode
}
```

**Language detection:**
- If trigger phrase is Korean → set `language = 'ko'`
- If trigger phrase is English → set `language = 'en'`

**Quick Mode initialization:**
- If triggered via Quick Mode pattern → set `quick_mode = true`, set `mode`, skip to Step 5
- Otherwise → proceed to Step 3

---

### Step 3: Context Detection (Mode Selection)

Ask 3 context questions to determine appropriate mode.

**Context Question 1: Team Size**

English:
```
AskUserQuestion(
  "Let's start by understanding your context. How many people are working on this product?",
  options=["Just me (solo)", "2-10 people (small team)", "10+ people (established team)"],
  allow_freeform=false
)
```

Korean:
```
AskUserQuestion(
  "먼저 상황을 파악하겠습니다. 이 제품을 개발하는 팀 규모는 어떻게 되나요?",
  options=["혼자 (1인)", "2-10명 (소규모)", "10명 이상 (중대규모)"],
  allow_freeform=false
)
```

**Context Question 2: Stakeholder Buy-in**

English:
```
AskUserQuestion(
  "Do you need to get buy-in from investors, executives, or other stakeholders for this product?",
  options=["No, I'm deciding on my own", "Yes, need to convince a few people", "Yes, need formal approval from multiple stakeholders"],
  allow_freeform=false
)
```

**Context Question 3: Launch Timeline**

English:
```
AskUserQuestion(
  "What's your target timeline to launch or ship this?",
  options=["< 3 months (fast iteration)", "3-6 months (standard)", "6+ months (strategic initiative)"],
  allow_freeform=false
)
```

**Scoring rubric:**

| Answer Pattern | Mode Selection |
|----------------|----------------|
| Just me + No buy-in + < 3 months | **Solo** (Lean Canvas, 15-20 min) |
| 2-10 people + Few people + 3-6 months | **Startup** (Product Brief, 25-30 min) |
| 10+ people + Multiple stakeholders + 6+ months | **Team** (Full PRD, 35-45 min) |

Proceed to Step 4.

---

### Step 4: Mode Confirmation

Present recommended mode with preview.

**English:**
```
"Based on your answers, I recommend **{MODE} mode** ({DURATION}, produces {OUTPUT}).

**{MODE} mode** will cover:
{MODE_SPECIFIC_TOPICS}

Shall we proceed with **{MODE} mode**?"
```

```
AskUserQuestion(
  "Proceed with {mode} mode?",
  options=["{mode} mode (recommended)", "Solo mode", "Startup mode", "Team mode"],
  allow_freeform=false
)
```

Set `session.mode`, `session.max_rounds`, `session.template_type` based on confirmation.

Proceed to Step 5.

---

### Step 5: Conduct Interview Rounds

Execute adaptive interview based on selected mode. Questions organized into 5 categories:

1. **Problem & Business Goals** - Why this product? What problem does it solve?
2. **Solution & Product Strategy** - What are you building? Core value proposition?
3. **Users & Market** - Who is this for? Market size? Competition?
4. **Constraints & Priorities** - Limitations? Must-haves vs nice-to-haves?
5. **Success Metrics** - How measure success? North Star metric?

**Question allocation by mode:**

| Category | Solo | Startup | Team |
|----------|------|---------|------|
| Problem & Business Goals | 1 question | 2 questions | 2 questions |
| Solution & Product Strategy | 1 question | 1 question | 2 questions |
| Users & Market | 1 question | 2 questions | 2 questions |
| Market & Competition | 0 | 1 question | 1 question |
| Constraints & Priorities | 1 question | 1 question | 1 question |
| Success Metrics | 0 | 1 question | 1 question |
| **Total rounds** | **3-4** | **5-6** | **8-9** |

For each round:
1. Select question from category pool
2. Ask question using AskUserQuestion
3. Score answer completeness (1-5 scale, see Step 5.4)
4. If score <3, ask follow-up from same category
5. Store answer in session.answers[category]
6. Increment session.current_round

After every 3 rounds (Team mode only), offer session save (Step 5.5).

---

### Step 5.1: Solo Mode Question Examples

**Round 1: Problem & Business Goals**

```
AskUserQuestion(
  "What specific problem does this product solve? Describe a time when your target user faced this issue.",
  allow_freeform=true
)
```

**Round 2: Solution & Product Strategy**

```
AskUserQuestion(
  "What's your proposed solution in one sentence? What makes it different from existing alternatives?",
  allow_freeform=true
)
```

**Round 3: Users & Market**

```
AskUserQuestion(
  "Who is your primary target user? Be specific about their role, needs, and current workarounds.",
  allow_freeform=true
)
```

**Round 4: Constraints & Priorities**

```
AskUserQuestion(
  "For your MVP, what's the absolute minimum feature set needed to validate the core value? What can wait for v2?",
  allow_freeform=true
)
```

---

### Step 5.2: Startup Mode Question Examples

**Round 1: Problem & Business Goals (2 questions)**

Q1:
```
AskUserQuestion(
  "What business opportunity or market gap are you addressing? What's the total addressable market size?",
  allow_freeform=true
)
```

Q2:
```
AskUserQuestion(
  "What specific pain point costs your target customer the most time or money today?",
  allow_freeform=true
)
```

**Round 2: Solution & Product Strategy**

```
AskUserQuestion(
  "Describe your product's core value proposition. If you had 30 seconds in an elevator, how would you pitch it?",
  allow_freeform=true
)
```

**Round 3: Users & Market (2 questions)**

Q1:
```
AskUserQuestion(
  "Who are your primary and secondary user personas? What are their goals, pain points, and current tools?",
  allow_freeform=true
)
```

Q2:
```
AskUserQuestion(
  "What's your go-to-market strategy? How will you acquire your first 100 customers?",
  allow_freeform=true
)
```

**Round 4: Market & Competition**

```
AskUserQuestion(
  "Who are your top 3 competitors or alternatives? What's your unique differentiation?",
  allow_freeform=true
)
```

**Round 5: Success Metrics**

```
AskUserQuestion(
  "What's your North Star metric? What quantitative goal would prove product-market fit?",
  allow_freeform=true
)
```

---

### Step 5.3: Team Mode Question Examples

**Round 1: Problem & Business Goals (2 questions)**

Q1:
```
AskUserQuestion(
  "How does this product align with our company's strategic objectives? What executive priority does it support?",
  allow_freeform=true
)
```

Q2:
```
AskUserQuestion(
  "What customer pain point or business problem are we solving? What's the cost of not solving it?",
  allow_freeform=true
)
```

**Round 2-6**: Similar structure with questions about solution strategy, users/market, competition, constraints, and metrics.

---

### Step 5.4: Answer Completeness Scoring (Alpha's 1-5 Scale)

After each user response, score answer completeness:

**Scoring heuristic:**

```pseudocode
function scoreAnswerCompleteness(answer, question_category):
  score = 5  // Start optimistic

  // Check 1: Length
  word_count = count_words(answer)
  if word_count < 10:
    score = min(score, 2)  // Very short
  else if word_count < 20:
    score = min(score, 3)  // Brief

  // Check 2: Specificity
  generic_terms = ["thing", "stuff", "better", "easier", "faster", "improve"]
  if contains_only_generic_terms(answer, generic_terms) AND lacks_examples(answer):
    score = min(score, 2)  // Too vague

  // Check 3: Metrics (if applicable)
  if asks_for_metrics(question_category) AND not_contains_numbers(answer):
    score = min(score, 3)  // Missing quantification

  // Check 4: Examples
  if has_concrete_example(answer):
    score = min(score + 1, 5)  // Bonus for examples

  return score
```

**Examples:**

| Answer | Word Count | Score | Reason |
|--------|-----------|-------|--------|
| "It's better for users." | 4 | 1 | Too short, generic, no specifics |
| "Developers waste 2-3 hours/day searching across 5 tools for API docs. This consolidates them." | 14 | 5 | Specific metrics, concrete example |
| "Users will be happier and more productive." | 7 | 2 | Short, vague, no metrics |

**Follow-up strategy:**

If category score < 3:
1. Ask targeted follow-up from same category
2. Update completeness score
3. If still < 3 after 1 follow-up, accept and proceed (mark section with `[TODO]`)

Store scores in `session.completeness_score[category]`.

---

### Step 5.5: Session Management (Team Mode Only)

After every 3 rounds in Team mode, offer save point:

```
"We're {percentage}% through the interview. Want to take a break?

Options:
- Continue now (we'll finish in ~{remaining_time} min)
- Save and resume later"
```

If user chooses "Save":
1. Generate draft filename: `planning-interview-draft-{project_slug}-{timestamp}.md`
2. Write session state with JSON footer
3. Resume trigger: "continue planning interview"

---

### Step 6: Optional Helpers

**Helper 6.1: MoSCoW Prioritization (All modes)**

If user mentioned multiple features, offer:

```
"I noticed you mentioned several features. Would you like help prioritizing them using the MoSCoW framework? (Takes 5 min)"
```

**Algorithm:**
1. Extract all features mentioned
2. For each feature, ask classification:

```
AskUserQuestion(
  "How would you classify these features?\n\n1. {feature_1}\n2. {feature_2}\n...",
  multiSelect=[
    {id: "feature_1", text: "{feature_1}", options: ["Must", "Should", "Could", "Won't"]}
  ]
)
```

3. Store in `session.answers.moscow_prioritization`

---

### Step 7: Detect Completion

Interview complete when:

**Condition 1: Content threshold reached**
- All required categories have ≥20 word responses
- Solo: 4 categories, Startup: 5 categories, Team: 7 categories

**Condition 2: User explicitly completes**
- User says: "done", "finish", "generate the PRD now"

**Condition 3: Max rounds reached**
- `session.current_round >= session.max_rounds`

Confirm with user before proceeding to Step 8.

---

### Step 8: Select & Validate Template

Based on session.mode, load appropriate template:

| Mode | Template File | Sections | Required Placeholders |
|------|---------------|----------|----------------------|
| Solo | `templates/lean-canvas.md` | 10 sections | 23 placeholders |
| Startup | `templates/product-brief.md` | 12 sections | 35 placeholders |
| Team | `templates/full-prd.md` | 13 sections | 50+ placeholders |

**Validation:**

```pseudocode
missing_data = []
for placeholder in required_placeholders:
  content = map_placeholder_to_answer(placeholder, session.answers)
  if is_empty(content) OR word_count(content) < 10:
    missing_data.append(placeholder)

if missing_data:
  for placeholder in missing_data:
    ask additional question to fill gap
    OR mark as "[TODO: User to complete - {description}]"
```

Proceed to Step 9.

---

### Step 9: Generate PRD

Fill template placeholders with user answers.

Add metadata header:

```markdown
<!-- Generated by planning-interview v1.0.0 -->
<!-- Mode: {session.mode} | Language: {session.language} -->
<!-- Date: {current_date} | Duration: {elapsed_time} min -->

# {project_name} - {document_type}

**Document Status:** Draft v1.0
**Last Updated:** {current_date}
**Mode:** {session.mode}
**Duration:** {elapsed_time} min
```

Store completed PRD in `prd_content` variable.

Proceed to Step 10.

---

### Step 10: Save PRD to File

**File naming convention:**

```
filename = "{mode}-{project_slug}-{YYYYMMDD}.md"

Examples:
- lean-canvas-taskflow-cli-20260215.md
- product-brief-insightboard-20260215.md
- full-prd-enterprise-sso-20260215.md
```

Ask user for save location:

```
AskUserQuestion(
  "I'll save your {document_type} to: {suggested_filename}\n\nWould you like to:\n- Use this filename\n- Specify different path\n- Preview first",
  options=["Save to {suggested_filename}", "Specify different path", "Preview first"],
  allow_freeform=false
)
```

Write file using Write() tool.

Proceed to Step 11.

---

### Step 11: Error Handling

| Error Type | Detection | Fallback Strategy |
|------------|-----------|-------------------|
| **Template missing** | File read fails | Use embedded default, warn user |
| **User abandons** | No response 5 min | Auto-save partial draft |
| **Vague answers loop** | Score <3 after 2 follow-ups | Accept answer, mark `[TODO]` |
| **Write permission denied** | Write() fails | Try ~/Desktop, ~/Downloads, or display content |
| **Invalid mode** | Unexpected value | Default to Startup mode |

**Error message template:**

```
"⚠️ {ERROR_TYPE} Error

**What happened:** {error_description}

**What I'm doing:** {fallback_action}

**What you can do:** {user_action}

Continue anyway? (yes/abort)"
```

End of algorithm.

---

## Notes

- Prioritize WHY and WHAT questions over HOW (technical is for spec-interview)
- Use completeness scoring (1-5) to drive adaptive follow-ups
- Balance completeness with time efficiency based on mode
- Validate inputs before using in template (sanitize markdown)
- Offer optional helpers but don't force them