---
name: career-compass
description: AI-powered career path analysis with 8-agent pipeline. Use when user says "analyze my career", "career path recommendation", "career compass", "transition to [role]", "career guidance", or wants personalized career roadmap.
version: 1.0.0
---

# Career Compass Skill

Comprehensive career guidance system using multi-agent analysis to generate personalized career paths and learning roadmaps.

## Trigger Phrases

**English:**
- "analyze my career"
- "career path recommendation"
- "how do I transition to [role]"
- "career compass"
- "career guidance"
- "/career-compass"

**Korean:**
- "커리어 분석해줘"
- "커리어 패스 추천"
- "[직무]로 전환하려면"

## When to Use

- Planning career transitions
- Evaluating skill gaps for target roles
- Generating personalized learning roadmaps
- Researching market trends and salary projections

## Execution Algorithm

### Step 0: Environment Setup

Check prerequisites and prepare directories.

```python
# Verify jd-analyzer data
jd_available = check_file_exists("~/.jd-analyzer/profile.yaml")

if jd_available:
    print("✓ Found jd-analyzer profile")
else:
    print("⚠️  For better results, run /jd-analyzer first")

# Create directories
create_directories([
    "~/.career-compass/roadmaps",
    "~/.career-compass/strategy"
])
```

---

### Step 1: User Interview

Collect user requirements.

```python
responses = AskUserQuestion(
    questions=[
        {
            "question": "What is your target role?",
            "header": "🎯 Target Role",
            "options": [
                {"label": "AI Engineer", "description": "..."},
                {"label": "ML Engineer", "description": "..."},
                {"label": "Other", "description": "Custom role"}
            ]
        },
        {
            "question": "Desired timeline?",
            "header": "⏱️ Timeline",
            "options": [
                {"label": "6-12 months", "description": "Fast track"},
                {"label": "12-18 months", "description": "Balanced"},
                {"label": "18-24 months", "description": "Gradual"}
            ]
        },
        {
            "question": "Weekly study time?",
            "header": "📚 Capacity",
            "options": [
                {"label": "5-10 hours", "description": "Part-time"},
                {"label": "10-20 hours", "description": "Serious"},
                {"label": "20+ hours", "description": "Full-time"}
            ]
        },
        {
            "question": "Constraints?",
            "header": "⚠️ Constraints",
            "options": [
                {"label": "Financial", "description": "Need income"},
                {"label": "Time", "description": "Family obligations"},
                {"label": "Confidence", "description": "Imposter syndrome"},
                {"label": "None", "description": "Flexible"}
            ],
            "multiSelect": true
        }
    ]
)

target_role = responses["Target Role"]
timeline = responses["Timeline"]
study_time = responses["Capacity"]
constraints = responses["Constraints"]
```

---

### Step 2: Phase 1 - Parallel Analysis

Launch 3 agents simultaneously.

```python
print("🔍 Phase 1: Analyzing your background...")

# CRITICAL: All 3 Task calls in single response for parallel execution
Task(
    subagent_type="resume-analyzer",
    model="sonnet",
    description="Analyze career background",
    prompt=f"""
    Analyze user's career from ~/.jd-analyzer/profile.yaml
    Target role: {target_role}
    Extract: timeline, skills, strengths, gaps
    Output: JSON with career_summary, skill_proficiency, gaps
    """
)

Task(
    subagent_type="jd-market-analyzer",
    model="sonnet",
    description="Analyze job market",
    prompt=f"""
    Analyze JD data from ~/.jd-analyzer/jds.json
    Target role: {target_role}
    Extract: top skills, salary, trends
    Output: JSON with top_demanded_skills, market_trends, salary_data
    """
)

Task(
    subagent_type="career-trend-researcher",
    model="opus",
    description="Research career trends",
    prompt=f"""
    Web research for {target_role} transition cases
    Find: success stories, courses, communities
    Output: JSON with success_cases, learning_resources, industry_insights
    """
)

# Wait for all to complete
```

Store: `resume_result`, `jd_market_result`, `career_trends_result`

---

### Step 3: Phase 1 Validation

Check minimum data requirements.

```python
success_count = sum([
    resume_result.status == "success",
    jd_market_result.status == "success",
    career_trends_result.status == "success"
])

if success_count < 2:
    print("❌ Insufficient data. Troubleshooting:")
    print("1. Run /jd-analyzer to create profile")
    print("2. Check internet connection")
    exit(1)

# Display Phase 1 summary
print(f"Your Profile: {resume_result.data['total_years']} years")
print(f"Market Demand: {jd_market_result.data['market_trends']['role_demand']}")
print(f"Transition Cases: {len(career_trends_result.data['success_cases'])}")
```

---

### Step 4: Phase 2 - Parallel Generation

Generate paths and analyze gaps.

```python
print("🛤️  Phase 2: Generating career paths...")

Task(
    subagent_type="skill-gap-analyzer",
    model="sonnet",
    description="Prioritize skill gaps",
    prompt=f"""
    Synthesize Phase 1 results
    Calculate ROI per skill: (demand × criticality) / difficulty
    Output: JSON with gaps_by_criticality, roi_ranked, learning_sequence
    """
)

Task(
    subagent_type="career-path-generator",
    model="opus",
    description="Generate 3-5 career paths",
    prompt=f"""
    Generate paths: Direct, Gradual, Hybrid, Bootcamp
    Each with: timeline, pros/cons, financial_impact, success_probability
    Output: JSON with paths array, recommended_path_id
    """
)

Task(
    subagent_type="salary-projector",
    model="sonnet",
    description="Calculate salary ROI",
    prompt=f"""
    Research salaries for {target_role}
    Calculate ROI per path
    Output: JSON with salary ranges, path_roi_analysis
    """
)

# Wait for completion
```

Store: `skill_gaps_result`, `paths_result`, `salary_result`

---

### Step 5: Phase 2 Validation

Validate paths generated.

```python
if len(paths_result.data['paths']) == 0:
    print("❌ No paths generated")
    exit(1)

# Display summary
print(f"Paths Generated: {len(paths_result.data['paths'])}")
for path in paths_result.data['paths']:
    print(f"  - {path['title']}: {path['duration_months']} months")
```

---

### Step 6: User Path Selection

Let user choose preferred path.

```python
path_options = [
    {
        "label": path['title'],
        "description": f"{path['duration_months']}m | {path['success_probability']}% success"
    }
    for path in paths_result.data['paths']
]

selected = AskUserQuestion(
    questions=[{
        "question": "Which career path?",
        "header": "🛤️  Select Path",
        "options": path_options
    }]
)

# Find selected path
selected_path = next(p for p in paths_result.data['paths'] if p['title'] == selected)
```

---

### Step 7: Phase 3 - Sequential Synthesis

Generate roadmap then strategy.

```python
print("📚 Phase 3: Generating your roadmap...")

# Step 7.1: Roadmap
roadmap_task = Task(
    subagent_type="roadmap-generator",
    model="sonnet",
    description="Generate learning roadmap",
    prompt=f"""
    Create month-by-month plan for: {selected_path['title']}
    Include: courses, projects, milestones
    Write to: ~/.career-compass/roadmaps/roadmap-{date}.md
    """
)

roadmap_file = roadmap_task.result.data['file_path']

# Step 7.2: Strategy (needs roadmap)
strategy_task = Task(
    subagent_type="strategy-advisor",
    model="opus",
    description="Generate strategy report",
    prompt=f"""
    Synthesize ALL results into comprehensive strategy
    Include: immediate actions, risk mitigation, networking, interview prep
    Reference roadmap: {roadmap_file}
    Write to: ~/.career-compass/strategy/strategy-{date}.md
    """
)

strategy_file = strategy_task.result.data['file_path']
```

---

### Step 8: Error Recovery

Collect and display errors.

```python
all_errors = []
for result in [resume_result, jd_market_result, ...]:
    all_errors.extend(result.errors)

if len(all_errors) > 0:
    print("⚠️  Some agents had issues:")
    for err in all_errors[:5]:
        print(f"  • {err}")
```

---

### Step 9: Display Results

Present final report.

```python
print("\n# ✅ Career Compass Complete!")
print("\n## Your Transition Plan")
print(f"**To:** {target_role}")
print(f"**Path:** {selected_path['title']}")
print(f"**Timeline:** {selected_path['duration_months']} months")

print("\n## Key Insights")
print(f"- Critical Skills: {top_3_gaps}")
print(f"- Success Probability: {selected_path['success_probability']}%")
print(f"- Salary Increase: +${salary_increase:,}")

print("\n## Generated Files")
print(f"📄 Roadmap: {roadmap_file}")
print(f"📄 Strategy: {strategy_file}")

print("\n## Next Steps")
print("1. Open roadmap and read executive summary")
print("2. Enroll in first recommended course")
print("3. Set up development environment")
print("4. Join recommended communities")
```

---

### Step 10: Session Summary (Optional)

Offer to save summary.

```python
save = AskUserQuestion(
    questions=[{
        "question": "Save session summary?",
        "options": [
            {"label": "Yes", "description": "Save to ~/.career-compass/sessions/"},
            {"label": "No", "description": "Keep just roadmap + strategy"}
        ]
    }]
)

if save == "Yes":
    write_file(f"~/.career-compass/sessions/session-{date}.md", summary)
```

---

## Model Selection

| Agent | Model | Reasoning |
|-------|-------|-----------|
| resume-analyzer | sonnet | Deep analysis, pattern recognition |
| jd-market-analyzer | sonnet | Complex data synthesis |
| career-trend-researcher | **opus** | Creative research, strategic thinking |
| skill-gap-analyzer | sonnet | Analytical prioritization |
| career-path-generator | **opus** | Creative path design (CRITICAL) |
| salary-projector | sonnet | Financial calculations |
| roadmap-generator | sonnet | Structured planning |
| strategy-advisor | **opus** | Strategic synthesis (CRITICAL) |

**Cost:** 5 Sonnet + 3 Opus per run (~$1.50)

**Performance:** 5-7 minutes total

---

## Error Handling

| Step | Error | Solution |
|------|-------|----------|
| 1 | No interview response | Exit gracefully |
| 2 | All Phase 1 fails | Display diagnostics, exit |
| 3 | No skills found | Request manual input |
| 4 | All Phase 2 fails | Use generic paths |
| 5 | No paths generated | Cannot proceed, exit |
| 6 | No selection | Ask to retry or exit |
| 7 | File write fails | Return inline, log error |
| 8 | Multiple failures | Warn about reduced accuracy |

---

## Quick Reference

**Usage:**
```
/career-compass
```

**Duration:** 5-7 minutes

**Output:**
- Roadmap: ~/.career-compass/roadmaps/
- Strategy: ~/.career-compass/strategy/

**Prerequisites:** 
- jd-analyzer (recommended)
- Internet connection (for web research)
