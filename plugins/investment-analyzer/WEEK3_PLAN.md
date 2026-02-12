# Week 3 Plan: Portfolio Integration & Dashboard

**Timeline**: Days 15-21
**Status**: 🔄 In Progress
**Goal**: Integrate scorecard into portfolio management and create HTML dashboard

---

## 🎯 Week 3 Objectives

### Primary Goals
1. **Portfolio Scorecard Integration** - Score all portfolio holdings automatically
2. **HTML Dashboard** - Visual portfolio overview with scores and charts
3. **Portfolio-Level Insights** - Diversification, sector allocation, risk metrics
4. **portfolio-review Skill** - User-facing interface for portfolio analysis

### Success Criteria
- [ ] All portfolio holdings automatically scored on demand
- [ ] HTML dashboard generated with portfolio visualization
- [ ] Sector allocation pie chart
- [ ] Score distribution chart
- [ ] portfolio-review skill functional
- [ ] Dashboard auto-opens in browser

---

## 📋 Task Breakdown

### Task 1: Portfolio Scorecard Integration (Days 15-16)
**Priority**: HIGH
**Estimated Time**: 2 days
**Files to Modify**: `scripts/portfolio_manager.py`

#### Implementation

**A. Add `score` Command**
```python
# New command: python3 portfolio_manager.py score
def score_portfolio(portfolio_id: int):
    """Score all holdings in portfolio"""
    holdings = get_all_holdings(portfolio_id)

    for holding in holdings:
        ticker = holding.ticker
        scorecard = generator.calculate_scorecard(ticker)

        # Save to score_history table
        save_score(
            ticker=ticker,
            total_score=scorecard['total_score'],
            financial_score=scorecard['financial_score'],
            valuation_score=scorecard['valuation_score'],
            momentum_score=scorecard['momentum_score'],
            price_at_scoring=scorecard['price']
        )

    print(f"✅ Scored {len(holdings)} holdings")
```

**B. Enhance `show` Command**
```python
# Modified: python3 portfolio_manager.py show --with-scores
def show_portfolio_with_scores(portfolio_id: int):
    holdings = get_all_holdings(portfolio_id)

    # Display table with scores
    print("\n📊 Portfolio Holdings with Scores\n")
    print(f"{'Ticker':<8} {'Shares':>8} {'Price':>10} {'P&L %':>8} {'Score':>8} {'Grade':>8}")
    print("─" * 70)

    for holding in holdings:
        score = get_latest_score(holding.ticker)  # From score_history
        grade = get_grade(score.total_score)

        print(f"{holding.ticker:<8} {holding.quantity:>8} "
              f"${holding.current_price:>9.2f} {holding.pnl_pct:>7.1f}% "
              f"{score.total_score:>7.1f} {grade:>8}")
```

**C. Portfolio-Level Metrics**
```python
def calculate_portfolio_metrics(portfolio_id: int):
    """Calculate aggregate portfolio metrics"""
    holdings = get_all_holdings_with_scores(portfolio_id)

    metrics = {
        'total_value': sum(h.market_value for h in holdings),
        'total_cost': sum(h.cost_basis for h in holdings),
        'total_pnl_pct': (total_value - total_cost) / total_cost * 100,
        'weighted_avg_score': sum(h.score * h.weight for h in holdings),
        'sector_allocation': calculate_sector_weights(holdings),
        'score_distribution': {
            'excellent': count(score >= 9),
            'good': count(8 <= score < 9),
            'fair': count(7 <= score < 8),
            'weak': count(score < 7)
        }
    }

    return metrics
```

---

### Task 2: HTML Dashboard Generator (Days 17-18)
**Priority**: HIGH
**Estimated Time**: 2 days
**File to Create**: `scripts/dashboard_generator.py`

#### Implementation

**A. Dashboard Structure**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Investment Analyzer - Portfolio Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* Financial Times inspired styling */
        body { font-family: 'Segoe UI', sans-serif; background: #fff1e5; }
        .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; }
        .score-excellent { color: #16a34a; }
        .score-good { color: #84cc16; }
        .score-fair { color: #eab308; }
        .score-weak { color: #ef4444; }
    </style>
</head>
<body>
    <h1>📊 Portfolio Dashboard</h1>

    <!-- Portfolio Summary Card -->
    <div class="card">
        <h2>Portfolio Summary</h2>
        <div class="summary-grid">
            <div>Total Value: $XX,XXX</div>
            <div>Total P&L: +XX.X%</div>
            <div>Avg Score: X.X/10</div>
            <div>Holdings: X stocks</div>
        </div>
    </div>

    <!-- Holdings Table with Scores -->
    <div class="card">
        <h2>Holdings</h2>
        <table id="holdings-table">
            <!-- Generated dynamically -->
        </table>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
        <div class="card">
            <h3>Sector Allocation</h3>
            <canvas id="sector-chart"></canvas>
        </div>

        <div class="card">
            <h3>Score Distribution</h3>
            <canvas id="score-chart"></canvas>
        </div>

        <div class="card">
            <h3>P&L Distribution</h3>
            <canvas id="pnl-chart"></canvas>
        </div>
    </div>

    <script>
        // Chart.js visualizations
        // Sector pie chart
        // Score bar chart
        // P&L scatter plot
    </script>
</body>
</html>
```

**B. Dashboard Generator Class**
```python
class PortfolioDashboardGenerator:
    """Generate HTML dashboard for portfolio"""

    def __init__(self):
        self.template_path = 'templates/portfolio_dashboard.html'

    def generate_dashboard(self, portfolio_id: int, output_path: str):
        """Generate HTML dashboard"""
        # 1. Fetch portfolio data with scores
        data = self._fetch_portfolio_data(portfolio_id)

        # 2. Calculate metrics
        metrics = self._calculate_metrics(data)

        # 3. Render HTML
        html = self._render_html(data, metrics)

        # 4. Write to file
        with open(output_path, 'w') as f:
            f.write(html)

        # 5. Open in browser
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(output_path)}')

        return output_path

    def _render_html(self, data, metrics):
        """Render HTML with data"""
        # Use Jinja2 or simple string formatting
        html = self.template.format(
            total_value=metrics['total_value'],
            total_pnl=metrics['total_pnl_pct'],
            avg_score=metrics['weighted_avg_score'],
            holdings_table=self._generate_holdings_table(data),
            sector_chart_data=json.dumps(metrics['sector_allocation']),
            score_chart_data=json.dumps(metrics['score_distribution'])
        )
        return html
```

**C. Chart.js Integration**
```javascript
// Sector Allocation Pie Chart
const sectorChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Technology', 'Healthcare', 'Finance', ...],
        datasets: [{
            data: [45, 25, 15, 10, 5],
            backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', ...]
        }]
    },
    options: {
        plugins: {
            legend: { position: 'right' },
            title: { display: true, text: 'Sector Allocation (%)' }
        }
    }
});

// Score Distribution Bar Chart
const scoreChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Excellent', 'Good', 'Fair', 'Weak'],
        datasets: [{
            label: 'Number of Stocks',
            data: [2, 3, 2, 1],
            backgroundColor: ['#16a34a', '#84cc16', '#eab308', '#ef4444']
        }]
    }
});
```

---

### Task 3: portfolio-review Skill (Day 19)
**Priority**: HIGH
**Estimated Time**: 1 day
**File to Create**: `skills/portfolio-review/SKILL.md`

#### Skill Definition

**Trigger**:
- "review my portfolio"
- "portfolio review"
- "/portfolio-review"
- "show portfolio with scores"
- "portfolio dashboard"

**Execution Flow**:
```
1. Score all portfolio holdings (if not recently scored)
2. Calculate portfolio-level metrics
3. Generate HTML dashboard
4. Display terminal summary
5. Open dashboard in browser
6. Provide insights and recommendations
```

**Terminal Output**:
```
📊 Portfolio Review

Scoring 8 holdings... ✅ Done

Portfolio Summary:
─────────────────────────────────────
Total Value:    $125,432.15
Total Cost:     $110,000.00
Total P&L:      +14.0% ($15,432.15)
Avg Score:      6.8/10 (Fair)

Holdings (sorted by score):
┌────────┬───────┬──────┬────────┬────────┐
│ Ticker │ Score │ P&L% │ Weight │ Grade  │
├────────┼───────┼──────┼────────┼────────┤
│ AAPL   │  8.5  │ +52% │  30%   │ A      │
│ MSFT   │  7.2  │  -2% │  25%   │ B+     │
│ NVDA   │  6.8  │ -76% │  20%   │ B      │
│ GOOG   │  6.5  │ +15% │  15%   │ B      │
│ TSLA   │  4.2  │ +30% │  10%   │ D      │
└────────┴───────┴──────┴────────┴────────┘

Sector Allocation:
Technology:        80% ⚠️ Over-concentrated
Consumer Cyclical: 10%
Cash:             10%

💡 Insights:
• High tech concentration (80%) - consider diversification
• 3 stocks underperforming (negative P&L)
• 2 stocks with weak scores (<5) - review for potential exit

🌐 Dashboard opened in browser at:
file:///tmp/portfolio-dashboard-2026-02-12.html
```

---

### Task 4: Portfolio Insights & Recommendations (Day 20)
**Priority**: MEDIUM
**Estimated Time**: 1 day

#### A. Diversification Analysis
```python
def analyze_diversification(holdings):
    """Analyze portfolio diversification"""
    insights = []

    # Sector concentration
    sector_weights = calculate_sector_weights(holdings)
    max_sector = max(sector_weights, key=sector_weights.get)

    if sector_weights[max_sector] > 0.50:
        insights.append({
            'type': 'warning',
            'category': 'diversification',
            'message': f'{max_sector} is {sector_weights[max_sector]:.0%} of portfolio - over-concentrated'
        })

    # Single stock concentration
    for holding in holdings:
        if holding.weight > 0.25:
            insights.append({
                'type': 'warning',
                'category': 'diversification',
                'message': f'{holding.ticker} is {holding.weight:.0%} - consider reducing position'
            })

    # Number of holdings
    if len(holdings) < 5:
        insights.append({
            'type': 'info',
            'message': 'Consider adding more stocks for better diversification (target: 10-20)'
        })

    return insights
```

#### B. Weak Holdings Alert
```python
def identify_weak_holdings(holdings):
    """Identify holdings with poor scores or performance"""
    weak = []

    for holding in holdings:
        score = holding.latest_score

        # Low score AND negative P&L
        if score.total_score < 5 and holding.pnl_pct < -10:
            weak.append({
                'ticker': holding.ticker,
                'issue': 'Low score + Underperforming',
                'score': score.total_score,
                'pnl_pct': holding.pnl_pct,
                'recommendation': 'Consider exiting'
            })

        # Extremely low score
        elif score.total_score < 4:
            weak.append({
                'ticker': holding.ticker,
                'issue': 'Very weak fundamentals',
                'score': score.total_score,
                'recommendation': 'Review immediately'
            })

    return weak
```

#### C. Rebalancing Suggestions
```python
def suggest_rebalancing(holdings, target_allocation):
    """Suggest rebalancing actions"""
    suggestions = []

    current = calculate_sector_weights(holdings)

    for sector, target_weight in target_allocation.items():
        current_weight = current.get(sector, 0)
        diff = current_weight - target_weight

        if abs(diff) > 0.10:  # 10% threshold
            action = 'Reduce' if diff > 0 else 'Increase'
            suggestions.append({
                'sector': sector,
                'action': action,
                'amount': abs(diff),
                'current': current_weight,
                'target': target_weight
            })

    return suggestions
```

---

### Task 5: End-to-End Testing (Day 21)
**Priority**: HIGH
**Estimated Time**: 1 day

#### Test Cases

**A. Score Portfolio Command**
```bash
python3 portfolio_manager.py score
# Expected: All holdings scored, score_history updated
```

**B. Show Portfolio with Scores**
```bash
python3 portfolio_manager.py show --with-scores
# Expected: Table with ticker, price, P&L, score, grade
```

**C. Generate Dashboard**
```bash
python3 dashboard_generator.py
# Expected: HTML file created, browser opened
```

**D. portfolio-review Skill**
```bash
# User: "review my portfolio"
# Expected:
# - Holdings scored
# - Dashboard generated
# - Terminal summary displayed
# - Browser opened with dashboard
```

**E. Validation**
- [ ] All 3 holdings in test portfolio scored correctly
- [ ] Dashboard renders without errors
- [ ] Charts display correctly (sector, score, P&L)
- [ ] Insights are relevant and accurate
- [ ] Browser auto-opens dashboard

---

## 📦 New Dependencies

```bash
# None required! Using built-in libraries:
# - json (for data serialization)
# - webbrowser (for opening dashboard)
# - datetime (for timestamps)

# Chart.js loaded via CDN in HTML template
```

---

## 🎯 Week 3 Success Criteria

- [ ] Portfolio holdings can be scored on demand
- [ ] `show --with-scores` displays comprehensive table
- [ ] HTML dashboard generated successfully
- [ ] Dashboard includes 3 charts (sector, score, P&L)
- [ ] portfolio-review skill functional end-to-end
- [ ] Insights and recommendations provided
- [ ] Dashboard auto-opens in browser
- [ ] All test cases pass

---

## 📊 Estimated Time Distribution

| Task | Days | Priority |
|------|------|----------|
| Portfolio Scorecard Integration | 2 | HIGH |
| HTML Dashboard Generator | 2 | HIGH |
| portfolio-review Skill | 1 | HIGH |
| Portfolio Insights | 1 | MEDIUM |
| End-to-End Testing | 1 | HIGH |

**Total**: 7 days (Week 3)

---

## 🚀 Week 3 Deliverables

1. **Enhanced portfolio_manager.py**
   - `score` command
   - `show --with-scores` command
   - Portfolio-level metrics calculation

2. **dashboard_generator.py** (new)
   - HTML generation
   - Chart.js integration
   - Browser auto-open

3. **portfolio-review skill** (new)
   - SKILL.md definition
   - End-to-end integration

4. **HTML Dashboard Template**
   - Responsive design
   - 3 interactive charts
   - Holdings table

5. **Portfolio Insights Module**
   - Diversification analysis
   - Weak holdings identification
   - Rebalancing suggestions

---

## 🔗 Integration Points

- `scorecard.py` (Week 2) → Used for scoring holdings
- `portfolio_manager.py` (Week 1) → Enhanced with scoring
- `database.py` (Week 1) → `score_history` table used
- `data_fetcher.py` (Week 1) → Data source for scoring

---

**Ready to start Week 3?** Begin with Task 1: Portfolio Scorecard Integration
