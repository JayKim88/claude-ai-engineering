# Competitive Agents - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/competitive-agents/skills/competitive-agents/SKILL.md`

## Session: 2026-02-27 17:56

> **Context**: launch-kit 플러그인 경쟁 생성 전체 파이프라인 실행 (2라운드) — planning-interview outputs를 mission context로 사용, Fuse A+B 선택 후 v1.1.0 배포

### Done

- feat(competitive-agents): launch-kit 플러그인 전체 파이프라인 실행 완료 (2라운드 × 2에이전트)
  - Phase 1: Alpha(Pragmatist) + Beta(Architect) v1 병렬 생성
  - Phase 2: Cross-review Round 1 — Alpha 81/100, Beta 88/100
  - Phase 3: Improve Round 1 — v1→v2 (Alpha 89/100, Beta 97/100)
  - Phase 4: Cross-review Round 2 — v2 평가 완료
  - Phase 5: Improve Round 2 — v2→v3
  - Phase 6: Judge evaluation (Opus) — Alpha 88.5/100 승, Beta 82.0/100
- feat(launch-kit): Fuse A+B 선택 → fused v1.1.0 생성
  - Alpha 구조(올바른 파일 형식, symlink-aware 템플릿 경로) + Beta 기능 통합
  - 통합된 Beta 기능: notes_partial 3단계 라우팅, 한국어 슬러그 처리, 이메일 preview text 규칙, CLAUDE.md 개발자 가이드, date bash 에러 핸들링
- chore(launch-kit): fused v1.1.0 → `plugins/launch-kit/` 복사 + `npm run link` 완료
  - skill + command 모두 링크 완료: `~/.claude/skills/launch-kit`, `~/.claude/commands/launch-kit`
- chore(competitive-agents): 대용량 임시 출력 파일(51~87KB) Python 파싱으로 v2/v3 파일 추출 처리

### Decisions

- **Beta v3 역전 원인**: v2 크리틱에서 97/100을 받은 Beta가 v3 improver에서 모든 파일을 ` ```markdown ``` ` 코드 펜스로 감싸 출력 → YAML frontmatter 파싱 불가 → Convention Compliance 15→7.5점 급락 → Alpha 역전 승리
- **Fuse 방식 선택**: Alpha의 올바른 파일 형식 + Beta의 기능적 우수성 결합이 최선. 점수차(6.5점)가 크지 않고 Beta 기능이 실제 UX 개선이므로 Fuse가 Use Winner보다 우월
- **notes_partial 3단계 라우팅**: 완전 추출(skip) / 부분 추출(targeted follow-up only) / 미추출(full question) — notes import UX 핵심 개선
- **한국어 제품명 슬러그**: `contains_non_ascii()` 감지 → Latin 슬러그 명시적 요청, 빈 슬러그 fallback까지 포함

### Issues

- **대용량 에이전트 출력 문제**: improver/fuser 출력이 51~87KB로 JSON 파일에 저장됨 → Python `re.split()` 파싱으로 해결. 정규식 패턴이 ` ```언어\n ... ``` ` 감싸기 여부에 따라 달라짐 — 매번 수동 대응 필요
- **Beta improver 코드 펜스 오류**: v3 improver가 모든 파일을 ` ```markdown ``` `로 감쌌음 — 프롬프트에 "파일 전체를 코드 펜스로 감싸지 말 것" 명시를 강화해야 할 수도 있음

### Next

- [ ] launch-kit v1.1.0 실제 사용 테스트
  - [ ] `/launch-kit` 트리거로 인터뷰 실행 — notes_partial 3단계 라우팅 검증
  - [ ] 한국어 제품명으로 슬러그 처리 흐름 확인
  - [ ] 이메일 preview text 생성 품질 확인
- [ ] competitive-agents: improver 프롬프트에 파일 형식 주의사항 보강 고려
  - "파일 내용을 ` ```언어 ``` ` 코드 펜스로 전체 감싸지 말 것. YAML frontmatter는 반드시 파일 첫 줄에"
- [ ] competitive-agents Step 11.5 동작 검증 (generate_docs = Yes 선택) — 이번 세션에서 No 선택으로 미테스트
  - [ ] decisions.md ADR 품질 확인 — judge report에서 올바르게 추출되는지 테스트

---

## Session: 2026-02-26 20:40

> **Context**: planning-interview outputs를 competitive-agents 입력으로 연결 + dev-log.md 제거 + frontmatter version 필드 제거

### Done

- feat(competitive-agents): Step 1에 "Use planning-interview outputs" 옵션 추가
  - 선택 시 디렉토리 경로를 입력받아 `prd.md`, `user-journey-map.md`, `tech-spec.md`, `wireframe-spec.md` 읽음
  - 4개 파일 내용을 mission context로 합산, `planning_docs_path` + `planning_docs` 변수로 저장
- feat(competitive-agents): Step 11.5에 planning-interview docs 복사 로직 추가
  - `planning_docs_path` 설정 시 `final/docs/`에 파일명 그대로 복사 (prd.md, user-journey-map.md, tech-spec.md, wireframe-spec.md)
- chore(competitive-agents): Step 11.5에서 `dev-log.md` 생성 제거
  - 빈 템플릿이라 실질적 가치 낮음 → 사용자 판단으로 제거
- fix(competitive-agents): SKILL.md frontmatter에서 `version` 필드 제거
  - skill 파일에서 지원되지 않는 속성 (IDE 경고 해소)
- docs(competitive-agents): Step 12 완료 요약 및 Quick Reference 출력 트리에 planning-interview docs 항목 반영

### Decisions

- **planning-interview → competitive-agents 연결**: planning-interview가 prd/user-journey/tech-spec/wireframe 4개를 생성하므로, 이를 그대로 mission context로 활용하는 것이 자연스러운 워크플로우
- **dev-log.md 제거**: 빈 템플릿은 생성 가치가 낮고, 사용자가 직접 만드는 편이 나음. decisions.md (ADR)만으로 프로젝트 히스토리 충분
- **version 필드 제거**: Claude Code skill 파일에서 지원되지 않는 속성임을 확인 → 완전 제거

### Next

- [ ] competitive-agents 실행 후 Step 11.5 동작 검증 (generate_docs = Yes 선택)
  - [ ] decisions.md ADR 품질 확인 — judge report에서 올바르게 추출되는지 테스트
  - [ ] spec 파일 제공 시 spec.md 복사 동작 확인
- [x] planning-interview → competitive-agents 전체 플로우 테스트 (from previous Next)
  - planning-interview outputs(prd.md + user-journey-map.md)를 mission context로 입력 → 파이프라인 정상 실행 확인

---

## Session: 2026-02-25 17:16

> **Context**: competitive-agents SKILL.md에 Step 11.5 추가 — 파이프라인 최종 결과물에 프로젝트 문서(ADR, dev-log, spec) 자동 생성 기능 포함

### Done

- feat: Step 1에 "Project Docs" 질문 추가 (rounds 수 질문과 함께 한 번에 제시)
  - "Yes — generate docs/ (Recommended)": `final/docs/`에 decisions.md, dev-log.md, spec.md 생성
  - "No — skip docs": 빠른 실험이나 플러그인만 필요한 경우 스킵
  - `generate_docs = True/False` 플래그로 이후 Step 11.5 진입 여부 결정
- feat: Step 11.5 신규 추가 (Step 11 `Execute Decision`과 Step 12 `Completion Summary` 사이)
  - `final/docs/decisions.md`: judge-report의 "Strengths to Preserve" + per-criterion 점수 + mission에서 ADR 3~6개 자동 추출
  - `final/docs/dev-log.md`: 개발 일지 빈 템플릿 (Session/작업내용/코드스니펫/에러/발견사항 구조)
  - `final/docs/spec.md`: spec 파일 제공 시에만 복사 (spec_path 제공 여부로 판단)
  - 서브에이전트 없이 Claude가 인라인으로 생성 (mission, judge-report가 이미 컨텍스트에 존재)
- docs: Step 12 완료 요약 업데이트 — `Files: {N} files (+ {M} docs files if generate_docs = True)` 및 docs 경로 표시
- docs: Quick Reference 출력 트리 업데이트 — `final/docs/` 서브디렉토리 구조 반영

### Decisions

- **인라인 생성 방식 채택 (서브에이전트 미사용)**: judge-report와 mission이 이미 메모리에 있으므로 별도 에이전트 없이 직접 생성. 더 빠르고 컨텍스트 손실 없음
- **ADR 소스 = judge-report**: "Strengths to Preserve", "Why Winner", per-criterion 분석이 자연스럽게 아키텍처 결정 사항을 담고 있음 → 추가 분석 불필요
- **opt-in 방식**: 기본 권장(Recommended)이지만 선택 가능 → 빠른 실험 케이스에서 불필요한 문서 생성 방지
- **트리거**: LinguaRAG F1 fused 결과물에 decisions.md가 없어 repo 이전 시 수동 작성 필요했던 경험 → 자동화 필요성 확인

### Next

- [ ] competitive-agents 실행 후 Step 11.5 동작 검증 (generate_docs = Yes 선택)
  - [ ] decisions.md ADR 품질 확인 — judge report에서 올바르게 추출되는지 테스트
  - [ ] dev-log.md 템플릿 형식 확인
  - [ ] spec 파일 제공 시 spec.md 복사 동작 확인
- [ ] decisions.md ADR 포맷 표준화 (한글 기준 날짜, 상태, 결정, 이유, 트레이드오프)
- [x] SKILL.md 버전 업데이트 (`version: 1.0.0` → `version: 1.1.0`) — version 필드 자체가 지원되지 않아 제거로 대응
