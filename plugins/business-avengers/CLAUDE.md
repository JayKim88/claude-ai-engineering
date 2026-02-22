# Business Avengers - Developer Guide

## Architecture Overview

Business Avengers is a multi-agent orchestration plugin that simulates a company organization for solo entrepreneurs. The SKILL.md acts as a central orchestrator that routes work to 23 AI agents (+ You as CEO = 24 roles) across 10 business phases.

### Design Philosophy

1. **Structured Document Communication** (from MetaGPT): Agents don't talk to each other. They produce structured documents that flow phase-to-phase via the orchestrator.

2. **Phase-Level Parallelism**: Within a phase, agents run in parallel where possible. Between phases, execution is sequential with CEO approval gates.

3. **Knowledge-Grounded Agents**: Each agent reads from domain-specific knowledge base files before executing, ensuring consistent quality.

4. **Sprint-Based Iteration**: Documents are versioned and tracked via changelog, supporting iterative product development.

## Directory Structure

```
plugins/business-avengers/
├── .claude-plugin/plugin.json    # Plugin metadata
├── skills/business-avengers/
│   └── SKILL.md                  # Main orchestrator (brain)
├── agents/                       # 23 agent definitions (CEO = user)
│   ├── cpo.md ... coo.md        # C-Level (5)
│   ├── product-manager.md ...    # Product (3)
│   ├── ui-designer.md            # Design (1)
│   ├── tech-lead.md ...          # Engineering (4)
│   ├── qa-lead.md                # QA (1)
│   ├── marketing-strategist.md   # Marketing (4)
│   ├── business-analyst.md ...   # Finance (2)
│   └── legal-advisor.md ...      # Operations (3)
├── templates/                    # 35+ output templates
├── knowledge/                    # 8 domain knowledge files
├── config/
│   ├── org-structure.yaml        # Organization hierarchy
│   └── init-project.py           # Project management script
├── README.md
└── CLAUDE.md (this file)
```

## Execution Flow

### Orchestra Mode (Full E2E)
```
User triggers → SKILL.md parses mode → Initialize project →
Phase 0 (dialogue) → CEO approval →
Phase 1 (3 agents parallel) → CEO approval →
Phase 2 (2 agents parallel) → CEO approval →
... →
Phase 9 (3 agents parallel) → CEO confirm →
Project complete
```

### Sprint Mode (Iteration)
```
User triggers sprint → Load project → Select phases to update →
For each phase: Read existing docs → Agent updates → Version backup →
Sprint review → CEO approval → Update project.yaml
```

### Ask Mode (Direct Agent)
```
User asks agent → SKILL.md maps to agent ID →
Load project context → Task(agent) → Display response
```

## Agent Communication Pattern

```
Phase N agents produce files → Orchestrator reads files →
Orchestrator injects file content into Phase N+1 agent prompts →
Phase N+1 agents produce files → ...
```

**Critical**: All parallel Task() calls within a phase MUST be in a single response block for true parallel execution.

## Key Components

### SKILL.md (Orchestrator)
- Parses user input to determine mode
- Manages project lifecycle (create/load/update)
- Routes work to appropriate agents per phase
- Handles CEO interaction (AskUserQuestion)
- Manages sprint cycles and version control

### Agent Files (agents/*.md)
Each agent has:
- Role description and responsibilities
- Expert frameworks and methodologies
- Communication map (who they work with)
- Output format specification
- Execution strategy (step-by-step approach)

### Templates (templates/*.md)
- Structured documents with {{PLACEHOLDER}} syntax
- Agents read templates and fill in placeholders
- Consistent output quality across runs

### Knowledge Base (knowledge/*.md)
- Domain-specific reference material
- Agents read relevant KB files before executing
- Ensures framework-based, professional output

### init-project.py
- Project CRUD operations
- Phase status management
- Document backup/versioning
- Sprint tracking

## Testing Checklist

### Basic Flow
- [ ] `/business-avengers new "test"` creates project directory
- [ ] Phase 0 interactive Q&A works
- [ ] Phase 1 runs 3 agents in parallel
- [ ] Each phase produces expected output files
- [ ] CEO approval gates work (approve/revise/pivot/stop)
- [ ] Project.yaml updates correctly after each phase

### Sprint Flow
- [ ] `/business-avengers sprint "change"` loads existing project
- [ ] Agents read existing documents before updating
- [ ] History backup is created before overwrite
- [ ] Changelog is updated
- [ ] Version numbers increment correctly

### Direct Ask
- [ ] `/business-avengers ask cto "question"` routes correctly
- [ ] Agent has project context if project exists
- [ ] Response is professional and actionable

### Edge Cases
- [ ] Resume after mid-phase interruption
- [ ] Project with missing phase outputs
- [ ] Invalid agent name in ask mode
- [ ] Network failure during WebSearch

## Model Selection

All agents use `sonnet` for optimal quality/speed/cost balance. The orchestrator (SKILL.md) runs on whatever model the user has configured.

## Cost Profile (Claude Max)

No additional API cost. All Task() subagent calls are included in Max subscription.
Estimated time per full E2E run: 30-50 minutes (processing) + 30-60 minutes (CEO interaction).

## Future Enhancements

- [ ] v2.0: Development agents generate actual code (React + Python)
- [ ] v2.1: Design agents generate HTML/CSS mockups
- [ ] v3.0: Multi-project portfolio management
- [ ] v4.0: Deployment automation (Vercel/AWS integration)
- [ ] v5.0: Direct agent-to-agent communication (pending Claude Code feature)
