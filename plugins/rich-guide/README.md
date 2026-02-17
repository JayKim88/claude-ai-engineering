# Rich Guide

**AI 다중 에이전트 기반 개인화 부자 전략 시스템**

재테크/투자/부업 정보의 파편화 문제를 해결하는 Claude Code 플러그인.
6개 전문 AI 에이전트가 협력하여 사용자의 재무 상태를 진단하고,
신뢰할 수 있는 정보를 큐레이션하여, 맞춤형 부자 전략과 주간 실행 로드맵을 생성합니다.

---

## 핵심 문제 해결

재테크 초보자가 겪는 "선택 마비" 문제:

- 유튜브/블로그에 정보가 넘치지만 신뢰도 판단이 어려움
- 개인 상황에 맞는 전략을 찾기 힘듦
- 어디서 시작해야 할지 모름

Rich Guide의 해답: AI 재무 상담사가 현재 상황을 분석하고, 흩어진 정보를 정리하여, 실행 가능한 첫 걸음을 제시합니다.

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                  SKILL.md (Orchestrator)                    │
│          AskUserQuestion + Task() 에이전트 조율             │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────▼───────────────┐
        │   Step 1: 환경 설정           │
        │   agent-config.yaml 로드      │
        │   profiles.db 초기화          │
        └───────────────┬───────────────┘
                        │
        ┌───────────────▼───────────────┐
        │   Step 2: 재무 인터뷰         │
        │   (7 필드, 기본값 폴백)        │
        │   24h 캐시 / 1-30d 갱신 분기  │
        │   profiles.db 로컬 저장       │
        └───────────────┬───────────────┘
                        │
        ┌───────────────▼─────────────────────────────────────┐
        │         Phase 1: 병렬 분석 (3개 에이전트)           │
        │                                                     │
        │  [financial-diagnostician]  [info-curator]          │
        │       Sonnet                    Haiku               │
        │  재무 건강도 점수화         화이트리스트 수집         │
        │                                                     │
        │  [market-context-analyzer]                          │
        │       Sonnet                                        │
        │  시장 맥락 분석                                     │
        └───────────────┬─────────────────────────────────────┘
                        │ /tmp/rich-guide-phase1-{ts}.json
        ┌───────────────▼─────────────────────────────────────┐
        │         Phase 2: 순차 전략 생성 + 평가              │
        │                                                     │
        │  Step 2A: [wealth-strategist]  →  전략 ID 확보      │
        │               Opus                                  │
        │  3-5개 전략 생성                                    │
        │                                                     │
        │  Step 2B: [risk-reward-evaluator]                   │
        │               Sonnet                                │
        │  실제 전략 ID 기반 리스크/보상 점수화               │
        └───────────────┬─────────────────────────────────────┘
                        │ 전략 선택 (AskUserQuestion)
        ┌───────────────▼─────────────────────────────────────┐
        │         Phase 3: 순차 실행 계획 생성                │
        │                                                     │
        │  [action-plan-generator]                            │
        │       Opus                                          │
        │  roadmap-template.md 읽기 → 플레이스홀더 채우기     │
        │  12주 주간 체크리스트 생성                          │
        │  ~/.claude/skills/rich-guide/roadmaps/*.md          │
        └─────────────────────────────────────────────────────┘
```

---

## 설치

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link
```

DB는 첫 실행 시 자동으로 초기화됩니다. 수동 초기화가 필요하면:

```bash
python3 plugins/rich-guide/config/init_db.py
```

---

## 사용법

### 트리거 구문

```
# 한국어
부자 되는 법
재테크 가이드
재무 분석
투자 전략
재테크 시작
/rich-guide

# 영어
rich guide
wealth strategy
financial planning
```

### 예시 1: 재테크 초보자 첫 실행

```
사용자: "부자 되는 법"

시스템: 재무 상태 분석을 시작합니다...

[7개 질문 인터뷰]
  월수입: 400만원
  월지출: 280만원
  예금: 1,500만원
  투자자산: 없음
  부채: 없음
  리스크 성향: 중위험
  목표: 자산 증식

Phase 1: 진단 시작 (3개 에이전트 병렬 실행)...
  재무 진단 완료 (건강점수: 68점)
  정보 수집 완료 (5개 검증 기사)
  시장 분석 완료

Phase 2-A: 전략 생성 중 (wealth-strategist)...
  4개 전략 생성됨

Phase 2-B: 리스크/보상 평가 중 (risk-reward-evaluator)...
  실제 전략 ID 기반 평가 완료

[전략 선택]
1. ISA + TIGER S&P500 ETF 장기 적립 (중위험 | 장기 | 연 7-10%)
2. 연금저축펀드 세액공제 극대화 (저위험 | 장기 | 세금 절약)
3. 직장인 프리랜서 부업 시작 (중위험 | 중기 | 월 +30만원)
4. 고금리 파킹통장 + 단기채권 (저위험 | 단기 | 연 4-5%)

사용자: "1번 선택"

Phase 3: 실행 계획 생성 중 (템플릿 기반)...
  12주 로드맵 생성 완료

결과:
  재무 건강도: 68점 (B등급)
  선택 전략: ISA + TIGER S&P500 ETF 장기 적립
  로드맵 파일: ~/.claude/skills/rich-guide/roadmaps/roadmap-{timestamp}.md
```

### 예시 2: 24시간 이내 빠른 재실행

```
사용자: "재테크 가이드"

시스템: 기존 재무 데이터(2026-02-17 작성)를 사용할까요?
  - 기존 데이터 사용 (빠름, 약 90초)
  - 새로 입력 (정확, 약 5분)

사용자: 기존 데이터 사용

[인터뷰 없이 Phase 1부터 즉시 시작]
→ 약 90초 후 전략 목록 출력
```

### 예시 3: 저위험 사용자 (안전 추구형)

```
사용자: "wealth strategy"

[인터뷰에서 리스크 성향: 저위험 선택]

생성 전략:
1. 고금리 파킹통장 + 단기채권 ETF (저위험 | 단기 | 연 4-5%)
2. ISA 예금 비과세 활용 (저위험 | 중기 | 세금 절약)
3. 연금저축 IRP 세액공제 최대화 (저위험 | 장기 | 세금 절약)
```

---

## 주요 기능

### FR-1: 7-Field 재무 인터뷰

월수입, 월지출, 예금, 투자자산, 부채, 리스크성향, 목표 7가지 정보 수집.
"잘 모르겠어요" 답변 시 한국 직장인 평균 기반 기본값 자동 적용.

### FR-2: SQLite 로컬 프로필 저장

`~/.claude/skills/rich-guide/data/profiles.db`에 버전별로 저장.
24시간 이내: 재사용 제안. 1-30일: 부분/전체 갱신 선택 가능. 30일 초과: 새 인터뷰.
DB 파일 권한 `600` (소유자만 읽기/쓰기).

### FR-3: 6-에이전트 파이프라인

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| financial-diagnostician | claude-sonnet-4-5-20250929 | 재무 건강도 0-100점 산출 |
| info-curator | claude-haiku-4-5 | 화이트리스트 기반 재테크 정보 수집 |
| market-context-analyzer | claude-sonnet-4-5-20250929 | 현재 금리/시장 상황 분석 |
| wealth-strategist | claude-opus-4-6 | 개인화 전략 3-5개 생성 |
| risk-reward-evaluator | claude-sonnet-4-5-20250929 | 실제 전략별 리스크/보상 정량 평가 |
| action-plan-generator | claude-opus-4-6 | 12주 주간 체크리스트 생성 |

### FR-4: 전략 다양성 보장

리스크(저/중/고) x 시간(1년/3년/10년) x 분야(투자/부업/커리어/절약) 조합.
사용자 리스크 성향에 따른 자동 전략 비중 조정.

### FR-5: 도메인 화이트리스트 큐레이션

한국경제, 서울경제, 네이버증권, 금융감독원 등 검증된 출처 우선.
미검증 출처는 수집하되 "미검증" 라벨 명시.

### FR-6: 주간 실행 체크리스트

월별 목표를 주간 태스크로 분해. 각 항목 예상 소요 시간 명시.
예: 1주차: ISA 계좌 개설 (30분), 2주차: 자동이체 설정 (15분).
템플릿(`templates/roadmap-template.md`) 기반으로 일관된 출력 보장.

### FR-7: 기존 플러그인 연동

portfolio-copilot DB 및 market-pulse 분석 파일 직접 읽기.
미설치 시 경고 메시지 + 기본값으로 계속 진행.

### FR-8: 3-Layer 검증

- Layer 1: 모든 출력에 AI 면책 조항 포함
- Layer 2: 모든 추천에 출처 URL 명시
- Layer 3: 최종 출력에 전문가 상담 권유 링크

---

## 설정

`config/agent-config.yaml` 편집으로 커스터마이징 (orchestrator가 자동 로드):

```yaml
# 타임아웃 조정 (인터넷이 느린 환경)
timeouts:
  info_curator: 120       # 기본 90초 → 120초
  wealth_strategist: 180  # 기본 120초 → 더 상세한 전략 원할 때

# 모델 변경 (비용 절약 시)
models:
  wealth_strategist: "claude-sonnet-4-5-20250929"  # opus → sonnet

# 인터뷰 기본값 변경
interview:
  defaults:
    monthly_income: 400  # 400만원으로 변경
```

---

## 트러블슈팅

### "데이터베이스 초기화 실패"

```bash
# Python 3 설치 확인
python3 --version

# 수동으로 DB 초기화
python3 plugins/rich-guide/config/init_db.py

# 디렉토리 권한 확인
mkdir -p ~/.claude/skills/rich-guide/data
chmod 700 ~/.claude/skills/rich-guide/data
```

### "에이전트 타임아웃" 오류

```yaml
# config/agent-config.yaml 수정
timeouts:
  wealth_strategist: 180
  action_plan_generator: 180
  info_curator: 120
```

### "market-pulse / portfolio-copilot 데이터 없음"

플러그인 미설치 시 기본 전략으로 자동 진행됩니다.
더 정확한 분석을 원하면:

```
/market-pulse
/portfolio-copilot
```

### "로드맵 파일을 찾을 수 없음"

```bash
# 저장 경로 확인
ls ~/.claude/skills/rich-guide/roadmaps/

# 권한 확인
chmod 755 ~/.claude/skills/rich-guide/roadmaps
```

---

## 성능

| 단계 | 소요 시간 |
|------|----------|
| 환경 설정 | 2-5초 |
| 재무 인터뷰 | 2-3분 (응답 시간 포함) |
| Phase 1 병렬 (3개 에이전트) | 45-90초 |
| Phase 2A 순차 (wealth-strategist) | 60-120초 |
| Phase 2B 순차 (risk-reward-evaluator) | 30-60초 |
| Phase 3 순차 | 60-120초 |
| **전체 (첫 실행)** | **4-6분** |
| **전체 (캐시 재실행)** | **90-120초** |

**예상 비용:** 약 $2.00-2.50/회 (Haiku x1 + Sonnet x3 + Opus x2)

---

## 데이터 프라이버시

- 모든 재무 데이터는 `~/.claude/skills/rich-guide/data/profiles.db`에만 저장
- 외부 서버로 재무 정보 전송 없음
- WebSearch 시 개인 재무 금액 정보가 아닌 일반 키워드만 전송
- DB 파일 권한: `600` (소유자만 읽기/쓰기)
- 로그에 금액 정보 기록하지 않음
- 세션 종료 후 `/tmp/rich-guide-*-{ts}.json` 임시 파일 자동 정리

---

## 연관 플러그인

| 플러그인 | 관계 | 설명 |
|---------|------|------|
| market-pulse | 데이터 소스 (선택) | 시장 데이터 제공 |
| portfolio-copilot | 데이터 소스 (선택) | 포트폴리오 현황 제공 |
| career-compass | 보완 플러그인 | 커리어 수입 성장 전략 |

---

## 에이전트 모델 선택 근거

| 에이전트 | 모델 | 근거 |
|---------|------|------|
| financial-diagnostician | claude-sonnet-4-5-20250929 | 재무 수치 분석, 패턴 인식에 깊이 필요 |
| info-curator | claude-haiku-4-5 | 속도 우선, 웹서치 처리는 간단 |
| market-context-analyzer | claude-sonnet-4-5-20250929 | 경제 지표 해석, 복합 분석 필요 |
| wealth-strategist | claude-opus-4-6 | 창의적 개인화 전략 생성이 핵심 가치 |
| risk-reward-evaluator | claude-sonnet-4-5-20250929 | 정량 평가, 분석력 중요 |
| action-plan-generator | claude-opus-4-6 | 구체적 실행 계획이 최종 사용자 가치 |

---

## 라이선스

MIT License

## 저자

Jay Kim (https://github.com/JayKim88)

---

재테크를 시작하는 첫 걸음, Rich Guide가 함께합니다.

```
부자 되는 법
```
