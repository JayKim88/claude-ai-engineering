# Wrap Up Plugin

Session work history and todo tracker. Records what was done and what's next into a per-project file.

## Quick Start

1. Work on your project in a Claude Code session
2. Run `/wrap-up` at the end of the session
3. File is created/updated at `wrap-up/{project-name}.md`
4. Next session: `/wrap-up` appends to the same file

## Key Behavior

- **One file per project**: `wrap-up/{project-name}.md`
- **Accumulates**: Each session adds a new entry, never overwrites
- **Continuity**: Tracks which previous Next items were completed
- **No questions**: Analyzes conversation and generates directly
