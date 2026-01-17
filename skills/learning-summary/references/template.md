# Learning Note Template

This is the standard template for learning summary documents.

---

## Example 1: Technical Concept Learning

```markdown
# Understanding Claude Code Marketplaces and Plugins

## Key Concepts

### 1. Marketplace

**Marketplace = GitHub Repository**

Claude Code's marketplace is a decentralized system.

| Feature | Description |
|---------|-------------|
| **Type** | Decentralized (similar to npm, pip) |
| **Creation** | GitHub repo + `.claude-plugin/marketplace.json` |
| **Approval** | No Anthropic approval required |

### 2. Plugin vs Marketplace

- **Marketplace**: Catalog containing multiple plugins
- **Plugin**: Individual extension providing specific functionality

## New Learnings

### Before: Misconceptions
- Thought marketplace = Anthropic-operated central store
- Believed plugins require marketplace registration

### After: Reality
- Marketplaces are decentralized, anyone can create
- 3 plugin installation methods (marketplace, npx, symlink)

## Practical Examples

### Example 1: Using Marketplace

```bash
# Connect marketplace
/plugin marketplace add team-attention/plugins-for-claude-natives

# Install plugin
/plugin install agent-council
```

### Example 2: Direct install via npx

```bash
npx github:team-attention/agent-council
```

## Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| Marketplace = Central store | Decentralized, anyone can create |
| `/plugin marketplace add` = I'm publishing | Connecting someone else's marketplace to my local Claude Code |

## References

### File Locations
- **Marketplace definition**: `~/.claude-plugin/marketplace.json`
- **Skills location**: `~/.claude/skills/`

### GitHub Repositories
- https://github.com/team-attention/plugins-for-claude-natives

## Next Steps

1. Use learning-summary skill regularly
2. Explore other plugins (agent-council, clarify)
3. Create custom skills
```

---

## Example 2: Programming Technique Learning

```markdown
# Understanding Python Async/Await Patterns

## Key Concepts

### 1. What is Asynchronous Programming?

Programming pattern that allows multiple operations to run concurrently

| Concept | Description |
|---------|-------------|
| **async** | Keyword to define async function |
| **await** | Wait for async operation to complete |
| **asyncio** | Python's async programming library |

## New Learnings

### Before
- Thought async/await is the same as threading
- Believed all I/O operations should use async

### After
- async/await is cooperative multitasking (different from threads)
- Only useful for I/O-bound operations (CPU-bound needs multiprocessing)

## Practical Examples

### Synchronous vs Asynchronous Comparison

```python
# Synchronous (sequential execution)
def fetch_data():
    data1 = requests.get(url1)  # Wait 1 second
    data2 = requests.get(url2)  # Wait 1 second
    return data1, data2  # Total: 2 seconds

# Asynchronous (parallel execution)
async def fetch_data():
    data1 = await aiohttp.get(url1)  # Start simultaneously
    data2 = await aiohttp.get(url2)  # Start simultaneously
    return data1, data2  # Total: 1 second
```

## Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| async = multithreading | Single-threaded execution |
| Use everywhere | Only useful for I/O-bound |
| Can call without await | Must use await |

## References

- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- Project file: `async_examples.py:45`

## Next Steps

1. Implement parallel API calls with aiohttp
2. Learn asyncio.gather() usage
3. Study error handling patterns
```

---

## Template Structure Guide

### Required Sections

1. **Key Concepts**
   - Define main concepts
   - Use tables for clarity
   - Include analogies or diagrams

2. **New Learnings**
   - Use Before/After format (recommended)
   - Specific misconception → accurate understanding

3. **Practical Examples**
   - Runnable code
   - Command examples
   - Real-world use cases

### Optional Sections

4. **Common Misconceptions**
   - Table format recommended
   - Clear contrasts

5. **References**
   - File paths (include line numbers)
   - URLs
   - Documentation links

6. **Next Steps**
   - Specific action items
   - Show priorities

---

## Formatting Tips

### Code Blocks
\`\`\`language
code here
\`\`\`

### Tables
| Header 1 | Header 2 |
|----------|----------|
| Value 1  | Value 2  |

### Emphasis
- **Bold**: Important keywords
- *Italic*: Supplementary explanations
- `code`: Commands, variable names

### Links
- External: [Title](URL)
- Files: `path/to/file.py:123` (with line number)

---

## Bilingual Support

The skill supports both English and Korean content:

### English Document
```markdown
## Key Concepts
## New Learnings
## Practical Examples
```

### Korean Document
```markdown
## 핵심 개념
## 새로 알게된 것
## 실용적 예시
```

### Mixed (Bilingual)
```markdown
## Key Concepts (핵심 개념)

**Marketplace** (마켓플레이스) = GitHub Repository
```

The `language` setting in config.yaml determines the default, but both languages are supported.
