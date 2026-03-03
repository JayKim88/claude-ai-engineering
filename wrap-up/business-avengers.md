# Business Avengers - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/business-avengers/`

## Session: 2026-03-03 23:44

> **Context**: Per-phase fine-tuning kick-off — Phase 0 ideation Q&A redesign + JTBD/Why Now additions, Phase 2 PM knowledge doc creation

### Done
- feat(SKILL.md Step 4): Phase 0 Q&A redesigned from 5 transactional questions → 7 exploratory questions
  - Added story-based problem discovery ("walk me through the last time you faced this")
  - Added Why Now question ("what changed recently that makes this the right moment?")
  - Added Switching Trigger question ("what would push someone from their current solution?")
  - Added closing open question for anything missed
  - CPO now introduces the conversation with "discovery mode" framing
- feat(agents/product-manager.md): Added Phase 0 expert frameworks section
  - Mom Test application rules (past-tense behavioral framing, false positive filters)
  - JTBD writing standard with 3 job types (Functional / Emotional / Social)
  - Why Now evaluation (Technology / Behavioral / Regulatory / Cost shift taxonomy)
  - Competitive Moat Test (structural vs. copyable differentiation)
  - Own Problem Validation guidance
- feat(templates/idea-canvas.md): Added JTBD section and Why Now section
  - JTBD: Core statement format + 3 job type fields + Switching Trigger field
  - Why Now: Timing Trigger + Enablement + Opportunity Window fields
- feat(quality/phase-rubrics.md): Expanded Phase 0 mandatory checklist and rubric
  - Checklist: JTBD format check + Why Now presence check added
  - Rubric: expanded from 4 → 6 criteria (added JTBD quality + Why Now)
- feat(SKILL.md Step 4 PM task): Strengthened PM task instructions
  - JTBD 3-type fill requirement (Functional/Emotional/Social + Switching Trigger)
  - Why Now explicit requirement (or flag as timing risk)
  - Differentiation 6-month moat test
  - "Every placeholder must be filled" rule added
- feat(knowledge/extended/prd-methods-advanced.md): New knowledge doc created
  - Inspired (Marty Cagan): 4 product risks, Opportunity Assessment 10 questions
  - Shape Up (Ryan Singer): Appetite sizing, Pitch format, Shaping, Hill Charts
  - User Story Mapping (Jeff Patton): Backbone, Walking Skeleton, Release slices
  - Continuous Discovery (Teresa Torres): Opportunity Solution Tree, Assumption Testing
  - PRD quality standards: outcome metrics, "Will NOT Build" format, RICE Confidence Gate
  - JTBD-based persona format (behavior > demographics)
- feat(SKILL.md Step 6 PM task): Phase 2 PM task strengthened (from previous Next)
  - Added prd-methods-advanced.md to knowledge base references
  - Added phase-rubrics.md reference
  - Expanded from 6 → 18 detailed steps covering Shape Up, 4 product risks, Story Map, RICE gate

### Decisions
- Phase 0 Q&A: transactional 5-question form → conversational 7-question exploration (Mom Test principle)
- Agent architecture: agent def = role + framework overview (thin) / knowledge doc = deep content with examples (Option B preferred)
- prd-methods-advanced.md: integrated Shape Up + Inspired + Story Mapping into single reference doc vs. separate files

### Next
- [ ] Test Phase 0 with updated Q&A: verify JTBD/Why Now sections are properly filled in idea-canvas output
- [ ] Phase 1 (Market Research) fine-tuning — business-analyst, marketing-strategist, revenue-strategist agents
- [ ] Phase 5 (Dev Guide) SKILL.md Step 9 strengthening — frontend-dev + backend-dev + devops-engineer
- [ ] Phase 6 (QA) SKILL.md Step 10 strengthening — qa-lead task, Test Pyramid + Core Web Vitals
- [ ] Phase 9 (Operations) SKILL.md Step 13 strengthening — cs-manager + data-analyst tasks
- [ ] Remaining agent Quality Standards — ui-designer, ux-researcher, coo, cto, cmo, cpo, frontend-dev, backend-dev, qa-lead, cs-manager

---

## Session: 2026-03-02 23:54

> **Context**: Sprint 2–4 완료 — 8개 extended KB 파일 생성 + 9개 에이전트 Quality Standards 추가 + SKILL.md 8개 Step 강화

### Done
- feat(knowledge/extended): Sprint 2 — Phase 0 + Phase 8 에이전트 강화
  - `agents/product-manager.md` — Shape Up Appetite 기준, Feature justification, "Will NOT Build" 필수, RICE Confidence 게이트, Self-Assessment 블록 추가
  - `agents/cfo.md` — Unit Economics 기준표(LTV:CAC >3:1, GM ≥70%), 3-Scenario 필수, Goldilocks 3-tier, Burn Multiple Red Flag 추가
  - `SKILL.md` Step 4 (Phase 0) — `problem-validation-deep.md` + `phase-rubrics.md` 참조 추가, 4→11 Steps 확장 (Mom Test / JTBD / Assumption Register / Why Now)
  - `SKILL.md` Step 12 (Phase 8) — `saas-metrics-bible.md` + `phase-rubrics.md` 참조 추가, Goldilocks/annual pricing steps 추가
- feat(knowledge/extended): Sprint 3 — Phase 7 + Phase 10 에이전트 강화
  - `knowledge/extended/gtm-advanced.md` 신규 생성 — Geoffrey Moore Chasm 전략, First 1,000 Users Playbook, Product Hunt/Indie Hacker 런치 플레이북, D-30→D+7 타임라인
  - `knowledge/extended/growth-engineering.md` 신규 생성 — Sean Ellis PMF 40% 테스트, NSM 선정 기준, Andrew Chen 4 Growth Loop, ICE/RICE/BRASS 우선순위, Activation Engineering
  - `agents/marketing-strategist.md` — ICP 구체성 게이트, First 100 Users 경로, 채널 집중 기준, Pre-launch warm-up 필수 추가
  - `agents/growth-hacker.md` — PMF signal 선행, NSM Non-Negotiable, Growth Loop 정의, Aha Moment, ICE ≥6 실험 의무화 추가
  - `SKILL.md` Step 11 (Phase 7) — `gtm-advanced.md` 참조, 7→12 Steps 확장 (ICP/First100/Pre-launch/Repeated Launch)
  - `SKILL.md` Step 14 (Phase 10) — `growth-engineering.md` 참조, PMF/NSM/Loop/ICE steps 추가
- feat(knowledge/extended): Sprint 4 — Phase 3 + Phase 4 + Phase 11 + Phase 12 에이전트 강화
  - `knowledge/extended/design-advanced.md` 신규 생성 — Nielsen 10 Heuristics, Conversion Design, Empty/Error/Loading States, Friction Audit, Mobile-first 기준
  - `knowledge/extended/tech-architecture-advanced.md` 신규 생성 — Boring Technology 40h 룰, MVA monolith 진화 경로, AWS Well-Architected 5 Pillars, OWASP Top 10, ADR 형식
  - `knowledge/extended/automation-scale.md` 신규 생성 — Automation ROI 공식, Bus Test 10문항, 3-Tier Stack, 3-Tier Monitoring, Autonomous Org 구조
  - `knowledge/extended/exit-strategy.md` 신규 생성 — Acquire.com 멀티플 테이블, 멀티플 드라이버/킬러, FIRE 계산 공식, DD 체크리스트, Scale vs. Sell 프레임워크
  - `agents/design-lead.md` — Design System 9-element gate, Nielsen 필수 5개, CTA hierarchy 1개 primary 룰 추가
  - `agents/tech-lead.md` — Boring Tech 40h 기준, ADR 5개 필수, OWASP Top 10 의무, 10× sizing 룰, No-code assessment 필수 추가
  - `agents/devops-engineer.md` — Automation ROI gate (payback <8주), Bus Test 필수(≥8/10), 3-Tier Monitoring 의무, Failure path 필수 추가
  - `agents/revenue-strategist.md` — Acquire.com 벤치마크 필수, Scale vs. Sell 명시적 결정, Multiple 개선 로드맵, FIRE 계산 추가
  - `SKILL.md` Step 7 (Phase 3) — `design-advanced.md` 참조, design-lead/ui-designer 양쪽 6→9 Steps 확장
  - `SKILL.md` Step 8 (Phase 4) — `tech-architecture-advanced.md` 참조, 7→12 Steps 확장 (ADR/OWASP/No-code assessment)
  - `SKILL.md` Step 15 (Phase 11) — `automation-scale.md` 참조, ROI/Bus Test/3-Tier steps 추가
  - `SKILL.md` Step 16 (Phase 12) — `exit-strategy.md` 참조, 6→11 Steps 확장 (benchmarked valuation/FIRE/Scale vs. Sell)

### Decisions
- KB 언어: 모든 extended KB 파일 영어로 작성 (토큰 1.5–2× 절감, 에이전트 지시사항과 동일 언어)
- Self-Assessment 블록 표준화: 모든 에이전트에 동일한 형식의 Quality Check 블록 삽입 (Depth/Evidence/Specificity 3차원 + 미충족 기준 명시)
- Quality Standards 위치: `## Expert Frameworks`와 `## Communication` 사이에 삽입 (기존 구조 최소 침범)
- 아직 강화하지 않은 Step(2, 6, 9, 10, 13)은 다음 Sprint에서 처리

### Next
- [ ] E2E 테스트: 실제 아이디어 1개로 전체 파이프라인 실행 후 품질 비교 (고도화 전/후 Phase별 Self-Assessment 점수 확인)
- [x] Phase 2 (PRD) `SKILL.md` Step 6 강화 — `product-manager.md` Extended KB 참조 + quality check 지시 추가 (from previous Next)
- [ ] Phase 5 (Dev Guide) `SKILL.md` Step 9 강화 — frontend-dev + backend-dev + devops-engineer tasks
- [ ] Phase 6 (QA) `SKILL.md` Step 10 강화 — qa-lead task, Test Pyramid + Core Web Vitals 기준 추가
- [ ] Phase 9 (Operations) `SKILL.md` Step 13 강화 — cs-manager + data-analyst tasks, North Star Metric + AARRR 기준 추가
- [ ] 나머지 에이전트 Quality Standards 추가 — ui-designer, ux-researcher, coo, cto, cmo, cpo, frontend-dev, backend-dev, qa-lead, cs-manager 등

---

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
