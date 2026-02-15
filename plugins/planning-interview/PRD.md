# Planning Interview

**AI-powered product planning through adaptive interviews**

Transform vague ideas into actionable PRDs in 30 minutes through context-aware questioning tailored to solo builders, startups, and teams.

---

# Planning Interview Plugin - Product Requirements Document

> **Version**: 1.0.0
> **Created**: 2026-02-14
> **Status**: Draft
> **Author**: Jay Kim

---

## Overview

Planning Interview helps you create comprehensive product planning documents without staring at a blank page. Through AI-driven interviews that adapt to your context (solo builder / startup / team), you get business-focused questions that uncover what really matters: user problems, market opportunities, MVP scope, and execution priorities.

### What You Get

After 15-45 minutes (depending on mode), you'll receive:

- ✅ **Context-matched PRD** (Lean Canvas / Product Brief / Full PRD)
- ✅ **MoSCoW prioritized features** (Must/Should/Could/Won't Have)
- ✅ **MVP scope definition** with clear boundaries
- ✅ **Success metrics framework** (North Star + supporting KPIs)
- ✅ **30-90 day action plan** with milestones

**📄 Output file:** `./{project-name}-planning.md`

---

## Installation

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link
```

That's it! No configuration needed.

---

## Usage

### Trigger Phrases

#### Start Planning Interview
```
"planning interview"
"기획해줘"
"제품 기획 도와줘"
"PRD 만들어줘"
"/planning-interview"
```

#### Quick Mode (skip context detection)
```
"planning interview (solo mode)"
"planning interview for startup"
"planning interview for team"
```

---

### Example Sessions

<details>
<summary><b>Solo Mode (1인 개발자)</b> - 15-20 minutes</summary>

**Input:**
```
User: "planning interview - I want to build a developer tool"

Claude: "Let me help you plan this! First, a few questions about your context:
- Are you working solo or with a team? → Solo
- What stage is this project? → Idea stage
- Planning experience? → First time

→ Solo Mode activated (3-4 rounds, ~15-20 min)

Round 1/3: Problem & Solution
Q1: What specific problem are you solving? Who has this problem?
Q2: How do people solve this today?
Q3: Why build this now?

..."
```

**Output (Lean Canvas):**
```markdown
# Developer Tool - Lean Canvas

## Problem
- Developers spend 30+ min/day context switching between tools
- Losing flow state costs 2-3 hours productivity daily
- Current dashboards are too complex for solo devs

## Solution
- Single unified command palette (like Spotlight for dev tools)
- AI-powered context awareness
- 3-second access to any tool/doc

## MVP Scope (3 months)
✅ Must Have:
- Command palette UI
- GitHub integration
- Local documentation search

❌ Won't Have (Phase 2):
- Team collaboration
- Cloud sync
- Custom integrations

## 30-Day Action Plan
Week 1: User interviews (5 developers)
Week 2-3: Core MVP development
Week 4: Beta launch to 10 users
```
</details>

<details>
<summary><b>Startup Mode (스타트업)</b> - 25-30 minutes</summary>

**Input:**
```
User: "planning interview for startup"

Claude: "Great! Tell me about your team:
- Team size? → 3 people (2 eng, 1 design)
- Stage? → MVP done, preparing for growth
- Goal? → Series A funding prep

→ Startup Mode activated (4-6 rounds, ~25-30 min)
```

**Output (Product Brief):**
```markdown
# SaaS Tool - Product Brief

## Executive Summary
B2B productivity platform targeting remote teams (10-50 employees).
$50B TAM, $5B SAM. Differentiation: AI-native vs legacy tools.

## Market Opportunity
- TAM: $50B (remote work tools)
- SAM: $5B (SMBs with 10-50 employees)
- Target: 100K companies (direct competitors serve enterprises only)

## Feature Prioritization (MoSCoW)
Must Have (3 months):
- ✅ Real-time collaboration
- ✅ AI meeting summaries
- ✅ Calendar integration

Should Have (6 months):
- 📋 Mobile apps
- 📋 Advanced analytics

## 6-Month Roadmap
Q1: MVP → Product-Market Fit (100 paid users)
Q2: Growth (1000 users, $50K MRR)
Q3: Series A ($2M raise)
```
</details>

<details>
<summary><b>Team Mode (중규모 팀)</b> - 35-45 minutes</summary>

**Output (Full PRD):**
```markdown
# Feature Name - Product Requirements Document

## 1. Executive Summary
[Strategic alignment with company OKRs]

## 2. Business Goals
- Increase user retention by 15%
- Reduce churn from 5% → 3%
- Target: $500K ARR increase

## 3. Target Users
[Detailed personas with research findings]

## 4. Requirements
### Functional Requirements
FR-1: User can [action] so that [benefit]
...

## 5. Success Metrics
- North Star: Weekly Active Users
- Supporting: Feature adoption, NPS, retention
- Targets: 10K WAU by Q2

## 6. Timeline
Phase 1 (2 months): Core features
Phase 2 (1 month): Polish & beta
Phase 3 (1 month): Full rollout

## 7. Risks & Mitigation
[Detailed risk matrix with mitigations]
```
</details>

---

## 1. Executive Summary

### Vision
제품 기획을 혼자서도, 팀으로도 체계적으로 수행할 수 있게 돕는 AI 인터뷰 기반 기획 도구

### Mission
인터뷰 방식으로 비즈니스 요구사항을 수집하고, 사용자 맥락에 맞는 맞춤형 제품 기획서(PRD)를 자동 생성하여 의사결정 속도와 품질을 동시에 향상

### Key Differentiators
- **적응형 인터뷰**: 1인 개발자부터 중대형 팀까지 맥락에 맞게 질문 조정
- **비즈니스 중심**: 기술 스펙이 아닌 비즈니스 가치와 사용자 문제에 집중
- **실행 가능한 산출물**: 바로 실행 가능한 PRD와 우선순위 로드맵 생성

### Success Criteria
- ✅ 30분 이내에 완전한 PRD 생성 가능
- ✅ 1인 개발자와 팀 모두에서 90% 이상 만족도
- ✅ spec-interview와 명확한 차별화 (기획 vs 기술)

---

## 2. Problem Statement

### Current Pain Points

#### 1인 개발자 / 솔로프레너
- ❌ **체계적인 기획 경험 부족**: "일단 만들고 보자" 접근으로 방향성 상실
- ❌ **우선순위 혼란**: 모든 것이 중요해 보여서 MVP 범위를 못 정함
- ❌ **비즈니스 관점 부족**: 기술에만 집중하고 시장/사용자 니즈 간과
- ❌ **시간 부족**: 기획 문서 작성에 시간 쓸 여유 없음

#### 스타트업 / 소규모 팀
- ❌ **비일관적인 의사결정**: 팀원마다 다른 우선순위와 목표
- ❌ **불명확한 목표**: "좋은 제품"이라는 막연한 목표만 있음
- ❌ **문서화 부재**: 구두로만 합의하고 기록 안 함
- ❌ **반복 작업**: 같은 논의를 계속 반복

#### 기존 도구의 한계
- **Notion/Confluence**: 빈 페이지 앞에서 막막함, 무엇을 써야 할지 모름
- **PRD 템플릿**: 일반적이고 포괄적이라 우리 상황에 안 맞음
- **spec-interview**: 기술 요구사항에 집중, 비즈니스 관점 부족

### Why Now?
- AI가 컨텍스트 이해하고 적응형 질문 가능한 수준 도달
- 1인 개발자/인디 해커 증가 (No-code, AI 도구 발전)
- 빠른 검증과 실행이 중요한 시대 (Lean Startup, MVP 문화)

---

## 3. Target Users & Personas

### Primary Persona 1: Solo Builder (1인 개발자)

**Demographics:**
- 역할: 개발자, 디자이너, 창업자
- 경험: 기획 경험 거의 없음
- 시간: 주 10-20시간 (부업/사이드 프로젝트)
- 예산: 제한적 (무료 또는 저비용)

**Goals:**
- 아이디어를 빠르게 검증하고 싶다
- MVP를 3-6개월 내에 만들고 싶다
- 혼자서도 체계적으로 일하고 싶다

**Pain Points:**
- "뭐부터 만들어야 할지 모르겠어"
- "기능을 계속 추가하다가 출시를 못함"
- "사용자가 원하는 게 뭔지 확신이 없음"

**Needs:**
- 간단하고 빠른 기획 프로세스
- MVP 범위 정하기 도움
- 비즈니스 관점 학습

---

### Primary Persona 2: Startup Founder (스타트업 창업자)

**Demographics:**
- 역할: CEO, CPO, Product Manager
- 팀: 2-10명
- 경험: 일부 기획 경험 있음
- 단계: Pre-seed ~ Series A

**Goals:**
- 팀원들과 비전 정렬하고 싶다
- 투자자에게 보여줄 PRD 필요
- 빠른 의사결정과 실행

**Pain Points:**
- "팀원마다 우선순위가 다름"
- "회의는 많은데 결론이 안 남"
- "PRD 작성에 너무 오래 걸림"

**Needs:**
- 팀 정렬 도구
- 빠른 PRD 생성
- 우선순위 프레임워크

---

### Secondary Persona 3: Product Manager (중규모 팀)

**Demographics:**
- 역할: PM, PO
- 팀: 10-50명
- 경험: 기획 경험 풍부
- 조직: 확립된 프로세스 있음

**Goals:**
- 일관된 PRD 품질 유지
- 이해관계자 정렬
- 효율적인 문서화

**Pain Points:**
- "PRD 작성에 시간이 너무 많이 걸림"
- "매번 같은 질문을 반복함"
- "놓치는 요소가 생김"

**Needs:**
- 체계적인 질문 프레임워크
- 완전한 PRD 템플릿
- 이해관계자 관리 도구

---

## 4. Solution Overview

### Core Concept: Adaptive Interview System

사용자의 **컨텍스트**(팀 규모, 역할, 경험)를 먼저 파악하고,
그에 맞는 **맞춤형 질문**을 하여
**적절한 수준의 PRD**를 생성하는 적응형 인터뷰 시스템

### How It Works

```
Context Detection → Mode Selection → Interview → PRD Generation
       ↓                  ↓              ↓            ↓
   3 questions    Solo/Startup/     2-8 rounds   Lean Canvas/
   (team/role)     Team mode       (adaptive)   Brief/Full PRD

Examples:
┌──────────────┬────────────┬────────────┬─────────────────┐
│ Team: Solo   │ 3-4 rounds │ 15-20 min  │ Lean Canvas     │
│ Team: 2-10   │ 4-6 rounds │ 25-30 min  │ Product Brief   │
│ Team: 10+    │ 6-8 rounds │ 35-45 min  │ Full PRD        │
└──────────────┴────────────┴────────────┴─────────────────┘
```

### Key Differentiation vs spec-interview

| 측면 | spec-interview | planning-interview |
|------|----------------|-------------------|
| **초점** | 기술 구현 (How) | 비즈니스 가치 (Why, What) |
| **질문** | 아키텍처, 기술 스택, 성능 | 사용자 니즈, 시장, 우선순위 |
| **산출물** | Technical Spec | PRD (Product Requirements) |
| **사용자** | 개발팀 | 창업자, PM, 경영진 |
| **단계** | 기획 후 개발 전 | 개발 전 기획 단계 |
| **질문 예시** | "동시 편집 시 충돌 해결?" | "왜 이 기능이 필요한가?" |

---

## 5. Key Features

### Feature 1: Context-Aware Interview (필수)

**Description:**
사용자의 맥락을 파악하고 그에 맞는 질문 플로우를 자동 선택

**User Story:**
> As a **1인 개발자**,
> I want **내 상황에 맞는 질문만** 받고 싶다,
> So that **시간을 절약하고 관련 있는 내용에만 집중**할 수 있다.

**Acceptance Criteria:**
- [ ] 첫 라운드에서 팀 규모, 역할, 경험 수준 파악
- [ ] 파악된 컨텍스트에 따라 질문 수, 깊이, 카테고리 조정
- [ ] Solo/Startup/Team 모드 자동 전환
- [ ] 사용자가 수동으로 모드 변경 가능

**Priority:** P0 (Must Have)

---

### Feature 2: Business-Focused Questions (필수)

**Description:**
기술이 아닌 비즈니스 가치, 사용자 문제, 시장 기회에 집중하는 질문

**Question Categories:**

#### Category 1: 비즈니스 목표 & 가치
- 왜 이 제품/기능이 필요한가?
- 해결하려는 문제는 무엇인가?
- 성공을 어떻게 정의할 것인가?
- 비즈니스 임팩트는?

#### Category 2: 사용자 & 시장
- 타겟 사용자는 누구인가?
- 사용자의 pain point는?
- 시장 규모와 기회는?
- 경쟁사는? 차별점은?

#### Category 3: 제품 전략
- 핵심 가치 제안은?
- MVP 범위는?
- 로드맵은? (Phase 1, 2, 3)
- 출시 전략은?

#### Category 4: 우선순위 & 제약
- Must-have vs Nice-to-have?
- 시간/예산 제약은?
- 리스크는?
- 의존성은?

#### Category 5: 성공 지표
- North Star Metric은?
- KPI는?
- 목표치는?
- 어떻게 측정할 것인가?

**User Story:**
> As a **창업자**,
> I want **비즈니스 관점의 질문**을 받고 싶다,
> So that **기술이 아닌 가치 중심으로 생각**할 수 있다.

**Priority:** P0 (Must Have)

---

### Feature 3: Adaptive PRD Templates (필수)

**Description:**
컨텍스트에 맞는 적절한 수준의 PRD 자동 생성

#### Template 1: Lean Canvas (Solo Mode)
**When:** 1인 개발자, MVP 단계
**Length:** 1-2 pages
**Sections:**
1. Problem (문제)
2. Solution (솔루션)
3. Unique Value Proposition (핵심 가치)
4. Key Metrics (핵심 지표)
5. Channels (채널)
6. Customer Segments (고객군)
7. Cost Structure (비용)
8. Revenue Streams (수익)
9. MVP Scope (MVP 범위)
10. Next 30 Days Action Plan (30일 실행 계획)

**Focus:** 빠른 실행, 검증

---

#### Template 2: Product Brief (Startup Mode)
**When:** 스타트업, 소규모 팀
**Length:** 3-5 pages
**Sections:**
1. Executive Summary
2. Problem Statement
3. Target Users & Personas
4. Solution Overview
5. Feature Prioritization (MoSCoW)
6. User Stories
7. Success Metrics & KPIs
8. Timeline & Milestones
9. Risks & Mitigation
10. Open Questions

**Focus:** 팀 정렬, 빠른 의사결정

---

#### Template 3: Full PRD (Team Mode)
**When:** 중규모 이상 팀, 복잡한 제품
**Length:** 8-12 pages
**Sections:**
1. Executive Summary
2. Business Goals & Objectives
3. Target Market & Competitive Analysis
4. User Personas & Research
5. Product Vision & Strategy
6. Detailed Requirements
7. Feature Prioritization Framework
8. User Stories & Use Cases
9. Success Metrics & KPIs
10. Timeline & Resource Planning
11. Stakeholder Alignment
12. Risk Assessment & Mitigation
13. Go-to-Market Strategy
14. Appendix (Research, Data)

**Focus:** 완전한 문서화, 이해관계자 정렬

---

**Priority:** P0 (Must Have)

---

### Feature 4: Smart Follow-up Questions (필수)

**Description:**
사용자의 답변을 분석하고 더 깊이 파고들어야 할 영역 식별

**Examples:**

**User says:** "타겟은 개발자입니다"
**Follow-up:**
- 프론트엔드/백엔드/풀스택 중 누구?
- 주니어/시니어?
- 회사 규모는? (스타트업/중견/대기업)
- 어떤 pain point를 가진 개발자?

**User says:** "3개월 안에 출시하고 싶어요"
**Follow-up:**
- 3개월이 중요한 이유는? (마켓 타이밍? 자금?)
- 혼자 하나요, 팀이 있나요?
- 하루에 투자 가능한 시간은?
- 3개월 안에 못 만들면 어떻게 되나요?

**User says:** "경쟁사는 없어요"
**Follow-up:**
- 사람들이 지금 이 문제를 어떻게 해결하나요?
- 대체재는? (수동 프로세스, 다른 도구)
- 왜 경쟁사가 없다고 생각하나요?

**Priority:** P0 (Must Have)

---

### Feature 5: MoSCoW Prioritization Helper (필수)

**Description:**
기능 우선순위를 Must/Should/Could/Won't로 분류 도와주기

**How it works:**
1. 사용자가 원하는 기능 리스트 수집
2. 각 기능에 대해 질문:
   - 이게 없으면 제품 출시 불가능? → Must Have
   - 1차 출시에 꼭 필요? → Should Have
   - 있으면 좋지만 나중에 해도 됨? → Could Have
   - 지금은 안 함 → Won't Have
3. 시간/리소스 제약 고려해서 조정
4. MVP 범위 명확히 정의

**User Story:**
> As a **1인 개발자**,
> I want **무엇을 먼저 만들어야 할지** 명확히 알고 싶다,
> So that **완벽한 제품을 만들려다 출시를 못하는 일이 없도록** 하고 싶다.

**Priority:** P0 (Must Have)

---

### Feature 6: Persona Builder (Should Have)

**Description:**
인터뷰 중 타겟 사용자 페르소나를 같이 만들기

**Template:**
```markdown
## Persona: [Name]

**Demographics:**
- Role:
- Age:
- Location:
- Company Size:

**Goals:**
- Primary Goal:
- Secondary Goal:

**Pain Points:**
- Frustration 1:
- Frustration 2:

**Current Solutions:**
- How they solve this now:

**Motivation:**
- Why they would use our product:

**Quote:**
> "Actual user quote that represents them"
```

**Priority:** P1 (Should Have)

---

### Feature 7: Competitive Analysis Helper (Should Have)

**Description:**
경쟁사 분석을 도와주는 질문과 프레임워크

**Questions:**
- 누가 비슷한 문제를 해결하나요?
- 그들의 접근법은?
- 그들이 잘하는 것은?
- 그들이 못하는 것은?
- 우리의 차별점은?
- 우리가 더 잘할 수 있는 이유는?

**Output:**
```markdown
## Competitive Landscape

### Direct Competitors
| Competitor | Strengths | Weaknesses | Pricing |
|------------|-----------|------------|---------|
| ...        | ...       | ...        | ...     |

### Indirect Competitors / Alternatives
| Alternative | How it works | Why users choose it |
|-------------|--------------|---------------------|
| ...         | ...          | ...                 |

### Our Differentiation
- **Unique Angle**:
- **Why Now**:
- **Defensibility**:
```

**Priority:** P1 (Should Have)

---

### Feature 8: Success Metrics Advisor (Should Have)

**Description:**
적절한 KPI와 목표치 설정 도와주기

**Framework:**
1. **North Star Metric 찾기**
   - 제품의 핵심 가치를 나타내는 단 하나의 지표
   - 예: DAU, Weekly Active Projects, Revenue per User

2. **Supporting Metrics**
   - Acquisition: 신규 사용자
   - Activation: 첫 가치 경험
   - Retention: 재방문율
   - Revenue: 수익화
   - Referral: 추천

3. **목표치 설정**
   - 현실적인 목표 vs 야심찬 목표
   - 시간 프레임 (1개월, 3개월, 6개월)
   - 달성 가능성 검증

**Priority:** P1 (Should Have)

---

### Feature 9: Timeline & Milestone Planner (Could Have)

**Description:**
현실적인 타임라인과 마일스톤 계획

**Questions:**
- 언제까지 출시하고 싶나요?
- 왜 그 날짜가 중요한가요?
- 하루/주에 투자 가능한 시간은?
- 혼자 하나요, 팀이 있나요?
- 외부 의존성은? (디자이너, API, 승인 등)

**Output:**
```markdown
## Timeline

### Phase 1: MVP (Months 1-2)
**Goal:** Launch basic version to early adopters

**Week 1-2:**
- [ ] User research & validation
- [ ] Core feature design

**Week 3-4:**
- [ ] Development Sprint 1

**Milestone 1:** First user can complete core flow

### Phase 2: Iteration (Month 3)
...
```

**Priority:** P2 (Could Have)

---

### Feature 10: Risk Assessment Matrix (Could Have)

**Description:**
잠재적 리스크 식별하고 완화 전략 수립

**Framework:**
```markdown
## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 시장이 너무 작음 | Medium | High | 초기 리서치로 검증, pivot 준비 |
| 경쟁사가 먼저 출시 | High | Medium | 차별화 포인트 강화, 틈새 공략 |
| 기술 구현 어려움 | Low | High | POC 먼저, 대체 기술 준비 |
```

**Priority:** P2 (Could Have)

---

## 6. User Experience Flow

### Flow 1: Solo Builder (1인 개발자)

```
1. Trigger: "planning interview 시작" 또는 "제품 기획해줘"

2. Context Detection (Round 0)
   Q: "현재 상황을 알려주세요"
   - 혼자 하나요, 팀이 있나요? → 혼자
   - 어떤 단계인가요? → 아이디어 단계
   - 기획 경험은? → 거의 없음

   → Solo Mode 활성화

3. Round 1: Problem & Solution (2-3 questions)
   Q1: "어떤 문제를 해결하고 싶나요? 누구의 문제인가요?"
   Q2: "사람들이 지금은 이 문제를 어떻게 해결하나요?"
   Q3: "왜 지금 이 문제를 해결해야 하나요?"

4. Round 2: Value & Validation (2-3 questions)
   Q1: "이 솔루션의 핵심 가치는 무엇인가요?"
   Q2: "첫 사용자가 '아, 이거다!'라고 느낄 순간은?"
   Q3: "어떻게 아이디어를 검증할 건가요?"

5. Round 3: MVP Scope (2-3 questions)
   Q1: "핵심 기능 3가지만 고른다면?"
   Q2: "3개월 안에 만들 수 있는 최소 버전은?"
   Q3: "첫 10명의 사용자를 어떻게 구할 건가요?"

6. Generate Lean Canvas (1-2 pages)

7. Confirmation
   ✅ Lean Canvas saved to: ./[project-name]-planning.md

   📋 Captured:
   - Problem: 개발자들의 코드 리뷰 병목
   - Solution: AI 기반 자동 리뷰
   - MVP: 3가지 핵심 검사만 지원
   - 30-Day Plan: Week 1-4 action items

   💡 Next Steps:
   - spec-interview로 기술 요구사항 정리?
   - 프로토타입 만들기 시작?
```

**Total Time:** 15-20분
**Total Rounds:** 3-4 rounds

---

### Flow 2: Startup Founder (스타트업)

```
1. Context Detection
   - 팀 규모? → 3명 (개발 2, 디자인 1)
   - 어떤 단계? → MVP 완성, 성장 준비
   - 목적? → 시리즈 A 투자 준비 PRD

   → Startup Mode 활성화

2. Round 1: Business Goals (3 questions)
   Q1: "비즈니스 목표는? 성공의 정의는?"
   Q2: "왜 지금 투자가 필요한가요?"
   Q3: "6개월 후 목표 지표는?"

3. Round 2: Market & Competition (3 questions)
   Q1: "타겟 시장 규모는? TAM/SAM/SOM?"
   Q2: "주요 경쟁사와 우리의 차별점은?"
   Q3: "왜 우리가 이길 수 있나요?"

4. Round 3: Product Strategy (3 questions)
   Q1: "다음 6개월 로드맵은?"
   Q2: "Must-have vs Nice-to-have 기준은?"
   Q3: "어떤 데이터로 의사결정할 건가요?"

5. Round 4: Team & Execution (2-3 questions)
   Q1: "팀 내 역할 분담은?"
   Q2: "어떻게 정렬을 유지할 건가요?"
   Q3: "주요 리스크와 완화 계획은?"

6. Generate Product Brief (3-5 pages)

7. Confirmation
   ✅ Product Brief saved to: ./[product-name]-PRD.md

   📋 Captured:
   - Market Size: $2B TAM, $200M SAM
   - Competitive Moat: AI 모델 특화
   - 6-Month Roadmap: 3 phases
   - Team Alignment: Weekly sync, OKRs
   - Investment Ask: $2M for team + marketing

   💡 Next Steps:
   - 투자자 deck 만들기?
   - 팀과 PRD 리뷰?
```

**Total Time:** 25-30분
**Total Rounds:** 4-6 rounds

---

### Flow 3: Product Manager (중규모 팀)

```
1. Context Detection
   - 팀 규모? → 25명
   - 역할? → Senior PM
   - 목적? → 새로운 기능 기획

   → Team Mode 활성화

2. Round 1: Strategic Alignment (3 questions)
   Q1: "회사/부서 OKR과 어떻게 연결되나요?"
   Q2: "주요 이해관계자는 누구이며 각자의 우선순위는?"
   Q3: "이 기능의 전략적 중요도는?"

3. Round 2: User Research (3 questions)
   Q1: "어떤 리서치를 했나요? 주요 인사이트는?"
   Q2: "타겟 페르소나별 니즈는?"
   Q3: "사용자 검증 계획은?"

4. Round 3: Requirements (3 questions)
   Q1: "Functional requirements는?"
   Q2: "Non-functional requirements는?"
   Q3: "Out of scope는?"

5. Round 4: Prioritization (3 questions)
   Q1: "RICE/ICE 스코어링 했나요?"
   Q2: "Phase별 출시 계획은?"
   Q3: "트레이드오프 의사결정 기준은?"

6. Round 5: Success & Measurement (2 questions)
   Q1: "Success metrics와 목표치는?"
   Q2: "어떻게 측정하고 모니터링할 건가요?"

7. Round 6: Risks & Dependencies (2 questions)
   Q1: "주요 리스크와 완화 전략은?"
   Q2: "외부 의존성과 블로커는?"

8. Generate Full PRD (8-12 pages)

9. Confirmation + Next Steps
```

**Total Time:** 35-45분
**Total Rounds:** 6-8 rounds

---

## 7. Question Quality Principles

### ✅ DO Ask

**1. 비즈니스 가치 중심**
- "왜 사용자가 이걸 원할까요?"
- "이게 없으면 어떤 일이 일어날까요?"
- "이것이 비즈니스에 어떤 영향을 줄까요?"

**2. 구체적이고 실행 가능한**
- "첫 10명의 사용자를 어디서 구할 건가요?"
- "6개월 후 얼마나 많은 사용자를 목표로 하나요?"
- "성공을 어떻게 측정할 건가요?"

**3. 트레이드오프 드러내기**
- "빠른 출시 vs 완성도, 무엇이 더 중요한가요?"
- "많은 기능 vs 단순함, 어떤 것을 선택하시겠어요?"
- "무료 사용자 많이 vs 유료 사용자 적게, 어느 쪽?"

**4. 가정 검증하기**
- "타겟 시장이 크다고 생각하시는 근거는?"
- "사용자가 돈을 낼 거라고 생각하는 이유는?"
- "경쟁사가 없다고 확신하시나요? 어떻게 아셨나요?"

---

### ❌ DON'T Ask

**1. 너무 뻔한 질문**
- ❌ "품질이 중요한가요?" (항상 yes)
- ❌ "사용자 경험이 좋아야 하나요?" (당연함)
- ❌ "성공하고 싶나요?" (의미 없음)

**2. 너무 기술적인 질문**
- ❌ "데이터베이스는 뭘 쓸 건가요?" (spec-interview 영역)
- ❌ "API 설계는?" (spec-interview 영역)
- ❌ "어떤 프레임워크?" (spec-interview 영역)

**3. 너무 추상적인 질문**
- ❌ "비전이 뭔가요?" (구체화 필요)
- ❌ "좋은 제품이란?" (정의가 모호)
- ❌ "혁신적인가요?" (기준 없음)

**4. Yes/No로만 답할 수 있는 질문**
- ❌ "모바일도 지원하나요?"
- ✅ "모바일/웹/데스크톱 중 어디에 우선순위를 두나요? 그 이유는?"

---

## 8. Success Metrics

### Product Metrics

#### Usage
- **Target:** 주 5회 이상 사용
- **Measure:** PRD 생성 완료 수
- **Goal:**
  - Month 1: 10 completed PRDs
  - Month 3: 50 completed PRDs
  - Month 6: 200 completed PRDs

#### Quality
- **Target:** 90% 이상 만족도
- **Measure:** 사용자 피드백 설문 (1-5 scale)
- **Questions:**
  - 질문이 도움이 되었나요?
  - 생성된 PRD가 유용한가요?
  - 다시 사용하시겠어요?

#### Time Saved
- **Target:** 평균 2시간 절약
- **Measure:** "얼마나 시간을 절약했나요?"
- **Baseline:**
  - 수동 PRD 작성: 3-4시간
  - planning-interview: 30-45분

#### Completion Rate
- **Target:** 80% 이상
- **Measure:** 인터뷰 시작 → PRD 생성 완료
- **Tracking:** 중도 이탈 지점 분석

---

### Business Metrics

#### Adoption
- **Target:** spec-interview 사용자의 30% 전환
- **Measure:** planning-interview도 사용하는 사용자 비율

#### Retention
- **Target:** 월 재사용률 60%
- **Measure:** 한 달에 2회 이상 사용

#### Referral
- **Target:** NPS 50+
- **Measure:** "동료에게 추천하시겠어요?"

---

### Leading Indicators

#### Engagement Signals
- ✅ 인터뷰를 끝까지 완료
- ✅ PRD를 다운로드/저장
- ✅ 일주일 내 재사용
- ✅ 다른 프로젝트에도 사용

#### Quality Signals
- ✅ 평균 답변 길이 > 50자
- ✅ "I don't know" 비율 < 30%
- ✅ Follow-up 질문 참여율 > 70%

---

## 9. Implementation Plan

### Phase 1: MVP (Weeks 1-4)

**Goal:** Solo Mode 완벽하게 동작

**Week 1-2: Core Interview Engine**
- [ ] Context detection (Solo/Startup/Team)
- [ ] Question flow logic
- [ ] AskUserQuestion integration
- [ ] Answer analysis & follow-up logic

**Week 3-4: Lean Canvas Generation**
- [ ] Lean Canvas template
- [ ] Data mapping from interview
- [ ] PRD file generation
- [ ] Basic formatting

**Deliverable:**
- 1인 개발자가 15-20분에 Lean Canvas 완성

**Success Criteria:**
- 3명의 1인 개발자 테스트
- 모두 완료 + 만족도 4+ / 5

---

### Phase 2: Expansion (Weeks 5-8)

**Goal:** Startup/Team Mode 추가

**Week 5-6: Startup Mode**
- [ ] 스타트업용 질문 카테고리
- [ ] Product Brief template
- [ ] 팀 정렬 질문
- [ ] 경쟁사 분석 섹션

**Week 7-8: Team Mode**
- [ ] 이해관계자 질문
- [ ] Full PRD template
- [ ] Risk assessment matrix
- [ ] Timeline planner

**Deliverable:**
- 3가지 모드 모두 동작
- 각 모드별 샘플 PRD

**Success Criteria:**
- 각 모드별 2명씩 테스트 (총 6명)
- 평균 만족도 4+ / 5

---

### Phase 3: Polish & Optimization (Weeks 9-12)

**Goal:** 사용자 경험 개선

**Week 9-10:**
- [ ] MoSCoW prioritization helper
- [ ] Persona builder
- [ ] Success metrics advisor
- [ ] Smart follow-up 개선

**Week 11-12:**
- [ ] 문서 품질 개선
- [ ] 한국어 지원 강화
- [ ] 에러 처리
- [ ] 성능 최적화

**Deliverable:**
- Production-ready plugin
- README & documentation
- Example PRDs

---

### Phase 4: Advanced Features (Future)

**Nice to Have:**
- [ ] Resume interview (중단된 인터뷰 이어하기)
- [ ] Batch interview (여러 기능 동시 기획)
- [ ] PRD update (기존 PRD 업데이트)
- [ ] Export formats (PDF, Notion, Confluence)
- [ ] Integration with project management tools

---

## 10. Technical Considerations

### Architecture

```
plugins/planning-interview/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── planning-interview/
│       └── SKILL.md              # Main skill logic
├── templates/
│   ├── lean-canvas.md           # Solo mode template
│   ├── product-brief.md         # Startup mode template
│   └── full-prd.md              # Team mode template
├── examples/
│   ├── solo-example.md
│   ├── startup-example.md
│   └── team-example.md
├── README.md
├── CLAUDE.md                     # Plugin instructions
└── PRD.md                        # This file
```

---

### Skill Logic (SKILL.md)

**Key Sections:**

1. **Context Detection Algorithm**
   ```
   Step 1: Ask 3 context questions
   - Team size?
   - Role?
   - Project stage?

   Step 2: Classify mode
   - Solo: team_size == 1
   - Startup: team_size 2-10
   - Team: team_size > 10

   Step 3: Set question parameters
   - rounds: 3-4 / 4-6 / 6-8
   - depth: basic / medium / advanced
   - template: lean / brief / full
   ```

2. **Question Category Rotation**
   - Solo: Problem → Value → MVP
   - Startup: Business → Market → Strategy → Execution
   - Team: Alignment → Research → Requirements → Metrics → Risks

3. **Follow-up Logic**
   ```
   If answer is vague:
     → Ask for specifics

   If answer contradicts previous:
     → Ask for clarification

   If answer raises concerns:
     → Drill deeper

   If answer is "I don't know":
     → Educate with options
   ```

4. **PRD Generation Logic**
   - Extract key insights from all rounds
   - Map to appropriate template
   - Fill in sections with user's words
   - Add analysis and recommendations
   - Format in markdown

---

### Dependencies

**Required:**
- Claude Code CLI
- AskUserQuestion tool
- Write tool (for saving PRD)

**Optional:**
- Bash (for directory creation)
- Read (for resume interview feature)

---

## 11. Requirements & Dependencies

### Required

- **Claude Code CLI** (latest version recommended)
- **AskUserQuestion tool** (for interactive Q&A)
- **Write tool** (for saving PRD files)

### Optional (for Enhanced Features)

- **spec-interview plugin** - Seamless handoff from planning to technical spec
- **future-architect plugin** - Thought organization before planning
- **Bash tool** - Directory creation and file management

### No Configuration Needed

Works out of the box! ✨ All templates and logic are built-in.

---

## 12. Performance

Expected execution time varies by mode:

| Mode | Rounds | Questions | Time | Output |
|------|--------|-----------|------|--------|
| **Solo** | 3-4 | 6-12 | **15-20 min** | Lean Canvas (1-2 pages) |
| **Startup** | 4-6 | 12-18 | **25-30 min** | Product Brief (3-5 pages) |
| **Team** | 6-8 | 18-24 | **35-45 min** | Full PRD (8-12 pages) |

### Performance Breakdown

| Task | Time | Notes |
|------|------|-------|
| Context Detection | 1-2 min | First round (3 questions) |
| Each Interview Round | 3-5 min | 2-4 questions per round |
| PRD Generation | 2-3 min | Template mapping + formatting |
| **Total (Solo)** | **15-20 min** | Fastest mode |
| **Total (Startup)** | **25-30 min** | Balanced mode |
| **Total (Team)** | **35-45 min** | Most comprehensive |

**Note:** Time varies based on answer complexity and follow-up questions.

---

## 13. Troubleshooting

### "Interview is taking too long"

**Solution:**
- Say "let's wrap up" to skip remaining rounds
- Use Solo mode for faster experience
- Provide shorter, more direct answers

### "Questions are too technical"

**Solution:**
- This means you might have triggered `spec-interview` instead
- Use `/planning-interview` to be explicit
- Say "focus on business questions" to adjust

### "PRD doesn't match my needs"

**Solution:**
- Edit the generated file directly (it's markdown)
- Run interview again with different mode
- Provide more specific context in Round 1

### "I don't know how to answer a question"

**Solution:**
- Say "I don't know" - AI will provide options and education
- Ask for clarification: "Can you rephrase that?"
- Skip and come back: "Let me think about this"

### "Mode classification seems wrong"

**Solution:**
- Override manually: "planning interview (solo mode)"
- Context detection is based on team size - you can correct it
- Provide clear context upfront

### "Can I pause and resume later?"

**Current:** Not supported in MVP

**Future:** Phase 4 will add resume feature

**Workaround:** Save your answers separately and paste when resuming

---

## 14. Data Models

### PRD Output Structure

Each mode generates a different document structure:

#### Lean Canvas (Solo Mode)

```markdown
# [Project Name] - Lean Canvas

> **Generated**: YYYY-MM-DD
> **Mode**: Solo Builder

## 1. Problem
- [Primary problem]
- [Secondary problem]
- [Existing alternatives]

## 2. Solution
- [Unique value proposition]
- [Key features]

## 3. Key Metrics
- North Star: [metric]
- Supporting: [metric 1], [metric 2]

## 4. Unique Value Proposition
[One sentence]

## 5. Unfair Advantage
[What can't be easily copied]

## 6. Channels
- [Channel 1]
- [Channel 2]

## 7. Customer Segments
- Primary: [segment]
- Secondary: [segment]

## 8. Cost Structure
- [Cost 1]
- [Cost 2]

## 9. Revenue Streams
- [Revenue model]

## 10. MVP Scope

### Must Have (Phase 1)
- ✅ [Feature 1]
- ✅ [Feature 2]

### Won't Have (Later)
- ❌ [Feature 3]
- ❌ [Feature 4]

## 11. Next 30 Days

**Week 1:** [Action items]
**Week 2:** [Action items]
**Week 3:** [Action items]
**Week 4:** [Milestone]

---

**Next Step:** Run `/spec-interview` for technical specification
```

---

#### Product Brief (Startup Mode)

```markdown
# [Product Name] - Product Brief

> **Generated**: YYYY-MM-DD
> **Mode**: Startup
> **Team**: [X people]

## 1. Executive Summary
[2-3 paragraphs]

## 2. Problem Statement
[User pain points]

## 3. Target Users & Personas

### Persona 1: [Name]
- Demographics
- Goals
- Pain Points
- Quote

### Persona 2: [Name]
...

## 4. Solution Overview
[Value proposition + key features]

## 5. Feature Prioritization (MoSCoW)

| Feature | Priority | Rationale | Timeline |
|---------|----------|-----------|----------|
| [Feature 1] | Must Have | [Why] | Phase 1 |
| [Feature 2] | Should Have | [Why] | Phase 2 |
...

## 6. User Stories
- As a [user], I want [feature] so that [benefit]

## 7. Success Metrics & KPIs
- North Star: [metric]
- Targets: [specific numbers]

## 8. Timeline & Milestones
- Q1: [milestone]
- Q2: [milestone]

## 9. Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|

## 10. Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

---

**Next Step:** Share with team for alignment
```

---

#### Full PRD (Team Mode)

```markdown
# [Product/Feature Name] - Product Requirements Document

> **Generated**: YYYY-MM-DD
> **Mode**: Team
> **Owner**: [PM name]
> **Status**: Draft

## 1. Executive Summary
[Strategic context + business case]

## 2. Business Goals & Objectives
[Alignment with company OKRs]

## 3. Target Market & Competitive Analysis
[Market size, competitors, positioning]

## 4. User Personas & Research
[Detailed personas with research data]

## 5. Product Vision & Strategy
[Long-term vision + strategic approach]

## 6. Detailed Requirements

### Functional Requirements
FR-1: [Requirement]
- Description
- Priority: P0/P1/P2
- Acceptance Criteria

### Non-Functional Requirements
NFR-1: Performance
NFR-2: Security
...

## 7. Feature Prioritization Framework
[RICE/ICE scores + rationale]

## 8. User Stories & Use Cases
[Detailed user flows]

## 9. Success Metrics & KPIs
[Detailed measurement plan]

## 10. Timeline & Resource Planning
[Gantt chart / phased approach]

## 11. Stakeholder Alignment
[Who needs to approve what]

## 12. Risk Assessment & Mitigation
[Comprehensive risk matrix]

## 13. Go-to-Market Strategy
[Launch plan + marketing]

## 14. Appendix
[Research data, mockups, technical notes]

---

**Next Step:** Stakeholder review → spec-interview → implementation
```

---

## 15. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Users find questions too generic** | Medium | High | Adaptive follow-ups, context-specific questions |
| **Interview takes too long** | Medium | Medium | Strict round limits, smart completion detection |
| **PRD quality inconsistent** | Low | High | Template refinement, user testing, examples |
| **Users don't understand business questions** | Medium | Medium | Educational options, examples in questions |
| **Overlap with spec-interview** | Low | Low | Clear differentiation in docs and triggers |
| **Mode classification wrong** | Low | Medium | Allow manual mode override |

---

## 16. Open Questions

### 🔴 Critical (Must Decide Before MVP)

#### Q1: PRD 저장 위치
**Options:**
- **A)** Current directory (user's project folder)
  - ✅ Pro: PRD stays with project
  - ❌ Con: No central location for all plans

- **B)** Standard location `~/.planning-interview/`
  - ✅ Pro: All plans in one place, versioning
  - ❌ Con: Separated from project files

**Decision:**
→ **Option A** (current directory) for MVP
→ Option B as Phase 4 feature with symlinks

---

#### Q2: spec-interview 연계
**Question:** Seamless handoff from planning to spec?

**Proposal:**
```
User: "Planning done, now I want to build this"
Claude: "Great! Run /spec-interview to create technical spec?"
        [Yes] → Launches spec-interview with PRD context
        [No] → "Run /spec-interview anytime"
```

**Decision:**
→ **Implement in Phase 2** (after both plugins stable)

---

#### Q3: 한국어 지원 우선순위
**Options:**
- **A)** English-only MVP, Korean in Phase 3
- **B)** Bilingual from start (Korean trigger + questions)

**Decision:**
→ **Option B** (bilingual from start)
→ Korean trigger phrases in Phase 1
→ Korean questions in Phase 2
→ Korean PRD templates in Phase 3

---

### 🟡 Important (Phase 2-3)

- [ ] **Mode switching mid-interview?**
  → MVP: No (complexity)
  → Phase 2: "Restart with different mode" option

- [ ] **Multiple projects management?**
  → MVP: Separate files
  → Phase 3: Project index + history

- [ ] **Progress indicator?**
  → MVP: "Round 2/4"
  → Phase 2: Visual progress bar

- [ ] **Edit previous answers?**
  → MVP: No (linear flow)
  → Phase 3: Review & edit mode

---

### 🟢 Nice-to-Know (Phase 4+)

- [ ] Template customization (user-defined sections)
- [ ] Export formats (PDF, Notion, Confluence)
- [ ] Collaborative interviews (multiple stakeholders)
- [ ] PRD versioning and diff
- [ ] Integration with Linear/Jira

---

## 13. Success Criteria (Launch)

### Must Have Before Launch
- [x] Context detection 정확도 95%+
- [ ] Solo mode 완벽 동작
- [ ] Startup mode 완벽 동작
- [ ] Team mode 완벽 동작
- [ ] 3가지 template 모두 고품질
- [ ] 10명 이상 베타 테스트 완료
- [ ] 평균 만족도 4+ / 5
- [ ] README & documentation 완성
- [ ] 3개 이상 example PRDs

### Nice to Have
- [ ] 한국어 trigger phrases
- [ ] Resume interview
- [ ] MoSCoW helper
- [ ] Persona builder

---

## 14. Competitive Analysis

### vs spec-interview (Internal)
**Differentiation:**
- planning = "왜" (why), spec = "어떻게" (how)
- planning = 기획자/창업자, spec = 개발자
- planning = 비즈니스, spec = 기술
- **결론:** 상호 보완적, 경쟁 아님

### vs Notion/Confluence
**우리 강점:**
- 빈 페이지 문제 해결 (AI가 질문)
- 맞춤형 (컨텍스트 기반)
- 빠름 (30분)
- 학습 효과 (질문을 통해 배움)

### vs PRD Templates
**우리 강점:**
- 인터랙티브 (정적 템플릿 vs 동적 인터뷰)
- 맞춤형 (일반적 템플릿 vs 상황별)
- 가이드 (혼자 쓰기 vs AI 도움)

### vs Product Coach/Consultant
**우리 강점:**
- 항상 이용 가능 (24/7)
- 무료 (vs $$$)
- 빠름 (30분 vs 수 시간)
- 일관성 (프레임워크 기반)

---

## 15. Go-to-Market Strategy

### Target Channels

#### 1. Claude Code Marketplace
- Primary distribution
- Searchable by keywords: planning, interview, PRD, product
- Star spec-interview users

#### 2. Communities
- **Indie Hackers**: 1인 개발자 집중
- **r/SideProject**: Reddit community
- **Product Hunt**: Launch showcase
- **Dev.to**: Technical writers

#### 3. Content Marketing
- Blog: "How to Plan Your Product in 30 Minutes"
- Tutorial: "Solo Founder's Guide to PRD"
- Comparison: "Planning Interview vs Manual PRD"

#### 4. Social Proof
- Example PRDs from real projects
- Testimonials from beta users
- Case studies

---

### Launch Plan

**Week 1: Soft Launch**
- Beta test with 10 users
- Gather feedback
- Fix critical issues

**Week 2: Internal Launch**
- Announce in claude-code community
- Get early adopters

**Week 3: Public Launch**
- Product Hunt launch
- Reddit posts
- Twitter announcement

**Week 4+: Growth**
- Content marketing
- Community engagement
- Iterate based on feedback

---

## 16. Appendix

### Related Documents
- [spec-interview Plugin](../spec-interview/)
- [future-architect Plugin](../future-architect/)

### References
- Lean Canvas: https://leanstack.com/lean-canvas
- MoSCoW Method: https://en.wikipedia.org/wiki/MoSCoW_method
- RICE Prioritization: https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/

### Interview Notes
- Based on successful patterns from spec-interview
- Inspired by YC's guidance on product planning
- Adapted from real PM workflows

---

## Changelog

### v1.0.0 (2026-02-14)
- Initial PRD
- Defined adaptive interview approach
- 3 modes: Solo / Startup / Team
- 3 templates: Lean Canvas / Product Brief / Full PRD

---

**Next Steps:**
1. [ ] Review this PRD with stakeholders
2. [ ] Create SKILL.md with detailed algorithm
3. [ ] Build MVP (Solo mode first)
4. [ ] Beta test with 3 solo developers
5. [ ] Iterate and expand to Startup/Team modes

---

_This PRD was created using the planning-interview approach itself (meta!)_
