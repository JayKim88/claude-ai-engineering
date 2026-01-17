---
description: Comprehensive project analysis with multi-agent insights
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
---

# /insight Command

Analyze project quality, structure, and documentation using a multi-agent pipeline.

## Quick Start

```
/insight                    # Analyze current directory
/insight --path src/        # Analyze specific directory
/insight --quick            # Skip documentation analysis (faster)
```

## What It Does

Spawns 4 specialized agents in a 2-phase pipeline:

### Phase 1: Parallel Analysis (3 agents)
1. **Tech Stack Analyzer** - Dependencies, frameworks, tools
2. **Structure Analyzer** - Organization, patterns, metrics
3. **README Analyzer** - Documentation quality, completeness

### Phase 2: Synthesis (1 agent)
4. **Insight Synthesizer** - Consolidate, prioritize, recommend

## Execution Flow

```
/insight
   ↓
┌──────────────────────────────────┐
│  project-insight skill           │
│  (Orchestrator)                  │
└────────┬─────────────────────────┘
         │
         ├─ Phase 1 (Parallel) ──────────────┐
         │                                    │
    ┌────▼─────┐  ┌────────────┐  ┌─────────▼──┐
    │ Tech     │  │ Structure  │  │ README     │
    │ Stack    │  │ Analyzer   │  │ Analyzer   │
    └────┬─────┘  └─────┬──────┘  └─────┬──────┘
         │              │               │
         └──────────────┴───────────────┘
                        │
         ├─ Phase 2 (Sequential) ────────┐
         │                                │
    ┌────▼───────────────┐                │
    │ Insight            │                │
    │ Synthesizer        │                │
    └────┬───────────────┘                │
         │                                │
         ▼                                │
    Final Report                          │
```

## Output

Consolidated report with:
- **Executive Summary** - 2-3 sentence overview
- **Project Profile** - Type, language, framework, maturity
- **Key Findings** - Strengths and improvements
- **Prioritized Recommendations**:
  - Critical (do now)
  - Important (this week)
  - Beneficial (nice to have)
- **Quick Wins** - Tasks under 1 hour
- **Health Score** - Overall rating out of 10

## Options

- `--path <dir>` - Target directory (default: current)
- `--quick` - Skip documentation analysis (2 agents instead of 3)
- `--verbose` - Include detailed agent outputs
- `--export <file>` - Save report to file (future)

## Examples

### Basic Analysis
```
User: /insight
→ Analyzes current directory
→ Returns comprehensive report in ~1-2 minutes
```

### Specific Directory
```
User: /insight --path packages/core
→ Analyzes only packages/core subdirectory
```

### Quick Analysis
```
User: /insight --quick
→ Skips README analysis
→ Faster execution (~30-45 seconds)
```

## When to Use

- **Onboarding** - Understand new codebase quickly
- **Health Check** - Quarterly project assessment
- **Pre-Refactor** - Identify improvement areas
- **Documentation Sprint** - Find doc gaps
- **Tech Debt Planning** - Prioritize improvements

## Follow-up Actions

After receiving the report, you can:

1. **Deep Dive**
   - "Explain the structure analysis in detail"
   - "Show me examples of the tech debt"

2. **Create Tasks**
   - "Create GitHub issues for critical items"
   - "Generate a TODO list from quick wins"

3. **Document Insights**
   - "Save this analysis to learning notes" (uses learning-summary)
   - "Add to project documentation"

4. **Compare**
   - "Compare with best practices for [framework]"
   - "How does this compare to similar projects?"

## Implementation Details

This command invokes the `project-insight` skill, which orchestrates:
- **3 analysis agents** (parallel execution)
- **1 synthesizer agent** (sequential after analysis)

See `skills/project-insight/SKILL.md` for detailed execution algorithm.

## Performance

- **Phase 1**: 30-60 seconds (parallel)
- **Phase 2**: 10-20 seconds (synthesis)
- **Total**: ~1-2 minutes for typical project

Larger projects (10k+ files) may take longer. Use `--path` to limit scope.

## Tips

- Run from **project root** for best results
- Ensure README.md exists for documentation analysis
- Works best with modern project structures
- Supports: Node.js, Python, Rust, Go, Java, Ruby

## Related Commands

- `/wrap` - Session wrap-up with insights
- (future) `/review` - Deep code review
- (future) `/refactor` - Refactoring suggestions
