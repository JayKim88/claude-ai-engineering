# Changelog

All notable changes to Market-Pulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-12

### Added - Phase 2.5: Value Investing Analysis Tools

#### AI Insights Dashboard Enhancement (2026-02-12 Evening Update)
- **Automatic Insights Generation** (`config/generate_insights.py`)
  - Data-driven market analysis without requiring AI agents
  - Heuristic-based interpretation of market data
  - Automatic detection of market trends, sector rotation, foreign flows
  - Generates synthesis with key takeaways and investment strategies
- **Enhanced HTML Dashboard** (`config/generate_html.py`)
  - Now includes full "MARKET ANALYSIS" section if `analysis` field exists
  - Displays: Today's Market Overview, US Market Analysis, Korean Market Analysis, Crypto & Macro Analysis
  - Investment implications, risk warnings, cross-market insights
- **Improved SKILL.md**
  - Step 4 Phase 3: Clear instructions for saving AI analysis to JSON
  - Step 6-2: Automatic verification of `analysis` field before HTML generation
  - Support for `--with-analysis` flag for one-command execution
- **Helper Scripts**
  - `save_analysis_to_json.py`: Save agent outputs to JSON
  - Auto-insights integration with `fetch_market.py --with-analysis`

### Added - Phase 2.5: Value Investing Analysis Tools (Original Release)

#### MCP Layer
- **Stock MCP Server** (`mcp/stock_mcp_server.py`)
  - 9 tools for fundamental data via yfinance
  - JSON-RPC 2.0 protocol implementation
  - Tools: fundamentals, financials, info, price history, options, dividends, recommendations, earnings, news
- **Stock MCP Client** (`mcp/stock_client.py`)
  - Python wrapper for MCP server communication
  - Subprocess-based JSON-RPC client

#### Analysis Engines
- **Safety Margin Calculator** (`analysis/intrinsic_value.py`)
  - Graham intrinsic value formula: IV = EPS × (8.5 + 2g)
  - Safety margin calculation and interpretation
  - Undervalued stock screening (min 20% margin)
  - Recommendation system: 강력 매수/매수/보유/매도

- **GARP Screener** (`analysis/lynch_screener.py`)
  - PEG ratio calculation (PER / growth rate)
  - Lynch's 6 stock categories:
    1. Slow Growers (저성장주)
    2. Stalwarts (우량주)
    3. Fast Growers (고성장주)
    4. Cyclicals (경기순환주)
    5. Turnarounds (회생주)
    6. Asset Plays (자산주)
  - GARP screening (PEG < 1.0, growth >= 10%)
  - Green/red flags identification

- **Company Deep Dive Analyzer** (`analysis/company_deep_dive.py`)
  - 8-perspective integrated analysis:
    1. **Graham**: Safety margin & intrinsic value
    2. **Buffett**: Economic moat strength (6 competitive advantages)
    3. **Lynch**: GARP category & PEG rating
    4. **Munger**: Risk analysis & failure scenarios (inversion thinking)
    5. **Asness**: Multi-factor scores (Value, Quality, Momentum, Low Volatility)
    6. **Dalio**: Economic cycle positioning (4 cycles)
    7. **Fisher**: Qualitative analysis (Scuttlebutt - innovation, management, employees, customers)
    8. **Synthesis**: Overall score, risk-reward ratio, final recommendation
  - Overall scoring algorithm with weighted perspectives
  - Investment horizon determination (단기/중기/장기)
  - Confidence level (0-100%)

- **Value Investing Analyzer** (`analysis/value_investing_analyzer.py`)
  - All-in-one CLI tool
  - 4 analysis types:
    - `safety_margin`: Undervalued stock screening
    - `garp`: GARP screening
    - `deep`: Deep dive analysis
    - `all`: All analyses
  - JSON export functionality
  - HTML section generation for dashboard integration

#### Report Generation (Phase 2.6)
- **Equity Report Generator** (`reports/equity_report_generator.py`)
  - Professional investment firm-style reports (키움증권/미래에셋 스타일)
  - 2 output formats:
    - **Markdown**: GitHub/Notion compatible, no PDF needed
    - **Terminal**: Console-friendly brief format
  - Report sections:
    1. Investment Opinion (투자 의견)
    2. Investment Thesis (핵심 요약)
    3. Financial Highlights (재무 하이라이트)
    4. Valuation Analysis (밸류에이션 분석)
    5. Economic Moat (경쟁 우위)
    6. Investment Points (투자 포인트)
    7. Risk Factors (리스크 요인)
    8. Factor Analysis (팩터 분석)
    9. Economic Cycle (경제 사이클)
    10. Qualitative Evaluation (정성적 평가)
    11. Overall Assessment (종합 평가)
  - Automatic investment thesis generation
  - Green flags extraction (top 5 investment points)
  - Rating emojis (🟢🔵🟡⚪🔴)

#### Documentation
- **Phase 2.5 README** (`analysis/README.md`)
  - Comprehensive usage guide
  - 4 main features documentation
  - Examples for all analysis types
  - Investment master strategy summary table
  - Installation and dependencies
  - Limitations and disclaimers

- **Architecture Documentation** (`docs/ARCHITECTURE.md`)
  - 10 Mermaid diagrams:
    1. Overall Process Flow
    2. System Components
    3. Multi-Agent Execution Flow
    4. Value Investing Analysis Flow
    5. Deep Dive Analysis Flow
    6. File Structure
    7. Data Flow
    8. Decision Tree
    9. Technology Stack
    10. Performance Metrics

### Changed
- **SKILL.md** updated to v2.0
  - Added Step 5-Value for value investing analysis
  - New trigger phrases: "가치투자 분석", "안전마진 분석", "PEG 스크리닝", "기업 분석"
  - Example 4: Value Investing Analysis scenarios
- **plugin.json** version: 1.0.0 → 2.0.0
  - Updated description to include value investing tools
  - Added keywords: value-investing, graham, buffett, lynch, safety-margin, garp, intrinsic-value
- **Main README.md**
  - Added Phase 2.5 features section
  - New trigger phrases
  - Architecture diagram for Phase 2.5
  - Usage examples (5 scenarios)
  - File structure with Phase 2.5 modules
  - Investment philosophy table
  - Key metrics interpretation (Safety Margin, PEG)
  - Enhanced disclaimer with data limitations

### Technical Details
- **Dependencies**: No new dependencies (uses existing yfinance, pyyaml)
- **Data Source**: yfinance (15-20 minute delayed, free tier)
- **Output Formats**: Terminal tables, Markdown reports, JSON files
- **Compatibility**: Python 3.8+, macOS/Linux/Windows

### Limitations
- PEG ratios calculated from yfinance data (may differ from official sources)
- Economic cycle analysis is simplified (not real-time GDP/interest rate integration)
- Qualitative analysis (Fisher Scuttlebutt) is simplified (no actual interviews)
- DCF model is basic implementation (not advanced WACC/terminal value)

## [1.0.0] - 2026-01-15

### Added - Initial Release
- **Market Analysis Dashboard**
  - US Market: S&P 500, NASDAQ, DOW, 11 SPDR Sector ETFs, VIX
  - Korean Market: KOSPI/KOSDAQ, foreign/institutional flows, top 10 stocks
  - Global Macro: Treasury yields, commodities (gold, oil), USD/KRW
  - Crypto: BTC, ETH, SOL
  - News aggregation from RSS feeds
- **Multi-Agent Pipeline**
  - 3 parallel agents: US Market Analyzer, KR Market Analyzer, Crypto-Macro Analyzer
  - Market Synthesizer for cross-market insights
- **HTML Dashboard**
  - Interactive charts and tables
  - Financial Times-inspired design
  - Auto-open in browser
- **Watchlist Management**
  - Personal stock tracking
  - Price alerts (alert_above, alert_below)
- **Configuration**
  - `sources.yaml`: Data sources customization
  - `watchlist.yaml`: Personal watchlist
- **Free Data Sources**
  - yfinance for US markets
  - pykrx for Korean markets
  - feedparser for news

### Documentation
- Main README.md
- SKILL.md orchestration guide
- Agent definitions (3 agents)
- Configuration guides

---

## Roadmap

### Phase 3: Quant Features (Planned)
- [ ] Historical data storage (SQLite)
- [ ] Technical indicators (RSI, MACD, Bollinger Bands, SMA/EMA)
- [ ] Backtesting engine
- [ ] Signal generation (multi-factor scoring)
- [ ] Alert system (email, notifications)
- [ ] Performance attribution

### Phase 4: Advanced Features (Future)
- [ ] Portfolio management
- [ ] Risk metrics (Sharpe, Sortino, Max Drawdown, VaR)
- [ ] Sector rotation timing
- [ ] Economic calendar integration
- [ ] Sentiment analysis
- [ ] PDF report generation (optional)
- [ ] REST API for external integration
- [ ] Interactive tutorials (educational mode)

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-12 | Phase 2.5: Value Investing Analysis Tools + Equity Report Generator |
| 1.0.0 | 2026-01-15 | Initial Release: Market Analysis Dashboard |

---

**Contributors**: Jay Kim (@JayKim88)

**License**: MIT

**Project**: https://github.com/JayKim88/claude-ai-engineering
