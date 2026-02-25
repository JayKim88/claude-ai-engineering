# planning-interview - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/planning-interview/`, `plugins/spec-interview/`

## Session: 2026-02-25 18:15

> **Context**: planning-interview E2E 전체 검증 완료 — LinguaRAG Product Brief 임포트 후 4종 문서 생성 (PRD, Journey Map, Tech Spec, Wireframe)

### Done

- test(planning-interview): E2E 전체 흐름 검증 (Startup Mode, 4-Phase, 기존 문서 임포트 경로) (from previous Next)
  - Step 2.5 Context Import: "기존 문서 있음" 선택 → LinguaRAG Product Brief 임포트 → 정상 동작 ✅
  - shouldSkipQuestion: Phase 1 6개 질문 중 5개 자동 스킵 (pre-filled). GTM 1개만 질문 ✅
  - Phase 2 인터뷰: plain text 질문 정상 출력 (AskUserQuestion 미호출). 2개 질문 (Aha Moment, Retention) ✅
  - Phase 3 인터뷰: 6개 중 5개 스킵. 보안 관련 1개 질문 ✅
  - Phase 4 인터뷰: 단원 패널 구조 + 입력창 카운터 위치 2개 질문 ✅
- feat(lingua-rag): planning-interview로 4종 기획 문서 생성
  - `projects/lingua-rag/prd.md` — Product Brief (Startup)
  - `projects/lingua-rag/user-journey-map.md` — 3 Journey (온보딩, Q&A, 단원 전환)
  - `projects/lingua-rag/tech-spec.md` — 6 FR, 3-Phase 구현 계획, NFR, ASCII 아키텍처
  - `projects/lingua-rag/wireframe-spec.md` — 4 화면 ASCII 레이아웃 + 컴포넌트 명세

### Decisions

- **Phase 4 단원 패널**: 트리 구조 (교재 > Band > 단원 펼치기/접기) 채택 — 드롭다운 대비 단원 맥락 파악 용이
- **입력창 카운터**: 우하단 실시간 카운터 "48/500" 항상 표시 — 초과 시에만 표시보다 예측 가능성 높음

### Next

- [ ] planning-interview 실전 테스트 피드백 기반 SKILL.md 개선 검토
  - Phase 간 handoff 메시지 명확성
  - shouldSkipQuestion 스킵 시 사용자 알림 문구 자연스럽게 개선

---

## Session: 2026-02-25 15:19

> **Context**: AskUserQuestion 제약 전수 점검 및 수정 — freeform 질문 처리 방식 명확화, Step 5 옵션 수 초과 버그 수정

### Done

- fix(planning-interview): Step 5 Document Selection 옵션 수 초과 수정
  - "직접 선택" 제거하여 5개 → 4개 (AskUserQuestion max 4 제약 준수)
  - 커스텀 조합은 자동 제공되는 "Other" 입력으로 처리하도록 로직 변경
- fix(planning-interview): Interview Question Convention 섹션 추가
  - Steps 7–14 인터뷰 질문에 `allow_freeform=true` 표기는 pseudo-code임을 명시
  - 실제 AskUserQuestion 도구 호출 금지, plain text 출력으로 처리 규칙 추가
  - 두 가지 질문 유형(구조적 선택 vs 자유 응답) 테이블로 명확화

### Decisions

- **freeform 질문 처리 전략**: 60개+ 개별 질문 블록 수정 대신, 단일 Convention 섹션으로 전체 규칙을 선언하는 방식 선택 — 유지보수성 우선

### Next

- [x] 새 세션에서 `/planning-interview` 실행하여 Step 2.5 Context Import 동작 검증
- [x] 실제 인터뷰 E2E 테스트 (Solo Mode + "기존 아이디어 있음" 경로)
- [x] AskUserQuestion 인터뷰 질문이 plain text로 출력되는지 실행 중 확인
- [x] Phase 2-4 각 인터뷰 round 실행 검증 (현재 Phase 1만 테스트됨)
- [x] shouldSkipQuestion 로직이 실제 인터뷰 흐름에서 올바르게 동작하는지 확인

---

## Session: 2026-02-25 15:06

> **Context**: planning-interview v2.0 통합 기획 플러그인 구현 — 4-Phase 단일 흐름 + Context Import 단계 추가

### Done

- feat: planning-interview + spec-interview 통합 설계
  - 기존 두 플러그인을 단일 흐름으로 통합하는 아키텍처 확정
  - Mode(Solo/Startup/Team)는 인터뷰 깊이만 결정, 문서 선택은 별도 단계로 분리
- feat(planning-interview): SKILL.md v2.0 전면 재작성
  - Step 구조 전면 개편: 기존 단일 PRD 흐름 → 4-Phase 멀티 문서 흐름
  - Phase 1: PRD (Lean Canvas / Product Brief / Full PRD)
  - Phase 2: User Journey Map (신규)
  - Phase 3: Technical Specification (spec-interview에서 이식)
  - Phase 4: Wireframe Specification (신규)
  - Mode×Phase 질문 수 매트릭스: Solo(4/3/4/3), Startup(6/5/6/4), Team(9/7/9/6)
  - Session state v2.0 객체: phases_selected, phase_state[1-4], shared_context 추가
  - Phase Router: 선택된 Phase만 순서대로 실행, 나머지 skip
  - Cross-phase context: Phase 1 답변(personas, core_features)을 Phase 2-4에서 참조
- feat(planning-interview): 신규 템플릿 3개 생성
  - `templates/user-journey-map.md` (~30 placeholders): Journey Stage Table, Aha Moment, Friction Points, Error Journeys, Retention Loop
  - `templates/tech-spec.md` (~45 placeholders): Architecture Overview + ASCII diagram, Data Models (TS interfaces), FR/NFR, Edge Cases, Testing Strategy, Decisions Log
  - `templates/wireframe-spec.md` (~40 placeholders): Site Map, Navigation, Screen-by-Screen specs (Layout ASCII + Components Table + States), Interaction Patterns
- chore(planning-interview): 기존 템플릿 3개 v2.0 업데이트
  - lean-canvas.md, product-brief.md, full-prd.md에 버전 태그 및 Phase handoff 안내 추가
- chore(planning-interview): plugin.json v1.0.0 → v2.0.0 업데이트
  - keywords에 user-journey, tech-spec, wireframe, unified-planning 추가
- chore(spec-interview): SKILL.md description에 planning-interview v2.0 통합 안내 추가
- fix: link-local.sh 실행으로 symlink 재연결
  - ~/.claude/skills/planning-interview가 파일 복사본이어서 변경사항 미반영되던 문제 해결
  - scripts/link-local.sh 실행 후 심볼릭 링크로 교체
- feat(planning-interview): Step 2.5 Context Import 추가
  - 트리거에 내용 포함(~50단어+) 시 자동 감지 → 질문 없이 바로 추출
  - 트리거가 짧을 경우 "기존 아이디어나 문서가 있으신가요?" 선제 질문
  - 추출 항목: problem, solution, users, features, tech_stack
  - imported_context.pre_filled_answers → 각 Phase 인터뷰 질문 skip 로직 연동
  - 추출 후 파악된/미파악 항목 피드백 표시
  - 예상 질문 감소 효과: 6Q → 2-3Q (Solo/Startup), 9Q → 4-5Q (Team)
  - Error Handling: 붙여넣은 내용이 너무 짧거나 추출 결과가 없으면 처음부터 시작

### Decisions

- **문서 제거 판단** (오버 엔지니어링): SDD (Tech Spec의 Architecture 섹션으로 흡수), 독립 IA 파일 (Wireframe Spec의 IA 섹션으로 흡수), Design System Reference (기획 범위 외), 독립 Use Cases (Journey Map에 embed), 독립 MoSCoW (PRD 요구사항 섹션에 내장)
- **Mode 역할 분리**: Mode는 인터뷰 깊이(질문 수/라운드)만 결정. 어떤 문서를 생성할지는 Mode와 무관하게 Document Selection 단계에서 사용자가 직접 선택
- **Context Import UX**: 트리거에 내용이 이미 포함된 경우 질문 건너뜀. 짧은 트리거 시에만 선제 질문. 추출된 답변은 pre_filled_answers로 Phase 인터뷰에서 자동 skip

### Issues

- AskUserQuestion 최소 옵션 2개 필요 제약: freeform-only 질문(옵션 1개)을 사용하려다 `"Too small: expected array to have >=2 items"` 에러 발생. 모든 질문에 최소 2개 옵션 제공으로 해결 필요

### Next

- [ ] 새 세션에서 `/planning-interview` 실행하여 Step 2.5 Context Import 동작 검증
- [ ] 실제 인터뷰 E2E 테스트 (Solo Mode + "기존 아이디어 있음" 경로)
- [x] AskUserQuestion 호출 시 freeform=true 케이스에서 옵션 2개 최소 요건 준수 여부 전체 점검
- [ ] Phase 2-4 각 인터뷰 round 실행 검증 (현재 Phase 1만 테스트됨)
- [ ] shouldSkipQuestion 로직이 실제 인터뷰 흐름에서 올바르게 동작하는지 확인
