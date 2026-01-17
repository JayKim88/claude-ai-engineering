---
name: project-insight
description: Comprehensive project analysis using multi-agent pipeline. Use when user says "analyze project", "project insight", "evaluate codebase", or wants to understand project quality.
version: 1.0.0
---

# Project Insight Skill

Rapid project analysis and improvement recommendations using multi-agent analysis.

## Trigger Phrases

- "analyze this project"
- "project insight"
- "evaluate the codebase"
- "what can we improve?"
- "project health check"
- "give me insights on this project"

## When to Use

- First time exploring a codebase
- Before making architectural decisions
- Onboarding new team members
- Quarterly project health checks
- Before refactoring initiatives

## Execution Algorithm

### Step 1: Confirm Target

Ask user to confirm the project directory if not obvious:

```python
AskUserQuestion(
    questions=[{
        "question": "Which directory should I analyze?",
        "header": "Target",
        "options": [
            {
                "label": "Current directory",
                "description": "Analyze the current working directory"
            },
            {
                "label": "Specify path",
                "description": "Provide a specific directory path"
            }
        ],
        "multiSelect": false
    }]
)
```

If "Specify path" selected, ask for the path.

### Step 2: Phase 1 - Parallel Analysis

Execute three independent analysis agents simultaneously:

```python
# Spawn 3 agents in parallel (single response with 3 Task calls)
Task(
    subagent_type="tech-stack-analyzer",
    model="sonnet",
    description="Analyze tech stack",
    prompt="""
    Analyze the technology stack of the project in: {project_dir}

    Tasks:
    1. Identify programming languages and versions
    2. List frameworks and libraries
    3. Find build tools and package managers
    4. Note development dependencies
    5. Flag outdated or deprecated dependencies

    Focus on PRIMARY technologies, not every dependency.
    Provide specific file:line references for findings.
    """
)

Task(
    subagent_type="structure-analyzer",
    model="sonnet",
    description="Analyze project structure",
    prompt="""
    Analyze the project structure and organization in: {project_dir}

    Tasks:
    1. Identify directory organization pattern
    2. Evaluate naming consistency
    3. Measure nesting depth and complexity
    4. Assess separation of concerns
    5. Find structural issues

    Use bash commands to gather metrics.
    Provide specific directory paths for issues.
    """
)

Task(
    subagent_type="readme-analyzer",
    model="sonnet",
    description="Analyze documentation",
    prompt="""
    Analyze documentation quality in: {project_dir}

    Tasks:
    1. Read README.md and evaluate completeness
    2. Check for essential sections
    3. Identify missing documentation
    4. Assess code example quality
    5. Suggest improvements

    Look for README.md, CONTRIBUTING.md, LICENSE, CHANGELOG.md.
    Rate quality on a scale of 1-10.
    """
)
```

**Wait for all three agents to complete.**

### Step 3: Phase 2 - Synthesis

After Phase 1 completes, synthesize findings:

```python
Task(
    subagent_type="insight-synthesizer",
    model="haiku",
    description="Synthesize insights",
    prompt="""
    You are receiving analysis results from three specialized agents.

    # Tech Stack Analysis
    {tech-stack-analyzer results}

    # Structure Analysis
    {structure-analyzer results}

    # Documentation Analysis
    {readme-analyzer results}

    ---

    Tasks:
    1. Remove duplicate or overlapping insights
    2. Prioritize findings (Critical/Important/Beneficial)
    3. Identify quick wins (< 1 hour tasks)
    4. Detect cross-cutting patterns
    5. Create actionable recommendations

    Output a consolidated Project Insight Report.
    Include:
    - Executive summary
    - Strengths and improvements
    - Prioritized action items
    - Quick wins checklist
    - Overall health score
    """
)
```

### Step 4: Present Results

Display the final consolidated report to the user.

Ask if they want to:
1. Deep dive into specific findings
2. Generate improvement tasks
3. Create GitHub issues for action items
4. Document insights using `/learning-summary`

## Model Selection Rationale

| Agent | Model | Reasoning |
|-------|-------|-----------|
| tech-stack-analyzer | sonnet | Deep analysis of dependencies and compatibility |
| structure-analyzer | sonnet | Complex pattern recognition and metrics |
| readme-analyzer | sonnet | Content quality assessment requires nuance |
| insight-synthesizer | haiku | Fast synthesis, validation is straightforward |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No package.json found | Not a Node.js project | Expand language detection logic |
| Permission denied | Restricted directory | Ask user to change directory or permissions |
| Phase 1 agent timeout | Large codebase | Add --max-depth flag to limit scope |
| Empty analysis | No files found | Verify correct directory |

## Quick Reference

**Usage:**
```
"analyze this project"
/insight
```

**Expected Duration:**
- Phase 1 (parallel): ~30-60 seconds
- Phase 2 (synthesis): ~10-20 seconds
- Total: ~1-2 minutes

**Output:**
Consolidated report with:
- Health score (X/10)
- Critical/Important/Beneficial items
- Quick wins checklist
- Actionable next steps

## Related Skills

- `learning-summary`: Document insights from analysis
- `session-wrap`: Wrap up analysis session
- Code review workflows (future)

## Future Enhancements

- [ ] Add test coverage analysis agent
- [ ] Security vulnerability scanning
- [ ] Performance metrics analysis
- [ ] Comparison with similar projects
- [ ] Export to JSON/Markdown file
- [ ] GitHub integration for issue creation
