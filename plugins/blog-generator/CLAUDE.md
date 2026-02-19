# Blog Generator Plugin - Development Guide

Development and maintenance guide for the blog-generator plugin.

## Directory Structure

```
blog-generator/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata and version
├── commands/
│   └── blog-generator/
│       └── blog-generator.md # /blog-generator command definition
├── skills/
│   └── blog-generator/
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
ls -l ~/.claude/skills/blog-generator
ls -l ~/.claude/commands/blog-generator
```

### Making Changes

1. Edit files in monorepo: `plugins/blog-generator/`
2. Changes reflect immediately via symlink
3. Test in Claude Code with `/blog-generator` or trigger phrases
4. Commit when satisfied

## Architecture

### Direct Skill Pattern (with Interview)

This plugin uses the **Direct Skill + Interview** pattern:

```
User Input (file/URL/text/IDE selection)
    ↓
Parse input type
    ↓
AskUserQuestion (audience, tone, language)
    ↓
Read config.yaml (defaults for unset options)
    ↓
Analyze content → Build outline
    ↓
Generate blog post using outline + settings
    ↓
Save to output directory
    ↓
Git commit/push (if enabled)
    ↓
Confirm to user
```

**Why direct skill (not multi-agent)?**
- Sequential task — analysis must complete before writing
- No benefit from parallelization
- Single content source, single output
- Interview + generation is a natural single-flow

### Key Design Decisions

**1. Interview before writing**
- Audience level drastically changes explanation depth
- Tone changes sentence structure and transitions
- Language affects the entire document
- These can't be guessed reliably from input alone

**2. Code preservation**
- Original code blocks are NEVER modified
- Only explanatory text around code is expanded
- This maintains technical accuracy

**3. Own config (not shared)**
- Unlike ai-digest (shares learning-summary config), blog-generator has its own config
- Blog output directory is typically separate from learning notes
- Different defaults make sense (blogs target readers, not personal reference)

## Execution Flow Details

### Step 1: Parse Input

**Goal**: Determine content source and extract raw text

**Detection priority:**
1. File path (contains `.md`, starts with `/`, `~`, or `./`)
2. URL (contains `https://` or `http://`)
3. IDE selection (present in context)
4. Direct text (everything else)

### Step 2: Interview

**Goal**: Understand target reader profile

Single `AskUserQuestion` call with 3 questions. This is more efficient than 3 separate calls and creates a better UX.

**Config override**: If config.yaml has defaults set, those become the "Recommended" option labels.

### Step 3-4: Analysis & Writing

**Goal**: Transform raw notes into narrative blog post

The analysis phase is internal (not shown to user). It produces an outline that guides the writing phase.

**Critical rules for writing:**
- Hook must be a relatable scenario, not "In this post..."
- Each section needs a transition from the previous one
- Code blocks are preserved verbatim; only surrounding text changes
- Tables and diagrams are kept or enhanced, never removed

### Step 5-6: Save & Confirm

**Filename**: `YYYY-MM-DD-{topic-slug}.md`
- No prefix (unlike ai-digest's "ai-" prefix)
- Slug is SEO-friendly, 5-6 words max

## Configuration

### Config Location

`~/.claude/skills/blog-generator/config.yaml`

Note: This reads from the **installed** location (symlinked), not the source.

### Config Fields

```yaml
output_dir: "~/Documents/blog/posts"  # Where to save posts
default_language: "ko"                 # ko, en, mixed
default_audience: "intermediate"       # beginner, intermediate, advanced
default_tone: "tutorial"               # tutorial, professional, conversational
auto_commit: false                     # Git commit after save
auto_push: false                       # Git push (requires auto_commit)
```

### Config Absent Behavior

If config.yaml doesn't exist, use hardcoded defaults silently. Do NOT interrupt the user to create config — just proceed.

## Testing

### Manual Testing Checklist

**Input parsing:**
- [ ] `/blog-generator ~/path/to/file.md` — reads file
- [ ] `/blog-generator https://example.com/article` — fetches URL
- [ ] `/blog-generator "direct text content"` — uses text
- [ ] IDE selection + trigger phrase — uses selection
- [ ] No content provided — asks user for input

**Interview:**
- [ ] All 3 questions appear in single AskUserQuestion call
- [ ] Selecting options works correctly
- [ ] Config defaults apply when user skips

**Blog generation:**
- [ ] Hook is engaging (not "In this post...")
- [ ] Sections have transitions
- [ ] Code blocks preserved verbatim
- [ ] Audience level affects explanation depth
- [ ] Tone affects writing style
- [ ] Language selection is respected

**Output:**
- [ ] File saved to correct directory
- [ ] Filename follows YYYY-MM-DD-slug pattern
- [ ] Frontmatter includes title, date, tags, read_time, audience
- [ ] TL;DR is concise and accurate
- [ ] Key takeaways section present

**Git integration:**
- [ ] Commits if auto_commit: true
- [ ] Skips commit if auto_commit: false
- [ ] Handles non-git directories gracefully

### Test Inputs

```bash
# Simple notes
/blog-generator "REST API는 HTTP 메서드를 사용하여..."

# Complex notes with code
/blog-generator ~/notes/rag-explained.md

# URL
/blog-generator https://blog.example.com/article

# Edge: very short input
/blog-generator "Docker is a container platform"

# Edge: very long input
/blog-generator ~/notes/comprehensive-kubernetes-guide.md
```

## Versioning

Update `.claude-plugin/plugin.json` version before committing:

- **MAJOR** (2.0.0): Breaking changes to output format or config
- **MINOR** (1.1.0): New features (series support, new tone options)
- **PATCH** (1.0.1): Bug fixes, documentation updates

## Common Issues

### Issue: Generated post is too shallow

**Cause**: Input notes lack detail
**Solution**: The quality of output directly correlates with input richness. Encourage detailed notes.

### Issue: Code blocks modified

**Cause**: Bug in generation instructions
**Solution**: SKILL.md explicitly forbids code modification. If this happens, it's an LLM adherence issue — reinforce the rule.

### Issue: Interview skipped

**Cause**: User provided content inline without triggering the skill
**Solution**: Trigger phrases in SKILL.md description should catch most cases. If not, skill falls back to config defaults.

## Related Documentation

- **ai-digest plugin**: `../ai-digest/CLAUDE.md` — similar single-flow architecture
- **SKILL.md**: Full execution algorithm with template
- **README.md**: User-facing documentation

## Support

- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
- Discussions: https://github.com/JayKim88/claude-ai-engineering/discussions
