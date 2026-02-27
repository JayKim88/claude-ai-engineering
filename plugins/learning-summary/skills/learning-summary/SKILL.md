---
name: learning-summary
description: Summarize and document key learnings from the conversation. Use when user says "summarize", "document", "what did I learn", or wants to capture insights.
version: 2.0.0
---

# Learning Summary

Extracts and documents key insights, concepts, and learnings from the current conversation.
Output is blog-ready with YAML frontmatter for Astro Content Collections.

---

## Execution Algorithm

### Step 1: Read Configuration

Read `~/.claude/skills/learning-summary/config.yaml`:

```yaml
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"
output_dir: "blog/src/content/learnings"
auto_commit: false
auto_push: false
```

**If config not found**: Use defaults (current directory, no auto-commit)

---

### Step 2: Analyze Conversation

Review the entire conversation history to identify:

| Category | What to Extract |
|----------|----------------|
| **Key Concepts** | Main topics, key terminology, fundamental concepts |
| **New Learnings** | New knowledge gained, before/after understanding |
| **Practical Examples** | Code snippets, commands, real-world examples |
| **Common Misconceptions** | Misconceptions clarified during conversation |
| **References** | Files, URLs, documentation referenced |
| **Next Steps** | Follow-up actions, topics to explore |

Also extract metadata for frontmatter:

| Field | How to Derive |
|-------|---------------|
| **title** | Main topic as concise title |
| **description** | 1-2 sentence summary of key insight |
| **tags** | 3-7 lowercase kebab-case keywords from conversation topics |
| **source** | Primary URL referenced (if any) |
| **lang** | Always `en` (output is always in English) |

---

### Step 3: Generate Filename

Create descriptive filename based on main topic:

**IMPORTANT**: Run `date '+%Y-%m-%d'` to get the exact current date. Never estimate.

**Format**: `YYYY-MM-DD-brief-topic-description.md`

**Examples**:
- `2026-01-17-claude-code-marketplace-guide.md`
- `2026-01-17-python-async-programming.md`
- `2026-01-17-docker-compose-networking.md`

---

### Step 4: Structure Document

Generate a blog-ready markdown file with YAML frontmatter:

```markdown
---
title: "[Main Topic Title]"
date: YYYY-MM-DD
description: "[1-2 sentence summary of key insight]"
category: learnings
tags: ["tag1", "tag2", "tag3"]
source: "https://..."
lang: en
draft: false
---

## Key Concepts

[Key concepts with clear definitions]

## New Learnings

[New learnings with before/after]

## Practical Examples

[Code, commands, examples]

## Common Misconceptions

[Clarified misconceptions]

## References

[Files, URLs, resources]

## Next Steps

[Follow-up actions]
```

**Important formatting rules**:
- Do NOT include `# Title` heading in body (the blog layout renders title from frontmatter)
- Body starts with `## Key Concepts` or first applicable section
- `category` is always `learnings`
- `tags` are lowercase, kebab-case, as a YAML array
- `source` is optional (omit the field entirely if no primary URL)
- `description` should be under 160 characters for SEO
- Empty sections should be omitted entirely

---

### Step 5: Save Document

**Save location**: `{learning_repo}/{output_dir}/{filename}`

**Example**: `/Users/jaykim/Documents/Projects/ai-learning/blog/src/content/learnings/2026-01-17-topic.md`

Use Write tool to create the markdown file.

---

### Step 6: Git Operations (if auto_commit)

Only if `auto_commit: true` in config:

```bash
cd "$learning_repo"
git add "blog/src/content/learnings/$filename"
git commit -m "Add learning: $topic

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

If `auto_push: true`, also run:
```bash
git push
```

When pushed to main, GitHub Actions will automatically build and deploy the blog.

---

### Step 7: Confirm to User

Show the user:
- Full path of saved file
- Brief summary of documented content
- Git commit status (if auto_commit enabled)
- Blog URL where post will appear after deploy
- Offer to open file or make adjustments

---

## Trigger Phrases

**English:**
- "summarize what I learned"
- "document my learnings"
- "create learning summary"
- "capture insights from this conversation"

**Korean:**
- "지금까지 대화 정리해줘"
- "배운 내용 문서화"
- "정리해서 문서로"

---

## Quick Reference

### When to Use

**Use this skill when**:
- End of significant learning conversation
- After understanding a complex topic
- When you want to preserve key insights
- Before switching to a different subject
- After solving a challenging problem

**Skip when**:
- Very short Q&A (single question/answer)
- Simple command lookup
- Already well-documented elsewhere
- Trivial clarifications

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Config file not found | Use defaults: `./blog/src/content/learnings/`, no auto-commit |
| Learning repo doesn't exist | `Error: Directory not found at {path}. Create with: mkdir -p {path}` |
| Git not initialized | `Warning: Not a git repository. Skipping auto-commit.` |
| Write permission denied | `Error: Cannot write to {path}. Check permissions: ls -la {dir}` |
| Empty conversation | `Warning: Not enough content to summarize. Continue the conversation first.` |
| Invalid YAML config | `Warning: Invalid config.yaml. Using defaults.` |
| Git commit fails | `Warning: Git commit failed. Document saved but not committed.` |

---

## Configuration

Edit `~/.claude/skills/learning-summary/config.yaml`:

```yaml
# Dedicated AI learning repository (absolute path)
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"

# Output directory (relative to learning_repo)
# Points to blog content directory for direct blog publishing
output_dir: "blog/src/content/learnings"

# Filename pattern (will be auto-generated based on date and topic)
filename_pattern: "YYYY-MM-DD-topic.md"

# Auto-commit to git
auto_commit: false

# Auto-push to remote (requires auto_commit: true)
auto_push: false

# Default sections to include
sections:
  - key_concepts
  - new_learnings
  - practical_examples
  - misconceptions
  - references
  - next_steps

# Language preference (auto-detect or set to 'ko'/'en')
language: en
```

---

## Additional Resources

See `references/` directory:
- `template.md` - Document template with examples
- `best-practices.md` - Tips for writing effective learning notes
- `configuration.md` - Detailed configuration guide
