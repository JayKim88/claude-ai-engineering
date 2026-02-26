---
name: prism-debate
description: Multi-perspective adversarial analysis. 3-5 agents view a proposition through different lenses — cross-rebutting across rounds with position tracking. Supports quick verdict, autonomous rounds, and user-participatory modes. Use when user says "prism-debate", "prism", "/prism", "토론해줘", "검증해줘", "반박해줘", "반론해줘", "도전해줘", or invokes adversarial analysis of any proposition.
version: 3.0.0
---

# prism-debate Skill

Multi-perspective adversarial analysis through structured rounds. Each agent holds a fixed worldview (not just a stance). From Round 2 onward, agents must directly respond to prior-round arguments — debate evolves, not repeats.

## Trigger Phrases

**English:**
- "prism-debate", "prism-debate:", "/prism-debate"
- "prism", "prism:", "/prism"
- "challenge this", "stress test", "steelman and critique"

**Korean:**
- "토론해줘", "검증해줘", "반론해줘"
- "반박해줘", "도전해줘"

---

## Execution Algorithm

### Step 1: Extract Proposition + Load Context

**Two input modes:**

```python
# Mode A: Explicit topic
# User wrote: "prism-debate: Should we use GraphQL?" or "prism: Python 배워야 하나?"
if user_input contains ":" or has meaningful content after trigger word:
    question = text_after_trigger_word(user_input)
    # Do NOT ask for confirmation — proceed directly to Step 2

# Mode B: Context extraction
# User wrote just: "prism-debate" or "/prism" or "토론해줘" with no topic
else:
    # Analyze recent conversation to find the main undecided question
    # Look for: undecided questions, A vs B comparisons, "should I..." patterns
    question = extract_main_decision_from_recent_conversation()

    AskUserQuestion(
        "이 주제로 토론을 시작할까요?",
        options=[
            f'"{question}" — 맞습니다, 시작',
            "직접 입력할게요"
        ]
    )

    if "직접 입력":
        question = user_provided_text
```

If no extractable topic: ask "토론하고 싶은 주제나 결정을 알려주세요."

**Load context files** (search in order, load all that exist):
```python
context_files = {}
for path in [
    "~/.claude/context/values.md",
    "~/.claude/context/constraints.md",
    "~/.claude/context/decision-log.md",
    "{cwd}/values.md",
    "{cwd}/constraints.md"
]:
    if exists(path):
        context_files[basename(path)] = Read(path)

context_block = format_context(context_files)  # "" if none
```

Display: `🔍 prism-debate: "{question}"`
Display: `📂 Context: {loaded_files or "없음"}`

---

### Step 2: Mode + Agent Selection

```python
AskUserQuestion(
    "토론 방식을 선택해주세요:",
    options=[
        {
            "label": "⚡ 빠른 판결",
            "description": "1 라운드 → 즉시 종합 판결. 빠른 스트레스 테스트"
        },
        {
            "label": "🔄 자율 토론",
            "description": "에이전트끼리 tiki-taka. 매 라운드 후 계속할지 결정"
        },
        {
            "label": "💬 참여형 토론",
            "description": "매 라운드 내 의견을 추가할 수 있음. 에이전트가 응답"
        }
    ]
)
# mode = 0 (quick) | 1 (autonomous) | 2 (participatory)

AskUserQuestion(
    "에이전트 구성을 선택하세요:",
    options=[
        {
            "label": "🎯 Core (3 에이전트)",
            "description": "Optimist + Critic + Pragmatist — 빠르고 집중적"
        },
        {
            "label": "🔬 Extended (5 에이전트)",
            "description": "+ Alternative (대안 탐색) + Pre-Mortem (실패 역분석). 더 풍부한 분석"
        }
    ]
)
# agent_mode = "core" | "extended"
```

---

### Step 3: Round 1 — Initial Positions

Launch agents in **a single response block** (parallel execution):

```python
# PARALLEL: All agents in same response block
Task(
    subagent_type="optimist",
    model="sonnet",
    description="Build strongest case FOR (Round 1)",
    prompt=f"""
## Debate Proposition
{question}

{context_block}

This is ROUND 1. Build the STRONGEST POSSIBLE case FOR this proposition.
Follow your Round 1 instructions. Output format per your agent file.
"""
)

Task(
    subagent_type="critic",
    model="sonnet",
    description="Build strongest case AGAINST (Round 1)",
    prompt=f"""
## Debate Proposition
{question}

{context_block}

This is ROUND 1. Build the STRONGEST POSSIBLE case AGAINST this proposition.
Follow your Round 1 instructions. Output format per your agent file.
"""
)

Task(
    subagent_type="pragmatist",
    model="sonnet",
    description="Assess feasibility and constraints (Round 1)",
    prompt=f"""
## Debate Proposition
{question}

{context_block}

This is ROUND 1. Assess feasibility, constraints, and key unknowns.
Follow your Round 1 instructions. Output format per your agent file.
"""
)

# Extended mode only — add to same parallel block:
if agent_mode == "extended":
    Task(
        subagent_type="alternative",
        model="sonnet",
        description="Generate alternative framings (Round 1)",
        prompt=f"""
## Debate Proposition
{question}

{context_block}

This is ROUND 1. Surface 2-3 genuinely different approaches not captured in the proposition.
Follow your Round 1 instructions. Output format per your agent file.
"""
    )

    Task(
        subagent_type="pre-mortem",
        model="sonnet",
        description="Pre-mortem failure analysis (Round 1)",
        prompt=f"""
## Debate Proposition
{question}

{context_block}

This is ROUND 1. Assume this proposition was adopted and failed. Identify why.
Follow your Round 1 instructions. Output format per your agent file.
"""
    )
```

Store:
```python
debate_history = {
    "round_1": {
        "optimist": optimist_result,
        "critic": critic_result,
        "pragmatist": pragmatist_result,
        "alternative": alternative_result if extended else None,
        "pre_mortem": pre_mortem_result if extended else None,
        "user_input": None
    }
}
current_round = 1
```

Display:
```
╔═══════════════════════════════════════╗
║  ROUND 1: {question}
╚═══════════════════════════════════════╝

🟢 OPTIMIST — The Builder (for)
{optimist_result}

🔴 CRITIC — The Skeptic (against)
{critic_result}

🟡 PRAGMATIST — The Operator (feasibility)
{pragmatist_result}

🔵 ALTERNATIVE — The Inventor (reframe)      ← Extended only
{alternative_result}

🟣 PRE-MORTEM — The Oracle (future failure)  ← Extended only
{pre_mortem_result}
```

**If Mode 0 (Quick Verdict):** → jump directly to Step 6.

---

### Step 4: Round Loop (Mode 1 & 2 only)

```python
maintained_streak = 0  # consecutive all-MAINTAINED rounds

loop:
    # --- Convergence Detection ---
    positions = extract_position_labels_from_round(debate_history[f"round_{current_round}"])
    # positions = {"optimist": "MAINTAINED", "critic": "PARTIALLY_CONCEDED", ...}

    if all(p == "MAINTAINED" for p in positions.values() if p is not None):
        maintained_streak += 1
    else:
        maintained_streak = 0

    if maintained_streak >= 2:
        display: "💡 포지션 변화 없음 — 토론이 수렴하고 있습니다. 판결로 이동을 권장합니다."

    for role, pos in positions.items():
        if pos in ["PARTIALLY_CONCEDED", "SHIFTED"]:
            display: f"⚡ {role.upper()} 포지션 변화: {pos}"

    # --- User Choice ---
    if mode == 1:
        AskUserQuestion(
            f"Round {current_round} 완료. 다음 행동을 선택하세요:",
            options=[
                {"label": f"Round {current_round + 1} 진행", "description": "에이전트들이 계속 토론"},
                {"label": "판결로 이동", "description": "토론 종료 후 최종 판결"}
            ]
        )

    elif mode == 2:
        AskUserQuestion(
            f"Round {current_round} 완료. 다음 행동을 선택하세요:",
            options=[
                {"label": f"Round {current_round + 1} 진행 (에이전트만)", "description": "내 의견 없이 계속"},
                {"label": "내 의견 추가하고 다음 라운드", "description": "내 논거 입력 → 에이전트가 응답"},
                {"label": "판결로 이동", "description": "토론 종료 후 최종 판결"}
            ]
        )

    if user chose "판결로 이동": break

    # --- Mode 2: Collect User Input (optional) ---
    user_input = None
    if mode == 2 and user chose "내 의견 추가":
        AskUserQuestion(
            "이번 라운드에 추가할 논거나 의견을 자유롭게 입력해주세요:",
            (free text input — user types their argument)
        )
        user_input = user_text

    # --- Round N: Build prior round context ---
    next_round = current_round + 1
    prev = debate_history[f"round_{current_round}"]

    prior_round_text = f"""
## Round {current_round} Arguments (아래 논거에 직접 응답할 것)

**Optimist (Round {current_round}):**
{prev["optimist"]}

**Critic (Round {current_round}):**
{prev["critic"]}

**Pragmatist (Round {current_round}):**
{prev["pragmatist"]}
{"**Alternative (Round " + str(current_round) + "):**\n" + prev["alternative"] if prev.get("alternative") else ""}
{"**Pre-Mortem (Round " + str(current_round) + "):**\n" + prev["pre_mortem"] if prev.get("pre_mortem") else ""}
{f'**User Input (Round {current_round}):**\n{user_input}' if user_input else ''}

CRITICAL: 위 논거 중 하나 이상을 직접 인용하거나 이름을 언급하여 반박/응답할 것.
첫 줄에 반드시 [MAINTAINED], [PARTIALLY_CONCEDED], 또는 [SHIFTED] 표기.
"""

    # --- Round N: Parallel Execution ---
    Task(subagent_type="optimist", model="sonnet", description=f"Round {next_round} — FOR",
         prompt=f"## Debate Proposition\n{question}\n\n{context_block}\n\n{prior_round_text}\n\nThis is ROUND {next_round}. Follow your Round N Behavior instructions.")
    Task(subagent_type="critic", model="sonnet", description=f"Round {next_round} — AGAINST",
         prompt=f"## Debate Proposition\n{question}\n\n{context_block}\n\n{prior_round_text}\n\nThis is ROUND {next_round}. Follow your Round N Behavior instructions.")
    Task(subagent_type="pragmatist", model="sonnet", description=f"Round {next_round} — FEASIBILITY",
         prompt=f"## Debate Proposition\n{question}\n\n{context_block}\n\n{prior_round_text}\n\nThis is ROUND {next_round}. Follow your Round N Behavior instructions.")

    if agent_mode == "extended":
        Task(subagent_type="alternative", model="sonnet", description=f"Round {next_round} — REFRAME",
             prompt=f"## Debate Proposition\n{question}\n\n{context_block}\n\n{prior_round_text}\n\nThis is ROUND {next_round}. Follow your Round N Behavior instructions.")
        Task(subagent_type="pre-mortem", model="sonnet", description=f"Round {next_round} — FUTURE FAILURE",
             prompt=f"## Debate Proposition\n{question}\n\n{context_block}\n\n{prior_round_text}\n\nThis is ROUND {next_round}. Follow your Round N Behavior instructions.")

    debate_history[f"round_{next_round}"] = {
        "optimist": optimist_result,
        "critic": critic_result,
        "pragmatist": pragmatist_result,
        "alternative": alternative_result if extended else None,
        "pre_mortem": pre_mortem_result if extended else None,
        "user_input": user_input
    }
    current_round = next_round

    # --- Display Round N Summary ---
    display:
    """
    ╔═══════════════════════════════════════╗
    ║  ROUND {current_round}: {question_summary}
    ╚═══════════════════════════════════════╝

    🟢 OPTIMIST [{position}]
    {optimist_result}

    🔴 CRITIC [{position}]
    {critic_result}

    🟡 PRAGMATIST [{position}]
    {pragmatist_result}

    🔵 ALTERNATIVE [{position}]    ← Extended only
    {alternative_result}

    🟣 PRE-MORTEM [{position}]     ← Extended only
    {pre_mortem_result}

    {convergence_message if maintained_streak >= 2}
    """
    # continue loop
```

---

### Step 6: Final Synthesis

```python
full_history = ""
for r in range(1, current_round + 1):
    rd = debate_history[f"round_{r}"]
    full_history += f"""
--- Round {r} ---
Optimist: {rd["optimist"]}
Critic: {rd["critic"]}
Pragmatist: {rd["pragmatist"]}
{"Alternative: " + rd["alternative"] if rd.get("alternative") else ""}
{"Pre-Mortem: " + rd["pre_mortem"] if rd.get("pre_mortem") else ""}
{f'User Input: {rd["user_input"]}' if rd.get("user_input") else ""}
"""

Task(
    subagent_type="synthesizer",
    model="sonnet",
    description="Synthesize full debate into final verdict",
    prompt=f"""
## Debate Proposition
{question}

{context_block}

## Complete Debate History ({current_round} rounds)
{full_history}

## Agent Configuration
{"Extended mode: includes Alternative (reframe) and Pre-Mortem (future failure) perspectives" if agent_mode == "extended" else "Core mode: Optimist, Critic, Pragmatist"}

Synthesize the full debate. Output must include:
1. Verdict: [RECOMMEND/REJECT/CONDITIONAL/UNCERTAIN]
2. Evidence (min 3 labeled points from debate)
3. Strongest Counter-Argument to your verdict
4. Preconditions for verdict to hold
5. Position Evolution: what changed, what converged, what stayed contested
6. Decision Log suggestion
Follow your output format exactly.
"""
)
```

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYNTHESIS ({current_round} 라운드 토론)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{synthesizer_output}
```

---

### Step 7: Decision Log (Optional)

```python
AskUserQuestion(
    "이 토론 결과를 decision-log.md에 기록할까요?",
    options=[
        {"label": "기록하기", "description": "예측을 기록하여 나중에 정확도 추적"},
        {"label": "건너뛰기", "description": "탐색적 분석이었으므로 기록 불필요"}
    ]
)

if "기록하기":
    # Search: ~/.claude/context/decision-log.md → {cwd}/decision-log.md
    # If not found: offer to create from template
    # Append new table row
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No extractable topic (Mode B) | Ask: "토론하고 싶은 주제나 결정을 알려주세요." |
| Agent timeout | Retry once; if fails, note gap, continue |
| No context files | Proceed without context, no warning |
| decision-log.md not found | Offer to create: `~/.claude/context/decision-log.md` |
| Synthesizer no clear verdict | [UNCERTAIN] + "토론이 균형을 이뤄 명확한 판결이 어렵습니다" |

---

## Quick Reference

```
"prism-debate: {topic}"  — explicit topic, skip confirmation
"prism: {topic}"         — short form trigger
"prism-debate"           — auto-detect from conversation
"/prism"                 — same as above
"토론해줘: {topic}"        — Korean explicit
"검증해줘"                 — Korean auto-detect
```

**Duration (Claude Max — no extra API cost):**
- Mode 0 Core: ~2 min (3 parallel + 1 synthesis)
- Mode 0 Extended: ~2.5 min (5 parallel + 1 synthesis)
- Each additional round (Core): ~1 min
- Each additional round (Extended): ~1.5 min
