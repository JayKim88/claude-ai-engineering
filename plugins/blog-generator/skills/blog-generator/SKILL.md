---
name: blog-generator
description: Transform technical notes into blog posts. Use when user says "blog-generator", "/blog-generator", "블로그 글 작성", "블로그로 변환", "write a blog post", "turn this into a blog", or provides technical content to convert into blog format.
version: 1.0.0
---

# Blog Generator

Transforms technical notes, memos, and documentation into well-structured blog posts with narrative flow, engaging introductions, and reader-friendly explanations.

---

## Trigger Phrases

**English:**
- "write a blog post about this"
- "turn this into a blog"
- "blog-generator"
- "/blog-generator [file path or content]"
- "convert to blog format"

**Korean:**
- "블로그 글 작성해줘"
- "블로그로 변환해줘"
- "이 내용으로 블로그 써줘"
- "기술 블로그로 만들어줘"

---

## Quick Reference

### When to Use

- User provides technical notes/memos and wants a blog post
- User points to an MD file to convert
- User pastes raw technical content
- User wants to publish-ready technical writing

### When NOT to Use

- Article digest/summary (use ai-digest)
- Conversation summary (use learning-summary)
- Code review or analysis (use project-insight)
- Creative/non-technical writing

---

## Execution Algorithm

### Step 1: Parse Input

Extract the content source from user message:

| Input Type | Detection | Action |
|---|---|---|
| **File path** | Contains `.md`, `/path/to/`, or `~` pattern | Read file using `Read` tool |
| **URL** | Contains `https://` or `http://` | Fetch using `WebFetch` tool |
| **Direct text** | Raw text content in message | Use text directly |
| **IDE selection** | Content in `ide_selection` tags | Use selected content |

**Examples:**
- `/blog-generator ~/notes/rag-explained.md` → Read file
- `/blog-generator https://example.com/article` → Fetch URL
- `/blog-generator "RAG는 질문에 답하기 전에..."` → Direct text
- Select text in editor + "블로그로 변환해줘" → IDE selection

**If no content detected:**
```
Ask user: "블로그로 변환할 내용을 제공해주세요. 파일 경로, URL, 또는 텍스트를 입력할 수 있습니다."
```

---

### Step 2: Reader Interview

Ask the user 3 questions using a **single** `AskUserQuestion` call with all 3 questions:

```python
AskUserQuestion(
    questions=[
        {
            "question": "Who is the target audience for this blog post?",
            "header": "Audience",
            "options": [
                {"label": "Beginner (Recommended)", "description": "입문자. 기본 개념부터 친절하게 설명"},
                {"label": "Intermediate", "description": "실무자. 핵심 개념은 알지만 깊이 있는 설명 필요"},
                {"label": "Advanced", "description": "시니어/전문가. 심화 내용과 트레이드오프 중심"}
            ],
            "multiSelect": false
        },
        {
            "question": "What tone and style should the blog post have?",
            "header": "Tone",
            "options": [
                {"label": "Tutorial (Recommended)", "description": "단계별 학습 가이드. 따라하기 쉬운 구성"},
                {"label": "Professional", "description": "기술 문서 스타일. 정확하고 간결한 톤"},
                {"label": "Conversational", "description": "대화체. 친근하고 읽기 편한 스타일"}
            ],
            "multiSelect": false
        },
        {
            "question": "Which language should the blog post be written in?",
            "header": "Language",
            "options": [
                {"label": "Korean (Recommended)", "description": "한국어로 작성. 기술 용어는 영문 병기"},
                {"label": "English", "description": "Written entirely in English"},
                {"label": "Mixed (Ko+En)", "description": "한영 혼용. 헤더는 영어, 본문은 한국어"}
            ],
            "multiSelect": false
        }
    ]
)
```

**If config.yaml exists**, show config defaults in the recommended labels. If user skips or selects defaults, use config values.

---

### Step 3: Read Configuration

Read `~/.claude/skills/blog-generator/config.yaml`:

```yaml
output_dir: "~/Documents/blog/posts"
default_language: "ko"
default_audience: "intermediate"
default_tone: "tutorial"
auto_commit: false
auto_push: false
```

**If config not found**: Use these defaults and continue without asking. The output directory will be created automatically.

**Apply interview answers**: Override config defaults with user's interview selections.

---

### Step 4: Analyze Content & Build Outline

Analyze the raw input to extract:

| Category | What to Extract |
|---|---|
| **Core Topic** | Main subject and its significance |
| **Key Concepts** | Individual concepts/ideas that need explanation |
| **Logical Flow** | Best order for progressive understanding |
| **Code Blocks** | Code snippets to preserve verbatim |
| **Diagrams/Tables** | Visual elements to keep or enhance |
| **Analogies** | Existing analogies to expand; opportunities for new ones |
| **Complexity Level** | How technical the content is |

**Generate an outline** (internal, not shown to user):

```
1. Hook/Introduction angle: [what relatable scenario to start with]
2. Section breakdown:
   - Section A: [concept] → [explanation approach]
   - Section B: [concept] → [explanation approach]
   - ...
3. Code example placement: [where code fits in the narrative]
4. Conclusion angle: [how to wrap up with takeaways]
```

---

### Step 5: Generate Blog Post

Write the blog post following this template structure. **Adapt sections based on content** — not every section is required for every post.

```markdown
---
title: "[SEO-Friendly, Engaging Title]"
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
read_time: "N min read"
audience: "beginner|intermediate|advanced"
---

# [Title - Same as frontmatter or slightly different for H1]

> **TL;DR**: [1-2 sentence summary of the entire post. What will the reader learn?]

## Introduction

[Hook: Start with a relatable scenario, question, or problem statement that the reader can connect with. NOT a dry "In this post, we'll cover..." opener.]

[Bridge: Connect the hook to the main topic. Why should the reader care?]

[Preview: Brief mention of what the post covers, without being a boring list.]

---

## [Main Section 1 - Core Concept]

[Explain the core concept with narrative flow. Use analogies to make abstract ideas concrete.]

[If there's a diagram or visual representation in the original, preserve or enhance it:]

```
[ASCII diagram or description for Mermaid conversion]
```

### [Subsection if needed]

[Deeper dive into a specific aspect]

---

## [Main Section 2 - How It Works / Implementation]

[Step-by-step explanation with context for WHY each step exists, not just WHAT it does.]

### Code Example

[Introduce the code with context — what problem it solves:]

```language
[Original code preserved verbatim]
```

[After code: explain key parts, highlight important lines, mention gotchas.
 Do NOT just repeat what the code says — add insight the reader wouldn't get from reading the code alone.]

---

## [Main Section 3 - Practical Applications / Use Cases]

[Real-world scenarios where this applies. Be specific, not generic.]

| Use Case | Description | Example |
|---|---|---|
| ... | ... | ... |

---

## [Optional: Common Pitfalls / Things to Watch Out For]

[Only include if the source material has warnings, limitations, or gotchas]

---

## Key Takeaways

[3-5 bullet points summarizing the most important things the reader should remember]

- **[Point 1]**: [Brief explanation]
- **[Point 2]**: [Brief explanation]
- **[Point 3]**: [Brief explanation]

## Further Reading

- [Related resource 1]
- [Related resource 2]
- [Next topic to explore]

---

*[Optional: Author note or call-to-action]*
```

**Writing Guidelines by Audience:**

| Audience | Explanation Depth | Jargon | Analogies | Code |
|---|---|---|---|---|
| **Beginner** | Explain everything from basics | Define all terms | Many, relatable | Full context, every line explained |
| **Intermediate** | Skip basics, focus on how/why | Use freely, explain niche terms | Selective | Key parts explained, assume basics |
| **Advanced** | Focus on tradeoffs, edge cases | Expert-level OK | Minimal, technical | Architecture-level, patterns |

**Writing Guidelines by Tone:**

| Tone | Opening | Transitions | Code Explanation | Closing |
|---|---|---|---|---|
| **Tutorial** | "Let's build..." | "Now that we've..., let's..." | Step-by-step walkthrough | "You've now learned..." |
| **Professional** | "[Topic] enables..." | Clear section headers | Concise annotation | "Key considerations..." |
| **Conversational** | "Ever wondered...?" | "So here's the thing..." | "This part is cool because..." | "That's the gist of it!" |

**Code Block Rules:**
- **NEVER modify** the original code. Preserve exactly as-is
- **ADD** explanatory comments only if the original lacks them
- **EXPAND** the explanation around the code (before/after paragraphs)
- **FORMAT** properly with language tag for syntax highlighting

---

### Step 6: Generate Filename

**Format**: `YYYY-MM-DD-{topic-slug}.md`

**Slug rules:**
- Lowercase, kebab-case
- Max 5-6 words
- Descriptive and SEO-friendly
- No language prefix (unlike ai-digest's "ai-" prefix)

**Examples:**
- `2026-02-19-understanding-rag-retrieval-augmented-generation.md`
- `2026-02-19-building-rest-api-with-fastapi.md`
- `2026-02-19-kubernetes-pod-networking-explained.md`

---

### Step 7: Save Document

**Save location**: `{output_dir}/{filename}`

**Create directory if needed:**
```bash
mkdir -p {output_dir}
```

Use `Write` tool to save the markdown file.

**Default output**: `~/Documents/blog/posts/YYYY-MM-DD-{slug}.md`

---

### Step 8: Git Operations (if auto_commit)

Only if `auto_commit: true` in config:

```bash
cd "$output_dir"
git add "$filename"
git commit -m "Add blog post: $title

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

If `auto_push: true`, also run:
```bash
git push
```

---

### Step 9: Confirm to User

Show the user:

```
Blog post generated!

File: {full_path}
Title: {title}
Read time: {N} min
Audience: {audience}
Tone: {tone}
Language: {language}

Tags: {tag1}, {tag2}, {tag3}

Want me to adjust the tone, expand a section, or make any changes?
```

---

## Error Handling

| Scenario | Response |
|---|---|
| No content provided | Ask user to provide file path, URL, or text |
| File not found | `Error: File not found at {path}. Please check the path.` |
| File is empty | `Error: File is empty. Please provide content to convert.` |
| URL fetch fails | `Error: Cannot fetch URL. Please paste the content directly.` |
| Content too short (< 100 chars) | `Warning: Content is very short. The blog post may be brief. Proceed?` |
| Write permission denied | `Error: Cannot write to {path}. Check permissions or provide a different output path.` |
| Config not found | Use defaults silently. Do not interrupt the flow. |
| Git not initialized | `Warning: {output_dir} is not a git repo. Document saved but not committed.` |

---

## Configuration

Located at `~/.claude/skills/blog-generator/config.yaml`:

```yaml
# Output directory for generated blog posts (absolute path)
output_dir: "~/Documents/blog/posts"

# Default language: ko (Korean), en (English), mixed (Korean+English)
default_language: "ko"

# Default audience: beginner, intermediate, advanced
default_audience: "intermediate"

# Default tone: tutorial, professional, conversational
default_tone: "tutorial"

# Auto-commit to git after saving
auto_commit: false

# Auto-push to remote (requires auto_commit: true)
auto_push: false
```

---

## Examples

### Example 1: File Input

```
User: /blog-generator ~/notes/rag-explained.md

Claude: [Reads file, asks 3 interview questions]
        [Generates blog post]

Blog post generated!

File: ~/Documents/blog/posts/2026-02-19-understanding-rag-retrieval-augmented-generation.md
Title: "RAG 완전 정복: LLM에게 오픈북 시험을 치르게 하는 방법"
Read time: 8 min
Audience: beginner
Tone: tutorial
Language: Korean
```

### Example 2: Direct Text

```
User: 블로그로 변환해줘

"Docker는 컨테이너 기반 가상화 기술이다.
VM과 달리 OS를 공유하므로 가볍다.
이미지 → 컨테이너 → 실행의 흐름..."

Claude: [Asks interview questions, generates blog post]

File: ~/Documents/blog/posts/2026-02-19-docker-container-basics-explained.md
```

### Example 3: URL Input

```
User: /blog-generator https://blog.example.com/kubernetes-networking

Claude: [Fetches content, asks interview questions, generates blog post]

File: ~/Documents/blog/posts/2026-02-19-kubernetes-pod-networking-explained.md
```
