# Rich Guide - Developer Guide

Rich Guide v3.0 플러그인 개발 및 유지보수 가이드.

## 디렉토리 구조

```
plugins/rich-guide/
├── .claude-plugin/
│   └── plugin.json              # 플러그인 메타데이터
├── skills/
│   ├── rich-guide/
│   │   └── SKILL.md             # Orchestrator v3.0 (파이프라인 모드)
│   └── rich-chat/
│       └── SKILL.md             # 대화형 모드 v1.0 (컨텍스트 프라이밍)
├── agents/                      # 6개 전문 에이전트 (.md 정의)
│   ├── financial-diagnostician.md   # 재무 건강도 진단 (Sonnet)
│   ├── knowledge-advisor.md         # 지식베이스 매칭 + 레벨 판정 (Sonnet) [v3.0 NEW]
│   ├── market-context-analyzer.md   # 시장 맥락 분석 (Sonnet)
│   ├── wealth-strategist.md         # 전문가 기반 전략 생성 (Opus)
│   ├── risk-reward-evaluator.md     # 리스크 평가 (Sonnet)
│   └── action-plan-generator.md     # 3-section 통합 로드맵 생성 (Opus)
├── knowledge/                   # 전문가 방법론 지식 베이스 [v3.0 NEW]
│   ├── investment-masters.md        # 투자 대가 8명 방법론
│   ├── entrepreneurs.md             # 자수성가 인물 8명 방법론
│   ├── side-hustles.md              # 부업 10카테고리 가이드
│   └── money-fundamentals.md        # 돈의 핵심 원리 5개
├── workflows/                   # 상황별 워크플로우 템플릿 [v3.0 NEW]
│   ├── first-investment.md          # 첫 투자 시작
│   ├── debt-freedom.md              # 빚 탈출
│   ├── side-hustle-launch.md        # 부업 시작
│   └── wealth-building.md           # 장기 자산 증식
├── commands/
│   └── rich-guide/
│       └── rich-guide.md        # /rich-guide 커맨드 정의
├── config/
│   ├── init_db.py               # SQLite 초기화 스크립트 (4테이블)
│   ├── agent-config.yaml        # 에이전트 동작 파라미터 (orchestrator가 로드)
│   └── whitelist.yaml           # 신뢰 도메인 화이트리스트
├── templates/
│   └── roadmap-template.md      # 3-section 로드맵 출력 템플릿
├── CLAUDE.md                    # 개발자 가이드 (이 파일)
└── README.md                    # 사용자 가이드
```

## 듀얼 모드 아키텍처

Rich Guide는 두 가지 모드로 실행 가능합니다:

| 모드 | 스킬 | 트리거 | 방식 | 출력 |
|------|------|--------|------|------|
| **파이프라인** | `/rich-guide` | "부자 되는 법", "재테크 가이드" | 7-agent pipeline | 로드맵 .md 파일 |
| **대화형** | `/rich-chat` | "재테크 상담", "투자 상담" | 지식 프라이밍 + 자유 대화 | 실시간 Q&A |

- **파이프라인 모드**: 종합 재무 진단 → 전문가 매칭 → 전략 생성 → 12주 로드맵 파일 출력
- **대화형 모드**: 지식 베이스 8파일 로딩 → "부자 멘토" 페르소나 → 무제한 Q&A
- 두 모드는 **독립 실행** 가능하며, **프로필 DB를 공유**합니다

### 대화형 모드 실행 흐름

```
rich-chat SKILL.md:
  Step 1: 지식 베이스 8파일 병렬 Read (knowledge 4 + workflows 4)
  Step 2: DB에서 기존 프로필 + 최근 세션 3건 조회
  Step 3: "부자 멘토" 페르소나 채택 + 레벨 맞춤 인사
  Step 4: 무한 대화 (Claude Code 컨텍스트 압축으로 사실상 무제한)
```

## 에이전트 역할 및 실행 순서

| 에이전트 | 모델 | Phase | 입력 | 출력 파일 |
|---------|------|-------|------|----------|
| financial-diagnostician | Sonnet | 1 (병렬) | 재무 프로필 JSON | `/tmp/rich-guide-diagnostician-{ts}.json` |
| knowledge-advisor | Sonnet | 1 (병렬) | 프로필 + 지식베이스 4파일 Read | `/tmp/rich-guide-knowledge-{ts}.json` |
| market-context-analyzer | Sonnet | 1 (병렬) | WebSearch + portfolio-copilot DB | `/tmp/rich-guide-market-{ts}.json` |
| wealth-strategist | Opus | 2A (순차) | Phase 1 통합 + 매칭된 전문가 목록 | `/tmp/rich-guide-strategist-{ts}.json` |
| risk-reward-evaluator | Sonnet | 2B (순차) | Phase 1 결과 + 실제 전략 목록 | `/tmp/rich-guide-evaluator-{ts}.json` |
| action-plan-generator | Opus | 3 (순차) | 선택 전략 + 커리큘럼 + 워크플로우 Read + 템플릿 | `~/.claude/skills/rich-guide/roadmaps/roadmap-{ts}.md` |

## 전체 실행 흐름

```
SKILL.md Step 1: Environment Setup & Config Load
  ├── agent-config.yaml 로드 (타임아웃, 캐시 임계값, 레벨 기준 등)
  ├── DB 존재 확인 → 없으면 init_db.py 자동 실행 (절대 경로 사용)
  └── 기존 프로필 조회 (24h 캐시 / 1-30d 갱신 / 신규)

SKILL.md Step 2: Financial Interview (8필드)
  ├── 24h 이내: "기존 데이터 사용" 옵션
  ├── 1-30일: "일부 업데이트 / 전체 재입력" 옵션 (AskUserQuestion)
  ├── AskUserQuestion 2회 (8필드: 월수입/월지출/예금/투자자산 + 부채/리스크/경험/목표)
  ├── "잘 모르겠어요" 기본값 폴백 처리
  └── profiles 테이블에 저장 (temp JSON 파일 경유, parameterized query)

SKILL.md Step 3: Phase 1 Parallel (진단 + 지식 매칭 + 시장)
  ├── 단일 응답 블록에서 3개 Task() 동시 호출 [CRITICAL]
  │   ├── financial-diagnostician: 재무건강도 0-100점
  │   ├── knowledge-advisor: 지식베이스 4파일 Read → 레벨 판정 → 전문가 매칭 → 학습 커리큘럼
  │   └── market-context-analyzer: 금리/시장 분석
  ├── 각 결과를 /tmp/rich-guide-{agent}-{ts}.json에 저장
  └── phase1 통합: /tmp/rich-guide-phase1-{ts}.json

SKILL.md Step 4: Phase 2 Sequential (전문가 기반 전략 → 리스크 평가)
  ├── Phase 2A: wealth-strategist Task()
  │   └── 매칭된 전문가 방법론 기반 3-5개 전략 생성 (expert_source 필수)
  ├── 실제 strategy IDs + titles 확보
  ├── Phase 2B: risk-reward-evaluator Task()
  │   └── 실제 전략 목록을 프롬프트에 포함하여 정량 평가
  └── phase2 통합: /tmp/rich-guide-phase2-{ts}.json

SKILL.md Step 5: Strategy Selection
  └── AskUserQuestion으로 사용자가 전략 선택 (전문가명 태그 포함)

SKILL.md Step 6: Phase 3 Sequential (3-section 통합 로드맵)
  ├── roadmap-template.md 읽기
  ├── 워크플로우 파일(1-2개) Read
  └── action-plan-generator Task() → 학습+실행+워크플로우 3-section 로드맵 생성

SKILL.md Step 7: Final Report, Session Record & Cleanup
  ├── 3-Layer 검증 (면책 조항 + 출처 + 전문가 링크)
  ├── 학습 계획 요약 출력
  ├── 콘솔 요약 출력
  ├── session_history 테이블에 기록
  └── /tmp/rich-guide-*-{ts}.json 임시 파일 정리
```

## 병렬 실행 패턴 (CRITICAL)

Claude Code에서 병렬 에이전트 실행은 **반드시 단일 응답에서** 모든 Task() 호출이 이루어져야 합니다.

```python
# 올바른 방법 - 단일 응답 블록에서 동시 호출
Task(subagent_type="financial-diagnostician", ...)
Task(subagent_type="knowledge-advisor", ...)
Task(subagent_type="market-context-analyzer", ...)

# 잘못된 방법 - 각각 다른 응답에서 호출하면 순차 실행됨
result1 = Task(...)  # 응답 1
result2 = Task(...)  # 응답 2 (순차 실행)
```

Phase 2는 wealth-strategist → (결과 읽기) → risk-reward-evaluator 순으로 **의도적으로 순차 실행**합니다.
이는 evaluator가 실제 생성된 전략 ID를 참조하여 정확한 평가를 수행하기 위함입니다.

knowledge-advisor는 지식베이스 4파일(~3,800줄)을 Read하므로 Phase 1에서 **가장 오래 걸리는 에이전트**입니다.
타임아웃을 120초로 설정한 이유입니다.

## DB 스키마 (4 테이블)

```sql
-- 사용자 재무 프로필 (버전 관리)
profiles (
  id INTEGER PRIMARY KEY,
  version INTEGER DEFAULT 1,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  monthly_income INTEGER,    -- 만원 단위
  monthly_expense INTEGER,
  savings INTEGER,
  investment_assets INTEGER,
  debt INTEGER,
  risk_tolerance TEXT,       -- low | medium | high
  goal TEXT
)

-- 에이전트 실행 결과 (디버깅/히스토리)
agent_results (
  id INTEGER PRIMARY KEY,
  profile_id INTEGER,
  agent_name TEXT,
  execution_time TIMESTAMP,
  result_json TEXT,          -- JSON blob
  status TEXT               -- success | failed | partial
)

-- [v3.0] 학습 진행률 추적
learning_progress (
  id INTEGER PRIMARY KEY,
  profile_id INTEGER,
  topic TEXT,                -- 학습 주제
  level TEXT,                -- 입문 | 중급 | 고급
  status TEXT,               -- 추천 | 학습중 | 완료
  expert_source TEXT,        -- 전문가 출처
  started_at TIMESTAMP,
  completed_at TIMESTAMP
)

-- [v3.0] 세션 히스토리
session_history (
  id INTEGER PRIMARY KEY,
  profile_id INTEGER,
  session_date TIMESTAMP,
  user_level TEXT,           -- 입문 | 중급 | 고급
  selected_strategy TEXT,
  matched_experts TEXT,      -- JSON array
  selected_workflows TEXT,   -- JSON array
  roadmap_path TEXT
)
```

## 보안 체크리스트

- [ ] `profiles.db` 파일 권한: `chmod 600` (자동 적용)
- [ ] `data/` 디렉토리 권한: `chmod 700` (자동 적용)
- [ ] 모든 SQLite 쿼리에 parameterized query 사용 (SQL Injection 방지)
- [ ] WebSearch 검색어에 개인 재무 정보(금액) 포함하지 않음
- [ ] 로그 파일에 금액 정보 기록하지 않음 (`agent-config.yaml: log_financial_amounts: false`)

## 에러 핸들링 패턴

```python
# 에이전트 파일 읽기 폴백 패턴
def read_agent_output(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default  # 기본값으로 계속 진행

# JSON 파싱 폴백 (outer json.loads)
try:
    existing = json.loads(result.stdout.strip())
except json.JSONDecodeError:
    existing = {"exists": False}

# 리스크 성향별 폴백 전략
fallback_strategies = {
    "low": [
        {"id": "F1", "title": "ISA 파킹통장 + 단기채권", "risk_level": "low"},
    ],
    "medium": [
        {"id": "F1", "title": "ISA 인덱스 ETF 적립식", "risk_level": "medium"},
    ],
    "high": [
        {"id": "F1", "title": "성장주 포트폴리오", "risk_level": "high"},
    ]
}
```

## 테스트 체크리스트

### 기본 기능

- [ ] `/rich-guide` 트리거로 스킬 실행 확인
- [ ] "부자 되는 법" 트리거로 스킬 실행 확인
- [ ] 8개 질문 인터뷰 완료 및 DB 저장 확인
- [ ] "잘 모르겠어요" 답변 시 기본값 적용 확인
- [ ] 로드맵 파일 생성 확인: `~/.claude/skills/rich-guide/roadmaps/`
- [ ] session_history 테이블에 세션 기록 확인

### 병렬 실행

- [ ] Phase 1: 3개 에이전트 동시 시작 확인 (diagnostician + knowledge-advisor + market)
- [ ] Phase 1: knowledge-advisor가 지식베이스 4파일 정상 Read 확인
- [ ] Phase 2A: wealth-strategist가 매칭된 전문가 기반 전략 생성 확인 (expert_source 포함)
- [ ] Phase 2B: risk-reward-evaluator가 실제 strategy IDs 사용 확인
- [ ] Phase 1 완료 후 Phase 2 시작 확인

### 재실행 및 캐시

- [ ] 24시간 이내 재실행: "기존 데이터 사용" 옵션 표시
- [ ] 1-30일 사이: "갱신 옵션" 3개 표시 (기존/부분/전체)
- [ ] 30일 이후: 새 인터뷰 진행 확인
- [ ] 기존 데이터 선택 시 인터뷰 건너뜀 확인

### 오류 처리

- [ ] portfolio-copilot 없을 때: 경고 표시 후 계속 진행
- [ ] market-pulse 없을 때: 경고 표시 후 계속 진행
- [ ] 에이전트 타임아웃: 폴백 전략 제공 확인
- [ ] DB 없을 때: init_db.py 자동 실행 확인
- [ ] agent-config.yaml 없을 때: 하드코딩 기본값으로 진행 확인

### 출력 검증

- [ ] 전략 3개 이상 생성 확인
- [ ] 각 전략에 expert_source (전문가명, 방법론) 포함 확인
- [ ] 각 전략에 learning_prerequisites 포함 확인
- [ ] 리스크/시간/분야 다양성 확인
- [ ] 면책 조항 포함 여부 확인
- [ ] 전문가 상담 링크 포함 여부 확인
- [ ] 로드맵 파일에 3-section (학습+실행+워크플로우) 포함 확인
- [ ] 로드맵 파일에 템플릿 플레이스홀더({PLACEHOLDER}) 없음 확인

### 대화형 모드 (rich-chat)

- [ ] `/rich-chat` 트리거로 스킬 실행 확인
- [ ] "재테크 상담" 트리거로 스킬 실행 확인
- [ ] 지식 베이스 8파일(knowledge 4 + workflow 4) 로드 확인
- [ ] 기존 프로필 있을 때: 레벨 맞춤 인사 메시지 출력
- [ ] 기존 프로필 없을 때: 일반 인사 + `/rich-guide` 안내
- [ ] 투자 질문에 지식 베이스 인용 포함 확인 (전문가명, 방법론)
- [ ] 부업 질문에 side-hustles.md 내용 참조 확인
- [ ] 고액(1,000만원+) 조언 시 면책 조항 포함 확인
- [ ] 여러 턴 대화 후에도 지식 베이스 참조 유지 확인

### 정리

- [ ] 세션 종료 후 `/tmp/rich-guide-*-{TS}.json` 파일 삭제 확인

## 로컬 개발 워크플로우

```bash
# 1. 플러그인 링크 설치
cd ~/Documents/Projects/claude-ai-engineering
npm run link

# 2. DB 수동 초기화 (개발/테스트용)
python3 plugins/rich-guide/config/init_db.py

# 3. DB 내용 확인
sqlite3 ~/.claude/skills/rich-guide/data/profiles.db \
  "SELECT id, risk_tolerance, goal, updated_at FROM profiles ORDER BY id DESC LIMIT 5;"

# 4. 에이전트 출력 확인 (디버깅)
ls /tmp/rich-guide-*.json
python3 -m json.tool /tmp/rich-guide-diagnostician-TIMESTAMP.json

# 5. 생성된 로드맵 확인
ls ~/.claude/skills/rich-guide/roadmaps/
cat ~/.claude/skills/rich-guide/roadmaps/roadmap-TIMESTAMP.md

# 6. DB 완전 초기화 (개발 중 리셋)
rm ~/.claude/skills/rich-guide/data/profiles.db
python3 plugins/rich-guide/config/init_db.py
```

## 버전 관리

버전 업데이트 기준:

- **MAJOR** (2.0.0): DB 스키마 변경, 에이전트 구조 변경, 파일 경로 변경
- **MINOR** (1.1.0): 새 에이전트 추가, 화이트리스트 확장, 신기능 추가
- **PATCH** (1.0.1): 버그 수정, 프롬프트 튜닝, 문서 업데이트

버전 변경 시 반드시 `.claude-plugin/plugin.json`의 `version` 필드를 업데이트하세요.

## 미래 개선 방향

### v3.1 계획
- 학습 진행률 자동 트래킹 (`learning_progress` 테이블 활용)
- 월별 체크인 알림 기능 (`/rich-guide check` 커맨드)
- 영어 출력 모드 (`/rich-guide --lang en`)

### v4.0 계획
- 자산 증가 시뮬레이션 그래프 (10년 예측)
- 커뮤니티 성공 사례 벤치마킹 데이터
- 대화형 모드에서 전략 수정 ("이 전략에서 투자 금액을 줄이고 싶어요")
- 지식 베이스 자동 업데이트 (최신 전문가 의견 반영)
- 대화형 세션 요약 → session_history 자동 저장

### 기술 부채
- [ ] 단위 테스트 추가 (`config/init_db.py` 스키마 검증)
- [ ] `whitelist.yaml` 자동 업데이트 메커니즘 (정기 검토)
- [ ] 에이전트 결과 JSON 파싱 실패 시 구조화된 재시도 로직
- [ ] 지식 베이스 파일 버전 관리 (마지막 수정일 추적)

## 관련 문서

- `README.md`: 사용자 가이드
- `../career-compass/CLAUDE.md`: 유사 다중 에이전트 패턴 참고
- `../portfolio-copilot/`: SQLite DB 패턴 참고
- `../market-pulse/`: 시장 데이터 연동 패턴 참고

## 지원

- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
