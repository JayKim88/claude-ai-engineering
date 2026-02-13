# portfolio-review

Comprehensive portfolio overview with scores and interactive dashboard

## Trigger

When the user says:
- "review my portfolio"
- "portfolio review"
- "/portfolio-review"
- "show portfolio with scores"
- "portfolio dashboard"
- "analyze my portfolio"
- "포트폴리오 리뷰"
- "포트폴리오 분석"
- "내 포트폴리오 확인"

## Description

Performs comprehensive portfolio review including:
- Scoring all portfolio holdings (Financial + Valuation + Momentum)
- Calculating portfolio-level metrics (Total value, P&L, weighted score)
- Generating interactive HTML dashboard with Chart.js visualizations
- Providing insights on diversification and weak holdings
- Auto-opening dashboard in browser

## Instructions

When triggered:

1. **Score all portfolio holdings**:
   ```bash
   cd plugins/investment-analyzer/scripts
   python3 portfolio_manager.py score
   ```
   - This updates scores for all holdings in the database
   - Shows scoring progress and success rate

2. **Generate HTML dashboard**:
   ```bash
   python3 dashboard_generator.py
   ```
   - Generates portfolio-dashboard-YYYY-MM-DD.html in data/ directory
   - Creates 3 interactive Chart.js visualizations:
     - Sector Allocation pie chart
     - Score Distribution bar chart
     - P&L by Holding bar chart
   - Auto-opens dashboard in browser

3. **Display terminal summary**:
   ```bash
   python3 portfolio_manager.py show --with-scores
   ```
   - Shows portfolio holdings table with scores
   - Displays ticker, shares, price, P&L%, score, and grade

4. **Provide insights and recommendations**:
   - Analyze the output and provide:
     - Portfolio health assessment based on weighted average score
     - Sector concentration warnings (if any sector > 50%)
     - Identification of weak holdings (score < 5)
     - Underperforming stocks (negative P&L AND low score)
     - Rebalancing suggestions if applicable

## Example Output

### Terminal Summary
```
🔄 Scoring 3 holdings...
  Scoring AAPL... ✅ 7.3/10 (B+ Good)
  Scoring MSFT... ✅ 3.9/10 (D  Poor)
  Scoring NVDA... ✅ 6.6/10 (B  Fair)

✅ Scored 3/3 holdings

📊 Portfolio Summary
─────────────────────────────────────
Total Value:    $29,707.10
Total Cost:     $37,625.00
Total P&L:      -21.04% (-$7,917.90)
Weighted Score: 6.1/10 (Fair)

Holdings (with scores):
┌────────┬─────────┬───────────┬──────────┬─────────┬────────┐
│ Ticker │  Shares │ Curr Price│   P&L %  │  Score  │ Grade  │
├────────┼─────────┼───────────┼──────────┼─────────┼────────┤
│ AAPL   │  50.00  │  $275.50  │  +52.63% │  7.3/10 │ B+ Good│
│ MSFT   │  30.00  │  $404.37  │   -3.72% │  3.9/10 │ D  Poor│
│ NVDA   │  20.00  │  $190.05  │  -76.24% │  6.6/10 │ B  Fair│
└────────┴─────────┴───────────┴──────────┴─────────┴────────┘

✅ Dashboard generated: data/portfolio-dashboard-2026-02-12.html
🌐 Opening dashboard in browser...
```

### AI Analysis
```
💡 Portfolio Analysis

**Overall Health**: Fair (6.1/10 weighted score)

**Sector Allocation**:
• Technology: 100% ⚠️ CRITICAL - Highly concentrated in single sector
• Recommendation: Consider diversifying into other sectors (Healthcare, Finance, Consumer)

**Performance Highlights**:
• Best Performer: AAPL (+52.63%, Score: 7.3/10) - Strong valuation, maintain position
• Worst Performer: NVDA (-76.24%, Score: 6.6/10) - Consider averaging down if fundamentals remain strong

**Weak Holdings Alert**:
• MSFT (Score: 3.9/10, P&L: -3.72%)
  - Issue: Poor score indicates weak fundamentals
  - Recommendation: Monitor closely, consider exiting if score doesn't improve

**Action Items**:
1. Diversify out of Technology sector (reduce from 100% to ~60%)
2. Monitor MSFT closely - potential exit candidate
3. Consider adding positions in:
   - Healthcare sector (Johnson & Johnson, UnitedHealth)
   - Financial sector (JPMorgan, Visa)
   - Consumer sector (Procter & Gamble, Coca-Cola)

**Dashboard**: View detailed charts and visualizations in the browser dashboard
```

## Dashboard Features

The HTML dashboard includes:

1. **Portfolio Summary Card**
   - Total Value, Cost, P&L, Average Score, Number of Holdings
   - Color-coded P&L (green for positive, red for negative)

2. **Holdings Table**
   - Complete list of holdings with live data
   - Ticker, Shares, Avg Cost, Current Price, Market Value, P&L%, Score, Grade
   - Color-coded scores (Excellent, Good, Fair, Weak)

3. **Interactive Charts**
   - **Sector Allocation Pie Chart**: Visual breakdown of sector diversification
   - **Score Distribution Bar Chart**: Number of holdings in each score category
   - **P&L by Holding Bar Chart**: Performance comparison across holdings

4. **Responsive Design**
   - Clean, professional Financial Times-inspired styling
   - Mobile-friendly layout
   - Easy to read and navigate

## Notes

- Portfolio ID defaults to 1 (primary portfolio)
- Scores are cached in database - use `score` command to refresh
- Dashboard is saved as static HTML file in `data/` directory
- Dashboard uses CDN for Chart.js (requires internet connection)
- All monetary values displayed in portfolio's base currency

## Error Handling

- If no portfolio exists: Prompts user to create one first
- If holdings have no scores: Runs scoring automatically
- If data fetch fails: Displays "N/A" and shows error message
- If browser doesn't auto-open: Provides file path to open manually

## Related Skills

- **analyze-stock**: Deep-dive analysis of individual stocks
- **find-opportunities**: Discover undervalued stocks (Phase 2)
- **portfolio-chat**: AI conversational portfolio advisor (Phase 3)

## CLI Commands Reference

### Score Portfolio
```bash
cd plugins/investment-analyzer/scripts
python3 portfolio_manager.py score
```

### Show Portfolio with Scores
```bash
python3 portfolio_manager.py show --with-scores
```

### Generate Dashboard
```bash
python3 dashboard_generator.py [PORTFOLIO_ID]
```

### All-in-One Portfolio Review
```bash
python3 portfolio_manager.py score && \
python3 portfolio_manager.py show --with-scores && \
python3 dashboard_generator.py
```
