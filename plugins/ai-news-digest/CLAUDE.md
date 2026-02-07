# PLUGIN_NAME Plugin - Development Guide

Development and maintenance guide for the PLUGIN_NAME plugin.

## Directory Structure

```
PLUGIN_NAME/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata and version
├── skills/
│   └── PLUGIN_NAME/
│       ├── SKILL.md          # Skill definition
│       └── [other files]
├── agents/                   # (if using multi-agent pattern)
│   └── agent-name.md
├── commands/                 # (if providing command)
│   └── command-name/
│       └── command-name.md
├── README.md                 # User documentation
└── CLAUDE.md                 # Development guide (you are here)
```

## Development Workflow

### Local Development Setup

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link

# Verify symlink
ls -l ~/.claude/skills/PLUGIN_NAME
```

### Making Changes

1. Edit files in monorepo: `plugins/PLUGIN_NAME/`
2. Changes reflect immediately via symlink
3. Test in Claude Code
4. Commit when satisfied

## Versioning

### When to Update Version

Update `.claude-plugin/plugin.json` version before committing:

```json
{
  "version": "1.0.1"  // <- Increment this
}
```

### Semantic Versioning Rules

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features (backward compatible)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes and docs

## Testing

### Manual Testing

- [ ] Test basic functionality
- [ ] Test edge cases
- [ ] Verify error handling
- [ ] Check output format

## Architecture (if multi-agent)

[Describe agent roles, execution flow, etc.]

## Common Issues

### Issue: [Problem]

**Diagnosis:**
```bash
[How to diagnose]
```

**Solution:**
```bash
[How to fix]
```

## Future Enhancements

- [ ] Planned improvement 1
- [ ] Planned improvement 2

## Contributing

### Pull Request Checklist

- [ ] Update version in plugin.json
- [ ] Test functionality
- [ ] Update README.md if user-facing changes
- [ ] Update CLAUDE.md with development notes

## References

- [Relevant documentation links]

## Support

For issues or questions:
- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
