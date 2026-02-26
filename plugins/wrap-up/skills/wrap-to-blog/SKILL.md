---
name: wrap-to-blog
description: Converts wrap-up session data into a blog log post for the ai-learning blog's logs collection. Invoked automatically from wrap-up Step 6, or triggered manually.
version: 1.0.0
---

# Wrap-to-Blog

Converts today's wrap-up session(s) into a single dated blog log post under the `logs` collection.
Multiple topics worked on the same day are merged into one post with per-topic sections.

---

## Algorithm

### Step 1: Resolve Paths

```pseudocode
config = Read("~/.claude/skills/wrap-up/config.yaml")

blog_dir = expandHome(config.blog_log.blog_dir)
// e.g., "/Users/jaykim/Documents/Projects/ai-learning/blog"

collection = config.blog_log.collection  // "logs"
logs_dir = f"{blog_dir}/src/content/{collection}"
// e.g., ".../blog/src/content/logs"
```

### Step 2: Determine Target Date & Output Path

```pseudocode
// If invoked from wrap-up Step 6: session_date is passed as context
// If invoked standalone: use today's date
today = session_date OR Bash("date '+%Y-%m-%d'").strip()

output_file = f"{logs_dir}/{today}-session-log.md"
```

### Step 3: Collect All Sessions for Today

Scan all wrap-up files for sessions matching today's date:

```pseudocode
wrap_up_files = Glob("{cwd}/wrap-up/*.md")

today_sessions = []
for file in wrap_up_files:
    content = Read(file)
    sessions = parse_sessions(content)  // Extract all "## Session: YYYY-MM-DD HH:MM" blocks
    for session in sessions:
        if session.date == today:
            today_sessions.append({
                topic: extract_topic_from_filename(file),  // e.g., "planning-interview" from planning-interview.md
                context: session.context,
                done: session.done_items,
                decisions: session.decisions,  // may be empty
                next: session.next_items
            })
```

**Note**: If invoked from wrap-up Step 6, the current session's data is already passed in — add it to `today_sessions` if not already present in the file (file may not be written yet at invocation time).

### Step 4: Handle Existing File

```pseudocode
if fileExists(output_file):
    AskUserQuestion(
      f"{today} 날짜의 로그 파일이 이미 존재합니다. 어떻게 할까요?",
      options=[
        { label: "업데이트", description: "wrap-up 파일들을 재스캔해서 최신 세션을 포함해 재생성합니다 (추천)" },
        { label: "덮어쓰기", description: "업데이트와 동일하게 동작합니다" },
        { label: "건너뜀", description: "기존 파일을 유지하고 종료합니다" }
      ]
    )
    if answer == "건너뜀":
        exit
    // "업데이트" 또는 "덮어쓰기": 이후 Step 3을 이미 수행했으므로 그대로 진행
    // (Step 3에서 전체 재스캔이 이루어지므로 자동으로 최신 상태가 됨)
```

### Step 5: Build Post Content

```pseudocode
// Frontmatter
all_tags = unique([session.topic for session in today_sessions])
description = ", ".join([f"{s.topic}: {s.context}" for s in today_sessions])
if len(description) > 120: description = description[:120] + "..."

frontmatter = f"""---
title: "{today} 작업 로그"
date: {today}
description: "{description}"
tags: {json(all_tags)}
---"""

// Topic index (only if 2+ topics)
if len(today_sessions) > 1:
    topic_links = "\n".join([f"- [{s.topic}](#{s.topic})" for s in today_sessions])
    toc = f"\n## 오늘 작업한 주제\n{topic_links}\n\n---\n"
else:
    toc = ""

// Per-topic sections
sections = []
for session in today_sessions:
    section = f"## {session.topic}\n\n> {session.context}\n"

    section += "\n### 한 일\n"
    section += "\n".join([f"- {item}" for item in session.done])

    if session.decisions:
        section += "\n\n### 주요 결정\n"
        section += "\n".join([f"- {item}" for item in session.decisions])

    if session.next:
        section += "\n\n### 다음\n"
        section += "\n".join([f"- [ ] {item}" for item in session.next])

    sections.append(section)

body = "\n\n---\n\n".join(sections)
full_content = frontmatter + "\n" + toc + body
```

### Step 6: Write File

```pseudocode
// Create logs directory if it doesn't exist
Bash(f"mkdir -p {logs_dir}")

Write(output_file, full_content)
```

### Step 7: Confirm to User

```
✅ 블로그 로그 생성 완료

📄 {output_file}
📅 날짜: {today}
🏷️  주제: {", ".join(all_tags)} ({len(today_sessions)}개 세션)

다음 단계:
  cd {blog_dir} && npm run dev   # 로컬에서 확인
  git add . && git commit && git push   # 배포
```

---

## Standalone Trigger

This skill can also be invoked directly (without wrap-up):

```
/wrap-to-blog
```

In this case, it scans all wrap-up files for today's sessions and generates the post.
If no sessions are found for today, it reports: "오늘 날짜의 wrap-up 세션이 없습니다."

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No wrap-up files found | "wrap-up/ 디렉토리에 파일이 없습니다." |
| No sessions for today | "오늘 ({today}) 날짜의 세션이 없습니다." |
| blog_dir not found | "블로그 디렉토리를 찾을 수 없습니다: {blog_dir}. config.yaml의 blog_log.blog_dir를 확인해주세요." |
| Write permission denied | "파일 쓰기 권한이 없습니다: {output_file}" |
| config.yaml missing | Use fallback: blog_dir = "~/Documents/Projects/ai-learning/blog", collection = "logs" |
