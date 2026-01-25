---
description: Digest AI/tech articles from URLs or text into structured learning documents
allowed-tools: Read, Write, Bash, WebFetch, AskUserQuestion
---

# /ai-digest Command

Analyzes AI/tech articles or content and creates structured learning documents in your ai-learning repository.

## Usage

```bash
# Digest article from URL
/ai-digest https://anthropic.com/news/claude-sonnet-4-5

# With specific focus
/ai-digest "Focus on API changes" https://docs.anthropic.com/...

# Digest pasted content
/ai-digest "Analyze this content: [paste your text here]"
```

## What It Does

1. **Fetches content** (from URL or direct text)
2. **Analyzes** AI/tech concepts, changes, and practical applications
3. **Generates** structured learning document
4. **Saves** to your ai-learning repository
5. **Optionally commits** to git (if configured)

## Execution

When this command is invoked, automatically trigger the `ai-digest` skill located at `skills/ai-digest/SKILL.md` to handle the request.

The skill will:
1. Parse the input (URL, focus, or direct content)
2. Fetch content if URL provided
3. Analyze and structure the content
4. Save to your ai-learning repository's `digests/` folder
5. Optionally commit to git (if configured)
