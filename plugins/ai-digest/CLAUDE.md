# AI Digest Plugin - Development Guide

Development and maintenance guide for the ai-digest plugin.

## Directory Structure

```
ai-digest/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata and version
├── commands/
│   └── ai-digest/
│       └── ai-digest.md      # /ai-digest command definition
├── skills/
│   └── ai-digest/
│       └── SKILL.md          # Skill execution algorithm
├── README.md                 # User documentation
└── CLAUDE.md                 # Development guide (you are here)
```

## Development Workflow

### Local Development Setup

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link

# Verify symlinks
ls -l ~/.claude/skills/ai-digest
ls -l ~/.claude/commands/ai-digest
```

### Making Changes

1. Edit files in monorepo: `plugins/ai-digest/`
2. Changes reflect immediately via symlink
3. Test in Claude Code with `/ai-digest` or trigger phrases
4. Commit when satisfied

## Architecture

### Simple Skill Pattern

This plugin uses the **Simple Skill** pattern (not multi-agent):

```
User Input (/ai-digest URL)
    ↓
Parse input (URL, focus, content)
    ↓
WebFetch (if URL) or Direct Content
    ↓
Analyze Content
    ↓
Generate Structured Document
    ↓
Read learning-summary Config
    ↓
Save to ai-learning repo
    ↓
Git commit/push (if enabled)
    ↓
Confirm to user
```

**Why simple skill?**
- Single-step task (no parallel analysis needed)
- WebFetch handles content retrieval
- Analysis is straightforward (extract and structure)
- No need for agent coordination

### Key Components

**1. Command Definition** (`commands/ai-digest/ai-digest.md`)
- Entry point for `/ai-digest`
- Triggers the ai-digest skill
- Allowed tools: Read, Write, Bash, WebFetch, AskUserQuestion

**2. Skill Definition** (`skills/ai-digest/SKILL.md`)
- Execution algorithm (9 steps)
- Trigger phrases
- Error handling
- Configuration reuse

**3. Configuration** (Reuses learning-summary)
- No separate config file
- Reads from `~/.claude/skills/learning-summary/config.yaml`
- Falls back to asking user if config missing

## Execution Flow Details

### Step 1: Parse Input

**Goal**: Extract URL, focus, and content from user message

**Examples**:
```
Input: "/ai-digest https://example.com"
→ URL: https://example.com, Focus: None, Content: None

Input: "/ai-digest 'Focus on API changes' https://example.com"
→ URL: https://example.com, Focus: "API changes", Content: None

Input: "/ai-digest 'Analyze: [text]'"
→ URL: None, Focus: None, Content: [text]
```

**Implementation**:
- Regex or string parsing to extract URL patterns
- Remaining text is focus or content

### Step 2: Fetch Content

**If URL provided**:
```python
WebFetch(
    url=url,
    prompt="Extract main content, technical details, code examples..."
)
```

**WebFetch will**:
- Fetch the URL
- Convert HTML to markdown
- Filter out navigation/ads
- Return clean content

**If direct content**:
- Use provided text as-is

### Step 3: Analyze Content

**Key extraction logic**:
1. Identify main topic
2. Extract changes/concepts
3. Find practical applications
4. Collect code examples
5. Note limitations

**Consider user focus**:
- If focus = "API changes", emphasize API sections
- If focus = "code examples", extract more examples

### Step 4-5: Config and Filename

**Config reading**:
```yaml
# ~/.claude/skills/learning-summary/config.yaml
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"
auto_commit: false
auto_push: false
```

**Output directory**: Hardcoded to `digests/` (not configurable)

**Filename generation**:
- Parse main topic from content
- Slugify: lowercase, kebab-case, max 4-5 words
- Prefix with "ai-"
- Example: `2026-01-25-ai-claude-sonnet-4-5-release.md`

### Step 6: Generate Document

**Use AI-specific template**:
- Bilingual (Korean/English)
- Sections: 요약, 주요 변경사항, 실무 적용, 코드 예제
- Tags for searchability
- Source attribution

**Conditional sections**:
- Include "Before/After" only if migration/upgrade content exists
- Include "주의사항" only if warnings exist
- Always include: 요약, 주요 변경사항, 실무 적용, 참고 링크

### Step 7-8: Save and Git

**Save**:
```bash
mkdir -p {learning_repo}/digests
# Write document using Write tool
```

**Git (if auto_commit)**:
```bash
cd {learning_repo}
git add digests/{filename}
git commit -m "Add AI digest: {topic}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# If auto_push
git push
```

### Step 9: Confirm

**Show user**:
- ✅ Full file path
- 📝 Summary of what was captured
- 🔗 Original URL (if applicable)
- 🔧 Git status
- 💡 Next action suggestions

## Testing

### Manual Testing Checklist

**Basic functionality:**
- [ ] `/ai-digest [URL]` works
- [ ] Trigger phrase "digest this article [URL]" works
- [ ] Direct content input works
- [ ] Focus parameter works ("Focus on X")

**Content extraction:**
- [ ] Fetches URL content correctly
- [ ] Extracts main topic
- [ ] Identifies code examples
- [ ] Captures key changes/concepts

**Document generation:**
- [ ] Filename is descriptive and dated
- [ ] Template sections are populated
- [ ] Code blocks are properly formatted
- [ ] Tags are relevant

**Configuration:**
- [ ] Reads learning-summary config
- [ ] Falls back if config missing
- [ ] Creates output directory if needed
- [ ] Saves to correct location

**Git integration:**
- [ ] Commits if auto_commit: true
- [ ] Skips commit if auto_commit: false
- [ ] Pushes if auto_push: true
- [ ] Handles non-git repos gracefully

**Edge cases:**
- [ ] Invalid URL (WebFetch fails)
- [ ] Empty content
- [ ] Config file missing
- [ ] Write permission denied
- [ ] Very long articles
- [ ] Articles with no code examples

### Test URLs

Use these for testing:
```bash
# Good test cases
/ai-digest https://anthropic.com/news/claude-sonnet-4-5
/ai-digest https://openai.com/blog/chatgpt-plus
/ai-digest https://python.langchain.com/docs/

# Edge cases
/ai-digest https://invalid-url-12345.com  # Should fail gracefully
/ai-digest "Analyze: Short text"          # Should warn about insufficient content
```

## Versioning

### When to Update Version

Update `.claude-plugin/plugin.json` version before committing:

```json
{
  "version": "1.0.1"  // <- Increment this
}
```

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
  - Change template format significantly
  - Remove trigger phrases
  - Change config location

- **MINOR** (1.0.0 → 1.1.0): New features
  - Add new sections to template
  - Add batch processing
  - Add new trigger phrases

- **PATCH** (1.0.0 → 1.0.1): Bug fixes
  - Fix URL parsing
  - Improve error messages
  - Documentation updates

## Common Issues

### Issue: WebFetch fails

**Diagnosis:**
```
Error: Failed to fetch URL. Please check the link and try again.
```

**Causes:**
- Invalid URL
- Website blocks bots
- Network issues
- Paywall/authentication required

**Solution:**
```
Prompt user to paste content directly:
"Paste the article content and I'll analyze it for you."
```

### Issue: Config not found

**Diagnosis:**
```
Warning: Config file not found at ~/.claude/skills/learning-summary/config.yaml
```

**Solution:**
```
Ask user:
"Where should I save the learning document?"

Then use provided path or create default config.
```

### Issue: Duplicate documents

**Current behavior**: Creates new document each time

**Future enhancement**: Check if topic already exists and offer to update

**Workaround**: Manually check learnings directory or use git log

### Issue: Empty document sections

**Cause**: Article doesn't contain expected content type

**Solution**: Skip empty sections or add placeholder text

## Configuration Reuse

### Why Reuse learning-summary Config?

**Benefits:**
1. Consistency: All learning docs in one place
2. No duplicate config management
3. Same git settings for both plugins
4. Simpler user experience

**Shared config fields:**
- `learning_repo`: Where to save documents
- `auto_commit`: Git commit behavior
- `auto_push`: Git push behavior

**Independent behavior:**
- ai-digest uses `digests/` folder (hardcoded)
- ai-digest uses "ai-" filename prefix
- ai-digest uses different template
- ai-digest has different trigger phrases

**Folder structure:**
```
ai-learning/
├── learnings/    # learning-summary output
└── digests/      # ai-digest output
```

## Future Enhancements

### Planned Features

1. **Batch URL Processing**
   ```bash
   /ai-digest https://url1 https://url2 https://url3
   ```
   - Process multiple URLs in one command
   - Generate separate documents
   - Summary report at end

2. **Update Existing Documents**
   - Detect if topic already documented
   - Offer to update vs create new
   - Merge new information

3. **Tag-Based Organization**
   - Auto-suggest tags based on content
   - Organize by tags (#ai, #llm, #api)
   - Search by tag

4. **Export Formats**
   - Export to Notion
   - Export to Obsidian
   - JSON export for programmatic access

5. **Weekly Digests**
   - Summarize week's digested articles
   - Cross-link related content
   - Highlight key themes

### Implementation Notes

**Batch processing**:
- Parse multiple URLs from input
- Process sequentially (WebFetch limitations)
- Use Task tool to parallelize if needed

**Update existing**:
- Grep for similar titles in digests/
- Ask user: "Found 2026-01-20-ai-claude-sonnet-4.md. Update or create new?"
- Merge sections intelligently

## Performance Considerations

### WebFetch Timing

- Typical fetch: 3-5 seconds
- Large articles: 10-15 seconds
- Paywall/auth: Immediate fail

**Optimization**: Cache fetched content for retry scenarios

### Document Generation

- Analysis: 5-10 seconds
- Template population: 1-2 seconds
- Total: ~10-20 seconds per article

**Fast enough for single articles**, batch processing may need progress indicators.

## Contributing

### Pull Request Checklist

- [ ] Update version in plugin.json
- [ ] Test with multiple URL types
- [ ] Test direct content input
- [ ] Test focus parameter
- [ ] Verify config reuse works
- [ ] Test git integration
- [ ] Update README.md if user-facing changes
- [ ] Update CLAUDE.md with technical notes

### Code Style

**Markdown:**
- Use ATX headings (##)
- Fence code blocks with language
- Keep lines under 100 characters where reasonable

**SKILL.md:**
- Clear step-by-step algorithm
- Include examples for each step
- Document error scenarios

## Related Documentation

- **learning-summary plugin**: `../learning-summary/CLAUDE.md`
- **WebFetch tool**: Claude Code documentation
- **Template guide**: See SKILL.md Step 6

## Support

For issues or questions:
- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
- Discussions: https://github.com/JayKim88/claude-ai-engineering/discussions

---

**Development Tips:**

1. **Test with real AI articles**: Use actual Anthropic/OpenAI/etc. announcements
2. **Verify bilingual output**: Ensure Korean sections are properly populated
3. **Check file naming**: Ensure slugs are readable and searchable
4. **Monitor WebFetch**: Some sites block automated fetches
5. **Git safety**: Test auto_commit with test repository first
