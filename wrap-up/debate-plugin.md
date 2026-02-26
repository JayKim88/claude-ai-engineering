# Debate Plugin - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/prism-debate/`, `~/.claude/CLAUDE.md`, `~/.claude/context/`

## Session: 2026-02-26 20:06

> **Context**: debate → prism-debate 리네임 + 에이전트 2개 신규 추가 (Alternative, Pre-Mortem) + Worldview 캐릭터화 + README v2 (Mermaid + How It Works)

### Done

- feat(prism-debate): `debate` → `prism-debate` 리네임 (v3.0.0)
  - `plugins/debate/` → `plugins/prism-debate/`, `skills/debate/` → `skills/prism-debate/`
  - `plugin.json`: name "prism-debate", version "3.0.0", 트리거 `prism`, `prism-debate`, `/prism`
  - `SKILL.md`, `CLAUDE.md`, `README.md` 모든 참조 업데이트

- feat(prism-debate): 에이전트 2개 신규 생성
  - `agents/alternative.md` — "The Inventor" (REFRAME): 명제 밖 대안 2-3개 구체 제시, 이분법 맹점 해소. De Bono Green Hat 기반.
  - `agents/pre-mortem.md` — "The Oracle" (FUTURE FAILURE): 실패 기정사실로 두고 역추적, 5 Whys 인과 체인. Gary Klein PreMortem 기반.

- feat(prism-debate): 모든 에이전트 Worldview 캐릭터화 (Moltbook 인사이트)
  - Optimist → "The Builder": "변화는 항상 가능하다. 현상 유지가 진짜 리스크다"
  - Critic → "The Skeptic": "대부분은 실패한다. 입증 부담은 명제 쪽에 있다"
  - Pragmatist → "The Operator": "자원과 시간은 항상 당신 생각보다 부족하다"
  - Synthesizer → "The Judge": "좋은 판결은 틀릴 수 있는 것을 정직하게 인정하는 것이다"

- feat(prism-debate): SKILL.md Core/Extended 에이전트 선택 로직 추가
  - Core (3): Optimist + Critic + Pragmatist — 빠르고 집중적
  - Extended (5): + Alternative + Pre-Mortem — 고위험/전략 결정용
  - Mode 선택 시 에이전트 구성도 함께 선택

- docs(prism-debate): README v2 전면 개선
  - Mermaid 다이어그램 2개: System Architecture + UX Flow
  - How It Works 신규 섹션: Evidence hierarchy, Position labels, Verdict types + 최소 요건
  - Context Integration 섹션: values/constraints.md 활용 방식, Decision Log 품질 기준
  - Output Reference 섹션: 라운드별/synthesis 출력 포맷 가이드
  - Purpose 섹션 개선: 구체적 상황 5개 + 쓰지 않는 상황 명시 (from previous Next ✓)

- docs(prism-debate): CLAUDE.md 전면 업데이트 (v3.0.0 아키텍처, 에이전트 테이블, 검증 체크리스트)

### Decisions

- **이름 prism-debate**: "prism"(목적: 다각 분석) + "debate"(메커니즘: 교차 반박) 합성으로 왜/어떻게 동시 전달
- **De Bono Six Hats 매핑**: Yellow(Optimist) + Black(Critic) + White(Pragmatist) + Green(Alternative) + 별도 Oracle(Pre-Mortem) — Red Hat(직관)은 Future 보류
- **Moltbook 인사이트**: 스탠스(FOR/AGAINST)보다 Worldview(세계관)가 에이전트를 더 일관되고 예측 가능하게 만듦
- **Alternative 우선 추가**: 이분법 맹점(A vs not-A)이 가장 보편적 blind spot → 첫 확장 에이전트
- **Pre-Mortem은 Critic과 다름**: Critic은 순방향 위험 식별, Pre-Mortem은 실패 기정사실 + 역추적 → 별도 에이전트 정당화
- **2-티어 구조**: Core 3(항상) + Extended 2(선택) — 복잡도 최소화 vs 분석 깊이 균형

### Next

- [ ] prism-debate Mode 0 Core로 실제 결정 테스트 (e.g. 기술 스택, 커리어 결정)
- [ ] prism-debate Extended 모드 테스트 — Alternative + Pre-Mortem 실제 동작 확인
- [ ] decision-log.md 첫 번째 실제 엔트리 기록
- [ ] Future agents 설계: Gut Check (Red Hat / 직관·가치관) + Red Team (악의적 공격 시뮬레이션)
- [ ] Layer 1 강화: `~/.claude/context/` 파일들 실제 토론에서 사용하며 업데이트

---

## Session: 2026-02-26 17:44

> **Context**: 5-layer AI quality system 구현 + think-deep → debate v2 리네임 + 멀티라운드 tiki-taka 토론 엔진 설계 및 구현

### Done

- feat: 5-layer AI quality system 설계 및 구현
  - Layer 3 (Output Quality): `~/.claude/CLAUDE.md`에 Claim Labeling 규칙 추가 ([FACT]/[ESTIMATE]/[OPINION]/[UNCERTAIN])
  - Layer 5 (Usage Quality): `~/.claude/CLAUDE.md`에 Question Routing 테이블 추가 (technical/values-based/prediction 분류)
  - Layer 1 (Input Quality): `~/.claude/context/` 인프라 생성 (values.md, constraints.md, decision-log.md)
  - Layer 2 (Process Quality): debate 플러그인으로 구현
  - Layer 4 (Validation Quality): decision-log.md 템플릿으로 구현

- feat(debate): `think-deep` → `debate` 플러그인 리네임
  - `plugins/think-deep/` → `plugins/debate/`
  - `skills/think-deep/` → `skills/debate/`
  - `plugin.json` name/version 업데이트 (v2.0.0)
  - `CLAUDE.md`, `README.md` 내 모든 참조 업데이트

- feat(debate): v2 멀티라운드 토론 엔진 구현
  - `skills/debate/SKILL.md` 전면 재작성 (5-step → 7-step)
  - Mode 0 (빠른 판결): 1 라운드 → 즉시 synthesis
  - Mode 1 (자율 토론): 에이전트 tiki-taka, 사용자가 각 라운드 후 종료 결정
  - Mode 2 (참여형 토론): 사용자가 매 라운드 논거 투입 가능

- feat(debate): 컨텍스트 자동 감지 기능 추가
  - "debate"만 입력해도 최근 대화에서 결정 주제 자동 추출
  - 사용자 확인 후 진행 또는 직접 입력으로 전환

- feat(debate): 에이전트 4개 Round N Behavior 추가
  - `optimist.md`: [MAINTAINED/PARTIALLY_CONCEDED/SHIFTED] + 상대 논거 직접 반박 규칙
  - `critic.md`: Optimist 최강 논거 직접 챌린지 + 에스컬레이션 규칙
  - `pragmatist.md`: 이전 라운드 기반 feasibility 업데이트 + unknown 해소 또는 심화 규칙
  - `synthesizer.md`: Position Evolution 섹션 추가 (다중 라운드 시 필수)

- feat(debate): llm-council 개념 선택적 채택
  - 채택: 교차 반박 (에이전트가 상대 논거 직접 인용), 포지션 추적, 수렴 감지, synthesizer 전체 히스토리 수신
  - 미채택: 익명화 (단일 모델이므로 불필요), 다중 LLM, Stage 2 랭킹

- chore: `~/.claude/context/` 개인화된 컨텍스트 파일 생성
  - `values.md`: 4-goal framework (커리어 70%, 독일 2027, 스타트업 30%, 투자)
  - `constraints.md`: 서울 재택 전용, 6mo 타임라인, 기술 프로필
  - `decision-log.md`: 빈 추적 테이블

### Decisions

- **debate vs 별도 재검증 도구**: Layer 3 (always-on claim labeling)이 일상 답변 신뢰성 커버, debate Mode 0이 집중 재검증 커버 → 별도 도구 불필요
- **익명화 미채택**: llm-council의 익명화는 다중 LLM prestige bias 방지용; 단일 Claude 모델에서는 역할명이 tiki-taka 구조에 필요하므로 미채택
- **Claude Max = 추가 API 비용 없음**: Task() 호출은 구독 내 포함, 라운드 제한 불필요

### Next

- [ ] debate Mode 0으로 실제 결정 테스트 (e.g. 기술 스택 선택, 커리어 결정)
- [ ] decision-log.md 첫 번째 실제 엔트리 기록
- [x] debate 주제 범위 확장 고려: 중요한 결정뿐만 아니라 탐구적 질문, 개념 분석도 지원 여부 결정 (from previous Next — README Purpose 섹션에서 해결)
- [ ] "verify" 모드 추가 검토: 특정 Claude 답변을 debate 에이전트로 사후 검증하는 shortcut
- [ ] Layer 1 강화: `~/.claude/context/` 파일들 실제 사용하며 업데이트
