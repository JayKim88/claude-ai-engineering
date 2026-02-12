# Competitive Agents - Development Guide

## Directory Structure

```
plugins/competitive-agents/
├── .claude-plugin/plugin.json        # Metadata
├── agents/
│   ├── generator-alpha.md            # Pragmatist generator
│   ├── generator-beta.md             # Architect generator
│   ├── cross-reviewer.md             # Rubric-based reviewer
│   ├── improver.md                   # Critique-based improver
│   ├── judge.md                      # Final evaluator (opus)
│   └── fuser.md                      # A+B merger
├── skills/competitive-agents/
│   └── SKILL.md                      # Orchestration algorithm
├── templates/
│   ├── evaluation-rubric.md          # Scoring criteria (100pt)
│   └── plugin-conventions.md         # Format reference for generators
├── commands/compete/compete.md       # /compete command
├── README.md
└── CLAUDE.md                         # This file
```

## Execution Flow

```
Step 1:  Parse mission + collect conventions
Step 2:  Build shared context (read reference plugins)
Step 3:  PARALLEL: generator-alpha + generator-beta (sonnet x2)
Step 4:  Save v1 outputs to agent-a/v1/ and agent-b/v1/
Step 5:  PARALLEL: cross-reviewer x2 (sonnet x2)
Step 6:  Display review summary → user confirms continue
Step 7:  PARALLEL: improver x2 (sonnet x2)
Step 8:  Save v2 → [Optional Round 2: repeat Steps 5-7 → v3]
Step 9:  judge evaluation (opus x1)
Step 10: User decision: Use A / Use B / Fuse / Keep both
Step 11: Execute decision → save to final/
Step 12: Completion summary
```

## Agent Responsibilities

| Agent | Role | Model | When |
|-------|------|-------|------|
| generator-alpha | Generate with simplicity focus | sonnet | Phase 1 |
| generator-beta | Generate with completeness focus | sonnet | Phase 1 |
| cross-reviewer | Score and critique one implementation | sonnet | Phase 2 |
| improver | Refine based on critique | sonnet | Phase 3 |
| judge | Compare both finals, declare winner | opus | Phase 4 |
| fuser | Merge best of both | sonnet | Phase 5 (optional) |

## Key Design Decisions

### Why Two Philosophies?
Same-model agents given identical prompts converge to similar outputs. Fixed philosophical lenses (Pragmatist vs Architect) create genuine design tension across multiple dimensions: file count, architecture, error handling, documentation depth, and model selection.

### Why Opus for Judge Only?
The judge needs the highest reasoning quality to make fair comparisons. Generation and review work well with sonnet. This keeps costs reasonable while ensuring evaluation quality.

### Why Save Every Version?
The v1/, v2/, v3/ structure preserves the improvement trajectory. Users can compare versions to understand what changed and why. Critiques and changelogs provide traceability.

## Parallel Execution Rules

**Must be in single response block** (parallel):
- Step 3: generator-alpha + generator-beta
- Step 5: cross-reviewer (Alpha) + cross-reviewer (Beta)
- Step 7: improver (Alpha) + improver (Beta)

**Must be sequential** (depends on previous):
- Step 9: judge (needs both final versions)
- Step 11: fuser (needs judge report + both versions)

## Testing Checklist

- [ ] `npm run link` creates symlinks for skill + 6 agents + command
- [ ] Trigger phrase "compete" activates the skill
- [ ] `/compete` command works
- [ ] Both generators produce parseable `=== FILE: ===` output
- [ ] Cross-reviewer produces scores and critique
- [ ] Improver addresses critical issues
- [ ] Judge produces weighted scores
- [ ] Fuser creates coherent merged output
- [ ] All files save to correct directories under tempo/

## Future Enhancements

- [ ] Support non-plugin generation (e.g., React components, API endpoints)
- [ ] Add a "coaching" mode where agents see each other's v1 before generating v2
- [ ] Configurable philosophies (user defines the two lenses)
- [ ] Tournament mode (4+ agents, bracket elimination)
- [ ] History tracking across missions for agent performance trends
