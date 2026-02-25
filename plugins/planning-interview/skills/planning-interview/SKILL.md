---
name: planning-interview
description: Conducts adaptive product planning interviews to generate comprehensive service documentation in a unified flow. Covers PRD (Lean Canvas / Product Brief / Full PRD), User Journey Map, Technical Specification, and Wireframe Specification. Mode determines interview depth; user selects which documents to generate. Use when user says "planning interview", "PRD", "기획해줘", "전체 기획", "서비스 기획", "기획부터 스펙까지".
version: 2.0.0
author: Fused Implementation (Alpha + Beta)
model: claude-opus-4-6
fallback_model: claude-sonnet-4-6
---

# Planning Interview Skill v2.0

## Purpose

Transform product ideas into complete service documentation through a unified, multi-phase interview flow.
Mode (Solo / Startup / Team) controls interview depth per phase.
User selects which documents to generate — any combination of 4 document types.

**Available documents:**
1. **PRD** — Lean Canvas / Product Brief / Full PRD (always Phase 1)
2. **User Journey Map** — Core user flows, friction points, retention loop
3. **Technical Specification** — Architecture, data models, NFR, testing strategy
4. **Wireframe Specification** — Information architecture, screen specs, interaction patterns

## Model Selection

- **Recommended**: `claude-opus-4-6` — Nuanced follow-up questions, strategic insight synthesis
- **Acceptable**: `claude-sonnet-4-6` — Faster interviews, suitable for simple features

---

## Algorithm

### Step 1: Trigger Detection

Detect trigger phrases to initiate the planning interview:

**English triggers:**
- "planning interview", "PRD", "product requirements", "product planning"
- "help me plan [product/feature]", "create a PRD for [X]"
- "full planning", "service planning", "spec this out"

**Korean triggers:**
- "기획해줘", "기획 도와줘", "제품 기획 도와줘"
- "PRD 만들어줘", "전체 기획", "서비스 기획", "기획부터 스펙까지"

**Quick Mode triggers** (auto-select mode, skip context detection):
- "PRD for B2B SaaS" → Startup mode
- "Lean Canvas for mobile app" → Solo mode
- "Full PRD for enterprise" → Team mode

Upon detection, proceed to Step 2.

---

### Step 2: Initialize Session

Create session state object (v2.0):

```
session = {
  // Core identity
  mode: null,              // "Solo" | "Startup" | "Team"
  language: null,          // "en" | "ko" (detected from trigger)
  quick_mode: false,
  project_name: null,      // Derived from user input during Phase 1
  project_slug: null,      // kebab-case version (e.g., "taskflow-cli")
  start_time: null,        // Run `date '+%Y-%m-%d %H:%M'` — never estimate

  // Phase management
  current_phase: null,
  phases_selected: [],     // User-selected: any subset of [1, 2, 3, 4]
  phases_completed: [],    // [1, 2, ...] filled as phases finish

  // Phase-specific state (all 4 initialized, only selected ones used)
  phase_state: {
    1: { status: "pending", current_round: 0, max_rounds: null,
         answers: {}, completeness_scores: {}, output_file: null, template_type: null },
    2: { status: "pending", current_round: 0, max_rounds: null,
         answers: {}, completeness_scores: {}, output_file: null },
    3: { status: "pending", current_round: 0, max_rounds: null,
         answers: {}, completeness_scores: {}, output_file: null },
    4: { status: "pending", current_round: 0, max_rounds: null,
         answers: {}, completeness_scores: {}, output_file: null }
  },

  // Cross-phase context (populated after Phase 1, referenced in Phase 2-4)
  shared_context: {
    personas: null,         // Key personas from Phase 1 user/market answers
    core_features: null,    // Must-Have features from Phase 1 constraints
    project_goals: null,    // Success metrics from Phase 1
    problem_statement: null // Core problem from Phase 1
  },

  // Imported context (populated in Step 2.5 if user provides existing material)
  imported_context: {
    has_content: false,     // Whether user provided existing material
    raw_text: null,         // Raw pasted text or document content
    extracted: {
      problem: null,        // Extracted problem/opportunity statement
      solution: null,       // Extracted solution or product idea
      users: null,          // Extracted target user description
      features: null,       // Extracted feature list or MVP scope
      tech_stack: null,     // Extracted technical preferences
      other: null           // Any other extractable info
    },
    pre_filled_answers: {}  // Maps phase_state[N].answers keys → extracted values
  },

  // Output tracking
  output_directory: null,  // "{cwd}/{project-slug}/"
  generated_files: [],     // List of created files in order
  version: "2.0.0"
}
```

**Language detection:** Korean trigger → `language = 'ko'`, English → `language = 'en'`

**Quick Mode:** If triggered via Quick Mode → set `quick_mode = true`, set `mode`, skip to Step 5.

---

### Step 2.5: Context Import

Before asking interview questions, check if the user already has existing material to share.

#### Detection Logic

**Case A: Trigger already contains substantial content**

If the trigger message contains more than ~50 words of description after the trigger keyword, skip the question and extract directly.

```
예시:
"기획해줘: 배달 라이더를 위한 경로 최적화 서비스입니다.
 주요 사용자는 음식배달 플랫폼 소속 라이더이며, 핵심 기능은
 실시간 교통 데이터 연동, 다중 배달지 최적화, 라이더 피로도 기반 경로 조절입니다."

→ 질문 없이 바로 추출 진행
→ session.imported_context.has_content = true
→ session.imported_context.raw_text = [trigger 내용 전체]
```

**Case B: Trigger is short (< ~50 words of content)**

Ask proactively:

Korean:
```
AskUserQuestion(
  "기획하려는 서비스에 대해 기존 아이디어 메모나 문서가 있으신가요?
   있다면 먼저 공유해 주시면 인터뷰 질문을 절반 이하로 줄여드릴 수 있습니다.",
  options=[
    { label: "아이디어/메모 있음", description: "간단한 아이디어 메모, 기능 목록, 구상 중인 내용을 붙여넣어 주세요" },
    { label: "기존 문서 있음", description: "PRD 초안, 기획서, 노션 문서 등을 붙여넣어 주세요" },
    { label: "처음부터 시작", description: "아직 정리된 내용이 없어요. 인터뷰로 처음부터 만들겠습니다" }
  ]
)
```

English:
```
AskUserQuestion(
  "Do you have any existing notes or documents about this product?
   If so, sharing them upfront can cut the interview questions in half.",
  options=[
    { label: "I have notes/ideas", description: "Paste your idea memo, feature list, or rough thoughts" },
    { label: "I have a document", description: "Paste an existing PRD draft, brief, or planning doc" },
    { label: "Starting fresh", description: "Nothing written yet — let's build it from scratch" }
  ]
)
```

If user selects "처음부터 시작" / "Starting fresh":
- Set `session.imported_context.has_content = false`
- Proceed to Step 3 normally

If user selects either content option:
- Prompt: "내용을 여기에 붙여넣어 주세요." / "Please paste your content here."
- Set `session.imported_context.has_content = true`
- Set `session.imported_context.raw_text` = pasted content
- Proceed to extraction (below)

#### Content Extraction

When content is available (Case A or Case B with content), extract:

```pseudocode
function extractFromContent(raw_text):
  extracted = {}

  // Extract problem/opportunity
  if contains_problem_indicators(raw_text):  // "문제", "불편", "pain", "problem", "opportunity"
    extracted.problem = summarize_problem_section(raw_text)

  // Extract solution description
  if contains_solution_indicators(raw_text):  // "기능", "feature", "해결", "솔루션", "solution"
    extracted.solution = summarize_solution_section(raw_text)

  // Extract user/persona mentions
  if contains_user_indicators(raw_text):  // "사용자", "타겟", "user", "customer", "persona"
    extracted.users = extract_user_description(raw_text)

  // Extract feature list
  if contains_feature_list(raw_text):  // bullet lists, numbered lists, "기능 1/2/3"
    extracted.features = extract_feature_list(raw_text)

  // Extract tech preferences
  if contains_tech_indicators(raw_text):  // "React", "Python", "AWS", language/framework names
    extracted.tech_stack = extract_tech_mentions(raw_text)

  session.imported_context.extracted = extracted
  return extracted
```

Map extracted fields to pre-filled answers:
```pseudocode
if extracted.problem:    pre_filled_answers["problem_goals"] = extracted.problem
if extracted.users:      pre_filled_answers["users_market"] = extracted.users
if extracted.features:   pre_filled_answers["constraints"] = extracted.features
if extracted.tech_stack: pre_filled_answers["tech_stack"] = extracted.tech_stack
```

#### User Feedback After Extraction

Show what was extracted before proceeding:

Korean:
```
"내용을 분석했습니다. 다음 정보를 파악했어요:

✅ 문제/기회: [extracted.problem 요약]
✅ 타겟 사용자: [extracted.users 요약]
✅ 핵심 기능: [extracted.features 요약]
⚠️ 아직 파악 안 됨: [미추출 항목 목록]

이 내용을 바탕으로 빠진 부분만 인터뷰로 채워드리겠습니다."
```

**Interview question reduction effect:**
- Pre-filled answers are automatically used during Phase interviews
- Questions whose answers are already extracted are **skipped**
- Typical reduction: 6 questions → 2-3 questions (Solo/Startup), 9 questions → 4-5 questions (Team)

---

### Step 3: Context Detection (Mode Selection)

Ask 3 context questions to determine appropriate mode.

**Question 1: Team Size**

Korean:
```
AskUserQuestion(
  "먼저 상황을 파악하겠습니다. 이 제품을 개발하는 팀 규모는 어떻게 되나요?",
  options=["혼자 (1인)", "2-10명 (소규모)", "10명 이상 (중대규모)"],
  allow_freeform=false
)
```

English:
```
AskUserQuestion(
  "Let's start by understanding your context. How many people are working on this product?",
  options=["Just me (solo)", "2-10 people (small team)", "10+ people (established team)"],
  allow_freeform=false
)
```

**Question 2: Stakeholder Buy-in**

Korean:
```
AskUserQuestion(
  "이 제품에 대해 투자자, 임원, 또는 다른 이해관계자의 승인이 필요한가요?",
  options=["아니오, 혼자 결정", "네, 몇 명 설득 필요", "네, 여러 이해관계자 공식 승인 필요"],
  allow_freeform=false
)
```

**Question 3: Launch Timeline**

Korean:
```
AskUserQuestion(
  "출시 또는 배포 목표 일정은 어떻게 되나요?",
  options=["3개월 미만 (빠른 실험)", "3-6개월 (일반적)", "6개월 이상 (전략적 이니셔티브)"],
  allow_freeform=false
)
```

**Scoring rubric:**

| Answer Pattern | Mode |
|----------------|------|
| 혼자 + 혼자 결정 + 3개월 미만 | **Solo** (Lean Canvas, 20-30분/phase) |
| 2-10명 + 몇 명 설득 + 3-6개월 | **Startup** (Product Brief, 30-40분/phase) |
| 10명 이상 + 공식 승인 + 6개월 이상 | **Team** (Full PRD, 45-60분/phase) |

Mixed answers → use majority scoring. If tie → default to Startup.

---

### Step 4: Mode Confirmation

Present recommended mode and allow override:

Korean:
```
"컨텍스트를 바탕으로 **{MODE} 모드**를 권장합니다.

**{MODE} 모드** 특징:
- 인터뷰 깊이: {DEPTH_DESCRIPTION}
- Phase당 소요 시간: {TIME_PER_PHASE}

이 모드로 진행할까요?"

AskUserQuestion(
  "{MODE} 모드로 진행하시겠어요?",
  options=["{MODE} 모드 (권장)", "Solo 모드", "Startup 모드", "Team 모드"],
  allow_freeform=false
)
```

Set `session.mode` based on confirmation.

**Mode characteristics:**
- **Solo**: 4→3→4→3 questions per phase, 1 round each. Focus on essentials.
- **Startup**: 6→5→6→4 questions per phase, 2 rounds for Phase 1&3. Covers business depth.
- **Team**: 9→7→9→6 questions per phase, 2-3 rounds. Full strategic + operational coverage.

---

### Step 5: Document Selection

After mode is confirmed, ask which documents to generate.

Korean:
```
"좋습니다. 어떤 문서를 생성할까요? (여러 개 선택 가능)

① PRD ({PRD_TYPE})         — 제품 요구사항 정의 (항상 포함 권장)
② User Journey Map         — 사용자 흐름 및 경험 정의
③ Technical Specification  — 기술 명세, 아키텍처, 데이터 모델
④ Wireframe Specification  — 화면 명세 및 IA"
```

```
AskUserQuestion(
  "생성할 문서를 선택해주세요",
  options=[
    "① PRD만",
    "① + ② (PRD + User Journey)",
    "① + ② + ③ (PRD + Journey + Tech Spec)",
    "① + ② + ③ + ④ (전체)"
  ],
  allow_freeform=false
)
```

If "Other" / user types a custom combination:
```
AskUserQuestion(
  "생성할 문서를 모두 선택해주세요",
  options=[
    "① PRD",
    "② User Journey Map",
    "③ Technical Specification",
    "④ Wireframe Specification"
  ],
  multiSelect=true
)
```

Set `session.phases_selected` based on selection. Example: [1, 2, 3] for ① + ② + ③.

**Note:** Phase 1 (PRD) is strongly recommended as the foundation for all other documents.
If user selects Phase 2/3/4 without Phase 1, warn but allow: "PRD 없이 진행하면 다른 문서에서 컨텍스트 참조가 제한됩니다."

---

### Interview Question Convention

> **IMPORTANT — Two question types, two different approaches:**
>
> | Type | When | How to execute |
> |------|------|----------------|
> | `AskUserQuestion(q, options=[...])` | Steps 2.5, 3, 4, 5 — structured choice | Call the **AskUserQuestion tool** (options required, 2–4 items) |
> | `AskUserQuestion(q, allow_freeform=true)` | Steps 7–14 — open-ended interview | **Output the question as plain text.** Do NOT call the AskUserQuestion tool. Wait for free-form user response. |
>
> The `allow_freeform=true` notation is pseudo-code shorthand. The real AskUserQuestion tool does not accept this parameter and requires at least 2 options — calling it for freeform questions will error.

---

### Step 6: Phase Router

Execute phases in order (1 → 2 → 3 → 4), skipping unselected phases.

```pseudocode
for phase_num in [1, 2, 3, 4]:
  if phase_num in session.phases_selected:
    session.current_phase = phase_num
    session.phase_state[phase_num].status = "in_progress"
    execute_phase(phase_num)
    session.phase_state[phase_num].status = "completed"
    session.phases_completed.append(phase_num)
  else:
    session.phase_state[phase_num].status = "skipped"

show_final_summary()
```

---

### Step 7: Phase 1 Interview — PRD

**Max rounds by mode:**
- Solo: 1 round (4 questions)
- Startup: 2 rounds (6 questions)
- Team: 3 rounds (9 questions)

Set `session.phase_state[1].max_rounds` and `session.phase_state[1].template_type`:
- Solo → `lean-canvas`
- Startup → `product-brief`
- Team → `full-prd`

#### Step 7.1: Solo Mode Questions (4Q / 1R)

```
AskUserQuestion(
  "이 제품이 해결하는 구체적인 문제는 무엇인가요? 타겟 사용자가 이 문제를 겪는 실제 상황을 설명해주세요.",
  allow_freeform=true
)
→ session.phase_state[1].answers["problem_goals"]
```

```
AskUserQuestion(
  "한 문장으로 솔루션을 설명해주세요. 기존 대안과 비교했을 때 무엇이 다른가요?",
  allow_freeform=true
)
→ session.phase_state[1].answers["solution_strategy"]
```

```
AskUserQuestion(
  "주요 타겟 사용자는 누구인가요? 역할, 필요한 것, 현재 사용하는 대안을 구체적으로.",
  allow_freeform=true
)
→ session.phase_state[1].answers["users_market"]
```

```
AskUserQuestion(
  "MVP에서 반드시 필요한 기능 3가지는? 그리고 v2로 미룰 수 있는 것은?",
  allow_freeform=true
)
→ session.phase_state[1].answers["constraints"]
```

#### Step 7.2: Startup Mode Questions (6Q / 2R)

**Round 1:**

```
AskUserQuestion(
  "이 제품이 해결하는 비즈니스 기회나 시장 공백은 무엇인가요? TAM(전체 시장 규모)은 어느 정도인가요?",
  allow_freeform=true
)
→ answers["problem_goals"]
```

```
AskUserQuestion(
  "타겟 고객이 오늘날 가장 많은 시간이나 비용을 허비하는 구체적인 Pain Point는 무엇인가요?",
  allow_freeform=true
)
→ answers["pain_points"]
```

```
AskUserQuestion(
  "제품의 핵심 가치 제안을 30초 엘리베이터 피치로 설명해주세요.",
  allow_freeform=true
)
→ answers["solution_strategy"]
```

**Round 2:**

```
AskUserQuestion(
  "주요 사용자 페르소나를 설명해주세요. 역할, 목표, Pain Point, 현재 사용하는 도구를 포함해서.",
  allow_freeform=true
)
→ answers["users_market"]
```

```
AskUserQuestion(
  "첫 100명의 고객을 어떻게 확보할 계획인가요? GTM 전략은?",
  allow_freeform=true
)
→ answers["gtm_strategy"]
```

```
AskUserQuestion(
  "North Star Metric은 무엇인가요? PMF(제품-시장 적합성)를 증명할 정량적 목표는?",
  allow_freeform=true
)
→ answers["success_metrics"]
```

#### Step 7.3: Team Mode Questions (9Q / 3R)

**Round 1 (Strategic Alignment):**

```
AskUserQuestion(
  "이 제품/기능이 회사의 어떤 전략적 목표와 연결되나요? 어떤 OKR 또는 경영진 우선순위를 지원하나요?",
  allow_freeform=true
)
→ answers["strategic_alignment"]
```

```
AskUserQuestion(
  "이해관계자는 누구이고, 각자 어떤 성공을 기대하나요? 승인을 위한 핵심 기준은?",
  allow_freeform=true
)
→ answers["stakeholders"]
```

```
AskUserQuestion(
  "이 기능이 없으면 비즈니스에 어떤 비용이 발생하나요? (기회비용, 이탈률, 매출 손실 등)",
  allow_freeform=true
)
→ answers["problem_goals"]
```

**Round 2 (User & Market):**

```
AskUserQuestion(
  "사용자 세그먼트별 Pain Point를 설명해주세요. 기존 사용자 리서치나 데이터가 있다면 인사이트를 공유해주세요.",
  allow_freeform=true
)
→ answers["users_market"]
```

```
AskUserQuestion(
  "경쟁 환경과 시장 포지셔닝 전략은? 주요 경쟁사 대비 우리의 차별화 포인트는?",
  allow_freeform=true
)
→ answers["competitive_analysis"]
```

```
AskUserQuestion(
  "핵심 가치 제안과 솔루션 개요를 설명해주세요. 제품 비전(1-2년 후)은 어떤 모습인가요?",
  allow_freeform=true
)
→ answers["solution_strategy"]
```

**Round 3 (Requirements):**

```
AskUserQuestion(
  "MoSCoW로 기능을 분류해주세요. Must-Have/Should-Have/Could-Have/Won't-Have 기준은 무엇인가요?",
  allow_freeform=true
)
→ answers["constraints"]
```

```
AskUserQuestion(
  "비기능 요구사항은? (성능 목표, 보안 등급, 접근성, 다국어 지원 등)",
  allow_freeform=true
)
→ answers["nfr"]
```

```
AskUserQuestion(
  "성공 지표와 측정 방법, 목표치를 구체적으로 설명해주세요. 각 이해관계자 그룹별 성공 기준은?",
  allow_freeform=true
)
→ answers["success_metrics"]
```

#### Step 7.4: Pre-filled Answer Skip Logic

Before asking any question, check if it was already answered via Context Import:

```pseudocode
function shouldSkipQuestion(answer_key):
  if session.imported_context.has_content:
    pre_filled = session.imported_context.pre_filled_answers
    if answer_key in pre_filled AND pre_filled[answer_key] is not null:
      // Auto-populate the answer
      session.phase_state[1].answers[answer_key] = pre_filled[answer_key]
      return true  // Skip this question
  return false

// Usage before each question:
if not shouldSkipQuestion("problem_goals"):
  AskUserQuestion("이 제품이 해결하는 구체적인 문제는...")
```

When skipping, briefly inform the user:
```
"문제/기회는 이미 파악되었습니다: [{extracted summary}] — 다음 질문으로 넘어갑니다."
```

#### Step 7.5: Answer Completeness Scoring

After each response, score 1-5:

```pseudocode
function scoreAnswerCompleteness(answer, question_category):
  score = 5

  word_count = count_words(answer)
  if word_count < 10: score = min(score, 2)
  elif word_count < 20: score = min(score, 3)

  generic_terms = ["thing", "stuff", "better", "easier", "faster", "improve", "좋아", "편리", "빠르게"]
  if contains_only_generic_terms(answer) AND lacks_examples(answer):
    score = min(score, 2)

  if asks_for_metrics(question_category) AND not_contains_numbers(answer):
    score = min(score, 3)

  if has_concrete_example(answer):
    score = min(score + 1, 5)

  return score
```

If score < 3: ask one targeted follow-up. If still < 3 after follow-up: accept and mark `[TODO]`.

Store in `session.phase_state[1].completeness_scores[category]`.

#### Step 7.6: Session Management (Team Mode)

After every 3 rounds in Team mode, offer save point:
```
"현재 {percentage}% 진행되었습니다. 잠깐 쉬시겠어요?
- 계속 진행 (~{remaining} min 남음)
- 저장 후 나중에 재개"
```

If save: write `planning-interview-draft-{project_slug}-{timestamp}.md` with session JSON.
Resume trigger: "planning interview 계속해줘"

---

### Step 8: Phase 1 Completion — Generate PRD

1. **Determine project name & slug** from answers:
   - Ask if not yet determined: "제품 이름이 뭔가요?"
   - Generate slug: lowercase, spaces→hyphens, remove special chars
   - Set `session.project_name`, `session.project_slug`

2. **Create output directory:**
   ```bash
   mkdir -p {project_slug}
   ```

3. **Populate shared_context** from Phase 1 answers:
   ```
   session.shared_context.personas = extract_personas(answers["users_market"])
   session.shared_context.core_features = extract_must_haves(answers["constraints"])
   session.shared_context.project_goals = answers["success_metrics"]
   session.shared_context.problem_statement = answers["problem_goals"]
   ```

4. **Load template** based on `session.phase_state[1].template_type`:
   - Solo: `templates/lean-canvas.md`
   - Startup: `templates/product-brief.md`
   - Team: `templates/full-prd.md`

5. **Validate placeholders:**
   ```pseudocode
   for placeholder in required_placeholders:
     content = map_placeholder_to_answer(placeholder, answers)
     if empty(content): mark as "[TODO: {description}]"
   ```

6. **Add metadata header:**
   ```markdown
   <!-- Generated by planning-interview v2.0.0 -->
   <!-- Phase: 1 (PRD) | Mode: {mode} | Language: {language} -->
   <!-- Session Start: {start_time} | Generated: {current_datetime} -->
   ```

7. **Save file:** `{project_slug}/prd.md`

8. **Confirm and show Phase Handoff** (if more phases selected):
   ```
   ✅ PRD 생성 완료: {project_slug}/prd.md

   다음 단계: User Journey Map 작성
   계속 진행할까요?
   ```

---

### Step 9: Phase 2 Interview — User Journey Map

Skip if Phase 2 not in `session.phases_selected`.

**Pre-fill check:** Before each question, run `shouldSkipQuestion(answer_key)` using `session.imported_context.pre_filled_answers`. Skip and auto-populate if already extracted.

**Max rounds by mode:**
- Solo: 1 round (3 questions)
- Startup: 1 round (5 questions)
- Team: 2 rounds (7 questions)

**Context injection from shared_context:**
Reference `session.shared_context.personas` and `session.shared_context.problem_statement` in questions:
> "Phase 1에서 [persona]를 주요 사용자로 언급하셨는데..."

#### Step 9.1: Solo Mode Questions (3Q / 1R)

```
AskUserQuestion(
  "제품의 핵심 사용 흐름을 처음부터 끝까지 설명해주세요. 사용자가 처음 접속해서 핵심 가치를 경험하는 순간까지 단계별로.",
  allow_freeform=true
)
→ phase_state[2].answers["core_journey"]
```

```
AskUserQuestion(
  "가장 자주 발생할 실패 시나리오나 사용자가 막힐 것 같은 지점은 어디인가요?",
  allow_freeform=true
)
→ answers["friction_points"]
```

```
AskUserQuestion(
  "사용자가 처음 사용할 때 'aha moment'는 언제이고, 그 순간을 얼마나 빠르게 경험하게 할 건가요?",
  allow_freeform=true
)
→ answers["aha_moment"]
```

#### Step 9.2: Startup Mode Questions (5Q / 1R)

```
AskUserQuestion(
  "[{persona}] 관점에서, 핵심 사용 시나리오 2-3가지를 단계별로 설명해주세요. 각 시나리오에서 사용자 목표, 행동, 기대 결과를 포함해서.",
  allow_freeform=true
)
→ answers["core_journeys"]
```

```
AskUserQuestion(
  "사용자가 'aha moment'를 언제 경험하길 바라나요? 처음 접속부터 그 순간까지 몇 단계, 몇 분이 걸리나요?",
  allow_freeform=true
)
→ answers["aha_moment"]
```

```
AskUserQuestion(
  "가장 예상되는 마찰 지점(friction point)은 어디인가요? 사용자가 이탈할 가능성이 높은 순간은?",
  allow_freeform=true
)
→ answers["friction_points"]
```

```
AskUserQuestion(
  "사용자가 제품을 습관적으로 사용하게 만드는 트리거와 리텐션 메커니즘은 무엇인가요?",
  allow_freeform=true
)
→ answers["retention"]
```

```
AskUserQuestion(
  "네트워크 오류, 데이터 없음, 권한 없음 등 예외 상황에서 사용자 흐름은 어떻게 되나요?",
  allow_freeform=true
)
→ answers["error_journeys"]
```

#### Step 9.3: Team Mode Questions (7Q / 2R)

**Round 1:**

```
AskUserQuestion(
  "사용자 유형별로 핵심 journey를 설명해주세요. [{personas}] 각각의 진입점, 주요 행동, 목표, 이탈 지점을 포함해서.",
  allow_freeform=true
)
→ answers["user_type_journeys"]
```

```
AskUserQuestion(
  "각 journey의 주요 단계마다 사용자의 목표(Goal), 행동(Action), 감정(Emotion), 고통(Pain)을 설명해주세요.",
  allow_freeform=true
)
→ answers["stage_details"]
```

```
AskUserQuestion(
  "크로스-채널 touchpoint가 있나요? (예: 앱 → 이메일 알림 → 웹 접속). 채널 간 전환 시 데이터/컨텍스트 유지는?",
  allow_freeform=true
)
→ answers["cross_channel"]
```

```
AskUserQuestion(
  "가장 중요한 edge case journey는? (권한 없음, 데이터 없음, 오류 상황, 동시 접근 등)",
  allow_freeform=true
)
→ answers["edge_journeys"]
```

**Round 2:**

```
AskUserQuestion(
  "온보딩 흐름을 설명해주세요. 신규 사용자가 처음 가치를 경험하기까지 단계와 예상 소요 시간은?",
  allow_freeform=true
)
→ answers["onboarding"]
```

```
AskUserQuestion(
  "리텐션 트리거는 무엇인가요? 사용자가 다시 돌아오게 만드는 메커니즘(알림, 습관, 가치 제공 주기)은?",
  allow_freeform=true
)
→ answers["retention"]
```

```
AskUserQuestion(
  "접근성(장애인, 고령자) 요구사항이나 다국어 지원이 필요한 journey 단계가 있나요?",
  allow_freeform=true
)
→ answers["accessibility"]
```

---

### Step 10: Phase 2 Completion — Generate User Journey Map

1. Load `templates/user-journey-map.md`
2. Map answers to placeholders, mark gaps as `[TODO]`
3. Add metadata header:
   ```markdown
   <!-- Generated by planning-interview v2.0.0 -->
   <!-- Phase: 2 (User Journey Map) | Mode: {mode} | Language: {language} -->
   <!-- PRD Reference: {project_slug}/prd.md -->
   ```
4. Save: `{project_slug}/user-journey-map.md`
5. Confirm and show Phase Handoff (if next phase selected)

---

### Step 11: Phase 3 Interview — Technical Specification

Skip if Phase 3 not in `session.phases_selected`.

**Pre-fill check:** Before each question, run `shouldSkipQuestion(answer_key)`. Tech stack, data storage, and dependency questions may be pre-filled if the user's imported content mentioned specific technologies.

**Max rounds by mode:**
- Solo: 1 round (4 questions)
- Startup: 2 rounds (6 questions)
- Team: 3 rounds (9 questions)

**Context injection:** Reference `session.shared_context.core_features` in questions:
> "[{core_features}]를 구현하기 위한 기술 스택은..."

#### Step 11.1: Solo Mode Questions (4Q / 1R)

```
AskUserQuestion(
  "[{core_features}]를 구현할 기술 스택은? (언어, 프레임워크, 데이터베이스) 선택 이유는?",
  allow_freeform=true
)
→ phase_state[3].answers["tech_stack"]
```

```
AskUserQuestion(
  "데이터를 어디에 어떻게 저장하나요? 민감한 데이터(개인정보, 결제 등)가 있나요?",
  allow_freeform=true
)
→ answers["data_storage"]
```

```
AskUserQuestion(
  "외부 서비스나 API 의존성이 있나요? 있다면 해당 서비스가 다운됐을 때 어떻게 처리하나요?",
  allow_freeform=true
)
→ answers["dependencies"]
```

```
AskUserQuestion(
  "예상 사용자 규모와 성능 요구사항은? (응답 시간 목표, 동시 사용자 수)",
  allow_freeform=true
)
→ answers["performance"]
```

#### Step 11.2: Startup Mode Questions (6Q / 2R)

**Round 1:**

```
AskUserQuestion(
  "기술 스택과 선택 이유를 설명해주세요. 특별히 고려한 대안과 선택하지 않은 이유는?",
  allow_freeform=true
)
→ answers["tech_stack"]
```

```
AskUserQuestion(
  "핵심 데이터 모델을 설명해주세요. 주요 엔티티와 그들의 관계는? 어떤 데이터베이스를 사용하고 왜인가요?",
  allow_freeform=true
)
→ answers["data_models"]
```

```
AskUserQuestion(
  "외부 서비스/API 의존성과 fallback 전략은? 각 의존성이 실패했을 때 사용자에게 어떻게 보여야 하나요?",
  allow_freeform=true
)
→ answers["dependencies"]
```

**Round 2:**

```
AskUserQuestion(
  "성능 요구사항을 구체적으로 설명해주세요. (동시 사용자 수, 응답 시간 SLA, 데이터 규모 예측)",
  allow_freeform=true
)
→ answers["performance"]
```

```
AskUserQuestion(
  "보안 요구사항은? 인증 방식(OAuth/JWT/세션), 권한 모델, 민감 데이터 처리 방법은?",
  allow_freeform=true
)
→ answers["security"]
```

```
AskUserQuestion(
  "배포 환경과 인프라는? (클라우드 서비스, 컨테이너, CI/CD 파이프라인 구성)",
  allow_freeform=true
)
→ answers["infrastructure"]
```

#### Step 11.3: Team Mode Questions (9Q / 3R)

**Round 1 (Architecture):**

```
AskUserQuestion(
  "현재 시스템 아키텍처와 이 제품/기능이 어떻게 통합되나요? 레거시 호환성 제약이 있나요?",
  allow_freeform=true
)
→ answers["architecture"]
```

```
AskUserQuestion(
  "핵심 데이터 모델과 엔티티 관계를 설명해주세요. 데이터베이스 선택과 그 이유는?",
  allow_freeform=true
)
→ answers["data_models"]
```

```
AskUserQuestion(
  "동시성 처리가 필요한 시나리오가 있나요? (동시 편집, 실시간 업데이트, 분산 트랜잭션 등) 어떻게 처리할 건가요?",
  allow_freeform=true
)
→ answers["concurrency"]
```

**Round 2 (Quality & Risk):**

```
AskUserQuestion(
  "장애 시나리오와 복구 전략은? (failover, circuit breaker, 데이터 일관성 보장, RTO/RPO 목표)",
  allow_freeform=true
)
→ answers["failure_recovery"]
```

```
AskUserQuestion(
  "보안 아키텍처를 설명해주세요. 인증, 인가, 데이터 암호화, API 보안, 감사 로깅 전략은?",
  allow_freeform=true
)
→ answers["security"]
```

```
AskUserQuestion(
  "테스트 전략은? 단위/통합/E2E 테스트 커버리지 목표와 테스트 환경 구성은?",
  allow_freeform=true
)
→ answers["testing"]
```

**Round 3 (Operations):**

```
AskUserQuestion(
  "모니터링과 알림 요구사항은? 어떤 메트릭을 추적하고, 어떤 조건에서 알림을 발송할 건가요?",
  allow_freeform=true
)
→ answers["monitoring"]
```

```
AskUserQuestion(
  "보안 감사나 컴플라이언스 요구사항이 있나요? (GDPR, SOC2, ISO27001, HIPAA 등)",
  allow_freeform=true
)
→ answers["compliance"]
```

```
AskUserQuestion(
  "구현을 Phase로 나눈다면? 각 Phase의 목표, 포함 기능, 완료 기준과 예상 일정은?",
  allow_freeform=true
)
→ answers["implementation_phases"]
```

---

### Step 12: Phase 3 Completion — Generate Technical Specification

1. Load `templates/tech-spec.md`
2. Map answers to placeholders. For data models, format as TypeScript interfaces.
3. Add metadata header:
   ```markdown
   <!-- Generated by planning-interview v2.0.0 -->
   <!-- Phase: 3 (Technical Specification) | Mode: {mode} | Language: {language} -->
   <!-- PRD Reference: {project_slug}/prd.md -->
   ```
4. Save: `{project_slug}/tech-spec.md`
5. Confirm and show Phase Handoff (if Phase 4 selected)

---

### Step 13: Phase 4 Interview — Wireframe Specification

Skip if Phase 4 not in `session.phases_selected`.

**Pre-fill check:** Before each question, run `shouldSkipQuestion(answer_key)`. Screen list or navigation structure may be pre-filled if the user's imported content described specific UI flows.

**Max rounds by mode:**
- Solo: 1 round (3 questions)
- Startup: 1 round (4 questions)
- Team: 2 rounds (6 questions)

**Context injection:** Reference User Journey screens from Phase 2 (if completed):
> "Phase 2에서 언급하신 [journey stages]를 화면으로 구현한다면..."

#### Step 13.1: Solo Mode Questions (3Q / 1R)

```
AskUserQuestion(
  "제품의 주요 화면 목록을 나열해주세요. 각 화면의 핵심 목적 한 문장씩.",
  allow_freeform=true
)
→ phase_state[4].answers["screen_list"]
```

```
AskUserQuestion(
  "가장 중요한 화면에서 사용자가 볼 수 있는 주요 UI 요소와 취할 수 있는 행동은?",
  allow_freeform=true
)
→ answers["key_screen"]
```

```
AskUserQuestion(
  "내비게이션 구조는? 화면 간 이동 방식과 주요 탐색 패턴은?",
  allow_freeform=true
)
→ answers["navigation"]
```

#### Step 13.2: Startup Mode Questions (4Q / 1R)

```
AskUserQuestion(
  "화면 목록과 각 화면의 목적, 그 화면에서 완료해야 할 주요 task를 설명해주세요.",
  allow_freeform=true
)
→ answers["screen_list"]
```

```
AskUserQuestion(
  "내비게이션 구조와 화면 간 이동 플로우는? (탭, 사이드바, 드로어, 모달 등 어떤 패턴을 사용하나요?)",
  allow_freeform=true
)
→ answers["navigation"]
```

```
AskUserQuestion(
  "각 주요 화면에서 가장 중요한 UI 컴포넌트 3가지와 그 역할 및 동작을 설명해주세요.",
  allow_freeform=true
)
→ answers["components"]
```

```
AskUserQuestion(
  "빈 상태(empty state), 로딩, 오류, 성공 상황에서 각 화면이 어떻게 보여야 하나요?",
  allow_freeform=true
)
→ answers["ui_states"]
```

#### Step 13.3: Team Mode Questions (6Q / 2R)

**Round 1:**

```
AskUserQuestion(
  "모든 화면 목록과 각 화면의 URL/라우트, 목적, 진입 경로(어디서 이 화면으로 오는가)를 설명해주세요.",
  allow_freeform=true
)
→ answers["screen_list"]
```

```
AskUserQuestion(
  "내비게이션 구조를 설명해주세요. 주요 탐색 방식(탭바, 사이드바, 드로어)과 그 안의 항목들은?",
  allow_freeform=true
)
→ answers["navigation"]
```

```
AskUserQuestion(
  "각 주요 화면의 레이아웃을 설명해주세요. 헤더, 메인 컨텐츠 영역, 사이드바, 푸터 구성은?",
  allow_freeform=true
)
→ answers["layouts"]
```

**Round 2:**

```
AskUserQuestion(
  "화면별 핵심 컴포넌트 유형과 역할, 동작을 설명해주세요. (버튼, 폼, 테이블, 카드, 리스트 등)",
  allow_freeform=true
)
→ answers["components"]
```

```
AskUserQuestion(
  "주요 인터랙션 패턴은 무엇인가요? (드래그앤드롭, 인라인 편집, 무한 스크롤, 모달, 토스트 알림 등)",
  allow_freeform=true
)
→ answers["interactions"]
```

```
AskUserQuestion(
  "빈 상태, 로딩, 오류, 성공 상태에서 각 화면이 어떻게 보여야 하나요? 접근성(WCAG) 요구사항은?",
  allow_freeform=true
)
→ answers["ui_states"]
```

---

### Step 14: Phase 4 Completion — Generate Wireframe Specification

1. Load `templates/wireframe-spec.md`
2. Map answers to placeholders. Generate ASCII layout diagrams for key screens using answers.
3. Add metadata header:
   ```markdown
   <!-- Generated by planning-interview v2.0.0 -->
   <!-- Phase: 4 (Wireframe Specification) | Mode: {mode} | Language: {language} -->
   <!-- PRD Reference: {project_slug}/prd.md -->
   ```
4. Save: `{project_slug}/wireframe-spec.md`

---

### Step 15: Final Summary

After all selected phases complete, show completion summary:

```
🎉 기획 문서 생성 완료!

📁 {project_slug}/
{GENERATED_FILES_LIST}

총 소요 시간: {elapsed_time}분

다음 단계:
1. 생성된 문서들을 검토하고 [TODO] 항목을 채워주세요
2. 팀과 공유하고 피드백을 받으세요
3. 기술 구현을 시작하세요
```

Where `{GENERATED_FILES_LIST}` shows each file with a brief description:
```
  ✅ prd.md               (Product Brief, Mode: Startup)
  ✅ user-journey-map.md  (3가지 journey 정의)
  ✅ tech-spec.md         (12개 기능 요구사항)
  ✅ wireframe-spec.md    (8개 화면 명세)
```

---

### Step 16: Error Handling

| Error Type | Detection | Fallback Strategy |
|------------|-----------|-------------------|
| Template missing | File read fails | Use embedded minimal template, warn user |
| Directory creation fails | mkdir fails | Save to current directory, warn user |
| User abandons (5 min) | No response | Auto-save partial draft as `{project_slug}/draft-{phase}-{timestamp}.md` |
| Vague answers loop | Score <3 after 2 follow-ups | Accept, mark `[TODO]`, continue |
| Write permission denied | Write() fails | Try `~/Desktop/{project_slug}/`, display content if all fail |
| Invalid mode | Unexpected value | Default to Startup mode |
| Phase skip after start | User says "다음으로" | Mark current phase complete, move to next selected |
| Pasted content is too short | raw_text < 30 words | Treat as "처음부터 시작", proceed without import |
| Extraction yields nothing | All extracted fields null | Treat as "처음부터 시작", run full interview |
| Pre-filled answer is vague | Extracted text is generic/incomplete | Ask question anyway; use extracted value as default option |

---

## Notes

- **Phase 1 is foundational**: shared_context from Phase 1 enriches all subsequent phase interviews
- **Completeness over speed**: Use the 1-5 scoring system consistently; mark gaps as [TODO] rather than skipping
- **Language consistency**: Detect language from trigger, maintain throughout all phases and generated files
- **Mode determines depth, not scope**: Any mode can generate any document combination
- **Project slug**: Generate from product name early in Phase 1; all files go under `{project_slug}/`
- **spec-interview plugin**: Remains as a standalone option for users who only need a tech spec without product planning
- **Context Import is additive**: Never trust imported content blindly — always validate key extracted facts during interview if they seem vague or contradictory
- **Content in trigger = skip the question**: If the user already wrote their idea in the trigger message itself (>50 words), skip the "Do you have existing material?" question entirely
- **Don't over-skip**: Even with rich imported content, always ask at least 1-2 clarifying questions per phase to validate understanding and surface unstated assumptions
