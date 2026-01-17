# Learning Note Best Practices

Best practices for writing effective learning notes

---

## 1. When to Write

### ✅ Good Timing

- **Write immediately**: Right after the conversation (while fresh)
- **Before context switching**: Before moving to a different topic
- **After "aha" moments**: Right after understanding a complex concept
- **After problem solving**: When the solution is clear

### ❌ Timing to Avoid

- End of day combining multiple topics
- Days later relying on memory
- Before fully understanding (leads to inaccurate documentation)

---

## 2. Title Writing

### Good Title Examples

✅ **Specific and searchable**
- `Understanding Claude Code Marketplace Architecture`
- `Optimizing Python asyncio for Parallel API Calls`
- `Docker Compose Networking and Inter-Service Communication`

❌ **Titles to Avoid**
- `What I Learned Today` (not searchable)
- `Claude Code` (too broad)
- `Question` (meaningless)

### Filename Convention

**Format**: `YYYY-MM-DD-descriptive-topic.md`

**Good examples**:
- `2026-01-17-claude-code-marketplace-architecture.md`
- `2026-01-17-kubernetes-pod-networking.md`

**Bad examples**:
- `notes.md`
- `learning-1.md`
- `2026-01-17.md` (no topic)

---

## 3. Writing Key Concepts

### Principles

1. **Be concise**: Define in 3-5 sentences
2. **Use analogies**: Connect to familiar concepts
3. **Use tables**: Effective for comparisons
4. **Hierarchical structure**: Top concept → sub-concepts

### Example: Good Key Concept Explanation

```markdown
## Key Concepts

### 1. Marketplace

**Marketplace = GitHub Repository**

A decentralized system where anyone can publish, unlike App Store.

| Feature | Description |
|---------|-------------|
| Type | Decentralized (similar to npm) |
| Creation | GitHub + marketplace.json |
| Approval | Not required |
```

---

## 4. Before/After Pattern

### Why It's Effective

- **Document misconceptions**: Record wrong understanding
- **Preserve learning process**: Prevent same mistakes later
- **Relatable**: Others likely have same misconceptions

### Template

```markdown
## New Learnings

### Before: Misconceptions
- [Specific misconception 1]
- [Specific misconception 2]

### After: Reality
- [Accurate understanding 1]
- [Accurate understanding 2]
```

### Real Example

```markdown
### Before
- Thought async/await is the same as multithreading
- Believed all I/O operations must use async

### After
- async/await is cooperative multitasking (single-threaded)
- Only useful for I/O-bound; CPU-bound needs multiprocessing
```

---

## 5. Writing Practical Examples

### Requirements for Good Examples

1. **Executable**: Copy-paste and run
2. **Minimal**: Only essential elements
3. **Include comments**: Explain important parts
4. **Show output**: Include expected results

### Template

```markdown
## Practical Examples

### Example 1: [Scenario description]

\`\`\`bash
# [Command explanation]
command --option value

# Expected output:
# Output here
\`\`\`

**Explanation**: [Why it works this way]
```

### Real Example

```markdown
## Practical Examples

### Example 1: Add Marketplace and Install Plugin

\`\`\`bash
# Connect marketplace
/plugin marketplace add team-attention/plugins-for-claude-natives

# Install specific plugin
/plugin install agent-council

# Verify installation
ls ~/.claude/plugins/
# → agent-council/ directory created
\`\`\`

**Explanation**: `marketplace add` registers remote repository to local Claude Code,
`install` downloads the specific plugin from that repository.
```

---

## 6. Referencing Resources

### Link Types

1. **Local files**: Absolute path + line number
2. **Web docs**: Full URL
3. **Git repos**: Specific file/commit

### Format

```markdown
## References

### File Locations
- **Config file**: `~/.claude/skills/learning-summary/config.yaml`
- **Script**: `scripts/save-learning.sh:42`

### Web Documentation
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

### GitHub
- [agent-council](https://github.com/team-attention/agent-council)
```

---

## 7. Writing Next Steps

### Principles

1. **Be specific**: Not "Study more" ✗ → "Read aiohttp official docs" ✓
2. **Actionable**: Can start immediately
3. **Prioritize**: Show importance/urgency
4. **Realistic scope**: Achievable timeframe

### Template

```markdown
## Next Steps

### Immediate (High Priority)
1. [Specific action 1]
2. [Specific action 2]

### Explore Later (Low Priority)
3. [Optional action 1]
4. [Optional action 2]
```

### Real Example

```markdown
## Next Steps

### Immediate
1. ✅ Install and test agent-council plugin
2. ✅ Document this conversation with learning-summary

### This Week
3. ⚪ Try clarify plugin
4. ⚪ List custom skill ideas

### Someday
5. 📌 Create my own marketplace
6. 📌 Integrate session history analysis skill
```

---

## 8. Language Usage

### Bilingual Principles

✅ **Recommended**:
- Titles: English (for searchability)
- Key terms: English + translation
- Example: `Marketplace (마켓플레이스)`

✅ **Code/Commands**:
- Always keep original English
- Comments can be bilingual

### Example

```markdown
## Key Concepts

### 1. Asynchronous Programming (비동기 프로그래밍)

Use **async/await keywords** to efficiently handle I/O-bound operations

\`\`\`python
# Define async function
async def fetch_data():
    # Wait for completion with await
    data = await client.get(url)
    return data
\`\`\`
```

---

## 9. Using Visualization

### Tables

**Strength**: Effective for comparison, contrast, classification

```markdown
| Before | After |
|--------|-------|
| Misconception | Accurate understanding |
```

### Diagrams (ASCII)

```
Phase 1: Analysis
┌──────────┬──────────┐
│ Agent A  │ Agent B  │
└────┬─────┴────┬─────┘
     └──────────┘
          │
     Phase 2: Synthesis
```

### Code Block Language Specification

```python
def example():
    pass
```

```bash
ls -la
```

---

## 10. Regular Review

### Weekly Review

1. List this week's notes
2. Add links between related notes
3. Update next steps progress

### Monthly Review

1. Reclassify by topic
2. Merge duplicate content
3. Update outdated information

### Tools

```bash
# Find notes from past week
find ~/Documents/Projects/ai-learning/learnings -type f -mtime -7

# Search for specific keyword
grep -r "async" ~/Documents/Projects/ai-learning/learnings/
```

---

## Checklist

Before finalizing a learning note:

- [ ] Is the title specific and searchable?
- [ ] Did I document the learning process with Before/After?
- [ ] Are examples executable?
- [ ] Are reference links clear?
- [ ] Are next steps specific and actionable?
- [ ] Are code blocks language-specified?
- [ ] Does filename follow standard format? (YYYY-MM-DD-topic.md)
- [ ] Is the content concise but comprehensive?

---

## Common Pitfalls

### 1. Too Verbose

❌ **Bad**: Paragraph after paragraph of explanation
✅ **Good**: Bullet points, tables, concise explanations

### 2. Missing Context

❌ **Bad**: Code snippets without explanation
✅ **Good**: Code + comment + explanation of why

### 3. No Examples

❌ **Bad**: Only theoretical concepts
✅ **Good**: Concepts + practical examples

### 4. Vague Next Steps

❌ **Bad**: "Learn more about this"
✅ **Good**: "Read Chapter 3 of Python Async Cookbook"

---

## Examples of Excellent Notes

### Example 1: Technical Learning

- ✅ Clear title: "Understanding JWT Authentication Flow"
- ✅ Before/After misconceptions documented
- ✅ Executable code examples with comments
- ✅ Diagram showing token flow
- ✅ Specific next steps: "Implement refresh token logic"

### Example 2: Tool Learning

- ✅ Clear title: "Using Docker Compose for Multi-Container Apps"
- ✅ Real `docker-compose.yml` example
- ✅ Common errors and solutions
- ✅ Reference to official docs
- ✅ Next step: "Add nginx reverse proxy"

---

## Tips for Different Content Types

### For Concepts

- Start with simple definition
- Build up complexity gradually
- Use analogies to familiar ideas
- Include diagrams if helpful

### For Workflows

- Step-by-step breakdown
- Screenshot or ASCII diagram
- Common pitfalls at each step
- Alternative approaches

### For Tools/Commands

- Basic syntax first
- Common use cases
- Comparison with alternatives
- Tips and tricks section

### For Debugging Sessions

- Original problem statement
- Investigation steps taken
- Root cause discovered
- Solution implemented
- How to prevent in future

---

## Customization

This skill supports customization via `config.yaml`:

```yaml
# Customize which sections to include
sections:
  - key_concepts
  - new_learnings
  - practical_examples

# Organize by category
organize_by_category: true
categories:
  - programming
  - devops
  - architecture
```

Adjust based on your learning style and needs!
