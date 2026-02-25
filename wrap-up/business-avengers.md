# Business Avengers - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/business-avengers/`

## Session: 2026-02-25 14:51

> **Context**: v2.1 감사 37건 잔여 항목 완료 + Phase 0 아이디어 문서 입력 기능 추가

### Done
- feat: v2.1 감사 잔여 항목 전체 완료 (from previous Next)
  - I2: Phase 9 CS Manager에 GTM 전략 컨텍스트 추가
  - I3: Phase 5 프론트/백엔드 개별 sprint_context 변수 분리 (`sprint_context_frontend`, `sprint_context_backend`)
  - I5: Phase 11 sprint_context에 sprint_goal 포함
  - I7: Step 20 (Sprint Completion)에 sprint-review.md 템플릿 기반 리뷰 생성 통합
  - I8: RESUME 모드에서 `workflow` 변수 미정의 버그 수정
  - I10: Phase 실행 루프 명시적 매핑 추가 (Phase 0→Step 4, ..., Phase 12→Step 16)
  - I11: 완료 후 라우팅 추가 (Sprint→Step 20, Orchestra→Step 21)
  - M7: market-first 모드 Phase 0에서 Phase 1 결과물 읽기 추가
  - M8: SINGLE_PHASE 모드 범위 체크 추가 (0-12 외 입력 시 오류 안내)
  - M1-M6, M9: org-structure.yaml inputs_from/agents 동기화
- feat: Phase 0 아이디어 문서 입력 기능 추가
  - Q&A 시작 전 CPO가 먼저 "기존 문서가 있나요?" 분기 질문
  - 파일 경로 입력 시 Glob+Read로 로드 (확장자 + `/` 포함 감지)
  - 텍스트 붙여넣기 시 그대로 사용
  - 파일 못 찾으면 텍스트로 폴백 + 안내 메시지
  - 기존 Q&A 흐름은 `else` 분기로 완전 보존

### Decisions
- 문서 입력 방식: `--from-doc` 커맨드 플래그 대신 Phase 0 CPO 대화 내 자연스러운 분기 채택 (UX 우선, 커맨드 변경 없음)
- 파일 경로 판별: `/` 또는 `\` 포함 AND 확장자 체크 (`.md`, `.txt`, `.pdf`, `.docx`)

### Issues
- E2E 테스트 중 AskUserQuestion 툴 거부로 테스트 중단 (permission mode 이슈)
- Skill 로드 시 일부 구버전 내용이 반영되는 현상 관찰 — 캐시 혹은 심링크 타이밍 가능성 (미확인)

### Next
- [ ] 새 세션에서 E2E 전체 플로우 테스트 (Phase 0→1→2)
  - [ ] 문서 입력 분기 검증 (파일 경로 / 텍스트 붙여넣기 양쪽)
  - [ ] Q&A 분기 정상 동작 검증
  - [ ] Phase 1 병렬 3개 에이전트 실행 및 출력 검증

---

## Session: 2026-02-23

### Done
- feat: v2.0 MAKE Methodology Extension 완료
  - Indie Maker Handbook (@levelsio) 컨텐츠를 KB, 에이전트, 템플릿, 오케스트레이터 4개 레이어에 통합
  - Phase 10 (Growth), Phase 11 (Automation), Phase 12 (Scale & Exit) 추가
  - 3개 KB, 15개 템플릿, 3개 워크플로우 프리셋 (make, full-lifecycle, post-launch) 추가
  - 6개 에이전트에 MAKE 프레임워크 추가 (CPO, PM, Growth Hacker, PR Manager, Revenue Strategist, DevOps)
- fix: v2.0.1 MAKE Audit 수정 (Part 2-4)
  - 에이전트 역할 경계 정리: 실행전략 오버라이드 제거 3건 (marketing-strategist, devops-engineer, revenue-strategist)
  - Phase 11 에이전트 재배치: CS Manager + Data Analyst → Business Analyst
  - 템플릿 MAKE 컨텐츠 압축 (gtm ~94행→~30행, cs-playbook Stripe 일반화, pricing-strategy 섹션 재배치)
  - Step 번호 통일 (11.5-11.9 → 12-16)
- docs: v2.1 프로세스 플로우 감사 수행 및 TODO 생성 (37건)
  - 3개 병렬 Opus Explore 에이전트로 전체 프로세스 감사
  - CRITICAL 4 / HIGH 7 / IMPORTANT 13 / MEDIUM 4 / MINOR 9
- docs: 외부 AI UX/Content 리뷰 검증 및 TODO 반영
  - 6건 신규 UX 발견 채택 (UX1-UX5, UX8), 2건 기존 확장
  - pricing-strategy "과다" 판단은 부정확으로 기각
- chore: 단일 커밋 `34d9173` (35파일, +14,192행)

### Decisions
- MAKE 컨텐츠 배치 원칙: "Would a professional naturally use this framework regardless of MAKE?" → Yes: 에이전트 identity, No: KB reference
- Phase 11 에이전트 통합: CS Manager + Data Analyst → Business Analyst 1개로 통합
- UX1 Fix 방향: make 프리셋에 Phase 2 추가보다 idea-canvas fallback 로직 채택 (린 철학 유지)

### Issues
- make 프리셋 `[0,1,7,8,10,11]`에서 Phase 2 미실행 → 에이전트가 PRD 없이 작업 (UX1)
- post-launch 프리셋 `[10,11,12]`에 기존 서비스 온보딩 부재 (UX2)
- 12개 승인 게이트에서 "수정 요청" 선택 시 실제 분기 처리 없음 (C1)

### Next
- [x] v2.1 감사 수정 실행 (37건) — 상세: `docs/TODO-v2.1-audit.md`
  - [x] C2+C4: KB 참조 + 변수명 빠른 수정
  - [x] C3+UX1: Glob guard + idea-canvas fallback
  - [x] H4+H5: current_version, project_slug 변수 정의
  - [x] H1+H2+H3: Sprint 모드 Phase 0/12 추가
  - [x] C1: 승인 게이트 분기 처리
  - [x] UX2: post-launch 온보딩 스텝
  - [x] UX5: Sprint 옵션 전체 Phase 포함 + 용어 통일
  - [x] I1-I13: 개선사항
  - [x] UX3+UX8: MAKE 네이밍 + Phase 12 타이밍
  - [x] M1-M9+UX4: 마이너 정리
