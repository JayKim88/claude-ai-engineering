# Design Advanced Knowledge Base

Expert design frameworks for Phase 3 (Design System & Wireframes).
Source: Jakob Nielsen (Usability Heuristics), Don Norman (Design of Everyday Things),
Intercom (JTBD for UX), Steve Krug (Don't Make Me Think), Basecamp (Shape Up design).

---

## 1. Nielsen's 10 Usability Heuristics

Every UI component and screen must be evaluated against these 10 heuristics.

| # | Heuristic | Pass Criteria | Common Violations |
|---|-----------|---------------|-------------------|
| 1 | Visibility of system status | User always knows what's happening (loading, saved, error) | Missing loading states, silent failures |
| 2 | Match between system and real world | Language matches user vocabulary, not internal/technical | Jargon, unfamiliar icons, developer-speak |
| 3 | User control and freedom | Easy undo, cancel, escape routes | No back button, irreversible actions without confirmation |
| 4 | Consistency and standards | Same words, icons, colors mean the same thing everywhere | Inconsistent button labels, icons with multiple meanings |
| 5 | Error prevention | Design prevents errors before they happen | No confirmation on destructive actions, no input validation hints |
| 6 | Recognition over recall | Show options; don't force users to remember | Empty search with no suggestions, no recent items |
| 7 | Flexibility and efficiency | Power users can shortcut; beginners can learn | No keyboard shortcuts, no bulk actions |
| 8 | Aesthetic and minimalist design | Every element earns its place | Information overload, decorative elements that distract |
| 9 | Help users recognize and recover from errors | Error messages in plain language with solution path | "Error 500", red screens with no guidance |
| 10 | Help and documentation | Easy to find, focused on task, concrete steps | FAQ buried in footer, generic "contact support" |

---

## 2. Conversion-Focused Design Patterns

### Trust Signal Hierarchy
Order by persuasive impact (use all that apply):
1. **Social proof numbers** — "10,000+ companies trust us" (specific > vague)
2. **Customer logos** — recognizable brand logos
3. **Testimonials with specifics** — "$X saved per month" beats "Great product!"
4. **Star ratings** — G2, Capterra, App Store ratings with count
5. **Media mentions** — "As seen in TechCrunch" badges
6. **Security badges** — SSL, SOC2, GDPR seals
7. **Money-back guarantee** — reduces purchase anxiety

### CTA Hierarchy Rules
Every page has exactly 1 Primary CTA. Secondary CTAs must be visually subordinate.

| CTA Type | Visual Treatment | Copy Standard |
|----------|-----------------|---------------|
| Primary | Solid, high-contrast brand color, large (48px+ height) | Action verb + benefit: "Start Free Trial" not "Submit" |
| Secondary | Outlined or text button | Lower commitment: "See how it works" |
| Destructive | Red, separated from primary action | "Delete" never near "Save" |

**Good CTA copy:** "Get My Free Report", "Start Building — Free"
**Bad CTA copy:** "Submit", "Click Here", "Learn More" (ambiguous)

### Above-the-Fold Standard (Landing Pages)
In first 5 seconds, user must see:
1. **Hero headline** — what it does (outcome), not what it is (category)
2. **Sub-headline** — who it's for + main benefit
3. **Primary CTA** — visible without scrolling
4. **At least 1 trust signal** — social proof, logo, or number

**Headline formula:** `[Verb] your [outcome] [qualifier]`
- Good: "Ship your SaaS in 2 weeks, not 6 months"
- Bad: "The All-In-One Platform for Modern Teams"

---

## 3. Empty State, Error State, Loading State Design

### The "Little Big Details" Framework (Samuel Hulick)
Every state must provide: Context → Cause → Action path

**Empty State Design:**
```
┌─────────────────────────────────┐
│       [Contextual illustration] │
│                                 │
│   You don't have any [items]    │  ← What's empty
│                                 │
│   [Items] help you [benefit].   │  ← Why it matters
│                                 │
│   [Primary CTA: Create first X] │  ← Clear next step
└─────────────────────────────────┘
```
- Never: blank white space
- Always: illustration + explanation + action button

**Error State Design:**
```
Error message structure:
1. What happened (plain language, no codes)
2. Why it happened (when helpful)
3. How to fix it (specific next step)

Good: "Your payment didn't go through. The card ending in 4242
      may have expired. Update your payment method →"
Bad:  "Error: PAYMENT_FAILED_3042"
```

**Loading State Hierarchy:**
- < 100ms: No indicator needed (feels instant)
- 100ms–1s: Spinner
- 1s–3s: Skeleton screen (keeps layout stable)
- > 3s: Progress bar + time estimate + option to cancel

---

## 4. Friction Audit Methodology

### Friction Categories (Steve Krug)
Rate each friction point: High / Medium / Low impact

| Category | What to check | High friction examples |
|----------|---------------|----------------------|
| Cognitive load | How much must user remember or understand? | 10-field forms, unexplained requirements |
| Motor friction | How many clicks/taps required? | 3 clicks to complete core action |
| Time friction | How long does it take? | Forced reading, long animations |
| Trust friction | Does user feel safe? | Requesting info before establishing value |
| Decision friction | Too many choices? | 7 options when 3 suffice |

### Onboarding Friction Audit
Ideal onboarding: User reaches Aha Moment in < 5 minutes and < 5 steps.

**Audit checklist:**
- [ ] Signup form: max 2 fields (email + password) — defer all profile info
- [ ] Email verification: optional for initial entry, required before paid action
- [ ] First screen: shows pre-populated example or guided first action (not blank)
- [ ] Progress indicator visible if onboarding > 3 steps
- [ ] No walls of instructional text — show, don't tell

### Checkout / Upgrade Friction Audit
- [ ] Price appears before checkout form
- [ ] No surprise fees at last step
- [ ] Annual/monthly toggle visible on pricing page
- [ ] "What's included" visible without clicking
- [ ] 1-click upgrade path for existing users (card on file)

---

## 5. Mobile-First Design Principles

### Tap Target Standards
- Minimum: 44×44px (iOS HIG) / 48×48dp (Material Design)
- Preferred: 56×56px for primary actions
- Spacing between targets: minimum 8px

### Thumb Zone Map (right-handed phone)
```
┌──────────────────┐
│ ○○○○○○○○○○○○○  │  Hard to reach (secondary actions)
│ ○○○○○○○○○○○○○  │
│ ●●●●●○○○○○○○  │
│ ●●●●●●●●○○○○  │  Natural / Easy (primary actions)
│ ●●●●●●●●●●●○  │
│ ●●●●●●●●●●●●  │  Easy reach (navigation)
└──────────────────┘
```
Place primary CTA in natural/easy zone. Navigation at bottom.

### Content Priority for Mobile
- Show: headline, primary value, primary CTA
- Hide behind tap: secondary info, detailed specs, navigation items
- Never: horizontal scroll tables, tiny text (<14px), auto-playing video with sound

---

## 6. Design Quality Standards (Phase 3)

**Design System Completeness Checklist:**
- [ ] Color tokens defined: primary, secondary, neutral, semantic (success/warning/error/info)
- [ ] Typography scale: min 6 levels (H1–H4, body, caption) with px sizes and line heights
- [ ] Spacing system: 8px base grid, 6+ tokens defined (xs/sm/md/lg/xl/2xl)
- [ ] Component states: every interactive component has default/hover/active/disabled/focus states
- [ ] Accessibility: WCAG AA contrast checked for all text/background combos
- [ ] Responsive breakpoints defined (mobile/tablet/desktop min)
- [ ] Empty states designed for all data-dependent screens
- [ ] Error states designed for all forms and API-dependent displays
- [ ] Loading states designed (skeleton screens for >1s operations)

**Self-Assessment Block (add at top of design output before saving):**
```markdown
---
**Design Quality Check**
- Depth: [1–3] — [atomic components defined vs. page-level only]
- Evidence: [1–3] — [usability heuristics checked, user research integrated]
- Specificity: [1–3] — [exact px/color values vs. vague descriptions]
- Accessibility: [WCAG AA: pass/fail/untested]
- Mobile-first: [yes/no]
- Empty/error/loading states: [covered/missing]
- Unmet criteria: [list or "none"]
---
```
