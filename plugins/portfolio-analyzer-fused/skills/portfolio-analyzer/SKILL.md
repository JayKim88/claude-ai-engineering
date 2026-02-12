---
name: portfolio-analyzer
description: AI-powered portfolio management with multi-agent analysis. Use when user says "analyze portfolio", "check stocks", "portfolio review", or similar investment-related requests.
version: 1.0.0
---

# Portfolio Analyzer Skill

## Trigger Phrases

**English:**
- "analyze my portfolio"
- "portfolio review"
- "analyze stock TICKER"
- "find investment opportunities"
- "check portfolio risk"
- "portfolio dashboard"
- "talk about my investments"

**Korean:**
- "포트폴리오 분석해줘"
- "주식 분석"
- "투자 기회 찾아줘"
- "포트폴리오 리스크"
- "포트폴리오 대시보드"

## When to Use

- Stock research and deep-dive analysis
- Portfolio performance review and visualization
- Investment opportunity discovery (undervalued stocks)
- Risk assessment and correlation analysis
- Investment advisory conversations
- Portfolio rebalancing suggestions

## Execution Algorithm

### Step 1: Intent Detection

Parse user request to determine which command to execute:

```python
if user_request contains ticker symbol (e.g., "AAPL", "TSLA"):
    command = "analyze-stock"
elif "review" or "dashboard" or "show portfolio":
    command = "portfolio-review"
elif "opportunity" or "find" or "discover" or "undervalued":
    command = "find-opportunities"
elif "risk" or "volatility" or "correlation" or "beta":
    command = "portfolio-risk"
elif conversational_question about portfolio:
    command = "portfolio-chat"
else:
    # Ask user for clarification
    command = "portfolio-review"  # Default to review
```

### Step 2: Route to Appropriate Sub-Algorithm

Based on detected intent, execute one of five command algorithms:

1. **analyze-stock**: Deep AI analysis of a single stock
2. **portfolio-review**: Comprehensive portfolio overview with dashboard
3. **find-opportunities**: Discover undervalued stocks and rebalancing ideas
4. **portfolio-risk**: Risk metrics and scenario analysis
5. **portfolio-chat**: AI conversational portfolio advisor

---

## Command 1: analyze-stock

**Purpose**: Perform comprehensive AI-powered analysis of a single stock with scoring and strategic insights.

**Trigger**: User request contains a stock ticker symbol (e.g., "analyze AAPL", "tell me about TSLA")

### Algorithm

#### Phase 1: Data Fetching (Sequential)

```python
# Step 1.1: Extract ticker from user input
ticker = extract_ticker_from_input(user_request)

if not ticker:
    ask_user("What stock ticker would you like to analyze?")
    ticker = user_response.upper()

# Step 1.2: Fetch stock data (multi-source)
result = Bash(f"python3 scripts/fetch_stock_data.py {ticker}")

if result.returncode != 0:
    inform_user(f"❌ Could not fetch data for {ticker}. Please verify the ticker symbol.")
    return

stock_data = parse_json(result.stdout)
```

#### Phase 2: Scoring (Sequential)

```python
# Step 2.1: Calculate investment score
result = Bash(f"python3 scripts/calculate_score.py {ticker} --save")

if result.returncode != 0:
    inform_user("⚠️  Scoring failed, but proceeding with available data...")
    score_data = None
else:
    score_data = parse_json(result.stdout)
```

#### Phase 3: Strategic Analysis (Opus Agent)

```python
# Step 3.1: Launch Strategic Advisor (Opus for deep reasoning)
strategic_insight = Task(
    subagent_type="strategic-advisor",
    model="opus",
    description="Generate investment thesis",
    prompt=f"""
    Analyze {ticker} and provide strategic investment insights.

    ## Stock Data
    {stock_data}

    ## Scoring Results
    {score_data}

    Provide:
    1. Executive Summary (2-3 sentences)
    2. Bull Case (3-5 points)
    3. Bear Case (3-5 points)
    4. Investment Thesis
    5. Recommendation (BUY/HOLD/SELL) with conviction level
    6. 12-month price target estimate
    """
)
```

#### Phase 4: Present Report

```python
# Step 4.1: Format and display comprehensive report
display_to_user(f"""
# Investment Analysis: {ticker}

## Company Overview
{stock_data['company']['name']} - {stock_data['company']['sector']}
Current Price: ${stock_data['price']['current']}

## Investment Score: {score_data['overall_score']}/10 ({score_data['grade']})

### Component Scores
- Financial Health: {score_data['component_scores']['financial_health']}/10
- Valuation: {score_data['component_scores']['valuation']}/10
- Momentum: {score_data['component_scores']['momentum']}/10

{strategic_insight}

---
💡 Add to portfolio: `python3 scripts/add_to_portfolio.py {ticker} buy <shares> <price>`
""")
```

**Duration**: 30-60 seconds

---

## Command 2: portfolio-review

**Purpose**: Generate comprehensive portfolio overview with interactive HTML dashboard.

**Trigger**: "portfolio review", "show portfolio", "dashboard"

### Algorithm

#### Phase 1: Data Collection (Sequential)

```python
# Step 1.1: Query portfolio holdings
result = Bash("python3 scripts/query_portfolio.py --format json --with-scores")

if result.returncode != 0:
    inform_user("❌ Failed to load portfolio. Run init_portfolio.py first.")
    return

portfolio_data = parse_json(result.stdout)

if portfolio_data['summary']['count'] == 0:
    inform_user("📭 Portfolio is empty. Add holdings with add_to_portfolio.py")
    return
```

#### Phase 2: Score Update (Parallel)

```python
# Step 2.1: Update scores for all holdings in parallel
holdings = portfolio_data['holdings']

# Launch scoring tasks in parallel for faster execution
scoring_tasks = []
for holding in holdings:
    ticker = holding['ticker']
    task_id = Task(
        subagent_type="market-analyst",
        model="sonnet",
        description=f"Score {ticker}",
        prompt=f"Run: python3 scripts/calculate_score.py {ticker} --save"
    )
    scoring_tasks.append(task_id)

# Wait for all scoring tasks to complete
wait_for_all(scoring_tasks)
```

#### Phase 3: Dashboard Generation (Sequential)

```python
# Step 3.1: Generate HTML dashboard
result = Bash("python3 scripts/generate_dashboard.py")

if result.returncode == 0:
    inform_user("✅ Dashboard generated and opened in browser")
else:
    inform_user("⚠️  Dashboard generation failed")
```

#### Phase 4: Summary Display

```python
# Step 4.1: Display text summary to user
summary = portfolio_data['summary']

display_to_user(f"""
# 📊 Portfolio Review

## Summary
- Total Value: ${summary['total_value']:,.2f}
- Total P&L: ${summary['total_pl']:,.2f} ({summary['total_pl_pct']:+.2f}%)
- Holdings: {summary['count']} stocks

## Top Holdings
{format_top_holdings(holdings[:5])}

## Dashboard
Interactive HTML dashboard opened in browser with:
- Sector allocation chart
- Score distribution chart
- Holdings table with scores
- Performance metrics

---
💡 Next steps:
- Update prices: `python3 scripts/update_prices.py`
- Find opportunities: Use /find-opportunities
- Check risk: Use /portfolio-risk
""")
```

**Duration**: 45-90 seconds (depends on number of holdings)

---

## Command 3: find-opportunities

**Purpose**: Discover undervalued stocks and rebalancing suggestions using AI-powered screening.

**Trigger**: "find opportunities", "discover undervalued stocks", "rebalancing ideas"

### Algorithm

#### Phase 1: Portfolio Analysis (Sequential)

```python
# Step 1.1: Load current portfolio
result = Bash("python3 scripts/query_portfolio.py --format json --with-scores")
portfolio_data = parse_json(result.stdout)

# Step 1.2: Load target allocation from config
config = read_yaml("config/portfolio.yaml")
target_allocation = config['allocation']
```

#### Phase 2: Opportunity Scanning (Parallel)

```python
# Step 2.1: Define screening criteria
screening_criteria = {
    'min_score': config['preferences']['min_stock_score'],
    'max_pe': 25,
    'min_roe': 0.10,
    'sectors': config['preferences']['excluded_sectors']
}

# Step 2.2: Scan for opportunities (could expand to screen broader universe)
# For now, focus on improving existing holdings

opportunities = []

for holding in portfolio_data['holdings']:
    ticker = holding['ticker']
    score = holding['overall_score']

    if score and score < screening_criteria['min_score']:
        opportunities.append({
            'type': 'SELL',
            'ticker': ticker,
            'reason': f'Score {score:.1f} below threshold {screening_criteria["min_score"]}',
            'priority': 'High' if score < 5.0 else 'Medium'
        })
```

#### Phase 3: Rebalancing Analysis (Sequential)

```python
# Step 3.1: Calculate current allocation
current_allocation = calculate_allocation(portfolio_data)

# Step 3.2: Compare to target allocation
allocation_drift = []

for sector, target_pct in target_allocation['sectors'].items():
    current_pct = current_allocation.get(sector, 0)
    drift = current_pct - target_pct

    if abs(drift) > config['risk']['rebalance_threshold']:
        allocation_drift.append({
            'sector': sector,
            'current': current_pct,
            'target': target_pct,
            'drift': drift,
            'action': 'REDUCE' if drift > 0 else 'ADD'
        })
```

#### Phase 4: AI Opportunity Prioritization (Sonnet Agent)

```python
# Step 4.1: Get AI recommendations
recommendations = Task(
    subagent_type="opportunity-scanner",
    model="sonnet",
    description="Prioritize opportunities",
    prompt=f"""
    Analyze the following investment opportunities and rebalancing needs.

    ## Current Portfolio
    {portfolio_data}

    ## Identified Opportunities
    {opportunities}

    ## Allocation Drift
    {allocation_drift}

    ## User Preferences
    Risk Tolerance: {config['preferences']['risk_tolerance']}
    Investment Style: {config['preferences']['investment_style']}

    Provide:
    1. Top 3 actionable recommendations (prioritized)
    2. Rationale for each recommendation
    3. Suggested timing and position sizing
    4. Risk considerations
    """
)
```

#### Phase 5: Present Recommendations

```python
display_to_user(f"""
# 💡 Investment Opportunities

{recommendations}

## Allocation Drift Analysis
{format_allocation_table(allocation_drift)}

---
💡 To execute:
- Add holding: `python3 scripts/add_to_portfolio.py TICKER buy <shares> <price>`
- Reduce holding: `python3 scripts/add_to_portfolio.py TICKER sell <shares> <price>`
""")
```

**Duration**: 60-90 seconds

---

## Command 4: portfolio-risk

**Purpose**: Calculate and analyze portfolio risk metrics (beta, volatility, VaR, correlation).

**Trigger**: "portfolio risk", "check volatility", "risk analysis"

### Algorithm

#### Phase 1: Calculate Metrics (Sequential)

```python
# Step 1.1: Calculate portfolio-level risk metrics
result = Bash("python3 scripts/calculate_portfolio_metrics.py --format json")

if result.returncode != 0:
    inform_user("❌ Failed to calculate risk metrics")
    return

metrics = parse_json(result.stdout)
```

#### Phase 2: Risk Interpretation (Sonnet Agent)

```python
# Step 2.1: Get AI risk assessment
risk_assessment = Task(
    subagent_type="risk-assessor",
    model="sonnet",
    description="Interpret risk metrics",
    prompt=f"""
    Interpret the following portfolio risk metrics and provide actionable insights.

    ## Portfolio Metrics
    {metrics}

    ## User Configuration
    Risk Tolerance: {config['preferences']['risk_tolerance']}
    Max Position Size: {config['risk']['max_position_size']}%
    Max Sector Weight: {config['risk']['max_sector_weight']}%

    Provide:
    1. Overall risk assessment (Low/Medium/High)
    2. Key risk concerns (concentration, volatility, correlation)
    3. Comparison to risk tolerance
    4. Actionable recommendations to reduce risk
    5. Scenarios to watch (market downturn, sector rotation)
    """
)
```

#### Phase 3: Present Risk Report

```python
display_to_user(f"""
# ⚠️ Portfolio Risk Analysis

## Metrics
- Portfolio Beta: {metrics['risk']['portfolio_beta']}
- Portfolio Volatility: {metrics['risk']['portfolio_volatility']}
- Max Position Weight: {metrics['concentration']['max_position_weight']}%
- Top 3 Holdings: {metrics['concentration']['top_3_weight']}%

## Risk Alerts
{check_risk_alerts(metrics, config)}

{risk_assessment}

---
💡 Risk management actions:
- Diversify: Use /find-opportunities
- Review: Use /portfolio-review
- Discuss: Use /portfolio-chat
""")
```

**Duration**: 45-60 seconds

---

## Command 5: portfolio-chat

**Purpose**: Multi-round conversational AI advisor for investment questions.

**Trigger**: Conversational questions about portfolio or investments

### Algorithm

#### Phase 1: Initialize Conversation (Sequential)

```python
# Step 1.1: Load portfolio context
result = Bash("python3 scripts/query_portfolio.py --format json --with-scores")
portfolio_data = parse_json(result.stdout)

result = Bash("python3 scripts/calculate_portfolio_metrics.py --format json")
metrics = parse_json(result.stdout)

# Step 1.2: Load conversation history from database
conn = sqlite3.connect("data/portfolio.db")
session_id = generate_session_id()

history = load_chat_history(conn, session_id, max_turns=10)
```

#### Phase 2: AI Advisor Response (Opus Agent)

```python
# Step 2.1: Get AI advisor response
advisor_response = Task(
    subagent_type="portfolio-advisor",
    model="opus",
    description="AI portfolio advisor",
    prompt=f"""
    You are an AI portfolio advisor. Answer the user's question with strategic insights.

    ## User Question
    {user_request}

    ## Portfolio Context
    {portfolio_data}

    ## Risk Metrics
    {metrics}

    ## Conversation History
    {history}

    ## User Preferences
    Risk Tolerance: {config['preferences']['risk_tolerance']}
    Investment Style: {config['preferences']['investment_style']}
    Time Horizon: {config['preferences']['time_horizon']}

    Provide thoughtful, personalized investment advice. Be conversational but professional.
    Ask clarifying questions if needed. Reference specific holdings when relevant.
    """
)
```

#### Phase 3: Save and Continue

```python
# Step 3.1: Save conversation to history
save_chat_message(conn, session_id, "user", user_request)
save_chat_message(conn, session_id, "assistant", advisor_response)

# Step 3.2: Display response
display_to_user(advisor_response)

# Step 3.3: Wait for follow-up
inform_user("💡 Ask follow-up questions or type 'exit' to end conversation")
```

**Duration**: 20-40 seconds per turn

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Ticker not found | Invalid symbol | Suggest similar tickers, ask user to verify |
| Database not found | init_portfolio.py not run | Inform user to run initialization script |
| Database locked | Concurrent access | Retry with exponential backoff (3 attempts) |
| API timeout | Network/rate limit | Use cached data if available, warn user |
| Agent task failed | Agent error | Log error, fall back to simpler analysis without AI |
| Empty portfolio | No holdings | Inform user, suggest adding holdings |
| Missing dependencies | yfinance/pykrx not installed | Display installation instructions |
| Scoring failed | Insufficient data | Proceed without scores, inform user |
| Dashboard generation failed | Template/data issue | Display text summary instead |

### Error Recovery Strategy

```python
def execute_with_retry(command, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            result = execute_command(command)
            if result.success:
                return result
        except DatabaseLocked:
            if attempt < max_retries - 1:
                time.sleep(backoff ** attempt)
            else:
                raise
        except Exception as e:
            log_error(e)
            if attempt == max_retries - 1:
                return fallback_behavior()
```

---

## Performance Optimization

### Parallel Execution

Commands that benefit from parallel agent execution:
- **portfolio-review**: Score multiple holdings simultaneously (Step 2.1)
- **find-opportunities**: Screen multiple stocks in parallel

### Caching Strategy

- Stock data: Cache for 1 hour (configured in portfolio.yaml)
- Scores: Persist in database, reuse if < 24 hours old
- Dashboard: Regenerate on demand

### Model Selection

- **Haiku**: Not used in this plugin (complexity requires Sonnet minimum)
- **Sonnet**: Data analysis, scoring, opportunity scanning, risk assessment (cost-efficient)
- **Opus**: Strategic advisor, portfolio advisor (deep reasoning, 2 of 6 agents)

---

## Configuration

All behavior is customizable via `/plugins/portfolio-analyzer-fused/config/`:

- `portfolio.yaml`: Target allocation, risk parameters, user preferences
- `scoring.yaml`: Scoring weights and thresholds
- `schema.sql`: Database structure

---

## Quick Reference

### Usage

```bash
# In Claude Code conversation:
/analyze-stock AAPL
/portfolio-review
/find-opportunities
/portfolio-risk
/portfolio-chat

# Or natural language:
"analyze apple stock"
"show me my portfolio dashboard"
"find undervalued stocks"
"what's my portfolio risk?"
"should I rebalance?"
```

### Python Scripts (Direct Usage)

```bash
# Initialize
python3 scripts/init_portfolio.py

# Add holding
python3 scripts/add_to_portfolio.py AAPL buy 10 150.00

# Query
python3 scripts/query_portfolio.py --with-scores

# Update prices
python3 scripts/update_prices.py

# Score stock
python3 scripts/calculate_score.py TSLA --save

# Risk metrics
python3 scripts/calculate_portfolio_metrics.py

# Dashboard
python3 scripts/generate_dashboard.py
```

### Expected Duration

- `analyze-stock`: 30-60 seconds
- `portfolio-review`: 45-90 seconds (scales with holdings)
- `find-opportunities`: 60-90 seconds
- `portfolio-risk`: 45-60 seconds
- `portfolio-chat`: 20-40 seconds per turn

---

## Legal Disclaimer

⚠️ **IMPORTANT**: This tool provides informational analysis only and does NOT constitute investment advice. All investment decisions are your sole responsibility. Consult a licensed financial advisor before investing.

---

**Version**: 1.0.0
**Generated**: Competitive-Agents Fusion (Alpha + Beta)
**Last Updated**: 2026-02-12
