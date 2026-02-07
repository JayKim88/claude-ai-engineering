---
name: market-pulse
description: Financial market analysis dashboard. Use when user says "market overview", "market pulse", "stock market", "시장 분석", "주식 시장", "시장 현황", "증시 분석", "시장 브리핑", or wants to check financial markets, stocks, crypto.
version: 1.0.0
---

# Market Pulse

Fetches real-time financial market data (US stocks, Korean stocks, global macro, crypto) and generates a comprehensive analysis dashboard using multi-agent pipeline.

---

## Execution Algorithm

### Step 1: Acknowledge and Start

Briefly confirm in Korean and start immediately with default scope (overview):

"시장 분석을 시작합니다. 데이터를 수집하고 있습니다..."

**Default scope: `overview`** (미국, 한국, 글로벌 매크로, 크립토 전체 요약)

**Note:** User can request specific scope by saying "미국 시장만", "한국 시장만", etc. In that case, use the appropriate scope:
- "미국 시장" → `--scope us`
- "한국 시장" → `--scope kr`
- "글로벌 매크로" or "크립토" → `--scope crypto`
- "워치리스트" → `--scope watchlist`
- "딥 다이브" → `--scope deep`

---

### Step 2: Check Dependencies & Fetch Data

**2-1. Check Python dependencies (silent auto-install):**

```bash
python3 -c "import yfinance, pykrx, yaml" 2>/dev/null || \
  pip3 install yfinance pykrx pyyaml feedparser --quiet
```

**2-2. Locate and run the fetch script:**

Find the plugin directory. Check these paths in order:
1. `~/.claude/skills/market-pulse/../../config/fetch_market.py` (installed via symlink)
2. `plugins/market-pulse/config/fetch_market.py` (local development)

```bash
# Save output to temp file for later use
TEMP_JSON=/tmp/market-pulse-data-$(date +%s).json
python3 {path_to_fetch_market.py} --scope {scope} --output json > $TEMP_JSON
```

**2-3. Error handling:**
- If script not found: inform user of the path issue and suggest reinstalling
- If script fails: show error and suggest checking internet connection
- If partial data: proceed with available data, note missing sections

---

### Step 3: Branch by Scope

**For `overview` or `deep` scope** → Go to Step 4 (Multi-Agent Pipeline)

**For single-market scope (`us`, `kr`, `crypto`)** → Go to Step 5-Single

**For `watchlist` scope** → Go to Step 5-Watchlist

---

### Step 4: Multi-Agent Analysis (overview / deep)

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

**Phase 3: Save Analysis to JSON**

After synthesis completes, add analysis results to the JSON file:

```bash
# Read original JSON
ORIGINAL_JSON=$(cat $TEMP_JSON)

# Create new JSON with analysis added
python3 -c "
import json, sys
data = json.loads('''$ORIGINAL_JSON''')
data['analysis'] = {
    'us_market': '''(us-market-analyzer output text)''',
    'kr_market': '''(kr-market-analyzer output text)''',
    'crypto_macro': '''(crypto-macro-analyzer output text)''',
    'synthesis': '''(market-synthesizer output text)'''
}
print(json.dumps(data, indent=2, ensure_ascii=False))
" > $TEMP_JSON
```

Go to Step 6.

---

### Step 5-Single: Single Market Analysis

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

Go to Step 6.

---

### Step 5-Watchlist: Watchlist Display

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

Go to Step 6.

---

### Step 6: Generate HTML Dashboard and Auto-Open

**6-1. Display Terminal Summary**

Present a brief summary of the analysis in the terminal (key takeaways only, 5-10 lines).

**6-2. Generate Interactive HTML Dashboard**

Automatically generate HTML dashboard with visualizations (auto-named with timestamp):

```bash
# Locate generate_html.py (same directory as fetch_market.py)
# Output path will be auto-generated: /tmp/market-pulse-YYYYMMDD-HHMMSS.html
HTML_OUTPUT=$(python3 {path_to_generate_html.py} --input $TEMP_JSON)
```

**6-3. Auto-Open in Browser**

Automatically open the HTML dashboard:

```bash
# macOS
open "$HTML_OUTPUT"

# Linux
xdg-open "$HTML_OUTPUT" 2>/dev/null || sensible-browser "$HTML_OUTPUT"

# Windows
start "$HTML_OUTPUT"
```

**6-4. Confirm to User**

Output in Korean:

"✅ 대시보드가 생성되었습니다!
📊 HTML 파일: $HTML_OUTPUT
🌐 브라우저에서 자동으로 열렸습니다.

대시보드에는 다음 정보가 포함되어 있습니다:
- 대화형 차트 (Chart.js)
- 상세 데이터 테이블
- 정확한 데이터 출처 링크

추가로 필요하신 게 있으시면 말씀해주세요!"

---

### Step 7: Optional Follow-up

If user requests additional analysis:

- **특정 종목 분석**: Use WebSearch to find latest news and provide brief analysis
- **워치리스트 확인**: Run fetch with `--scope watchlist` and display
- **마무리**: "감사합니다. 다음에 시장 분석이 필요하면 말씀해주세요!"

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
