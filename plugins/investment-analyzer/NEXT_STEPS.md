# Investment Analyzer - Next Steps

**Current Status**: Week 1 Complete ✅
**Next Phase**: Week 2 - Company Scorecard Engine
**Timeline**: 7 days

---

## 🎯 Week 2 Objectives (Days 8-14)

Build the **Company Scorecard Engine** - a comprehensive stock analysis system that combines quantitative metrics with AI-powered insights.

### Goal
Create a scoring system that evaluates stocks across three dimensions:
1. **Financial Health** (0-10 points)
2. **Valuation** (0-10 points)
3. **Momentum** (0-10 points)

**Total Score**: Weighted average (Financial 40% + Valuation 30% + Momentum 30%)

---

## 📋 Week 2 Task Breakdown

### Task 1: Company Scorecard Generator (Days 8-9)
**Priority**: HIGH
**Estimated Time**: 2 days
**File to Create**: `scripts/scorecard.py`

#### Implementation Details

**A. Financial Score (0-10)**

**Components**:
1. **Profitability** (40% weight)
   - ROE (Return on Equity)
   - Operating Margin
   - Net Profit Margin

2. **Growth** (30% weight)
   - Revenue YoY growth
   - Operating Income YoY growth

3. **Stability** (30% weight)
   - Debt-to-Equity ratio (lower is better)
   - Current Ratio (liquidity)

**Data Sources**:
- US stocks: yfinance financials (or MCP if available)
- Korean stocks: pykrx basic data (Phase 2: DART API)

**Scoring Algorithm**:
```python
def calculate_financial_score(ticker):
    financials = get_financials(ticker)

    # Profitability (0-10)
    roe_score = normalize(roe, excellent=20%, good=15%, acceptable=10%)
    margin_score = normalize(operating_margin + net_margin)
    profitability = (roe_score + margin_score) / 2

    # Growth (0-10)
    growth = normalize(revenue_yoy * 0.6 + operating_income_yoy * 0.4)

    # Stability (0-10)
    stability = normalize(1 / debt_ratio * 0.5 + current_ratio * 0.5)

    # Weighted average
    return 0.4 * profitability + 0.3 * growth + 0.3 * stability
```

---

**B. Valuation Score (0-10)**

**Components**:
1. **Sector Relative Valuation** (60% weight)
   - Current P/E vs Sector Average P/E
   - Current P/B vs Sector Average P/B
   - Current P/S vs Sector Average P/S

2. **Historical Valuation** (40% weight)
   - Current P/E vs 3-year average P/E
   - Current P/B vs 3-year average P/B

**Scoring Logic**:
- **Lower valuation = Higher score** (undervalued stocks get high scores)
- Discount to sector/history → 8-10 points
- In line with sector/history → 5-7 points
- Premium to sector/history → 0-4 points

**Data Required**:
- Current ratios: yfinance/MCP
- Sector averages: Calculate from sector constituents
- Historical ratios: yfinance historical data (3 years)

---

**C. Momentum Score (0-10)**

**Components**:
1. **Moving Average Alignment** (40% weight)
   - Price > MA20 > MA60 > MA120 (perfect alignment = 10 points)
   - Each condition met = +2.5 points

2. **RSI (Relative Strength Index)** (30% weight)
   - Ideal range: 40-60 (neutral, sustainable)
   - Overbought (>70) or oversold (<30) = penalty

3. **MACD Signal** (20% weight)
   - MACD > Signal line = bullish (+5 points)
   - Golden cross recently = bonus

4. **Volume Trend** (10% weight)
   - Increasing volume on up days = positive

**Data Required**:
- Historical prices: 120 days minimum
- Technical library: TA-Lib or pandas_ta

**Dependencies to Install**:
```bash
pip3 install pandas-ta  # For technical indicators
```

---

**D. Total Score Calculation**

```python
total_score = (
    financial_score * 0.40 +
    valuation_score * 0.30 +
    momentum_score * 0.30
)
```

**Score Interpretation**:
- **9.0-10.0**: Exceptional (strong buy candidate)
- **8.0-8.9**: Excellent (buy candidate)
- **7.0-7.9**: Good (hold or accumulate)
- **6.0-6.9**: Fair (monitor)
- **5.0-5.9**: Weak (caution)
- **0.0-4.9**: Poor (avoid or sell)

---

### Task 2: Outlier Detector (Day 9)
**Priority**: HIGH
**Estimated Time**: 0.5 days
**File to Create**: `scripts/outlier_detector.py`

#### Purpose
Validate data quality before analysis to prevent garbage-in-garbage-out.

#### Implementation

**A. Price Outliers**
```python
def detect_price_outliers(ticker, window=90):
    prices = get_historical_prices(ticker, days=window)
    returns = prices.pct_change()

    # Z-score method
    z_scores = (returns - returns.mean()) / returns.std()

    outliers = []
    for date, z in z_scores.items():
        if abs(z) > 3:  # |Z| > 3 = outlier
            outliers.append({
                'date': date,
                'return': returns[date],
                'z_score': z,
                'severity': 'high' if abs(z) > 4 else 'medium'
            })

    return outliers
```

**B. Financial Data Outliers**
```python
def validate_financials(ticker):
    current = get_financials(ticker, quarter='latest')
    previous = get_financials(ticker, quarter='previous')

    issues = []

    for metric in ['revenue', 'operating_income', 'net_income']:
        change = abs(current[metric] - previous[metric]) / previous[metric]
        if change > 1.0:  # 100%+ change QoQ
            issues.append({
                'metric': metric,
                'change_pct': change * 100,
                'current': current[metric],
                'previous': previous[metric]
            })

    # Negative equity check
    if current.get('equity', 0) < 0:
        issues.append({'metric': 'equity', 'issue': 'negative_equity'})

    return issues
```

**C. Missing Data Handling**
- **Critical data missing** (e.g., no price): Skip stock, return error
- **Non-critical missing** (e.g., P/S ratio): Impute or exclude from score

---

### Task 3: Analyze-Stock Skill (Day 10)
**Priority**: HIGH
**Estimated Time**: 1 day
**File to Create**: `skills/analyze-stock/SKILL.md`

#### Skill Definition

**Trigger**: `/analyze-stock [TICKER]`

**Execution Flow**:
```
1. Parse ticker from user input
2. Detect market (US/KR)
3. Fetch comprehensive data:
   - Stock info (price, sector, market cap)
   - Financial statements
   - Historical prices (120 days)
4. Run outlier detection
5. Calculate scorecard:
   - Financial score
   - Valuation score
   - Momentum score
   - Total score
6. Display terminal output:
   - Header (company name, ticker, price)
   - Score breakdown (bar charts)
   - Key metrics table
   - Warnings/flags
7. Return scorecard object for next step
```

**Terminal Output Format**:
```
════════════════════════════════════════
Apple Inc. (AAPL) Stock Analysis
════════════════════════════════════════

📈 Current Price: $273.68 (+1.2%)
💰 Market Cap: $4.2T
🏢 Sector: Technology

🏆 Overall Score: 8.5 / 10 ⭐⭐⭐

Score Breakdown:
─────────────────────────────────────────
Financial Health:  9.2 / 10  ████████████████████
Valuation:         7.5 / 10  ███████████████░░░░░
Momentum:          8.8 / 10  ██████████████████░░

💰 Financial Metrics
─────────────────────────────────────────
ROE:              28.5%  (Industry: 22.1%)
Operating Margin: 30.2%  (Excellent)
Debt/Equity:      1.8    (Stable)
Revenue Growth:   8.3% YoY

📊 Valuation
─────────────────────────────────────────
P/E Ratio:  34.6   (Sector: 28.5, Historic: 30.2)
P/B Ratio:  8.2    (Sector: 6.5)
Status:     Slight Premium (+21% vs sector)

📈 Technical Indicators
─────────────────────────────────────────
MA Alignment:  ✅ Perfect (Price > MA20 > MA60 > MA120)
RSI(14):       62.5      ⚠️  Approaching overbought
MACD:          Golden Cross ✅

⚠️  Warnings
─────────────────────────────────────────
• Valuation premium to sector (consider entry timing)
• RSI elevated, potential short-term pullback

Next: Use /portfolio add AAPL [qty] [price] to add to portfolio
```

---

### Task 4: AI Company Analyst Agent (Days 11-12)
**Priority**: HIGH
**Estimated Time**: 2 days
**File to Create**: `agents/company-analyst.md`

#### Agent Specification

**Model**: Opus 4.6 (for nuanced analysis)

**Agent Role**: AI Stock Analyst

**Input**:
- Scorecard data (all 3 scores + metrics)
- Financial statements (latest quarter)
- Recent news headlines (top 5)
- Valuation comparison data
- Technical indicators

**Output**: Comprehensive narrative analysis

**Prompt Structure**:
```markdown
You are an expert stock analyst. Analyze the following stock data and provide investment insights.

# Company: {company_name} ({ticker})

## Scorecard
- Overall Score: {total_score}/10
- Financial Score: {financial_score}/10
- Valuation Score: {valuation_score}/10
- Momentum Score: {momentum_score}/10

## Financial Metrics
{financial_data}

## Valuation
{valuation_data}

## Technical Indicators
{technical_data}

## Recent News
{news_headlines}

## Task
Provide a comprehensive analysis with:
1. **Strengths** (3-5 bullet points)
2. **Weaknesses** (3-5 bullet points)
3. **Key Risks** (2-3 risks)
4. **Investment Idea** (1 paragraph: bull case, bear case, recommendation for different investor types)

## Constraints
- Be objective and data-driven
- Highlight data quality issues if any
- Include disclaimer: "This is informational analysis, not investment advice"
- Keep analysis under 300 words
```

**Integration**:
```python
# In analyze-stock skill
scorecard = calculate_scorecard(ticker)
ai_analysis = run_agent('company-analyst', scorecard)
print(ai_analysis)
```

---

### Task 5: HTML Stock Report (Days 12-13)
**Priority**: MEDIUM
**Estimated Time**: 1.5 days
**File to Create**: `scripts/stock_report_generator.py`

#### Features

**A. Report Sections**
1. Header (company name, ticker, price, score badge)
2. Score visualization (horizontal bar charts with Chart.js)
3. Financial metrics table
4. Valuation comparison chart
5. Price chart with MA overlays
6. AI analysis section
7. Data sources footer
8. Disclaimer

**B. Chart.js Visualizations**
- Score bars (color-coded: green >8, yellow 6-8, red <6)
- Historical P/E trend line
- Price + MA20/60/120 line chart

**C. Styling**
- Clean, professional design (similar to market-pulse)
- Responsive (mobile-friendly)
- Dark mode toggle (optional)

**D. Auto-open in Browser**
```python
import webbrowser

html_file = f"/tmp/stock-analysis-{ticker}-{timestamp}.html"
generate_html_report(scorecard, ai_analysis, html_file)
webbrowser.open(f"file://{html_file}")
```

---

### Task 6: End-to-End Testing (Day 14)
**Priority**: HIGH
**Estimated Time**: 1 day

#### Test Scenarios

**A. US Stock Analysis**
```bash
python portfolio_manager.py /analyze-stock AAPL
python portfolio_manager.py /analyze-stock MSFT
python portfolio_manager.py /analyze-stock NVDA
```

**Expected**:
- ✅ Scorecard calculated
- ✅ AI analysis generated
- ✅ HTML report opened
- ✅ No errors

**B. Korean Stock Analysis**
```bash
python portfolio_manager.py /analyze-stock 005930  # Samsung
```

**Expected**:
- ✅ pykrx data fetched
- ✅ Scorecard (financial may be limited)
- ✅ Analysis completed

**C. Edge Cases**
- Invalid ticker → Error message
- Insufficient data (newly listed stock) → Partial scorecard
- Data outlier detected → Warning displayed

**D. Validation**
- Compare AI analysis quality across 10 stocks
- Verify score accuracy (manually check 3 stocks)
- Test HTML rendering on mobile

---

## 📦 New Dependencies for Week 2

```bash
# Technical analysis library
pip3 install pandas-ta

# Or alternative:
pip3 install ta-lib  # Requires compilation, pandas-ta is easier
```

---

## 🎯 Week 2 Success Criteria

- [ ] Scorecard generator produces scores for any US/KR stock
- [ ] Financial, valuation, momentum scores are reasonable (spot-check 5 stocks)
- [ ] Outlier detector catches anomalies (test with known outliers)
- [ ] `/analyze-stock` skill works end-to-end
- [ ] AI analyst provides valuable insights (subjective but testable)
- [ ] HTML reports are professional and informative
- [ ] 10+ stocks analyzed successfully without errors

---

## 🔧 Technical Debt to Address

1. **MCP Integration**: When MCP session is active, switch from yfinance to MCP for US stocks
2. **Korean Financials**: Currently limited to pykrx data (Phase 2: add DART API)
3. **Sector Averages**: Need to calculate or fetch sector P/E averages (Phase 2)
4. **Caching**: Implement data_cache table usage (currently only in-memory)

---

## 📚 Reference Files for Week 2

**Patterns to Follow**:
- `plugins/market-pulse/config/generate_html.py` - HTML generation pattern
- `plugins/market-pulse/agents/market-synthesizer.md` - Agent prompt pattern

**Data Sources**:
- yfinance documentation: https://pypi.org/project/yfinance/
- pandas-ta documentation: https://github.com/twopirllc/pandas-ta

---

## ⏭️ Preview: Week 3-4

**Week 3**: AI Analysis & Portfolio Integration
- Integrate scorecard into portfolio review
- Portfolio-level insights
- HTML dashboard with all holdings scored

**Week 4**: Validation & Polish
- Comprehensive testing
- Bug fixes
- Documentation
- Week 1-4 retrospective

---

## 💡 Tips for Week 2

1. **Start with scorecard.py**: This is the foundation for everything else
2. **Test incrementally**: Test each score (financial, valuation, momentum) separately
3. **Use real data**: Test with diverse stocks (tech, finance, healthcare, Korean)
4. **Keep AI prompts concise**: Opus is powerful but expensive, optimize tokens
5. **Cache aggressively**: Stock data doesn't change minute-to-minute, cache for hours

---

**Ready to begin Week 2?** Start with `scripts/scorecard.py` and work through each task sequentially.
