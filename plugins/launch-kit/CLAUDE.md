# CLAUDE.md — launch-kit Developer Guide

Technical documentation for developers and maintainers of the launch-kit plugin.

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Architecture Decisions](#architecture-decisions)
3. [Execution Flow Details](#execution-flow-details)
4. [Content Generation Logic](#content-generation-logic)
5. [Testing Checklist](#testing-checklist)
6. [Customization Guide](#customization-guide)
7. [Debugging Tips](#debugging-tips)
8. [Future Enhancements](#future-enhancements)

---

## Directory Structure

```
plugins/launch-kit/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata, keywords, author, skills/triggers registry
├── commands/
│   └── launch-kit/
│       └── launch-kit.md        # /launch-kit slash command definition
├── skills/
│   └── launch-kit/
│       └── SKILL.md             # Full execution algorithm (primary source of truth)
├── templates/
│   └── launch-kit-output.md     # Output document template with placeholders
├── README.md                    # User-facing documentation
├── CLAUDE.md                    # Developer guide (this file)
└── IDEA.md                      # Original concept document (preserved for reference)
```

### Installed locations (via symlinks)

```
~/.claude/skills/launch-kit       → plugins/launch-kit/skills/launch-kit/
~/.claude/commands/launch-kit     → plugins/launch-kit/commands/launch-kit/
```

**Install with npm run link (monorepo):**

```bash
cd ~/Documents/Projects/claude-ai-engineering
npm run link
```

**Install manually (standalone):**

```bash
ln -s /path/to/plugins/launch-kit/skills/launch-kit ~/.claude/skills/launch-kit
ln -s /path/to/plugins/launch-kit/commands/launch-kit ~/.claude/commands/launch-kit
```

---

## Architecture Decisions

### Why Simple Skill (not multi-agent)

The mission brief specifies "Simple Skill — NO agents". The reasoning is sound:

1. The execution is **sequential by nature**: interview must complete before generation can begin
2. **No parallelization benefit**: all 4 interview answers are needed before any generation starts
3. **AskUserQuestion is incompatible**: the tool requires structured options (2-4 choices). Free-form interview questions must be output as plain text and await user response organically
4. **Single output file**: no coordination between parallel content generators needed
5. **State is simple**: 4 answer fields + completeness scores + notes_partial flags — no need for agent context passing

The content generation in Step 8 generates all 5 sections in a single synthesis pass, which is efficient without parallelization.

### When AskUserQuestion IS Appropriate

`AskUserQuestion` requires an `options[]` array with 2-4 structured choices. It is NOT used for interview questions Q1-Q4 (those are free-form). However, it IS the right tool for binary or multi-choice decisions within the skill, such as:

- Confirming a language selection when detection is ambiguous: `["Continue in English", "Switch to Korean"]`
- Selecting an output mode if revision mode is implemented: `["Generate new", "Update existing file"]`
- Confirming overwrite behavior: `["Save as new file with timestamp", "Overwrite existing"]`

Using `AskUserQuestion` for open-ended interview questions would force users into pre-written options, defeating the specificity goal.

### Completeness Scoring: Why 1-5

The 1-5 scoring system (borrowed from planning-interview) serves a specific purpose: it gates follow-up questions.

Design contract:
- **Score >= 3**: Answer is usable. Proceed.
- **Score < 3**: Answer is too vague for specific copy generation. Ask one targeted follow-up.
- **Score < 3 after follow-up**: Accept with [TODO] marker. Do not loop — user frustration is worse than a placeholder.

One follow-up maximum is a deliberate design constraint. The goal is getting to output, not perfect interviews.

### Notes Import: Why >50 Words

50 words is calibrated as the threshold between "casual mention" and "structured notes." Below 50 words, extraction would likely pick up incomplete fragments. Above 50 words, there's usually enough to extract at least 2-3 of the 4 answers meaningfully.

This threshold can be adjusted in SKILL.md Step 2 if empirical use shows a different number works better.

### Notes Import: Partial Extraction and the notes_partial Flag

When notes are imported, individual fields may be extracted but with low completeness (score < 3) or with very short text (<=15 words). In these cases, running the full interview question would feel redundant and confusing to the user — they already provided context.

The `notes_partial` flag per field handles this:
- `notes_partial[field] = true` → ask a targeted follow-up only ("Could you add more detail to X?")
- `notes_partial[field] = false AND score >= 3` → skip the question entirely
- field not extracted at all → run the full question

This three-tier routing avoids both redundancy (re-asking something already answered) and vagueness (accepting a sub-threshold answer without any follow-up).

**Extraction Summary Transparency:** The show_extraction_summary() call in Step 2 surfaces partial fields explicitly. Fields marked notes_partial=true display "(partial — follow-up question coming)" inline in the summary, so the user understands why additional questions will be asked for those fields. The reason is also provided: "under 15 words" or "score < 3".

### Slug Generation: Korean and Non-ASCII Names

Product names containing Korean or other non-ASCII characters will produce empty slugs after ASCII sanitization. The skill handles this explicitly:

1. After the user confirms the product name, check `contains_non_ascii(name)`
2. If true, prompt for a Latin slug: "영문 파일 경로용 슬러그를 알려주세요. (예: my-product)"
3. Apply standard slug sanitization to the Latin input
4. If the result is still empty or too short (< 2 chars), ask again with a specific fallback prompt

This avoids silent failures where the output directory would be named "" or "-".

### Language Detection: Marker-Based

Language is detected by presence of Korean markers in the trigger message, not by a language detection API. This is:
- Fast (no network call)
- Simple to maintain
- Sufficient for the two supported languages (Korean and English)

If a user writes in Korean but forgets to use a Korean trigger, they can re-run with a Korean trigger phrase. Only Korean and English output are supported; other trigger languages default to English.

### Template Resolution: Symlink-Aware

Step 9 resolves the template path using `readlink -f ~/.claude/skills/launch-kit` to find the absolute symlink target, then navigates to the plugin root to load the template. This is necessary because Claude Code's cwd is the user's project directory, not the plugin directory. A relative path like `templates/launch-kit-output.md` would never resolve after symlink install. If template resolution fails for any reason, the skill falls back silently to the inline template structure — no user-facing warning is shown.

---

## Execution Flow Details

### Session State Object

```javascript
session = {
  language: "en" | "ko",           // Set in Step 1, never changes
  product_name: null,              // Set in Step 7
  product_slug: null,              // Derived from product_name in Step 7
  answers: {
    problem: null,                 // Q1 final answer (possibly with [TODO])
    solution: null,                // Q2 final answer
    target: null,                  // Q3 final answer
    mvp_scope: null                // Q4 final answer
  },
  completeness: {
    problem: 0,                    // 1-5 score from scoreCompleteness()
    solution: 0,
    target: 0,
    mvp_scope: 0
  },
  notes_imported: false,           // True if inline notes were extracted
  notes_partial: {                 // True if field was extracted but needs targeted follow-up
    problem: false,                // Set true when: extracted word_count <= 15, or score < 3
    solution: false,
    target: false,
    mvp_scope: false
  },
  output_path: null,               // Set in Step 10 after file is saved
  generated_at: null               // Set in Step 9 from `date '+%Y-%m-%d %H:%M'`
}
```

### Completeness Scoring Algorithm

```
scoreCompleteness(answer) → integer 1-5

Input: string
Output: integer 1-5

1. Start at score = 5
2. Apply word count penalty:
   - words < 10: score = min(score, 1)
   - words < 20: score = min(score, 2)
3. Apply generic terms penalty:
   - If answer contains only generic/vague terms (better, easier, faster, etc.)
     and lacks specific examples → score = min(score, 2)
4. Apply specificity bonus:
   - If answer contains numbers, timeframes, named tools, quoted scenarios → score = min(score + 1, 5)
5. Apply example bonus:
   - If answer has a concrete example, scenario, or real situation → score = min(score + 1, 5)
6. Return score
```

### Q2 Special Handling

Q2 (differentiation) is the question with the highest user drop-off rate. Two design decisions address this:

1. **Always show the hint example** — even if notes were imported and Q2 is being re-asked for more detail
2. **Follow-up is specifically about current alternatives** — "How are people currently solving this?" bridges toward a differentiation answer naturally

### Slug Generation Rules

```
input: product_name (any string)

steps:
  0. If name contains non-ASCII characters → prompt user for Latin slug first
  1. lowercase
  2. remove non-alphanumeric chars except spaces and hyphens
  3. replace consecutive spaces with single hyphen
  4. replace consecutive hyphens with single hyphen
  5. trim leading/trailing hyphens
  6. If result is empty or length < 2 → ask user for folder name

examples:
  "TaskBot" → "taskbot"
  "Task Bot 2.0" → "task-bot-20"
  "CodePulse AI" → "codepulse-ai"
  "My SaaS App!" → "my-saas-app"
  "태스크봇" → [prompt for Latin slug] → user types "task-bot" → "task-bot"
```

### date Bash Call Error Handling

Steps 9 and 10 both call `date` via Bash. Both are wrapped in try/except:

```pseudocode
// Step 9: timestamp for document header
try:
  run_bash("date '+%Y-%m-%d %H:%M'") → generated_at
  if bash_exit_code != 0:
    generated_at = "unknown"
except:
  generated_at = "unknown"

// Step 10: timestamp for duplicate filename
try:
  run_bash("date '+%Y%m%d-%H%M%S'") → timestamp
  if bash_exit_code != 0:
    timestamp = "backup"
except:
  timestamp = "backup"
```

The skill continues normally in all cases. An "unknown" timestamp or "backup" filename suffix is a cosmetic degradation, not a blocker.

### Inline Template Structure (INLINE_TEMPLATE_STRUCTURE)

When `templates/launch-kit-output.md` is not found, Step 9 falls back silently to `INLINE_TEMPLATE_STRUCTURE`. This is an ordered list of 10 document sections generated inline:

1. HTML comment header (plugin version 1.1.0, product, generated timestamp, completeness scores)
2. H1 heading + metadata block (generated date, plugin version, [TODO] search note)
3. Interview Summary table (4 rows: Problem, Solution, Target, MVP with completeness scores)
4. Section 1 — Landing Page Copy (Headline, Subheadline, Feature 1-3, CTA, FAQ 1-5)
5. Section 2 — Indie Hackers Post (Title + full body)
6. Section 3 — Reddit r/SideProject Post (Title + body)
7. Section 4 — Email Sequence (Email 1 Welcome: subject/preview text/body; Email 2 Day 3: subject/preview text/body)
8. Section 5 — Founding Plan Pre-Sale Offer (Headline, Intro, Benefits, Pricing, Scarcity, CTA, Objection handler)
9. Next Steps Checklist (Immediate / This week / After 10+ signups / After 20+ signups)
10. Footer attribution (launch-kit link, planning-interview suggestion)

---

## Content Generation Logic

### Section-Specific Writing Rules

Each section has distinct tone requirements. The SKILL.md details these per section. Key rules by section:

**Landing Page Copy**
- Headline: outcome or eliminated problem, NOT a feature description
- Subheadline: {target user} + {specific mechanism} = one sentence
- Features: benefit-first naming, 2 sentences each
- FAQs: objection-handling, not usage help

**Indie Hackers Post**
- Builder identity is essential: write as "I" — a person who felt the problem
- Opening paragraph must NOT start with "Excited to announce" or "Today I'm launching"
- Status section must be honest — vague hype kills IH posts
- Close with a question to the community, not just a link

**Reddit r/SideProject Post**
- Title format: "I built X for Y" or "After doing Z, I built X"
- Body: 2-3 sentences MAX before any feature list
- No hard CTAs — "link in comments" is the Reddit convention
- The post should feel like a conversation, not a product launch

**Email Welcome**
- Subject line: personal, references what they signed up for
- NOT: "Welcome to [Product]!" (this is generic and gets low open rates)
- Preview text: 1 sentence under 90 chars; teases body without repeating subject; no greeting (no "Hi" or "Hello")
- Body: acknowledge their pain from Q1 before explaining the product
- ONE call to action: reply with a question (maximizes responses for learning)

**Email D+3**
- Subject: question or curiosity gap, not reminder
- Preview text: 1 sentence under 90 chars; create curiosity without spoiling the email content; no greeting
- Body adds value (insight, user story, update) — not just "hey, did you forget?"
- P.S. introduces Founding Plan — first mention, low pressure

**Founding Plan**
- Price must be specific — `[TODO: set pricing]` if unknown, but the copy structure must be there
- Scarcity must be honest — defaulting to "20 spots" is acceptable, but note it's a placeholder
- Objection handler addresses the "not ready to pay" objection specifically

### [TODO] Marker Convention

When an answer is too vague or skipped, the generated copy uses markers:
```
[TODO: add specific scenario with real numbers or situation]
[TODO: clarify differentiation vs existing alternatives]
[TODO: define target user role and current tools more clearly]
[TODO: define 3 MVP features explicitly]
[TODO: set pricing]
[TODO: update spot count]
```

Markers follow the format `[TODO: specific action]`. The specificity is intentional — generic `[TODO]` is unhelpful.

---

## Testing Checklist

### Core Functionality Tests

**Test 1: Full English Interview, Fresh Start**

Input: `validate my idea`

Expected flow:
- [ ] Language detected as "en"
- [ ] No notes import (trigger too short)
- [ ] Q1 asked as plain text
- [ ] Q2 asked with hint example included
- [ ] Q3 and Q4 asked
- [ ] Product name confirmed
- [ ] All 5 sections generated
- [ ] File saved to `{cwd}/{slug}/launch-kit.md`
- [ ] Next steps shown with planning-interview mention

Validation:
- Headline does not start with "Introducing" or "Welcome to"
- Indie Hackers title uses "I built" or "Show IH:" format
- Email subject is not "Welcome to [Product]!"
- Email preview text is present and under 90 chars

**Test 2: Korean Trigger, Full Interview**

Input: `아이디어 검증`

Expected:
- [ ] Language detected as "ko"
- [ ] All interview questions output in Korean
- [ ] All 5 sections generated in Korean
- [ ] Next steps displayed in Korean

**Test 3: Inline Notes Import (English)**

Input: `launch-kit I'm building an app for freelancers who hate writing invoices. They currently use Excel or Wave, which is time-consuming and error-prone. The app auto-generates invoices from time tracking data. Must-haves: time tracking integration, invoice template builder, PDF export. V2: payment collection, client portal.`

Expected:
- [ ] word_count > 50 → extraction triggered
- [ ] problem, target, mvp_scope extracted
- [ ] solution missing → only Q2 asked
- [ ] Output generated with 3 pre-filled answers + 1 interview answer

**Test 3b: Partial Notes Extraction**

Input: `launch-kit I'm building a tool for developers. It's faster than Jira. Must-haves: issue tracking, sprint planning. V2: reporting.`

Expected:
- [ ] word_count > 50 → extraction triggered
- [ ] target extracted (score < 3, notes_partial.target = true)
- [ ] solution extracted (score < 3, notes_partial.solution = true)
- [ ] mvp_scope extracted (score >= 3, notes_partial.mvp_scope = false)
- [ ] Extraction summary shows "(partial — follow-up question coming)" next to target and solution fields
- [ ] For target: targeted follow-up asked ("Could you describe your target user's role and what specific tools they currently use?")
- [ ] For solution: targeted follow-up asked with hint ("Can you clarify the differentiation? Hint: 'Unlike X, my product does Y by Z.'")
- [ ] Full Q1 (problem) asked (not extracted)
- [ ] Full Q4 (MVP scope) skipped (score >= 3, partial = false)

**Test 4: Vague Answer Handling**

Input on Q1: `It helps people work better`

Expected:
- [ ] scoreCompleteness < 3
- [ ] Follow-up question asked in plain text
- [ ] If follow-up also vague: [TODO] marker applied, Q2 proceeds

**Test 5: User Skips Questions**

Input: `skip` on Q3

Expected:
- [ ] [TODO: define target user role and current tools more clearly] in output
- [ ] Q4 asked normally
- [ ] File still generated

**Test 6: File Already Exists**

Setup: Run launch-kit twice with same product name

Expected:
- [ ] Second run saves to `launch-kit-{timestamp}.md`
- [ ] Original file not overwritten
- [ ] If date bash call fails: saves to `launch-kit-backup.md`

**Test 7: Write Permission Failure**

Setup: Remove write permission from cwd

Expected:
- [ ] Fallback to ~/Desktop/{slug}/launch-kit.md
- [ ] If Desktop also fails: document displayed in chat

**Test 8: All Answers [TODO] (Edge Case)**

Input: All 4 questions answered with "I don't know"

Expected:
- [ ] All answers marked [TODO]
- [ ] Warning at top of output file
- [ ] Generic placeholder copy generated for all sections
- [ ] Document still saved

**Test 8b: Korean Product Name**

Input: Product name entered as "태스크봇" when prompted

Expected:
- [ ] contains_non_ascii("태스크봇") → true
- [ ] Prompt for Latin slug displayed in Korean: "영문 파일 경로용 슬러그를 알려주세요."
- [ ] User provides "task-bot"
- [ ] Output directory: `./task-bot/launch-kit.md`

**Test 8c: Template File Not Found**

Setup: Remove or rename `templates/launch-kit-output.md`

Expected:
- [ ] readlink -f resolution fails or template Read returns error
- [ ] INLINE_TEMPLATE_STRUCTURE used as fallback silently
- [ ] No user-facing warning message shown
- [ ] Document still generated with all 10 sections in order
- [ ] File saved normally

**Test 8d: date Bash Call Fails (Step 9)**

Setup: Override date command to return exit code 1

Expected:
- [ ] generated_at = "unknown" set
- [ ] Document header shows "unknown" timestamp
- [ ] Output file still generated normally

**Test 8e: date Bash Call Fails (Step 10, duplicate file)**

Setup: File already exists; date command returns exit code 1

Expected:
- [ ] timestamp = "backup"
- [ ] File saved as `launch-kit-backup.md`

### Content Quality Tests

**Test 9: Headline Specificity**

Expected: Headline references a specific outcome from Q1 answer, not a generic benefit.

Failure condition: Headline contains "better", "easier", "faster" without specific context.

**Test 10: Indie Hackers Tone**

Expected: IH post does not contain "excited to announce", "thrilled", "proud to launch".

**Test 11: Language Consistency**

Expected: Korean trigger → 100% Korean output (all 5 sections + next steps).

**Test 12: Email Preview Text**

Expected: Both Welcome and Day 3 emails include preview text fields. Preview text is under 90 chars and does not start with "Hi" or any greeting.

---

## Customization Guide

### Adding a 6th Content Section (e.g., ProductHunt)

1. Add ProductHunt generation rules to SKILL.md Step 8 under a new "Section 6" heading
2. Add placeholders to `templates/launch-kit-output.md`:
   ```
   ## Section 6 — ProductHunt Launch Post

   **Tagline:** {PH_TAGLINE}

   **Description (260 chars):** {PH_DESCRIPTION}
   ```
3. Add section 6 to the INLINE_TEMPLATE_STRUCTURE list in SKILL.md Step 9
4. Add to the Next Steps checklist in the template
5. Update README.md output structure table

### Adjusting Completeness Score Threshold

The threshold of 3 (below which a follow-up is asked) is in SKILL.md Steps 3-6.

To change: edit the condition `if score < 3` in each step's scoring section.

Recommended values:
- `< 2`: Only follow up on extremely vague answers (fewer interruptions)
- `< 3`: Current default (balanced)
- `< 4`: Follow up on most answers (more thorough but more friction)

### Changing the Follow-up Limit

Currently: 1 follow-up maximum per question.

To allow 2 follow-ups: in each step's scoring block, add a second follow-up question if the revised answer is still below threshold.

Warning: more than 1 follow-up per question significantly increases time-to-output and user frustration. Do not add more than 2.

### Modifying the Inline Notes Threshold

The 50-word threshold for notes import is in SKILL.md Step 2:

```pseudocode
if word_count > 50:  // ← change this number
  return content
```

Increasing to 100 words reduces false extractions from casual mentions.
Decreasing to 30 words extracts from shorter notes but may get incomplete answers.

### Modifying the Partial Extraction Threshold

The 15-word threshold for marking a field as partial is in SKILL.md Step 2:

```pseudocode
if word_count > 15:
  // full extraction
else:
  session.notes_partial[field] = true  // ← adjust this threshold
```

### Adding a New Language

1. Add language markers to SKILL.md Step 1 detection logic
2. Add translated versions of all interview questions (Steps 3-6)
3. Add translated extraction summary (Step 2)
4. Add translated completion message (Step 11)
5. Add language to plugin.json keywords and triggers array
6. Update README.md to reflect supported languages

---

## Debugging Tips

### Check Session State

Ask Claude mid-interview: "Show me the current session state for launch-kit"

Expected response:
```json
{
  "language": "en",
  "answers": {
    "problem": "Team leads spend 30 minutes...",
    "solution": null,
    "target": null,
    "mvp_scope": null
  },
  "completeness": {
    "problem": 4,
    "solution": 0,
    "target": 0,
    "mvp_scope": 0
  },
  "notes_partial": {
    "problem": false,
    "solution": false,
    "target": false,
    "mvp_scope": false
  }
}
```

### Common Issues

| Issue | Likely Cause | Debug Step |
|-------|-------------|------------|
| Interview runs but no file saved | Write permission denied | Check cwd permissions; fallback to Desktop |
| Copy is too generic | Vague interview answers | Review answers; look for [TODO] markers |
| Language wrong | Trigger phrase had no Korean markers | Use explicit Korean trigger phrase |
| Q2 hint not shown | Code skipped hint on import | Verify hint is shown even when Q2 is re-asked |
| Notes not extracted | Trigger under 50 words | Add more content inline or run full interview |
| Full question asked despite notes | notes_partial flag not set | Check extraction word count threshold (>15 words) |
| Partial fields not shown in summary | show_extraction_summary skipping them | Check that partial fields display "(partial — follow-up question coming)" |
| Product name not found | Answers don't mention product name | Claude asks directly — just type the name |
| Slug is empty or invalid | Korean/non-ASCII product name | Expected — Claude will prompt for Latin slug |
| Timestamp shows "unknown" | date bash call failed in Step 9 | Cosmetic only; output file still saved normally |
| Duplicate file named "backup" | date bash call failed in Step 10 | Cosmetic only; file still saved |
| Template fallback not triggered | File path check not reaching else branch | Verify INLINE_TEMPLATE_STRUCTURE fallback activates on Read failure |

### Template Placeholder Debugging

If a section in the output is missing content, check:
1. Is the corresponding `session.answers.*` field populated?
2. Does the template have the matching placeholder? (e.g., `{LANDING_HEADLINE}`)
3. Is the completeness score >= 3? If not, a [TODO] may have been inserted instead.
4. For email preview text: check that `{EMAIL_WELCOME_PREVIEW}` and `{EMAIL_D3_PREVIEW}` are present in the template.

---

## Future Enhancements

### Planned Features

| Feature | Priority | Complexity |
|---------|----------|------------|
| ProductHunt launch post as Section 6 | High | Low |
| Twitter/X thread from Indie Hackers post | Medium | Low |
| Carrd layout template generation | Medium | Medium |
| Gumroad/LemonSqueezy founding plan link integration | Low | Medium |
| Revision mode: re-run with updated answers, update specific sections | High | Medium |
| A/B headline variants: generate 3 headline options with rationale | Medium | Low |
| PostHog/Mixpanel event tracking suggestions for landing page | Low | Low |

### Revision Mode Design

When implemented, revision mode would:
1. Read existing `{slug}/launch-kit.md`
2. Extract the interview summary section to reconstruct session state
3. Ask which questions to update (using AskUserQuestion with multi-select options)
4. Re-interview only changed questions
5. Regenerate only affected sections
6. Preserve unchanged sections
7. Save as `launch-kit-v2.md` (preserve original)

### A/B Headline Variants

The Q1 answer typically supports multiple headline angles:
- Problem-focused: "Stop spending X hours on Y"
- Outcome-focused: "Get Y done in Z minutes"
- User-identity: "For [target users] who [specific situation]"

Generating 3 variants would let users A/B test on their landing page.

---

## Versioning

```
Semantic versioning: MAJOR.MINOR.PATCH

MAJOR: Breaking changes to interview structure or output format
MINOR: New content sections, language support, or significant behavior changes
PATCH: Bug fixes, copy improvements, documentation updates
```

Update version in:
1. `.claude-plugin/plugin.json` → `version`
2. `skills/launch-kit/SKILL.md` → `version` in frontmatter AND heading
3. `templates/launch-kit-output.md` → comment header
4. `commands/launch-kit/launch-kit.md` → description if needed

---

## Support

- Issues: https://github.com/JayKim88/claude-ai-engineering/issues
- Discussions: https://github.com/JayKim88/claude-ai-engineering/discussions

---

**Last Updated:** 2026-02-27
**Version:** 1.1.0