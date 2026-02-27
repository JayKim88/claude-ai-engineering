---
name: launch-kit
description: 4-question interview that instantly generates all validation content for an indie hacker's product idea. Produces landing page copy, Indie Hackers post, Reddit r/SideProject post, email sequence, and Founding Plan pre-sale offer — all in one markdown file. Use when user says "launch-kit", "/launch-kit", "아이디어 검증", "랜딩페이지 만들어줘", "validate my idea", "검증 키트", "launch my idea".
metadata:
  version: 1.1.0
  author: Jay Kim
---

# Launch Kit Skill v1.1.0

## Purpose

Transform a raw product idea into a complete set of launch-ready validation content through a lean 4-question interview. The output is a single markdown file with 5 content sections, ready to copy-paste into Carrd, Kit, Indie Hackers, and Reddit.

**Output sections:**
1. Landing Page Copy (Headline, Subheadline, 3 features, CTA button, 5 FAQs)
2. Indie Hackers post (community-appropriate, show-don't-tell tone)
3. Reddit r/SideProject post (casual, value-first tone)
4. Email Sequence (Welcome email + Day 3 follow-up)
5. Founding Plan Pre-Sale Offer (50% discount copy with urgency)

**Key design principles:**
- Interview uses plain text output for free-form questions (NOT AskUserQuestion tool)
- Language auto-detected from trigger: Korean trigger → Korean output, English → English
- Supported output languages: Korean and English only
- Notes pasted inline (>50 words) → extract answers, skip covered questions
- Partially extracted answers → targeted follow-up only (not full question)
- Vague answer: ask ONE follow-up, then accept and mark [TODO]
- Q2 (differentiation) always includes a hint example
- After save: suggest planning-interview for PRD

---

## Trigger Phrases

**English:**
- "launch-kit"
- "/launch-kit"
- "validate my idea"
- "launch my idea"
- "landing page copy"
- "help me launch [product]"

**Korean:**
- "아이디어 검증"
- "랜딩페이지 만들어줘"
- "검증 키트"
- "런치킷"
- "아이디어 검증해줘"

---

## When to Use

Use this skill when the user wants to:
- Validate a product idea before building
- Generate landing page copy quickly
- Create community posts for Indie Hackers or Reddit
- Write an email sequence for early waitlist subscribers
- Draft a pre-sale offer for founding members

**Note: Supported output languages are Korean and English only. Triggers in other languages will default to English output.**

Do NOT use this skill when:
- User wants a full PRD or technical spec (use `planning-interview`)
- User wants market research or competitive analysis (use `market-research-by-desire`)
- User wants a business plan (use `business-avengers`)

---

## Execution Algorithm

### Step 1: Trigger Detection and Language Setting

Detect language from the trigger message and initialize session state.

```pseudocode
function detectLanguage(trigger_message):
  korean_markers = ["아이디어", "랜딩페이지", "검증", "런치킷", "만들어줘", "해줘"]
  for marker in korean_markers:
    if marker in trigger_message:
      return "ko"
  return "en"

session = {
  language: detectLanguage(trigger_message),
  product_name: null,
  product_slug: null,
  answers: {
    problem: null,       // Q1: specific problem and real situation
    solution: null,      // Q2: one-sentence differentiation
    target: null,        // Q3: target user with role and tools
    mvp_scope: null      // Q4: 3 must-haves + v2 deferred items
  },
  completeness: {
    problem: 0,
    solution: 0,
    target: 0,
    mvp_scope: 0
  },
  notes_imported: false,
  notes_partial: {      // tracks which fields were extracted from notes but need targeted follow-up
    problem: false,     // set true when: extracted word_count <= 15, or score < 3
    solution: false,
    target: false,
    mvp_scope: false
  },
  output_path: null,
  generated_at: null
}
```

---

### Step 2: Notes Import Detection

Before asking the first interview question, check if the trigger message already contains substantial product description.

```pseudocode
function extractInlineNotes(trigger_message):
  content = remove_trigger_keyword(trigger_message)
  word_count = count_words(content)
  if word_count > 50:
    return content
  return null
```

**Case A: Trigger contains more than 50 words of description**

Extract answers from the inline notes without asking the user whether they have notes.

```pseudocode
if inline_notes = extractInlineNotes(trigger_message):
  session.notes_imported = true
  extracted = extractAnswersFromNotes(inline_notes)

  for field in [problem, solution, target, mvp_scope]:
    if extracted[field] is not null:
      word_count = count_words(extracted[field])
      if word_count > 15:
        session.answers[field] = extracted[field]
        session.completeness[field] = scoreCompleteness(extracted[field])
        // Mark as partial if score is borderline (< 3) — needs targeted follow-up
        session.notes_partial[field] = (scoreCompleteness(extracted[field]) < 3)
      else:
        // Too short to be reliable — mark for targeted follow-up
        session.notes_partial[field] = true
    // If extracted[field] is null, leave notes_partial[field] = false (no data → full question)

  show_extraction_summary(extracted, session.language)
```

**Extraction logic:**

```pseudocode
function extractAnswersFromNotes(notes):
  extracted = {}

  problem_keywords = ["문제", "불편", "pain", "problem", "struggle", "frustration",
                      "hours", "시간", "힘들", "어렵", "waste", "낭비"]
  if contains_any(notes, problem_keywords):
    extracted.problem = summarize_section(notes, "problem")

  solution_keywords = ["unlike", "different", "vs", "compared", "대신", "차별점",
                       "unique", "only", "first", "유일", "특징", "instead"]
  if contains_any(notes, solution_keywords):
    extracted.solution = summarize_section(notes, "solution")

  target_keywords = ["target", "user", "customer", "developer", "designer", "타겟",
                     "사용자", "개발자", "누구", "for ", "aimed at", "팀"]
  if contains_any(notes, target_keywords):
    extracted.target = summarize_section(notes, "target")

  feature_keywords = ["feature", "must-have", "기능", "MVP", "v1", "v2",
                      "need to", "필요", "포함", "exclude", "핵심"]
  if contains_any(notes, feature_keywords):
    extracted.mvp_scope = summarize_section(notes, "mvp_scope")

  return extracted
```

Show extraction summary before continuing.

For each field in the summary: if `session.notes_partial[field] == true`, append the reason in parentheses ("under 15 words" or "score < 3").

Korean:
```
"내용을 분석했습니다:

확인된 내용:
- 문제: [extracted.problem 요약, 최대 20단어]  ← notes_partial.problem == true인 경우: "(부분 추출 — 추가 질문 예정: 15단어 미만 또는 점수 < 3)"
- 솔루션: [extracted.solution 요약]  ← notes_partial.solution == true인 경우: "(부분 추출 — 추가 질문 예정)"
- 타겟: [extracted.target 요약]  ← notes_partial.target == true인 경우: "(부분 추출 — 추가 질문 예정)"
- MVP 범위: [extracted.mvp_scope 요약]  ← notes_partial.mvp_scope == true인 경우: "(부분 추출 — 추가 질문 예정)"

아직 확인이 필요한 내용: [null 필드 목록]
부분적으로 추출된 내용: [notes_partial=true 필드 목록 + 이유: 15단어 미만 또는 점수 < 3]

빠진 부분과 부분 추출된 부분만 추가로 질문드리겠습니다."
```

English:
```
"I analyzed your notes:

Extracted:
- Problem: [summary, max 20 words]  ← if notes_partial.problem == true: "(partial — follow-up question coming: under 15 words or score < 3)"
- Solution: [summary]  ← if notes_partial.solution == true: "(partial — follow-up question coming)"
- Target: [summary]  ← if notes_partial.target == true: "(partial — follow-up question coming)"
- MVP scope: [summary]  ← if notes_partial.mvp_scope == true: "(partial — follow-up question coming)"

Still need: [list of null fields]
Partial extracts (follow-up needed): [list of notes_partial=true fields with reason: under 15 words or score < 3]

I'll only ask about the missing or partial pieces."
```

**Case B: Trigger is short (fewer than 50 words)**

Do NOT ask whether the user has existing notes. Proceed directly to Step 3.

---

### Step 3: Interview — Q1 (Problem)

**Skip condition:** `session.completeness.problem >= 3 AND session.notes_partial.problem == false`

**Targeted follow-up condition:** `session.completeness.problem >= 3 AND session.notes_partial.problem == true`
→ In this case, skip the full question and ask only:
  - Korean: "문제 부분을 좀 더 구체적으로 설명해 주시겠어요? 실제 상황이나 수치가 있으면 카피가 훨씬 강력해집니다."
  - English: "Could you add more detail to the problem you described? A specific scenario or number would make the copy stronger."
  Set `session.notes_partial.problem = false` after handling.

**Ask as plain text output (do NOT call AskUserQuestion tool):**

Korean:
```
이 제품이 해결하는 구체적인 문제는 무엇인가요?

타겟 사용자가 이 문제를 겪는 실제 상황을 설명해주세요.
(예: "매주 월요일 팀 미팅 때마다 누가 무엇을 했는지 파악하느라 30분을 낭비한다")
```

English:
```
What specific problem does this solve?

Describe a real situation where your target user faces this problem.
(e.g., "Every Monday standup, team leads spend 30 minutes just figuring out what everyone did last week")
```

Wait for the user's free-form response.

**Completeness scoring (run after each answer):**

```pseudocode
function scoreCompleteness(answer):
  score = 5
  words = count_words(answer)

  if words < 10:  score = min(score, 1)
  elif words < 20: score = min(score, 2)

  generic_terms = ["better", "easier", "faster", "좋아", "편리", "빠르게",
                   "improve", "solve problems", "helps with", "도움이"]
  if all_words_are_generic(answer, generic_terms):
    score = min(score, 2)

  specificity_markers = ["every", "매일", "매주", "minutes", "분", "hours",
                         "시간", "dollars", "원", "percent", "%", "~할 때"]
  if contains_any(answer, specificity_markers):
    score = min(score + 1, 5)

  if has_concrete_example(answer):  // quotes, named tools, specific scenarios
    score = min(score + 1, 5)

  return score
```

**If score < 3 — ask ONE follow-up as plain text:**

Korean: "좀 더 구체적으로 알려주세요. 실제 상황이나 수치를 포함해주시면 더 강력한 카피를 만들 수 있습니다."

English: "Could you be more specific? A concrete scenario or number (e.g., '2 hours wasted', '30% conversion drop') will make the copy much stronger."

Wait for response. Re-score.

**If still score < 3 after follow-up:** Accept the answer and append `[TODO: add specific scenario with real numbers or situation]`. Do not loop again.

```pseudocode
session.answers.problem = answer  // including [TODO] if applicable
session.completeness.problem = scoreCompleteness(answer)
session.notes_partial.problem = false  // clear partial flag after interview step
```

---

### Step 4: Interview — Q2 (Solution / Differentiation)

**Skip condition:** `session.completeness.solution >= 3 AND session.notes_partial.solution == false`

**Targeted follow-up condition:** `session.completeness.solution >= 3 AND session.notes_partial.solution == true`
→ Skip the full question. Ask only (always include the hint regardless):
  - Korean: "차별점을 더 구체적으로 설명해 주실 수 있나요? 힌트: 'X와 달리, 제 제품은 Y를 Z 방식으로 합니다.'"
  - English: "Can you clarify the differentiation? Hint: 'Unlike X, my product does Y by Z.'"
  Set `session.notes_partial.solution = false` after handling.

This is the highest-friction question for most users. Always include the hint example regardless of what the user has provided.

**Ask as plain text:**

Korean:
```
한 문장으로 솔루션을 설명해주세요. 기존 대안과 비교했을 때 무엇이 다른가요?

힌트: "X와 달리, 제 제품은 Y를 Z 방식으로 합니다."
예시: "Notion과 달리, 제 앱은 개발자의 GitHub 활동에서 자동으로 주간 리포트를 생성합니다."
```

English:
```
In one sentence: what makes this different from existing alternatives?

Hint: "Unlike X, my product does Y by Z."
Example: "Unlike Notion, my app automatically generates weekly reports from your team's GitHub activity — no manual updates needed."
```

**If score < 3 — ask ONE follow-up:**

Korean: "기존에 사람들이 어떻게 이 문제를 해결하고 있나요? 그리고 당신의 제품은 그것과 어떻게 다른가요?"

English: "How are people currently solving this problem? And what does your product do differently or better?"

**If still < 3:** Accept, append `[TODO: clarify differentiation vs existing alternatives]`.

```pseudocode
session.answers.solution = answer
session.completeness.solution = scoreCompleteness(answer)
session.notes_partial.solution = false
```

---

### Step 5: Interview — Q3 (Target User)

**Skip condition:** `session.completeness.target >= 3 AND session.notes_partial.target == false`

**Targeted follow-up condition:** `session.completeness.target >= 3 AND session.notes_partial.target == true`
→ Ask only:
  - Korean: "타겟 사용자의 역할과 현재 사용하는 도구를 더 구체적으로 설명해 주시겠어요?"
  - English: "Could you describe your target user's role and what specific tools they currently use?"
  Set `session.notes_partial.target = false` after handling.

**Ask as plain text:**

Korean:
```
주요 타겟 사용자는 누구인가요?

역할, 현재 사용하는 도구나 방법, 그리고 가장 큰 불편함을 구체적으로 설명해주세요.
```

English:
```
Who is your primary user?

Describe their role, what tools or methods they currently use, and their biggest pain point.
```

**If score < 3 — ask ONE follow-up:**

Korean: "그 사람들이 지금 이 문제를 어떻게 해결하고 있나요? 어떤 도구나 방법을 쓰나요?"

English: "What do they use right now to handle this? Any specific tools or workarounds you've observed?"

**If still < 3:** Accept, append `[TODO: define target user role and current tools more clearly]`.

```pseudocode
session.answers.target = answer
session.completeness.target = scoreCompleteness(answer)
session.notes_partial.target = false
```

---

### Step 6: Interview — Q4 (MVP Scope)

**Skip condition:** `session.completeness.mvp_scope >= 3 AND session.notes_partial.mvp_scope == false`

**Targeted follow-up condition:** `session.completeness.mvp_scope >= 3 AND session.notes_partial.mvp_scope == true`
→ Ask only:
  - Korean: "MVP 핵심 기능 3가지를 더 구체적으로 설명해 주시겠어요?"
  - English: "Could you list the 3 must-have MVP features more explicitly?"
  Set `session.notes_partial.mvp_scope = false` after handling.

**Ask as plain text:**

Korean:
```
MVP에서 반드시 있어야 하는 핵심 기능 3가지는 무엇인가요?

그리고 나중에 v2에서 추가해도 괜찮은 기능은 무엇인가요?
```

English:
```
What are the 3 must-have features for your MVP?

What can wait until v2?
```

**If score < 3 — ask ONE follow-up:**

Korean: "사용자가 처음 방문에서 반드시 경험해야 하는 핵심 가치가 무엇인가요? 그것을 가능하게 하는 기능은?"

English: "What's the single core value a first-time user must experience? What feature delivers that experience?"

**If still < 3:** Accept, append `[TODO: define 3 MVP features explicitly]`.

```pseudocode
session.answers.mvp_scope = answer
session.completeness.mvp_scope = scoreCompleteness(answer)
session.notes_partial.mvp_scope = false
```

---

### Step 7: Product Name and Slug

After all 4 answers are collected, derive or confirm the product name.

```pseudocode
candidates = extractProductNames(session.answers)
// Look for: capitalized proper nouns, quoted names, "called X", "named X", "제품명", "앱 이름"

if candidates is not empty:
  // Confirm as plain text — then WAIT for user response before continuing
  if session.language == "ko":
    output "제품 이름이 '{candidates[0]}'인가요? 다른 이름이 있다면 알려주세요."
  else:
    output "Is the product name '{candidates[0]}'? Let me know if you have a different name."

else:
  // Ask directly as plain text — then WAIT for user response before continuing
  if session.language == "ko":
    output "제품 이름이 무엇인가요? (예: TaskBot, DailySpark, CodePulse)"
  else:
    output "What's the product name? (e.g., TaskBot, DailySpark, CodePulse)"

// STOP HERE. Do not proceed to Step 8 until user provides a name response.
session.product_name = user_response  // Accept any response as the confirmed name

// Generate slug — handles non-ASCII (Korean) names
function generateSlug(name):
  // If name contains non-ASCII characters (e.g. Korean), prompt for Latin slug first
  if contains_non_ascii(name):
    if session.language == "ko":
      output "영문 파일 경로용 슬러그를 알려주세요. (예: my-product, task-bot)"
    else:
      output "Please provide a Latin slug for the file path (e.g., my-product, task-bot)"
    name = wait_for_user_response()

  slug = name.toLowerCase()
  slug = replace(/[^a-z0-9\s-]/g, "")  // remove special chars
  slug = replace(/\s+/g, "-")            // spaces to hyphens
  slug = replace(/-+/g, "-")             // collapse multiple hyphens
  slug = trim("-")                        // trim leading/trailing hyphens

  // Secondary fallback: if slug is empty or too short after sanitization
  if slug is empty or slug.length < 2:
    if session.language == "ko":
      output "유효한 파일 이름을 생성할 수 없습니다. 출력 폴더 이름을 영문으로 알려주세요. (예: my-product)"
    else:
      output "Could not generate a valid file name. What should the output folder be called? (e.g., my-product)"
    slug = wait_for_user_response().toLowerCase().replace(/[^a-z0-9-]/g, "-")

  return slug

session.product_slug = generateSlug(session.product_name)
```

---

### Step 8: Generate All 5 Content Sections

Generate all content using the interview answers. This is the core synthesis step.

**CRITICAL GENERATION RULES:**
- Use specific details from the user's answers — never produce generic placeholder copy
- Mirror the output language: Korean interview → Korean output, English → English
- Every headline, feature name, and FAQ must reference actual problem/solution/target details from answers
- If any answer has a [TODO] marker, use it as a placeholder in that section but generate all other sections fully
- Do not use hype words: "revolutionary", "game-changing", "disruptive", "cutting-edge"

**Section 1: Landing Page Copy**

Generate using these rules for each element:

```
HEADLINE:
  - Lead with the outcome or problem eliminated, not the product feature
  - Use specific numbers from Q1 if available (e.g., "30 minutes → 30 seconds")
  - Max 10 words
  - Korean example: "팀 스탠드업 준비에 30분? 이제 30초면 됩니다"
  - English example: "Stop wasting 2 hours every Monday on team standups"

SUBHEADLINE:
  - Name the target user (from Q3) and the specific mechanism (from Q2)
  - One sentence, 20-30 words
  - English: "{ProductName} connects to GitHub and automatically generates your team's weekly report before the meeting starts."

FEATURE 1 (derived from MVP must-have #1):
  - Lead with a benefit, not a label
  - 2 sentences: what it does + specific value it delivers
  - Use Q1 context to make it resonate with the problem

FEATURE 2 (derived from MVP must-have #2):
  - Same structure

FEATURE 3 (derived from MVP must-have #3):
  - Same structure

CTA:
  - Button text: action verb + outcome (not just "Submit" or "Sign Up")
  - Examples: "Get Early Access", "Join the Waitlist", "Start Free Today"
  - Subtext: "No credit card required. Join [X] builders already on the waitlist."

FAQ 1: Objection about ROI or time-to-value
FAQ 2: Objection about switching from current solution
FAQ 3: Question about data privacy or security
FAQ 4: Question about who this is best suited for
FAQ 5: Question about launch timeline or current status
```

**Section 2: Indie Hackers Post**

Tone guide: builder-to-builder, authentic, honest about current status, metrics-forward.

```
TITLE:
  - Format options: "Show IH: [product]", "I built [X] because [problem]", "After [situation], I made [product]"
  - Avoid: "Excited to announce", "Launching today", "Check out my new app"
  - Example: "Show IH: I got tired of spending 45 minutes every Monday prepping standups, so I built TaskBot"

BODY structure:
  Paragraph 1 — Hook on the problem (personal or observed)
    Write in first person. Specific situation, specific frustration.
    Reference Q1 answer directly.

  Paragraph 2 — What I built
    One clear description of the product. Reference Q2 differentiation.
    What it does in plain language, not marketing speak.

  Paragraph 3 — How it works (3 bullet points)
    Three specific capabilities from Q4 MVP features.
    Each bullet: one concrete action or output.

  Paragraph 4 — Honest current status
    "This is in beta / I'm validating the idea / X people are testing it"
    Number of users, stage of development, what's working.

  Closing — Specific community ask
    "Would love feedback from [target user from Q3]"
    "What's your current solution to this?"
    "Link in profile / comments if you want to check it out"
```

**Section 3: Reddit r/SideProject Post**

Tone guide: casual, value-first, no hard sell, community-aware. Reddit rejects overt marketing.

```
TITLE:
  - Format: "I built [X] for [target user] — [one-line value]"
    OR: "After [doing something painful] manually for [time], I built [X]"
  - Keep under 100 characters
  - Example: "I built a tool that turns GitHub activity into standup reports — no more manual updates"

BODY:
  2-3 sentences: problem hook → what you built → one differentiator
  Casual, human language. Imagine you're telling a friend.
  Reference Q3 target user and Q1 problem.

  Optional: 3-bullet feature list if the product has distinct capabilities worth listing

  Closing (1-2 sentences):
    Honest ask. "Curious if anyone else has dealt with this problem."
    "Link in comments if interested" (follow subreddit rules on self-promotion)
```

**Section 4: Email Sequence**

**Welcome Email:**

```
SUBJECT:
  - Avoid: "Welcome to {Product}!", "You're in!", "Confirmation"
  - Use: Personal, specific, references what they signed up for
  - Example: "Your early access to TaskBot — here's what happens next"

PREVIEW TEXT:
  - 1 sentence that teases the email body without repeating the subject line
  - Keep under 90 characters (email clients truncate longer preview text)
  - Do NOT start with "Hi", "Hello", or any greeting
  - Reveal a benefit or next step — not a summary of the subject line
  - English example: "Here's what you unlocked and what happens next."
  - Korean example: "어떤 기능이 포함됐는지, 다음 단계가 무엇인지 확인해보세요."

BODY:
  Opening (2 sentences max):
    Acknowledge what they signed up for. Reference the specific problem from Q1.
    Make them feel understood, not processed.
    Example: "You signed up because prepping standups eats too much time. Same thing drove me to build this."

  Feature list (3 bullets from Q4 MVP must-haves):
    Brief, benefit-focused. Not feature labels.

  Honest status paragraph:
    Where the product stands. Beta count, stage, what's shipping next.
    Example: "I'm currently in private beta with 18 people. Your feedback will directly shape v1."

  ONE clear next step:
    Make it easy. Low friction.
    Example: "Reply to this email: what's your biggest standup headache right now?"

  Signature:
    First name only. "— [Founder first name], founder of {Product}"
```

**Day 3 Follow-up Email:**

```
SUBJECT:
  - Curiosity or question-based. Reference the original pain point.
  - Example: "Did you try TaskBot yet? (quick question)"
  - Korean: "TaskBot 써보셨나요? (짧은 질문 하나)"

PREVIEW TEXT:
  - 1 sentence that creates curiosity without spoiling the email content
  - Keep under 90 characters
  - Frame as a question or tease a specific value reveal
  - Do NOT start with "Hi", "Hello", or any greeting
  - English example: "A quick check-in — and one thing we noticed this week."
  - Korean example: "이번 주 베타 사용자들에게서 들은 이야기 하나 공유하고 싶어요."

BODY:
  Opening (2 sentences):
    Reference original problem without repeating the full context.
    Create a natural connection to 3 days ago.

  Middle (2-3 sentences):
    One new thing: a specific insight, a user story from beta, or a product update.
    Something that adds value, not just another "reminder".

  Social proof element (if applicable):
    "Three people this week told me [specific insight about the problem]."
    Skip if no real data is available — do not fabricate.

  Soft CTA (low friction):
    Check-in link OR a simple reply question.
    Example: "If you haven't checked in yet: [link]"
    OR: "Quick yes/no: is [problem] something you deal with weekly?"

  P.S. — Founding Plan teaser:
    "P.S. We're offering 50% off for founding members — only 20 spots. Details: [link]"
```

**Section 5: Founding Plan Pre-Sale Offer**

```
HEADLINE:
  - Urgency + exclusivity. Specific number of spots.
  - English: "Join as a Founding Member — 50% Off the Regular Price, Forever"
  - Korean: "Founding Plan: 평생 50% 할인 — 딱 20자리"

BODY (1 paragraph):
  Who this is for (reference Q3 target user).
  What core value they unlock (reference Q2 differentiation).
  Why founding members get special access.

WHAT YOU GET (list):
  - {ProductName} — [core value in 5 words]
  - 50% off the regular price, permanently locked in
  - Direct line to the founder — your feedback shapes the product
  - Priority access to every new feature before general release

PRICING:
  Regular price: $[XX]/month
  Founding Member price: $[XX]/month (billed forever at this rate)
  [Use [TODO: set pricing] if user hasn't mentioned price]

SCARCITY (honest):
  Specific number. If real number not known, use 20 as a default.
  "Limiting to 20 founding members to give each one personal attention."
  "X spots taken. Y remaining." [Use [TODO: update spot count] if unknown]

CTA:
  "Claim Your Founding Member Spot"
  Subtext: "Secure your price now. Cancel anytime. No long-term commitment."

OBJECTION HANDLER:
  "Still validating? Reserve your spot now — you won't be charged until launch.
   I'll send a 48-hour reminder before the first payment."
```

---

### Step 9: Assemble Full Output Document

Combine all sections using the output template structure.

```pseudocode
// Get current timestamp with error handling
try:
  run_bash("date '+%Y-%m-%d %H:%M'") → generated_at
  if bash_exit_code != 0:
    generated_at = "unknown"
except:
  generated_at = "unknown"

session.generated_at = generated_at

// Load template using absolute path resolution
// The template lives alongside this skill in the plugin directory.
// Resolve absolute path at runtime: find the plugin root relative to cwd,
// or use the known install path ~/.claude/skills/launch-kit/
//
// Priority order:
//   1. Read("{plugin_root}/../../templates/launch-kit-output.md")
//      where plugin_root is derived from the known symlink target, e.g.
//      run_bash("readlink -f ~/.claude/skills/launch-kit 2>/dev/null || echo ''") → plugin_root
//   2. Inline template (embedded below — use if file read fails, silently)

template_loaded = false

try:
  run_bash("readlink -f ~/.claude/skills/launch-kit 2>/dev/null || echo ''") → plugin_root
  if plugin_root is not empty:
    template = Read("{plugin_root}/../../templates/launch-kit-output.md")
    template_loaded = true
except:
  pass

if not template_loaded:
  // Use inline embedded structure — no warning shown to user, silently fall back
  template = INLINE_TEMPLATE  // see INLINE_TEMPLATE_STRUCTURE below

// Populate and write
document = populate_template(template, {
  PRODUCT_NAME: session.product_name,
  PRODUCT_SLUG: session.product_slug,
  GENERATED_AT: session.generated_at,
  LANGUAGE: session.language,
  PROBLEM_SUMMARY: first_20_words(session.answers.problem),
  SOLUTION_SUMMARY: first_20_words(session.answers.solution),
  TARGET_SUMMARY: first_20_words(session.answers.target),
  MVP_SUMMARY: first_20_words(session.answers.mvp_scope),
  PROBLEM_COMPLETENESS: session.completeness.problem,
  SOLUTION_COMPLETENESS: session.completeness.solution,
  TARGET_COMPLETENESS: session.completeness.target,
  MVP_COMPLETENESS: session.completeness.mvp_scope,
  // ... all generated section content from Step 8
})
```

**Inline embedded template structure** (used silently when template file is unavailable):

Generate the document with these sections in order:
1. HTML comment header with metadata (plugin version 1.1.0, product, generated timestamp, completeness scores)
2. `# {PRODUCT_NAME} — Launch Kit` heading with generated_at note and plugin version
3. Interview Summary table (4 rows: problem, solution, target, mvp with completeness scores)
4. Section 1 — Landing Page Copy (headline, subheadline, 3 features, CTA, 5 FAQs)
5. Section 2 — Indie Hackers Post (title + body)
6. Section 3 — Reddit r/SideProject Post (title + body)
7. Section 4 — Email Sequence (Email 1 Welcome: subject/preview text/body; Email 2 Day 3: subject/preview text/body)
8. Section 5 — Founding Plan Pre-Sale Offer (headline, intro, benefits, pricing, scarcity, CTA, objection handler)
9. Next Steps Checklist (immediate / this week / after 10+ signups / after 20+ signups)
10. Footer attribution (launch-kit link, planning-interview suggestion)

---

### Step 10: Save to File

```pseudocode
output_dir = f"{cwd}/{session.product_slug}"
output_file = f"{output_dir}/launch-kit.md"

// Check for existing file (avoid overwrite)
if file_exists(output_file):
  try:
    run_bash("date '+%Y%m%d-%H%M%S'") → timestamp
    if bash_exit_code != 0:
      timestamp = "backup"
  except:
    timestamp = "backup"
  output_file = f"{output_dir}/launch-kit-{timestamp}.md"

// Create directory and write
run_bash(f"mkdir -p {output_dir}")
Write(output_file, document)

session.output_path = output_file
```

**Fallback chain if Write fails:**

```pseudocode
// Fallback 1: Desktop
try:
  desktop_path = f"~/Desktop/{session.product_slug}/launch-kit.md"
  run_bash(f"mkdir -p ~/Desktop/{session.product_slug}")
  Write(desktop_path, document)
  session.output_path = desktop_path

// Fallback 2: Display in chat
except:
  warn_user("Could not write to filesystem. Displaying full content here:")
  output(document)
```

---

### Step 11: Completion Confirmation

After saving, display a structured completion message.

Korean:
```
launch-kit.md 생성 완료!

저장 위치: {session.output_path}

생성된 콘텐츠:
  - 랜딩페이지 카피 (헤드라인, 서브헤드라인, 기능 3개, CTA, FAQ 5개)
  - Indie Hackers 포스트
  - Reddit r/SideProject 포스트
  - 이메일 시퀀스 (웰컴 + D+3 팔로업)
  - Founding Plan 선판매 오퍼

다음 단계:
1. {session.output_path} 파일을 열어 [TODO] 항목을 채우세요
2. Carrd 또는 Typedream으로 랜딩페이지를 만드세요
3. Indie Hackers와 Reddit에 포스트를 게시하세요
4. Kit 또는 Mailchimp로 이메일 시퀀스를 설정하세요
5. 시장 반응을 확인한 후 `planning-interview`로 PRD를 작성하세요
```

English:
```
launch-kit.md generated!

Saved to: {session.output_path}

Generated content:
  - Landing page copy (headline, subheadline, 3 features, CTA, 5 FAQs)
  - Indie Hackers post
  - Reddit r/SideProject post
  - Email sequence (welcome + day 3 follow-up)
  - Founding Plan pre-sale offer

Next Steps:
1. Open {session.output_path} and fill in any [TODO] items
2. Build your landing page with Carrd or Typedream
3. Post to Indie Hackers and Reddit
4. Set up your email sequence in Kit or Mailchimp
5. After validating market response, run `planning-interview` to create your PRD
```

---

## Error Handling

| Step | Error Condition | Detection Method | Fallback Strategy |
|------|-----------------|------------------|-------------------|
| Step 1 | Language detection ambiguous | No Korean markers found | Default to "en" |
| Step 1 | Mixed-language input (Korean trigger + English answers) | Korean markers in trigger, English text in answers | Use trigger language for all output; accept answer content as-is |
| Step 2 | Inline notes extraction yields nothing | All extracted fields null | Treat as Case B, run full 4-question interview |
| Step 2 | Notes present but fewer than 50 words | word_count < 50 | Skip extraction, run full interview |
| Step 2 | Field extracted but score < 3 | scoreCompleteness < 3 after extraction | Set notes_partial[field] = true; ask targeted follow-up only |
| Step 2 | Field extracted but word count <= 15 | word_count <= 15 | Set notes_partial[field] = true; ask targeted follow-up only |
| Step 3-6 | User answers "I don't know" | Answer matches "모름", "idk", "not sure", "don't know" | Mark [TODO], proceed to next question without follow-up |
| Step 3-6 | User gives fewer than 5 words | word_count < 5 | Treat as vague (score = 1), ask one follow-up |
| Step 3-6 | Follow-up answer is still vague | scoreCompleteness < 3 | Accept, append [TODO] with specific guidance, continue |
| Step 3-6 | User skips question explicitly | Answer is "pass", "skip", "건너뛰기", "넘어가" | Mark [TODO], proceed without follow-up |
| Step 3-6 | notes_partial flag is true | notes_partial[field] == true | Ask targeted follow-up only, not full question |
| Step 7 | Cannot extract product name from answers | extractProductNames returns empty | Ask as plain text, wait for response, accept any reply |
| Step 7 | Product name is Korean/non-ASCII | contains_non_ascii(name) returns true | Prompt user for Latin slug explicitly |
| Step 7 | Product name slug is empty after sanitization | slug.length < 2 | Ask user for folder name directly |
| Step 8 | One or more answers contain [TODO] | answers field contains "[TODO" | Generate all other sections fully; use placeholder in affected sections |
| Step 8 | All 4 answers are [TODO] | session.completeness all 0 | Generate document with prominent warning at top; use generic placeholders |
| Step 9 | Template file not found | Read fails (symlink not resolved or file missing) | Use inline embedded structure silently; no user-facing warning |
| Step 9 | date bash call fails | exit code non-zero or exception | Set generated_at = "unknown" and continue |
| Step 10 | Output directory creation fails | mkdir exit code non-zero | Try ~/Desktop/{slug}/launch-kit.md as fallback |
| Step 10 | Write fails at Desktop path | Write tool returns error | Display full document as code block in chat |
| Step 10 | launch-kit.md already exists in directory | File exists check | Append timestamp: launch-kit-{YYYYMMDD-HHMMSS}.md; if date fails use "backup" |
| Step 11 | Session language is null | language field is null | Default to "en" for completion message |

---

## Quick Reference

### Interview Flow

```
Trigger detected
    └── Language detected (ko / en)
    └── Notes import check (trigger > 50 words?)
        ├── Yes → Extract → notes_partial flags set
        │   ├── score >= 3, partial = false → Skip question
        │   ├── score >= 3, partial = true  → Targeted follow-up only
        │   └── Not extracted               → Full question
        └── No  → Full 4-question interview

Q1: Problem — specific real situation (plain text, no tool call)
Q2: Solution — differentiation + hint example (plain text)
Q3: Target — role + tools + pain (plain text)
Q4: MVP Scope — 3 must-haves + v2 deferred (plain text)

Each Q: score answer (1-5)
         score < 3 → ONE follow-up (plain text)
         still < 3 → accept + [TODO]

Confirm product name → WAIT for response → generate slug (Latin slug prompt for Korean names)

Generate 5 sections (simultaneous synthesis):
  1. Landing page copy
  2. Indie Hackers post
  3. Reddit r/SideProject post
  4. Email sequence (welcome + D+3)
  5. Founding Plan pre-sale offer

Save → {cwd}/{product-slug}/launch-kit.md
Show next steps → suggest planning-interview
```

### Completeness Score Reference

| Score | Meaning | Action |
|-------|---------|--------|
| 5 | Specific, concrete, with examples or metrics | Use directly |
| 4 | Good detail, minor gaps | Use directly |
| 3 | Acceptable, could be stronger | Use with light enhancement |
| 2 | Vague or too short | Ask ONE follow-up |
| 1 | Generic or unusably brief | Ask ONE follow-up; if still 1, mark [TODO] |

### Output File Location

```
{cwd}/{product-slug}/launch-kit.md

Examples:
./taskbot/launch-kit.md
./daily-spark/launch-kit.md
./codepulse-ai/launch-kit.md
```

### Tone Reference by Section

| Section | Tone | Avoid |
|---------|------|-------|
| Landing page | Clear, benefit-first, specific | Jargon, hype words ("revolutionary", "game-changing") |
| Indie Hackers | Builder-to-builder, honest, metrics | Corporate language, "excited to announce" |
| Reddit | Casual, value-first, human | Hard sell, excessive links, hype |
| Email welcome | Personal, direct, curious | Newsletter tone, "Dear Customer" |
| Email D+3 | Conversational, soft nudge | Pushy, spam-like urgency |
| Founding Plan | Exclusive but honest, specific price | Fake scarcity, vague benefits |