# Business Avengers

## Purpose

AI partner organization for solo entrepreneurs. 23 AI agents + You as CEO (24 roles) that plan, research, design, develop, market, and monetize your online service from idea to launch — with sprint cycles for continuous improvement.

## Trigger Phrases

**English:**
- "business avengers"
- "/business-avengers"
- "start a business"
- "build a service"
- "launch a product"

**Korean:**
- "비즈니스 어벤저스"
- "사업 시작"
- "서비스 만들기"
- "제품 출시"

## Model Selection

- **Recommended**: `claude-opus-4-6` for orchestration (strategic decision routing)
- **Agents**: `claude-sonnet-4-5` for all 23 AI agents (quality + speed balance)

## Algorithm

### Step 0: Resolve Plugin Directory

Before executing any step, resolve the plugin root directory:

```python
# The SKILL.md is loaded from ~/.claude/skills/business-avengers/SKILL.md (symlink)
# Resolve the actual plugin root by following the symlink
SKILL_PATH = Bash("readlink ~/.claude/skills/business-avengers").strip()
# SKILL_PATH = .../plugins/business-avengers/skills/business-avengers
PLUGIN_DIR = SKILL_PATH + "/../.."  # Go up 2 levels to plugin root

# Alternatively, use Glob to find the plugin root:
# PLUGIN_DIR = Glob("**/plugins/business-avengers/config/init-project.py")[0].replace("/config/init-project.py", "")

# Set derived paths
TEMPLATE_DIR = f"{PLUGIN_DIR}/templates"
KNOWLEDGE_DIR = f"{PLUGIN_DIR}/knowledge"
AGENTS_DIR = f"{PLUGIN_DIR}/agents"
CONFIG_DIR = f"{PLUGIN_DIR}/config"
```

### Step 1: Parse Command & Determine Mode

Parse the user's trigger to determine operating mode:

```
INPUT PATTERNS:
  /business-avengers new "{idea}"                    → ORCHESTRA mode (idea-first)
  /business-avengers new --mode market-first "{q}"   → ORCHESTRA mode (market-first)
  /business-avengers new --mode mvp-build "{idea}"   → ORCHESTRA mode (mvp-build)
  /business-avengers phase {phase-name}              → SINGLE PHASE mode
  /business-avengers sprint "{goal}"                 → SPRINT mode
  /business-avengers ask {agent} "{question}"        → ASK mode
  /business-avengers status                          → STATUS mode
  /business-avengers resume                          → RESUME mode
  /business-avengers history                         → HISTORY mode
  "비즈니스 어벤저스" + free text                      → ORCHESTRA mode (detect intent)
```

**Set mode variables:**
```python
is_sprint = (mode == "SPRINT")
sprint_goal = user_input if is_sprint else ""
```

**Mode routing:**
- If mode = STATUS → Go to Step 12
- If mode = HISTORY → Go to Step 13
- If mode = ASK → Go to Step 14
- If mode = RESUME → Go to Step 3 (load project, continue from last phase)
- If mode = SINGLE PHASE → Go to Step 3 (load project, run specific phase)
- If mode = SPRINT → Go to Step 3 (load project, enter sprint mode)
- If mode = ORCHESTRA → Go to Step 2

---

### Step 2: Initialize New Project

```python
# 2.1 Get project name from user if not provided
AskUserQuestion(
  "프로젝트 이름을 정해주세요. (예: '음식 리뷰 큐레이션 앱')",
  options=["직접 입력"],
  allow_freeform=true
)

# 2.2 Generate slug from name
project_slug = slugify(project_name)  # "food-review-curation"

# 2.3 Select workflow mode
if not specified:
  AskUserQuestion(
    "어떤 모드로 시작할까요?",
    options=[
      "아이디어 우선 (Recommended) - 아이디어가 있으면 이 모드",
      "시장 우선 - 시장 기회를 먼저 탐색",
      "MVP 빌드 - 최소 기능으로 빠르게",
      "커스텀 - Phase를 직접 선택"
    ]
  )

# 2.4 Initialize project
Bash("python3 {PLUGIN_DIR}/config/init-project.py create '{project_name}' '{project_slug}' '{workflow_mode}'")
```

**Variables set:**
```
# PLUGIN_DIR, TEMPLATE_DIR, KNOWLEDGE_DIR, AGENTS_DIR, CONFIG_DIR → resolved in Step 0
PROJECT_DIR = ~/.business-avengers/projects/{project_slug}
```

---

### Step 3: Load Existing Project

```python
# Load project.yaml (init-project.py outputs JSON to stdout)
result = Bash("python3 {CONFIG_DIR}/init-project.py load '{project_slug}'")
# result is JSON: {"status": "loaded", "data": {...}} or {"status": "not_found", ...}

# Handle project not found
if "not_found" in result:
  AskUserQuestion(
    f"프로젝트 '{project_slug}'를 찾을 수 없습니다.",
    options=["새 프로젝트 생성 → Step 2로 이동", "다른 프로젝트 이름 입력"]
  )

# Extract project data from JSON output
project = result  # The JSON data from init-project.py

# Determine which phases to run based on mode:
if mode == ORCHESTRA:
  phases_to_run = WORKFLOW_PRESETS[workflow_mode]
elif mode == SINGLE_PHASE:
  phases_to_run = [requested_phase_number]
elif mode == SPRINT:
  # Ask CEO which phases need updating
  AskUserQuestion(
    "이번 스프린트에서 어떤 단계를 업데이트해야 할까요?",
    options=[
      "기획 수정 (Phase 2)",
      "디자인 수정 (Phase 3)",
      "기술 설계 수정 (Phase 4)",
      "마케팅 전략 수정 (Phase 7)",
      "직접 선택"
    ],
    multiSelect=true
  )
  phases_to_run = selected_phases
elif mode == RESUME:
  # Find first incomplete phase
  phases_to_run = [p for p in workflow if project.phases[p].status != "completed"]
```

---

### Step 4: Execute Phase 0 - Ideation

**Condition**: Only runs if Phase 0 is in phases_to_run

**Lead**: CPO + Product Manager
**CEO Interaction**: Dialogue (interactive Q&A)

```python
# 4.1 CPO introduces the ideation process
# Display as CPO speaking:
"""
[CPO] 안녕하세요, CEO님. 새로운 프로젝트를 시작하겠습니다.
아이디어를 구체화하기 위해 몇 가지 질문을 드리겠습니다.
"""

# 4.2 Interactive Q&A (5-7 questions)
questions = [
  "이 서비스가 해결하는 구체적인 문제는 무엇인가요?",
  "주요 타겟 사용자는 누구인가요? (나이, 직업, 상황 등)",
  "현재 사용자들이 이 문제를 어떻게 해결하고 있나요? (기존 대안)",
  "기존 대안 대비 우리 서비스의 핵심 차별점은?",
  "첫 수익은 어떻게 발생할 것으로 예상하시나요?",
]

for q in questions:
  AskUserQuestion(q, allow_freeform=true)

# 4.3 Product Manager synthesizes into Idea Canvas
Task(
  subagent_type="product-manager",
  model="sonnet",
  description="Create Idea Canvas",
  prompt=f"""
  당신은 Business Avengers의 Product Manager입니다.

  CEO와의 대화 내용:
  {all_qa_responses}

  작업:
  1. Read로 템플릿 읽기: {TEMPLATE_DIR}/idea-canvas.md
  2. CEO 답변을 분석하여 모든 플레이스홀더를 채우세요
  3. Write로 저장: {PROJECT_DIR}/phase-0-ideation/idea-canvas.md

  전문적이고 구체적으로 작성하세요. 모호한 표현 없이.
  """
)

# 4.4 Present to CEO for approval
idea_canvas = Read("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
# Display idea canvas content to CEO

AskUserQuestion(
  "[CPO] Idea Canvas를 검토해주세요. 어떻게 진행할까요?",
  options=[
    "승인 - 다음 단계로 진행",
    "수정 요청 - 피드백 반영 후 재작업",
    "중단 - 프로젝트 보류"
  ]
)

# If approved: update project.yaml phase 0 status
Bash("python3 {PLUGIN_DIR}/config/init-project.py update-phase '{project_slug}' 0 completed v1.0")
```

---

### Step 5: Execute Phase 1 - Market Research

**Condition**: Only runs if Phase 1 is in phases_to_run

**Lead**: CFO
**Agents**: business-analyst + marketing-strategist + revenue-strategist (PARALLEL)
**CEO Interaction**: Approve

```python
# 5.1 Read previous phase outputs for context (check existence with Glob first)
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""

# 5.2 Sprint mode: read existing docs for update context
sprint_context = ""
if is_sprint:
  existing_files = Glob("{PROJECT_DIR}/phase-1-market-research/*.md")
  existing_market = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md") if "market-analysis.md" in str(existing_files) else ""
  existing_competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md") if "competitive-analysis.md" in str(existing_files) else ""
  existing_revenue = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md") if "revenue-model-draft.md" in str(existing_files) else ""
  # Backup existing docs before overwriting
  Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-1-market-research market-analysis.md {current_version}")
  sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 내용:\n{existing_market}"

# 5.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="Market size analysis",
  prompt=f"""
  당신은 Business Avengers의 Business Analyst입니다.

  프로젝트 컨텍스트:
  {idea_canvas}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/startup-best-practices.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/market-analysis.md

  작업:
  1. WebSearch로 실제 시장 데이터를 조사하세요
  2. TAM/SAM/SOM을 산정하세요
  3. 시장 트렌드와 성장 동력을 분석하세요
  4. 템플릿을 채워 Write로 저장: {PROJECT_DIR}/phase-1-market-research/market-analysis.md

  {sprint_context if sprint else ""}
  데이터 출처를 반드시 명시하세요. 추정치에는 근거를 달아주세요.
  """
)

Task(
  subagent_type="marketing-strategist",
  model="sonnet",
  description="Competitive analysis",
  prompt=f"""
  당신은 Business Avengers의 Marketing Strategist입니다.

  프로젝트 컨텍스트:
  {idea_canvas}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/competitive-analysis.md

  작업:
  1. WebSearch + WebFetch로 경쟁사 5개를 조사하세요
  2. 각 경쟁사의 기능, 가격, 강점/약점을 분석하세요
  3. SWOT 분석과 포지셔닝 맵을 작성하세요
  4. 템플릿을 채워 Write로 저장: {PROJECT_DIR}/phase-1-market-research/competitive-analysis.md

  {sprint_context if sprint else ""}
  실제 URL과 데이터를 포함하세요.
  """
)

Task(
  subagent_type="revenue-strategist",
  model="sonnet",
  description="Revenue model analysis",
  prompt=f"""
  당신은 Business Avengers의 Revenue Strategist입니다.

  프로젝트 컨텍스트:
  {idea_canvas}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/pricing-strategies.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/revenue-model-draft.md

  작업:
  1. WebSearch로 유사 서비스의 가격 정책을 조사하세요
  2. 3-5개의 수익 모델을 제안하세요
  3. 각 모델의 예상 수익, 장단점을 분석하세요
  4. 추천 모델과 근거를 제시하세요
  5. 템플릿을 채워 Write로 저장: {PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md

  {sprint_context if sprint else ""}
  """
)

# 5.4 Wait for all agents, then present summary to CEO
market = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
revenue = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")

# Display summary
"""
[CFO] 시장 조사 결과를 보고드립니다:

📊 시장 분석: {market_summary}
🏢 경쟁사 분석: {competitive_summary}
💰 수익 모델: {revenue_summary}

상세 문서는 프로젝트 폴더에 저장되었습니다.
"""

AskUserQuestion(
  "[CFO] 시장 조사 결과를 검토해주세요.",
  options=[
    "승인 - 시장성 확인, 다음 단계로",
    "수정 요청 - 추가 조사 필요",
    "피봇 - 방향 전환 (Phase 0으로)",
    "중단 - 시장성 부족"
  ]
)

Bash("python3 {PLUGIN_DIR}/config/init-project.py update-phase '{project_slug}' 1 completed v1.0")
```

---

### Step 6: Execute Phase 2 - Product Planning

**Condition**: Only runs if Phase 2 is in phases_to_run
**Lead**: CPO
**Agents**: product-manager + ux-researcher (PARALLEL → synthesis)

```python
# 6.1 Read all previous phase outputs for context
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
market_files = Glob("{PROJECT_DIR}/phase-1-market-research/*.md")
market_analysis = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md") if market_files else ""
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md") if market_files else ""
revenue_draft = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md") if market_files else ""

# 6.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-2-product-planning/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-2-product-planning prd.md {current_version}")
    existing_prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 PRD:\n{existing_prd}"

# 6.3 Launch 2 agents in PARALLEL
Task(
  subagent_type="product-manager",
  model="sonnet",
  description="Write PRD, user stories, feature priority",
  prompt=f"""
  당신은 Business Avengers의 Product Manager입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/product-manager.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - 시장 분석: {market_analysis}
  - 경쟁 분석: {competitive}
  - 수익 모델 초안: {revenue_draft}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/startup-best-practices.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/prd.md
  - {TEMPLATE_DIR}/user-stories.md
  - {TEMPLATE_DIR}/feature-priority.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. Knowledge Base를 Read로 읽어 참고하세요
  3. 시장 분석 결과를 반영하여 PRD를 작성하세요
  4. User Stories를 INVEST 원칙으로 작성하세요
  5. 기능 우선순위를 MoSCoW 프레임워크로 정리하세요
  6. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-2-product-planning/prd.md
     - {PROJECT_DIR}/phase-2-product-planning/user-stories.md
     - {PROJECT_DIR}/phase-2-product-planning/feature-priority.md
  """)

Task(
  subagent_type="ux-researcher",
  model="sonnet",
  description="Create user personas",
  prompt=f"""
  당신은 Business Avengers의 UX Researcher입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/ux-researcher.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - 시장 분석: {market_analysis}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/ux-principles.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/user-personas.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. WebSearch로 타겟 사용자 관련 리서치를 수행하세요
  3. 2-3개의 상세 페르소나를 작성하세요 (이름, 나이, 직업, 목표, 고충, 시나리오)
  4. 각 페르소나별 사용자 여정 맵을 포함하세요
  5. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-2-product-planning/user-personas.md
  """)

# 6.4 CEO reviews PRD + does MoSCoW prioritization
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
personas = Read("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")

AskUserQuestion(
  "[CPO] PRD와 기능 우선순위를 검토해주세요.",
  options=[
    "승인 - 다음 단계로 진행",
    "수정 요청 - 피드백 반영 후 재작업",
    "피봇 - 방향 전환"
  ]
)

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 2 completed v1.0")
```

---

### Step 7: Execute Phase 3 - Design

**Condition**: Only runs if Phase 3 is in phases_to_run
**Lead**: CPO (Design Lead)
**Agents**: design-lead → ui-designer (SEQUENTIAL)

```python
# 7.1 Read previous phase outputs
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
personas = Read("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")

# 7.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-3-design/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-3-design design-system.md {current_version}")
    existing_design = Read("{PROJECT_DIR}/phase-3-design/design-system.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 디자인 시스템:\n{existing_design}"

# 7.3 SEQUENTIAL: Design Lead FIRST, then UI Designer
Task(
  subagent_type="design-lead",
  model="sonnet",
  description="Create design system",
  prompt=f"""
  당신은 Business Avengers의 Design Lead입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/design-lead.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 페르소나: {personas}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/ux-principles.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/design-system.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. UX 원칙 Knowledge Base를 Read로 읽어 참고하세요
  3. 서비스 특성에 맞는 디자인 시스템을 설계하세요
  4. 컬러 팔레트, 타이포그래피, 스페이싱, 컴포넌트 규칙을 정의하세요
  5. 접근성(WCAG 2.1 AA) 기준을 반영하세요
  6. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-3-design/design-system.md
  """)

# 7.4 WAIT for design-lead, then read output for ui-designer
design_system = Read("{PROJECT_DIR}/phase-3-design/design-system.md")

Task(
  subagent_type="ui-designer",
  model="sonnet",
  description="Create wireframes and UI specs",
  prompt=f"""
  당신은 Business Avengers의 UI Designer입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/ui-designer.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 페르소나: {personas}
  - 디자인 시스템: {design_system}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/ux-principles.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/wireframes.md
  - {TEMPLATE_DIR}/ui-specifications.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 디자인 시스템을 기반으로 핵심 화면의 와이어프레임을 작성하세요
  3. 각 화면별 컴포넌트 명세와 인터랙션 패턴을 정의하세요
  4. PRD의 핵심 기능이 모두 와이어프레임에 반영되었는지 확인하세요
  5. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-3-design/wireframes.md
     - {PROJECT_DIR}/phase-3-design/ui-specifications.md
  """)

# 7.5 CEO reviews design
AskUserQuestion(
  "[CPO] 디자인 시스템과 와이어프레임을 검토해주세요.",
  options=[
    "승인 - 다음 단계로 진행",
    "수정 요청 - 피드백 반영 후 재작업",
    "피봇 - 방향 전환"
  ]
)

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 3 completed v1.0")
```

---

### Step 8: Execute Phase 4 - Technical Planning

**Condition**: Only runs if Phase 4 is in phases_to_run
**Lead**: CTO
**Agents**: tech-lead (single)
**CEO Interaction**: Delegate + Report (CTO makes decisions)

```python
# 8.1 Read previous phase outputs
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
ui_specs_files = Glob("{PROJECT_DIR}/phase-3-design/ui-specifications.md")
ui_specs = Read(ui_specs_files[0]) if ui_specs_files else ""

# 8.2 Sprint mode
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-4-tech-planning/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-4-tech-planning tech-architecture.md {current_version}")
    existing_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 아키텍처:\n{existing_arch}"

# 8.3 Tech Lead designs architecture
Task(
  subagent_type="tech-lead",
  model="sonnet",
  description="Design technical architecture",
  prompt=f"""
  당신은 Business Avengers의 Tech Lead입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/tech-lead.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - UI 스펙: {ui_specs}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/tech-architecture.md
  - {TEMPLATE_DIR}/api-design.md
  - {TEMPLATE_DIR}/database-schema.md
  - {TEMPLATE_DIR}/tech-stack-decision.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. Tech Stack Guide를 Read로 읽어 서비스 유형에 맞는 스택을 선택하세요
  3. PRD의 기능 요구사항을 기반으로 시스템 아키텍처를 설계하세요
  4. RESTful API를 설계하고 엔드포인트를 정의하세요
  5. 데이터베이스 스키마를 ERD와 함께 설계하세요
  6. 기술 스택 결정 문서에 선택 근거를 작성하세요
  7. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md
     - {PROJECT_DIR}/phase-4-tech-planning/api-design.md
     - {PROJECT_DIR}/phase-4-tech-planning/database-schema.md
     - {PROJECT_DIR}/phase-4-tech-planning/tech-stack-decision.md
  """)

# 8.4 CTO reports to CEO (lighter review - delegate level)
tech_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")

"""
[CTO] 기술 설계가 완료되었습니다. 상세 내용은 프로젝트 폴더를 확인해주세요.
"""

AskUserQuestion("[CTO] 기술 설계 보고입니다. 확인해주세요.",
  options=["확인 - 진행", "질문 있음", "수정 요청"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 4 completed v1.0")
```

---

### Step 9: Execute Phase 5 - Development Guide

**Condition**: Only runs if Phase 5 is in phases_to_run
**Lead**: CTO
**Agents**: frontend-dev + backend-dev + devops-engineer (PARALLEL)
**CEO Interaction**: Delegate + Report (CTO manages)

```python
# 9.1 Read previous phase outputs
tech_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
api_design = Read("{PROJECT_DIR}/phase-4-tech-planning/api-design.md")
db_schema = Read("{PROJECT_DIR}/phase-4-tech-planning/database-schema.md")
ui_specs_files = Glob("{PROJECT_DIR}/phase-3-design/ui-specifications.md")
ui_specs = Read(ui_specs_files[0]) if ui_specs_files else ""
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")

# 9.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-5-development/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-5-development frontend-guide.md {current_version}")
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-5-development backend-guide.md {current_version}")
    existing_frontend = Read("{PROJECT_DIR}/phase-5-development/frontend-guide.md")
    existing_backend = Read("{PROJECT_DIR}/phase-5-development/backend-guide.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}"

# 9.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="frontend-dev",
  model="sonnet",
  description="Frontend implementation guide",
  prompt=f"""
  당신은 Business Avengers의 Frontend Developer입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/frontend-dev.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 기술 아키텍처: {tech_arch}
  - UI 스펙: {ui_specs}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/frontend-guide.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 기술 아키텍처에서 선택된 프론트엔드 스택을 확인하세요
  3. 프로젝트 구조(디렉토리, 파일 구성)를 설계하세요
  4. 핵심 컴포넌트 목록과 각 컴포넌트의 역할을 정의하세요
  5. 상태 관리 전략, 라우팅, API 통신 패턴을 설계하세요
  6. UI 스펙의 각 화면을 컴포넌트로 분해하세요
  7. 성능 최적화 전략(코드 스플리팅, 레이지 로딩 등)을 포함하세요
  8. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-5-development/frontend-guide.md
  """)

Task(
  subagent_type="backend-dev",
  model="sonnet",
  description="Backend implementation guide",
  prompt=f"""
  당신은 Business Avengers의 Backend Developer입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/backend-dev.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 기술 아키텍처: {tech_arch}
  - API 설계: {api_design}
  - DB 스키마: {db_schema}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/backend-guide.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 기술 아키텍처에서 선택된 백엔드 스택을 확인하세요
  3. 프로젝트 구조(디렉토리, 모듈, 레이어)를 설계하세요
  4. API 엔드포인트별 구현 가이드를 작성하세요 (컨트롤러, 서비스, 리포지토리)
  5. 인증/인가 구현 전략을 상세히 기술하세요
  6. DB 마이그레이션 전략과 ORM 모델 설계를 포함하세요
  7. 에러 핸들링, 로깅, 모니터링 패턴을 정의하세요
  8. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-5-development/backend-guide.md
  """)

Task(
  subagent_type="devops-engineer",
  model="sonnet",
  description="Deployment strategy and implementation roadmap",
  prompt=f"""
  당신은 Business Avengers의 DevOps Engineer입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/devops-engineer.md

  프로젝트 컨텍스트:
  - 기술 아키텍처: {tech_arch}
  - PRD: {prd}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/deployment-strategy.md
  - {TEMPLATE_DIR}/implementation-roadmap.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. CI/CD 파이프라인을 설계하세요 (빌드, 테스트, 배포 단계)
  3. 인프라 아키텍처를 설계하세요 (클라우드 서비스, 서버리스 등)
  4. 환경 구성(개발/스테이징/프로덕션)을 정의하세요
  5. 모니터링, 알림, 로그 관리 전략을 수립하세요
  6. 보안 설정(HTTPS, 방화벽, 시크릿 관리)을 포함하세요
  7. 전체 구현 로드맵을 스프린트 단위로 작성하세요
  8. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-5-development/deployment-strategy.md
     - {PROJECT_DIR}/phase-5-development/implementation-roadmap.md
  """)

# 9.4 CTO reports to CEO (delegate level - light confirmation)
"""
[CTO] 개발 가이드가 완료되었습니다:
- 프론트엔드 구현 가이드
- 백엔드 구현 가이드
- 배포 전략 & 구현 로드맵

상세 내용은 프로젝트 폴더를 확인해주세요.
"""

AskUserQuestion("[CTO] 개발 가이드가 완료되었습니다.", options=["확인 - 진행", "질문 있음", "수정 요청"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 5 completed v1.0")
```

---

### Step 10: Execute Phase 6 - QA Planning

**Condition**: Only runs if Phase 6 is in phases_to_run
**Lead**: CTO
**Agents**: qa-lead (single)
**CEO Interaction**: Delegate + Report

```python
# 10.1 Read previous phase outputs
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
user_stories = Read("{PROJECT_DIR}/phase-2-product-planning/user-stories.md")
tech_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
api_design = Read("{PROJECT_DIR}/phase-4-tech-planning/api-design.md")
frontend_guide_files = Glob("{PROJECT_DIR}/phase-5-development/frontend-guide.md")
frontend_guide = Read(frontend_guide_files[0]) if frontend_guide_files else ""

# 10.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-6-qa/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-6-qa test-plan.md {current_version}")
    existing_test = Read("{PROJECT_DIR}/phase-6-qa/test-plan.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 테스트 계획:\n{existing_test}"

# 10.3 QA Lead creates test plan
Task(
  subagent_type="qa-lead",
  model="sonnet",
  description="Create test plan and QA checklist",
  prompt=f"""
  당신은 Business Avengers의 QA Lead입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/qa-lead.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 유저 스토리: {user_stories}
  - 기술 아키텍처: {tech_arch}
  - API 설계: {api_design}
  - 프론트엔드 가이드: {frontend_guide}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/test-plan.md
  - {TEMPLATE_DIR}/qa-checklist.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. PRD와 유저 스토리를 기반으로 테스트 케이스를 도출하세요
  3. 기능 테스트, 통합 테스트, E2E 테스트 전략을 수립하세요
  4. API 엔드포인트별 테스트 시나리오를 작성하세요
  5. 성능 테스트 기준(응답 시간, 동시 접속 등)을 정의하세요
  6. 보안 테스트 체크리스트(OWASP Top 10)를 포함하세요
  7. QA 체크리스트를 출시 전/후로 구분하여 작성하세요
  8. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-6-qa/test-plan.md
     - {PROJECT_DIR}/phase-6-qa/qa-checklist.md
  """)

# 10.4 CTO reports to CEO
AskUserQuestion("[CTO] QA 계획이 완료되었습니다. 테스트 계획서와 QA 체크리스트가 생성되었습니다.",
  options=["확인 - 진행", "질문 있음", "수정 요청"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 6 completed v1.0")
```

---

### Step 11: Execute Phase 7 - Launch Strategy

**Condition**: Only runs if Phase 7 is in phases_to_run
**Lead**: CMO
**Agents**: marketing-strategist + content-creator + growth-hacker + pr-manager (PARALLEL)
**CEO Interaction**: Strategic Approval

```python
# 11.1 Read previous phase outputs
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
personas = Read("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")
market_analysis = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")

# 11.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-7-launch-strategy/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-7-launch-strategy gtm-strategy.md {current_version}")
    existing_gtm = Read("{PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 GTM 전략:\n{existing_gtm}"

# 11.3 Launch 4 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="marketing-strategist",
  model="sonnet",
  description="GTM strategy",
  prompt=f"""
  당신은 Business Avengers의 Marketing Strategist입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/marketing-strategist.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 페르소나: {personas}
  - 시장 분석: {market_analysis}
  - 경쟁 분석: {competitive}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/gtm-strategy.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 마케팅 플레이북 Knowledge Base를 참고하세요
  3. 타겟 세그먼트별 GTM 전략을 수립하세요
  4. 채널 전략(SEO, SNS, 이메일, 유료 광고)을 구체적으로 작성하세요
  5. 출시 전/당일/후 타임라인을 작성하세요
  6. 마케팅 예산 배분과 기대 ROI를 산정하세요
  7. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md
  """)

Task(
  subagent_type="content-creator",
  model="sonnet",
  description="Content marketing plan",
  prompt=f"""
  당신은 Business Avengers의 Content Creator입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/content-creator.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 페르소나: {personas}
  - 시장 분석: {market_analysis}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/content-plan.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 페르소나별 콘텐츠 전략을 수립하세요
  3. 채널별(블로그, SNS, 뉴스레터, 영상) 콘텐츠 캘린더를 작성하세요
  4. 핵심 메시지와 톤앤매너를 정의하세요
  5. SEO 키워드 전략을 포함하세요
  6. 콘텐츠 제작 워크플로우와 품질 기준을 정의하세요
  7. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-7-launch-strategy/content-plan.md
  """)

Task(
  subagent_type="growth-hacker",
  model="sonnet",
  description="Growth strategy",
  prompt=f"""
  당신은 Business Avengers의 Growth Hacker입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/growth-hacker.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 페르소나: {personas}
  - 시장 분석: {market_analysis}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/growth-hacking.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/growth-strategy.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 그로스 해킹 Knowledge Base를 참고하세요
  3. AARRR 퍼널 분석 프레임워크를 적용하세요
  4. 핵심 성장 지표(North Star Metric)를 정의하세요
  5. 바이럴 루프, 레퍼럴 프로그램 등 성장 레버를 설계하세요
  6. A/B 테스트 계획을 수립하세요
  7. 첫 1000명 사용자 획득 전략을 구체적으로 작성하세요
  8. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-7-launch-strategy/growth-strategy.md
  """)

Task(
  subagent_type="pr-manager",
  model="sonnet",
  description="PR plan and launch checklist",
  prompt=f"""
  당신은 Business Avengers의 PR Manager입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/pr-manager.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 시장 분석: {market_analysis}
  - 경쟁 분석: {competitive}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/pr-plan.md
  - {TEMPLATE_DIR}/launch-checklist.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. PR 전략(미디어 리스트, 보도자료, 인터뷰 등)을 수립하세요
  3. 출시 스토리 앵글을 3-5개 개발하세요
  4. 미디어 타겟 리스트(기자, 블로거, 인플루언서)를 작성하세요
  5. 위기 대응 시나리오와 Q&A를 준비하세요
  6. 출시 체크리스트를 D-30, D-7, D-1, D-Day, D+7로 구분하세요
  7. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-7-launch-strategy/pr-plan.md
     - {PROJECT_DIR}/phase-7-launch-strategy/launch-checklist.md
  """)

# 11.4 CMO presents to CEO for strategic approval
"""
[CMO] 출시 전략이 완료되었습니다:
- GTM 전략: 채널별 마케팅 계획
- 콘텐츠 플랜: 콘텐츠 캘린더 및 제작 계획
- 성장 전략: AARRR 퍼널 및 그로스 해킹 전략
- PR 플랜: 미디어 전략 및 출시 체크리스트

상세 문서는 프로젝트 폴더에 저장되었습니다.
"""

AskUserQuestion("[CMO] 출시 전략을 검토해주세요.",
  options=["승인 - 출시 전략 확정", "수정 요청 - 피드백 반영", "예산 조정 필요", "재검토 - 방향 재설정"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 7 completed v1.0")
```

---

### Step 11.5: Execute Phase 8 - Monetization

**Condition**: Only runs if Phase 8 is in phases_to_run
**Lead**: CFO
**Agents**: revenue-strategist + business-analyst (PARALLEL)
**CEO Interaction**: Strategic Approval (pricing decisions)

```python
# 11.5.1 Read previous phase outputs
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
market_analysis = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
revenue_draft = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")
feature_priority_files = Glob("{PROJECT_DIR}/phase-2-product-planning/feature-priority.md")
feature_priority = Read(feature_priority_files[0]) if feature_priority_files else ""

# 11.5.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-8-monetization/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-8-monetization pricing-strategy.md {current_version}")
    existing_pricing = Read("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 가격 전략:\n{existing_pricing}"

# 11.5.3 Launch 2 agents in PARALLEL
Task(
  subagent_type="revenue-strategist",
  model="sonnet",
  description="Pricing strategy",
  prompt=f"""
  당신은 Business Avengers의 Revenue Strategist입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/revenue-strategist.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 시장 분석: {market_analysis}
  - 경쟁 분석: {competitive}
  - 수익 모델 초안 (Phase 1): {revenue_draft}
  - 기능 우선순위: {feature_priority}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/pricing-strategies.md
  - {KNOWLEDGE_DIR}/business-models.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/pricing-strategy.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 가격 전략 Knowledge Base를 Read로 읽어 참고하세요
  3. Phase 1의 수익 모델 초안을 발전시켜 구체적인 가격 전략을 수립하세요
  4. 경쟁사 가격 비교 분석을 포함하세요
  5. 프리미엄/무료/프리미엄 tier별 기능 매핑을 작성하세요
  6. 가격 민감도 분석과 최적 가격 포인트를 제시하세요
  7. 할인/프로모션 전략을 수립하세요
  8. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-8-monetization/pricing-strategy.md
  """)

Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="Financial projections and unit economics",
  prompt=f"""
  당신은 Business Avengers의 Business Analyst입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/business-analyst.md

  프로젝트 컨텍스트:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - 시장 분석: {market_analysis}
  - 수익 모델 초안: {revenue_draft}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/pricing-strategies.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/financial-projections.md
  - {TEMPLATE_DIR}/unit-economics.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 3개년 재무 예측(매출, 비용, 이익)을 작성하세요
  3. 월별 캐시플로우 예측을 포함하세요
  4. Unit Economics를 산정하세요 (CAC, LTV, LTV/CAC, Payback Period)
  5. 손익분기점(BEP) 분석을 수행하세요
  6. 시나리오 분석(낙관/기본/비관)을 포함하세요
  7. 초기 투자 필요 금액과 자금 조달 전략을 제시하세요
  8. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-8-monetization/financial-projections.md
     - {PROJECT_DIR}/phase-8-monetization/unit-economics.md
  """)

# 11.5.4 CFO presents to CEO for strategic approval
"""
[CFO] 수익화 전략이 완료되었습니다:
- 가격 전략: tier별 가격 및 기능 매핑
- 재무 예측: 3개년 매출/비용/이익 전망
- Unit Economics: CAC, LTV, 손익분기점 분석

상세 문서는 프로젝트 폴더에 저장되었습니다.
"""

AskUserQuestion("[CFO] 수익화 전략을 검토해주세요.",
  options=["승인 - 가격 확정", "수정 요청 - 가격 조정 필요", "재검토 - 수익 모델 변경"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 8 completed v1.0")
```

---

### Step 11.6: Execute Phase 9 - Operations

**Condition**: Only runs if Phase 9 is in phases_to_run
**Lead**: COO
**Agents**: cs-manager + legal-advisor + data-analyst (PARALLEL)
**CEO Interaction**: Delegate + Report

```python
# 11.6.1 Read previous phase outputs
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
personas = Read("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")
pricing_files = Glob("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
pricing = Read(pricing_files[0]) if pricing_files else ""
tech_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")

# 11.6.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-9-operations/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-9-operations cs-playbook.md {current_version}")
    existing_cs = Read("{PROJECT_DIR}/phase-9-operations/cs-playbook.md")
    sprint_context = f"기존 문서를 업데이트하세요. 변경 목표: {sprint_goal}\n기존 CS 플레이북:\n{existing_cs}"

# 11.6.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="cs-manager",
  model="sonnet",
  description="CS playbook and FAQ",
  prompt=f"""
  당신은 Business Avengers의 CS Manager입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/cs-manager.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 페르소나: {personas}
  - 가격 전략: {pricing}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/startup-best-practices.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/cs-playbook.md
  - {TEMPLATE_DIR}/faq-template.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 고객 문의 유형별 대응 시나리오를 작성하세요
  3. 에스컬레이션 프로세스를 정의하세요 (1차→2차→CEO)
  4. 자주 묻는 질문(FAQ)을 카테고리별로 30개 이상 작성하세요
  5. 고객 만족도 측정 방법(NPS, CSAT)을 정의하세요
  6. 1인 기업에 맞는 효율적인 CS 운영 방안을 제시하세요
  7. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-9-operations/cs-playbook.md
     - {PROJECT_DIR}/phase-9-operations/faq-template.md
  """)

Task(
  subagent_type="legal-advisor",
  model="sonnet",
  description="Legal documentation",
  prompt=f"""
  당신은 Business Avengers의 Legal Advisor입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/legal-advisor.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 가격 전략: {pricing}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/legal-compliance.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/legal-docs.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 법규 준수 Knowledge Base를 Read로 읽어 참고하세요
  3. 이용약관(Terms of Service)을 작성하세요
  4. 개인정보처리방침(Privacy Policy)을 작성하세요
  5. 환불 정책을 작성하세요
  6. 서비스 특성에 따른 필수 법적 고지사항을 포함하세요
  7. 한국 법률(개인정보보호법, 전자상거래법 등) 준수 사항을 체크하세요
  8. 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-9-operations/legal-docs.md
  """)

Task(
  subagent_type="data-analyst",
  model="sonnet",
  description="Metrics dashboard and feedback loop",
  prompt=f"""
  당신은 Business Avengers의 Data Analyst입니다.

  에이전트 정의 (Read로 읽으세요):
  - {AGENTS_DIR}/data-analyst.md

  프로젝트 컨텍스트:
  - PRD: {prd}
  - 기술 아키텍처: {tech_arch}
  - 가격 전략: {pricing}

  Knowledge Base (Read로 읽으세요):
  - {KNOWLEDGE_DIR}/growth-hacking.md

  템플릿 (Read로 읽으세요):
  - {TEMPLATE_DIR}/metrics-dashboard.md
  - {TEMPLATE_DIR}/feedback-loop.md

  {sprint_context}

  작업:
  1. 에이전트 정의를 Read로 읽고 역할과 전문 프레임워크를 숙지하세요
  2. 핵심 KPI를 정의하세요 (비즈니스, 제품, 기술 지표)
  3. 대시보드 구성을 설계하세요 (실시간/일간/주간/월간)
  4. 데이터 수집 포인트와 이벤트 트래킹 계획을 작성하세요
  5. 분석 도구 추천 및 설정 가이드를 포함하세요
  6. 사용자 피드백 수집→분석→반영 프로세스를 설계하세요
  7. 데이터 기반 의사결정 프레임워크를 제시하세요
  8. 각 템플릿의 {{PLACEHOLDER}}를 채워 Write로 저장:
     - {PROJECT_DIR}/phase-9-operations/metrics-dashboard.md
     - {PROJECT_DIR}/phase-9-operations/feedback-loop.md
  """)

# 11.6.4 COO reports to CEO
"""
[COO] 운영 계획이 완료되었습니다:
- CS 플레이북: 고객 대응 시나리오 및 FAQ
- 법무 문서: 이용약관, 개인정보처리방침, 환불 정책
- 메트릭 대시보드: KPI 정의 및 데이터 수집 계획
- 피드백 루프: 사용자 피드백 수집→반영 프로세스

상세 문서는 프로젝트 폴더에 저장되었습니다.
"""

AskUserQuestion("[COO] 운영 계획이 완료되었습니다. 검토해주세요.",
  options=["확인 - 진행", "질문 있음", "수정 요청"])

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 9 completed v1.0")
```

---

### Step 12: Status Mode

```python
result = Bash("python3 {PLUGIN_DIR}/config/init-project.py load '{project_slug}'")
project = parse_json(result)

# Display formatted status
"""
📋 프로젝트: {project.name}
🔄 현재 스프린트: #{project.current_sprint}
📊 진행 상황:

| Phase | 이름 | 상태 | 버전 |
|-------|------|------|------|
| 0 | Ideation | ✅ 완료 | v1.0 |
| 1 | Market Research | ✅ 완료 | v1.1 |
| 2 | Product Planning | 🔄 진행중 | v1.2 |
| 3 | Design | ⏳ 대기 | - |
...
"""
```

---

### Step 13: History Mode

```python
# Read all changelogs
for phase_dir in project_dirs:
  changelog = Read("{phase_dir}/changelog.md") if exists

# Read sprint history
for sprint_file in sprints_dir:
  sprint = Read(sprint_file)

# Display formatted history
"""
📜 프로젝트 히스토리: {project.name}

Sprint 1 (2026-02-21): Initial E2E
  - Phase 0-8 완료
  - CEO 결정: 타겟을 20-30대로 좁힘

Sprint 2 (2026-03-01): 온보딩 개선
  - Phase 2 v1.1: PRD 온보딩 섹션 수정
  - Phase 3 v1.1: 온보딩 와이어프레임 업데이트

Sprint 3 (진행중): 소셜 로그인 추가
  - Phase 2 v1.2: 소셜 로그인 기능 추가
  - Phase 4 v1.1: OAuth 아키텍처 추가
"""
```

---

### Step 14: Ask Mode (Direct Agent Conversation)

```python
# Parse: /business-avengers ask {agent_or_team} "{question}"

# Map team names to agents
TEAM_MAP = {
  "cto": "cto",
  "cfo": "cfo",
  "cmo": "cmo",
  "cpo": "cpo",
  "coo": "coo",
  "marketing": "marketing-strategist",
  "product": "product-manager",
  "design": "design-lead",
  "tech": "tech-lead",
  "legal": "legal-advisor",
  "data": "data-analyst",
  "qa": "qa-lead",
  "cs": "cs-manager",
  "growth": "growth-hacker",
  "pr": "pr-manager",
  "content": "content-creator",
  "finance": "business-analyst",
  "revenue": "revenue-strategist",
  "frontend": "frontend-dev",
  "backend": "backend-dev",
  "devops": "devops-engineer",
  "ux": "ux-researcher",
  "ui": "ui-designer",
}

agent_id = TEAM_MAP.get(agent_or_team, agent_or_team)

# Load project context if exists
project_context = ""
if project_exists:
  project_context = f"현재 프로젝트: {project.name}\n"
  # Include relevant phase outputs based on agent's domain

Task(
  subagent_type=agent_id,
  model="sonnet",
  description=f"Direct question to {agent_id}",
  prompt=f"""
  당신은 Business Avengers의 {agent_title}입니다.
  CEO가 직접 질문합니다.

  {project_context}

  CEO 질문: {question}

  전문가로서 구체적이고 실행 가능한 답변을 하세요.
  필요하면 WebSearch로 최신 정보를 조사하세요.
  """
)
```

---

### Step 15: Sprint Completion

After all sprint phases are executed:

```python
# Update sprint record
sprint_data = {
  "goal": sprint_goal,
  "phases": phases_updated,
  "completed": current_date,
  "changes": changelog_entries
}
Write("{PROJECT_DIR}/sprints/sprint-{N}.yaml", yaml.dump(sprint_data))

# Update project.yaml current_sprint
Bash("python3 ... update sprint number")

# Sprint review
"""
[COO] 스프린트 #{N} 완료 보고:

🎯 목표: {sprint_goal}
📝 업데이트된 Phase: {phases_list}
📊 변경 사항: {changes_summary}

다음 스프린트를 계획하시겠습니까?
"""

AskUserQuestion(
  "다음 단계를 선택해주세요.",
  options=[
    "새 스프린트 시작",
    "현재 상태 유지",
    "프로젝트 완료"
  ]
)
```

---

### Step 16: Project Completion (Orchestra Mode)

When all phases are completed:

```python
# Generate executive summary
"""
🎉 프로젝트 완료: {project.name}

📁 생성된 산출물:
├── Phase 0: Idea Canvas
├── Phase 1: 시장 분석, 경쟁 분석, 수익 모델
├── Phase 2: PRD, 페르소나, 유저 스토리, 기능 우선순위
├── Phase 3: 디자인 시스템, 와이어프레임, UI 스펙
├── Phase 4: 기술 아키텍처, API 설계, DB 스키마
├── Phase 5: 프론트/백엔드 가이드, 배포 전략
├── Phase 6: 테스트 계획, QA 체크리스트
├── Phase 7: GTM 전략, 콘텐츠 플랜, 성장 전략, PR
├── Phase 8: 가격 전략, 재무 예측, Unit Economics
└── Phase 9: CS 플레이북, 법무, 메트릭 대시보드

📂 프로젝트 폴더: {PROJECT_DIR}

💡 다음 단계:
1. 산출물을 검토하고 CEO의 비전과 일치하는지 확인
2. 개발 가이드(Phase 5)를 기반으로 실제 개발 시작
3. 필요 시 '/business-avengers sprint "목표"'로 스프린트 시작
"""
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Project not found | Invalid slug or no project | Guide user to create new project |
| Agent timeout | Complex analysis | Retry with simplified prompt |
| Phase output missing | Previous phase not completed | Warn user, offer to skip or run missing phase |
| WebSearch fails | Network issue | Proceed with available data, mark [TODO] |
| project.yaml corrupted | File system issue | Recreate from existing phase outputs |
| Permission denied | Directory access | Check ~/.business-avengers permissions |

## Key Design Decisions

1. **Structured documents over free dialogue**: Following MetaGPT's proven pattern, agents communicate through structured output files, not natural language conversations between agents.

2. **Phase-level parallelism**: Within each phase, agents run in parallel where possible. Between phases, execution is sequential with CEO gates.

3. **Version control via file system**: Each document has a history/ folder for backups and a changelog.md for tracking changes across sprints.

4. **Knowledge base grounding**: Every agent has access to domain-specific knowledge files, ensuring consistent quality regardless of the model's training data.

5. **Hybrid autonomy**: Strategic decisions (phases 0,1,2,7,8) require CEO approval. Tactical decisions (phases 4,5,6) are delegated to C-Level with reporting.
