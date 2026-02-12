# Investment Analyzer

AI-powered portfolio management and stock analysis tool for intelligent investment decisions.

## Overview

**Investment Analyzer** is a comprehensive Claude Code plugin that combines:
- **Portfolio Management**: Track holdings, transactions, P&L, and performance
- **Stock Analysis**: AI-powered company scorecards (financial, valuation, momentum)
- **Investment Opportunities**: Discover undervalued stocks and rebalancing suggestions
- **Risk Management**: Correlation analysis, beta, volatility, VaR metrics
- **AI Advisor**: Multi-round conversational portfolio reviews

## Key Features

### Phase 1 (Weeks 1-3): Foundation ✅ COMPLETE
- ✅ **Week 1**: Project structure and data infrastructure (SQLite, yfinance, pykrx)
- ✅ **Week 2**: Company scorecard engine (3-dimensional scoring)
- ✅ **Week 3**: Portfolio integration & HTML dashboard
- ✅ analyze-stock skill for stock analysis
- ✅ portfolio-review skill for comprehensive portfolio review
- ✅ Interactive dashboard with Chart.js visualizations

**현재 상태**: **개인 사용 가능한 완전한 MVP** 🎯

### Phase 2 (Weeks 4-7): Portfolio Intelligence (예정)
- ⏳ Data quality improvements (ROE, margins, technical indicators)
- ⏳ Portfolio insights (diversification warnings, weak holdings)
- ⏳ Correlation analysis and diversification scoring
- ⏳ Investment opportunity finder (undervalued stocks, rebalancing)

### Phase 3 (Weeks 8-10): Advanced Features (예정)
- ⏳ Performance tracking (time-weighted returns, drawdown analysis)
- ⏳ Risk analytics (beta, Sharpe ratio, VaR)
- ⏳ AI conversational advisor (Opus 4.6 multi-round review)

## Data Sources

### Primary: UsStockInfo MCP (US Stocks)
- Financial statements (income, balance sheet, cashflow)
- Institutional holdings and insider transactions
- Analyst recommendations and upgrades/downgrades
- Options chains and implied volatility

### Fallback: yfinance (US & Global)
- Real-time price data (OHLCV)
- Basic financial data
- Global indices and FX rates

### Korean Market: pykrx
- KOSPI/KOSDAQ prices
- Quarterly financials
- Foreign/institutional trading flows

## Skills (Commands)

- `/analyze-stock [TICKER]` - Deep-dive stock analysis with AI insights
- `/portfolio-review` - Comprehensive portfolio overview and dashboard
- `/find-opportunities` - Discover undervalued stocks and rebalancing ideas
- `/portfolio-risk` - Risk metrics and scenario analysis (Phase 3)
- `/portfolio-chat` - AI conversational portfolio advisor (Phase 3)

## Architecture

```
plugins/investment-analyzer/
├── scripts/                           # ✅ Core modules (2,810 lines)
│   ├── database.py                    # SQLite ORM models (6 tables)
│   ├── data_fetcher.py               # Multi-source data (yfinance, pykrx)
│   ├── portfolio_manager.py          # Portfolio CRUD + scoring (600 lines)
│   ├── scorecard.py                  # 3D stock scoring (650 lines)
│   └── dashboard_generator.py        # HTML + Chart.js (650 lines)
├── skills/                            # ✅ Claude AI integration
│   ├── analyze-stock/
│   │   └── SKILL.md                  # Stock analysis skill
│   └── portfolio-review/
│       └── SKILL.md                  # Portfolio review skill (40 lines)
├── data/                              # ✅ Database & output
│   ├── portfolio.db                  # SQLite (44KB, 6 tables)
│   └── portfolio-dashboard-*.html    # Generated dashboards
├── docs/                              # ✅ Documentation (3,600+ lines)
│   ├── README.md                     # This file
│   ├── USER_FLOW.md                  # 🆕 사용자 플로우 & 수익 가이드 (800 lines)
│   ├── ARCHITECTURE.md               # 🆕 시스템 아키텍처 (800 lines)
│   ├── SESSION_SUMMARY.md            # 세션 요약 (420 lines)
│   ├── PROGRESS.md                   # 개발 진행 상황 (700 lines)
│   ├── WEEK3_PLAN.md                 # Week 3 계획 (540 lines)
│   └── NEXT_STEPS.md                 # Week 2 가이드 (550 lines)
└── config/ (예정)                     # ⏳ Phase 2
    ├── portfolio.yaml                # Target allocation
    └── scoring.yaml                  # Scoring rules
```

**코드 통계**:
- Python 코드: 2,810 lines
- 문서: 3,600+ lines
- 총 6,400+ lines

## Legal Disclaimer

⚖️ This tool is provided for INFORMATIONAL PURPOSES ONLY and does not constitute financial, investment, legal, or tax advice. Investment decisions carry risk, including potential loss of principal. You are solely responsible for your investment decisions. Always consult with a licensed financial advisor.

## License

MIT

## Development Status

- **Version**: 0.4.0 (Week 3 - Portfolio Integration Complete) ✅
- **Last Updated**: 2026-02-12 18:30 KST
- **Current Phase**: Week 3 Complete (100% - All features delivered)
- **Next Milestone**: Phase 2 - Portfolio Intelligence & Correlation Analysis

## 🎯 Two Ways to Use This Tool

### Mode 1: Stock Screening (No Portfolio Required) ✅

**Use Case**: Analyze stocks BEFORE buying

```bash
cd plugins/investment-analyzer/scripts

# Analyze any stock instantly
python3 scorecard.py AAPL
python3 scorecard.py TSLA
python3 scorecard.py GOOGL

# Compare multiple candidates
python3 scorecard.py AAPL   # 7.3/10 → Good
python3 scorecard.py GOOGL  # 4.7/10 → Poor
python3 scorecard.py JPM    # 4.3/10 → Poor

# Make investment decision based on scores
```

**Perfect for**: Pre-investment research, stock comparison, candidate screening

---

### Mode 2: Portfolio Management (Portfolio Required) ✅

**Use Case**: Track and manage existing investments

```bash
# 1. Create portfolio (one-time)
python3 portfolio_manager.py create "My Portfolio"

# 2. Add stocks after buying
python3 portfolio_manager.py add AAPL 100 275.50

# 3. Monitor regularly
python3 portfolio_manager.py score
python3 portfolio_manager.py show --with-scores
python3 dashboard_generator.py
```

**Perfect for**: P&L tracking, portfolio monitoring, rebalancing decisions

---

## Quick Start

### View Portfolio
```bash
cd plugins/investment-analyzer/scripts
python3 portfolio_manager.py show
```

### Add Stock to Portfolio
```bash
python3 portfolio_manager.py add AAPL 50 180.5 --notes "Long term hold"
```

### Analyze Stock
```bash
python3 scorecard.py AAPL
# Comprehensive analysis with financial, valuation, and momentum scores
```

### Score Portfolio
```bash
python3 portfolio_manager.py score
# Score all holdings in portfolio
```

### Show Portfolio with Scores
```bash
python3 portfolio_manager.py show --with-scores
# View portfolio with investment scores and grades
```

### Generate Portfolio Dashboard
```bash
python3 dashboard_generator.py
# Generate interactive HTML dashboard with Chart.js visualizations
# Auto-opens in browser with sector allocation, score distribution, and P&L charts
```

### Complete Portfolio Review
```bash
python3 portfolio_manager.py score && \
python3 portfolio_manager.py show --with-scores && \
python3 dashboard_generator.py
# All-in-one: score, display, and visualize portfolio
```

### Test Data Fetcher
```bash
python3 data_fetcher.py
# Tests AAPL (US) and Samsung (KR) data fetching
```

## Documentation

### 📖 필수 문서 (시작하기 전에 읽으세요)
- **[DELIVERABLES.md](DELIVERABLES.md)** - 🆕 **전체 산출물 목록** (코드, 문서, 통계)
- **[USER_FLOW.md](USER_FLOW.md)** - 🆕 **사용자 플로우 & 수익 창출 가이드** (필독!)

### 🏗️ 기술 문서
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - 🆕 시스템 아키텍처, 프로세스, 데이터 흐름 (다이어그램 8개)
- **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)** - Comprehensive session summary and achievements

### 📝 개발 문서
- **[PROGRESS.md](PROGRESS.md)** - Detailed progress tracking (Week 1-3 complete)
- **[WEEK3_PLAN.md](WEEK3_PLAN.md)** - Week 3 implementation plan
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Week 2 implementation guide
- **[DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)** - Chronological development log
- **[Plan](~/.claude/plans/inherited-plotting-stonebraker.md)** - Original 10-week plan

## Recent Achievements

### Week 1 ✅
- ✅ Project structure and database schema (6 tables)
- ✅ Multi-source data fetching (yfinance + pykrx, MCP-ready)
- ✅ Portfolio CRUD operations with CLI
- ✅ Real-time price updates and P&L calculation
- ✅ Transaction history tracking
- ✅ End-to-end testing with 3-stock portfolio

**Test Portfolio Performance**:
- AAPL: +51.62% | MSFT: -1.60% | NVDA: -76.43%
- Total P&L: -20.66%

### Week 2 ✅
- ✅ Company Scorecard Engine (600+ lines)
- ✅ Financial Health scoring (profitability, growth, stability)
- ✅ Valuation scoring (P/E, P/B vs sector benchmarks)
- ✅ Momentum scoring (MA, RSI, MACD)
- ✅ analyze-stock skill with formatted output
- ✅ Multi-stock testing (AAPL, MSFT, NVDA, TSLA)

**Sample Scores**:
- AAPL: 7.3/10 (B+ Good) | MSFT: 3.9/10 (D Poor) | NVDA: 6.6/10 (B Fair)

### Week 3 ✅ (Complete)
- ✅ Portfolio scoring integration (`score` command)
- ✅ Show portfolio with scores (`show --with-scores`)
- ✅ Score database persistence (ScoreHistory table)
- ✅ HTML dashboard generator (`dashboard_generator.py` - 650+ lines)
- ✅ Chart.js visualizations (sector allocation, score distribution, P&L)
- ✅ portfolio-review skill with comprehensive instructions
- ✅ Auto-update existing scores (handles UNIQUE constraint)
- ✅ End-to-end workflow testing

**Portfolio with Scores**:
```
AAPL  50.00  $275.50  +52.63%  7.3/10  B+ (Good)
MSFT  30.00  $404.37   -3.72%  3.9/10  D  (Poor)
NVDA  20.00  $190.05  -76.24%  6.6/10  B  (Fair)
```

**Dashboard Features**:
- Interactive HTML dashboard with Financial Times-inspired styling
- 3 Chart.js visualizations (pie chart, 2 bar charts)
- Portfolio summary card with total value, P&L, weighted score
- Holdings table with color-coded scores
- Auto-opens in browser
