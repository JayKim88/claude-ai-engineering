# Claude AI Engineering Toolkit

A curated collection of Claude Code skills, agents, and AI engineering experiments for enhancing developer productivity and exploring AI capabilities.

## Overview

This repository serves as both a learning playground and a production-ready toolkit for working with Claude Code. It includes reusable skills, specialized agents, and experimental projects that demonstrate various AI engineering patterns and best practices.

## Features

- **Modular Skills**: Standalone skills that can be installed individually or as a complete toolkit
- **Specialized Agents**: Purpose-built agents for specific development workflows
- **Dual Installation**: Support for both local development (symlinks) and user installation (npx)
- **Marketplace Ready**: Compatible with Claude Code's decentralized marketplace system
- **Portfolio Quality**: Production-ready code with comprehensive documentation

## Available Skills

### learning-summary

Automatically capture and document key learnings from Claude Code conversations with structured markdown output.

**Features:**
- Conversation analysis and insight extraction
- Structured document generation with customizable sections
- Git integration (auto-commit/push support)
- Bilingual support (English/Korean)
- Session history integration (planned)

**Usage:**
```bash
# Trigger in any conversation with:
"document this conversation"
"summarize key learnings"
"save this as learning notes"
```

## Installation

### For Users: Install via npx

Install all skills and agents:
```bash
npx github:jaykim/claude-ai-engineering
```

Install a specific skill:
```bash
npx github:jaykim/claude-ai-engineering learning-summary
```

List available items:
```bash
npx github:jaykim/claude-ai-engineering --list
```

### For Developers: Local Development

Clone and link to Claude Code for live development:

```bash
# Clone the repository
cd ~/Documents/Projects
git clone https://github.com/jaykim/claude-ai-engineering.git
cd claude-ai-engineering

# Link all skills and agents to Claude Code
npm run link
# or directly: ./scripts/link-local.sh

# Now edit files in this repo and test immediately in Claude Code
```

**Benefits of local development:**
- Edit files in your IDE
- Test changes immediately in Claude Code
- Commit and push directly to git
- No need to reinstall after changes

### Via Claude Code Marketplace

```bash
/plugin marketplace add jaykim/claude-ai-engineering
/plugin install claude-ai-engineering:learning-summary
```

## Repository Structure

```
claude-ai-engineering/
├── skills/              # Claude Code skills
│   └── learning-summary/
├── agents/              # Specialized agents (coming soon)
├── experiments/         # AI engineering experiments
├── scripts/
│   └── link-local.sh   # Local development setup
├── bin/
│   └── install.js      # npx installer
├── examples/           # Example outputs and usage
└── .claude-plugin/
    └── marketplace.json
```

## Usage Examples

### Learning Summary Skill

**Basic usage:**
```
User: "Please help me debug this authentication issue..."
[After conversation...]
User: "Document this learning"
```

**With customization:**
Claude will ask which sections to include, allowing you to choose:
- Key Insights
- Problem & Solution
- Code Examples
- Resources & References

**Configuration:**
Edit `~/.claude/skills/learning-summary/config.yaml`:
```yaml
learning_repo: "/path/to/your/learning/notes"
output_dir: "learnings"
auto_commit: true
auto_push: false

categories:
  - claude-code
  - debugging
  - authentication
```

## Development

### Adding New Skills

1. Create skill directory:
```bash
mkdir -p skills/your-skill-name
cd skills/your-skill-name
```

2. Create required files:
- `SKILL.md` - Skill definition with frontmatter
- `CLAUDE.md` - Execution instructions for Claude
- `.claude-plugin/plugin.json` - Plugin manifest

3. Register in marketplace:
```json
// .claude-plugin/marketplace.json
{
  "plugins": [
    {
      "name": "your-skill-name",
      "description": "Brief description",
      "source": "./skills/your-skill-name"
    }
  ]
}
```

4. Test locally:
```bash
npm run link
# Test in Claude Code
```

### Adding New Agents

Similar structure under `agents/` directory.

## Best Practices

### Skill Development
- Keep skills focused on a single responsibility
- Provide comprehensive error handling
- Include detailed documentation in `references/`
- Create executable scripts for complex operations
- Support configuration via `config.yaml`

### Documentation
- Use progressive disclosure (SKILL.md → CLAUDE.md → references/)
- Include practical examples
- Document all configuration options
- Add troubleshooting sections

### Testing
- Test with symlinked local development
- Verify npx installation works
- Test error scenarios
- Validate configuration parsing

## Contributing

Contributions are welcome! This repository serves as both a personal learning space and a community resource.

### Guidelines
1. Follow existing patterns and structure
2. Include comprehensive documentation
3. Add examples for new features
4. Test both local and npx installation
5. Update marketplace.json when adding plugins

## Project Goals

This repository aims to:
- **Learn**: Explore Claude Code capabilities and AI engineering patterns
- **Build**: Create production-ready tools for developer productivity
- **Share**: Contribute to the Claude Code ecosystem
- **Document**: Capture learnings and best practices along the way

## Roadmap

- [ ] Add more skills (session analysis, code review, etc.)
- [ ] Create specialized agents (refactoring, testing, documentation)
- [ ] Develop experiments with multi-agent patterns
- [ ] Build integration with external tools (GitHub, Linear, Notion)
- [ ] Create examples directory with sample outputs
- [ ] Add CI/CD for testing and validation

## Technical Stack

- **Runtime**: Claude Code CLI
- **Languages**: Bash, JavaScript (Node.js), Markdown
- **Configuration**: YAML
- **Distribution**: npm/npx, Git
- **Documentation**: Markdown with code examples

## License

MIT License - See LICENSE file for details

## Author

**Jay Kim**
- GitHub: [@jaykim](https://github.com/jaykim)
- Email: your-email@example.com

## Acknowledgments

- Anthropic team for Claude Code
- Claude Code community for patterns and best practices
- Inspired by [plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives)

---

**Note**: This is an active learning project. Skills and agents are continuously evolving based on real-world usage and experimentation.

