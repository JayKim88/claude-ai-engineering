---
name: market-pulse
description: Financial market analysis dashboard with value investing tools. Use when user says "market overview", "market pulse", "stock market", "시장 분석", "주식 시장", "시장 현황", "증시 분석", "시장 브리핑", "가치투자", "안전마진", "PEG 스크리닝", "기업 분석", or wants to check financial markets, stocks, crypto, or analyze stocks using Graham/Lynch/Buffett strategies.
version: 2.0.0
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

# Option 1: With automatic insights (Recommended)
python3 {path_to_fetch_market.py} --scope {scope} --output json --with-analysis > $TEMP_JSON

# Option 2: Without insights (will need manual Phase 3)
# python3 {path_to_fetch_market.py} --scope {scope} --output json > $TEMP_JSON
```

**Note**: `--with-analysis` flag automatically generates data-driven insights, eliminating the need for manual Phase 3. The insights are based on heuristics and will be displayed in the HTML dashboard.

**2-3. Error handling:**
- If script not found: inform user of the path issue and suggest reinstalling
- If script fails: show error and suggest checking internet connection
- If partial data: proceed with available data, note missing sections

---

### Step 3: Branch by Scope

**For `overview` or `deep` scope** → Go to Step 4 (Multi-Agent Pipeline)

**For single-market scope (`us`, `kr`, `crypto`)** → Go to Step 5-Single

**For `watchlist` scope** → Go to Step 5-Watchlist

**For value investing analysis (`value`, `안전마진`, `garp`, `deep-dive`)** → Go to Step 5-Value

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

**CRITICAL**: After Phase 2 synthesis completes, you MUST add all agent analysis results to the JSON file before proceeding to Step 6. This ensures the HTML dashboard includes AI insights, not just raw data.

**Instructions**:
1. Save each agent's output to temporary files during Phase 1 & 2
2. Read the agent outputs and add them to the JSON using Python
3. Verify the JSON contains the 'analysis' section

**Method 1: Save to temp files (Recommended)**

During Phase 1, save each agent output:
```python
# After us-market-analyzer completes
us_analysis = """[paste the full output from us-market-analyzer agent]"""
with open('/tmp/us_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(us_analysis)

# After kr-market-analyzer completes
kr_analysis = """[paste the full output from kr-market-analyzer agent]"""
with open('/tmp/kr_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(kr_analysis)

# After crypto-macro-analyzer completes
crypto_analysis = """[paste the full output from crypto-macro-analyzer agent]"""
with open('/tmp/crypto_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(crypto_analysis)
```

After Phase 2, save synthesis:
```python
synthesis = """[paste the full output from market-synthesizer agent]"""
with open('/tmp/synthesis.txt', 'w', encoding='utf-8') as f:
    f.write(synthesis)
```

Then add all analysis to JSON:
```python
import json

# Read JSON
with open(TEMP_JSON, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read analysis files
with open('/tmp/us_analysis.txt', 'r', encoding='utf-8') as f:
    us_market = f.read()
with open('/tmp/kr_analysis.txt', 'r', encoding='utf-8') as f:
    kr_market = f.read()
with open('/tmp/crypto_analysis.txt', 'r', encoding='utf-8') as f:
    crypto_macro = f.read()
with open('/tmp/synthesis.txt', 'r', encoding='utf-8') as f:
    synthesis = f.read()

# Add analysis section
data['analysis'] = {
    'us_market': us_market,
    'kr_market': kr_market,
    'crypto_macro': crypto_macro,
    'synthesis': synthesis
}

# Save updated JSON
with open(TEMP_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Analysis added to JSON")
```

**Method 2: Direct inline (Alternative)**

If you prefer, you can directly paste the agent outputs into a Python script:
```bash
python3 << 'EOF'
import json

# Read original JSON
with open("$TEMP_JSON", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add analysis (paste actual agent outputs here)
data['analysis'] = {
    'us_market': """[paste us-market-analyzer output]""",
    'kr_market': """[paste kr-market-analyzer output]""",
    'crypto_macro': """[paste crypto-macro-analyzer output]""",
    'synthesis': """[paste market-synthesizer output]"""
}

# Save
with open("$TEMP_JSON", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Analysis saved")
EOF
```

**Verification**:
```bash
# Verify analysis was added
grep -c '"analysis"' $TEMP_JSON
# Should output: 1

# Preview synthesis
python3 -c "import json; data=json.load(open('$TEMP_JSON')); print(data['analysis']['synthesis'][:200])"
```

**IMPORTANT**: Do NOT skip Phase 3! If you skip it, the HTML dashboard will only show data tables without any AI insights or investment recommendations.

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

### Step 5-Value: Value Investing Analysis (Phase 2.5)

**NEW in v2.0**: Analyze stocks using investment masters' strategies (Graham, Lynch, Buffett, Munger, Asness, Dalio, Fisher).

**Trigger phrases:**
- "가치투자 분석", "안전마진 분석", "저평가 종목"
- "PEG 스크리닝", "GARP 종목", "린치 분석"
- "기업 심층 분석", "[TICKER] 분석해줘"

**Analysis Types:**

**1. Safety Margin Analysis (안전마진 - Graham/Buffett)**
```bash
python3 {path_to}/analysis/value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL,NVDA,META,TSLA,AMZN" \
  --analysis safety_margin
```

Output: 저평가 종목 (안전마진 20%+) with intrinsic value, current price, safety margin %, recommendation.

**2. GARP Screening (Growth At Reasonable Price - Lynch)**
```bash
python3 {path_to}/analysis/value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL,NVDA,META" \
  --analysis garp
```

Output: GARP 종목 (PEG < 1.0, growth >= 10%) with category, PEG ratio, growth rate, ROE, recommendation.

**3. Company Deep Dive (8-Perspective Analysis)**
```bash
python3 {path_to}/analysis/company_deep_dive.py
```

Then provide single ticker when prompted. Generates comprehensive report with:
- Graham: Safety margin & intrinsic value
- Buffett: Economic moat strength
- Lynch: GARP category & PEG
- Munger: Risk analysis (inversion thinking)
- Asness: Factor scores (Value, Quality, Momentum)
- Dalio: Economic cycle positioning
- Fisher: Qualitative analysis (Scuttlebutt)
- Overall: Comprehensive score, risk-reward ratio, final recommendation

**4. All-in-One Analysis**
```bash
python3 {path_to}/analysis/value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL" \
  --analysis all \
  --output /tmp/value-analysis-{timestamp}.json
```

**Display Format:**

Present results in markdown tables:

**안전마진 Top 10 (Safety Margin)**
| 종목 | 회사명 | 현재가 | 내재가치 | 안전마진 | 추천 |
|------|--------|--------|----------|----------|------|
| MSFT | Microsoft | $404.37 | $2,045.76 | 80.2% | 강력 매수 |
| NVDA | NVIDIA | $190.05 | $574.70 | 66.9% | 강력 매수 |

**GARP 종목 (PEG < 1.0)**
| 종목 | 카테고리 | PEG | 성장률 | ROE | 추천 |
|------|----------|-----|--------|-----|------|
| MSFT | 고성장주 | 0.36 | 59.8% | 34.4% | 강력 매수 |
| NVDA | 고성장주 | 0.37 | 66.7% | 107.4% | 강력 매수 |

**Notes:**
- Safety margin analysis uses Graham formula: IV = EPS × (8.5 + 2g)
- GARP screening combines value (PEG < 1.0) + growth (earnings growth >= 10%)
- Deep dive provides 8 different investment perspectives for comprehensive due diligence
- All analysis uses yfinance data (15-20 min delayed)

Go to Step 6.

---

### Step 6: Generate HTML Dashboard and Auto-Open

**6-1. Display Terminal Summary**

Present a brief summary of the analysis in the terminal (key takeaways only, 5-10 lines).

**6-2. Generate Interactive HTML Dashboard**

**Before generating HTML, verify JSON contains AI analysis**:
```bash
# Check if analysis section exists
if grep -q '"analysis"' "$TEMP_JSON"; then
    echo "✅ Analysis found in JSON"
else
    echo "⚠️  WARNING: JSON missing 'analysis' section - HTML will show data only, no insights!"
    echo "Did you complete Step 4 Phase 3? The dashboard needs AI analysis for investment insights."
fi
```

Automatically generate HTML dashboard with visualizations (auto-named with timestamp):

```bash
# Locate generate_html.py (same directory as fetch_market.py)
# Output path will be auto-generated: /tmp/market-pulse-YYYYMMDD-HHMMSS.html
HTML_OUTPUT=$(python3 {path_to_generate_html.py} --input $TEMP_JSON)
```

**What the HTML includes**:
- **If analysis exists**: Full AI insights section with key takeaways, investment strategies, cross-market analysis
- **If analysis missing**: Data tables and charts only (no investment recommendations)

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

**Market Overview (English):**
- "market overview"
- "market pulse"
- "stock market analysis"
- "how are the markets doing"
- "check the markets"
- "financial dashboard"

**Market Overview (Korean):**
- "시장 분석"
- "주식 시장"
- "시장 현황"
- "오늘 시장 어때"
- "증시 분석"
- "시장 브리핑"

**Value Investing Analysis (NEW in v2.0):**
- "가치투자 분석"
- "안전마진 분석" / "safety margin"
- "저평가 종목" / "undervalued stocks"
- "PEG 스크리닝" / "GARP screening"
- "린치 분석" / "Lynch analysis"
- "[TICKER] 기업 분석" / "analyze [TICKER]"
- "[TICKER] 내재가치" / "intrinsic value of [TICKER]"
- "심층 분석" / "deep dive"

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

### Example 4: Value Investing Analysis (NEW v2.0)

```
User: "안전마진 분석해줘" or "저평가 종목 찾아줘"
→ Ask for tickers: "어떤 종목들을 분석하시겠습니까? (쉼표로 구분)"
User: "AAPL, MSFT, GOOGL, NVDA, META"
→ Run: value_investing_analyzer.py --tickers "AAPL,MSFT,GOOGL,NVDA,META" --analysis safety_margin
→ Display table with safety margins (80.2% MSFT, 66.9% NVDA, 59.4% GOOGL)
→ "MSFT, NVDA, GOOGL이 20% 이상 저평가되어 있습니다."
```

```
User: "AAPL 기업 분석해줘"
→ Run: company_deep_dive.py (single ticker analysis)
→ Display comprehensive 8-perspective report
   - Graham: 22.8% safety margin (HOLD)
   - Buffett: Wide moat (100/100)
   - Lynch: Fast Grower, PEG 1.62 (expensive)
   - Munger: Low risk (15/100), high survivability (85/100)
   - Asness: Weak factor scores (27.5/100)
   - Overall: 69.3/100, "조건부 매수", 1-3 year horizon
→ "추가로 다른 종목을 분석하시겠습니까?"
```

```
User: "PEG 스크리닝해줘" or "GARP 종목 찾아줘"
→ Ask for tickers
User: "테크 대장주들"
→ Interpret: AAPL, MSFT, GOOGL, NVDA, META, AMZN, TSLA
→ Run: value_investing_analyzer.py --tickers "..." --analysis garp
→ Display GARP stocks (PEG < 1.0):
   - MSFT: PEG 0.36, 성장률 59.8%
   - NVDA: PEG 0.37, 성장률 66.7%
   - GOOGL: PEG 0.75, 성장률 31.1%
→ "3개 GARP 종목 발견 (Growth At Reasonable Price)"
```
