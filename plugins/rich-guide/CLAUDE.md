# Rich Guide - Developer Guide

Rich Guide 플러그인 개발 및 유지보수 가이드.

## 디렉토리 구조

```
plugins/rich-guide/
├── .claude-plugin/
│   └── plugin.json              # 플러그인 메타데이터
├── skills/
│   └── rich-guide/
│       └── SKILL.md             # Orchestrator (핵심 실행 로직)
├── agents/                      # 6개 전문 에이전트
│   ├── financial-diagnostician.md   # 재무 건강도 진단 (Sonnet)
│   ├── info-curator.md              # 화이트리스트 정보 수집 (Haiku)
│   ├── market-context-analyzer.md   # 시장 맥락 분석 (Sonnet)
│   ├── wealth-strategist.md         # 전략 생성 (Opus)
│   ├── risk-reward-evaluator.md     # 리스크 평가 (Sonnet)
│   └── action-plan-generator.md    # 실행 계획 생성 (Opus)
├── commands/
│   └── rich-guide/
│       └── rich-guide.md        # /rich-guide 커맨드 정의
├── config/
│   ├── init_db.py               # SQLite 초기화 스크립트
│   ├── agent-config.yaml        # 에이전트 동작 파라미터 (orchestrator가 로드)
│   └── whitelist.yaml           # 신뢰 도메인 화이트리스트
├── templates/
│   └── roadmap-template.md      # 로드맵 출력 템플릿 (action-plan-generator가 사용)
├── CLAUDE.md                    # 개발자 가이드 (이 파일)
└── README.md                    # 사용자 가이드
```

## 에이전트 역할 및 실행 순서

| 에이전트 | 모델 | Phase | 입력 | 출력 파일 |
|---------|------|-------|------|----------|
| financial-diagnostician | Sonnet | 1 (병렬) | 재무 프로필 JSON | `/tmp/rich-guide-diagnostician-{ts}.json` |
| info-curator | Haiku | 1 (병렬) | 리스크 성향, 목표 | `/tmp/rich-guide-curator-{ts}.json` |
| market-context-analyzer | Sonnet | 1 (병렬) | market-pulse 파일 | `/tmp/rich-guide-market-{ts}.json` |
| wealth-strategist | Opus | 2A (순차) | Phase 1 통합 결과 | `/tmp/rich-guide-strategist-{ts}.json` |
| risk-reward-evaluator | Sonnet | 2B (순차) | Phase 1 결과 + 실제 전략 목록 | `/tmp/rich-guide-evaluator-{ts}.json` |
| action-plan-generator | Opus | 3 (순차) | 선택 전략 + 전체 컨텍스트 + 템플릿 | `~/.claude/skills/rich-guide/roadmaps/roadmap-{ts}.md` |

## 전체 실행 흐름

```
SKILL.md Step 1: Environment Setup & Config Load
  ├── agent-config.yaml 로드 (타임아웃, 캐시 임계값 등)
  ├── DB 존재 확인 → 없으면 init_db.py 자동 실행 (절대 경로 사용)
  └── 기존 프로필 조회 (24h 캐시 / 1-30d 갱신 / 신규)

SKILL.md Step 2: Financial Interview
  ├── 24h 이내: "기존 데이터 사용" 옵션
  ├── 1-30일: "일부 업데이트 / 전체 재입력" 옵션 (AskUserQuestion)
  ├── AskUserQuestion 7회 (월수입 / 월지출 / 예금 / 투자자산 / 부채 / 리스크 / 목표)
  ├── "잘 모르겠어요" 기본값 폴백 처리
  └── profiles 테이블에 저장 (parameterized query)

SKILL.md Step 3: Phase 1 Parallel
  ├── 단일 응답 블록에서 3개 Task() 동시 호출 [CRITICAL]
  └── 각 결과를 /tmp/rich-guide-{agent}-{ts}.json에 저장

SKILL.md Step 4: Phase 2 Sequential
  ├── wealth-strategist Task() → 완료 후 결과 읽기
  ├── 실제 strategy IDs 확보
  └── risk-reward-evaluator Task() (실제 전략 목록을 프롬프트에 포함)

SKILL.md Step 5: Strategy Selection
  └── AskUserQuestion으로 사용자가 전략 선택

SKILL.md Step 6: Phase 3 Sequential
  ├── roadmap-template.md 읽기
  └── action-plan-generator Task() → 템플릿 플레이스홀더 채워 .md 파일 생성

SKILL.md Step 7: Final Report & Cleanup
  ├── 3-Layer 검증 (면책 조항 + 출처 + 전문가 링크)
  ├── 콘솔 요약 출력
  └── /tmp/rich-guide-*-{ts}.json 임시 파일 정리
```

## 병렬 실행 패턴 (CRITICAL)

Claude Code에서 병렬 에이전트 실행은 **반드시 단일 응답에서** 모든 Task() 호출이 이루어져야 합니다.

```python
# 올바른 방법 - 단일 응답 블록에서 동시 호출
Task(subagent_type="financial-diagnostician", ...)
Task(subagent_type="info-curator", ...)
Task(subagent_type="market-context-analyzer", ...)

# 잘못된 방법 - 각각 다른 응답에서 호출하면 순차 실행됨
result1 = Task(...)  # 응답 1
result2 = Task(...)  # 응답 2 (순차 실행)
```

Phase 2는 wealth-strategist → (결과 읽기) → risk-reward-evaluator 순으로 **의도적으로 순차 실행**합니다.
이는 evaluator가 실제 생성된 전략 ID를 참조하여 정확한 평가를 수행하기 위함입니다.

## DB 스키마

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
- [ ] 7개 질문 인터뷰 완료 및 DB 저장 확인
- [ ] "잘 모르겠어요" 답변 시 기본값 적용 확인
- [ ] 로드맵 파일 생성 확인: `~/.claude/skills/rich-guide/roadmaps/`

### 병렬 실행

- [ ] Phase 1: 3개 에이전트 동시 시작 확인 (로그 타임스탬프)
- [ ] Phase 2A: wealth-strategist 완료 후 결과 파일 존재 확인
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
- [ ] 리스크/시간/분야 다양성 확인
- [ ] 각 전략에 출처 포함 여부 확인
- [ ] 면책 조항 포함 여부 확인
- [ ] 전문가 상담 링크 포함 여부 확인
- [ ] 로드맵 파일에 템플릿 플레이스홀더 없음 확인

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

### v2.1 계획
- 전략 실행률 트래킹 (완료된 체크리스트 항목 수 추적)
- 월별 체크인 알림 기능 (`/rich-guide check` 커맨드)
- 영어 출력 모드 (`/rich-guide --lang en`)

### v3.0 계획
- 자산 증가 시뮬레이션 그래프 (10년 예측)
- 커뮤니티 성공 사례 벤치마킹 데이터
- 대화형 전략 수정 ("이 전략에서 투자 금액을 줄이고 싶어요")
- 다국어 완전 지원 (영어/일어)

### 기술 부채
- [ ] 단위 테스트 추가 (`config/init_db.py` 스키마 검증)
- [ ] `whitelist.yaml` 자동 업데이트 메커니즘 (정기 검토)
- [ ] 에이전트 결과 JSON 파싱 실패 시 구조화된 재시도 로직

## 관련 문서

- `README.md`: 사용자 가이드
- `../career-compass/CLAUDE.md`: 유사 다중 에이전트 패턴 참고
- `../portfolio-copilot/`: SQLite DB 패턴 참고
- `../market-pulse/`: 시장 데이터 연동 패턴 참고

## 지원

- GitHub Issues: https://github.com/JayKim88/claude-ai-engineering/issues
