# New Plugin Creation Guide

Step-by-step guide to creating a new plugin following the claude-ai-engineering structure.

## Quick Start

```bash
# 1. Copy the template
cp -r templates/plugin-template plugins/your-plugin-name

# 2. Customize the files (see below)

# 3. Link to Claude Code
npm run link

# 4. Test
# In Claude Code: "your trigger phrase"

# 5. Commit
git add plugins/your-plugin-name
git commit -m "feat: add your-plugin-name plugin"
```

## Step-by-Step Guide

### Step 1: Plan Your Plugin

Answer these questions:

1. **What does it do?** (one sentence)
2. **What are the trigger phrases?**
3. **Does it need agents?** (multi-step analysis) or just a skill?
4. **Does it need a command?** (like `/insight`)
5. **What are the key features?**

**Example:**
- What: "Analyzes git commit history and suggests improvements"
- Triggers: "analyze commits", "review commit history"
- Agents: Yes - 1 analyzer, 1 suggester
- Command: `/commit-review`
- Features: Pattern detection, message quality scoring, best practices

### Step 2: Copy Template

```bash
cd ~/Documents/Projects/claude-ai-engineering

# Choose a descriptive kebab-case name
PLUGIN_NAME="your-plugin-name"

# Copy template
cp -r templates/plugin-template plugins/$PLUGIN_NAME
```

### Step 3: Customize Files

#### 3.1 Update plugin.json

Edit `plugins/your-plugin-name/.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin-name",           // ← Change this
  "version": "1.0.0",
  "description": "Your description",     // ← Change this
  "author": {
    "name": "jaykim",
    "url": "https://github.com/JayKim88"
  },
  "license": "MIT",
  "keywords": [
    "claude-code",
    "your-keyword-1",                    // ← Change these
    "your-keyword-2"
  ]
}
```

#### 3.2 Write README.md

Edit `plugins/your-plugin-name/README.md`:

1. Replace all `PLUGIN_NAME` with your plugin name
2. Replace all `COMMAND_NAME` with your command name (if applicable)
3. Fill in:
   - Features section
   - Trigger phrases
   - Usage examples
   - Configuration (if applicable)
   - Tips and troubleshooting

**Use existing plugins as reference:**
- Simple skill: `plugins/learning-summary/README.md`
- Multi-agent: `plugins/project-insight/README.md`

#### 3.3 Write CLAUDE.md

Edit `plugins/your-plugin-name/CLAUDE.md`:

1. Replace `PLUGIN_NAME` with your plugin name
2. Document:
   - Directory structure
   - Development workflow
   - Architecture (if multi-agent)
   - Testing procedures
   - Common issues

**Purpose:** Help your future self and other developers understand the plugin.

#### 3.4 Create Skill

Rename and edit `plugins/your-plugin-name/skills/PLUGIN_NAME/`:

```bash
mv plugins/your-plugin-name/skills/PLUGIN_NAME \
   plugins/your-plugin-name/skills/your-skill-name
```

Edit `SKILL.md`:

```yaml
---
name: your-skill-name
description: Trigger phrases here. Use when user says "phrase 1", "phrase 2"...
version: 1.0.0
---

# Your Skill Name

## Trigger Phrases
- "phrase 1"
- "phrase 2"

## Execution Algorithm

### Step 1: [Describe what happens first]
### Step 2: [Next step]
### Step 3: [Present results]
```

**Key points:**
- `name` must match the directory name
- `description` must include trigger phrases
- Execution algorithm should be clear step-by-step

#### 3.5 Create Agents (if multi-agent)

For each agent you need:

```bash
cp templates/plugin-template/agents/agent-template.md \
   plugins/your-plugin-name/agents/your-agent-name.md
```

Edit each agent file:

```yaml
---
name: your-agent-name         # Must match filename (without .md)
description: What it does
tools: ["Read", "Glob"]       # What tools it needs
model: sonnet                 # sonnet, haiku, or opus
color: blue                   # UI indicator
---

# Agent responsibilities, strategy, output format...
```

**Update SKILL.md to spawn agents:**

```markdown
### Step 2: Phase 1 - Parallel Analysis

```python
Task(subagent_type="your-agent-1", ...)
Task(subagent_type="your-agent-2", ...)
```
```

#### 3.6 Create Command (optional)

If you want a `/command`:

```bash
mkdir -p plugins/your-plugin-name/commands/your-command
```

Create `plugins/your-plugin-name/commands/your-command/your-command.md`:

```markdown
---
description: Command description
allowed-tools: Read, Task, AskUserQuestion
---

# /your-command Command

What it does, how to use it...
```

### Step 4: Update Marketplace

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "learning-summary",
      "description": "...",
      "source": "./plugins/learning-summary"
    },
    {
      "name": "project-insight",
      "description": "...",
      "source": "./plugins/project-insight"
    },
    {
      "name": "your-plugin-name",              // ← Add this
      "description": "Your description",
      "source": "./plugins/your-plugin-name"
    }
  ]
}
```

### Step 5: Link and Test

```bash
# Create symlinks
npm run link

# Verify
ls -l ~/.claude/skills/your-skill-name
ls -l ~/.claude/agents/your-agent-name.md  # if you have agents
ls -l ~/.claude/commands/your-command      # if you have command

# Test in Claude Code
```

In Claude Code:
```
User: "your trigger phrase"
→ Should trigger your skill
→ Test all functionality
→ Verify output
```

### Step 6: Commit

```bash
git add plugins/your-plugin-name
git add .claude-plugin/marketplace.json

git commit -m "feat: add your-plugin-name plugin

Brief description of what it does.

Features:
- Feature 1
- Feature 2
- Feature 3

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push
```

## Plugin Patterns

### Pattern 1: Simple Skill (No Agents)

**Example:** learning-summary

**Structure:**
```
plugins/your-plugin/
├── .claude-plugin/plugin.json
├── skills/your-skill/SKILL.md
├── README.md
└── CLAUDE.md
```

**Use when:**
- Single-step task
- No parallel processing needed
- Direct user interaction

### Pattern 2: Multi-Agent Pipeline

**Example:** project-insight

**Structure:**
```
plugins/your-plugin/
├── .claude-plugin/plugin.json
├── agents/
│   ├── analyzer-1.md
│   ├── analyzer-2.md
│   └── synthesizer.md
├── skills/your-skill/SKILL.md
├── commands/your-command/
├── README.md
└── CLAUDE.md
```

**Use when:**
- Multi-dimensional analysis
- Parallel processing beneficial
- Need to consolidate results

**2-Phase Pipeline:**
1. Phase 1: Multiple agents run in parallel (analysis)
2. Phase 2: One agent consolidates (synthesis)

### Pattern 3: Command + Skill

**Example:** project-insight with `/insight`

**Structure:**
```
plugins/your-plugin/
├── commands/your-command/your-command.md
├── skills/your-skill/SKILL.md
...
```

**Use when:**
- Want both command and trigger phrase access
- User might prefer explicit command

## File Naming Conventions

- **Plugin directory:** `kebab-case` (e.g., `project-insight`)
- **Skill name:** `kebab-case` (e.g., `project-insight`)
- **Agent files:** `kebab-case.md` (e.g., `tech-stack-analyzer.md`)
- **Command files:** `kebab-case.md` (e.g., `insight.md`)

**Must match:**
- Plugin directory name = plugin.json `name` field
- Skill directory name = SKILL.md `name` field
- Agent filename (without .md) = agent frontmatter `name` field

## Checklist

Before committing your new plugin:

- [ ] All `PLUGIN_NAME` placeholders replaced
- [ ] plugin.json has correct name, description, keywords
- [ ] README.md is user-friendly and complete
- [ ] CLAUDE.md has development notes
- [ ] SKILL.md has clear trigger phrases
- [ ] Agents have proper frontmatter (if applicable)
- [ ] marketplace.json includes new plugin
- [ ] Symlinks work (`npm run link`)
- [ ] Tested in Claude Code
- [ ] Git committed with descriptive message

## Tips

1. **Start simple**: Begin with a basic skill, add agents later if needed
2. **Copy existing plugins**: Use learning-summary or project-insight as reference
3. **Test early**: Link and test after each major change
4. **Document as you go**: Update README.md and CLAUDE.md while building
5. **Follow existing patterns**: Consistency helps maintainability

## Examples

### Example 1: Simple Skill

```bash
# Create git-summary plugin
cp -r templates/plugin-template plugins/git-summary
cd plugins/git-summary

# Edit files
# - plugin.json: name, description, keywords
# - README.md: features, usage examples
# - skills/git-summary/SKILL.md: trigger phrases, execution

npm run link
# Test: "summarize my git history"
```

### Example 2: Multi-Agent

```bash
# Create code-quality plugin
cp -r templates/plugin-template plugins/code-quality
cd plugins/code-quality

# Create agents
cp ../templates/plugin-template/agents/agent-template.md agents/linter-analyzer.md
cp ../templates/plugin-template/agents/agent-template.md agents/complexity-analyzer.md
cp ../templates/plugin-template/agents/agent-template.md agents/quality-synthesizer.md

# Edit all files
# - Update agent frontmatter
# - Update SKILL.md to spawn agents
# - Document in CLAUDE.md

npm run link
# Test: "analyze code quality"
```

## Troubleshooting

**Issue**: Skill not triggering
- Check SKILL.md `description` has trigger phrases
- Verify symlink: `ls -l ~/.claude/skills/your-skill`
- Run `npm run link` again

**Issue**: Agent not found
- Check agent filename matches frontmatter `name`
- Verify symlink: `ls -l ~/.claude/agents/your-agent.md`
- Ensure SKILL.md uses correct `subagent_type`

**Issue**: Command not working
- Check command directory structure
- Verify symlink: `ls -l ~/.claude/commands/your-command`
- Ensure command.md has proper frontmatter

## Resources

- **Existing plugins**: Study `plugins/learning-summary` and `plugins/project-insight`
- **Session-wrap**: https://github.com/team-attention/plugins-for-claude-natives/tree/main/plugins/session-wrap
- **Claude Code docs**: https://code.claude.com/docs
- **Multi-agent patterns**: https://www.anthropic.com/news/claude-code-multi-agent-patterns

## Support

Questions or issues?
- Open an issue: https://github.com/JayKim88/claude-ai-engineering/issues
- Check discussions: https://github.com/JayKim88/claude-ai-engineering/discussions

Happy plugin building! 🚀
