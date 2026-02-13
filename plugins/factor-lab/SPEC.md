# factor-lab Specification

> **Version**: 1.0.0
> **Date**: 2026-02-13
> **Status**: Phase 1 Complete, Phase 2 Planning
> **Based on**: PROGRESS.md retrospective analysis

---

## 1. Overview

factor-lab is a quantitative stock screening and backtesting platform for systematic factor investing based on the Fama-French 5-Factor Model.

### Philosophy: CLI-First Approach
- Reproducible backtesting (same input = same output)
- Academically validated factors
- Fast execution without Agent overhead
- Industry-standard Python CLI tools

---

## 2. Functional Requirements

### Phase 1: Core Engine (CLI Tools)

#### FR-1: Data Infrastructure
**Priority**: High
Complete data management system with multi-market support and caching.

**Components**:
- SQLite database with 3 tables (stock_info, historical_prices, universe_members)
- Multi-universe support (SP500, NASDAQ100, KOSPI200, KOSDAQ150)
- yfinance integration for US stocks
- pykrx integration for Korean stocks
- 30-day cache validity with automatic refresh

#### FR-2: Factor Calculator
**Priority**: High
Calculate 5 quantitative factors with sector-relative scoring.

**Factors**:
- Value Factor (P/E, P/B vs sector benchmarks)
- Quality Factor (ROE, Debt/Equity, Margins)
- Momentum Factor (12-month returns, skip recent 1-month)
- Low Volatility Factor (Beta, 60-day volatility)
- Size Factor (Market Cap tiers)

**Output**: Composite score (0-100), Grade (A+/A/B+/B/C/D)

#### FR-3: Factor Screener CLI
**Priority**: High
Command-line tool for multi-factor stock screening.

**Features**:
- CLI argument parser (universe, factors, min-score, top-n, output)
- Factor weight parsing (e.g., "value:0.3,quality:0.4,momentum:0.3")
- Multi-factor screening engine with progress indicators
- Error handling (continue on failures)
- CSV/JSON export with terminal display
- Sector breakdown summary

#### FR-4: Backtest Engine
**Priority**: High
Historical simulation with realistic transaction costs.

**Features**:
- Historical simulation with monthly/quarterly rebalancing
- Transaction cost modeling (commission 0.1%, slippage 0.05%)
- Performance metrics (Total return, CAGR, Sharpe Ratio, Max Drawdown, Win rate)
- Equity curve generation (CSV + PNG visualization)
- CLI interface with 12+ parameters

#### FR-5: Strategy Library
**Priority**: High
Pluggable strategy system with 4 built-in strategies.

**Strategies**:
- Buy-and-Hold (baseline benchmark)
- Momentum Strategy (12M lookback, skip 1M)
- Value Factor Strategy (low P/E, P/B)
- Quality Strategy (ROE > 15%, Debt/Equity < 0.5)

#### FR-6: Cache Pre-population Script
**Priority**: Medium
Bulk data download to avoid API rate limiting.

**Features**:
- Bulk historical data download (10 years default)
- Rate limiting (1.5s delay between stocks)
- Progress tracking
- CLI interface (--universe, --years, --delay, --limit)
- Error handling and retry logic

#### FR-7: Documentation
**Priority**: Medium
Comprehensive user and developer documentation.

**Components**:
- README.md with Quick Start, Features, Architecture
- Workflow Process Mermaid diagram
- 5 Factors explanation (Fama-French Model)
- Usage examples (3 scenarios)
- Data sources and key metrics explanation

#### FR-8: Integration Testing
**Priority**: Low
Cross-plugin integration with market-pulse and investment-analyzer.

**Tests**:
- JSON schema validation
- End-to-end workflow (screening → validation → execution)
- Performance benchmarking (< 2 min screening, < 5 min backtesting)

#### FR-9: Unit Tests
**Priority**: Low
Comprehensive unit test suite.

**Coverage**:
- test_factor_calculator.py
- test_data_manager.py
- test_backtest_engine.py
- test_screener_workflow.py
- test_backtest_workflow.py

---

## 3. Non-Functional Requirements

### NFR-1: Performance
**Screening**: Complete 500-stock screening in under 2 minutes
**Backtesting**: 10-year backtest execution in under 5 minutes
**Cache**: 95%+ cache hit rate after initial population

### NFR-2: Accuracy
**Factor Scores**: Sector-relative scoring with normalization
**Backtesting**: Realistic transaction costs (0.1% commission, 0.05% slippage)
**Results**: Reproducible (same parameters = identical results)

### NFR-3: Reliability
**Data Fetching**: 98%+ success rate for S&P 500 universe
**Error Handling**: Graceful degradation (continue on individual stock failures)
**Cache Validity**: 30-day expiration with automatic refresh

### NFR-4: Usability
**CLI Interface**: Standard argparse with --help documentation
**Output Formats**: CSV, JSON, PNG (equity curves)
**Progress Indicators**: Real-time feedback for long operations

---

## 4. Technical Design

### 4.1 Data Models

#### Stock Info Table
- ticker: TEXT (primary key)
- name: TEXT
- sector: TEXT
- market_cap: REAL
- last_updated: TIMESTAMP

#### Historical Prices Table
- ticker: TEXT (foreign key)
- date: DATE
- open: REAL
- high: REAL
- low: REAL
- close: REAL
- volume: INTEGER
- adj_close: REAL

#### Universe Members Table
- universe_name: TEXT
- ticker: TEXT
- added_date: DATE

---

## 5. CLI Commands

### CLI-1: Factor Screener
```bash
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors value:0.3,quality:0.4,momentum:0.3 \
  --top-n 50 \
  --output results.csv
```

### CLI-2: Backtest Engine
```bash
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 50
```

### CLI-3: Cache Population
```bash
python3 scripts/populate_cache.py \
  --universe SP500 \
  --years 10 \
  --delay 1.5
```

### CLI-4: Debug Scoring
```bash
python3 quant/debug_scoring.py AAPL GOOGL MSFT
```

---

## 6. Edge Cases

### EC-1: API Rate Limiting
**Scenario**: yfinance free tier limits (2000 requests/hour)
**Handling**: Pre-population script with 1.5s delays, local cache

### EC-2: Missing Stock Data
**Scenario**: Stock delisted or data unavailable
**Handling**: Continue with remaining stocks, log errors, 98%+ success rate

### EC-3: Timezone-Aware Datetimes
**Scenario**: yfinance returns timezone-aware indexes (America/New_York)
**Handling**: Use pd.Timestamp with tz_localize() for comparisons

### EC-4: Insufficient Historical Data
**Scenario**: New IPOs with < 252 trading days
**Handling**: Skip momentum calculation, use neutral score (50.0)

### EC-5: Extreme Valuation Metrics
**Scenario**: Negative P/E, P/B > 50
**Handling**: Proper normalization with distance_ratio for outliers

### EC-6: S&P 500 Fetching Failure
**Scenario**: SSL certificate error or HTTP 403
**Handling**: ssl._create_unverified_context() + User-Agent header

---

## 7. Testing Requirements

### Validation Results (Week 1)
- ✅ 10 stocks sample: 35s execution, 100% success
- ✅ Full S&P 500: 503 stocks, 98% success, ~5 min (cached)
- ✅ AAPL scoring: 55.9/100 (realistic, not inflated)

### Backtest Results (Week 2)
- ✅ Buy-and-Hold (2023-2024): +20.23% return, Sharpe 10.98
- ✅ Momentum (2020-2024): +86.81% return, Sharpe 3.54
- ✅ Value (2020-2024): +51.47% return, Sharpe 2.56
- ✅ Quality (2020-2024): +52.15% return, Sharpe 2.53

---

## 8. Configuration

### factor_definitions.yaml
**Size**: 190 lines
**Sections**:
- Factor definitions (5 factors with metrics and weights)
- Default composite weights (conservative, balanced, aggressive)
- Sector benchmarks (11 sectors with P/E, P/B)
- Universe definitions
- Scoring parameters (grading thresholds)

---

## 9. Dependencies

### Core (Installed)
- numpy>=1.24
- pandas>=2.0
- scipy>=1.10
- yfinance>=0.2.28
- pykrx>=1.0.45
- PyYAML>=6.0
- matplotlib>=3.7 (for equity curve visualization)

---

## 10. Performance Metrics

### Achieved Benchmarks (Week 2)
- Cache population: 503/503 stocks, 100% success, ~12 minutes
- Backtest execution: < 1 minute (with cache)
- Momentum strategy: +16.91% CAGR (vs academic 8-10%)
- Quality strategy: +11.06% CAGR (vs academic 3-4%)

---

## 11. Bug Fixes History

### BUG-1: Value Score Normalization
**Fixed**: 2026-02-13
**Issue**: Overvalued stocks showing 100.0 score
**Solution**: Rewrote _normalize() with proper distance_ratio

### BUG-2: Momentum Score Calculation
**Fixed**: 2026-02-13
**Issue**: All stocks showing neutral 50.0
**Solution**: Extended fetch period to 450 calendar days

### BUG-3: Column Name Mismatch
**Fixed**: 2026-02-13
**Issue**: KeyError 'Close' with cached data
**Solution**: Added column capitalization in _get_cached_historical()

### BUG-4: S&P 500 Fetching
**Fixed**: 2026-02-13
**Issue**: SSL certificate error + HTTP 403
**Solution**: ssl._create_unverified_context() + User-Agent header

### BUG-5: Timezone Comparison
**Fixed**: 2026-02-13
**Issue**: TypeError with timezone-aware datetime
**Solution**: Use pd.Timestamp with tz_localize()

### BUG-6: API Rate Limiting
**Fixed**: 2026-02-13
**Issue**: "Too Many Requests" errors during backtesting
**Solution**: Cache pre-population script with rate limiting
