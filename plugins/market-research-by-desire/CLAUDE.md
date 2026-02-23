# Market Research by Desire - Developer Guide

## Quick Start

```bash
# Test the plugin
claude "욕망 기반 시장조사"
```

## Directory Structure

```
market-research-by-desire/
├── .claude-plugin/plugin.json          # Plugin manifest
├── skills/market-research-by-desire/   # Main skill orchestrator
├── agents/                             # 5 agent definitions (read by general-purpose subagents)
├── knowledge/                          # 4 knowledge files (framework, methods, assessment)
├── templates/                          # 3 output templates (structural guides for final docs)
├── commands/                           # Slash command definition
├── config/settings.yaml                # Tunable parameters
├── README.md                           # User documentation
└── CLAUDE.md                           # This file
```

## Agent Architecture

All agents run as `general-purpose` subagents via Task(). Each reads its definition from `agents/` directory.

| Agent | File | Role | Key Tools |
|-------|------|------|-----------|
| desire-cartographer | `agents/desire-cartographer/` | Desire → market structure, search terms | Read |
| market-trend-researcher | `agents/market-trend-researcher/` | TAM/SAM/SOM, trends via WebSearch | Read, WebSearch, WebFetch |
| competitive-scanner | `agents/competitive-scanner/` | Competitors, pricing, SWOT | Read, WebSearch, WebFetch |
| gap-opportunity-analyzer | `agents/gap-opportunity-analyzer/` | Gaps, positioning, solo-dev filter | Read |
| revenue-model-architect | `agents/revenue-model-architect/` | Revenue models, unit economics | Read, WebSearch |

## Execution Flow

1. SKILL.md orchestrates: interview → launch agents → generate documents
2. **Phase 1 (Parallel):** 2 Task() calls in single response block
3. **Phase 2 (Sequential):** competitive-scanner → gap-opportunity-analyzer
4. **Phase 3 (Solo):** revenue-model-architect
5. **Document generation:** Read templates as structural guides, read artifact JSONs, write final docs

## Document Generation (Step 7)

Templates in `templates/` serve as **structural guides**, not literal template files:
1. Read the template to understand section structure and required content
2. Read relevant artifact JSON files for actual data
3. Write final markdown document with data populated into the template structure
4. Mark missing data as "데이터 없음 — 추가 리서치 필요"

## Testing Checklist

- [ ] Interview accepts all 5 desire categories (4 options + Other)
- [ ] Output directory created at ~/.market-research-by-desire/projects/
- [ ] Phase 1 agents run in parallel
- [ ] All 5 agents complete without timeout
- [ ] 3 final documents generated with Korean content
- [ ] Solo-dev filtering works when enabled
- [ ] Blue ocean scenario handled (no competitors found)

## Common Issues

- **Agents run sequentially:** Ensure both Phase 1 Task() calls are in the same response block
- **Korean encoding broken:** Ensure UTF-8 in Write tool calls
- **Missing market data:** Check proxy market technique in market-research-methods.md
- **Agent timeout:** Reduce scope in config/settings.yaml

## Future Enhancements

- [ ] Integration with Business Avengers for MVP planning
- [ ] Multi-language output
- [ ] Desire taxonomy expansion (Level 4 nano-desires)
- [ ] Real-time market data API integration
