---
name: spec-interview
description: AI-driven requirements interview. Use when user says "interview me", "gather requirements", "help me spec this out", "ask me questions about", or wants to create detailed specifications through interactive Q&A.
version: 1.0.0
---

# Spec Interview

Conducts in-depth interviews to gather comprehensive requirements, then generates detailed specification documents.

---

## Execution Algorithm

### Step 1: Parse Initial Request

Extract from user message:

| Element | What to Extract |
|---------|----------------|
| **Topic** | What feature/project they want to specify |
| **Context** | Any initial description or constraints provided |
| **Focus Areas** | Specific aspects they want to emphasize |

**Examples:**
- `"Interview me about building a task management app"` → Topic extracted
- `"Help me spec out a new authentication system"` → Topic + domain
- `"Ask me questions about redesigning our dashboard"` → Topic + focus (UI/UX)

**Initial acknowledgment:**
Briefly confirm the topic and explain the interview process.

---

### Step 2: Generate First Question Set

Create 2-4 in-depth questions using AskUserQuestion tool.

**Question Categories (rotate through these):**

| Category | Question Types |
|----------|---------------|
| **Technical Implementation** | Architecture, tech stack, integrations, scalability, performance |
| **User Experience** | User flows, interactions, edge cases, error states, accessibility |
| **Business Logic** | Rules, constraints, validations, permissions, workflows |
| **Concerns & Risks** | Security, privacy, compliance, data handling, potential issues |
| **Trade-offs** | Performance vs features, complexity vs simplicity, cost vs quality |
| **Non-functional Requirements** | Monitoring, logging, testing, deployment, maintenance |

**Question Quality Rules:**

✅ **DO Ask:**
- "What happens when two users edit the same item simultaneously?"
- "How should the system behave when the external API is down?"
- "What's your priority: faster implementation or more flexible architecture?"
- "Who should have permission to delete data, and what's the recovery process?"

❌ **DON'T Ask:**
- "Do you want this to be fast?" (too obvious)
- "Should we use React?" (too specific without context)
- "Is security important?" (always yes, not insightful)

**AskUserQuestion Format:**
```python
AskUserQuestion(
    questions=[
        {
            "question": "What happens when...",
            "header": "Edge Case",
            "options": [
                {"label": "Option A", "description": "What this means..."},
                {"label": "Option B", "description": "Trade-off here..."},
                {"label": "Option C", "description": "Alternative approach..."}
            ],
            "multiSelect": false
        },
        # 1-3 more questions
    ]
)
```

**Important:**
- Ask 2-4 questions per round (not overwhelming)
- Each question should reveal non-obvious insights
- Options should present real trade-offs, not obvious good/bad choices
- Headers should be short (max 12 chars): "Tech Stack", "User Flow", "Trade-off"

---

### Step 3: Analyze Responses

After receiving answers, analyze what you learned:

**Track Coverage:**
- ✅ Technical architecture
- ✅ User experience flows
- ⚠️ Security concerns (needs more depth)
- ❌ Performance requirements (not covered yet)
- ❌ Testing strategy (not covered yet)

**Identify Gaps:**
- What critical aspects haven't been discussed?
- What answers raised new questions?
- What assumptions need validation?

---

### Step 4: Generate Next Question Set

Based on gaps and new insights, ask 2-4 more questions.

**Follow-up Strategy:**
1. **Drill deeper** on concerning answers
2. **Explore uncovered areas** from the tracking list
3. **Validate assumptions** from previous responses
4. **Challenge trade-offs** if user chose all easy options

**Example Progression:**

**Round 1:** High-level architecture, main user flows
**Round 2:** Edge cases, error handling, data consistency
**Round 3:** Security, permissions, compliance
**Round 4:** Performance, scalability, monitoring

**Depth over breadth:**
Better to fully understand 3 critical areas than superficially cover 10.

---

### Step 5: Determine Completion

Interview is complete when:

✅ **Coverage criteria met:**
- Core functionality clearly defined
- Critical edge cases discussed
- Major technical decisions made
- Key risks and trade-offs identified
- Non-obvious insights gathered

✅ **Diminishing returns:**
- New questions would be minor details
- User has given comprehensive answers
- No significant gaps remain

**Don't over-interview:**
- Stop at 3-5 rounds for simple features
- Stop at 5-8 rounds for complex projects
- If user is repeating themselves, move on

---

### Step 6: Generate Specification Document

Create comprehensive spec document using all gathered information.

**Spec Template:**

```markdown
# [Feature/Project Name] - Technical Specification

> **Generated**: YYYY-MM-DD
> **Author**: [User name if known]
> **Status**: Draft

## 1. Overview

### Purpose
[What this feature/project does and why it's needed]

### Scope
**In Scope:**
- [Item 1]
- [Item 2]

**Out of Scope:**
- [Item 1]
- [Item 2]

## 2. Requirements

### Functional Requirements

#### FR-1: [Requirement Name]
- **Description**: [What it does]
- **Priority**: High/Medium/Low
- **Rationale**: [Why this is needed]
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2

#### FR-2: [Next Requirement]
...

### Non-Functional Requirements

#### NFR-1: Performance
- [Specific performance requirements]

#### NFR-2: Security
- [Security requirements and concerns]

#### NFR-3: Scalability
- [Scalability considerations]

## 3. Technical Design

### Architecture Overview
[High-level architecture description]

```
[ASCII diagram or description]
```

### Technology Stack
- **Frontend**: [Choices and rationale]
- **Backend**: [Choices and rationale]
- **Database**: [Choices and rationale]
- **Infrastructure**: [Choices and rationale]

### Key Components

#### Component 1: [Name]
- **Responsibility**: [What it does]
- **Interfaces**: [How it connects]
- **Dependencies**: [What it needs]

### Data Models

#### Model 1: [Entity Name]
```typescript
interface Entity {
  id: string
  field1: Type
  field2: Type
}
```

## 4. User Experience

### User Flows

#### Flow 1: [Happy Path]
1. User does X
2. System responds with Y
3. User sees Z

#### Flow 2: [Edge Case]
...

### UI/UX Considerations
- [Key interaction patterns]
- [Accessibility requirements]
- [Error states and messaging]

## 5. Implementation Details

### Phase 1: [MVP / Core Features]
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Phase 2: [Enhancements]
- [ ] Task 1
- [ ] Task 2

### Technical Decisions

#### Decision 1: [What was decided]
- **Options Considered**: A, B, C
- **Chosen**: B
- **Rationale**: [Why B over A and C]
- **Trade-offs**: [What we're giving up]

## 6. Edge Cases & Error Handling

### Edge Case 1: [Scenario]
- **Situation**: [When this happens]
- **Expected Behavior**: [What should happen]
- **Fallback**: [If primary approach fails]

### Error Scenarios

| Error Type | User Action | System Response |
|------------|-------------|-----------------|
| Network failure | Submitting form | Show retry option, preserve data |
| Invalid input | Entering data | Inline validation, clear error message |

## 7. Security & Privacy

### Security Considerations
- [Authentication approach]
- [Authorization rules]
- [Data encryption]
- [API security]

### Privacy & Compliance
- [Data handling policies]
- [User consent requirements]
- [Compliance requirements (GDPR, etc.)]

## 8. Testing Strategy

### Test Coverage

#### Unit Tests
- [What to unit test]

#### Integration Tests
- [What to integration test]

#### E2E Tests
- [Critical user flows to test]

### Test Scenarios
1. **Happy path**: [Description]
2. **Edge case 1**: [Description]
3. **Error case 1**: [Description]

## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | How to mitigate |
| Risk 2 | High/Med/Low | High/Med/Low | How to mitigate |

## 10. Open Questions

- [ ] Question 1 that needs resolution
- [ ] Question 2 that needs stakeholder input
- [ ] Question 3 requiring further research

## 11. Success Metrics

### Key Metrics
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

### Monitoring
- [What to monitor]
- [Alert thresholds]

## 12. References

### Related Documents
- [Link to designs]
- [Link to API docs]
- [Link to research]

### Interview Notes
[Summary of key insights from the interview process]

---

**Next Steps:**
1. [ ] Review and validate this specification
2. [ ] Share with stakeholders for feedback
3. [ ] Break down into implementable tasks
4. [ ] Update as requirements evolve
```

**Customization Rules:**
- Include only relevant sections (skip empty ones)
- Adapt depth to project complexity
- Preserve all insights from interview
- Use user's own language and examples where possible
- If user mentioned specific concerns, highlight them

---

### Step 7: Choose Save Location

**Options:**

1. **Current directory** (default)
   - Save as `[feature-name]-spec.md` in current working directory
   - Good for project-specific specs

2. **Ask user for location**
   - If they have a preferred docs directory
   - If this should go into a specific repo

**Filename format:**
- `[feature-name]-spec.md` (e.g., `task-management-spec.md`)
- Or user's preferred format if specified

---

### Step 8: Save Document

Use Write tool to create the specification file.

**Save location examples:**
```
./task-management-spec.md
./docs/specs/authentication-spec.md
/Users/jaykim/Documents/Projects/myapp/specs/dashboard-redesign-spec.md
```

**If directory doesn't exist:**
```bash
mkdir -p path/to/directory
```

---

### Step 9: Confirm to User

Show the user:
- ✅ Full path of saved specification
- 📋 Brief summary of what was captured
- 🎯 Next steps recommendation
- 💡 Suggest related actions

**Example confirmation:**
```
✅ Specification saved to: ./task-management-spec.md

📋 Captured:
- 12 functional requirements
- Architecture: React + Node.js + PostgreSQL
- 8 key user flows with edge cases
- Security: JWT auth + role-based permissions
- 3 implementation phases defined

🎯 Next Steps:
1. Review and validate the specification
2. Break down into tasks (I can help with this!)
3. Identify any missing requirements

Want me to:
- Create a task breakdown from this spec?
- Generate API endpoint definitions?
- Draft database migration scripts?
```

---

## Trigger Phrases

**English:**
- "interview me"
- "interview me about [topic]"
- "help me spec this out"
- "gather requirements"
- "ask me questions about [topic]"
- "I want to build [X], ask me questions"

**Korean:**
- "인터뷰해줘"
- "[주제]에 대해 질문해줘"
- "요구사항 정리해줘"
- "스펙 작성 도와줘"

---

## Interview Best Practices

### 1. Ask Non-Obvious Questions

**Bad Questions:**
- "Should this be secure?" (always yes)
- "Do you want good performance?" (too vague)
- "Should we use best practices?" (meaningless)

**Good Questions:**
- "When two users edit the same item simultaneously, should the last write win, or should we detect conflicts?"
- "If the external API is down, should we queue requests or fail immediately with an error?"
- "Would you prioritize a more flexible architecture that takes longer to build, or a simpler implementation that ships faster but is harder to extend later?"

### 2. Present Real Trade-offs

**Bad Options:**
- Option A: Fast, secure, scalable (obviously good)
- Option B: Slow, insecure, doesn't scale (obviously bad)

**Good Options:**
- Option A: Server-side rendering (better SEO, slower interactivity)
- Option B: Client-side rendering (faster interactivity, SEO challenges)
- Option C: Hybrid approach (best of both, more complexity)

### 3. Dig Deeper on Vague Answers

If user says:
- "Make it fast" → Ask: "Fast for what? Page load? API response? Complex queries?"
- "Standard security" → Ask: "OAuth? JWT? Session cookies? Rate limiting rules?"
- "Good UX" → Ask: "What happens when they click X? How do they recover from errors?"

### 4. Validate Assumptions

If user says something concerning:
- "We'll handle millions of users" → Ask: "How many concurrent users? What's the traffic pattern?"
- "It needs to be real-time" → Ask: "Real-time as in WebSockets, or polling every 5 seconds is fine?"

### 5. Know When to Stop

Stop when:
- Diminishing returns (trivial details)
- User is frustrated or repeating
- Core requirements are clear
- You have enough to write a useful spec

Don't stop when:
- Critical decisions are unclear
- User hasn't thought about edge cases
- Security/privacy concerns unaddressed

---

## Quick Reference

### When to Use

✅ **Use this skill when:**
- User wants to build something but hasn't fully thought through requirements
- User says "help me spec this" or "interview me about X"
- Complex feature needs thorough planning
- User prefers interactive Q&A over writing a doc themselves

❌ **Skip when:**
- User has already written detailed requirements (just review instead)
- User wants to start coding immediately (respect their preference)
- Very simple, well-defined task (1-2 questions max, not a full interview)

---

## Error Handling

| Scenario | Response |
|----------|----------|
| User gives vague answers | Drill deeper with specific follow-up questions |
| User says "I don't know" | Offer options, educate on trade-offs, suggest industry standard |
| Interview going too long | Summarize and ask if they want to continue or wrap up |
| User wants to skip questions | Respect it, note as open question in spec |
| Critical gaps remain | Flag them clearly in the spec's "Open Questions" section |

---

## Examples

### Example 1: Simple Feature

```
User: "Interview me about adding a dark mode feature"

Round 1:
Q1: How should users toggle dark mode?
Q2: Should the preference persist across sessions?
Q3: Should it respect system preferences?

Round 2:
Q1: What about images that look bad in dark mode?
Q2: Should third-party embeds (YouTube, etc.) also be dark?

→ Stop here (simple feature, enough detail)

Generate spec: 5-page document covering implementation
```

### Example 2: Complex Project

```
User: "I want to build a real-time collaboration tool, interview me"

Round 1: Core functionality, main use cases
Round 2: Real-time sync approach, conflict resolution
Round 3: Permissions, security, data privacy
Round 4: Scalability, performance under load
Round 5: Edge cases, offline mode, error recovery
Round 6: Testing, deployment, monitoring

→ Stop here (complex project fully explored)

Generate spec: 20-page comprehensive document
```

### Example 3: Focused Interview

```
User: "Interview me about improving our API rate limiting"

Round 1: Current problems, desired behavior
Round 2: Rate limit rules, per-user vs global
Round 3: How to handle violations, error messages
Round 4: Monitoring, alerting, bypass for admins

→ Stop here (focused topic, thorough coverage)

Generate spec: 8-page technical design
```

---

## Related Skills

- `learning-summary`: For documenting the interview process itself
- `project-insight`: For analyzing existing codebase before planning new features

---

## Tips

1. **Build trust early**: Start with easier questions to get user comfortable
2. **Rotate categories**: Don't ask 10 technical questions in a row
3. **Use user's answers**: Reference their previous answers in follow-up questions
4. **Educate through options**: Option descriptions can teach trade-offs
5. **Flag disagreements**: If their answers contradict, ask them to clarify
6. **Preserve exact quotes**: Use their words in the spec for clarity
7. **Visual diagrams**: Ask if they want to sketch flows (can describe verbally)
8. **Celebrate completeness**: When you have what you need, tell them!

---

## Configuration

No configuration file needed. Saves to current directory by default or prompts user for location.

---

## Advanced Usage

### Batch Interview

User can interview for multiple features:
```
"Interview me about: 1) user authentication, 2) file uploads, 3) notifications"
```

Handle by:
- Interview each separately
- Generate separate specs
- Note dependencies between features

### Resume Interview

If interrupted, user can say:
```
"Continue the interview about [topic]"
```

Read the partial spec and continue from where it left off.

### Collaborative Spec

Multiple stakeholders:
```
"Interview me and my co-founder about our app"
```

Tag answers by person, note disagreements, highlight consensus decisions.
