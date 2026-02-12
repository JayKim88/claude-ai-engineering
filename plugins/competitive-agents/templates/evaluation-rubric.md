# Evaluation Rubric (100 Points)

## Scoring Criteria

| # | Criterion | Weight | Description |
|---|-----------|--------|-------------|
| 1 | **Convention Compliance** | 15 | Correct plugin.json format, YAML frontmatter in agents, SKILL.md structure, directory naming conventions |
| 2 | **Functional Completeness** | 20 | All required files present, installable via `npm run link`, trigger phrases defined, would run end-to-end |
| 3 | **SKILL.md Quality** | 20 | Execution algorithm clarity, correct Task() call syntax, proper parallel vs sequential specification, well-crafted prompts |
| 4 | **Error Handling** | 10 | Failure modes identified, fallbacks provided, handles missing dependencies, bad input, partial failures |
| 5 | **Documentation Quality** | 10 | README clarity, installation instructions, trigger phrases, usage examples |
| 6 | **Agent Design** | 10 | Clear non-overlapping responsibilities, justified model selection, specified output formats (if multi-agent) |
| 7 | **User Experience** | 10 | Intuitive usage, well-designed AskUserQuestion interactions, useful output format |
| 8 | **Maintainability** | 5 | Easy to modify, understandable architecture, clear code organization |

## Scoring Scale

- **9-10**: Exceptional. Matches or exceeds best existing plugins in the repository.
- **7-8**: Good. Solid implementation with minor gaps.
- **5-6**: Adequate. Works but has notable issues.
- **3-4**: Below standard. Multiple significant problems.
- **1-2**: Fundamentally flawed. Would not work as-is.

## Cross-Reviewer Output Format

```markdown
## Critique Summary
[2-3 sentence overall assessment]

## Scores (1-10)
| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Convention Compliance | X | ... |
| Functional Completeness | X | ... |
| SKILL.md Quality | X | ... |
| Error Handling | X | ... |
| Documentation Quality | X | ... |
| Agent Design | X | ... |
| User Experience | X | ... |
| Maintainability | X | ... |
| **Weighted Total** | **X/100** | |

## Specific Issues
### Critical (Must Fix)
1. [file] - [issue] - [suggested fix]

### Important (Should Fix)
1. [file] - [issue] - [suggested fix]

### Minor (Consider)
1. [observation] - [suggestion]

## Strengths to Preserve
1. [what works well and why]

## Missing Elements
1. [what was expected but absent]
```

## Judge Report Format

```markdown
# Competitive Agents - Judge Report

> **Mission**: {mission}
> **Date**: {date}
> **Rounds**: {N}

## Score Comparison

| Criterion (Weight) | Alpha | Beta | Notes |
|---------------------|-------|------|-------|
| Convention Compliance (15) | X/10 | Y/10 | ... |
| Functional Completeness (20) | X/10 | Y/10 | ... |
| SKILL.md Quality (20) | X/10 | Y/10 | ... |
| Error Handling (10) | X/10 | Y/10 | ... |
| Documentation (10) | X/10 | Y/10 | ... |
| Agent Design (10) | X/10 | Y/10 | ... |
| User Experience (10) | X/10 | Y/10 | ... |
| Maintainability (5) | X/10 | Y/10 | ... |
| **Weighted Total** | **A/100** | **B/100** | |

## Winner: Agent {Alpha|Beta}

### Key Differentiators
1. [What made the winner better]
2. [Where the winner excelled]

### Agent Alpha Analysis
**Strengths**: ...
**Weaknesses**: ...

### Agent Beta Analysis
**Strengths**: ...
**Weaknesses**: ...

## Fusion Guidance
- **From Alpha**: [elements worth taking]
- **From Beta**: [elements worth taking]
- **Conflicts to resolve**: [structural differences]
```
