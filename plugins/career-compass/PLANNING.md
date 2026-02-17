# Career Compass - Multi-Agent Pipeline 기획안

## Context

사용자가 자신의 경력을 바탕으로 앞으로의 커리어 패스를 분석하고 추천받을 수 있는 에이전트 시스템이 필요합니다.

**현재 상태**:
- `jd-analyzer` 플러그인 존재 (JD 수집, 스킬 매칭, 갭 분석)
- JD 중심의 분석만 제공 (어느 회사 지원할지, 어떤 스킬 배울지)

**요구사항**:
- 경력 중심의 분석 (현재 경력 → 가능한 커리어 패스)
- 복수의 커리어 패스 제안 (단일 답변이 아닌 선택지)
- 구체적인 학습 로드맵 (월별, 단계별)
- 전략적 조언 (네트워킹, 포트폴리오, 리스크 관리)

**참고 프로젝트**: oh-my-opencode의 multi-agent 아키텍처
- Sisyphus (orchestrator), Prometheus (planner), Oracle (advisor)
- Category-based delegation
- Tool restrictions per agent
- Background task support for parallel execution

**Claude Code 환경 적용**:
- 커스텀 sub-agent를 `.md` 파일로 정의
- `~/.claude/agents/`에 symlink 등록
- `Task(subagent_type="agent-name")` 방식으로 호출
- Claude 모델만 사용 (opus, sonnet, haiku)

---

## 아키텍처: Claude Code 환경 적용

### 핵심 원칙

```
oh-my-opencode의 설계 철학 (Claude Code로 구현):
1. "You NEVER work alone when specialists are available"
   → 각 역할별 전문 agent를 .md로 정의

2. "Planning ≠ Doing" (Planner와 Executor 분리)
   → SKILL.md가 orchestrator, agents/*.md가 executor

3. Parallel execution for maximum throughput
   → 단일 응답에 여러 Task 호출로 병렬 실행

4. Category-based delegation
   → Agent 정의에 role을 명확히 기술

5. Background tasks for independent work
   → Task(run_in_background=true) 활용 가능
```

### Multi-Agent 구조

```
SKILL.md (Orchestrator - Prometheus 패턴)
  │
  ├─ Step 1: AskUserQuestion (Interview Mode)
  │    - 목표 직무 확인
  │    - 전환 기간 합의
  │    - 학습 가능 시간 파악
  │
  ├─ Step 2: Phase 1 Analysis (병렬 3개 Task)
  │    ├─ Task(subagent_type="resume-analyzer")        [Sonnet]
  │    ├─ Task(subagent_type="jd-market-analyzer")     [Sonnet]
  │    └─ Task(subagent_type="career-trend-researcher") [Opus]
  │
  ├─ Step 3: Phase 2 Path Generation (병렬 3개 Task)
  │    ├─ Task(subagent_type="skill-gap-analyzer")     [Sonnet]
  │    ├─ Task(subagent_type="career-path-generator")  [Opus]
  │    └─ Task(subagent_type="salary-projector")       [Haiku]
  │
  ├─ Step 4: AskUserQuestion (Path Selection)
  │
  └─ Step 5: Phase 3 Synthesis (순차 2개 Task)
       ├─ Task(subagent_type="roadmap-generator")      [Sonnet]
       └─ Task(subagent_type="strategy-advisor")       [Opus]
```

**Phase 다이어그램**:
```
Phase 1: PARALLEL ANALYSIS
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Resume       │  │ JD Market    │  │ Career Trend │
│ Analyzer     │  │ Analyzer     │  │ Researcher   │
│ (Sonnet)     │  │ (Sonnet)     │  │ (Opus)       │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └──────────────────┼──────────────────┘
                          ▼
Phase 2: PARALLEL PATH GENERATION
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Skill Gap    │  │ Career Path  │  │ Salary       │
│ Analyzer     │  │ Generator    │  │ Projector    │
│ (Sonnet)     │  │ (Opus)       │  │ (Haiku)      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └──────────────────┼──────────────────┘
                          ▼
         [User Selects Path via AskUserQuestion]
                          ▼
Phase 3: SEQUENTIAL SYNTHESIS
        ┌──────────────────────────────┐
        │ Learning Roadmap Generator   │
        │ (Sonnet)                     │
        └──────────┬───────────────────┘
                   ▼
        ┌──────────────────────────────┐
        │ Strategy Advisor (Final)     │
        │ (Opus)                       │
        └──────────────────────────────┘
```

---

## Agent 상세 설계 (Markdown Frontmatter 방식)

### 1. resume-analyzer.md

**파일**: `agents/resume-analyzer.md`

```markdown
---
name: resume-analyzer
description: Analyze user's career history and extract insights
tools: ["Read", "Grep", "Glob"]
model: sonnet
color: blue
---

# Resume Analyzer Agent

## Responsibilities
경력 사항 심층 분석 (Sisyphus-Junior 패턴)

1. Load profile from ~/.jd-analyzer/profile.yaml
2. Extract career timeline (예: Frontend 4yr → AI/ML 2yr)
3. Classify skills by proficiency (Expert/Advanced/Learning)
4. Identify career transition patterns
5. Detect strengths and weaknesses

## Analysis Strategy

### Input Sources
- Primary: `~/.jd-analyzer/profile.yaml`
- Optional: `~/Documents/resume.pdf`

### Analysis Steps
1. **Timeline Extraction**: Parse years_experience per domain
2. **Skill Categorization**: Group by proficiency level
3. **Pattern Detection**: Identify career transitions
4. **Gap Analysis**: Compare current vs target skills

## Output Format

```json
{
  "total_years": 6,
  "domains": {
    "frontend": 4,
    "ai_ml": 2
  },
  "strengths": ["React", "TypeScript", "Claude AI"],
  "weaknesses": ["Backend", "DevOps"],
  "transition_pattern": "Frontend → AI Product Engineer",
  "key_skills": {
    "expert": ["React", "JavaScript"],
    "advanced": ["TypeScript", "Python"],
    "learning": ["LLM", "RAG"]
  }
}
```

## Constraints
- ONLY use Read, Grep, Glob tools
- DO NOT modify any files
- Focus on FACTUAL analysis only (no recommendations)
- If profile.yaml not found, ask user to run jd-analyzer first
```

---

### 2. jd-market-analyzer.md

**파일**: `agents/jd-market-analyzer.md`

```markdown
---
name: jd-market-analyzer
description: Analyze job market trends from JD data
tools: ["Read", "Grep", "Glob"]
model: sonnet
color: green
---

# JD Market Analyzer Agent

## Responsibilities
JD 데이터 분석 (기존 jd-analyzer 활용)

1. Load JD analysis results from ~/.jd-analyzer/
2. Extract top 20 in-demand skills
3. Compare with user's current skills
4. Identify critical skill gaps
5. Analyze market trends (YoY growth, remote work ratio)

## Analysis Strategy

### Input Sources
- `~/.jd-analyzer/jds.json` - Raw JD data
- `~/.jd-analyzer/matches.json` - Skill matching results
- `~/.jd-analyzer/analysis_report.md` - Previous analysis

### Analysis Steps
1. **Skill Frequency**: Count skill mentions across all JDs
2. **Demand Trends**: Identify growing/declining skills
3. **Gap Identification**: Skills in JDs but not in user profile
4. **Market Insights**: Remote work ratio, salary ranges

## Output Format

```json
{
  "top_demanded": [
    {"skill": "Python", "count": 78, "growth": "+15%"},
    {"skill": "Docker", "count": 65, "growth": "+22%"}
  ],
  "matched_skills": ["React", "TypeScript", "Git"],
  "critical_gaps": ["Python", "Docker", "Kubernetes"],
  "nice_to_have_gaps": ["AWS", "CI/CD"],
  "market_trends": {
    "ai_ml_growth": "+35% YoY",
    "remote_ratio": "68%",
    "avg_salary": "$120-150k"
  }
}
```

## Constraints
- ONLY use Read, Grep, Glob tools
- DO NOT run jd-analyzer (assume data exists)
- If data missing, inform orchestrator to run jd-analyzer first
```

---

### 3. career-trend-researcher.md

**파일**: `agents/career-trend-researcher.md`

```markdown
---
name: career-trend-researcher
description: Research career transition cases and learning resources via web
tools: ["WebSearch", "WebFetch", "Read"]
model: opus
color: purple
---

# Career Trend Researcher Agent

## Responsibilities
웹 트렌드 조사 및 전환 사례 연구 (Oracle 패턴 - 전략적 사고)

1. Search for career transition success cases
2. Collect 3-5 real-world examples
3. Extract common patterns (필수 스킬, 소요 기간)
4. Gather curated learning resources
5. Identify emerging trends in target role

## Research Strategy

### Search Queries
- "Frontend to AI Engineer transition 2026"
- "Career change to [target_role] success stories"
- "[target_role] learning path 2026"
- "Best courses for [target_role] beginners"

### Analysis Focus
1. **Success Cases**: Duration, background, key skills learned
2. **Common Patterns**: Shared characteristics across cases
3. **Learning Resources**: Courses, books, projects
4. **Emerging Skills**: New technologies in target domain

## Output Format

```json
{
  "success_cases": [
    {
      "from": "Frontend Developer",
      "to": "AI Engineer",
      "duration": "12-18 months",
      "key_skills_learned": ["Python", "ML Fundamentals", "LLM APIs"],
      "advice": "Start with Python, then ML basics, finally LLM projects"
    }
  ],
  "common_patterns": {
    "avg_duration": "12-18 months",
    "critical_skills": ["Python", "ML", "LLM"],
    "success_factors": ["Consistent learning", "Portfolio projects"]
  },
  "learning_resources": {
    "courses": ["DeepLearning.AI", "FastAPI Tutorial"],
    "books": ["Hands-On Machine Learning"],
    "projects": ["Build a RAG chatbot", "Fine-tune an LLM"]
  },
  "emerging_trends": ["Multi-modal AI", "AI agents", "Prompt engineering"]
}
```

## Constraints
- USE WebSearch, WebFetch for research
- DO NOT make up data - cite sources
- Focus on RECENT information (2025-2026)
- Limit to 3-5 high-quality cases (avoid spam)
```

---

### 4. skill-gap-analyzer.md

**파일**: `agents/skill-gap-analyzer.md`

```markdown
---
name: skill-gap-analyzer
description: Synthesize Phase 1 results and prioritize skill gaps
tools: ["Read"]
model: sonnet
color: yellow
---

# Skill Gap Analyzer Agent

## Responsibilities
Phase 1 결과 통합 및 스킬 갭 우선순위 분석

1. Merge outputs from Phase 1 (resume, JD, trends)
2. Classify gaps: Critical vs Nice-to-have
3. Estimate learning difficulty (1-5 scale)
4. Calculate ROI: (market_demand / learning_difficulty)
5. Generate prioritized learning list

## Analysis Strategy

### Input
Receives 3 JSON outputs from Phase 1:
- `resume_analysis` - User's current skills
- `jd_market_analysis` - Market demand data
- `career_trends` - Industry trends

### Analysis Steps
1. **Gap Identification**: Skills in market/trends but not in resume
2. **Classification**:
   - Critical: Required by >50% of JDs
   - Nice-to-have: Beneficial but not required
3. **Difficulty Scoring**: Based on prerequisite knowledge
4. **ROI Calculation**: Prioritize high-demand, low-difficulty first

## Output Format

```json
{
  "critical_gaps": [
    {
      "skill": "Python",
      "difficulty": 3,
      "demand_score": 78,
      "roi": 26.0,
      "prerequisite": "Programming basics (already have)",
      "estimated_time": "2-3 months"
    }
  ],
  "nice_to_have": [
    {
      "skill": "Kubernetes",
      "difficulty": 4,
      "demand_score": 45,
      "roi": 11.25
    }
  ],
  "prioritized_learning": [
    "1. Python (high ROI, foundational)",
    "2. LLM APIs (high demand, medium difficulty)",
    "3. Docker (prerequisite for K8s)"
  ]
}
```

## Constraints
- ONLY use Read tool (receives data via prompt)
- Focus on ACTIONABLE insights
- Provide clear rationale for prioritization
```

---

### 5. career-path-generator.md

**파일**: `agents/career-path-generator.md`

```markdown
---
name: career-path-generator
description: Generate 3-5 possible career paths with creative thinking
tools: ["Read"]
model: opus
color: purple
---

# Career Path Generator Agent

## Responsibilities
가능한 커리어 패스 3-5개 생성 (Opus - 창의성 필요)

1. Analyze current career → target role gap
2. Generate 3-5 distinct possible paths:
   - Direct transition (fastest)
   - Gradual transition (safest)
   - Lateral transition (alternative)
3. Assess pros/cons per path
4. Estimate success probability (based on market data)
5. Provide realistic timeline per path

## Path Generation Strategy

### Input
All Phase 1-2 results (resume, market, trends, gaps)

### Path Types
1. **Direct Path**: Current → Target (shortest, steepest)
2. **Gradual Path**: Current → Intermediate → Target (safer)
3. **Lateral Path**: Current → Adjacent → Target (alternative route)
4. **Hybrid Path**: Part-time learning + current job
5. **Bootcamp Path**: Intensive program-based transition

### Evaluation Criteria
- **Feasibility**: Given user's background and constraints
- **Duration**: Realistic timeline estimate
- **Success Rate**: Based on market data and trends
- **Risk**: Job security, financial impact

## Output Format

```json
{
  "paths": [
    {
      "id": 1,
      "title": "Direct AI Engineer Transition",
      "type": "direct",
      "steps": [
        "Master Python (3 months)",
        "Learn ML fundamentals (3 months)",
        "Build LLM projects (6 months)",
        "Apply to AI Engineer roles"
      ],
      "duration": "12-18 months",
      "success_rate": 70,
      "pros": [
        "Fastest route",
        "Clear learning path",
        "High demand for AI engineers"
      ],
      "cons": [
        "Steep learning curve",
        "Career gap if quitting job",
        "Competitive field"
      ],
      "best_for": "Self-motivated learners with 10+ hrs/week"
    },
    {
      "id": 2,
      "title": "AI Product Engineer (Gradual)",
      "type": "gradual",
      "steps": [
        "Add Python to current frontend stack",
        "Build AI-powered features in current job",
        "Transition to AI-focused product role",
        "Deepen ML skills over time"
      ],
      "duration": "18-24 months",
      "success_rate": 85,
      "pros": [
        "Lower risk (no career gap)",
        "Leverage existing frontend skills",
        "Gradual skill building"
      ],
      "cons": [
        "Slower transition",
        "Requires supportive employer",
        "May need to change companies eventually"
      ],
      "best_for": "Risk-averse learners with family obligations"
    }
  ],
  "recommendation": {
    "suggested_path": 1,
    "rationale": "Based on user's AI/ML interest and 2 years experience"
  }
}
```

## Constraints
- Generate REALISTIC paths (no fantasy scenarios)
- Base estimates on actual market data from Phase 1
- Consider user's constraints (time, financial)
- Provide 3-5 paths minimum (give options)
```

---

### 6. salary-projector.md

**파일**: `agents/salary-projector.md`

```markdown
---
name: salary-projector
description: Project salary ranges and calculate ROI for each path
tools: ["WebSearch", "Read"]
model: haiku
color: green
---

# Salary Projector Agent

## Responsibilities
연봉 예측 및 ROI 계산 (Haiku - 빠른 데이터 처리)

1. Search current salary data for target roles
2. Project salary after transition per path
3. Calculate ROI: (salary_increase / time_investment)
4. Regional salary comparison (if applicable)
5. Factor in cost of learning (courses, bootcamps)

## Projection Strategy

### Data Sources
- WebSearch: "AI Engineer salary 2026"
- WebSearch: "[target_role] salary range [location]"
- Market data from Phase 1

### Calculation
```
ROI = (Target Salary - Current Salary - Learning Costs) / Months of Transition
```

## Output Format

```json
{
  "current_salary_estimate": "$80-100k (Frontend Developer)",
  "path_projections": [
    {
      "path_id": 1,
      "path_name": "Direct AI Engineer Transition",
      "target_salary": "$120-150k",
      "increase": "+50-87%",
      "duration_months": 15,
      "learning_costs": "$2,000 (courses)",
      "monthly_roi": "$2,667",
      "roi_rating": "High",
      "breakeven_months": 6
    }
  ],
  "regional_comparison": {
    "san_francisco": "$150-200k",
    "remote_us": "$120-150k",
    "europe": "€70-90k"
  },
  "notes": [
    "Salaries based on 2026 market data",
    "Remote roles typically 10-20% lower than SF",
    "Senior AI Engineer can reach $200k+ after 2-3 years"
  ]
}
```

## Constraints
- USE WebSearch for latest salary data
- Provide REALISTIC ranges (not marketing hype)
- Include learning costs in ROI calculation
- Note data sources and recency
```

---

### 7. roadmap-generator.md

**파일**: `agents/roadmap-generator.md`

```markdown
---
name: roadmap-generator
description: Generate detailed month-by-month learning roadmap
tools: ["Read", "Write"]
model: sonnet
color: blue
---

# Learning Roadmap Generator Agent

## Responsibilities
선택된 패스의 구체적 학습 로드맵 생성

1. Generate month-by-month learning plan
2. Set milestones per phase (beginner → intermediate → advanced)
3. Map specific learning resources (courses, books, projects)
4. Suggest portfolio projects to demonstrate skills
5. Include review/consolidation periods

## Roadmap Structure

### Phases
1. **Foundation** (Months 1-3): Core prerequisites
2. **Skill Building** (Months 4-6): Target domain fundamentals
3. **Project Work** (Months 7-9): Apply knowledge to projects
4. **Job Prep** (Months 10-12): Portfolio, interview prep

### Per Month
- Learning goals
- Recommended resources
- Milestone project
- Expected outcomes

## Output Format

Write to file: `~/.career-compass/roadmaps/roadmap-path{id}-{date}.md`

```markdown
# Learning Roadmap: Direct AI Engineer Transition

**Selected Path**: Path 1 - Direct AI Engineer Transition
**Duration**: 12-18 months
**Generated**: 2026-02-14

---

## Phase 1: Python Fundamentals (Months 1-3)

### Month 1: Python Basics
**Goal**: Master Python syntax and core concepts

**Learning Resources**:
- Course: Python for Everybody (Coursera)
- Book: Automate the Boring Stuff with Python
- Practice: LeetCode Easy problems

**Weekly Breakdown**:
- Week 1-2: Variables, data types, control flow
- Week 3-4: Functions, modules, file I/O

**Milestone Project**: CLI tool for task automation

**Expected Outcome**: ✓ Comfortable writing Python scripts

### Month 2: Advanced Python
...

### Month 3: Python for Data Science
...

---

## Phase 2: ML Fundamentals (Months 4-6)
...
```

## Constraints
- CAN use Write tool
- ONLY write to `~/.career-compass/roadmaps/`
- ONLY create .md files
- Base roadmap on selected_path from orchestrator
- Include SPECIFIC resources (not generic "take a course")
```

---

### 8. strategy-advisor.md

**파일**: `agents/strategy-advisor.md`

```markdown
---
name: strategy-advisor
description: Provide strategic career advice and final recommendations
tools: ["Read", "Write"]
model: opus
color: purple
---

# Strategy Advisor Agent

## Responsibilities
종합 전략 조언 (Oracle 패턴 - 최종 검토 및 전략)

1. Synthesize ALL Phase 1-3 results
2. Generate executive summary
3. Create weekly/monthly action items (first 3 months)
4. Provide risk mitigation strategies
5. Suggest networking strategy
6. Recommend portfolio projects to stand out

## Strategy Areas

### 1. Executive Summary
- Current state vs target
- Selected path rationale
- Key success factors

### 2. Action Plan
- Week 1-4 immediate actions
- Month 1-3 detailed plan
- Month 4-12 milestones

### 3. Risk Management
- Identify potential obstacles
- Mitigation strategies per risk
- Plan B if primary path fails

### 4. Networking
- Communities to join
- Events to attend
- People to connect with

### 5. Portfolio Strategy
- Project ideas that demonstrate target skills
- How to showcase them (GitHub, blog, etc.)
- Interview preparation tips

## Output Format

Write to file: `~/.career-compass/strategy/strategy-{date}.md`

```markdown
# Career Strategy Report: Frontend → AI Engineer

**Generated**: 2026-02-14
**Target Role**: AI Engineer
**Timeline**: 12-18 months

---

## Executive Summary

Based on 6 years of software engineering experience (4 years frontend, 2 years AI/ML product work), you are well-positioned for a transition to AI Engineer. Your existing TypeScript and React expertise provides a strong foundation, and your recent exposure to Claude AI demonstrates genuine interest in the field.

**Key Strengths**:
- Strong programming fundamentals
- Product mindset (valuable for AI products)
- Recent AI/ML exposure

**Primary Challenge**: Bridging the gap from high-level AI usage to deep technical implementation (Python, ML algorithms, model training).

**Recommended Path**: Path 1 - Direct AI Engineer Transition (12-18 months)

---

## Immediate Action Items (First 3 Months)

### Week 1-2
- [ ] Enroll in "Python for Everybody" (Coursera)
- [ ] Set up development environment (Python, Jupyter, VS Code)
- [ ] Join r/MachineLearning and AI Discord communities

### Week 3-4
- [ ] Complete Python basics module
- [ ] Start LeetCode Easy problems (5 per week)
- [ ] Read "AI Product Management" to bridge current skills

### Month 2
- [ ] Finish Python fundamentals course
- [ ] Build CLI tool project (automate something in your workflow)
- [ ] Attend local AI meetup (search Meetup.com)

### Month 3
- [ ] Start FastAPI tutorial
- [ ] Build simple REST API with Python
- [ ] Begin DeepLearning.AI "Machine Learning Specialization"

---

## Risk Mitigation Strategies

### Risk 1: Learning burnout (steep curve)
**Mitigation**:
- Schedule fixed learning hours (not open-ended)
- Take 1 week break every 2 months
- Join study group for accountability

### Risk 2: Market saturation (too many AI engineers)
**Mitigation**:
- Specialize in niche (e.g., AI for frontend, LLM UI/UX)
- Build unique portfolio projects
- Leverage product experience (AI Product Engineer hybrid)

### Risk 3: Imposter syndrome
**Mitigation**:
- Document learning journey (blog posts)
- Celebrate small wins (monthly review)
- Remember: many AI engineers are also learning on the job

---

## Networking Strategy

### Communities to Join
1. **Online**:
   - r/MachineLearning (Reddit)
   - AI Tinkerers Discord
   - Hugging Face forums

2. **Local**:
   - AI/ML meetups in your city
   - Papers We Love reading group

3. **Professional**:
   - LinkedIn: Follow AI researchers, companies
   - Twitter/X: AI Engineering community

### Events to Attend
- NeurIPS (online attendance)
- Local AI hackathons
- Company tech talks (Google, OpenAI)

### People to Connect With
- AI engineers at target companies (informational interviews)
- Bootcamp graduates (realistic transition stories)
- AI startup founders (emerging opportunities)

---

## Portfolio Project Recommendations

### Project 1: RAG Chatbot (Months 4-6)
**Why**: Demonstrates LLM + backend skills
**Stack**: Python, LangChain, Pinecone, FastAPI
**Showcase**: Deploy on Vercel, write blog post

### Project 2: Fine-tune Open Source LLM (Months 7-9)
**Why**: Shows deep ML knowledge
**Stack**: Python, Hugging Face, LoRA, PyTorch
**Showcase**: Publish model on HF Hub

### Project 3: AI-Powered Tool (Months 10-12)
**Why**: End-to-end product (leverages your PM skills)
**Stack**: Full-stack AI app
**Showcase**: Live demo + user testimonials

---

## Success Metrics

Track these monthly:
- [ ] Courses completed
- [ ] Projects deployed
- [ ] GitHub commits (consistency)
- [ ] Community engagement (posts, answers)
- [ ] Interview invitations (after month 9)

---

## Final Thoughts

Your transition is highly feasible given your background. The key differentiator will be **consistent execution** over 12-18 months. Many start, few finish. Your product mindset is an underrated advantage in AI engineering—use it.

**Next Steps**:
1. Review the detailed roadmap file
2. Calendar block learning hours for the next 3 months
3. Take action on Week 1-2 items TODAY

Good luck! 🚀
```

## Constraints
- CAN use Write tool
- ONLY write to `~/.career-compass/strategy/`
- ONLY create .md files
- Synthesize ALL previous agent outputs
- Provide ACTIONABLE advice (not generic platitudes)
- Include SPECIFIC names (courses, communities, projects)
```

---

## 디렉토리 구조 (Claude Code 방식)

```
plugins/career-compass/
├── .claude-plugin/
│   └── plugin.json                # Plugin metadata
│
├── agents/                         # ⭐ 커스텀 sub-agent 정의 (.md)
│   ├── resume-analyzer.md         # [Sonnet] 경력 분석
│   ├── jd-market-analyzer.md      # [Sonnet] JD 시장 분석
│   ├── career-trend-researcher.md # [Opus] 웹 트렌드 조사
│   ├── skill-gap-analyzer.md      # [Sonnet] 스킬 갭 분석
│   ├── career-path-generator.md   # [Opus] 경로 생성 (창의성)
│   ├── salary-projector.md        # [Haiku] 연봉 예측 (빠름)
│   ├── roadmap-generator.md       # [Sonnet] 로드맵 생성
│   └── strategy-advisor.md        # [Opus] 전략 조언
│
├── skills/
│   └── career-compass/
│       └── SKILL.md               # ⭐ Main orchestrator
│
├── data/
│   ├── roadmaps/                  # Generated roadmaps
│   └── strategy/                  # Strategy reports
│
├── PLANNING.md                    # 이 문서
└── README.md                      # 사용자 문서

# ✅ 등록 방법
# npm run link 실행 시 자동으로:
# ~/.claude/agents/resume-analyzer.md → symlink
# ~/.claude/skills/career-compass/ → symlink
```

---

## SKILL.md 실행 알고리즘 (Orchestrator)

**파일**: `skills/career-compass/SKILL.md`

```markdown
---
name: career-compass
description: AI-powered career path analysis with multi-agent pipeline. Analyze your career, get personalized path recommendations, and receive detailed learning roadmaps.
version: 1.0.0
---

# Career Compass Skill

## Trigger Phrases
- "analyze my career"
- "career path recommendation"
- "how do I transition to [role]"
- "/career-compass"

## When to Use
- Career transition planning
- Skill gap analysis
- Learning roadmap generation
- Strategic career advice

---

## Execution Algorithm

### Step 0: Environment Check

Verify prerequisites:

```bash
# Check if jd-analyzer data exists
if [ ! -f ~/.jd-analyzer/profile.yaml ]; then
  echo "⚠️  Please run /jd-analyzer first to generate your profile"
  echo "   This provides market data for better recommendations"
  exit 1
fi

# Create data directories
mkdir -p ~/.career-compass/roadmaps
mkdir -p ~/.career-compass/strategy
```

### Step 1: Interview Mode

Gather user requirements via AskUserQuestion:

```python
AskUserQuestion(
  questions=[
    {
      "question": "What is your target role?",
      "header": "Target Role",
      "options": [
        {
          "label": "AI Engineer",
          "description": "Deep learning, model training, MLOps"
        },
        {
          "label": "AI Product Engineer",
          "description": "Build AI-powered products, LLM integration"
        },
        {
          "label": "ML Engineer",
          "description": "Production ML systems, data pipelines"
        },
        {
          "label": "Other",
          "description": "Specify custom role"
        }
      ],
      "multiSelect": false
    },
    {
      "question": "How quickly do you want to transition?",
      "header": "Timeline",
      "options": [
        {"label": "6-12 months", "description": "Intensive learning, career gap OK"},
        {"label": "12-18 months", "description": "Balanced pace (recommended)"},
        {"label": "18-24 months", "description": "Gradual, no career gap"}
      ],
      "multiSelect": false
    },
    {
      "question": "How much time can you dedicate to learning per week?",
      "header": "Study Time",
      "options": [
        {"label": "5-10 hours", "description": "Part-time learning"},
        {"label": "10-20 hours", "description": "Serious commitment"},
        {"label": "20+ hours", "description": "Full-time bootcamp mode"}
      ],
      "multiSelect": false
    }
  ]
)
```

Store responses in variables: `target_role`, `timeline`, `study_time`

---

### Step 2: Phase 1 - Parallel Analysis

**CRITICAL**: Spawn all 3 agents in a SINGLE response block for parallel execution.

```python
# Call these 3 Tasks in one response:

Task(
  subagent_type="resume-analyzer",
  model="sonnet",
  description="Analyze career history",
  prompt=f"""
  Analyze the user's career background.

  Profile location: ~/.jd-analyzer/profile.yaml

  Extract:
  1. Total years of experience
  2. Domain breakdown (years per domain)
  3. Skill proficiency levels
  4. Career transition patterns
  5. Strengths and weaknesses

  Output JSON format as defined in your agent description.
  """
)

Task(
  subagent_type="jd-market-analyzer",
  model="sonnet",
  description="Analyze JD market data",
  prompt=f"""
  Analyze job market from JD data.

  Data location: ~/.jd-analyzer/jds.json, matches.json

  Extract:
  1. Top 20 in-demand skills
  2. Skills user already has
  3. Critical skill gaps
  4. Market trends (growth rates, remote ratio)

  Output JSON format as defined in your agent description.
  """
)

Task(
  subagent_type="career-trend-researcher",
  model="opus",
  description="Research career trends",
  prompt=f"""
  Research career transition to: {target_role}

  Search for:
  1. Success cases (Frontend/similar → {target_role})
  2. Common patterns (skills, duration)
  3. Learning resources (courses, books, projects)
  4. Emerging trends in {target_role}

  Use WebSearch and WebFetch. Focus on 2025-2026 data.

  Output JSON format as defined in your agent description.
  """
)
```

**Wait for all 3 tasks to complete.** Store results in:
- `resume_result`
- `jd_market_result`
- `career_trends_result`

---

### Step 3: Phase 2 - Path Generation

**CRITICAL**: Spawn all 3 agents in a SINGLE response block.

```python
Task(
  subagent_type="skill-gap-analyzer",
  model="sonnet",
  description="Prioritize skill gaps",
  prompt=f"""
  Synthesize Phase 1 results and prioritize skills to learn.

  Input data:

  # Resume Analysis
  {resume_result}

  # JD Market Analysis
  {jd_market_result}

  # Career Trends
  {career_trends_result}

  Tasks:
  1. Identify all skill gaps
  2. Classify: Critical vs Nice-to-have
  3. Estimate difficulty (1-5)
  4. Calculate ROI (demand / difficulty)
  5. Generate prioritized list

  Output JSON format as defined.
  """
)

Task(
  subagent_type="career-path-generator",
  model="opus",
  description="Generate career paths",
  prompt=f"""
  Generate 3-5 possible career paths to: {target_role}

  Context:
  - Current background: {resume_result}
  - Market data: {jd_market_result}
  - Industry trends: {career_trends_result}
  - User timeline: {timeline}
  - Study time: {study_time}

  Generate paths:
  1. Direct transition
  2. Gradual transition
  3. Lateral transition
  4-5. Creative alternatives

  For each: steps, duration, success rate, pros/cons.

  Output JSON format as defined.
  """
)

Task(
  subagent_type="salary-projector",
  model="haiku",
  description="Project salary ranges",
  prompt=f"""
  Project salary for target role: {target_role}

  Use WebSearch to find 2026 salary data.

  Calculate ROI for each path (will receive path data).

  Include:
  - Current vs target salary
  - Regional comparison
  - Learning costs
  - Breakeven analysis

  Output JSON format as defined.
  """
)
```

**Wait for all 3 tasks.** Store results in:
- `skill_gaps_result`
- `paths_result`
- `salary_result`

---

### Step 4: User Path Selection

Present generated paths and let user choose:

```python
AskUserQuestion(
  questions=[{
    "question": "Which career path appeals to you?",
    "header": "Select Path",
    "options": [
      {
        "label": paths_result.paths[0].title,
        "description": f"{paths_result.paths[0].duration}, {paths_result.paths[0].success_rate}% success rate"
      },
      {
        "label": paths_result.paths[1].title,
        "description": f"{paths_result.paths[1].duration}, {paths_result.paths[1].success_rate}% success rate"
      },
      # ... repeat for all paths
    ],
    "multiSelect": false
  }]
)
```

Store selection in `selected_path_id`

---

### Step 5: Phase 3 - Sequential Synthesis

**CRITICAL**: Run these SEQUENTIALLY (not parallel) because roadmap depends on selected path.

#### 5.1: Generate Roadmap

```python
Task(
  subagent_type="roadmap-generator",
  model="sonnet",
  description="Generate learning roadmap",
  prompt=f"""
  Generate detailed learning roadmap for selected path.

  Selected path: {paths_result.paths[selected_path_id]}

  Skill gaps to address: {skill_gaps_result}

  User constraints:
  - Timeline: {timeline}
  - Study time: {study_time}

  Create month-by-month plan with:
  - Learning goals
  - Specific resources (courses, books)
  - Milestone projects
  - Review periods

  Write to file: ~/.career-compass/roadmaps/roadmap-path{selected_path_id}-{date}.md

  Follow the markdown format defined in your agent description.
  """
)
```

Wait for roadmap completion. Get file path: `roadmap_file`

#### 5.2: Strategic Advice

```python
Task(
  subagent_type="strategy-advisor",
  model="opus",
  description="Provide strategic advice",
  prompt=f"""
  Provide comprehensive strategic advice synthesizing all results.

  # All Input Data

  Resume: {resume_result}
  Market: {jd_market_result}
  Trends: {career_trends_result}
  Skill Gaps: {skill_gaps_result}
  Selected Path: {paths_result.paths[selected_path_id]}
  Salary: {salary_result}
  Roadmap: {roadmap_file}

  # User Context
  Target: {target_role}
  Timeline: {timeline}
  Study Time: {study_time}

  Create strategy report with:
  1. Executive summary
  2. Immediate action items (first 3 months)
  3. Risk mitigation
  4. Networking strategy
  5. Portfolio projects

  Write to: ~/.career-compass/strategy/strategy-{date}.md

  Follow the format defined in your agent description.
  Be SPECIFIC (not generic advice).
  """
)
```

Wait for strategy completion. Get file path: `strategy_file`

---

### Step 6: Present Results

Display summary to user:

```markdown
# ✅ Career Compass Analysis Complete!

## Selected Path
**{paths_result.paths[selected_path_id].title}**
- Duration: {duration}
- Success Rate: {success_rate}%

## Key Insights
- Critical skills to learn: {top 3 from skill_gaps}
- Estimated salary increase: {salary_result projection}
- First milestone: {from roadmap month 1}

## Generated Files
📄 **Learning Roadmap**: {roadmap_file}
📄 **Strategy Report**: {strategy_file}

## Next Steps
1. Review your detailed roadmap
2. Read the strategy report
3. Start with Week 1-2 action items

**Tip**: Open the strategy file now for immediate action items! 🚀
```

---

## Error Handling

### If jd-analyzer data missing:
```
⚠️  JD Analyzer data not found.

Please run: /jd-analyzer

This will:
- Collect job descriptions from LinkedIn/Wellfound
- Analyze market demand for skills
- Provide better career recommendations

Continue without JD data? (Not recommended)
```

### If agent fails:
```
❌ Agent {agent_name} failed.

Reason: {error_message}

Fallback: Continuing with partial results...
(Quality may be reduced)
```

---

## Performance Notes

- **Phase 1**: ~2-3 min (3 parallel agents)
- **Phase 2**: ~2-3 min (3 parallel agents)
- **Phase 3**: ~2 min (2 sequential agents)
- **Total**: ~6-8 minutes

**Optimization**:
- Haiku for fast data processing (salary)
- Opus for creative/strategic tasks (paths, strategy)
- Sonnet for analytical tasks (most agents)
```

---

## Tool Restrictions (Frontmatter 방식)

각 agent의 `.md` 파일 frontmatter에 정의:

```yaml
# 읽기 전용 agent (분석만)
tools: ["Read", "Grep", "Glob"]

# 웹 조사 agent
tools: ["WebSearch", "WebFetch", "Read"]

# 파일 생성 agent (결과 출력)
tools: ["Read", "Write"]
```

**보안 원칙**:
1. 분석 agent는 Read만 허용
2. 웹 조사 agent는 WebSearch/WebFetch만 추가
3. 파일 생성 agent는 Write 허용하되, prompt에서 경로 제한 명시
4. 어떤 agent도 Edit, Bash는 사용하지 않음

---

## Performance 예상

| Phase | Agents | Model | Duration | Parallel |
|-------|--------|-------|----------|----------|
| Interview | - | - | 1 min | N/A |
| Phase 1 | 3 | Sonnet×2, Opus×1 | 2-3 min | ✅ Yes |
| Phase 2 | 3 | Sonnet, Opus, Haiku | 2-3 min | ✅ Yes |
| User Select | - | - | 30 sec | N/A |
| Phase 3 | 2 | Sonnet, Opus | 2 min | ❌ Sequential |
| **Total** | **8** | - | **7-9 min** | - |

**Model Selection Strategy**:
- **Haiku**: 빠른 데이터 처리 (salary lookup)
- **Sonnet**: 대부분의 분석 작업 (정확성 + 속도 균형)
- **Opus**: 창의성 필요 (path generation, strategy advice)

---

## 차별화 포인트

### vs. 기존 jd-analyzer
| Feature | jd-analyzer | career-compass |
|---------|-------------|----------------|
| Focus | JD 중심 | 경력 중심 |
| Output | 회사 추천, 스킬 갭 | 3-5개 커리어 패스 + 로드맵 |
| Depth | 스킬 매칭 | 전략적 조언, ROI 계산 |
| Agents | 0 (Python script) | 8 multi-agent pipeline |
| Timeline | 즉시 (데이터만) | 월별 학습 로드맵 |

### vs. 일반 커리어 상담
- ✅ 실시간 시장 데이터 (JD 100+ 분석)
- ✅ 정량적 ROI 계산 (연봉, 학습 시간)
- ✅ 구체적 실행 계획 (월별 로드맵)
- ✅ 자동화된 트렌드 조사 (웹 검색)
- ✅ 복수 옵션 제공 (3-5 paths)

### vs. ChatGPT 일반 상담
- ✅ 개인화 (실제 프로필 데이터 사용)
- ✅ 시장 검증 (실제 JD 데이터 기반)
- ✅ 실행 가능성 (구체적 리소스, 프로젝트 제안)
- ✅ 일관성 (multi-agent pipeline)

---

## 구현 우선순위

### Sprint 1 (MVP): Core Pipeline
**Goal**: End-to-end 파이프라인 동작

- [x] 기획 완료 (이 문서)
- [ ] `plugin.json` 생성
- [ ] Agent 파일 4개:
  - [ ] `resume-analyzer.md`
  - [ ] `jd-market-analyzer.md`
  - [ ] `career-path-generator.md` (핵심!)
  - [ ] `roadmap-generator.md`
- [ ] `SKILL.md` orchestrator
- [ ] `npm run link` 실행
- [ ] 수동 테스트 (본인 프로필)

**Success Criteria**: `/career-compass` 실행 → 3개 path 생성 → 로드맵 파일 생성

---

### Sprint 2: Enhancement
**Goal**: 분석 품질 향상

- [ ] Agent 3개 추가:
  - [ ] `career-trend-researcher.md` (웹 검색)
  - [ ] `skill-gap-analyzer.md` (우선순위)
  - [ ] `salary-projector.md` (ROI)
- [ ] Phase 1 parallel execution 테스트
- [ ] Error handling 추가

**Success Criteria**: 모든 8개 agent 동작, 병렬 실행 확인

---

### Sprint 3: Polish
**Goal**: 프로덕션 준비

- [ ] `strategy-advisor.md` 완성도 높이기
- [ ] 에러 핸들링 강화
- [ ] jd-analyzer 데이터 없을 때 fallback
- [ ] README.md 작성
- [ ] 실제 사용자 테스트 (3-5명)
- [ ] 피드백 반영

**Success Criteria**: 타인이 사용 가능한 수준

---

## 검증 계획

### Phase 1: Manual Testing (Sprint 1)
1. `/career-compass` 실행
2. Interview 질문 답변
3. Phase 1-2 agent 실행 확인
4. 3개 path 생성 확인
5. Roadmap 파일 품질 평가

**Expected Issues**:
- Agent 호출 실패 → Tool restrictions 조정
- Parallel execution 안됨 → 단일 응답 블록 확인
- JSON 파싱 에러 → Output format 명확히

---

### Phase 2: Integration Testing (Sprint 2)
1. jd-analyzer 데이터 연동 확인
2. 모든 8개 agent 정상 실행
3. 병렬 실행 성능 측정 (Phase 1, 2)
4. 파일 생성 확인 (roadmap, strategy)

**Expected Issues**:
- WebSearch 실패 → Fallback to manual research
- Salary data inaccurate → Add disclaimer
- Phase 간 데이터 전달 오류 → 변수명 표준화

---

### Phase 3: User Acceptance (Sprint 3)
1. 실제 사용자 프로필 5개로 테스트
2. Path 추천의 타당성 평가
3. Roadmap 실행 가능성 검증
4. Strategy advice 유용성 평가

**Success Metrics**:
- [ ] 5/5 사용자가 path 중 하나를 선택
- [ ] 4/5 사용자가 roadmap을 "실행 가능"하다고 평가
- [ ] 3/5 사용자가 즉시 Week 1-2 action 시작

---

## 위험 요소 및 대응

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Agent 실행 실패 | Medium | High | Tool restrictions 명확히, fallback logic |
| 병렬 실행 안됨 | Low | Medium | 단일 응답 블록 패턴 준수 |
| JD 데이터 부족 | High | Medium | Fallback: 웹 검색으로 보완, 경고 표시 |
| Path 추천 부정확 | Medium | High | Opus 사용, 시장 데이터 기반 검증 |
| Roadmap 너무 generic | Medium | High | 구체적 리소스 명시 강제 (prompt engineering) |
| WebSearch 실패 | Low | Low | Graceful degradation, manual research 안내 |

---

## 예상 파일 출력

### 1. Roadmap File
`~/.career-compass/roadmaps/roadmap-path1-2026-02-14.md`

```markdown
# Learning Roadmap: Direct AI Engineer Transition

**Generated**: 2026-02-14
**Duration**: 12-18 months
**Study Time**: 10 hrs/week

## Phase 1: Python Fundamentals (Months 1-3)

### Month 1: Python Basics
**Goal**: Master Python syntax

**Resources**:
- Course: Python for Everybody (Coursera)
- Practice: LeetCode Easy (5/week)

**Milestone**: CLI automation tool

### Month 2: Advanced Python
...

## Phase 2: ML Fundamentals (Months 4-6)
...
```

### 2. Strategy Report
`~/.career-compass/strategy/strategy-2026-02-14.md`

```markdown
# Career Strategy Report

## Executive Summary
Based on 6 years experience...

## Immediate Actions (Week 1-2)
- [ ] Enroll in Python course
- [ ] Join r/MachineLearning
...

## Risk Mitigation
...
```

---

## 참고 자료

### Internal
- **jd-analyzer plugin**: `plugins/jd-analyzer/`
- **project-insight**: `plugins/project-insight/` (multi-agent 참고)
- **portfolio-analyzer**: `plugins/portfolio-analyzer-fused/agents/` (agent 정의 참고)

### External
- **oh-my-opencode**: Multi-agent orchestration patterns
- **Claude Code docs**: Task tool, agent registration

---

## 구현 후 사용법

```bash
# 1. 구현 완료 후 등록
cd ~/Documents/Projects/claude-ai-engineering
npm run link

# 2. 확인
ls -la ~/.claude/agents/ | grep -E "(resume|jd-market|career)"

# 3. Claude Code에서 실행
# 사용자: "/career-compass"
# 또는: "analyze my career and suggest paths"

# 4. 생성된 파일 확인
ls -la ~/.career-compass/roadmaps/
ls -la ~/.career-compass/strategy/
```

---

## 다음 단계

1. ✅ 기획 완료 (이 문서)
2. ⏳ 사용자 승인 대기
3. 🚧 Sprint 1 구현 시작
   - [ ] `plugin.json`
   - [ ] 핵심 4개 agent
   - [ ] `SKILL.md` orchestrator
4. 🚧 Sprint 2: 나머지 agent 추가
5. 🚧 Sprint 3: 완성도 향상

---

## 변경 이력

- **2026-02-14**: 초안 작성 (Multi-Agent Pipeline 설계)
- **2026-02-14**: Claude Code 환경에 맞게 전면 수정
  - TypeScript → Markdown frontmatter
  - delegate_task → Task tool
  - openai/gpt-5.2 → opus
  - 커스텀 sub-agent 등록 방식 적용
  - 실제 구현 가능한 형태로 구체화
