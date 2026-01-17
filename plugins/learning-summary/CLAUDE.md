# Learning Summary Plugin - Development Guide

Development and maintenance guide for the learning-summary plugin.

## Directory Structure

```
learning-summary/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata and version
├── skills/
│   └── learning-summary/
│       ├── SKILL.md          # Skill definition (frontmatter + overview)
│       ├── CLAUDE.md         # Detailed execution instructions for Claude
│       ├── config.yaml       # User configuration template
│       ├── scripts/
│       │   ├── parse-config.sh     # Parse YAML without dependencies
│       │   ├── git-commit.sh       # Git commit automation
│       │   └── save-learning.sh    # Main save workflow
│       └── references/
│           ├── template.md               # Document template examples
│           ├── best-practices.md         # Writing guidelines
│           ├── configuration.md          # Config documentation
│           └── session-history-integration.md  # Future feature
├── README.md                 # User-facing documentation (this plugin)
└── CLAUDE.md                 # Development guide (you are here)
```

## Development Workflow

### Local Development Setup

1. **Link plugin to Claude Code:**
   ```bash
   cd ~/Documents/Projects/claude-ai-engineering
   npm run link
   ```

2. **Verify symlink:**
   ```bash
   ls -l ~/.claude/skills/learning-summary
   # Should point to: .../plugins/learning-summary/skills/learning-summary
   ```

3. **Test the skill:**
   ```bash
   # In any Claude Code session
   "document this conversation"
   ```

### Making Changes

**When editing files:**
- Edit in the monorepo: `~/Documents/Projects/claude-ai-engineering/plugins/learning-summary/`
- Changes reflect immediately via symlink (no need to re-link)
- Test in Claude Code
- Commit to git when satisfied

**File modification checklist:**
- [ ] Edit files in monorepo
- [ ] Test with Claude Code
- [ ] Update version in `.claude-plugin/plugin.json` if needed
- [ ] Update README.md if user-facing changes
- [ ] Commit changes

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
  - Config format changes
  - Removed features
  - Changed trigger phrases

- **MINOR** (1.0.0 → 1.1.0): New features (backward compatible)
  - New sections
  - New configuration options
  - New scripts

- **PATCH** (1.0.0 → 1.0.1): Bug fixes and docs
  - Bug fixes
  - Documentation updates
  - Script improvements

### Version Update Checklist

- [ ] Update `.claude-plugin/plugin.json` version
- [ ] Update README.md if needed
- [ ] Test all features
- [ ] Commit with version in message: `chore: bump version to 1.0.1`

## Testing

### Manual Testing

1. **Basic flow:**
   ```
   User: "document this conversation"
   → Should trigger skill
   → Should ask section preferences
   → Should generate markdown
   → Should save to configured location
   ```

2. **Git integration:**
   ```yaml
   # config.yaml
   auto_commit: true
   auto_push: false
   ```
   - Verify commit is created
   - Check commit message format

3. **Config parsing:**
   ```bash
   cd ~/.claude/skills/learning-summary
   ./scripts/parse-config.sh
   echo $LEARNING_REPO  # Should show configured path
   ```

### Edge Cases

- [ ] Empty conversation (should warn user)
- [ ] Non-existent learning repository (should create or error)
- [ ] Git not initialized (should work without git features)
- [ ] Config file missing (should use defaults)

## Architecture

### Execution Flow

```
User triggers skill
     ↓
SKILL.md defines trigger phrases
     ↓
Claude reads CLAUDE.md for instructions
     ↓
1. Analyze conversation
2. Ask user for section preferences
3. Generate markdown content
4. Parse config (scripts/parse-config.sh)
5. Save file (scripts/save-learning.sh)
6. Git commit (scripts/git-commit.sh) if enabled
     ↓
Show success message to user
```

### Script Dependencies

**parse-config.sh:**
- Parses YAML without external dependencies
- Sets environment variables for other scripts
- Fallback to defaults if config missing

**save-learning.sh:**
- Sources parse-config.sh
- Generates filename (YYYY-MM-DD-topic.md)
- Writes content to file
- Creates directory if needed

**git-commit.sh:**
- Checks if git repo exists
- Stages file
- Commits with standard message format
- Optionally pushes (if auto_push: true)

## Common Issues

### Issue: Skill not triggering

**Diagnosis:**
```bash
ls -l ~/.claude/skills/learning-summary
# Check if symlink exists and points to correct location
```

**Solution:**
```bash
npm run link
```

### Issue: Scripts not executable

**Diagnosis:**
```bash
ls -la ~/.claude/skills/learning-summary/scripts/
# Check if scripts have execute permission (x flag)
```

**Solution:**
```bash
chmod +x ~/.claude/skills/learning-summary/scripts/*.sh
```

### Issue: Config not being read

**Diagnosis:**
```bash
cat ~/.claude/skills/learning-summary/config.yaml
# Check if file exists and has correct YAML syntax
```

**Solution:**
- Fix YAML syntax errors
- Ensure keys match what parse-config.sh expects

## Future Enhancements

### Planned Features (from references/session-history-integration.md)

1. **Multi-Session Analysis:**
   - Analyze last 24 hours of conversations
   - Weekly learning summaries
   - Project-specific session aggregation

2. **Session History Integration:**
   - Read from `~/.claude/projects/<encoded-cwd>/*.jsonl`
   - Extract conversations programmatically
   - Batch process multiple sessions

3. **Advanced Categorization:**
   - Auto-detect categories from conversation content
   - Suggest tags based on topics discussed
   - Link related learnings

### Implementation Notes

When implementing session history:
- Use parallel Task agents for large session files (6+ files)
- Read `.jsonl` files line by line (can be large)
- Filter by date range
- Aggregate insights across sessions

## Contributing

### Pull Request Checklist

- [ ] Update version in plugin.json
- [ ] Add tests for new features
- [ ] Update README.md with user-facing changes
- [ ] Update CLAUDE.md with development notes
- [ ] Follow existing code style
- [ ] Ensure scripts are executable
- [ ] Test locally before submitting

### Code Style

**Bash scripts:**
- Use `set -e` for error handling
- Quote all variables: `"$VAR"`
- Add comments for complex logic
- Exit codes: 0 = success, 1 = error

**Markdown:**
- Use ATX headings (##)
- Fence code blocks with language
- Keep lines under 100 characters where reasonable

## Maintenance

### Regular Tasks

**Monthly:**
- [ ] Review and update best-practices.md
- [ ] Check for broken links in documentation
- [ ] Update template.md with new examples

**Per Release:**
- [ ] Test all trigger phrases
- [ ] Verify git integration
- [ ] Check config parsing
- [ ] Update changelog

## References

- [Claude Code Skills Documentation](https://code.claude.com/docs)
- [YAML Specification](https://yaml.org/spec/)
- [Semantic Versioning](https://semver.org/)

## Support

For issues or questions:
- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
- Discussions: https://github.com/JayKim88/claude-ai-engineering/discussions
