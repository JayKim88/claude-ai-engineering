# Claude AI Engineering Toolkit

A curated collection of Claude Code plugins featuring skills, agents, and multi-agent workflows for enhancing developer productivity.

## Overview

This repository serves as both a learning playground and a production-ready toolkit for working with Claude Code. It includes reusable plugins with skills, specialized agents, and experiments that demonstrate various AI engineering patterns and best practices.

## Features

- **Plugin-Based Architecture**: Self-contained plugins following official Claude Code patterns
- **Multi-Agent Workflows**: Parallel and sequential agent pipelines for complex analysis
- **Dual Installation**: Support for both local development (symlinks) and user installation (npx)
- **Marketplace Ready**: Compatible with Claude Code's decentralized marketplace system
- **Portfolio Quality**: Production-ready code with comprehensive documentation

## Available Plugins

### 1. learning-summary

Capture and document key learnings from Claude Code conversations with structured markdown output.

**Features:**
- Automatic conversation analysis and insight extraction
- Structured document generation with customizable sections
- Git integration (auto-commit/push support)
- Bilingual support (English/Korean)
- Session history integration (planned)

**Usage:**
```
"document this conversation"
"summarize key learnings"
"save this as learning notes"
```

**[View Plugin →](./plugins/learning-summary/README.md)**

### 2. project-insight

Comprehensive project analysis using a multi-agent pipeline to evaluate code quality, structure, and documentation.

**Features:**
- 4 specialized agents in 2-phase pipeline
- Tech stack detection (languages, frameworks, dependencies)
- Structure analysis (organization, patterns, metrics)
- Documentation review (README quality, missing sections)
- Actionable recommendations (Critical/Important/Beneficial)
- Health scoring (X/10)

**Usage:**
```
/insight
"analyze this project"
"project health check"
```

**[View Plugin →](./plugins/project-insight/README.md)**

## Installation

### For Users: Install via npx

```bash
# Install all plugins
npx github:JayKim88/claude-ai-engineering

# Install specific plugin
npx github:JayKim88/claude-ai-engineering learning-summary
npx github:JayKim88/claude-ai-engineering project-insight

# List available plugins
npx github:JayKim88/claude-ai-engineering --list
```

### For Developers: Local Development

Clone and link to Claude Code for live development:

```bash
# Clone the repository
cd ~/Documents/Projects
git clone https://github.com/JayKim88/claude-ai-engineering.git
cd claude-ai-engineering

# Link all plugins to Claude Code
npm run link

# Now edit files in plugins/ and test immediately in Claude Code
```

**Benefits of local development:**
- Edit files in your IDE
- Changes reflect immediately via symlinks
- Test in Claude Code without reinstalling
- Commit and push directly to git

### Via Claude Code Marketplace (Coming Soon)

```bash
/plugin marketplace add JayKim88/claude-ai-engineering
/plugin install learning-summary
/plugin install project-insight
```

## Repository Structure

```
claude-ai-engineering/
├── plugins/                    # All plugins (self-contained)
│   ├── learning-summary/
│   │   ├── .claude-plugin/
│   │   ├── skills/
│   │   ├── README.md          # User documentation
│   │   └── CLAUDE.md          # Developer guide
│   └── project-insight/
│       ├── .claude-plugin/
│       ├── agents/            # Multi-agent components
│       ├── skills/
│       ├── commands/
│       ├── README.md
│       └── CLAUDE.md
├── templates/                  # Templates for new plugins
│   ├── plugin-template/
│   └── NEW_PLUGIN_GUIDE.md    # Step-by-step guide
├── scripts/
│   └── link-local.sh          # Local development setup
├── bin/
│   └── install.js             # npx installer
└── .claude-plugin/
    └── marketplace.json       # Marketplace manifest
```

## Creating New Plugins

We provide templates and a comprehensive guide to create new plugins following the established structure.

### Quick Start

```bash
# Copy the template
cp -r templates/plugin-template plugins/your-plugin-name

# Customize files (see NEW_PLUGIN_GUIDE.md)

# Link and test
npm run link

# Commit
git add plugins/your-plugin-name
git commit -m "feat: add your-plugin-name plugin"
```

### Detailed Guide

See **[templates/NEW_PLUGIN_GUIDE.md](./templates/NEW_PLUGIN_GUIDE.md)** for a complete step-by-step guide including:

- Plugin planning and structure
- File customization checklist
- Multi-agent vs simple skill patterns
- Testing and deployment
- Best practices and examples

## Plugin Patterns

### Pattern 1: Simple Skill

**Example:** learning-summary

**Use when:**
- Single-step task
- Direct user interaction
- No parallel processing needed

### Pattern 2: Multi-Agent Pipeline

**Example:** project-insight

**Use when:**
- Multi-dimensional analysis
- Parallel processing beneficial
- Need to consolidate results

**2-Phase Pipeline:**
```
Phase 1 (Parallel)          Phase 2 (Sequential)
┌─────────────┐             ┌─────────────┐
│  Agent A    │────┐        │             │
├─────────────┤    ├───────▶│  Validator  │
│  Agent B    │────┤        │             │
├─────────────┤    │        └─────────────┘
│  Agent C    │────┘
└─────────────┘
```

## Development

### Local Development Workflow

1. **Edit files** in `plugins/your-plugin/`
2. **Changes reflect immediately** (via symlinks)
3. **Test in Claude Code**
4. **Commit when satisfied**

### Adding a New Plugin

Follow the guide in `templates/NEW_PLUGIN_GUIDE.md`.

### Updating marketplace.json

When adding a new plugin:

```json
{
  "plugins": [
    {
      "name": "your-plugin-name",
      "description": "Brief description",
      "source": "./plugins/your-plugin-name"
    }
  ]
}
```

## Best Practices

### Plugin Development
- Keep plugins self-contained and focused
- Include both README.md (user) and CLAUDE.md (developer)
- Follow the template structure
- Provide comprehensive error handling
- Document trigger phrases clearly

### Documentation
- README.md: User-facing installation and usage
- CLAUDE.md: Developer notes, architecture, testing
- SKILL.md: Execution algorithm with trigger phrases
- Progressive disclosure (overview → details → references)

### Testing
- Test with local symlinks first
- Verify npx installation works
- Test all trigger phrases
- Validate error scenarios

## Contributing

Contributions are welcome! This repository serves as both a personal learning space and a community resource.

### Guidelines
1. Follow existing plugin patterns and structure
2. Use templates for new plugins
3. Include comprehensive documentation (README + CLAUDE)
4. Test both local and npx installation
5. Update marketplace.json when adding plugins

### Pull Request Checklist
- [ ] Plugin follows template structure
- [ ] README.md is user-friendly and complete
- [ ] CLAUDE.md has development notes
- [ ] Tested locally (`npm run link`)
- [ ] Tested npx installation
- [ ] marketplace.json updated
- [ ] Commit message follows conventional commits

## Project Goals

This repository aims to:
- **Learn**: Explore Claude Code capabilities and AI engineering patterns
- **Build**: Create production-ready tools for developer productivity
- **Share**: Contribute to the Claude Code ecosystem
- **Document**: Capture learnings and best practices along the way

## Roadmap

- [x] Plugin-based architecture
- [x] Multi-agent workflow (project-insight)
- [x] Learning documentation tool
- [x] Template system for new plugins
- [ ] More analysis plugins (git, code quality, security)
- [ ] Integration plugins (GitHub, Linear, Notion)
- [ ] CI/CD for testing and validation
- [ ] Example outputs and demos

## Technical Stack

- **Runtime**: Claude Code CLI
- **Languages**: Bash, JavaScript (Node.js), Markdown
- **Configuration**: YAML, JSON
- **Distribution**: npm/npx, Git, Marketplace
- **Documentation**: Markdown with code examples

## Resources

- **Plugin Templates**: `templates/plugin-template/`
- **Creation Guide**: `templates/NEW_PLUGIN_GUIDE.md`
- **Example Plugins**: `plugins/learning-summary/`, `plugins/project-insight/`
- **Official Patterns**: [plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives)
- **Claude Code Docs**: https://code.claude.com/docs

## License

MIT License - See LICENSE file for details

## Author

**Jay Kim**
- GitHub: [@JayKim88](https://github.com/JayKim88)

## Acknowledgments

- Anthropic team for Claude Code
- Claude Code community for patterns and best practices
- Inspired by [plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives) architecture
- Multi-agent patterns from [session-wrap](https://github.com/team-attention/plugins-for-claude-natives/tree/main/plugins/session-wrap)

---

**Note**: This is an active learning project. Plugins are continuously evolving based on real-world usage and experimentation.
