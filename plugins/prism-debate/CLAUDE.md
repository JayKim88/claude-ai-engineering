# prism-debate Developer Guide

## Purpose

Multi-perspective adversarial analysis for any proposition — decisions, claims, hypotheses, comparisons.
3-5 agents each hold a fixed worldview and argue from their lens, cross-rebutting across rounds.
The debate evolves: agents respond to each other's prior arguments, not just the original question.

## Architecture

5-layer AI quality system. This plugin = Layer 2 (Process Quality).

```
Layer 1 (Input Quality)    → Context files: values.md, constraints.md (templates/)
Layer 2 (Process Quality)  → This plugin: multi-round adversarial debate
Layer 3 (Output Quality)   → ~/.claude/CLAUDE.md: claim labeling (always-on)
Layer 4 (Validation)       → decision-log.md: prediction tracking (templates/)
Layer 5 (Usage Quality)    → ~/.claude/CLAUDE.md: question routing (always-on)
```

## Directory Structure

```
plugins/prism-debate/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata (v3.0.0)
├── agents/
│   ├── optimist.md              # FOR — The Builder: Yellow Hat worldview
│   ├── critic.md                # AGAINST — The Skeptic: Black Hat worldview
│   ├── pragmatist.md            # FEASIBILITY — The Operator: White Hat worldview
│   ├── alternative.md           # REFRAME — The Inventor: Green Hat worldview (Extended)
│   ├── pre-mortem.md            # FUTURE FAILURE — The Oracle: Gary Klein worldview (Extended)
│   └── synthesizer.md           # JUDGE: final verdict from full debate history
├── skills/
│   └── prism-debate/
│       └── SKILL.md             # 7-step orchestration (3 modes + agent selection + round loop)
├── templates/
│   ├── values.md                # Layer 1 context template
│   ├── constraints.md           # Layer 1 context template
│   └── decision-log.md          # Layer 4 tracking template
├── CLAUDE.md                    # This file
└── README.md                    # User documentation
```

## Agent Architecture

### Core (3 agents — always active)

| Agent | Role | Worldview |
|-------|------|---------|
| optimist | FOR — The Builder | "변화는 항상 가능하다. 현상 유지가 진짜 리스크다" |
| critic | AGAINST — The Skeptic | "대부분은 실패한다. 입증 부담은 명제 쪽에 있다" |
| pragmatist | FEASIBILITY — The Operator | "자원과 시간은 항상 당신 생각보다 부족하다" |

### Extended (2 agents — optional, user selects)

| Agent | Role | Worldview |
|-------|------|---------|
| alternative | REFRAME — The Inventor | "지금 묻고 있는 질문이 아마 틀렸을 것이다. 항상 세 번째 선택지가 있다" |
| pre-mortem | FUTURE FAILURE — The Oracle | "이 패턴이 어디로 향하는지 나는 이미 봤다. 결말은 좋지 않다" |

### Judge

| Agent | Role | Worldview |
|-------|------|---------|
| synthesizer | JUDGE | "좋은 판결은 옳은 것을 말하는 것이 아니다. 틀릴 수 있는 것을 정직하게 인정하는 것이다" |

## Execution Flow

```
User: "prism-debate" / "prism: {question}" / "토론해줘"
  │
  ▼
SKILL.md Step 1: Extract proposition
  (from input OR auto-detect from conversation context)
  + load ~/.claude/context/*.md
  │
  ▼
SKILL.md Step 2: Mode + Agent selection
  Mode 0/1/2 × Core/Extended
  │
  ▼
SKILL.md Step 3: Round 1 (3 or 5 parallel Task() calls)
  │
  ▼ (if Mode 0 → skip to Step 6)
SKILL.md Step 4: Round Loop
  [convergence check] → [user choice] → [Round N parallel] → repeat
  │
  ▼ (user chooses "end debate")
SKILL.md Step 6: Final synthesis
  synthesizer receives full debate_history + agent configuration
  │
  ▼
SKILL.md Step 7: Decision log
```

## Debate Modes

| Mode | Name | Behavior |
|------|------|----------|
| 0 | Quick Verdict | 1 round + immediate synthesis |
| 1 | Autonomous | Agents tiki-taka; user decides when to stop |
| 2 | Participatory | User injects argument each round; agents respond |

## Agent Selection

| Config | Agents | Best for |
|--------|--------|---------|
| Core | Optimist + Critic + Pragmatist | Most decisions, quick analysis |
| Extended | + Alternative + Pre-Mortem | Complex decisions, high-stakes choices, strategic planning |

## Round N Agent Behavior

From Round 2 onward, each agent MUST:
1. Reference specific prior-round arguments by role name
2. State position change: [MAINTAINED / PARTIALLY_CONCEDED / SHIFTED]
3. Not simply repeat Round 1 content — debate must evolve

## Context File Search Order

1. `~/.claude/context/values.md`
2. `~/.claude/context/constraints.md`
3. `~/.claude/context/decision-log.md`
4. `{cwd}/values.md`
5. `{cwd}/constraints.md`

## Convergence Detection

After each round, if all agents report [MAINTAINED] for 2+ consecutive rounds:
→ Signal "💡 포지션 변화 없음 — 토론이 수렴하고 있습니다. 종료를 권장합니다."

## Claim Labels

| Label | Meaning | Weight |
|-------|---------|--------|
| [FACT] | Verifiable, source-traceable | Highest |
| [ESTIMATE] | Reasoned inference | High |
| [OPINION] | Value judgment | Medium |
| [UNCERTAIN] | Genuinely unknown | Context-dependent |

## Position Labels (Round N)

| Label | Meaning |
|-------|---------|
| [MAINTAINED] | Same core position, new supporting evidence |
| [PARTIALLY_CONCEDED] | Concede sub-point X, counter with Y |
| [SHIFTED] | Significantly changed position (requires strong evidence) |

## Versioning

- v1.x.x: Single-round debate (original think-deep)
- v2.0.0: Multi-round + 3 modes + user participation
- v3.0.0: prism-debate rename + 5-agent Extended mode + worldview personas

## Testing Checklist

- [ ] "prism-debate" trigger (no topic) → auto-extract from conversation + confirm
- [ ] "prism: {topic}" trigger → skip extraction, use provided topic
- [ ] Korean triggers: "토론해줘", "검증해줘", "/prism"
- [ ] Mode 0 Core: 3 agents parallel → synthesizer fires immediately
- [ ] Mode 0 Extended: 5 agents parallel → synthesizer fires immediately
- [ ] Mode 1 Round 2: agents cite Round 1 arguments directly
- [ ] Position labels appear: [MAINTAINED / PARTIALLY_CONCEDED / SHIFTED]
- [ ] Convergence signal fires after 2 rounds of all-MAINTAINED
- [ ] Mode 2: user input reaches agents in next round
- [ ] Alternative agent: surfaces at least 1 non-binary alternative
- [ ] Pre-Mortem agent: provides specific failure causal chain (not vague risks)
- [ ] Synthesizer: Extended mode output incorporates Alternative + Pre-Mortem
- [ ] Synthesizer output includes "position evolution" section
- [ ] Decision log appended correctly after all modes
