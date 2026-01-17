# Learning Summary Skill

A Claude Code skill that captures and documents key learnings from conversations.

## What It Does

Analyzes your conversation with Claude and generates a structured markdown document with:
- Key concepts explained
- New knowledge gained
- Practical examples
- Important distinctions
- References and next steps

## Installation

### Global Installation (Recommended)

Already installed at: `~/.claude/skills/learning-summary/`

This makes it available in all projects.

### Project-Specific Installation

```bash
cp -r ~/.claude/skills/learning-summary ./.claude/skills/
```

## Usage

Simply ask Claude to summarize your learnings:

**English:**
```
"summarize what I learned"
"document my learnings"
"create learning summary"
```

**Korean:**
```
"지금까지 대화 정리해줘"
"배운 내용 문서화"
```

Claude will:
1. Analyze the conversation
2. Extract key insights
3. Generate a structured document
4. Save it to your dedicated AI learning repository

## Configuration

Edit `~/.claude/skills/learning-summary/config.yaml`:

```yaml
# Dedicated AI learning repository (absolute path)
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"

# Output directory (relative to learning_repo)
output_dir: "learnings"

# Auto-commit to git
auto_commit: false

# Auto-push to remote (requires auto_commit: true)
auto_push: false

# Language preference
language: auto
```

### Setup Your Learning Repository

1. **Create your AI learning repository** (or use an existing one):
   ```bash
   mkdir -p ~/Documents/Projects/ai-learning/learnings
   cd ~/Documents/Projects/ai-learning
   git init
   ```

2. **Update the config** to point to your repository:
   ```yaml
   learning_repo: "/Users/YOUR_USERNAME/Documents/Projects/ai-learning"
   ```

3. **Start learning!** All summaries will be saved to your dedicated repository.

## Output Example

Generated documents look like:

```markdown
# Understanding Claude Code Marketplaces and Plugins

## Key Concepts

### 1. What is a Marketplace?
A marketplace is a decentralized GitHub repository...

## New Learnings

### Before
- Thought marketplaces required Anthropic approval

### After
- Marketplaces are decentralized, anyone can create one

## Practical Examples

```bash
/plugin marketplace add team-attention/plugins
```

## References
- Documentation: https://...

## Next Steps
1. Install first plugin
2. Create custom skill
```

## Benefits

- **Never forget**: Capture important insights before they're lost
- **Structured**: Organized in a consistent, searchable format
- **Bilingual**: Supports Korean/English content
- **Portable**: Markdown files work everywhere

## File Naming

Documents are automatically named based on:
- Current date (YYYY-MM-DD)
- Main topic discussed

Example: `2026-01-17-claude-code-marketplace-guide.md`

## License

MIT
