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

### Step 2: Resolve Content

Determine the content source using the following priority:

**Priority 1 — Direct content provided:**
If the user pasted article text (beyond just a URL), use it directly. Skip WebFetch entirely. This is the most reliable path.

**Priority 2 — Fetchable URL only:**
If only a URL is provided (no pasted content), attempt WebFetch:

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

**Priority 3 — Auth-gated URL with no content:**
If the URL is from a known auth-gated domain AND no direct content is provided, do NOT attempt WebFetch. Instead, ask the user to paste the content.

Known auth-gated domains (non-exhaustive):
- `linkedin.com` — requires login
- `x.com`, `twitter.com` — requires login
- `medium.com` — may be paywalled
- `substack.com` — may be paywalled
- `notion.so` — requires access
- `docs.google.com` — requires access

**When both URL + direct content are provided:**
Use the direct content for analysis. Retain the URL only as a source reference in the output document.

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

**First, classify the content type** to determine which template variant to use:

| Content Type | Characteristics | Template Variant |
|-------------|-----------------|------------------|
| **Technical** | Code changes, API updates, library releases, tutorials | Full template (with code examples, Before/After) |
| **Strategic/Opinion** | Industry analysis, trend pieces, strategy frameworks | Strategy template (with frameworks, comparison tables) |
| **News/Announcement** | Product launches, funding, partnerships | News template (concise, fact-focused) |

#### Template: Core (always included)

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

## 주의사항 / 제한사항 (Limitations & Gotchas)

- [Warning 1]
- [Warning 2]
- [Tip 1]

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

#### Template: Technical Extensions (add when content type is Technical)

Include these sections when the article contains code, API changes, or migration guides:

```markdown
## 코드 예제 (Code Examples)

### Example 1: [What it demonstrates]
```language
[Runnable code]
```

**설명**: [What this code does]

## Before/After 비교

### Before (기존 방식)
```language
[Old way]
```

### After (새로운 방식)
```language
[New way]
```

**차이점**: [Key differences]
```

#### Template: Strategy Extensions (add when content type is Strategic/Opinion)

Include these sections when the article discusses frameworks, trends, or strategic analysis:

```markdown
## 핵심 프레임워크 (Key Framework)

[Visual or structured representation of the article's main framework]
[Use tables, diagrams (text-based), or hierarchical lists]

## 사례 비교 (Case Comparisons)

| 항목 | [Case A] | [Case B] |
|------|----------|----------|
| ... | ... | ... |
```

**Section inclusion rules:**
- Always: 요약, 주요 변경사항, 실무 적용, 참고 링크
- Technical content: + 코드 예제, Before/After
- Strategic content: + 핵심 프레임워크, 사례 비교
- Optional: 주의사항 (if important warnings exist), Next Steps
- Do not include empty sections. If a section has no meaningful content, omit it.

---

### Step 7: Save Document

**Save location**: `{learning_repo}/digests/{filename}`

**Example**: `/Users/jaykim/Documents/Projects/ai-learning/digests/2026-01-25-ai-claude-sonnet-4-5-release.md`

**Deduplication check**: Before saving, use Glob to check if a file with the same date and similar topic slug already exists in the digests directory. If a match is found, ask the user whether to overwrite, append, or create with a suffix (e.g., `-2`).

**Save**: Use the Write tool directly. Do NOT run `mkdir -p` — the `digests/` directory should already exist in a configured learning repo. If Write fails due to a missing directory, then create it.

---

### Step 8: Git Operations (if auto_commit)

Only if `auto_commit: true` in config:

```bash
cd "$learning_repo"
git add "digests/$filename"
git commit -m "Add AI digest: $topic

Co-Authored-By: Claude <model> <noreply@anthropic.com>"
```

**Note**: Replace `<model>` with the actual model name being used (e.g., "Opus 4.6", "Sonnet 4.5"). Do not hardcode a specific model name.

If `auto_push: true`, also run:
```bash
git push
```

---

### Step 9: Confirm to User

Show the user:
- **Saved**: Full path of saved file
- **Captured**: Brief summary of what was captured (bulleted list of key topics)
- **Source**: Original URL (if applicable)
- **Git**: Commit status (only if auto_commit enabled)

Do not use emojis in the confirmation output. Keep it concise and scannable.

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
| Auth-gated URL, no content | Ask user to paste the article content. Do NOT attempt WebFetch. |
| Auth-gated URL + content provided | Use direct content. Retain URL as source reference only. |
| WebFetch fails | `Error: Failed to fetch content. You can paste the content directly.` |
| Config not found | Ask user for ai-learning repository path |
| Write fails (missing directory) | Create directory with `mkdir -p`, then retry Write |
| Write permission denied | `Error: Cannot write to {path}. Check permissions.` |
| Git not initialized | `Warning: Not a git repository. Document saved but not committed.` |
| Empty content | `Error: No content to analyze. Please provide URL or text.` |
| Duplicate file exists | Ask user: overwrite, append, or save with `-2` suffix |

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

### Example 1: URL Digest (fetchable)

```
User: /ai-digest https://anthropic.com/news/claude-sonnet-4-5

Claude: [Fetches content via WebFetch, classifies as Technical, generates document]

Saved: .../digests/2026-01-25-ai-claude-sonnet-4-5-release.md

Captured:
- New Claude Sonnet 4.5 features and performance benchmarks
- Migration guide from previous versions
- Code examples showing before/after API changes
```

### Example 2: Auth-gated URL + pasted content

```
User: /ai-digest https://linkedin.com/posts/someone/...
[pasted article text]

Claude: [Detects LinkedIn URL + direct content → uses direct content, skips WebFetch]
[Classifies as Strategic/Opinion, uses strategy template variant]

Saved: .../digests/2026-01-25-ai-agent-economy-strategy.md
Source: https://linkedin.com/posts/someone/...

Captured:
- Agent economy framework and 3 survival conditions
- Case comparisons (Supabase vs competitors, Resend vs SendGrid)
```

### Example 3: Focused Analysis

```
User: /ai-digest "Focus on breaking changes only" https://openai.com/blog/gpt-5

Claude: [Fetches content, applies user focus filter to analysis]

Saved with focus on:
- API breaking changes and deprecated parameters
- Migration steps with before/after code examples
```

### Example 4: Auth-gated URL only (no content)

```
User: /ai-digest https://linkedin.com/posts/someone/...

Claude: LinkedIn requires authentication, so I can't fetch this content directly.
Please paste the article text and I'll digest it.
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
