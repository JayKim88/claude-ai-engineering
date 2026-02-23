---
name: market-research-by-desire
description: |
  Desire-based market research automation. Triggers: "market research by desire", "desire research",
  "욕망 기반 시장조사", "욕망 리서치", "욕망에서 시장 찾기", "/market-research-by-desire"
version: 1.0.0
---

# Market Research By Desire

Reverse-engineer market opportunities from human desires through 3-round interview and 5-agent analysis.

## Execution Flow

### STEP 0: Initialize

1. Run `date '+%Y%m%d-%H%M%S'` to get the exact current timestamp. Never estimate. Use this as project slug: `YYYYMMDD-HHMMSS`
2. Create output directory:
   ```bash
   mkdir -p "$HOME/.market-research-by-desire/projects/{slug}/artifacts"
   ```
3. If mkdir fails, fallback to `/tmp/market-research-by-desire/{slug}/artifacts`
4. Read `config/settings.yaml` for default settings. If missing, use defaults: language=ko, timeout=300
5. Store `output_dir` path for all subsequent steps

---

### STEP 1: Interview Round 1 — Desire Category

Display: "욕망 기반 시장조사를 시작합니다"

```
AskUserQuestion(
  questions=[{
    "question": "어떤 욕망 영역을 탐색할까요? (Which desire domain?)",
    "header": "욕망 카테고리",
    "options": [
      {"label": "성장과성취", "description": "실력 향상, 목표 달성, 학습, 커리어"},
      {"label": "연결과소속", "description": "관계 형성, 커뮤니티, 외로움 해소"},
      {"label": "자유와통제", "description": "시간/경제적 자유, 자율성, FIRE"},
      {"label": "생존과안전", "description": "재정안정, 건강, 주거, 보안"}
    ],
    "multiSelect": false
  }]
)
```

If user selects "Other": accept custom input (e.g., "즐거움과자극", or freeform desire description).

Store the selected `desire_category`.

---

### STEP 2: Interview Round 2 — Sub-Category

Read `knowledge/desire-framework.md` to find Level 2 sub-categories for the selected category.

Present sub-categories dynamically. Example for 성장과성취:

```
AskUserQuestion(
  questions=[{
    "question": "{desire_category}의 세부 욕망을 선택하세요:",
    "header": "세부 욕망",
    "options": [
      {"label": "전문성개발", "description": "Skill development, 자격증, 교육"},
      {"label": "커리어성장", "description": "Career advancement, 이직, 승진"},
      {"label": "창업/부업", "description": "Side hustle, entrepreneurship"},
      {"label": "자기계발", "description": "Productivity, 시간관리, 독서"}
    ],
    "multiSelect": false
  }]
)
```

Adapt options based on the category selected in Step 1. Each category has 3-4 sub-categories in desire-framework.md.

Store the selected `desire_subcategory`.

---

### STEP 3: Interview Round 3 — Context & Constraints

Ask all context questions in a single call:

```
AskUserQuestion(
  questions=[
    {
      "question": "대상 시장은? (Target market)",
      "header": "시장",
      "options": [
        {"label": "Korea", "description": "한국 시장 중심, 글로벌 참조"},
        {"label": "Global", "description": "글로벌 시장, 한국 포함"},
        {"label": "Korea + Japan", "description": "한일 시장 중심"}
      ],
      "multiSelect": false
    },
    {
      "question": "1인 개발 가능성을 우선할까요?",
      "header": "Solo-dev",
      "options": [
        {"label": "Yes", "description": "1인 실행 가능한 기회 우선"},
        {"label": "No preference", "description": "팀 규모 무관"}
      ],
      "multiSelect": false
    },
    {
      "question": "예산 제약은?",
      "header": "예산",
      "options": [
        {"label": "Bootstrap", "description": "최소 자본, 유기적 성장"},
        {"label": "VC-ready", "description": "투자 유치 가능"},
        {"label": "No constraint", "description": "예산 제약 없음"}
      ],
      "multiSelect": false
    },
    {
      "question": "선호 산업은?",
      "header": "산업",
      "options": [
        {"label": "Tech/SaaS", "description": "소프트웨어, 플랫폼"},
        {"label": "Service", "description": "서비스, 컨설팅, 코칭"},
        {"label": "E-commerce", "description": "커머스, 마켓플레이스"},
        {"label": "Any", "description": "산업 무관"}
      ],
      "multiSelect": false
    }
  ]
)
```

Store all responses as `context`: target_market, solo_dev_preferred, budget_constraint, industry_preference.

Display interview summary:
```
욕망: {desire_category} > {desire_subcategory}
시장: {target_market} | Solo-dev: {solo_dev_preferred} | 예산: {budget_constraint} | 산업: {industry_preference}
```

---

### STEP 4: Phase 1 — Parallel Discovery

Display: "Phase 1: 욕망 구조와 시장 동향을 분석합니다..."

Launch TWO Task() calls in a SINGLE response block for parallel execution:

**Task 1: Desire Cartographer**
```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  description="Map desire to market structure",
  prompt="""You are the Desire Cartographer agent.

Read the agent definition at: agents/desire-cartographer/desire-cartographer.md
Read the desire taxonomy at: knowledge/desire-framework.md

## User Interview Data
- Desire category: {desire_category}
- Sub-category: {desire_subcategory}
- Target market: {target_market}
- Solo-dev preferred: {solo_dev_preferred}
- Industry preference: {industry_preference}

## Your Task
1. Map the desire to Level 1 → Level 2 → Level 3 nano-desires
2. Generate Korean + English search terms (15-25 keywords)
3. Identify desire intersections with other categories
4. Define 3-5 market segments

## Output
Use the Write tool to save your output as JSON to:
{output_dir}/artifacts/desire-map.json

Follow the exact JSON structure defined in your agent definition file."""
)
```

**Task 2: Market Trend Researcher**
```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  description="Research market size and trends",
  prompt="""You are the Market Trend Researcher agent.

Read the agent definition at: agents/market-trend-researcher/market-trend-researcher.md
Read the research methodology at: knowledge/market-research-methods.md

## User Interview Data
- Desire category: {desire_category}
- Sub-category: {desire_subcategory}
- Target market: {target_market}
- Industry preference: {industry_preference}

## Your Task
1. Use WebSearch to find market size data (TAM/SAM/SOM)
2. If target_market == "Korea": prioritize 통계청 KOSIS, 중소벤처기업부
3. If target_market == "Global": use Statista, IBISWorld, CB Insights
4. Identify 3-5 major trends with evidence
5. Extract growth drivers and headwinds

If no direct data available, use proxy market technique (e.g., Japan market x 0.6 for Korea).

## Output
Use the Write tool to save your output as JSON to:
{output_dir}/artifacts/market-trends.json

Follow the exact JSON structure defined in your agent definition file."""
)
```

Wait for both to complete.

**Validation:**
- If desire-map.json was not created: display error, exit skill
- If market-trends.json was not created: display warning, continue with limited data
- Read both JSON files to extract key data for Phase 2

Display Phase 1 summary:
```
욕망 동인: {top 3 core drivers from desire-map.json}
시장 규모: TAM {value from market-trends.json}
성장률: {CAGR}%
```

---

### STEP 5: Phase 2 — Sequential Competitive Analysis

Display: "Phase 2: 경쟁사와 기회 빈틈을 분석합니다..."

**Step 5.1: Competitive Scanner**

Read desire-map.json to extract search_terms and market_segments for the prompt.

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  description="Scan competitive landscape",
  prompt="""You are the Competitive Scanner agent.

Read the agent definition at: agents/competitive-scanner/competitive-scanner.md
Read the analysis methodology at: knowledge/competitive-analysis-methods.md

## Context from Phase 1
- Desire: {desire_category} > {desire_subcategory}
- Target market: {target_market}
- Search terms (from desire-map.json): {paste search_terms}
- Market segments: {paste market_segments}
- Key players identified: {paste key_players from market-trends.json if available}

## Your Task
1. Use WebSearch with the provided search terms to find competitors
2. Analyze 5-10 competitors in depth, 10-20 total
3. For top 5: WebFetch pricing pages, extract SWOT
4. Build feature comparison matrix
5. Calculate pricing benchmarks

If target_market == "Korea": prioritize Naver/Daum search.
If no competitors found: set no_competition=true (blue ocean).

## Output
Use the Write tool to save your output as JSON to:
{output_dir}/artifacts/competitive-landscape.json

Follow the exact JSON structure defined in your agent definition file."""
)
```

Wait for completion. Read competitive-landscape.json.

**Step 5.2: Gap Opportunity Analyzer**

If competitive-landscape.json exists, launch gap analyzer:

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  description="Identify market gaps and opportunities",
  prompt="""You are the Gap Opportunity Analyzer agent.

Read the agent definition at: agents/gap-opportunity-analyzer/gap-opportunity-analyzer.md
Read the assessment framework at: knowledge/opportunity-assessment.md

## All Research Data
Read these artifact files:
- {output_dir}/artifacts/desire-map.json
- {output_dir}/artifacts/market-trends.json
- {output_dir}/artifacts/competitive-landscape.json

## User Context
- Solo-dev preferred: {solo_dev_preferred}
- Budget constraint: {budget_constraint}
- Target market: {target_market}

## Your Task
1. Cross-reference desires (from desire-map) with competitor offerings
2. Identify unmet needs, feature gaps, pricing gaps, segment gaps
3. Highlight desire intersection opportunities
4. Create 2-3 positioning recommendations with 2x2 map

If solo_dev_preferred == "Yes":
  - Score each gap by solo-dev feasibility (1-10)
  - Filter out team-required gaps (marketplaces requiring liquidity, heavy ops)

If budget_constraint == "Bootstrap":
  - Prioritize organic growth opportunities
  - Flag high-CAC gaps as "Not Recommended"

If no_competition == true (blue ocean):
  - Add "Market Education Risk" assessment
  - Suggest validation experiments

## Output
Use the Write tool to save your output as JSON to:
{output_dir}/artifacts/gap-analysis.json

Follow the exact JSON structure defined in your agent definition file."""
)
```

Wait for completion.

If competitive-scanner failed: skip gap analyzer, display warning.

Display Phase 2 summary:
```
경쟁사 분석: {count}개 기업
기회 영역: {count}개 발견
Top 기회: {top opportunity title} (feasibility: {score}/10)
```

---

### STEP 6: Phase 3 — Revenue Model Design

Display: "Phase 3: 수익 모델을 설계합니다..."

Read gap-analysis.json to extract top opportunities for the prompt.

```
Task(
  subagent_type="general-purpose",
  model="sonnet",
  description="Design revenue models",
  prompt="""You are the Revenue Model Architect agent.

Read the agent definition at: agents/revenue-model-architect/revenue-model-architect.md
Read the feasibility criteria at: knowledge/opportunity-assessment.md (solo-dev section)

## All Research Data
Read these artifact files:
- {output_dir}/artifacts/desire-map.json
- {output_dir}/artifacts/market-trends.json
- {output_dir}/artifacts/competitive-landscape.json (if available)
- {output_dir}/artifacts/gap-analysis.json (if available)

## User Context
- Solo-dev preferred: {solo_dev_preferred}
- Budget constraint: {budget_constraint}
- Industry preference: {industry_preference}

## Your Task
1. Design 3-5 distinct revenue models
2. For each: calculate CAC, LTV, gross margin, churn assumptions
3. Create 3-year revenue projections (Y1, Y2, Y3)
4. Use WebSearch for pricing benchmarks in the identified market
5. Rank models and recommend the best one

If solo_dev_preferred == "Yes":
  - Prioritize SaaS, info products, niche tools
  - Score each model on solo-dev feasibility (1-10)
  - Exclude high-ops models

If budget_constraint == "Bootstrap":
  - Prioritize fast payback (CAC < 6 months)
  - Emphasize organic growth channels

## Output
Use the Write tool to save your output as JSON to:
{output_dir}/artifacts/revenue-models.json

Follow the exact JSON structure defined in your agent definition file."""
)
```

Wait for completion.

---

### STEP 7: Generate Final Documents

Read all artifact JSON files and the 3 templates to produce final reports.

For each document:
1. Read the template from `templates/` as a structural guide
2. Read the relevant artifact JSON files
3. Write a complete markdown document populated with actual data from artifacts

**7.1: market-analysis.md**
- Read `templates/market-analysis.md` for structure
- Read `artifacts/desire-map.json` + `artifacts/market-trends.json`
- Write populated document to `{output_dir}/market-analysis.md`
- Fill all sections: 욕망 구조, TAM/SAM/SOM, 트렌드, 산업 개요, 진입 장벽
- Replace placeholder sections with actual data from JSON
- Mark any missing data as "데이터 없음 — 추가 리서치 필요"

**7.2: competitive-analysis.md**
- Read `templates/competitive-analysis.md` for structure
- Read `artifacts/competitive-landscape.json` + `artifacts/gap-analysis.json`
- Write populated document to `{output_dir}/competitive-analysis.md`
- Fill: 경쟁사 매트릭스, SWOT, 포지셔닝 맵, 빈틈 분석, 기회 평가

**7.3: revenue-model-draft.md**
- Read `templates/revenue-model-draft.md` for structure
- Read `artifacts/revenue-models.json`
- Write populated document to `{output_dir}/revenue-model-draft.md`
- Fill: 3-5 모델 상세, 비교 매트릭스, Unit Economics, 추천 모델

If any artifact is missing, write partial document with available data and mark incomplete sections.

---

### STEP 8: Summary & Next Steps

Verify files exist:
```bash
ls -1 {output_dir}/*.md
```

Display final summary:

```markdown
# 욕망 기반 시장조사 완료!

## 조사 개요
| 항목 | 값 |
|------|-----|
| 욕망 | {desire_category} > {desire_subcategory} |
| 시장 | {target_market} |
| TAM / SAM / SOM | {values from market-trends.json} |
| 경쟁사 | {count}개 분석 |
| 기회 영역 | {count}개 발견 |
| 추천 수익 모델 | {recommended model name} |

## 생성된 문서
- {output_dir}/market-analysis.md
- {output_dir}/competitive-analysis.md
- {output_dir}/revenue-model-draft.md
- {output_dir}/artifacts/ (JSON 원본 데이터)

## 다음 단계
1. 시장 분석 문서에서 TAM/SAM/SOM 검증
2. 경쟁사 분석에서 포지셔닝 빈틈 확인
3. 수익 모델 1개 선택 후 MVP 설계
4. 타겟 고객 10명과 인터뷰 진행
```

---

## Error Handling

| Step | Error | Recovery |
|------|-------|----------|
| 0 | config.yaml missing | Use hardcoded defaults |
| 0 | mkdir fails | Fallback to /tmp |
| 1-3 | User provides no response | Exit gracefully |
| 4 | desire-cartographer fails | Cannot proceed — exit |
| 4 | market-trend-researcher fails | Continue with warning |
| 5.1 | competitive-scanner finds 0 competitors | Mark as blue ocean, continue |
| 5.2 | gap-analyzer fails | Use competitive data only |
| 6 | revenue-model-architect fails | Provide partial results |
| 7 | Template missing | Use basic markdown structure |
| 7 | Artifact JSON missing/malformed | Mark sections as "데이터 없음" |

## Model Selection

All 5 agents use `general-purpose` subagent with `sonnet` model. Each agent reads its definition from `agents/` directory for role, output format, and strategy.

**Cost:** ~$1-2 per run (5 agents + orchestration)
**Duration:** 12-18 minutes

## Quick Reference

**Triggers:**
- "market research by desire", "desire research", "/market-research-by-desire"
- "욕망 기반 시장조사", "욕망 리서치", "욕망에서 시장 찾기"

**Output:** `~/.market-research-by-desire/projects/{slug}/`
- market-analysis.md, competitive-analysis.md, revenue-model-draft.md
- artifacts/ (5 JSON files)
