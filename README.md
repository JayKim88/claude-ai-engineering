# Claude AI Engineering Toolkit

A curated collection of **18 Claude Code plugins** featuring skills, agents, and multi-agent workflows — from solo developer productivity tools to full business automation pipelines.

## Plugins

### Business & Product

| Plugin | Description | Agents | Key Feature |
|--------|------------|--------|-------------|
| [**business-avengers**](./plugins/business-avengers/) | AI partner organization for solo entrepreneurs | 23 | Full business lifecycle: idea to revenue with sprint cycles |
| [**planning-interview**](./plugins/planning-interview/) | Adaptive product planning interviews | 1 | Generates Lean Canvas / Product Brief / Full PRD |
| [**spec-interview**](./plugins/spec-interview/) | AI-driven requirements gathering | 1 | Deep Q&A to comprehensive specifications |
| [**future-architect**](./plugins/future-architect/) | Thought organization to actionable plans | 1 | Conversational interviews with Mermaid diagrams |

### Development & Quality

| Plugin | Description | Agents | Key Feature |
|--------|------------|--------|-------------|
| [**project-insight**](./plugins/project-insight/) | Multi-agent project analysis | 4 | Tech stack, structure, docs review with health scoring |
| [**competitive-agents**](./plugins/competitive-agents/) | Dual-agent competitive generation | 7 | Alpha vs Beta, cross-review, judge, fusion |
| [**spec-validator**](./plugins/spec-validator/) | Validate code against specs | 1 | YAML checklists with 4-dimension scoring |

### Content & Learning

| Plugin | Description | Agents | Key Feature |
|--------|------------|--------|-------------|
| [**learning-summary**](./plugins/learning-summary/) | Capture learnings from conversations | 1 | Structured markdown with git integration |
| [**ai-digest**](./plugins/ai-digest/) | Digest AI/tech articles | 1 | URL fetch to structured learning documents |
| [**ai-news-digest**](./plugins/ai-news-digest/) | AI news aggregation | 1 | Multi-source RSS to curated Top 5 digest |
| [**blog-generator**](./plugins/blog-generator/) | Technical notes to blog posts | 1 | Narrative flow with SEO optimization |

### Finance & Investment

| Plugin | Description | Agents | Key Feature |
|--------|------------|--------|-------------|
| [**market-pulse**](./plugins/market-pulse/) | Financial market analysis dashboard | 5 | Graham/Lynch/Buffett analysis + safety margin |
| [**portfolio-analyzer-fused**](./plugins/portfolio-analyzer-fused/) | Multi-agent portfolio management | 5 | Stock scoring, risk analytics, AI advisor |
| [**portfolio-copilot**](./plugins/portfolio-copilot/) | Portfolio tracking with dashboards | 1 | P&L tracking, comprehensive stock scoring |
| [**factor-lab**](./plugins/factor-lab/) | Quantitative stock screening | 2 | Multi-factor backtesting + systematic strategies |
| [**rich-guide**](./plugins/rich-guide/) | Personalized wealth strategy system | 6 | Financial diagnosis to expert-matched roadmap (Korean) |

### Career

| Plugin | Description | Agents | Key Feature |
|--------|------------|--------|-------------|
| [**career-compass**](./plugins/career-compass/) | AI-powered career path analysis | 8 | Resume analysis, market trends, skill gap, roadmap |
| [**jd-analyzer**](./plugins/jd-analyzer/) | Job description analysis | 3 | Multi-source JD collection + skill matching |

---

## Quick Start

### Install via npx

```bash
# Install all plugins
npx github:JayKim88/claude-ai-engineering

# Install specific plugin
npx github:JayKim88/claude-ai-engineering business-avengers
npx github:JayKim88/claude-ai-engineering market-pulse

# List available plugins
npx github:JayKim88/claude-ai-engineering --list
```

### Local Development

```bash
git clone https://github.com/JayKim88/claude-ai-engineering.git
cd claude-ai-engineering
npm run link    # Symlink all plugins to Claude Code
```

Edit files in `plugins/` — changes reflect immediately in Claude Code.

---

## Repository Structure

```
claude-ai-engineering/
├── plugins/                    # 18 self-contained plugins
│   ├── business-avengers/     #   23-agent business pipeline
│   ├── planning-interview/    #   PRD generation
│   ├── project-insight/       #   Multi-agent project analysis
│   ├── competitive-agents/    #   Dual-agent generation
│   ├── market-pulse/          #   Financial market dashboard
│   ├── career-compass/        #   8-agent career analysis
│   ├── rich-guide/            #   6-agent wealth strategy
│   └── ...                    #   11 more plugins
├── templates/                  # Plugin creation templates
│   ├── plugin-template/
│   └── NEW_PLUGIN_GUIDE.md
├── projects/                   # Skill execution outputs
├── scripts/
│   └── link-local.sh
├── bin/
│   └── install.js             # npx installer
└── .claude-plugin/
    └── marketplace.json       # Plugin registry
```

---

## Plugin Patterns

### Pattern 1: Simple Skill

Single skill with direct user interaction.

**Examples:** learning-summary, ai-digest, blog-generator

### Pattern 2: Multi-Agent Pipeline

Parallel agents followed by synthesis/validation phase.

**Examples:** project-insight (4 agents), career-compass (8 agents)

```
Phase 1 (Parallel)          Phase 2 (Sequential)
┌─────────────┐             ┌─────────────┐
│  Agent A    │────┐        │             │
├─────────────┤    ├───────▶│  Synthesizer│
│  Agent B    │────┤        │             │
├─────────────┤    │        └─────────────┘
│  Agent C    │────┘
└─────────────┘
```

### Pattern 3: Competitive Generation

Two agents compete, then cross-review, improve, judge, and fuse.

**Example:** competitive-agents (7 agents across 5 rounds)

### Pattern 4: Orchestrated Organization

CEO-led multi-department pipeline with approval gates and sprint cycles.

**Example:** business-avengers (23 agents, 10 phases)

---

## Creating New Plugins

```bash
cp -r templates/plugin-template plugins/your-plugin-name
# Customize files (see templates/NEW_PLUGIN_GUIDE.md)
npm run link
```

See **[templates/NEW_PLUGIN_GUIDE.md](./templates/NEW_PLUGIN_GUIDE.md)** for the full guide.

---

## Contributing

1. Follow existing plugin patterns and structure
2. Include README.md (user) + CLAUDE.md (developer)
3. Test locally (`npm run link`)
4. Update marketplace.json
5. Commit with conventional commits

---

## Author

**Jay Kim** — [@JayKim88](https://github.com/JayKim88)

## License

MIT
