# Business Avengers v2.1 — Process Flow Audit TODO

**Date**: 2026-02-22
**Audit Method**: 3x Opus Explore agents (parallel) + External UX/Content review
**Findings**: 37 items (CRITICAL 4 / HIGH 7 / IMPORTANT 13 / MEDIUM 4 / MINOR 9)

---

## History

### v1.0 (Initial)
- 23 agents, 8 KB, 35 templates, Phase 0-9 pipeline
- 8 core files (SKILL.md, org-structure.yaml, etc.)

### v2.0 (MAKE Extension)
- Indie Maker Handbook (levelsio) methodology integrated
- Phase 10-12 added (Growth, Automation, Scale & Exit)
- 3 KB files added (growth-tactics, automation-guide, exit-guide)
- 15 new templates, 16 files modified

### v2.0.1 (MAKE Audit Fix)
- MAKE content architectural placement corrected (Agent identity vs KB reference)
- 4 bugs fixed (ceo_goal, sprint_context, legal-templates, make mode name)
- Agent role boundaries clarified (marketing-strategist, devops, revenue-strategist)
- Phase 11 agents reassigned (CS Manager + Data Analyst -> Business Analyst)
- Template content placement improved (gtm, cs-playbook, pricing-strategy)
- Step numbering unified (11.5-11.9 -> 12-16)
- 10 files modified

### v2.1 (Process Flow Audit) -- COMPLETED (2026-02-25)
- Full process flow audit completed, all 37 items resolved
- CRITICAL (4): All fixed — C1 gate branching, C2 KB refs, C3 Glob guards, C4 variable names
- HIGH (5): All fixed — H1-H3 sprint modes, H4-H5 variable definitions
- IMPORTANT (13): All fixed — I1-I11+I13 functional improvements
- MINOR (9): All fixed — M1-M9 org-structure.yaml sync + SKILL.md minor
- UX (6): All fixed — UX1-UX5+UX8 user experience improvements

---

## TODO: CRITICAL -- Runtime Crashes (4 items)

### C1. Approval Gate Dead Ends
- [ ] **All 12 AskUserQuestion gates in SKILL.md**
- "수정 요청", "피봇", "중단" 선택 시 분기 없이 `update-phase ... completed` 실행
- 사용자 피드백이 완전히 무시됨
- **Fix**: 각 게이트에 조건 분기 추가
  - "승인/확인" -> completed, proceed
  - "수정 요청" -> collect feedback, re-run agent, loop back to gate
  - "피봇" -> update-phase revision, go to Phase 0
  - "중단" -> update-phase cancelled, exit pipeline
- **Affected lines**: Step 5(~369), Step 6(~479), Step 7(~584), Step 8(~661), Step 9(~815), Step 10(~889), Step 11(~1077), Step 12(~1201), Step 13(~1352), Step 14(~1497), Step 15(~1614), Step 16(~1768)
- **Decision needed**: Full 12 gates / approve-type only (6) / common function pattern

### C2. KB File Reference Error: `growth-hacking.md` Does Not Exist
- [ ] **SKILL.md line ~1010** (Phase 7 growth-hacker): `growth-hacking.md` -> `growth-tactics.md`
- [ ] **SKILL.md line ~1320** (Phase 9 data-analyst): `growth-hacking.md` -> `data-metrics-guide.md`
- Actual KB file: `knowledge/growth-tactics.md` (used correctly in Phase 10-11)
- Also resolves I9 (data-metrics-guide.md orphan)

### C3. Unguarded Read() Crashes `make` and `mvp-build` Presets
- [ ] **14 direct Read() calls** need Glob+conditional pattern
- Pattern: `Read("{PROJECT_DIR}/phase-X/file.md")` -> `files = Glob(...); val = Read(files[0]) if files else ""`
- Affected locations:

  | Line | File Read | Phase | Crashes in preset |
  |------|-----------|-------|-------------------|
  | ~496 | phase-2/prd.md | 3 | - |
  | ~497 | phase-2/user-personas.md | 3 | - |
  | ~602 | phase-2/prd.md | 4 | - |
  | ~679 | phase-4/tech-architecture.md | 5 | - |
  | ~831 | phase-2/prd.md | 6 | - |
  | ~907 | phase-2/prd.md | 7 | make, mvp-build |
  | ~908 | phase-2/user-personas.md | 7 | make, mvp-build |
  | ~909 | phase-1/market-analysis.md | 7 | mvp-build |
  | ~910 | phase-1/competitive-analysis.md | 7 | mvp-build |
  | ~1096 | phase-2/prd.md | 8 | make |
  | ~1097 | phase-1/market-analysis.md | 8 | - |
  | ~1218 | phase-2/prd.md | 9 | post-launch |
  | ~1222 | phase-4/tech-architecture.md | 9 | post-launch |
  | ~1376 | phase-2/prd.md | 10 | make, post-launch |

### C4. `sprint` vs `is_sprint` Variable Name Mismatch
- [ ] **SKILL.md lines 285, 312, 341** (Phase 1 agent prompts)
- Uses `{sprint_context if sprint else ""}` but variable is `is_sprint`
- **Fix**: Change to `{sprint_context}` (already "" when not sprint, no conditional needed)
- Aligns with all other phases' pattern

---

## TODO: HIGH -- Data Loss / Functional Defects (5 items)

### H1. Phase 0 (Ideation) -- No Sprint Mode
- [ ] **SKILL.md Step 4 (lines 171-233)**
- No `is_sprint` check, no backup, no existing doc reading, no sprint_context
- Sprint with Phase 0 overwrites idea-canvas from scratch
- **Fix**: Add sprint block before Q&A (backup idea-canvas.md, read existing, pass to PM agent)

### H2. Phase 12 (Scale & Exit) -- No Sprint Mode
- [ ] **SKILL.md Step 16 (lines 1622-1772)**
- No sprint_context initialization, no backup, no existing doc read
- 5 documents overwritten without version history
- **Fix**: Add sprint block following other phases' pattern

### H3. Phase 1 Sprint -- Incomplete Backup and Context
- [ ] **SKILL.md lines 254-259**
- Only backs up `market-analysis.md` (1 of 3 files)
- `existing_competitive` and `existing_revenue` variables defined but never used in sprint_context
- **Fix**: Backup all 3 files, include each in agent-specific sprint_context

### H4. `current_version` Variable Never Defined
- [ ] **SKILL.md -- 12 backup calls**
- Used in: `Bash("... backup ... {current_version}")` everywhere
- Never assigned a value
- **Fix**: Define in Step 2 (`current_version = "v1.0"`) and Step 3 (`current_version = project.current_version`)

### H5. `project_slug` Undefined for RESUME/SPRINT/SINGLE Modes
- [ ] **SKILL.md Step 1 (lines 75-80), Step 3 (line 129)**
- These modes route to Step 3, skipping Step 2 where slug is created
- **Fix**: Extract slug from command args in Step 1, or prompt in Step 3

---

## TODO: IMPORTANT -- Functional Improvements (13 items)

### I1. Phase 0/1 Agents Missing Agent Definition Reference
- [ ] **SKILL.md Step 4 (lines 199-216), Step 5 (lines 262-343)**
- Phase 2+ agents all have `에이전트 정의 (Read로 읽으세요): {AGENTS_DIR}/xxx.md`
- Phase 0 (PM) and Phase 1 (BA, MS, RS) prompts lack this
- **Fix**: Add agent definition reference to 4 agent prompts

### I2. Phase 9 Missing Phase 7 Input Read
- [ ] **SKILL.md Step 13 (lines 1217-1222)**
- org-structure: `inputs_from: [2, 4, 7, 8]` -- Phase 7 outputs never read
- CS/Legal/DA miss launch strategy context for operations planning
- **Fix**: Add `gtm_files = Glob(...); gtm = Read(...)` for Phase 7 gtm-strategy.md

### I3. Phase 5 Sprint -- Existing Docs Read but Not Passed to Agents
- [ ] **SKILL.md lines 693-695**
- `existing_frontend`, `existing_backend` defined but not in sprint_context
- **Fix**: Include existing content in sprint_context

### I4. Sprint Backup Only Covers Primary File Per Phase
- [ ] **SKILL.md -- all sprint backup sections**
- Each phase backs up 1 file, but agents may overwrite 2-5 files
- **Fix**: Backup all files in phase directory, or backup per-output-file

### I5. Phase 11 sprint_context Missing sprint_goal
- [ ] **SKILL.md line ~1529**
- Unlike other phases, sprint_context doesn't include `{sprint_goal}`
- **Fix**: Add sprint_goal to sprint_context string

### I6. `faq-template.md` Missing from org-structure.yaml
- [ ] **org-structure.yaml line 175**
- CS Manager produces this in Phase 9 but it's not in outputs list
- **Fix**: Add `faq-template.md` to Phase 9 outputs

### I7. `sprint-review.md` Template Orphaned
- [ ] **templates/sprint-review.md**
- Never referenced in SKILL.md
- **Fix**: Integrate into Step 20 (Sprint Completion) or remove

### I8. RESUME Mode `workflow` Variable Undefined
- [ ] **SKILL.md lines 164-166**
- `phases_to_run = [p for p in workflow if ...]` -- `workflow` never defined
- **Fix**: Load from project.yaml saved workflow_mode

### I9. `data-metrics-guide.md` KB Orphaned
- [ ] Resolved by C2 fix (Phase 9 data-analyst gets this KB)

### I10. No Explicit Phase Execution Loop
- [ ] **SKILL.md after Step 2/3**
- No explicit "for phase in phases_to_run: execute Step(4+phase)" construct
- Relies on LLM to iterate through conditional steps
- **Fix**: Add explicit loop/iteration instruction

### I11. No Transition to Completion Steps
- [ ] **SKILL.md after Step 16**
- No "if is_sprint: go to Step 20" or "if orchestra: go to Step 21"
- **Fix**: Add completion routing after last phase step

### I12. Inconsistent Glob vs Direct Read (overlaps with C3)
- [ ] Resolved by C3 fix (all reads become Glob+conditional)

### I13. ui-designer Reporting Chain Mismatch
- [ ] **agents/ui-designer.md** -- "Reports to: Design Lead"
- **org-structure.yaml** -- listed under CPO manages
- **Fix**: Update agent file to "Reports to: CPO (via Design Lead)"

---

## TODO: MINOR (9 items)

### M1-M5. org-structure.yaml `inputs_from` Desync
- [ ] Phase 5: actual reads Phase 2,3 -- yaml says [4]
- [ ] Phase 7: actual reads Phase 0 -- yaml says [1,2]
- [ ] Phase 8: actual reads Phase 0 -- yaml says [1,2]
- [ ] Phase 10: actual reads Phase 2 -- yaml says [7,8,9]
- [ ] Phase 0: yaml says inputs_from [1] but never reads Phase 1 (market-first)
- **Fix**: Update yaml inputs_from to match actual implementation

### M6. Phase 0 ux-researcher Listed but Unused
- [ ] org-structure lists [product-manager, ux-researcher] for Phase 0
- SKILL.md only invokes product-manager
- **Fix**: Remove from yaml or add UX researcher Task in Phase 0

### M7. Market-first Mode: Phase 0 Ignores Phase 1 Results
- [ ] Phase 0 declared `inputs_from: [1]` but never reads Phase 1 files
- **Fix**: In market-first, read Phase 1 outputs and provide as context to CPO dialogue

### M8. SINGLE PHASE Mode No Validation
- [ ] No check that requested_phase_number is 0-12
- **Fix**: Add bounds check

### M9. Phase 6 (QA) Terminal Node
- [ ] QA outputs (test-plan.md, qa-checklist.md) not consumed by any later phase
- This is intentional (for human developers) but undocumented
- **Fix**: Add comment in org-structure.yaml

---

## TODO: UX & Content Review (6 new items, from external review)

### UX1. `make` Preset Content Quality — Missing PRD Context (HIGH)
- [ ] **`make` preset `[0, 1, 7, 8, 10, 11]`**: Phase 2 미실행 → Phase 7/8/10 에이전트가 PRD 없이 작업
- Phase 7: PRD + user-personas 빈 값 (market-analysis는 존재)
- Phase 8: PRD 빈 값 (market-analysis 존재)
- Phase 10: PRD 빈 값, Phase 9 metrics 빈 값
- Phase 11: Phase 9 cs-playbook, Phase 5 deployment 빈 값
- C3 Glob guard로 크래시 방지되지만, 에이전트 출력 품질 저하
- **Fix**: C3 수정 시 fallback 로직 통합 — PRD 미존재 시 idea-canvas를 대용으로 사용
  ```python
  prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
  if prd_files:
    prd = Read(prd_files[0])
  else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""
  ```
- **Relates to**: C3 (Glob guard) — 동시 진행 권장

### UX2. `post-launch` Preset — No Onboarding for Existing Services (HIGH)
- [ ] **`post-launch` preset `[10, 11, 12]`**: 기존 서비스용인데 Phase 0-9 산출물 없음
- Phase 10이 phase-2 PRD를 읽지만 존재하지 않음
- Phase 11이 phase-5 deployment, phase-9 cs-playbook을 읽지만 존재하지 않음
- **Fix**: `post-launch` 모드 진입 시 온보딩 스텝 추가
  - 서비스 URL, 주요 기능, 현재 가격, 현재 사용자 수를 Q&A로 수집
  - 간이 컨텍스트 문서 생성 (idea-canvas + prd 대용)
  - SKILL.md Step 2 또는 별도 Step에서 처리

### UX3. "MAKE 모드" Naming Unclear (MEDIUM)
- [ ] **SKILL.md line ~106**: "MAKE 모드 - 인디메이커 린 경로"
- "MAKE"는 책 제목이지 보편적 개념이 아님 — 책을 모르는 사용자에게 의미 불명
- **Fix**: "인디 메이커 모드 - 최소 단계로 빠르게 (아이디어→시장→런칭→수익화→성장→자동화)"
- "MAKE"는 부제/출처 표기로 이동

### UX4. Phase Number Jump in `make` Mode (MINOR → M 카테고리로 통합 가능)
- [ ] make 모드 실행 시 Phase 0 → 1 → 7 → 8 → 10 → 11 진행
- 사용자가 Phase 2-6 건너뛴 이유를 모름 ("에러인가?")
- **Fix**: 모드 시작 시 안내 메시지 추가
  - "이 모드는 린 경로로 Phase 2-6, 9를 건너뛰고 진행합니다"

### UX5. Sprint Options Incomplete + Terminology Inconsistent (MEDIUM)
- [ ] **SKILL.md lines 151-158**: Sprint 옵션 7개만 존재
- **누락된 Phase**: 0 (Ideation), 1 (Market Research), 5 (Dev), 6 (QA), 8 (Monetization), 9 (Operations)
- **용어 혼재**: "수정" (Phase 2,3,4,7) / "업데이트" (Phase 10,11) / "분석" (Phase 12)
- **Fix**:
  - 13개 Phase 전체를 옵션에 포함
  - 용어 통일: 전부 "업데이트"로
  - 카테고리 그루핑: 기획(0-2) / 개발(3-6) / 런칭(7-9) / 성장(10-12)

### UX8. Phase 12 Exit Timing Guidance Missing (MEDIUM)
- [ ] **SKILL.md lines 1647-1655**: CEO dialogue에서 장기 목표만 묻고, 현재 사업 상태(타이밍)를 묻지 않음
- MAKE 책 핵심: "Sell at the peak, not when you're desperate"
- **Fix**: CEO dialogue에 사업 상태 질문 추가
  ```python
  AskUserQuestion(
    "[CFO] 현재 사업 상태는 어떤가요?",
    options=[
      "성장 중 - 매출/사용자가 계속 늘고 있다",
      "정체 - 성장이 멈추거나 둔화되었다",
      "번아웃 - 사업은 괜찮지만 내가 지쳤다",
      "하락 - 매출/사용자가 줄고 있다"
    ]
  )
  ```

---

### Existing TODO Extensions (from UX review)

- **I5 보강**: Phase 11 sprint_context에만 "변경사항만 반영하고, 기존 분석은 유지하세요" 지시 있음 — 다른 Phase와 패턴 불일치. 통일 필요.
- **M1-M5 확장**: Phase 10 `inputs_from: [7,8,9]`이지만 실제 Phase 2 PRD도 읽음 — 신규 Phase도 동기화 필요.

---

## Confirmed Safe (No Action Needed)

- **Parallel execution**: All parallel phases write to independent files. No conflicts.
- **Template mapping**: All 49 referenced templates exist.
- **Agent-Phase mapping**: Phases 1-12 all match between org-structure.yaml and SKILL.md.
- **Phase 3 sequential**: design-lead -> ui-designer correctly implemented as non-parallel.
- **Phase 6 QA terminal**: Intentional design -- QA docs for human use.
- **Global tool permissions**: Sufficient for all agent needs.

---

## Recommended Execution Order

1. **C2 + C4** (quick fixes, <5 min) -- KB reference + variable name
2. **C3 + UX1** (systematic, ~40 min) -- 14 Read() → Glob pattern + idea-canvas fallback for lean presets
3. **H4 + H5** (variable definitions, ~10 min)
4. **H1 + H2 + H3** (sprint mode additions, ~30 min)
5. **C1** (approval gates, ~60 min) -- largest change, design decision needed
6. **UX2** (post-launch onboarding, ~20 min) -- new Step for existing service import
7. **UX5** (sprint options, ~15 min) -- all 13 phases + terminology unification
8. **I1-I13** (improvements, ~45 min)
9. **UX3 + UX8** (naming + Phase 12 timing, ~10 min)
10. **M1-M9 + UX4** (minor cleanup, ~25 min)

**Estimated total**: ~4.5 hours of implementation
**Files modified**: SKILL.md (primary), org-structure.yaml, agents/ui-designer.md
