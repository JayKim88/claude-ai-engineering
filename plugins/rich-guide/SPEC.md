# Rich Guide - Technical Specification

> **Generated**: 2026-02-15
> **Status**: Draft v1.0
> **Based on**: PLANNING.md (Lean Canvas)

---

## 1. Overview

### Purpose
**Rich Guide**는 재테크/투자/부업 정보가 파편화되어 초보자가 어디서부터 시작해야 할지 모르는 문제를 해결하는 다중 에이전트 파이프라인 시스템입니다. 사용자의 재무 상태를 진단하고, 흩어진 정보를 큐레이션하여, 개인화된 부자 전략을 단계별로 제시합니다.

### Scope

**In Scope (v1.0 MVP):**
- 사용자 재무 인터뷰 & 프로필 생성
- 6개 전문 에이전트 파이프라인 (진단 → 전략 생성 → 실행 계획)
- SQLite 로컬 DB를 통한 데이터 저장 & 버전 관리
- 기존 플러그인(market-pulse, portfolio-copilot) 데이터 연동
- 도메인 화이트리스트 기반 정보 큐레이션
- 주간 단위 실행 체크리스트 생성
- 다층 검증 (면책 조항 + 출처 명시 + 전문가 상담 권유)

**Out of Scope (v2.0 이후):**
- 실시간 대시보드 UI
- 진행률 트래킹 시스템
- 커뮤니티 성공 사례 벤치마킹
- 자동 리밸런싱 알림

---

## 2. Requirements

### Functional Requirements

#### FR-1: 사용자 재무 인터뷰
- **Description**: AskUserQuestion을 사용해 사용자의 재무 상태를 상세히 파악
- **Priority**: High
- **Rationale**: 개인화된 전략의 핵심 기반 데이터
- **Acceptance Criteria**:
  - [ ] 월수입, 월지출, 예금, 투자자산, 대출, 리스크성향 7가지 필수 정보 수집
  - [ ] 사용자가 "모르겠음" 답변 시 기본값 제시 (나이/직업 기반 추정치)
  - [ ] 모호한 답변 감지 시 구체적 후속 질문 제공

#### FR-2: 재무 데이터 저장 & 버전 관리
- **Description**: SQLite DB에 사용자 재무 프로필을 버전별로 저장
- **Priority**: High
- **Rationale**: 시간 경과에 따른 재무 상태 변화 추적 & 히스토리 관리
- **Acceptance Criteria**:
  - [ ] `~/.claude/skills/rich-guide/data/profiles.db` 경로에 SQLite DB 생성
  - [ ] 각 프로필에 `version`, `created_at`, `updated_at` 타임스탬프 포함
  - [ ] 기존 데이터가 30일 이상 지났을 때 자동 갱신 제안

#### FR-3: 6개 에이전트 파이프라인 실행
- **Description**: 전문 분야별 에이전트가 협력하여 진단 → 전략 생성 → 실행 계획 제공
- **Priority**: High
- **Rationale**: 단일 AI보다 전문화된 다중 에이전트가 더 정확한 분석 제공
- **Acceptance Criteria**:
  - [ ] Phase 1: 병렬 3개 Task (financial-diagnostician, info-curator, market-context-analyzer)
  - [ ] Phase 2: 병렬 2개 Task (wealth-strategist, risk-reward-evaluator)
  - [ ] Phase 3: 순차 1개 Task (action-plan-generator)
  - [ ] 각 에이전트 결과를 파일로 저장 (`/tmp/rich-guide-{agent}-{timestamp}.json`)

#### FR-4: 전략 다양성 보장 (복합 기준)
- **Description**: wealth-strategist가 리스크/시간/분야를 모두 고려해 3-5개 다양한 전략 생성
- **Priority**: High
- **Rationale**: 사용자에게 선택권 제공, 획일적인 답변 방지
- **Acceptance Criteria**:
  - [ ] 리스크 범위: 저위험(예금) / 중위험(인덱스) / 고위험(개별주식) 포함
  - [ ] 시간 범위: 단기(1년) / 중기(3년) / 장기(10년) 포함
  - [ ] 분야 범위: 투자 / 부업 / 커리어 성장 / 비용 절감 중 최소 2개 이상

#### FR-5: 정보 큐레이션 & 신뢰도 평가
- **Description**: 웹에서 재테크 정보 수집 시 도메인 화이트리스트 기반 필터링
- **Priority**: Medium
- **Rationale**: 광고성/저품질 콘텐츠 차단, 신뢰도 높은 정보만 제공
- **Acceptance Criteria**:
  - [ ] 화이트리스트 도메인: 한국경제, 서울경제, 네이버 증권, 투자 포럼(38커뮤니케이션즈 등)
  - [ ] 모든 추천 정보에 출처 URL 명시
  - [ ] 화이트리스트 외 도메인은 수집하되 "미검증" 라벨 표시

#### FR-6: 주간 실행 체크리스트 생성
- **Description**: 선택된 전략에 대한 구체적인 주간 단위 실행 계획 제공
- **Priority**: Medium
- **Rationale**: 추상적 목표가 아닌 실행 가능한 액션 제시
- **Acceptance Criteria**:
  - [ ] 월별 목표 → 주간 체크리스트로 분해
  - [ ] 각 체크리스트 항목에 예상 소요 시간 표시
  - [ ] 1주차: ISA 계좌 개설, 2주차: 자동이체 설정 등 구체적 액션

#### FR-7: 기존 플러그인 데이터 연동
- **Description**: market-pulse, portfolio-copilot DB/파일을 직접 읽어 최신 시장/포트폴리오 정보 활용
- **Priority**: Medium
- **Rationale**: 기존 생태계 활용, 중복 데이터 수집 방지
- **Acceptance Criteria**:
  - [ ] `plugins/portfolio-copilot/data/portfolio.db` 읽기
  - [ ] `plugins/market-pulse/analysis/*.json` 파일 읽기
  - [ ] 플러그인 미설치 시 "자동 설치 안내" 메시지 + 기본 전략 제공

#### FR-8: 다층 검증 (리스크 관리)
- **Description**: 잘못된 재무 조언 방지를 위한 3단계 검증
- **Priority**: High
- **Rationale**: AI 환각으로 인한 부적절한 재무 조언 최소화
- **Acceptance Criteria**:
  - [ ] Layer 1: 모든 출력 시작 시 "이 조언은 참고용이며, 투자 책임은 본인에게 있습니다" 면책 조항
  - [ ] Layer 2: 모든 추천에 출처 URL/논문 링크 포함
  - [ ] Layer 3: 최종 출력에 "재무설계사 상담 권장" 문구 + 관련 링크

### Non-Functional Requirements

#### NFR-1: Performance
- **전체 파이프라인 실행 시간**: 목표 3분 이내 (6개 에이전트, 병렬 실행)
- **에이전트별 타임아웃**: 각 에이전트 최대 60초
- **DB 쿼리 응답 시간**: SQLite 읽기 < 100ms

#### NFR-2: Security & Privacy
- **로컬 저장만**: 모든 재무 데이터는 로컬 DB에만 저장, 외부 전송 없음
- **DB 파일 권한**: `chmod 600` (소유자만 읽기/쓰기)
- **민감 정보 로깅 금지**: 수입/자산 금액을 로그에 기록하지 않음

#### NFR-3: Usability
- **진행 상태 피드백**: 에이전트별 상태 표시 (✓ 완료, ⏳ 실행 중, ⏸ 대기 중)
- **인터뷰 중단 복구**: Ctrl+C 중단 시 지금까지의 답변을 DB에 부분 저장
- **반복 호출 최적화**: 24시간 이내 재실행 시 "기존 데이터를 사용할까요?" 자동 제안

#### NFR-4: Maintainability
- **에이전트 독립성**: 각 에이전트는 `.md` 파일로 독립 정의, 도구 제약 명시
- **파일 기반 통신**: 에이전트 간 데이터 전달은 JSON 파일로 (디버깅 용이)
- **버전 관리**: 프로필 스키마 변경 시 마이그레이션 스크립트 제공

---

## 3. Technical Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      SKILL.md (Orchestrator)                 │
│                  - AskUserQuestion으로 인터뷰                │
│                  - Task() 호출로 에이전트 조율               │
│                  - 에러 핸들링 & 폴백 로직                   │
└───────┬─────────────────────────────────────────────────────┘
        │
        ├─ Step 1: 재무 인터뷰 (AskUserQuestion)
        │   → profiles.db에 저장
        │
        ├─ Step 2: Phase 1 - 진단 (병렬 3개)
        │   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
        │   │ financial-         │  │ info-curator       │  │ market-context-    │
        │   │ diagnostician      │  │ (Haiku)            │  │ analyzer (Sonnet)  │
        │   │ (Sonnet)           │  │ WebSearch/WebFetch │  │ MCP (UsStockInfo)  │
        │   └────────┬───────────┘  └────────┬───────────┘  └────────┬───────────┘
        │            └──────────────────┬────────────────────────────┘
        │                               ▼
        │                   [/tmp/phase1-results.json]
        │
        ├─ Step 3: Phase 2 - 전략 생성 (병렬 2개)
        │   ┌────────────────────┐  ┌────────────────────┐
        │   │ wealth-strategist  │  │ risk-reward-       │
        │   │ (Opus)             │  │ evaluator (Sonnet) │
        │   │ 3-5개 전략 생성    │  │ 리스크 평가        │
        │   └────────┬───────────┘  └────────┬───────────┘
        │            └──────────────────┬────────────────┘
        │                               ▼
        │                   [/tmp/phase2-strategies.json]
        │
        ├─ Step 4: AskUserQuestion (전략 선택)
        │   → 사용자가 1개 전략 선택
        │
        └─ Step 5: Phase 3 - 실행 계획 (순차)
            ┌────────────────────────────────────┐
            │ action-plan-generator (Opus)       │
            │ 주간 체크리스트 생성               │
            └────────┬───────────────────────────┘
                     ▼
         [plugins/rich-guide/roadmaps/{timestamp}.md]
```

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Orchestration** | SKILL.md (Claude Code) | 기존 플러그인 패턴 재사용 |
| **Database** | SQLite 3 | 로컬 저장, 가벼움, 버전 관리 용이 |
| **Agent Communication** | JSON 파일 (`/tmp/`) | 디버깅 용이, 에이전트 독립성 |
| **Web Search** | WebSearch/WebFetch 도구 | 실시간 재테크 정보 수집 |
| **Market Data** | MCP (UsStockInfo) | 기존 MCP 서버 활용 |
| **Model Selection** | Opus (전략 생성), Sonnet (분석), Haiku (정보 수집) | 토큰 비용 최적화 |

### Key Components

#### Component 1: SKILL.md (Orchestrator)
- **Responsibility**: 전체 파이프라인 조율, 사용자 인터뷰, 에러 핸들링
- **Interfaces**:
  - Input: 사용자 트리거 ("부자 되는 법", "재테크 가이드", "rich guide")
  - Output: 최종 로드맵 마크다운 파일
- **Dependencies**: profiles.db, 6개 에이전트

#### Component 2: profiles.db (SQLite Database)
- **Responsibility**: 사용자 재무 프로필 저장 & 버전 관리
- **Schema**:
```sql
CREATE TABLE profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  monthly_income INTEGER,
  monthly_expense INTEGER,
  savings INTEGER,
  investment_assets INTEGER,
  debt INTEGER,
  risk_tolerance TEXT CHECK(risk_tolerance IN ('low', 'medium', 'high')),
  short_term_goal TEXT,
  mid_term_goal TEXT,
  long_term_goal TEXT
);

CREATE TABLE agent_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_id INTEGER REFERENCES profiles(id),
  agent_name TEXT NOT NULL,
  execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  result_json TEXT,  -- JSON blob
  status TEXT CHECK(status IN ('success', 'failed', 'partial'))
);
```

#### Component 3: Agent Pool (agents/*.md)
6개 독립 에이전트 정의:

| Agent File | Model | Tools | Timeout |
|------------|-------|-------|---------|
| `financial-diagnostician.md` | Sonnet | Read, Bash | 60s |
| `info-curator.md` | Haiku | WebSearch, WebFetch, Grep | 90s |
| `market-context-analyzer.md` | Sonnet | MCP (UsStockInfo), WebSearch | 60s |
| `wealth-strategist.md` | Opus | Read | 120s |
| `risk-reward-evaluator.md` | Sonnet | Read | 60s |
| `action-plan-generator.md` | Opus | Read, Write | 120s |

### Data Models

#### Model 1: FinancialProfile
```typescript
interface FinancialProfile {
  id: number
  version: number
  created_at: Date
  updated_at: Date
  monthly_income: number  // 만원 단위
  monthly_expense: number
  savings: number
  investment_assets: number
  debt: number
  risk_tolerance: 'low' | 'medium' | 'high'
  short_term_goal: string  // 1년 이내
  mid_term_goal: string    // 3년 이내
  long_term_goal: string   // 10년 이내
}
```

#### Model 2: WealthStrategy
```typescript
interface WealthStrategy {
  id: string
  title: string
  category: 'investment' | 'side-hustle' | 'career' | 'cost-saving'
  risk_level: 'low' | 'medium' | 'high'
  time_horizon: 'short' | 'mid' | 'long'  // 1년 / 3년 / 10년
  expected_return: string  // 예: "연 5-7%"
  initial_capital_required: number
  monthly_commitment: string  // 예: "주 3시간"
  description: string
  pros: string[]
  cons: string[]
  sources: string[]  // URL 배열
}
```

#### Model 3: ActionPlan
```typescript
interface ActionPlan {
  strategy_id: string
  weekly_checklists: WeeklyChecklist[]
}

interface WeeklyChecklist {
  week: number
  month: number
  tasks: Task[]
}

interface Task {
  description: string
  estimated_time: string  // 예: "30분"
  category: 'research' | 'setup' | 'execution' | 'review'
  completed: boolean
}
```

---

## 4. User Experience

### User Flows

#### Flow 1: 첫 실행 (신규 사용자)
1. 사용자: `"부자 되는 법"`
2. 시스템: "재무 상태 분석을 시작합니다. 몇 가지 질문드리겠습니다."
3. 시스템: AskUserQuestion (월수입, 월지출, 자산, 부채, 목표, 리스크 성향)
4. 사용자: 각 질문에 답변 (또는 "모르겠어요" → 기본값 제시)
5. 시스템: "분석 중입니다..." + 에이전트별 상태 표시
   ```
   ✓ 재무 진단 완료
   ⏳ 정보 수집 중...
   ⏸ 시장 분석 대기 중
   ```
6. 시스템: 3-5개 전략 제시 (각각 리스크/시간/분야 다름)
7. 사용자: AskUserQuestion에서 1개 전략 선택
8. 시스템: 선택된 전략의 주간 체크리스트 생성 + 마크다운 파일 저장

#### Flow 2: 재실행 (기존 데이터 있음)
1. 사용자: `"재테크 가이드"`
2. 시스템: DB에서 마지막 프로필 조회 (updated_at < 24시간 전)
3. 시스템: "기존 재무 데이터(2026-02-14 작성)를 사용할까요?"
   - 옵션 A: 기존 데이터 사용 (바로 Phase 2로)
   - 옵션 B: 새로 인터뷰 시작
4. 사용자: 옵션 A 선택 → Phase 2부터 시작

#### Flow 3: 인터뷰 중단 복구
1. 사용자: 인터뷰 중 Ctrl+C
2. 시스템: 지금까지의 답변을 `profiles` 테이블에 `status='partial'`로 저장
3. 다음 실행 시: "중단된 인터뷰가 있습니다. 이어서 진행할까요?"

### UI/UX Considerations

**진행 상태 표시**:
```
부자 전략 분석 중...

Phase 1: 진단 (3/3 완료)
  ✓ 재무 진단 완료
  ✓ 정보 수집 완료
  ✓ 시장 분석 완료

Phase 2: 전략 생성 (1/2 진행 중)
  ✓ 전략 생성 완료
  ⏳ 리스크 평가 중...

Phase 3: 실행 계획 (대기 중)
  ⏸ 로드맵 생성 대기 중
```

**에러 상태 처리**:
```
⚠️ 일부 에이전트 실패

✓ 재무 진단 완료
✗ 정보 수집 실패 (네트워크 오류) → 재시도 중... (1/1)
✓ 시장 분석 완료

기본 데이터로 진행합니다. 정보 큐레이션은 제한적일 수 있습니다.
```

---

## 5. Implementation Details

### Phase 1: MVP Core Features
- [ ] SQLite DB 스키마 생성 (`config/init_db.py`)
- [ ] SKILL.md Orchestrator 작성
- [ ] 6개 에이전트 `.md` 파일 작성
- [ ] 재무 인터뷰 AskUserQuestion 로직
- [ ] 파일 기반 에이전트 통신 (JSON)
- [ ] 도메인 화이트리스트 설정 (`config/whitelist.yaml`)
- [ ] 면책 조항 + 출처 명시 템플릿
- [ ] 에러 핸들링 (재시도 + 폴백)

### Phase 2: 기존 플러그인 연동
- [ ] `portfolio-copilot/data/portfolio.db` 읽기 로직
- [ ] `market-pulse/analysis/*.json` 파일 파싱
- [ ] 플러그인 미설치 감지 + 설치 안내 메시지
- [ ] 연동 데이터 검증 (오래된 데이터 감지)

### Phase 3: UX 개선
- [ ] 에이전트별 상태 표시 (진행 중/완료/실패)
- [ ] 인터뷰 중단 시 부분 저장
- [ ] 반복 호출 시 기존 데이터 활용 제안
- [ ] 버전 관리 (30일 이상 지난 데이터 갱신 제안)

### Technical Decisions

#### Decision 1: SQLite vs YAML
- **Options Considered**:
  - A) YAML 파일 (portfolio-analyzer 패턴)
  - B) SQLite DB
  - C) 메모리만 사용
- **Chosen**: B (SQLite DB)
- **Rationale**:
  - 버전 관리 용이 (타임스탬프, 히스토리)
  - 쿼리 성능 (최신 프로필 조회, 에이전트 결과 조인)
  - 확장성 (추후 대시보드 추가 시 유리)
- **Trade-offs**:
  - 파일보다 복잡도 증가
  - 하지만 portfolio-copilot에서 이미 검증됨

#### Decision 2: 에이전트 통신 방식
- **Options Considered**:
  - A) 메모리 JSON 반환값
  - B) 파일 기반 JSON
  - C) 하이브리드
- **Chosen**: B (파일 기반)
- **Rationale**:
  - 디버깅 용이 (각 에이전트 출력 확인 가능)
  - 에이전트 재실행 시 캐싱 가능
  - 대용량 데이터 처리 (info-curator가 많은 URL 수집)
- **Trade-offs**:
  - 파일 I/O 오버헤드 (하지만 /tmp 사용으로 최소화)

#### Decision 3: 모델 배분
- **Options Considered**:
  - A) 전부 Opus (최고 품질, 비용 높음)
  - B) 전부 Sonnet (균형)
  - C) 혼합 (Opus 전략 생성, Sonnet 분석, Haiku 정보 수집)
- **Chosen**: C (혼합)
- **Rationale**:
  - 전략 생성은 창의성 필요 → Opus
  - 재무 진단/리스크 평가는 분석력 필요 → Sonnet
  - 정보 수집은 속도 중요 → Haiku
- **Trade-offs**:
  - 복잡도 증가, 하지만 토큰 비용 60% 절감 예상

---

## 6. Edge Cases & Error Handling

### Edge Case 1: 사용자가 모든 질문에 "모르겠어요"
- **Situation**: 재무 인터뷰에서 수입/지출/자산 모두 모호한 답변
- **Expected Behavior**:
  1. "평균 데이터를 기반으로 추정치를 제시해드릴까요?" 제안
  2. 나이/직업 기반 평균값 제시 (예: 30대 직장인 → 연봉 4000만원 추정)
  3. "추정치로 진행하되, 정확도가 낮을 수 있습니다" 경고
- **Fallback**: 기본 보수적 전략만 제공 (저위험 예금 위주)

### Edge Case 2: info-curator가 화이트리스트 도메인에서 정보를 못 찾음
- **Situation**: 특정 키워드("블록체인 투자")에 대한 화이트리스트 기사 없음
- **Expected Behavior**:
  1. 화이트리스트 외 도메인에서 수집
  2. "미검증 출처" 라벨 표시
  3. "더 신뢰할 만한 정보는 금융감독원 등을 참고하세요" 안내
- **Fallback**: 관련 정보 없이도 재무 진단 기반 기본 전략 제공

### Edge Case 3: 기존 플러그인(market-pulse) 데이터가 오래됨
- **Situation**: `market-pulse` 마지막 실행이 7일 전
- **Expected Behavior**:
  1. "시장 데이터가 7일 전 것입니다. 최신 데이터를 가져올까요?" 제안
  2. 옵션 A: market-pulse 스킬 재실행 (느림, 최신 보장)
  3. 옵션 B: 기존 데이터 사용 (빠름, 시의성 낮음)
- **Fallback**: 기존 데이터로 진행 + "시장 상황이 변했을 수 있습니다" 경고

### Edge Case 4: 에이전트 타임아웃
- **Situation**: wealth-strategist가 120초 안에 완료 못함
- **Expected Behavior**:
  1. 1회 재시도 (동일 입력)
  2. 재시도 실패 시: "전략 생성이 지연되고 있습니다. 기본 전략을 제공합니다"
  3. 폴백: 리스크 성향 기반 템플릿 전략 사용
- **Fallback**:
  - 저위험 → 예금/채권 위주
  - 중위험 → 인덱스 펀드
  - 고위험 → 개별 주식 + 부업

### Error Scenarios

| Error Type | User Action | System Response |
|------------|-------------|-----------------|
| 네트워크 실패 | WebSearch 실패 | 재시도 1회 → 실패 시 "오프라인 기본 전략 제공" |
| DB 파일 없음 | 첫 실행 | 자동으로 `init_db.py` 실행 + 스키마 생성 |
| DB 마이그레이션 필요 | 스키마 버전 불일치 | "데이터베이스 업데이트가 필요합니다" + 마이그레이션 스크립트 실행 |
| 에이전트 파일 누락 | `.md` 파일 없음 | "필수 파일이 없습니다. 플러그인을 재설치하세요" |
| 디스크 용량 부족 | 파일 쓰기 실패 | "저장 공간이 부족합니다. /tmp를 정리하세요" |

---

## 7. Security & Privacy

### Security Considerations

**1. 로컬 저장만**
- 모든 재무 데이터는 `~/.claude/skills/rich-guide/data/profiles.db`에만 저장
- 외부 API로 재무 데이터 전송 금지 (WebSearch는 키워드만 전송)

**2. 파일 권한**
```bash
# 플러그인 설치 시 자동 실행
chmod 600 ~/.claude/skills/rich-guide/data/profiles.db
chmod 700 ~/.claude/skills/rich-guide/data/
```

**3. 민감 정보 로깅 금지**
- 금액 정보는 로그에 기록하지 않음
- 에러 로그에는 "금액 정보 포함됨 (로그에서 제외)" 플레이스홀더 사용

**4. SQL Injection 방지**
- SQLite 쿼리는 모두 parameterized query 사용
```python
# ❌ 취약한 방식
cursor.execute(f"SELECT * FROM profiles WHERE id = {user_id}")

# ✅ 안전한 방식
cursor.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
```

### Privacy & Compliance

**1. 면책 조항 (모든 출력 시작 시)**
```
⚠️ 면책 조항
이 분석은 AI가 생성한 참고용 정보입니다.
투자 결정은 본인의 판단과 책임 하에 이루어져야 하며,
중요한 재무 결정 전에는 전문 재무설계사와 상담하시기 바랍니다.
```

**2. 출처 명시 (모든 추천에)**
```
📚 출처:
- 한국경제: "2026년 ISA 세제 혜택" (https://...)
- 서울경제: "인덱스 펀드 수익률 비교" (https://...)
```

**3. 전문가 상담 권유 (최종 출력에)**
```
💡 다음 단계
1. 생성된 로드맵 검토
2. 재무설계사 상담 예약 (추천: https://www.fpsb.or.kr/)
3. 소액으로 테스트 시작
```

**4. 데이터 보존 기간**
- 사용자가 명시적으로 삭제 요청 전까지 보존
- 플러그인 삭제 시 DB 파일도 함께 삭제 안내

---

## 8. Testing Strategy

### Test Coverage

#### Unit Tests
- [ ] `init_db.py`: 스키마 생성, 마이그레이션
- [ ] `utils/profile_manager.py`: CRUD 연산
- [ ] `utils/whitelist.py`: 도메인 필터링 로직
- [ ] `utils/fallback.py`: 에러 핸들링, 기본값 생성

#### Integration Tests
- [ ] SKILL.md → 6개 에이전트 호출 → 파일 생성 확인
- [ ] profiles.db 읽기/쓰기 → 버전 관리 동작
- [ ] market-pulse, portfolio-copilot 연동 (mock 데이터)

#### E2E Tests
1. **신규 사용자 플로우**:
   - 입력: "부자 되는 법"
   - 인터뷰 완료 → 전략 3개 생성 → 로드맵 파일 저장
   - 검증: `roadmaps/*.md` 파일 존재, 주간 체크리스트 포함

2. **기존 사용자 재실행**:
   - 입력: "재테크 가이드" (24시간 이내)
   - "기존 데이터 사용" 선택 → Phase 2부터 시작
   - 검증: 인터뷰 스킵, 전략 생성 시간 < 2분

3. **에이전트 실패 시나리오**:
   - Mock: info-curator 타임아웃
   - 결과: 재시도 → 폴백 전략 사용 → 경고 메시지 표시
   - 검증: 에러 발생해도 최종 로드맵 생성됨

### Test Scenarios

| Scenario | Input | Expected Output |
|----------|-------|----------------|
| 완전한 재무 정보 | 수입 500만원, 자산 5000만원, 리스크 중 | 5개 전략 (투자 2개, 부업 1개, 커리어 1개, 절약 1개) |
| 모호한 답변 | "대충 300만원 정도?" | 기본값 제시 → 확인 → 진행 |
| 인터뷰 중단 | Ctrl+C at 질문 3/7 | 부분 저장 → 다음 실행 시 "이어서 진행할까요?" |
| 플러그인 미설치 | market-pulse 없음 | "설치 안내" + 기본 시장 가정으로 진행 |

---

## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| AI 환각 (잘못된 재무 조언) | Medium | High | 3단계 검증 (면책 + 출처 + 전문가 권유) |
| 토큰 소모 과다 (6개 에이전트) | High | Medium | Haiku(수집) / Sonnet(분석) / Opus(전략) 분배 |
| 개인정보 유출 (재무 데이터) | Low | High | 로컬 저장만, 파일 권한 600, 로깅 금지 |
| 정보 시의성 (오래된 데이터) | Medium | Medium | 30일 이상 데이터 자동 갱신 제안 |
| 에이전트 실패 (네트워크/타임아웃) | Medium | Medium | 재시도 1회 + 폴백 전략 제공 |
| 화이트리스트 한계 (새 도메인) | High | Low | 미검증 라벨로 수집 + 출처 표시 |
| 기존 플러그인 의존성 | Medium | Medium | 미설치 시 기본 전략 제공 + 설치 안내 |

---

## 10. Open Questions

- [ ] **도메인 화이트리스트 업데이트 주기**: 수동 vs 자동? 새 신뢰 도메인 발견 시 어떻게 추가?
- [ ] **다국어 지원**: 영어권 재테크 정보도 포함할지? (현재는 한국어만)
- [ ] **전략 추천 개수**: 3-5개가 적절한지? 사용자 피드백 필요
- [ ] **로드맵 갱신 알림**: 월별로 "이번 달 목표 확인하세요" 알림을 줄지?
- [ ] **포트폴리오 시뮬레이션**: 전략 실행 시 예상 자산 증가를 시뮬레이션할지?

---

## 11. Success Metrics

### Key Metrics
- **전략 완성도**: 세션당 생성된 구체적 액션 수 ≥ 5개
- **정보 신뢰도**: 출처 명시율 ≥ 80% (화이트리스트 도메인)
- **실행 시간**: 전체 파이프라인 < 3분
- **에러율**: 에이전트 실패율 < 10%

### Monitoring
```bash
# 로그 파일: ~/.claude/skills/rich-guide/logs/metrics.log
{
  "session_id": "abc123",
  "timestamp": "2026-02-15T10:30:00Z",
  "duration_seconds": 142,
  "strategies_generated": 5,
  "sources_cited": 12,
  "agent_failures": 0,
  "user_satisfaction": null  // 추후 피드백 수집
}
```

**Alert Thresholds**:
- 에이전트 실패율 > 20%: 네트워크 문제 또는 타임아웃 설정 재검토
- 평균 실행 시간 > 5분: 모델 최적화 또는 병렬화 개선 필요

---

## 12. References

### Related Documents
- [PLANNING.md](./PLANNING.md) - Lean Canvas (기획안)
- [plugins/career-compass/PLANNING.md](../career-compass/PLANNING.md) - 다중 에이전트 참고 아키텍처
- [plugins/market-pulse/docs/ARCHITECTURE.md](../market-pulse/docs/ARCHITECTURE.md) - 시장 데이터 연동
- [plugins/portfolio-copilot/](../portfolio-copilot/) - SQLite DB 패턴 참고

### Interview Notes

**핵심 설계 결정 (4라운드 인터뷰 기반)**:

1. **데이터 저장**: SQLite DB (버전 관리, 히스토리 추적)
2. **에이전트 통신**: 파일 기반 JSON (디버깅 용이)
3. **플러그인 연동**: 직접 DB/파일 읽기 (속도 우선)
4. **리스크 관리**: 다층 검증 (면책 + 출처 + 전문가 권유)
5. **재무 인터뷰**: 상세 정보 수집 + 기본값 제시
6. **데이터 갱신**: 버전 관리 (30일 자동 제안)
7. **전략 다양성**: 복합 기준 (리스크/시간/분야)
8. **정보 신뢰도**: 도메인 화이트리스트
9. **실행 계획**: 주간 체크리스트
10. **에러 처리**: 재시도 + 폴백
11. **UX**: 에이전트별 상태 표시
12. **중단 복구**: 부분 저장
13. **반복 호출**: 기존 데이터 활용 제안
14. **의존성 관리**: 자동 설치 안내

---

**Next Steps:**
1. [ ] SKILL.md 작성 (Orchestrator 로직)
2. [ ] 6개 에이전트 `.md` 파일 작성
3. [ ] SQLite 스키마 & 초기화 스크립트 작성
4. [ ] 도메인 화이트리스트 YAML 작성
5. [ ] Unit 테스트 작성
6. [ ] E2E 테스트로 전체 플로우 검증
7. [ ] README.md 작성 (사용자 가이드)
