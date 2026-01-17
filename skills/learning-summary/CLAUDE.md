# Instructions for Claude Code

When the user invokes this skill:

## Steps

1. **Analyze Conversation**: Review the entire conversation history to identify:
   - Key concepts and terminology explained
   - New knowledge gained by the user
   - Practical examples and use cases
   - Important distinctions or clarifications made
   - Files and resources referenced

2. **Structure Content**: Organize the information into these sections:
   - **Key Concepts**: Main topics discussed with clear definitions
   - **New Learnings**: What the user learned, with before/after understanding
   - **Practical Examples**: Code snippets, commands, or real examples
   - **Common Misconceptions**: Clarifications on misunderstandings
   - **References**: Files, URLs, or resources mentioned
   - **Next Steps**: Suggested follow-up actions or topics to explore

3. **Ask Section Preferences** (Optional): If the conversation is complex or the user might prefer a focused summary, ask which sections to include:

   ```
   AskUserQuestion(
       questions=[{
           "question": "Which sections would you like to include?",
           "header": "Section Selection",
           "multiSelect": true,
           "options": [
               {"label": "Key Concepts (Recommended)", "description": "Main topics and definitions"},
               {"label": "New Learnings", "description": "Before/after learnings"},
               {"label": "Practical Examples", "description": "Code, commands, examples"},
               {"label": "Common Misconceptions", "description": "Clarified misconceptions"},
               {"label": "References", "description": "Files, URLs, resources"},
               {"label": "Next Steps", "description": "Follow-up actions"}
           ]
       }]
   )
   ```

   **When to ask**:
   - User explicitly requests specific sections
   - Very long conversation (might want focused summary)
   - User says "briefly", "concise", or "short summary"

   **When to skip**:
   - Normal length conversation (include all sections by default)
   - User doesn't express preference
   - First time using the skill (show full example)

4. **Generate Filename**: Create a descriptive filename based on the main topic:
   - Format: `YYYY-MM-DD-brief-topic-description.md`
   - Example: `2026-01-17-claude-code-marketplace-guide.md`

5. **Read Configuration**: Read the config file at `~/.claude/skills/learning-summary/config.yaml` to get:
   - `learning_repo`: The dedicated AI learning repository path
   - `output_dir`: Output directory (relative to learning_repo)
   - `auto_commit`: Whether to auto-commit
   - `auto_push`: Whether to auto-push (requires auto_commit)
   - `sections`: Default sections to include (if user didn't select in Step 3)

6. **Save Document**:
   - Location: `{learning_repo}/{output_dir}/YYYY-MM-DD-topic.md`
   - Example: `/Users/username/Documents/Projects/ai-learning/learnings/2026-01-17-claude-code-marketplace.md`
   - Use Write tool to create the markdown file at the configured path
   - Include only the sections selected in Step 3 (or all if skipped)

7. **Git Operations** (if auto_commit is true):
   - Change to the learning_repo directory
   - Run `git add {filename}`
   - Run `git commit -m "Add learning: {topic}"`
   - If auto_push is true, run `git push`

8. **Confirm**: Show the user:
   - Full path of saved file
   - Brief summary of what was documented
   - Git commit status (if auto_commit was enabled)
   - Offer to open the file or make adjustments

## Example

```
User: "Summarize what I learned today"

Claude: I'll create a learning summary document capturing the key insights from our conversation about Claude Code marketplaces and plugins.

[Reads config.yaml to get learning_repo path]
[Uses Write tool to create the document at /Users/username/Documents/Projects/ai-learning/learnings/2026-01-17-claude-code-marketplace.md]

I've created a comprehensive guide at `/Users/username/Documents/Projects/ai-learning/learnings/2026-01-17-claude-code-marketplace.md` covering:

- What marketplaces are (decentralized GitHub repos)
- How they differ from plugins
- Three installation methods (marketplace, npx, symlink)
- Global vs local installation
- Common misconceptions

The document has been saved to your AI learning repository. Would you like me to commit this to git or make any adjustments?
```

## Notes

- Be comprehensive but concise
- Use tables and code blocks for clarity
- Include bilingual content when appropriate (Korean/English examples preserved as-is)
- Preserve important terminology in both languages when relevant
- Focus on practical, actionable information

---

## Advanced: Session History Integration (Future)

If user mentions "recent sessions", "this week", or "past conversations", you can analyze historical sessions:

**Trigger phrases (English)**:
- "summarize the past 3 days"
- "review this week's learnings"
- "analyze all sessions in this project"

**Trigger phrases (Korean)**:
- "최근 3일간 대화 정리"
- "이번 주 학습 내용 정리"
- "이 프로젝트의 모든 세션 분석"

**Process**:
1. Determine scope (current project vs all projects)
2. Find session files: `~/.claude/projects/<encoded-cwd>/*.jsonl`
3. Extract conversations (filter out metadata)
4. Combine with current session
5. Generate unified learning document

**For details**: See `references/session-history-integration.md`

**Note**: This is a planned feature. Current version analyzes current conversation only.
