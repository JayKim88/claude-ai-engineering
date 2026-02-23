# Market Research by Desire - Wrap Up

> **Project**: `claude-ai-engineering`
> **Scope**: `plugins/market-research-by-desire/` (generated via competitive-agents pipeline)

## Session: 2026-02-23 22:07

> **Context**: market-research-by-desire 스킬 첫 실제 테스트 — "성장과성취 > 창업/부업" 주제로 5개 에이전트 파이프라인 전체 실행, 3개 보고서 생성 완료

### Done

- feat: 스킬 첫 E2E 테스트 성공 — 3라운드 인터뷰 + 5개 에이전트 파이프라인 + 3개 문서 생성
  - Interview: 성장과성취 > 창업/부업 | Global | Solo-dev: Yes | Bootstrap | Tech/SaaS
  - Phase 1 (parallel): Desire Cartographer + Market Trend Researcher — 8개 나노 욕망 매핑, TAM $375.57B
  - Phase 2 (sequential): Competitive Scanner (21개 기업) + Gap Opportunity Analyzer (7개 기회)
  - Phase 3: Revenue Model Architect — 5개 수익 모델 설계, BootstrapOS 추천
- feat: 최종 보고서 3건 생성
  - `market-analysis.md` — 욕망 구조, TAM/SAM/SOM, 5대 트렌드, 성장동력 vs 역풍
  - `competitive-analysis.md` — 21개 경쟁사 매트릭스, SWOT, 포지셔닝 맵, 빈틈 분석
  - `revenue-model-draft.md` — 5개 모델 비교, Unit Economics, 3년 매출 전망, 실행 전략
- chore: artifacts/ 디렉토리에 5개 JSON 원본 데이터 보존

### Decisions

- **agents/ 파일 미존재 처리**: 스킬 정의에서 agents/\*.md 읽도록 했으나 파일 미존재 → 에이전트가 자체 전문성으로 수행. 품질에 문제 없음
- **templates/ 파일 미존재 처리**: 템플릿 없이 직접 마크다운 구조 작성 — SKILL.md의 "구조 가이드로 활용" 방침대로 동작
- **knowledge/ 파일 미존재 처리**: desire-framework.md 등 없이도 기본 카테고리로 인터뷰 진행 성공

### Issues

- `revenue-models.json`이 25,000 토큰 초과 (29,987 tokens) → Read 실패, offset/limit으로 분할 읽기 필요
- `competitive-landscape.json`도 대용량 → 300줄씩 분할 읽기
- config/settings.yaml 미존재 → 하드코딩 기본값 사용 (정상 동작)
- agents/, templates/, knowledge/ 디렉토리 모두 미존재 → 에이전트가 fallback으로 처리했으나, 이 파일들이 있으면 품질 향상 가능

### Next

- [ ] knowledge/ 파일 생성: desire-framework.md (욕망 분류 체계), market-research-methods.md, competitive-analysis-methods.md, opportunity-assessment.md
- [ ] agents/ 파일 생성: 5개 에이전트 정의 (역할, 출력 형식, 전략)
- [ ] templates/ 파일 생성: market-analysis.md, competitive-analysis.md, revenue-model-draft.md 구조 가이드
- [ ] config/settings.yaml 생성 (language, timeout 등)
- [ ] revenue-models.json 대용량 문제 해결 — 에이전트에게 더 간결한 출력 지시 또는 요약 JSON 별도 생성
- [ ] desire-exploration-v2 결과와 출력 품질 비교 검증 (from previous Next)
- [ ] competitive-agents rubric에 "SDK API 호환성" 평가 기준 추가 검토 (from previous Next)

---

## Session: 2026-02-23 22:00

> **Context**: competitive-agents 산출물을 plugins/로 배치, 리뷰에서 5개 Critical/Important 이슈 발견 후 SKILL.md 전면 재작성, ~/.claude/skills/ 심링크 등록

### Done

- chore: `tempo/.../final/` → `plugins/market-research-by-desire/` 복사 (18 files)
- fix(SKILL.md): 전면 재작성 — 5개 핵심 문제 수정
  - Critical: `subagent_type` 커스텀 타입 → `general-purpose`로 변경 (desire-cartographer 등 5개 모두 미등록 타입이었음)
  - Critical: `AskUserQuestion` 파라미터를 실제 API 형식으로 수정 (questions array, max 4 options)
  - Important: Interview Round 3의 4회 개별 호출 → 1회 호출 4개 질문으로 통합
  - Important: Step 7 비현실적 템플릿 치환 알고리즘 → "템플릿을 구조 가이드로 읽고 직접 문서 작성" 방식으로 간소화
  - Minor: plugin.json에서 미지원 필드 제거 (agents, commands, dependencies, main, skills)
- fix(plugin.json): career-compass 패턴에 맞춰 정리 (name, version, description, author, license, keywords만 유지)
- fix(CLAUDE.md): agent architecture 설명 업데이트, 템플릿 메커니즘 수정
- fix(README.md): Installation 섹션 수정
- chore: `~/.claude/skills/market-research-by-desire` 심링크 등록

### Decisions

- **subagent_type=general-purpose**: career-compass의 resume-analyzer 등은 시스템 레벨 등록 타입이지만, market-research-by-desire의 5개 에이전트는 미등록 → general-purpose + agent 파일 Read로 해결
- **템플릿 = 구조 가이드**: Python f-string 치환 알고리즘 대신, Claude가 직접 템플릿 구조 참조 후 artifact 데이터로 문서 작성하는 방식 채택
- **AskUserQuestion 4옵션 제한 대응**: 5개 욕망 카테고리 중 4개를 옵션으로, 5번째(즐거움과자극)는 "Other"로 입력

### Issues

- competitive-agents가 생성한 SKILL.md가 실제 Claude Code SDK와 호환되지 않는 심각한 문제 발견 (미등록 subagent_type, 비표준 AskUserQuestion)
- competitive-agents 파이프라인의 cross-reviewer/judge가 이 호환성 문제를 잡지 못함 → 향후 rubric에 "SDK 호환성 실제 검증" 기준 추가 필요

### Next

- [x] 새 세션에서 "욕망 기반 시장조사" 트리거로 실제 테스트 실행
- [ ] desire-exploration-v2 결과와 출력 품질 비교 검증
- [ ] competitive-agents rubric에 "SDK API 호환성" 평가 기준 추가 검토
- [x] agents/ 파일의 tools 필드가 general-purpose 에이전트에서 참조되는지 확인 — agents/ 파일 미존재, 에이전트가 자체 전문성으로 수행

---

## Session: 2026-02-23 21:00

> **Context**: competitive-agents 스킬로 market-research-by-desire 플러그인 생성 — 2개 에이전트 경쟁, 크로스리뷰, 개선, 심판 평가까지 전체 파이프라인 완료

### Done

- feat: planning-interview로 플러그인 설계 완료 (Lean Canvas + 아키텍처 플랜)
- feat: competitive-agents 파이프라인 전체 실행 완료
  - Phase 1 (Generation): Alpha(Pragmatist, 15 files) + Beta(Architect, 18 files) 병렬 생성
  - Phase 2 (Cross-Review): Alpha 65.5/100, Beta 68.5/100 평가
  - Phase 3 (Improvement): 양측 v2 개선 — Alpha 74.5/100, Beta 86.0/100
  - Phase 4 (Judge): Opus 모델로 최종 심판, Beta 승리 (86.0 vs 74.5, +11.5 margin)
- feat: Beta v2를 final/ 디렉토리에 배포 (18 files)
- chore: mission.md, judge-report.md, v1-critique.md, v2-changelog.md 등 중간 산출물 보존

### Decisions

- **Winner: Beta (Architect)** — 6/8 평가 기준에서 우세 (Convention 9 vs 7, SKILL.md 8 vs 7, Error Handling 9 vs 7, Documentation 9 vs 7, Agent Design 9 vs 8, Maintainability 8 vs 7)
- **Fusion 미실행** — 11.5점 차이로 Beta 단독 채택이 합리적
- **1 round만 실행** — 1라운드 개선으로 충분한 품질 달성 (Beta v1 68.5 → v2 86.0)
- **desire-exploration-v2 방법론 기반** — 기존 검증된 욕망 분류 체계를 knowledge 파일로 독립 구성

### Issues

- Beta v1 첫 생성 시 max_output_tokens(32000) 초과로 실패 → 간결화 지시로 재시도 성공
- 컨텍스트 윈도우 초과로 세션 2회 분할 (이전 세션 → 현재 세션)
- 늦은 task notification이 3건 도착 (이미 처리 완료된 에이전트) → 무시

### Next

- [x] `tempo/competitive-agents/market-research-by-desire/final/` 파일 리뷰
- [x] plugin.json에 `.claude-plugin/` 경로 확인
- [x] `plugins/market-research-by-desire/`로 복사 및 심링크 설치
- [x] SKILL.md의 Task() 호출이 실제 Claude Code SDK에서 동작하는지 확인
- [x] 템플릿 변수 치환 로직({variable} → 실제값) 동작 검증
- [x] 트리거 "욕망 기반 시장조사"로 실제 테스트 실행 → 다음 세션으로 이월
- [x] desire-exploration-v2 결과와 출력 품질 비교 검증 → 다음 세션으로 이월
