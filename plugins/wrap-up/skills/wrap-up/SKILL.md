---
name: wrap-up
description: Document session work history and todos into a per-topic file. Use when user says "wrap up", "wrap-up", "작업 정리", "세션 정리", "마무리", or wants to record session progress.
version: 3.0.0
---

# Wrap Up

Records what was done in the current session and what needs to be done next, saving to a **per-topic** markdown file that accumulates across sessions.

**Defaults** (no config file needed):
- Output directory: `wrap-up/`
- File naming: `wrap-up/{topic-name}.md` (topic = main feature/subject worked on)
- Sections: Done, Decisions (optional), Issues (optional), Next
- Language: auto-detect from conversation

---

## Execution Algorithm

### Step 1: Detect Topic & Match Existing File

1. **Analyze conversation** to identify the primary topic or feature
2. **Scan existing files**: `Glob("wrap-up/*.md")` to list all wrap-up files
3. **Match logic**:

| Scenario | Action |
|----------|--------|
| **Exact match** found (filename = topic) | Ask user to confirm: "기존 `wrap-up/{name}.md`에 이어서 기록할까요?" |
| **Similar match** found (related title/content) | Show candidates and ask user to select |
| **Multiple candidates** | Present list with AskUserQuestion for selection |
| **No match** | Ask user to confirm new file creation with suggested topic name |

**Matching criteria:**
- Filename similarity (e.g., topic `auth` matches `auth.md`)
- Title in file header (e.g., `# Auth Module - Wrap Up`)
- Content overlap (recent Done/Next items relate to current session's work)

**Naming rules:**
- Use kebab-case: `business-avengers`, `wrap-up`, `api-refactor`
- Be specific to the feature, NOT the project directory name

---

### Step 2: Load Context (Prepend only)

If adding to an existing file:

1. **Read the entire file**
2. **Parse the FIRST (most recent) `### Next` section** to identify pending items
3. **Cross-reference** with current session's work to determine which Next items were completed
4. This context informs Step 3 (Analyze Conversation)

---

### Step 3: Analyze Conversation

Review the entire conversation history to extract:

| Section | What to Extract |
|---------|----------------|
| **Done** | Tasks completed, features added, bugs fixed, refactoring done. Use conventional commit prefixes (feat, fix, refactor, docs, chore). If items from previous Next were completed, include them with "(from previous Next)" note |
| **Decisions** | Architecture choices, library selections, approach decisions made during the session |
| **Issues** | Blockers, errors, unresolved problems, workarounds applied |
| **Next** | Pending tasks, follow-up items, explicitly mentioned TODOs. Use checkbox format `- [ ]` |

---

### Step 4: Create or Append

**If NEW file** (user confirmed new topic):
- Create `wrap-up/` directory if needed
- Write new file with topic header + session entry

**If EXISTING file** (user selected existing file):
- Update the FIRST (most recent) session's **Next** checkboxes: completed items `[ ]` → `[x]`
- **Insert new session entry AFTER the header block** (after `> **Scope**:` line), BEFORE existing sessions
- Add `---` separator between the new entry and the previous most-recent session
- This ensures **newest session is always at the top**, oldest at the bottom (reverse chronological order)

**Session date format:**
- **Must run `date '+%Y-%m-%d %H:%M'`** to get the exact current time. Never estimate or guess the time.
- Format: `## Session: 2026-02-23 14:00`
- Time helps identify and trace specific sessions across conversation history

**Context line:**
- Each session entry includes `> **Context**: {brief summary}` right after the session header
- 1-line summary of what the session was about (for quick identification when scanning the file)

**Session ordering:** Reverse chronological (newest first, oldest last).

Template (new file):

```markdown
# {Topic Name} - Wrap Up

> **Project**: `{CWD}`
> **Scope**: `{relative path to primary working directory}` (e.g., `plugins/business-avengers/`)

## Session: 2026-02-23 14:00

> **Context**: OAuth 2.0 소셜 로그인 연동 및 Google/GitHub 프로바이더 구현

### Done
- ...

### Decisions
- ...

### Next
- [ ] ...
```

Template (existing file — insert new session at top):

```markdown
# {Topic Name} - Wrap Up

> **Project**: `{CWD}`
> **Scope**: `...`

## Session: 2026-02-24 10:00        ← NEW (inserted here)

> **Context**: ...

### Done
- ...

### Next
- [ ] ...

---

## Session: 2026-02-23 14:00        ← PREVIOUS (pushed down)

> **Context**: ...

### Done
- ...

### Next
- [x] completed item (from previous Next)
- [ ] remaining item
```

**Section omission rules:**
- Omit **Decisions** if no significant decisions were made
- Omit **Issues** if no problems were encountered
- **Done** and **Next** are always included

---

### Step 5: Confirm to User

Show the user:
- Full path of saved file (new or updated)
- Whether it was a new file or appended to existing
- Number of items in each section
- (Append only) Number of previous Next items completed

---

### Step 6: Blog Log Generation (Optional)

After confirming the wrap-up file, check `config.yaml` for `blog_log.enabled`:

```pseudocode
config = Read("config.yaml")  // from skill directory

if config.blog_log.enabled == false:
    exit  // skip silently

// Prompt user
AskUserQuestion(
  "블로그 로그도 생성할까요?",
  options=[
    { label: "네", description: "오늘 작업 내용을 블로그 logs 컬렉션에 저장합니다" },
    { label: "아니요", description: "wrap-up만 저장하고 종료합니다" }
  ]
)

if answer == "네":
    // Invoke wrap-to-blog skill with current session context
    // Pass: session date, topic name, Done items, Decisions, Next items
    invoke_skill("wrap-to-blog", {
      session_date: current_date,        // YYYY-MM-DD
      topic: current_topic,              // e.g., "planning-interview"
      done: session.done_items,
      decisions: session.decisions,
      next: session.next_items,
      context_summary: session.context,
      blog_dir: config.blog_log.blog_dir,
      collection: config.blog_log.collection
    })
```

**Note**: This step only runs if `blog_log.enabled: true` in config.yaml. If config.yaml is missing or `blog_log` section is absent, skip silently.

---

## Trigger Phrases

**English:**
- "wrap up", "wrap-up", "session summary", "document progress", "record what we did"

**Korean:**
- "작업 정리", "세션 정리", "마무리", "진행 상황 기록", "오늘 한 일 정리"

---

## Quick Reference

### When to Use

**Use this skill when**:
- End of a work session
- Switching to a different project or topic
- Before closing a chat session
- After completing a significant milestone

**Skip when**:
- Very short Q&A (nothing substantial to record)
- Pure research/exploration with no actionable output

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Output directory doesn't exist | Create it with `mkdir -p` |
| Write permission denied | `Error: Cannot write to {path}. Check permissions.` |
| Empty conversation | `Warning: Not enough content to summarize. Continue working first.` |
| Existing file is malformed | Append new session entry at the end regardless |
