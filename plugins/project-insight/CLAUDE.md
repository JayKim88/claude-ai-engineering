# Project Insight Plugin - Development Guide

Development and maintenance guide for the project-insight multi-agent analysis plugin.

## Directory Structure

```
project-insight/
├── .claude-plugin/
│   └── plugin.json                 # Plugin metadata and version
├── agents/
│   ├── tech-stack-analyzer.md      # Technology detection agent
│   ├── structure-analyzer.md       # Architecture analysis agent
│   ├── readme-analyzer.md          # Documentation assessment agent
│   └── insight-synthesizer.md      # Consolidation and prioritization agent
├── skills/
│   └── project-insight/
│       └── SKILL.md                # Skill definition with multi-agent orchestration
├── commands/
│   └── insight/
│       └── insight.md              # /insight command definition
├── README.md                       # User-facing documentation
└── CLAUDE.md                       # Development guide (you are here)
```

## Multi-Agent Architecture

### 2-Phase Pipeline Pattern

This plugin uses the **2-Phase Pipeline** pattern from session-wrap:

```
Phase 1: Parallel Analysis (Generate)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Tech Stack   │  │ Structure    │  │ README       │
│ Analyzer     │  │ Analyzer     │  │ Analyzer     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └──────────────────┼──────────────────┘
                          ▼
Phase 2: Sequential Synthesis (Validate & Consolidate)
                  ┌──────────────┐
                  │ Insight      │
                  │ Synthesizer  │
                  └──────────────┘
```

**Why this pattern?**
- Phase 1 agents are independent → can run in parallel (faster)
- Phase 2 needs all Phase 1 outputs → must run sequentially
- Clear separation: Generate insights → Validate and prioritize

### Agent Definitions

Each agent is a markdown file with frontmatter:

```yaml
---
name: agent-name
description: What this agent does
tools: ["Read", "Glob", "Grep", "Bash"]
model: sonnet | haiku | opus
color: blue | green | purple | yellow
---

# Agent Name

## Responsibilities
...

## Analysis Strategy
...

## Output Format
...
```

**Key fields:**
- **name**: Must match filename (without .md)
- **tools**: Array of allowed Claude Code tools
- **model**: Computational power needed (sonnet for analysis, haiku for synthesis)
- **color**: UI indicator (cosmetic)

## Agent Responsibilities

### 1. tech-stack-analyzer.md

**Purpose:** Identify all technologies used in the project

**Tools:**
- `Read` - Read package.json, requirements.txt, etc.
- `Glob` - Find config files (tsconfig.json, .eslintrc, etc.)
- `Grep` - Search for import statements

**Model:** sonnet (requires deep analysis)

**Key tasks:**
1. Detect languages (file extensions, config files)
2. Identify frameworks (package.json dependencies)
3. Find build tools (scripts in package.json)
4. Check for deprecated packages (outdated versions)

**Output format:**
- Technology list with versions
- Notable dependencies with explanations
- Deprecated/outdated warnings

### 2. structure-analyzer.md

**Purpose:** Evaluate project organization and architecture

**Tools:**
- `Bash` - Run find/tree commands for metrics
- `Glob` - List directories
- `Grep` - Find patterns
- `Read` - Sample key files

**Model:** sonnet (pattern recognition)

**Key tasks:**
1. Identify organization pattern (MVC, Clean Architecture, Feature-based)
2. Calculate metrics (nesting depth, file counts)
3. Check naming consistency
4. Assess separation of concerns

**Output format:**
- Organization pattern identified
- Metrics (depth, file distribution)
- Strengths and improvement opportunities
- Specific file:line references for issues

### 3. readme-analyzer.md

**Purpose:** Assess documentation quality

**Tools:**
- `Read` - Read README.md, CONTRIBUTING.md, etc.
- `Glob` - Find documentation files
- `Grep` - Search for specific sections

**Model:** sonnet (content quality assessment)

**Key tasks:**
1. Check for essential sections (installation, usage, license)
2. Evaluate code example quality
3. Identify missing documentation
4. Rate overall quality (1-10)

**Output format:**
- Quality score
- Existing sections with ratings
- Missing sections with importance
- Quick win suggestions

### 4. insight-synthesizer.md

**Purpose:** Consolidate findings and create actionable recommendations

**Tools:**
- `Read` (receives Phase 1 outputs)

**Model:** haiku (fast synthesis, straightforward logic)

**Key tasks:**
1. Remove duplicate findings across agents
2. Prioritize (Critical/Important/Beneficial)
3. Identify quick wins (< 1 hour)
4. Detect cross-cutting patterns
5. Generate overall health score

**Output format:**
- Executive summary
- Prioritized recommendations
- Quick wins checklist
- Health score (X/10)

## Skill Orchestration

### SKILL.md Structure

```markdown
---
name: project-insight
description: Trigger phrases...
version: 1.0.0
---

# Project Insight Skill

## Execution Algorithm

### Step 1: Confirm Target
[Ask user which directory to analyze]

### Step 2: Phase 1 - Parallel Analysis
```python
Task(subagent_type="tech-stack-analyzer", ...)
Task(subagent_type="structure-analyzer", ...)
Task(subagent_type="readme-analyzer", ...)
```

### Step 3: Phase 2 - Synthesis
```python
Task(
    subagent_type="insight-synthesizer",
    prompt="""
    [Phase 1 results]
    Consolidate and prioritize...
    """
)
```

### Step 4: Present Results
[Display report to user]
```

**Critical:** Phase 1 tasks must be in a single response block for parallel execution.

## Development Workflow

### Local Development Setup

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link

# Verify symlinks
ls -l ~/.claude/agents/tech-stack-analyzer.md
ls -l ~/.claude/skills/project-insight
ls -l ~/.claude/commands/insight
```

### Making Changes

**Adding a new agent:**

1. Create agent file: `agents/new-agent.md`
2. Define frontmatter (name, description, tools, model, color)
3. Write responsibilities and output format
4. Update SKILL.md to spawn the agent
5. Run `npm run link` to create symlink
6. Test

**Modifying existing agent:**

1. Edit agent file in `agents/`
2. Changes reflect immediately (symlink)
3. Test with `/insight`
4. Commit

**Changing orchestration:**

1. Edit `skills/project-insight/SKILL.md`
2. Modify execution algorithm
3. Test
4. Update README.md if user-visible changes

## Versioning

### When to Update Version

Update `.claude-plugin/plugin.json` version:

```json
{
  "version": "1.1.0"  // <- Increment
}
```

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
  - Remove an agent
  - Change output format significantly
  - Remove trigger phrases

- **MINOR** (1.0.0 → 1.1.0): New features
  - Add new agent
  - Add new analysis dimension
  - New command options

- **PATCH** (1.0.0 → 1.0.1): Bug fixes
  - Fix agent logic
  - Improve output clarity
  - Documentation updates

## Testing

### Manual Testing Checklist

**Basic flow:**
- [ ] `/insight` triggers skill
- [ ] Phase 1 runs 3 agents in parallel
- [ ] Phase 2 synthesizes results
- [ ] Report is well-formatted
- [ ] Health score makes sense

**Per agent:**
- [ ] tech-stack-analyzer detects languages correctly
- [ ] structure-analyzer identifies organization pattern
- [ ] readme-analyzer finds missing sections
- [ ] insight-synthesizer removes duplicates

**Edge cases:**
- [ ] Empty project directory
- [ ] No package.json (non-Node project)
- [ ] No README
- [ ] Very large project (10k+ files)

### Testing Individual Agents

You can test agents in isolation:

```
User: "Use the tech-stack-analyzer agent to analyze this project"

Claude: [Spawns only that agent]
```

### Debugging

**Check agent output:**
- Each agent should return structured findings
- Look for file:line references
- Verify no errors in agent execution

**Check synthesis:**
- Are duplicates removed?
- Is prioritization logical?
- Are quick wins actually quick?

## Model Selection Strategy

| Agent | Model | Reasoning |
|-------|-------|-----------|
| tech-stack-analyzer | sonnet | Deep dependency analysis, version checking |
| structure-analyzer | sonnet | Pattern recognition, architectural assessment |
| readme-analyzer | sonnet | Content quality evaluation, nuanced assessment |
| insight-synthesizer | haiku | Fast synthesis, straightforward deduplication |

**Cost optimization:**
- Phase 1 uses sonnet (parallel, need quality)
- Phase 2 uses haiku (sequential, but simple logic)

## Performance Optimization

### Current Performance

- Phase 1: 30-60 seconds (3 agents in parallel)
- Phase 2: 10-20 seconds (1 agent)
- Total: ~1-2 minutes

### If Too Slow

**Reduce scope:**
```markdown
### Step 1: Confirm Target
Ask user if they want:
- Full analysis (all 3 agents)
- Quick analysis (tech + structure only)
- Documentation only (readme agent)
```

**Optimize bash commands:**
```bash
# Bad (scans everything)
find . -type f

# Good (excludes node_modules)
find . -type f -not -path '*/node_modules/*'
```

## Common Issues

### Issue: Agents not found

**Diagnosis:**
```bash
ls -l ~/.claude/agents/
# Check if symlinks exist
```

**Solution:**
```bash
npm run link
```

### Issue: Phase 1 runs sequentially instead of parallel

**Cause:** Tasks were in separate response blocks

**Solution:** Ensure all Phase 1 Task calls are in a single response block in SKILL.md

### Issue: Synthesis quality is poor

**Cause:** Phase 1 agents didn't provide structured output

**Solution:** Enforce output format in agent definitions

## Future Enhancements

### Planned Agents

1. **test-coverage-analyzer**
   - Detect test files
   - Calculate coverage metrics
   - Suggest missing tests

2. **security-scanner**
   - Check for known vulnerabilities
   - Scan for hardcoded secrets
   - Validate dependencies

3. **performance-analyzer**
   - Identify performance anti-patterns
   - Bundle size analysis
   - Lazy loading opportunities

### Implementation Notes

**Adding test-coverage-analyzer:**

1. Create `agents/test-coverage-analyzer.md`
2. Tools: Bash (run coverage tools), Grep (find test files)
3. Model: sonnet
4. Update SKILL.md Phase 1 to include it
5. Update synthesizer to handle test coverage data

## Contributing

### Pull Request Checklist

- [ ] Update version in plugin.json
- [ ] Test all agents individually
- [ ] Test full pipeline
- [ ] Update README.md with user-facing changes
- [ ] Update CLAUDE.md with development notes
- [ ] Add agent description if new agent
- [ ] Verify parallel execution works

### Agent Creation Template

```markdown
---
name: your-agent
description: One-line description
tools: ["Read", "Glob"]
model: sonnet
color: blue
---

# Your Agent

## Responsibilities
[What this agent does]

## Analysis Strategy
[How it approaches the task]

## Output Format
[Expected structure]
```

## References

- [Session-wrap multi-agent patterns](https://github.com/team-attention/plugins-for-claude-natives/tree/main/plugins/session-wrap)
- [Anthropic's composable patterns](https://www.anthropic.com/news/claude-code-multi-agent-patterns)
- [Claude Code Task tool documentation](https://code.claude.com/docs)

## Support

For issues or questions:
- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
- Discussions: https://github.com/JayKim88/claude-ai-engineering/discussions
