---
name: future-architect
description: Organize thoughts and create actionable plans through conversational interviews. Use when user says "생각 정리", "계획 수립", "organize my thoughts", "plan clarification", or provides free-form thoughts with multiple topics
version: 1.0.0
---

# Future Architect Skill

**Trigger patterns**:
- Korean: "생각 정리", "계획 수립", "아이디어 정리", "목표 정리"
- English: "organize my thoughts", "plan clarification", "organize ideas", "structure my plan"

This skill detects user intent and launches the **future-architect agent** to conduct multi-round thought organization interviews.

---

## Execution Logic

### Step 1: Detect Intent

Check if the user wants to:
- **Create a new plan** (free-form input with topics)
- **Update an existing plan** (mentions "업데이트", "update", or references an existing document)

### Step 2: Route to Agent

#### Case A: New Plan

If the user provides free-form input with topics (bullet points or narrative):

```
Use Task tool:
  subagent_type: "future-architect"
  description: "Organize thoughts into actionable plan"
  prompt: |
    The user wants to organize their thoughts. Here is their input:

    {user_input}

    Please conduct the 10-step thought organization process:
    - Parse topics from input
    - Conduct topic-by-topic interviews (2-6 rounds per topic)
    - Generate cross-topic relationship analysis
    - Create Mermaid diagram
    - Generate capacity-aware TODO list
    - Save markdown document with agent_id in frontmatter
```

**IMPORTANT**: The agent will handle all interview rounds, question generation, and document creation. Do NOT conduct the interview yourself — just launch the agent.

#### Case B: Update Existing Plan

If the user mentions updating an existing plan:

1. **Ask for the document path**:
   ```
   AskUserQuestion:
     question: "어떤 계획을 업데이트하시겠어요?"
     header: "문서 선택"
     multiSelect: false
     options:
       - "직접 경로 입력" (파일 경로를 입력하겠습니다)
   ```

2. **Read the document** using the Read tool

3. **Extract agent_id from frontmatter**:
   ```yaml
   ---
   agent_id: abc123
   created_at: 2026-02-11
   status: active
   ---
   ```

4. **Resume the agent**:
   ```
   Use Task tool:
     subagent_type: "future-architect"
     description: "Update existing thought plan"
     resume: "{extracted_agent_id}"
     prompt: |
       The user wants to update their existing plan.

       Original document path: {document_path}

       Ask the user what they want to update:
       - Add new topics
       - Deepen existing topics
       - Update TODOs
       - Regenerate diagram with new relationships

       Then proceed with the relevant steps from the 10-step algorithm.
   ```

**IMPORTANT**: You must extract and provide the `agent_id` from the document frontmatter. If the frontmatter doesn't have `agent_id`, it was created before the agent conversion — treat it as a new plan instead.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No topics detected in input | Ask user to provide topics in bullet format or narrative |
| User input is too vague | Ask clarifying question: "무엇에 대한 생각을 정리하고 싶으신가요?" |
| Existing document has no agent_id | Inform user: "이 문서는 이전 버전으로 생성되어 agent_id가 없습니다. 새 계획으로 시작하시겠어요?" |
| Document path doesn't exist | Ask user to verify path or create new plan |

---

## Examples

### Example 1: New Plan (Multi-Topic)

**User**:
```
생각 정리해줘

- 커리어 전환
  급하게 취업을 시도하기 보다, 현재까지 vntg에서 했던 것들을 정리...
- 독일행
  독일에서 취업할 수 있는 개발자 포지션은...
- 창업
  서비스를 많이 만들어보고 싶다...
```

**Skill action**:
```
→ Detect: New plan with 3 topics
→ Launch agent with Task tool
→ Agent conducts full 10-step process
→ Document saved with agent_id
```

### Example 2: New Plan (Single Topic)

**User**: "커리어 전환에 대해 생각 정리하고 싶어"

**Skill action**:
```
→ Detect: New plan with 1 topic
→ Launch agent
→ Agent parses single topic, conducts interview
→ Document saved
```

### Example 3: Update Existing Plan

**User**: "이전 계획을 업데이트하고 싶어"

**Skill action**:
```
→ Detect: Update intent
→ Ask for document path
→ User provides: ~/Documents/plans/2026-02-11-커리어-독일-창업-투자.md
→ Read document
→ Extract agent_id from frontmatter
→ Resume agent with agent_id
→ Agent asks what to update, proceeds accordingly
```

### Example 4: Ambiguous Input

**User**: "생각 정리"

**Skill action**:
```
→ Detect: Trigger phrase but no content
→ Ask: "무엇에 대한 생각을 정리하고 싶으신가요? 자유롭게 말씀해주세요."
→ Wait for user response
→ Launch agent with user's clarified input
```

---

## Configuration

The agent reads configuration from:
`~/.claude/skills/future-architect/config.yaml`

**Default config**:
```yaml
output_dir: "~/Documents/plans"
auto_open: true
diagram_direction: "TD"
priority_system: "3-tier"
filename_format: "{date}-{topic1}-{topic2}-....md"  # Must run `date '+%Y-%m-%d'` to get exact date. Never estimate.
```

If config doesn't exist, the agent uses these defaults.

---

## Related Files

- **Agent**: `plugins/future-architect/agents/future-architect.md` (actual logic)
- **Config**: `~/.claude/skills/future-architect/config.yaml` (settings)
- **Output**: `~/Documents/plans/` (default save location)

---

## Important Notes

- This Skill is just a **trigger and router** — all logic is in the agent
- The agent maintains state across multiple turns (multi-round interviews)
- The agent saves `agent_id` in document frontmatter for resume functionality
- To update a plan, the user must provide the document path (Skill extracts agent_id)

---

## Architecture

```
User input
    ↓
future-architect Skill (this file)
    ↓
Detect: New plan or Update?
    ↓
Launch future-architect Agent
    ↓
Agent executes 10-step algorithm
    ↓
Document saved with agent_id
```
