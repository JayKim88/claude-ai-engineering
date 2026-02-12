---
description: Orchestrate competing agents to generate higher-quality plugin implementations
allowed-tools: Read, Write, Bash, Glob, Grep, Task, AskUserQuestion, TodoWrite
---

# /compete Command

Launch the competitive agents pipeline. Two agents with different philosophies generate competing implementations, cross-review each other, and a judge evaluates the results.

## Usage

```
/compete [mission description]
/compete --spec path/to/spec.md
/compete --improve existing-plugin-name
```

## Execution

When this command is invoked, automatically trigger the `competitive-agents` skill with the provided arguments as the mission input.
