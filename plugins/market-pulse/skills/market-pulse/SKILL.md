---
name: market-pulse
description: Financial market analysis dashboard. Use when user says "market overview", "market pulse", "stock market", "시장 분석", "주식 시장", "시장 현황", "증시 분석", "시장 브리핑", or wants to check financial markets, stocks, crypto.
version: 1.0.0
---

# Market Pulse

Fetches real-time financial market data (US stocks, Korean stocks, global macro, crypto) and generates a comprehensive analysis dashboard using multi-agent pipeline.

---

## Execution Algorithm

### Step 1: Acknowledge Trigger

Briefly confirm in Korean:

"시장 분석을 시작하겠습니다. 먼저 분석 범위를 선택해주세요."

---

### Step 2: Ask Analysis Scope

Use AskUserQuestion to let the user choose the analysis scope.

```
AskUserQuestion:
  questions:
    - question: "어떤 시장 분석을 원하시나요?"
      header: "분석 범위"
      multiSelect: false
      options:
        - label: "전체 시장 개요 (Overview)"
          description: "미국, 한국, 글로벌 매크로, 크립토 전체 요약 (Recommended)"
        - label: "미국 시장 (US Market)"
          description: "S&P 500, 섹터 ETF, VIX 상세 분석"
        - label: "한국 시장 (Korean Market)"
          description: "KOSPI/KOSDAQ, 외국인/기관, 주요 종목 상세 분석"
        - label: "글로벌 매크로 + 크립토"
          description: "금리, 원자재, 환율, 암호화폐 분석"
        - label: "내 워치리스트 (My Watchlist)"
          description: "개인 관심 종목 집중 분석"
        - label: "딥 다이브 (Deep Dive)"
          description: "전체 시장 + 워치리스트 + 뉴스 (가장 상세)"
```

**Map selection to --scope argument:**
- "전체 시장 개요" → `--scope overview`
- "미국 시장" → `--scope us`
- "한국 시장" → `--scope kr`
- "글로벌 매크로 + 크립토" → `--scope crypto`
- "내 워치리스트" → `--scope watchlist`
- "딥 다이브" → `--scope deep`

---

### Step 3: Check Dependencies & Fetch Data

**3-1. Check Python dependencies:**

```bash
python3 -c "import yfinance, pykrx, yaml" 2>/dev/null || \
  pip3 install yfinance pykrx pyyaml feedparser --quiet
```

**3-2. Locate and run the fetch script:**

Find the plugin directory. Check these paths in order:
1. `~/.claude/skills/market-pulse/../../config/fetch_market.py` (installed via symlink)
2. `plugins/market-pulse/config/fetch_market.py` (local development)

```bash
python3 {path_to_fetch_market.py} --scope {scope} --output json
```

**3-3. Error handling:**
- If script not found: inform user of the path issue and suggest reinstalling
- If script fails: show error and suggest checking internet connection
- If partial data: proceed with available data, note missing sections

---

### Step 4: Branch by Scope

**For `overview` or `deep` scope** → Go to Step 5 (Multi-Agent Pipeline)

**For single-market scope (`us`, `kr`, `crypto`)** → Go to Step 6-Single

**For `watchlist` scope** → Go to Step 6-Watchlist

---

### Step 5: Multi-Agent Analysis (overview / deep)

**Phase 1: Parallel Analysis**

Launch all 3 agents in a SINGLE response block for parallel execution:

```
Task(
    subagent_type="us-market-analyzer",
    model="sonnet",
    description="Analyze US market data",
    prompt="Analyze the following US market data and provide insights.\n\n{us_indices + us_sectors + vix data from JSON}\n\nProvide index trend interpretation, sector rotation analysis, and market sentiment assessment."
)

Task(
    subagent_type="kr-market-analyzer",
    model="sonnet",
    description="Analyze Korean market data",
    prompt="Analyze the following Korean market data and provide insights.\n\n{kr_indices + kr_foreign_institutional + kr_top_stocks data from JSON}\n\nAlso consider USD/KRW from currencies data: {usd_krw data}\n\nProvide KOSPI/KOSDAQ interpretation, 외국인/기관 flow analysis, and notable stocks."
)

Task(
    subagent_type="crypto-macro-analyzer",
    model="sonnet",
    description="Analyze crypto and global macro",
    prompt="Analyze the following crypto and global macro data.\n\n{crypto + treasury_yields + commodities + currencies data from JSON}\n\nProvide crypto market overview, bond market interpretation, commodity trends, dollar analysis, and global risk assessment."
)
```

**Phase 2: Synthesis**

After Phase 1 completes, run the synthesizer:

```
Task(
    subagent_type="market-synthesizer",
    model="haiku",
    description="Synthesize market dashboard",
    prompt="Synthesize the following market analyses into a unified dashboard.\n\nMarket Status: {market_status from JSON}\n\n# US Market Analysis\n{us-market-analyzer output}\n\n# Korean Market Analysis\n{kr-market-analyzer output}\n\n# Crypto & Global Macro Analysis\n{crypto-macro-analyzer output}\n\nCreate unified dashboard with: top 3 key takeaways, all market sections, cross-market themes, and disclaimer."
)
```

Go to Step 7.

---

### Step 6-Single: Single Market Analysis

For `us`, `kr`, or `crypto` scope:
- Only launch the relevant single agent
- No Phase 2 synthesis needed
- Display the agent's output directly

For `us`:
```
Task(subagent_type="us-market-analyzer", model="sonnet", ...)
```

For `kr`:
```
Task(subagent_type="kr-market-analyzer", model="sonnet", ...)
```

For `crypto`:
```
Task(subagent_type="crypto-macro-analyzer", model="sonnet", ...)
```

Go to Step 7.

---

### Step 6-Watchlist: Watchlist Display

For `watchlist` scope, no agents are needed. Display watchlist data directly in a table format:

```markdown
## My Watchlist

### US Stocks
| Symbol | Price | Change | Alert | Notes |
|--------|-------|--------|-------|-------|
| {symbol} | ${price} | {change_pct}% | {alerts or --} | {notes} |

### Korean Stocks (한국 주식)
| 종목 | 가격 | 등락 | Notes |
|------|------|------|-------|
| {name} ({ticker}) | {price}원 | {change_pct}% | {notes} |

### Crypto
| Coin | Price | 24h Change |
|------|-------|------------|
| {name} | ${price} | {change_pct}% |
```

Go to Step 7.

---

### Step 7: Display Dashboard

Present the analysis directly in the terminal. **DO NOT save to a file automatically.**

After displaying the dashboard or analysis, output this follow-up message:

"추가 분석이 필요하시면 말씀해주세요:"
"1. 특정 종목 딥다이브 (종목명이나 티커 입력)"
"2. 대시보드를 파일로 저장"
"3. 워치리스트 확인"
"4. 없음 (마무리)"

---

### Step 8: Handle Follow-up

**Parse user response:**

- If specific stock/ticker requested: Use WebSearch to find latest news, or fetch specific stock data and provide brief analysis
- If save requested:
  - Read `~/.claude/skills/learning-summary/config.yaml`
  - If `learning_repo` configured: save to `{learning_repo}/digests/market-pulse-YYYY-MM-DD.md`
  - Otherwise: save to `./market-pulse-YYYY-MM-DD.md`
  - Confirm: "대시보드를 저장했습니다: {file_path}"
- If watchlist requested: Run fetch with `--scope watchlist` and display
- If "없음" or done: "마무리합니다. 다음에 시장 분석이 필요하면 말씀해주세요!"

---

## Trigger Phrases

**English:**
- "market overview"
- "market pulse"
- "stock market analysis"
- "how are the markets doing"
- "check the markets"
- "financial dashboard"

**Korean:**
- "시장 분석"
- "주식 시장"
- "시장 현황"
- "오늘 시장 어때"
- "증시 분석"
- "시장 브리핑"

---

## Configuration

### Data Sources (config/sources.yaml)

**US Market**: S&P 500, NASDAQ, DOW, Russell 2000, 11 SPDR Sector ETFs, VIX
**Korean Market**: KOSPI, KOSDAQ, Top 10 market cap stocks, Foreign/Institutional flows
**Global Macro**: Treasury yields (5Y, 10Y, 30Y), Gold, Oil, Natural Gas, DXY, USD/KRW, EUR/USD, USD/JPY
**Crypto**: BTC, ETH, SOL, BNB, XRP, ADA

### Personal Watchlist (config/watchlist.yaml)

Edit this file to add your own stocks:
```yaml
us_stocks:
  - symbol: "AAPL"
    name: "Apple"
    alert_above: 250    # Optional price alert
    alert_below: 180
kr_stocks:
  - ticker: "005930"
    name: "삼성전자"
crypto:
  - symbol: "BTC-USD"
    name: "Bitcoin"
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Python missing | "Python 3가 필요합니다. 설치 후 다시 시도해주세요." |
| yfinance/pykrx not installed | Auto-install via pip3 |
| No internet | "인터넷 연결을 확인해주세요." |
| US market closed | Show last close data + note "미국 장 마감 상태" |
| KR market closed | Show last close data + note "한국 장 마감" |
| Partial data failure | Proceed with available data, note missing sections |
| Script not found | Check both symlink and local paths |
| Invalid ticker in watchlist | Skip with warning: "[SYMBOL] 데이터 없음" |

---

## Performance

- Data fetching: 15-45 seconds (depends on scope)
- Phase 1 agents: 30-60 seconds (parallel)
- Phase 2 synthesis: 10-20 seconds
- Total (overview): ~1-2 minutes

---

## Dependencies

```bash
pip3 install yfinance pykrx pyyaml feedparser
```

---

## Related Skills

- `ai-news-digest`: For AI-specific news (use for tech sector context)
- `ai-digest`: For detailed article analysis (use after finding interesting financial articles)

---

## Examples

### Example 1: Quick Overview

```
User: "시장 분석해줘"
→ AskUserQuestion: 분석 범위 선택
User: "전체 시장 개요"
→ Fetch data (30s) → 3 agents parallel (45s) → synthesis (15s)
→ Display dashboard with all markets
→ "추가 분석이 필요하시면..."
User: "없음"
→ End
```

### Example 2: Korean Market Focus

```
User: "한국 시장 어때?"
→ AskUserQuestion: 분석 범위
User: "한국 시장"
→ Fetch KR data → kr-market-analyzer only
→ Display KR-focused analysis
→ "추가 분석이 필요하시면..."
User: "삼성전자 좀 더 자세히"
→ Fetch Samsung Electronics detailed data + recent news
→ Display analysis
```

### Example 3: Deep Dive

```
User: "market deep dive"
→ Scope: deep
→ Fetch all data + watchlist + news (45s)
→ Full multi-agent pipeline
→ Extended dashboard with watchlist and news sections
```
