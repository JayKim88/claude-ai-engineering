---
description: Transform technical notes into well-structured blog posts with narrative flow
allowed-tools: Read, Write, Edit, Bash, WebFetch, AskUserQuestion
---

# /blog-generator Command

Transforms technical notes, memos, and documentation into publish-ready blog posts with engaging introductions, narrative flow, and reader-friendly explanations.

## Usage

```bash
# Convert a markdown file to blog post
/blog-generator ~/notes/rag-explained.md

# Convert pasted content
/blog-generator "RAG는 질문에 답하기 전에 관련 문서를 먼저 찾아서..."

# Convert from URL
/blog-generator https://blog.example.com/technical-article

# Convert selected text in IDE
# Select text in editor, then:
/blog-generator
```

## What It Does

1. **Parses input** (file path, URL, direct text, or IDE selection)
2. **Interviews** the user about audience, tone, and language
3. **Analyzes** content structure, key concepts, and logical flow
4. **Generates** a blog post with hook, narrative sections, and takeaways
5. **Saves** to configured output directory
6. **Optionally commits** to git (if configured)

## Execution

When this command is invoked, automatically trigger the `blog-generator` skill located at `skills/blog-generator/SKILL.md` to handle the request.

The skill will:
1. Parse the input to determine content source
2. Ask 3 interview questions (audience, tone, language)
3. Analyze content and build an outline
4. Write the blog post with proper narrative flow
5. Save to the configured output directory
6. Optionally commit to git
