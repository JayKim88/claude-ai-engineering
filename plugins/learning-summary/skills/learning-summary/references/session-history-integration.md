# Session History Integration

Automatically analyze Claude Code session history to generate learning notes

---

## Overview

The learning-summary skill can analyze not only the current conversation but also past session history to generate learning notes.

**Use Cases**:
- Review yesterday/last week's conversations
- Consolidate project-specific learning
- Discover recurring themes
- Document long-term learning journey

---

## Session File Location

```
~/.claude/projects/<encoded-cwd>/*.jsonl
```

**Path Encoding**: `/Users/foo/project` → `-Users-foo-project`

---

## Integration Methods

### Method 1: Analyze Current Session (Default)

```
"지금까지 대화 정리해줘"
```

현재 진행 중인 대화만 분석합니다.

---

### Method 2: Include Recent Sessions

**English:**
```
"summarize the past 3 days"
"review this week's learnings"
```

**Korean:**
```
"최근 3일간 대화 정리해줘"
"이번 주 학습 내용 정리"
```

**Process**:
1. Find session files modified in recent N days
2. Extract conversation (filter out metadata)
3. Analyze combined sessions
4. Generate unified learning document

---

### Method 3: Analyze Specific Project

**English:**
```
"summarize all sessions in this project"
```

**Korean:**
```
"이 프로젝트의 모든 세션 정리"
```

**Process**:
1. Get current project path
2. Find all session files for this project
3. Extract and combine conversations
4. Generate comprehensive learning document

---

## Data Extraction

### Session File Structure

Claude Code session files are in JSONL format:

```jsonl
{"type": "user", "message": {...}, "timestamp": "..."}
{"type": "assistant", "message": {...}, "timestamp": "..."}
{"type": "file-history-snapshot", ...}  # 불필요 (67%)
{"type": "queue-operation", ...}        # 불필요 (27%)
```

**필요한 데이터**: `user` + `assistant.message.content[].text`
**불필요한 데이터**: `file-history-snapshot`, `queue-operation`, `thinking`, `tool_use`

### Extraction Command

```bash
# Extract conversations only
jq -c '
  if .type == "user" then
    {type: "user", content: .message.content, ts: .timestamp}
  elif .type == "assistant" then
    {type: "assistant", texts: [.message.content[]? | select(.type == "text") | .text], ts: .timestamp}
    | select(.texts | length > 0)
  else empty end
' session.jsonl
```

**Result**: 12MB → 160KB (93% reduction)

---

## Implementation in CLAUDE.md

### Option A: Extended Step 1

Add to **Step 1: Analyze Conversation**:

```markdown
1. **Analyze Conversation**:

   **Decision**: Current session only or include history?

   - Default: Analyze current conversation
   - If user mentions "recent", "this week", "past conversations": Include session history

   **If including history**:
   a. Determine scope (ask if unclear):
      - "Current project only" → ~/.claude/projects/<encoded-cwd>/*.jsonl
      - "All sessions" → ~/.claude/projects/**/*.jsonl

   b. Find session files:
      ```bash
      find ~/.claude/projects/<encoded-cwd> -name "*.jsonl" -mtime -7  # Last 7 days
      ```

   c. Extract conversations (use jq filter above)

   d. Combine with current session

   e. Proceed with analysis as normal
```

### Option B: Separate Preprocessing Step

Add **new Step 0** before current steps:

```markdown
0. **Determine Scope** (if user mentions history):

   If user mentions "recent", "this week", or "past conversations", ask:

   ```
   AskUserQuestion(
       questions=[{
           "question": "What conversation range would you like to analyze?",
           "header": "Analysis Scope",
           "multiSelect": false,
           "options": [
               {"label": "Current conversation only (Recommended)", "description": "Just the ongoing conversation"},
               {"label": "Past 3 days", "description": "All conversations from past 3 days"},
               {"label": "This week", "description": "All conversations this week"},
               {"label": "Entire project", "description": "All sessions in current project"}
           ]
       }]
   )
   ```

   Then proceed to extract and combine sessions.
```

---

## Example Usage

### Example 1: Current Session Only

```
User: "지금까지 대화 정리해줘"

Claude: [Analyzes current conversation only]
```

---

### Example 2: Recent Sessions

```
User: "최근 3일간 Claude Code 공부한 내용 정리해줘"

Claude: I'll analyze your recent Claude Code sessions from the past 3 days.

[Finds session files modified in last 3 days]
[Extracts conversations, filters for Claude Code topics]
[Generates unified learning document]

I've created a comprehensive summary at `.../2026-01-17-claude-code-3-day-review.md` covering:
- Marketplace concepts learned on Day 1
- Skill creation learned on Day 2
- Session history integration on Day 3
```

---

### Example 3: Project-wide Review

```
User: "이 프로젝트에서 배운 모든 내용 정리"

Claude: I'll analyze all sessions for this project.

[Finds all session files for current project]
[Processes ~10 sessions]
[Generates comprehensive learning document]

Created a project-wide learning summary with:
- 15 key concepts discovered
- 8 practical examples accumulated
- Common patterns and best practices
- Comprehensive reference section
```

---

## Performance Considerations

### File Size Handling

| Sessions | Total Size | Processing Method |
|----------|-----------|-------------------|
| 1-2 files | < 5 MB | Direct Read + parse |
| 3-5 files | 5-20 MB | Batch extract + summarize |
| 6+ files | > 20 MB | Parallel Task agents |

### Optimization Strategies

**Small sessions (1-2 files)**:
- Direct Read tool
- Parse JSONL in Claude
- No preprocessing needed

**Medium sessions (3-5 files)**:
- Use extraction script
- Batch process with jq
- Single analysis pass

**Large sessions (6+ files)**:
```bash
# Split into batches
find ~/.claude/projects -name "*.jsonl" | split -l 2 - /tmp/batch_

# Process each batch in parallel
for batch in /tmp/batch_*; do
  Task(subagent_type="general-purpose", model="opus", run_in_background=true,
       prompt="Analyze sessions in $batch and extract key learnings")
done

# Merge results
Task(subagent_type="general-purpose", model="opus",
     prompt="Combine all batch results into unified learning document")
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No session files found | "No session files found. Analyzing current conversation only." |
| jq not installed | "Warning: jq not found. Install with: brew install jq" |
| File too large | Auto-preprocess with extraction script |
| Permission denied | "Error: Cannot read session files. Check permissions." |
| Corrupted JSONL | "Warning: Skipping corrupted session file: {file}" |

---

## Configuration

Add to `config.yaml`:

```yaml
# Session history integration
session_history:
  # Enable session history analysis
  enabled: true

  # Default lookback period (days)
  default_lookback_days: 7

  # Maximum sessions to process
  max_sessions: 10

  # Preprocessing script
  extract_script: "scripts/extract-session.sh"
```

---

## Future Enhancements

1. **Incremental Processing**: Track which sessions were already processed
2. **Topic Filtering**: Only analyze sessions related to specific topic
3. **Timeline View**: Generate chronological learning progression
4. **Cross-Project Search**: Find related learnings across all projects

---

## References

- session-wrap plugin: `history-insight` skill
- Extraction script: Borrowed from `session-wrap/skills/history-insight/scripts/extract-session.sh`
- Session file format: `.jsonl` structure documentation
