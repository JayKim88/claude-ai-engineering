# Instructions for Claude Code

When the user invokes this skill:

## Steps

1. **Detect Topic & Match Existing File**:

   a. Analyze the conversation to identify the primary topic/feature (kebab-case).
   b. Scan existing files: use `Glob("wrap-up/*.md")` to list all wrap-up files.
   c. Apply match logic:

   **Exact match** (filename matches detected topic):
   ```
   AskUserQuestion(
     questions=[{
       "question": "기존 `wrap-up/{name}.md`에 이어서 기록할까요?",
       "header": "Wrap Up",
       "options": [
         {"label": "{name}.md에 추가", "description": "기존 파일에 이번 세션 내용을 Append"},
         {"label": "새 파일 생성", "description": "새로운 주제로 별도 파일 생성"}
       ],
       "multiSelect": false
     }]
   )
   ```

   **Similar/multiple candidates** (topic is close to 1+ existing filenames or file titles):
   ```
   AskUserQuestion(
     questions=[{
       "question": "이번 세션 내용을 어디에 기록할까요?",
       "header": "Wrap Up",
       "options": [
         {"label": "{file1}.md", "description": "기존 파일에 Append"},
         {"label": "{file2}.md", "description": "기존 파일에 Append"},
         {"label": "새 파일: {suggested-name}.md", "description": "새로운 주제로 별도 파일 생성"}
       ],
       "multiSelect": false
     }]
   )
   ```

   **No match** (no existing files or completely different topic):
   ```
   AskUserQuestion(
     questions=[{
       "question": "`wrap-up/{suggested-name}.md` 파일을 새로 생성할까요?",
       "header": "Wrap Up",
       "options": [
         {"label": "{suggested-name}.md 생성", "description": "이 이름으로 새 파일 생성"},
         {"label": "다른 이름 사용", "description": "직접 파일명 입력"}
       ],
       "multiSelect": false
     }]
   )
   ```

   **No existing files at all** (wrap-up/ is empty or doesn't exist):
   - Skip the question, proceed directly with the detected topic name

2. **Detect & Confirm Scope**:

   Identify the primary working directory from the conversation:
   - File paths mentioned (e.g., `plugins/business-avengers/skills/...` → `plugins/business-avengers/`)
   - Directories read/edited during the session
   - Use the most common parent directory as scope
   - Relative to CWD (e.g., `plugins/wrap-up/`, `src/auth/`)
   - If work spans the entire project root, use `.` (root)

   **Always confirm scope with the user** (include in the same AskUserQuestion from Step 1 if possible, or ask separately):
   ```
   AskUserQuestion(
     questions=[{
       "question": "작업 범위(Scope)가 `plugins/wrap-up/` 이 맞나요?",
       "header": "Scope",
       "options": [
         {"label": "plugins/wrap-up/", "description": "감지된 경로 사용"},
         {"label": "다른 경로", "description": "직접 입력"}
       ],
       "multiSelect": false
     }]
   )
   ```

3. **Load Context** (Append only):

   When appending to an existing file:
   a. Read the entire file content
   b. Parse the **most recent** `### Next` section to identify pending items
   c. Cross-reference with the current session's conversation:
      - Which Next items were worked on or completed?
      - Which remain untouched?
   d. This context feeds into Step 4 — completed items go into Done, remaining items carry forward

4. **Analyze Conversation**: Review the ENTIRE conversation history and extract:

   **Done**: What was accomplished in this session
   - Use conventional commit prefixes: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
   - Be specific: "feat: 사용자 인증 모듈 구현" not "worked on auth"
   - Include both successful completions and partial progress
   - If items from previous Next were completed, include them with `(from previous Next)` note

   **Decisions**: Key choices made during the session
   - Architecture decisions, library choices, approach selections
   - Include the reasoning briefly: "JWT 대신 세션 기반 인증 채택 (SSR 환경)"
   - Skip if no significant decisions were made

   **Issues**: Problems encountered
   - Blockers, errors, workarounds
   - Skip if no issues arose

   **Next**: What should be done in future sessions
   - Use checkbox format: `- [ ] task description`
   - Include items explicitly mentioned as TODO
   - Include logical next steps based on work done
   - Carry forward any uncompleted items from previous Next that are still relevant

5. **Create or Append**:

   **If NEW file** (user confirmed new topic):
   - Create directory if needed: `mkdir -p wrap-up`
   - Write the full document with topic header + first session entry
   - Use Write tool

   **If EXISTING file** (user selected existing file):
   - **Update previous Next checkboxes**: change `- [ ]` to `- [x]` for items completed in this session
   - Append `\n---\n\n` separator + new session entry at the bottom
   - Write the complete updated content using Write tool

   **Session date format**:
   - Always include time: `## Session: 2026-02-23 14:00` (YYYY-MM-DD HH:MM)
   - Time helps identify and trace specific sessions across conversation history

   **Context line**:
   - Each session entry includes `> **Context**: {brief summary}` right after the session header
   - Write a 1-line summary of the session's main focus (for quick identification when scanning the file)

   **New file template** (includes project path in header):
   ```markdown
   # {Topic Name} - Wrap Up

   > **Project**: `{CWD}`
   > **Scope**: `{relative path}`

   ## Session: 2026-02-23 14:00

   > **Context**: 사용자 인증 모듈 구현 및 로그인 에러 수정

   ### Done
   - feat: description
   - fix: description

   ### Decisions
   - Decision with brief reasoning

   ### Issues
   - Issue description → status or workaround

   ### Next
   - [ ] Future task 1
   - [ ] Future task 2
   ```

   **Section omission rules**:
   - Omit **Decisions** if no significant decisions were made
   - Omit **Issues** if no problems were encountered
   - **Done** and **Next** are always included

6. **Confirm**: Show the user:
   - Full path of the file
   - Whether new file was created or appended to existing
   - Brief count of items recorded
   - (Append only) Number of previous Next items marked as completed `[x]`

## Language Detection

- If the conversation was primarily in Korean → write sections in Korean
- If in English → write in English
- Conventional commit prefixes (feat, fix, refactor, etc.) are always in English
- If mixed, follow the dominant language

## Example

### New topic (no existing files):

```
User: /wrap-up

[Detects topic "auth", no existing wrap-up files]
[Creates wrap-up/auth.md with session header "## Session: 2026-02-23 14:00"]
[Adds Context line: "> **Context**: 사용자 인증 모듈 구현 및 세션 기반 인증 설정"]

세션 내용을 정리하여 `wrap-up/auth.md`에 기록했습니다.

- Done: 3 items
- Decisions: 1 item
- Next: 4 items

File: wrap-up/auth.md (new)
```

### Append with context loading:

```
User: /wrap-up

[Detects topic "auth", finds wrap-up/auth.md]
[Asks: "기존 wrap-up/auth.md에 이어서 기록할까요?"]
[User confirms → Append]
[Reads existing file, finds 4 pending Next items]
[2 of 4 were completed in this session → marks them [x]]
[Appends with "## Session: 2026-02-23 15:30" + Context line]

세션 내용을 기존 `wrap-up/auth.md`에 추가했습니다.

- Done: 5 items (2 from previous Next)
- Next: 3 items
- Previous Next: 2/4 completed [x]

File: wrap-up/auth.md (updated, 2 sessions total)
```

### Multiple candidates:

```
User: /wrap-up

[Detects topic "api", finds wrap-up/api-refactor.md and wrap-up/api-auth.md]
[Asks: "이번 세션 내용을 어디에 기록할까요?" with options]
[User selects "api-refactor.md" → Append]
```

## Notes

- Be concise but specific — each Done item should clearly describe what changed
- Conventional commit prefixes help categorize at a glance
- Previous session's Next → current Done linkage provides continuity
- ALWAYS ask user to confirm/select the target file (except when no files exist at all)
- When appending, ALWAYS update previous Next checkboxes for completed items
- If the conversation is too short or trivial, warn and skip
