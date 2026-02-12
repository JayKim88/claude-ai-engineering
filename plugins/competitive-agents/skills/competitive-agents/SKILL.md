---
name: competitive-agents
description: Orchestrate competing agents to generate higher-quality plugin implementations. Use when user says "compete", "competitive agents", "dual generate", "에이전트 경쟁", "플러그인 배틀", or wants two agents to compete on a generation task.
version: 1.0.0
---

# Competitive Agents Skill

Two agents with different philosophies generate competing implementations, cross-review each other, improve, and a judge picks the winner. The user chooses the final result.

## Trigger Phrases

**English:**
- "compete"
- "competitive agents"
- "dual generate"
- "plugin battle"
- "/compete"

**Korean:**
- "에이전트 경쟁"
- "플러그인 배틀"
- "경쟁 생성"

## When to Use

- Generating a new Claude Code plugin from scratch
- When quality matters more than speed
- When exploring different architectural approaches

## Execution Algorithm

### Step 1: Parse Mission Input

Determine what the user wants to build:

```python
AskUserQuestion(
    questions=[
        {
            "question": "What plugin do you want to build? Describe its purpose and key features.",
            "header": "Mission",
            "options": [
                {"label": "Describe now", "description": "I'll describe the plugin I want to build"},
                {"label": "Use a spec file", "description": "I have a spec document to reference"},
                {"label": "Improve existing", "description": "Generate a better version of an existing plugin"}
            ],
            "multiSelect": false
        }
    ]
)
```

**If "Describe now"**: Collect the user's text description as the mission.

**If "Use a spec file"**: Ask for path, then read the spec file.

**If "Improve existing"**: Ask for plugin name, read its current files as the mission context.

Then confirm round count:

```python
AskUserQuestion(
    questions=[
        {
            "question": "How many improvement rounds?",
            "header": "Rounds",
            "options": [
                {"label": "1 round (Recommended)", "description": "Cross-review + improve once (~3-5 min)"},
                {"label": "2 rounds", "description": "Two cycles of cross-review + improve (~5-8 min)"}
            ],
            "multiSelect": false
        }
    ]
)
```

### Step 2: Build Shared Context

Read existing plugin patterns to provide as reference:

```python
# Read 2 reference plugins for convention examples
Read("plugins/project-insight/.claude-plugin/plugin.json")
Read("plugins/project-insight/skills/project-insight/SKILL.md")
Read("plugins/competitive-agents/templates/plugin-conventions.md")
Read("plugins/competitive-agents/templates/evaluation-rubric.md")
```

Construct `shared_context`:
- `mission`: User's description or spec content
- `reference_patterns`: Key excerpts from reference plugins
- `conventions`: From `templates/plugin-conventions.md`
- `max_rounds`: 1 or 2
- `mission_slug`: lowercase, hyphened, max 40 chars from mission keywords

Create output directory:

```bash
mkdir -p tempo/competitive-agents/{mission_slug}/agent-a
mkdir -p tempo/competitive-agents/{mission_slug}/agent-b
```

Save mission:

```python
Write("tempo/competitive-agents/{mission_slug}/mission.md", mission_text)
```

### Step 3: Phase 1 - Parallel Generation

Launch both generators in a **single response block** for parallel execution:

```python
# PARALLEL: Both agents run simultaneously
Task(
    subagent_type="generator-alpha",
    model="sonnet",
    description="Generate plugin (Pragmatist)",
    prompt="""
    You are Agent Alpha, the Pragmatist.

    ## Mission
    {mission}

    ## Your Philosophy
    - SIMPLICITY over completeness
    - Minimum viable file count (3-5 files)
    - Single-skill design preferred, multi-agent only if clearly necessary
    - SKILL.md with 3-5 concise steps
    - Handle top 3 most likely errors only
    - Use haiku model where possible for cost efficiency
    - README under 100 lines, no CLAUDE.md unless essential
    - Prefer sensible defaults over asking user questions

    ## Plugin Conventions (MUST follow)
    {conventions from plugin-conventions.md}

    ## Reference Patterns
    {reference plugin excerpts}

    ## Output Format
    For each file, output exactly:
    === FILE: relative/path/to/file.ext ===
    [complete file contents]
    === END FILE ===

    Generate a COMPLETE, FUNCTIONAL plugin. Every file must be production-ready.
    """
)

Task(
    subagent_type="generator-beta",
    model="sonnet",
    description="Generate plugin (Architect)",
    prompt="""
    You are Agent Beta, the Architect.

    ## Mission
    {mission}

    ## Your Philosophy
    - COMPLETENESS over minimalism
    - Rich structure: plugin.json, SKILL.md, README.md, CLAUDE.md, agents/, commands/, config
    - Multi-agent design when it adds value, with explicit parallel/sequential phases
    - SKILL.md with 7-10 detailed steps, branching logic, comprehensive pseudocode
    - Exhaustive error handling table for every step
    - Use sonnet model for quality-critical agents
    - Detailed README with architecture diagram, examples, troubleshooting
    - Full CLAUDE.md developer guide
    - Config file with all tunable parameters and comments

    ## Plugin Conventions (MUST follow)
    {conventions from plugin-conventions.md}

    ## Reference Patterns
    {reference plugin excerpts}

    ## Output Format
    For each file, output exactly:
    === FILE: relative/path/to/file.ext ===
    [complete file contents]
    === END FILE ===

    Generate a COMPLETE, FUNCTIONAL plugin. Every file must be production-ready.
    """
)
```

**Wait for both agents to complete.**

### Step 4: Save v1 Outputs

Parse each agent's output by extracting `=== FILE: ... ===` blocks.

Write files to:
- `tempo/competitive-agents/{mission_slug}/agent-a/v1/` (all of Alpha's files)
- `tempo/competitive-agents/{mission_slug}/agent-b/v1/` (all of Beta's files)

Display summary to user:

```
Agent Alpha (Pragmatist): Generated {N} files
Agent Beta (Architect): Generated {M} files
```

### Step 5: Phase 2 - Parallel Cross-Review (Round 1)

Launch two cross-review tasks in a **single response block**:

```python
# PARALLEL: Both reviews run simultaneously
Task(
    subagent_type="cross-reviewer",
    model="sonnet",
    description="Review Alpha's work",
    prompt="""
    Review Agent Alpha's (Pragmatist) plugin implementation.

    ## Evaluation Rubric
    {evaluation-rubric.md contents}

    ## Original Mission
    {mission}

    ## Plugin Convention Reference
    {plugin-conventions.md contents}

    ## Agent Alpha's Implementation
    {all files from agent-a/v1/, each prefixed with file path}

    Produce a structured critique following the Cross-Reviewer Output Format in the rubric.
    Be specific with file references. Score each criterion 1-10.
    """
)

Task(
    subagent_type="cross-reviewer",
    model="sonnet",
    description="Review Beta's work",
    prompt="""
    Review Agent Beta's (Architect) plugin implementation.

    ## Evaluation Rubric
    {evaluation-rubric.md contents}

    ## Original Mission
    {mission}

    ## Plugin Convention Reference
    {plugin-conventions.md contents}

    ## Agent Beta's Implementation
    {all files from agent-b/v1/, each prefixed with file path}

    Produce a structured critique following the Cross-Reviewer Output Format in the rubric.
    Be specific with file references. Score each criterion 1-10.
    """
)
```

**Wait for both reviews to complete.**

Save critiques:
- `tempo/competitive-agents/{mission_slug}/agent-a/v1-critique.md`
- `tempo/competitive-agents/{mission_slug}/agent-b/v1-critique.md`

### Step 6: Display Review Summary + User Confirmation

Show condensed summary:

```
=== Cross-Review Round 1 ===

Agent Alpha (Pragmatist):
  Score: X/100 | Critical issues: N | Top strength: ... | Top weakness: ...

Agent Beta (Architect):
  Score: Y/100 | Critical issues: M | Top strength: ... | Top weakness: ...
```

```python
AskUserQuestion(
    questions=[
        {
            "question": "Proceed with improvement round?",
            "header": "Continue",
            "options": [
                {"label": "Yes, improve both (Recommended)", "description": "Apply critiques and generate v2"},
                {"label": "Skip to Judge", "description": "Go straight to final evaluation with v1"},
                {"label": "Stop here", "description": "Save current outputs and stop"}
            ],
            "multiSelect": false
        }
    ]
)
```

**If "Stop here"**: Display file paths and end.

**If "Skip to Judge"**: Go to Step 9.

### Step 7: Phase 3 - Parallel Improvement (Round 1)

```python
# PARALLEL: Both improvements run simultaneously
Task(
    subagent_type="improver",
    model="sonnet",
    description="Improve Alpha's plugin",
    prompt="""
    Improve Agent Alpha's (Pragmatist) plugin implementation based on critique.

    ## Original Implementation
    {all files from agent-a/v1/}

    ## Critique Received
    {v1-critique.md for Alpha}

    ## Rules
    1. Address ALL Critical issues
    2. Address MOST Important issues
    3. Selectively address Minor issues
    4. DO NOT change the fundamental Pragmatist philosophy
    5. Preserve all identified strengths

    ## Output Format
    First output a CHANGELOG:
    === CHANGELOG ===
    - [Fixed/Added/Changed]: [description] (addresses: [Critical/Important/Minor] #N)
    - [Skipped]: [description] (reason: [why])
    === END CHANGELOG ===

    Then output all files (complete contents, not diffs):
    === FILE: relative/path/to/file.ext ===
    [complete file contents]
    === END FILE ===
    """
)

Task(
    subagent_type="improver",
    model="sonnet",
    description="Improve Beta's plugin",
    prompt="""
    Improve Agent Beta's (Architect) plugin implementation based on critique.

    ## Original Implementation
    {all files from agent-b/v1/}

    ## Critique Received
    {v1-critique.md for Beta}

    ## Rules
    1. Address ALL Critical issues
    2. Address MOST Important issues
    3. Selectively address Minor issues
    4. DO NOT change the fundamental Architect philosophy
    5. Preserve all identified strengths

    ## Output Format
    First output a CHANGELOG:
    === CHANGELOG ===
    - [Fixed/Added/Changed]: [description] (addresses: [Critical/Important/Minor] #N)
    - [Skipped]: [description] (reason: [why])
    === END CHANGELOG ===

    Then output all files (complete contents, not diffs):
    === FILE: relative/path/to/file.ext ===
    [complete file contents]
    === END FILE ===
    """
)
```

**Wait for both. Save to agent-a/v2/ and agent-b/v2/.**

Save changelogs:
- `tempo/competitive-agents/{mission_slug}/agent-a/v2-changelog.md`
- `tempo/competitive-agents/{mission_slug}/agent-b/v2-changelog.md`

### Step 8: Optional Round 2

If `max_rounds == 2`, repeat Steps 5-7 with v2 as input, producing v3.

The cross-reviewer prompt in Round 2 additionally includes:
- The previous critique (v1-critique.md)
- The changelog (v2-changelog.md)
- Instruction: "Verify whether v1 issues were actually fixed. Check for regressions."

After Round 2, proceed to Step 9.

### Step 9: Phase 4 - Judge Evaluation

```python
# SEQUENTIAL: Judge needs both final versions
Task(
    subagent_type="judge",
    model="opus",
    description="Judge final implementations",
    prompt="""
    You are the impartial Judge. Evaluate two competing plugin implementations.

    ## Original Mission
    {mission}

    ## Evaluation Rubric
    {evaluation-rubric.md contents}

    ## Agent Alpha's Final Implementation (Pragmatist)
    {all files from agent-a/v{final}/}

    ## Agent Beta's Final Implementation (Architect)
    {all files from agent-b/v{final}/}

    ## Tasks
    1. Score each implementation on every rubric criterion (1-10)
    2. Calculate weighted totals (see rubric for weights)
    3. Declare the winner with margin
    4. Provide specific reasoning for each score
    5. Identify best elements from each for potential fusion
    6. Output the full Judge Report (see rubric for format)
    """
)
```

Save: `tempo/competitive-agents/{mission_slug}/judge-report.md`

### Step 10: Present Results + User Decision

Display the Judge's verdict (scores table, winner, key differentiators).

```python
AskUserQuestion(
    questions=[
        {
            "question": "What would you like to do with the results?",
            "header": "Decision",
            "options": [
                {"label": "Use winner ({winner_name} {winner_score}/100)", "description": "Deploy the winning agent's version"},
                {"label": "Fuse A + B", "description": "Merge best elements of both (~2 min extra)"},
                {"label": "Keep both", "description": "Save both versions for manual review"}
            ],
            "multiSelect": false
        }
    ]
)
```

### Step 11: Execute Decision

**If "Use winner"**:
Copy the winning agent's final version to `tempo/competitive-agents/{mission_slug}/final/`.

**If "Fuse A + B"**:

```python
Task(
    subagent_type="fuser",
    model="sonnet",
    description="Fuse best of both",
    prompt="""
    Merge the best elements of two competing plugin implementations.

    ## Judge's Analysis
    {judge-report.md}

    ## Agent Alpha's Final Version
    {all files from agent-a/v{final}/}

    ## Agent Beta's Final Version
    {all files from agent-b/v{final}/}

    ## Rules
    1. Take higher-scoring elements from each agent per criterion
    2. Resolve structural conflicts coherently (pick one approach, don't mix)
    3. Maintain internal consistency across all files
    4. For each file, note which agent's version you primarily drew from

    ## Output Format
    === FILE: relative/path/to/file.ext === (from: Alpha|Beta|Merged)
    [complete file contents]
    === END FILE ===
    """
)
```

Save fused output to `tempo/competitive-agents/{mission_slug}/fused/` and copy to `final/`.

**If "Keep both"**: Both versions already saved. Skip to Step 12.

### Step 12: Completion Summary

```
Competitive generation complete!

Output: tempo/competitive-agents/{mission_slug}/final/
Judge Report: tempo/competitive-agents/{mission_slug}/judge-report.md

Generated plugin: {plugin_name}
Files: {N} files
Trigger phrases: {list}

Next steps:
1. Review generated files
2. Copy to plugins/ if satisfied
3. Run `npm run link` to install
4. Test with trigger phrases
```

## Error Handling

| Scenario | Response |
|----------|----------|
| Mission too vague (< 20 chars) | Ask user for more detail |
| Spec file not found | Inform user, ask for corrected path |
| Agent generation fails/timeout | Retry once. If still fails, proceed with single agent, skip competition |
| Output not parseable (no === FILE === blocks) | Retry agent with stricter format instructions |
| Directory creation fails | Check permissions, suggest alternative path |
| Cross-reviewer gives all 10/10 | Re-invoke with: "You MUST identify at least 3 areas for improvement" |
| Judge scores within 2 points | Report as "Too close to call", recommend fusion |
| User aborts mid-pipeline | Save all completed work, display paths |

## Quick Reference

**Usage:**
```
"compete"
"competitive agents"
"/compete"
"에이전트 경쟁"
```

**Expected Duration:**
- 1 round: ~3-5 minutes
- 2 rounds: ~5-8 minutes
- 2 rounds + fuse: ~7-10 minutes

**Output:**
```
tempo/competitive-agents/{mission-slug}/
├── agent-a/v1/, v2/ (v3/ if 2 rounds)
├── agent-b/v1/, v2/ (v3/ if 2 rounds)
├── judge-report.md
└── final/
```
