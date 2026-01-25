---
name: ai-digest
description: Digest AI/tech articles into structured learning documents. Use when user says "digest this article", "/ai-digest", "analyze this AI news", or provides URL/content to summarize.
version: 1.0.0
---

# AI Digest

Analyzes AI/tech articles, blog posts, or content and creates structured learning documents optimized for quick reference and practical application.

---

## Execution Algorithm

### Step 1: Parse Input

Extract from user message:

| Element | What to Extract |
|---------|----------------|
| **URL** | Any URL (https://...) |
| **Focus** | User's specific interest (e.g., "focus on API changes") |
| **Direct Content** | Text content if no URL provided |

**Examples:**
- `/ai-digest https://anthropic.com/news/...` → URL extracted
- `/ai-digest "Focus on breaking changes" https://...` → URL + Focus
- `/ai-digest "Analyze: [pasted content]"` → Direct content

---

### Step 2: Fetch Content

**If URL provided:**
```python
WebFetch(
    url=extracted_url,
    prompt="""
    Extract the main content of this article.

    Focus on:
    - Main topic and key points
    - Technical details and specifications
    - Code examples
    - Changes or new features
    - Practical applications

    Ignore navigation, ads, and footer content.
    """
)
```

**If direct content:**
Use the provided text directly.

---

### Step 3: Analyze Content

Analyze the fetched content to identify:

| Category | What to Extract |
|----------|----------------|
| **Topic & Context** | What is this about? Why does it matter? |
| **Key Changes/Concepts** | New features, updates, or core concepts |
| **Practical Applications** | How to use this in real projects |
| **Code Examples** | Runnable code snippets |
| **Migration/Upgrade Notes** | Breaking changes, migration steps |
| **Limitations** | Known issues, constraints, gotchas |

**Consider user's focus** if provided (e.g., "API changes only").

---

### Step 4: Read Configuration

Read `~/.claude/skills/learning-summary/config.yaml`:

```yaml
learning_repo: "/Users/username/Documents/Projects/ai-learning"
auto_commit: false
auto_push: false
```

**Why reuse learning-summary config?**
- Keeps all learning documents in one repository
- Shares git settings (auto_commit, auto_push) for consistency
- No duplicate configuration needed
- Users only configure once

**Output directory**: Always use `"digests"` subfolder (not "learnings") to separate article digests from conversation summaries.

**If config not found**: Ask user for learning repository path. You can create the config file or use the provided path for this session only.

---

### Step 5: Generate Filename

Create descriptive filename:

**Format**: `YYYY-MM-DD-ai-[topic-slug].md`

**Examples**:
- `2026-01-25-ai-claude-sonnet-4-5-release.md`
- `2026-01-25-ai-openai-gpt5-features.md`
- `2026-01-25-ai-langchain-updates.md`

**Topic slug rules:**
- Lowercase, kebab-case
- Max 4-5 words
- Descriptive and searchable

---

### Step 6: Generate Document

Use AI-optimized template:

```markdown
# [Article Title or Main Topic]

> **Source**: [Original URL or "Direct Input"]
> **Date**: YYYY-MM-DD
> **Tags**: #ai #[topic] #[subtopic]

## 요약 (Summary)

[1-2 paragraph summary in Korean]
[What this is about and why it matters]

## 주요 변경사항 / 새로운 개념 (Key Changes/Concepts)

### [Change/Concept 1]
- **What**: [Description]
- **Why**: [Reasoning or benefit]
- **Impact**: [Who/what is affected]

### [Change/Concept 2]
...

## 실무 적용 방법 (Practical Applications)

### Use Case 1: [Scenario]
[How to apply this in real projects]

### Use Case 2: [Scenario]
...

## 코드 예제 (Code Examples)

### Example 1: [What it demonstrates]
```language
[Runnable code]
```

**설명 (Explanation)**:
[What this code does]

## Before/After 비교 (If applicable)

### Before (기존 방식)
```language
[Old way]
```

### After (새로운 방식)
```language
[New way]
```

**차이점**: [Key differences]

## 주의사항 / 제한사항 (Limitations & Gotchas)

- ⚠️ [Warning 1]
- ⚠️ [Warning 2]
- 💡 [Tip 1]

## 참고 링크 (References)

- [Original article URL]
- [Related documentation]
- [Related tools/libraries]

## Next Steps

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Topic to explore further]

---

**메모 (Notes)**:
[Personal notes or context]
```

**Sections to include:**
- Always: 요약, 주요 변경사항, 실무 적용, 참고 링크
- If available: 코드 예제, Before/After, Next Steps
- Optional: 주의사항 (if important warnings exist)

---

### Step 7: Save Document

**Save location**: `{learning_repo}/digests/{filename}`

**Example**: `/Users/jaykim/Documents/Projects/ai-learning/digests/2026-01-25-ai-claude-sonnet-4-5-release.md`

Use Write tool to create the markdown file.

**Create directory if needed**:
```bash
mkdir -p {learning_repo}/digests
```

---

### Step 8: Git Operations (if auto_commit)

Only if `auto_commit: true` in config:

```bash
cd "$learning_repo"
git add "digests/$filename"
git commit -m "Add AI digest: $topic

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

If `auto_push: true`, also run:
```bash
git push
```

---

### Step 9: Confirm to User

Show the user:
- ✅ Full path of saved file
- 📝 Brief summary of what was captured
- 🔗 Original URL (if applicable)
- 🔧 Git commit status (if auto_commit enabled)
- 💡 Suggest next actions (e.g., "Want to add related articles?")

---

## Trigger Phrases

**English:**
- "digest this article"
- "analyze this AI news"
- "summarize this tech blog"
- "/ai-digest [URL or content]"

**Korean:**
- "이 글 정리해줘"
- "AI 뉴스 요약"
- "기술 블로그 분석"

---

## Quick Reference

### When to Use

✅ **Use this skill when**:
- User provides URL to AI/tech article
- User pastes content to analyze
- Need to capture rapidly changing AI updates
- Want structured notes for future reference

❌ **Skip when**:
- General conversation summary (use learning-summary)
- Code review (use other tools)
- Already documented elsewhere

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Invalid URL | `Error: Cannot fetch URL. Please check the link and try again.` |
| WebFetch fails | `Error: Failed to fetch content. You can paste the content directly.` |
| Config not found | Ask user for ai-learning repository path |
| Write permission denied | `Error: Cannot write to {path}. Check permissions.` |
| Git not initialized | `Warning: Not a git repository. Document saved but not committed.` |
| Empty content | `Error: No content to analyze. Please provide URL or text.` |

---

## Configuration

Reuses `~/.claude/skills/learning-summary/config.yaml`:

```yaml
# Dedicated AI learning repository (absolute path)
learning_repo: "/Users/username/Documents/Projects/ai-learning"

# Auto-commit to git
auto_commit: false

# Auto-push to remote (requires auto_commit: true)
auto_push: false
```

**Output directory**: Always uses `digests/` subfolder (hardcoded).

**No separate config needed** - shares learning_repo and git settings with learning-summary for consistency.

---

## Examples

### Example 1: URL Digest

```
User: /ai-digest https://anthropic.com/news/claude-sonnet-4-5

Claude: I'll digest this article about Claude Sonnet 4.5 release.

[Fetches content, analyzes, generates document]

✅ Saved to: /Users/jaykim/Documents/Projects/ai-learning/digests/2026-01-25-ai-claude-sonnet-4-5-release.md

📝 Captured:
- New Claude Sonnet 4.5 features
- Performance improvements (2x faster, 3x cheaper)
- New capabilities (extended context, vision)
- Migration guide from previous versions
- Practical code examples

Want me to analyze related articles or commit this to git?
```

### Example 2: Focused Analysis

```
User: /ai-digest "Focus on breaking changes only" https://openai.com/blog/gpt-5

Claude: I'll focus on breaking changes from the GPT-5 announcement.

[Analyzes with focus on breaking changes]

✅ Document saved with emphasis on:
- API breaking changes
- Deprecated parameters
- Migration steps
- Code examples showing before/after
```

### Example 3: Direct Content

```
User: /ai-digest "Analyze this: [pastes article text]"

Claude: I'll digest this content about [topic].

[Analyzes pasted content, generates document]

✅ Saved to: .../digests/2026-01-25-ai-[detected-topic].md
```

---

## Related Skills

- `learning-summary`: For conversation summaries
- `project-insight`: For codebase analysis

---

## Tips

1. **Batch processing**: Digest multiple articles in one session
2. **Tag consistently**: Use consistent tags for searchability
3. **Update existing**: If topic already documented, offer to update
4. **Link related**: Suggest related articles from ai-learning repo
