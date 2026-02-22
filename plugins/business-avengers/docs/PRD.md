# Business Avengers - Product Requirements Document (PRD)

> **Document Status**: Draft v2.0 (Feedback Incorporated)
> **Date**: 2026-02-21
> **Mode**: Solo (1인 기업가)
> **Plugin Name**: `business-avengers`

---

## 1. Executive Summary

**Business Avengers**는 1인 기업가(CEO)가 온라인 서비스를 구상부터 수익화까지 E2E로 실행할 수 있도록, 실제 회사의 조직 구조와 업무 프로세스를 AI 에이전트 조직으로 **구현**한 Claude Code 플러그인입니다.

각 에이전트는 실제 전문가처럼 전문 스킬과 판단력을 가지고 업무를 수행하며, CEO(사용자)는 의사결정에 집중합니다. 이것은 시뮬레이션이 아니라, **실제로 문서를 작성하고, 시장을 조사하고, 전략을 수립하는 AI 파트너 조직**입니다.

**핵심 차별화**:

| | MetaGPT | ChatDev | **Business Avengers** |
|---|---|---|---|
| 범위 | 소프트웨어 개발 | 소프트웨어 개발 | **전체 비즈니스 운영** |
| 수익화 | 없음 | 없음 | **핵심 목표** |
| 반복 개선 | 단일 실행 | 단일 실행 | **스프린트 사이클** |
| Phase 유연성 | 고정 순서 | 고정 순서 | **완전 유연** |
| 사용자 역할 | 요구사항 입력자 | 요구사항 입력자 | **CEO (의사결정자)** |

### 인터뷰 확정 요구사항

| 항목 | 결정 |
|------|------|
| 서비스 범위 | **범용** (모든 온라인 서비스) |
| 자율성 수준 | **하이브리드** (전략=CEO승인, 실행=위임) |
| 조직 범위 | **전체 조직 한번에** (리서치 기반 최적 구성) |
| 호출 방식 | **오케스트라 + 부서 직접 호출 모두** |
| 산출물 저장 | **전용 프로젝트 폴더** (`~/.business-avengers/projects/`) |
| 프로젝트 수 | **단일 프로젝트 집중** |
| 코드 작성 | **단계적** (MVP는 문서, 향후 코드 생성) |
| 시장 분석 | **실시간 웹 리서치** (WebSearch/WebFetch) |
| Phase 순서 | **완전 유연** (CEO가 원하는 순서로 조합 가능) |
| 반복 개선 | **스프린트 사이클** (변경된 Phase만 재실행, 문서 버전 관리) |
| 비용 | **Claude Max 구독 포함** (추가 API 비용 없음) |

---

## 2. Problem Statement

1인 기업가가 온라인 서비스를 만들 때의 현실:
- 기획, 디자인, 개발, 마케팅, 재무를 **혼자** 해야 함
- 전문성 부족한 영역에서 **치명적 실수** 발생 (예: 수익 모델 없이 개발 시작)
- "만들고 보자" 접근 → 시장 검증 없이 시간/돈 낭비
- 각 단계의 산출물이 체계적으로 관리되지 않음
- AI 도구를 써도 **단편적** (ChatGPT에 마케팅 물어보고, Claude에 코드 물어보고...)
- 한 번 만들고 끝이 아니라 **지속적 개선**이 필요한데, 체계가 없음

**필요한 것**: 실제 스타트업처럼 각 분야 전문가들이 체계적으로 협업하며, CEO(사용자)는 의사결정에만 집중할 수 있는 **AI 경영 파트너 조직**.

---

## 3. Organization Structure (조직 구조)

### 3.1 조직도 (리서치 기반 최적 구성)

리서치 결과, SaaS/온라인 서비스 회사의 핵심 부서는 다음과 같습니다:
- 참고: [SaaS Org Chart Guide](https://theorgchart.com/saas-company-org-charts/), [RevPartners](https://blog.revpartners.io/en/revops-articles/organizational-structure-of-saas-companies)

```
                              CEO (사용자)
                                  │
          ┌───────────┬───────────┼───────────┬───────────┐
          │           │           │           │           │
        [CPO]       [CTO]      [CMO]       [CFO]       [COO]
       제품총괄    기술총괄    마케팅총괄   재무총괄    운영총괄
          │           │           │           │           │
    ┌─────┤     ┌─────┼─────┐   ┌┼────┐   ┌──┤──┐    ┌──┤──┐
    │     │     │     │     │   ││    │   │     │    │     │
  [PM]  [UXR] [TL] [FE]  [BE] [MS] [CC] [BA] [RS] [LG] [DA]
  기획   UX   기술  프론트 백엔드 전략 콘텐츠 비즈  수익  법무  데이터
        리서치 리드  엔드   엔드       마케팅 분석  전략  컴플  분석
                │                │
          ┌─────┤          ┌────┤
          │     │          │    │
       [DvO]  [QA]       [GH] [PR]
       배포    품질       그로스 홍보

 별도: [UI] UI디자이너 (CPO)  [CS] CS매니저 (COO)  [DL] 디자인리드 (CPO)
```

### 3.2 에이전트 상세 목록 (24개)

| ID | 역할 | 소속 | 핵심 도구 | 전문 스킬 |
|----|------|------|----------|----------|
| **C-Level (5)** |||||
| `cpo` | Chief Product Officer | CEO | Read, WebSearch | 제품 전략, 로드맵, PMF 판단 |
| `cto` | Chief Technology Officer | CEO | Read, Bash, Glob, Grep | 기술 전략, 아키텍처 리뷰, 기술 부채 관리 |
| `cmo` | Chief Marketing Officer | CEO | Read, WebSearch, WebFetch | GTM 전략, 브랜드 전략, 채널 믹스 |
| `cfo` | Chief Financial Officer | CEO | Read, WebSearch | 재무 계획, 투자 전략, 리스크 관리 |
| `coo` | Chief Operating Officer | CEO | Read, Write | 운영 효율, 프로세스 최적화, 법무/컴플라이언스 |
| **Product Team (3)** |||||
| `product-manager` | 제품 기획, PRD 작성 | CPO | Read, Write, WebSearch | User Story 작성, MoSCoW 우선순위, 백로그 관리 |
| `ux-researcher` | 사용자 조사, 페르소나 | CPO | Read, Write, WebSearch | 페르소나 프레임워크, 사용자 여정 맵, 설문 설계 |
| `design-lead` | 디자인 전략, 브랜딩 | CPO | Read, Write | 디자인 시스템, 브랜드 가이드, 접근성(WCAG) |
| **Design Team (1)** |||||
| `ui-designer` | UI 스펙, 와이어프레임 | CPO | Read, Write | 와이어프레임, 컴포넌트 명세, 인터랙션 패턴 |
| **Engineering Team (4)** |||||
| `tech-lead` | 아키텍처, 기술 스택 | CTO | Read, Write, Glob, Grep | 시스템 설계, API 설계, DB 스키마, 기술 스택 평가 |
| `frontend-dev` | 프론트엔드 구현 가이드 | CTO | Read, Write, Glob | React/Next.js 패턴, 상태 관리, 성능 최적화 |
| `backend-dev` | 백엔드 구현 가이드 | CTO | Read, Write, Glob | FastAPI/Node.js 패턴, DB 설계, 인증/보안 |
| `devops-engineer` | 인프라, 배포 전략 | CTO | Read, Write, Bash | CI/CD, Docker, 클라우드 아키텍처, 모니터링 |
| **QA Team (1)** |||||
| `qa-lead` | 테스트 전략, 품질 관리 | CTO | Read, Write | 테스트 피라미드, E2E 테스트 전략, 품질 메트릭 |
| **Marketing Team (4)** |||||
| `marketing-strategist` | GTM, 채널 전략 | CMO | Read, Write, WebSearch, WebFetch | SWOT 분석, 포지셔닝 맵, 마케팅 퍼널, CAC/LTV |
| `content-creator` | 콘텐츠 마케팅, 카피 | CMO | Read, Write, WebSearch | SEO 콘텐츠, 카피라이팅(AIDA), 소셜미디어 전략 |
| `growth-hacker` | 성장 전략, 퍼널 분석 | CMO | Read, Write, WebSearch | A/B 테스트 설계, 바이럴 루프, 리텐션 전략 |
| `pr-manager` | 홍보, 미디어 관계 | CMO | Read, Write, WebSearch | 보도자료 작성, 위기 관리, 미디어 리스트, 브랜드 보이스 |
| **Finance Team (2)** |||||
| `business-analyst` | 시장 분석, 경쟁 분석 | CFO | Read, Write, WebSearch, WebFetch | TAM/SAM/SOM, Porter's Five Forces, 경쟁사 매트릭스 |
| `revenue-strategist` | 수익 모델, 가격 전략 | CFO | Read, Write, WebSearch | 가격 전략 프레임워크, Unit Economics, 재무 모델링 |
| **Operations Team (3)** |||||
| `legal-advisor` | 법무, 컴플라이언스 | COO | Read, Write, WebSearch | 이용약관, 개인정보처리방침, IP 보호, 규제 확인 |
| `data-analyst` | 데이터 분석, 메트릭 | COO | Read, Write, WebSearch | KPI 설계, 대시보드 설계, 코호트 분석, 퍼널 분석 |
| `cs-manager` | CS 전략, FAQ 설계 | COO | Read, Write | CS 플레이북, FAQ 설계, 피드백 루프, NPS 설계 |

### 3.3 에이전트 전문 스킬 (Agent Skills)

각 에이전트는 자신의 .md 파일 내에 **전문 프레임워크와 방법론**이 내장됩니다:

```markdown
# 예시: business-analyst.md 내 전문 스킬 섹션

## Expert Frameworks
1. **TAM/SAM/SOM Calculator**: 시장 규모 산정 프레임워크
   - TAM: 전체 시장 규모 (top-down + bottom-up)
   - SAM: 접근 가능 시장 (지역, 채널 필터)
   - SOM: 획득 가능 시장 (경쟁력 기반)

2. **Porter's Five Forces**: 산업 경쟁 분석
   - 신규 진입 위협, 대체재 위협, 구매자 교섭력, 공급자 교섭력, 기존 경쟁

3. **Competitor Matrix Builder**: 경쟁사 비교 분석
   - 기능, 가격, 타겟, 강점/약점을 매트릭스로 정리

## Output Format
반드시 다음 구조로 출력:
- Executive Summary (3줄)
- 상세 분석 (프레임워크별)
- 데이터 출처 (WebSearch 결과 링크)
- CEO를 위한 핵심 인사이트 (3-5개)
- 추천 액션 (우선순위순)
```

knowledge/ 디렉토리의 파일들이 에이전트의 "교육 자료" 역할:

| Knowledge File | 내용 | 사용 에이전트 |
|---|---|---|
| `business-models.md` | SaaS, 마켓플레이스, 프리미엄, 광고 등 15+ 수익 모델 | revenue-strategist, cfo, business-analyst |
| `pricing-strategies.md` | 가치기반, 경쟁기반, 원가기반 등 가격 프레임워크 | revenue-strategist, cfo |
| `marketing-playbooks.md` | SEO, SNS, 유료광고, 이메일, 콘텐츠 등 채널별 전략 | marketing-strategist, content-creator, growth-hacker, pr-manager |
| `startup-best-practices.md` | 린 스타트업, MVP, PMF, 피봇 원칙 | cpo, product-manager |
| `ux-principles.md` | 닐슨 10 원칙, 접근성, 모바일 퍼스트 | ux-researcher, design-lead, ui-designer |
| `tech-stack-guide.md` | 서비스 유형별 권장 기술 스택 | cto, tech-lead |
| `legal-templates.md` | 이용약관, 개인정보처리방침, 저작권 가이드 | legal-advisor |
| `data-metrics-guide.md` | KPI 설계, 핵심 메트릭 (AARRR, NPS 등) | data-analyst, growth-hacker |

### 3.4 에이전트 간 커뮤니케이션 맵

에이전트는 직접 통신하지 않습니다. 대신 **구조화된 문서**를 통해 협업합니다 (MetaGPT의 검증된 패턴):

```
[Phase N Output 문서] → 오케스트레이터(SKILL.md) → [Phase N+1 Input으로 전달]
```

**핵심 협업 관계**:

| From | To | 협업 내용 | 방식 |
|------|-----|----------|------|
| product-manager | ux-researcher | 기능 요구사항 ↔ 사용자 니즈 | 동일 Phase 병렬 → 결과 교차 참조 |
| product-manager | design-lead | PRD → 디자인 방향 | Phase 순차 (PRD 승인 후 디자인) |
| design-lead | ui-designer | 디자인 시스템 → UI 스펙 | 동일 Phase 순차 |
| tech-lead | frontend-dev, backend-dev | 아키텍처 → 구현 가이드 | 동일 Phase (TL 먼저 → FE/BE 병렬) |
| marketing-strategist | content-creator, pr-manager | 전략 → 콘텐츠/홍보 방향 | 동일 Phase 순차 |
| business-analyst | revenue-strategist | 시장 데이터 → 수익 모델 | 동일 Phase 병렬 → 결과 종합 |
| data-analyst | growth-hacker | 메트릭 설계 → 성장 실험 | Phase 순차 |
| legal-advisor | product-manager | 법적 제약 → 기능 설계 반영 | Phase 순차 |

---

## 4. Workflow Phases (업무 흐름)

### 4.1 유연한 Phase 시스템

Phase 순서는 **고정이 아닙니다**. CEO가 상황에 맞게 자유롭게 조합할 수 있습니다.

**프리셋 모드 (Preset Workflows)**:

| 모드 | 순서 | 적합한 상황 |
|------|------|------------|
| **아이디어 우선** | Ideation → Market → Planning → Design → Tech → Dev → QA → Launch → Monetization → Ops | CEO가 이미 아이디어가 있을 때 |
| **시장 우선** | Market Research → Ideation → Planning → Design → Tech → ... | 시장 기회를 먼저 파악하고 아이디어를 도출할 때 |
| **MVP 빌드** | Ideation → Planning → Tech → Dev → Launch | 빠른 검증이 필요할 때 (디자인/QA 생략) |
| **커스텀** | CEO가 원하는 Phase를 자유롭게 선택/조합 | 특정 단계만 필요할 때 |

### 4.2 Phase 목록 (10개)

각 Phase는 독립적으로 실행 가능하며, 이전 Phase 산출물이 있으면 자동으로 참조합니다.

| Phase | 이름 | 리드 | 실행 에이전트 | CEO 개입 | 핵심 산출물 |
|:-----:|------|------|-------------|:--------:|-----------|
| 0 | **Ideation** | CPO | PM, UXR | 대화형 | idea-canvas.md |
| 1 | **Market Research** | CFO | BA, MS, RS | 승인 | market-analysis.md, competitive-analysis.md, revenue-model-draft.md |
| 2 | **Product Planning** | CPO | PM, UXR | 승인 | prd.md, user-personas.md, user-stories.md, feature-priority.md |
| 3 | **Design** | CPO | DL, UI | 승인 | design-system.md, wireframes.md, ui-specifications.md |
| 4 | **Technical Planning** | CTO | TL | 위임+보고 | tech-architecture.md, api-design.md, database-schema.md |
| 5 | **Development Guide** | CTO | FE, BE, DvO | 확인 | frontend-guide.md, backend-guide.md, deployment-strategy.md |
| 6 | **QA Planning** | CTO | QA | 확인 | test-plan.md, qa-checklist.md |
| 7 | **Launch Strategy** | CMO | MS, CC, GH, PR | 승인 | gtm-strategy.md, content-plan.md, growth-strategy.md, pr-plan.md |
| 8 | **Monetization** | CFO | RS, BA | 승인 | pricing-strategy.md, financial-projections.md, unit-economics.md |
| 9 | **Operations** | COO | CS, LG, DA | 확인 | cs-playbook.md, legal-docs.md, metrics-dashboard.md |

**CEO 개입 레벨**:
- **대화형**: CEO와 에이전트가 Q&A로 함께 작업 (Phase 0)
- **승인**: 산출물 리뷰 후 승인/수정/피봇/중단 선택
- **위임+보고**: C-Level이 자율 판단, CEO에게 결과 보고
- **확인**: CEO가 결과물 확인 후 자동 진행

### 4.3 Phase 상세 (핵심 Phase만)

#### Phase 0: Ideation

**인터랙션 흐름**:
1. CEO가 아이디어를 자유롭게 설명 (또는 "시장 먼저 보고 싶다"고 요청)
2. CPO가 핵심 질문 5-7개를 순차적으로 질문 (AskUserQuestion)
   - 해결하는 문제는? / 타겟 사용자는? / 기존 대안은? / 차별점은? / 수익은?
3. product-manager가 답변을 종합하여 Idea Canvas 초안 작성
4. CEO에게 초안 제시 → 피드백 반영 → 승인

#### Phase 1: Market Research

**에이전트 병렬 실행**:
```
business-analyst     → TAM/SAM/SOM, 시장 트렌드, 성장률 (WebSearch)
marketing-strategist → 경쟁사 5개 분석, SWOT, 포지셔닝 맵 (WebSearch + WebFetch)
revenue-strategist   → 수익 모델 3-5개 제안, 벤치마크 가격 (WebSearch)
```

**CEO 승인 시 선택지**:
- 진행 (시장성 확인)
- 피봇 (방향 전환 → Phase 0으로 돌아감)
- 중단 (시장성 부족)

#### Phase 9: Operations (확장됨)

**에이전트 3개 병렬 실행**:
```
cs-manager    → CS 플레이북, FAQ, 피드백 수집 설계
legal-advisor → 이용약관, 개인정보처리방침, 저작권 (WebSearch로 최신 규제 확인)
data-analyst  → KPI 대시보드 설계, 핵심 메트릭 정의 (AARRR 프레임워크)
```

---

## 5. Sprint Cycle (스프린트 사이클)

### 5.1 왜 스프린트가 필요한가

실제 제품은 한 번의 라운드로 완성되지 않습니다:
- 출시 후 사용자 피드백 → 기획 문서 업데이트 → 재개발
- 시장 변화 → 마케팅 전략 수정
- 새로운 기능 추가 → 기술 설계 업데이트

### 5.2 스프린트 흐름

```
Sprint N:
  1. Sprint Planning (CEO + 관련 C-Level)
     └── "이번 스프린트에서 뭘 할까?"
     └── 변경이 필요한 Phase들 선택

  2. Phase 실행 (변경된 Phase만 재실행)
     └── 기존 산출물을 읽고, 변경사항을 반영하여 업데이트
     └── 새 버전으로 저장 (v1.0 → v1.1)

  3. Sprint Review (CEO)
     └── 이번 스프린트 산출물 리뷰
     └── 다음 스프린트 방향 결정

  4. Sprint Retrospective (자동)
     └── 변경 이력 기록 (changelog)
```

**호출 방식**:
```
/business-avengers sprint "사용자 피드백 반영: 온보딩 플로우 개선"
/business-avengers sprint "새 기능 추가: 소셜 로그인"
```

### 5.3 문서 버전 관리

```
phase-2-product-planning/
├── prd.md                    # 항상 최신 버전 (현재 v1.2)
├── history/
│   ├── prd-v1.0-2026-02-21.md   # 최초 버전
│   ├── prd-v1.1-2026-03-01.md   # Sprint 2: 온보딩 개선 반영
│   └── prd-v1.2-2026-03-15.md   # Sprint 3: 소셜 로그인 추가
└── changelog.md              # 변경 이력 추적
```

**changelog.md 예시**:
```markdown
# PRD Changelog

## v1.2 (2026-03-15) - Sprint 3
- 추가: 소셜 로그인 기능 (Google, Apple)
- 수정: 온보딩 플로우 3단계 → 2단계로 간소화
- 관련 Phase: Phase 2 (기획), Phase 4 (기술 설계)

## v1.1 (2026-03-01) - Sprint 2
- 수정: 온보딩 플로우 개선 (사용자 피드백 반영)
- 추가: 튜토리얼 모달 기능
```

### 5.4 스프린트 실행 시 에이전트 동작

에이전트가 기존 문서를 **업데이트**할 때:
1. 기존 문서(prd.md)를 Read로 읽음
2. 변경 요청 사항을 분석
3. 기존 문서의 전체 맥락을 유지하면서 변경사항만 반영
4. 변경 전 문서를 history/에 백업
5. 업데이트된 문서를 prd.md로 저장
6. changelog.md에 변경 이력 추가

---

## 6. Interaction Model (인터랙션 모델)

### 6.1 호출 방식

**A. 오케스트라 모드 (전체 흐름)**
```
/business-avengers new "배달 음식 리뷰 큐레이션 앱"
/business-avengers new --mode market-first "어떤 시장 기회가 있을까?"
/business-avengers new --mode mvp-build "빠르게 MVP 만들기"
```

**B. 직접 호출 모드 (특정 Phase/부서)**
```
/business-avengers phase market-research     → Phase 1만 실행
/business-avengers phase design              → Phase 3만 실행
/business-avengers ask cto "기술 스택 추천해줘"  → CTO에게 직접 질문
/business-avengers ask marketing "SNS 전략 짜줘" → 마케팅팀에 직접 요청
/business-avengers ask legal "이용약관 필요한 항목은?" → 법무 자문
```

**C. 스프린트 모드 (반복 개선)**
```
/business-avengers sprint "사용자 피드백: 온보딩이 복잡하다"
/business-avengers sprint "새 기능: 결제 시스템 추가"
```

**D. 상태 관리**
```
/business-avengers status     → 현재 프로젝트 진행 상황 + 문서 버전
/business-avengers resume     → 중단된 Phase부터 재개
/business-avengers history    → 스프린트 히스토리 + 변경 이력
```

### 6.2 CEO 승인 메커니즘

각 Phase/Sprint 종료 시 AskUserQuestion:
- **승인 (Approve)**: 다음 단계로 진행
- **수정 요청 (Revise)**: 구체적 피드백 반영 후 재작업
- **피봇 (Pivot)**: 방향 전환 (다른 Phase로 이동)
- **중단 (Stop)**: 프로젝트 중단 (모든 산출물 보존)

---

## 7. Data Model (데이터 구조)

### 7.1 프로젝트 디렉토리 구조

```
~/.business-avengers/
├── config.yaml                          # 글로벌 설정
├── projects/
│   └── {project-slug}/                  # 예: food-review-curation
│       ├── project.yaml                 # 프로젝트 메타데이터
│       ├── sprints/                     # 스프린트 히스토리
│       │   ├── sprint-001.yaml
│       │   └── sprint-002.yaml
│       ├── phase-0-ideation/
│       │   ├── idea-canvas.md           # 항상 최신 버전
│       │   ├── history/                 # 이전 버전 아카이브
│       │   └── changelog.md
│       ├── phase-1-market-research/
│       │   ├── market-analysis.md
│       │   ├── competitive-analysis.md
│       │   ├── revenue-model-draft.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-2-product-planning/
│       │   ├── prd.md
│       │   ├── user-personas.md
│       │   ├── user-stories.md
│       │   ├── feature-priority.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-3-design/
│       │   ├── design-system.md
│       │   ├── wireframes.md
│       │   ├── ui-specifications.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-4-tech-planning/
│       │   ├── tech-architecture.md
│       │   ├── api-design.md
│       │   ├── database-schema.md
│       │   ├── tech-stack-decision.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-5-development/
│       │   ├── frontend-guide.md
│       │   ├── backend-guide.md
│       │   ├── deployment-strategy.md
│       │   ├── implementation-roadmap.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-6-qa/
│       │   ├── test-plan.md
│       │   ├── qa-checklist.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-7-launch/
│       │   ├── gtm-strategy.md
│       │   ├── content-plan.md
│       │   ├── growth-strategy.md
│       │   ├── pr-plan.md
│       │   ├── launch-checklist.md
│       │   ├── history/
│       │   └── changelog.md
│       ├── phase-8-monetization/
│       │   ├── pricing-strategy.md
│       │   ├── financial-projections.md
│       │   ├── unit-economics.md
│       │   ├── history/
│       │   └── changelog.md
│       └── phase-9-operations/
│           ├── cs-playbook.md
│           ├── faq-template.md
│           ├── legal-docs.md
│           ├── metrics-dashboard.md
│           ├── feedback-loop.md
│           ├── history/
│           └── changelog.md
└── templates/                           # 재사용 가능한 템플릿
```

### 7.2 프로젝트 상태 관리 (`project.yaml`)

```yaml
name: "Food Review Curation App"
slug: food-review-curation
created: 2026-02-21
updated: 2026-03-15
status: in_progress
current_sprint: 3
workflow_mode: idea-first    # idea-first | market-first | mvp-build | custom

phases:
  0: { status: completed, version: "1.0", completed_at: "2026-02-21" }
  1: { status: completed, version: "1.1", completed_at: "2026-02-21" }
  2: { status: completed, version: "1.2", completed_at: "2026-03-15" }
  3: { status: completed, version: "1.0", completed_at: "2026-02-22" }
  4: { status: in_progress, version: "1.1", started_at: "2026-03-15" }
  5: { status: pending }
  6: { status: pending }
  7: { status: completed, version: "1.0", completed_at: "2026-02-23" }
  8: { status: completed, version: "1.0", completed_at: "2026-02-23" }
  9: { status: pending }

sprints:
  1: { goal: "Initial E2E", phases: [0,1,2,3,4,7,8], completed: "2026-02-23" }
  2: { goal: "온보딩 개선", phases: [2,3], completed: "2026-03-01" }
  3: { goal: "소셜 로그인 추가", phases: [2,4], in_progress: true }

ceo_decisions:
  - sprint: 1
    phase: 0
    decision: approved
    notes: "타겟을 20-30대 1인 가구로 좁힘"
    date: "2026-02-21"
  - sprint: 3
    phase: 2
    decision: approved
    notes: "Google + Apple 소셜 로그인 추가"
    date: "2026-03-15"
```

---

## 8. Technical Architecture (기술 구현)

### 8.1 플러그인 구조

```
plugins/business-avengers/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── business-avengers/
│       └── SKILL.md                    # 메인 오케스트레이터
├── agents/                             # 24개 에이전트 정의
│   ├── cpo.md
│   ├── cto.md
│   ├── cmo.md
│   ├── cfo.md
│   ├── coo.md
│   ├── product-manager.md
│   ├── ux-researcher.md
│   ├── design-lead.md
│   ├── ui-designer.md
│   ├── tech-lead.md
│   ├── frontend-dev.md
│   ├── backend-dev.md
│   ├── devops-engineer.md
│   ├── qa-lead.md
│   ├── marketing-strategist.md
│   ├── content-creator.md
│   ├── growth-hacker.md
│   ├── pr-manager.md
│   ├── business-analyst.md
│   ├── revenue-strategist.md
│   ├── legal-advisor.md
│   ├── data-analyst.md
│   └── cs-manager.md
├── templates/                          # 35+ 산출물 템플릿
│   ├── idea-canvas.md
│   ├── market-analysis.md
│   ├── ... (Phase별 모든 산출물)
│   └── feedback-loop.md
├── knowledge/                          # 8개 도메인 지식 베이스
│   ├── business-models.md
│   ├── pricing-strategies.md
│   ├── marketing-playbooks.md
│   ├── startup-best-practices.md
│   ├── ux-principles.md
│   ├── tech-stack-guide.md
│   ├── legal-templates.md
│   └── data-metrics-guide.md
├── config/
│   ├── org-structure.yaml
│   └── init-project.py
├── README.md
└── CLAUDE.md
```

### 8.2 오케스트레이션 패턴 (SKILL.md)

```
Step 1: 트리거 감지 + 모드 결정
        - "new" → 오케스트라 모드
        - "new --mode market-first" → 시장 우선 모드
        - "phase {name}" → 단일 Phase 실행
        - "sprint {goal}" → 스프린트 모드
        - "ask {agent} {question}" → 직접 대화
        - "status" / "resume" / "history" → 상태 관리

Step 2: 프로젝트 초기화 또는 로드
        - new: project.yaml + 디렉토리 생성
        - sprint/phase/resume: project.yaml 로드

Step 3: 워크플로우 모드에 따라 Phase 순서 결정
        - idea-first: [0,1,2,3,4,5,6,7,8,9]
        - market-first: [1,0,2,3,4,5,6,7,8,9]
        - mvp-build: [0,2,4,5,7]
        - custom: CEO가 선택

Step 4-13: Phase 실행 (순서대로)
        - 해당 Phase의 에이전트를 Task()로 호출
        - 이전 Phase 산출물이 있으면 Read로 참조하여 input에 포함
        - sprint 모드면: 기존 문서를 Read → 변경사항 반영 → 버전 업데이트
        - 각 Phase 후 CEO 인터랙션 (승인 레벨에 따라)

Step 14: 완료 처리
        - project.yaml 업데이트
        - 전체 요약 보고서 생성 (new 모드)
        - changelog 업데이트 (sprint 모드)
```

### 8.3 비용

**Claude Max 구독 사용 시: 추가 API 비용 없음.**

Claude Max에서는 Claude Code의 모든 기능(Task 서브에이전트 포함)이 구독료에 포함됩니다.

**예상 소요 시간**:
| 모드 | 에이전트 호출 수 | 예상 시간 (에이전트 처리) | 인터랙션 포함 |
|------|---------------|---------------------|-------------|
| E2E (idea-first) | ~24 | 30-50분 | 1-2시간 |
| MVP Build | ~10 | 15-25분 | 30-60분 |
| 단일 Phase | 1-4 | 3-10분 | 5-15분 |
| Sprint (2-3 Phase) | 5-10 | 15-25분 | 30-60분 |
| Ask (직접 질문) | 1 | 1-3분 | 5분 |

---

## 9. Constraints & Risk Mitigation

### 기술적 제약

| 제약 | 완화 전략 |
|------|----------|
| 에이전트 간 직접 통신 불가 | 구조화된 문서 기반 커뮤니케이션 (MetaGPT 패턴) |
| Context window 제한 | 각 Phase 산출물을 파일로 저장, 필요 시 Read |
| 24개 에이전트 처리 시간 | Phase별 병렬 실행 + 필요 없는 Phase 스킵 |
| 웹 리서치 정확도 | CEO 검증 게이트에서 교차 확인 |
| 문서 버전 충돌 | changelog 기반 추적 + history/ 백업 |

### 실행 리스크

| 리스크 | 대응 |
|--------|------|
| Phase 간 산출물 불일치 | 각 Phase에서 이전 산출물을 input으로 명시적 참조 |
| CEO 인터랙션 과다 | 하이브리드 자율성: 실행 단계는 위임, 전략만 승인 |
| 스프린트 시 문서 일관성 깨짐 | 에이전트가 전체 문서를 읽은 후 부분 업데이트 |
| 프로젝트 중단 후 재개 | project.yaml에 상태 저장, resume으로 복구 |

---

## 10. Implementation Plan

### Step 1: 플러그인 기반 구조 (Week 1)
- [ ] 플러그인 디렉토리 구조 생성 (`plugins/business-avengers/`)
- [ ] plugin.json, CLAUDE.md, README.md 작성
- [ ] org-structure.yaml 정의
- [ ] init-project.py (프로젝트/스프린트 초기화 스크립트) 작성
- [ ] config.yaml 기본 설정

### Step 2: Knowledge Base & Templates (Week 1-2)
- [ ] 8개 knowledge base 문서 작성
- [ ] 35+ 산출물 템플릿 작성

### Step 3: 에이전트 정의 (Week 2)
- [ ] 24개 에이전트 .md 파일 작성
- [ ] 각 에이전트별 전문 스킬/프레임워크 프롬프트 작성
- [ ] 에이전트별 output format 정의

### Step 4: SKILL.md 오케스트레이터 (Week 2-3)
- [ ] 메인 오케스트레이터 로직 (트리거 감지, 모드 결정)
- [ ] Phase 실행 로직 (10개 Phase)
- [ ] 유연한 Phase 순서 지원 (프리셋 + 커스텀)
- [ ] CEO 인터랙션 로직 (승인/수정/피봇/중단)
- [ ] 스프린트 사이클 로직 (문서 버전 관리)
- [ ] 직접 호출 모드 (ask + phase)
- [ ] 상태 관리 (status/resume/history)

### Step 5: 테스트 & 검증 (Week 3)
- [ ] E2E 테스트: 전체 Phase 실행
- [ ] Sprint 테스트: 기존 프로젝트에 변경사항 반영
- [ ] 직접 호출 테스트: 개별 Phase/에이전트
- [ ] Resume 테스트: 중단 후 재개
- [ ] 에이전트 출력 품질 검증 및 프롬프트 튜닝

### Verification
- `/business-avengers new "테스트 서비스"` → Phase 0-9 전체 실행, 모든 산출물 생성 확인
- `/business-avengers sprint "기능 추가"` → 기존 문서 업데이트 + 버전 관리 확인
- `/business-avengers ask cto "기술 추천"` → 직접 대화 동작 확인
- `/business-avengers resume` → 중단점부터 재개 확인
- 산출물 품질: 각 문서가 전문가 수준의 프레임워크 기반인지 확인

---

## 11. Future Roadmap

| Version | Feature |
|---------|---------|
| **v1.0** | 문서 중심 E2E 파이프라인 + 스프린트 사이클 (현재 PRD) |
| **v1.1** | 에이전트 프롬프트 튜닝 + 템플릿 품질 개선 |
| **v2.0** | 개발 에이전트 실제 코드 생성 (React + Python/Node.js) |
| **v2.1** | 디자인 에이전트 HTML/CSS mockup 생성 |
| **v3.0** | 멀티 프로젝트 포트폴리오 관리 |
| **v4.0** | 실제 배포 자동화 (Vercel, AWS 연동) |
| **v5.0** | 에이전트 간 직접 통신 (향후 Claude Code 기능 확장 시) |

---

## References

- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) - 구조화된 문서 기반 에이전트 통신 패턴
- [ChatDev](https://www.ibm.com/think/topics/chatdev) - 가상 소프트웨어 회사 컨셉
- [SaaS Org Chart Guide](https://theorgchart.com/saas-company-org-charts/) - 스타트업 조직 구조 참고
- [AI One-Person Company](https://orbilontech.com/ai-automation-1b-one-person-company/) - 1인 AI 기업 트렌드
- [SaaS Company Structure](https://userguiding.com/blog/saas-roles) - SaaS 회사 역할/부서 참고

---

*Generated by Planning Interview v2.0 | 2026-02-21*
*Interviewer: Claude Code (Opus 4.6)*
*Interviewee: Jay Kim (CEO)*
