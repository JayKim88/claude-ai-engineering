# Plugin Conventions Reference

This document defines the conventions that generated plugins MUST follow. Both generator agents and the cross-reviewer reference this document.

## Required Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED
├── skills/
│   └── plugin-name/
│       └── SKILL.md         # REQUIRED
└── README.md                # REQUIRED
```

## Optional Components

```
plugin-name/
├── agents/                  # If multi-agent
│   └── agent-name.md
├── commands/
│   └── command-name/
│       └── command-name.md
├── templates/
│   └── output-template.md
├── config/                  # Python scripts, data files
├── CLAUDE.md                # Developer guide
└── docs/
```

## plugin.json Format

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": {
    "name": "Jay Kim",
    "url": "https://github.com/JayKim88"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

## SKILL.md Format

```yaml
---
name: skill-name
description: Trigger phrases and when to use. Use when user says "phrase1", "phrase2", ...
version: 1.0.0
---
```

Body contains:
1. `## Trigger Phrases` - English and Korean
2. `## When to Use` - Scenarios
3. `## Execution Algorithm` - Numbered steps with pseudocode
4. `## Error Handling` - Table of scenario/response
5. `## Quick Reference` - Usage summary

### Step Format

```markdown
### Step N: Action Name

Description of what this step does.

```python
ToolName(
    param="value",
    ...
)
```
```

### Task() Call for Multi-Agent

```python
Task(
    subagent_type="agent-name",
    model="sonnet",
    description="Short description",
    prompt="Detailed instructions..."
)
```

**Critical**: For parallel execution, ALL Task calls must be in a single response block.

## Agent .md Format

```yaml
---
name: agent-name
description: What this agent does
tools: ["Read", "Glob", "Grep"]
model: sonnet
color: blue
---
```

Body contains:
1. `## Responsibilities` - What it analyzes/does
2. `## Analysis Strategy` or `## Execution Strategy` - How it works
3. `## Output Format` - Expected result structure

## Command .md Format

```yaml
---
description: What the command does
allowed-tools: Read, Write, Bash, WebFetch, AskUserQuestion
---
```

## Model Selection Guide

| Use Case | Model | Reason |
|----------|-------|--------|
| Deep analysis, generation | sonnet | Balance of quality and speed |
| Fast synthesis, simple tasks | haiku | Speed and cost efficiency |
| Critical evaluation, judgment | opus | Highest quality reasoning |

## Naming Conventions

- Plugin name: lowercase, hyphens (e.g., `my-plugin`)
- Agent files: lowercase, hyphens (e.g., `data-analyzer.md`)
- Skill directory: matches plugin name
- Command directory: short verb (e.g., `analyze`, `compete`)
