# Market Pulse

Financial market analysis dashboard plugin for Claude Code. Fetches real-time data from free sources and generates comprehensive market analysis using a multi-agent pipeline.

## Features

- **US Market**: S&P 500, NASDAQ, DOW, 11 SPDR Sector ETFs, VIX
- **Korean Market**: KOSPI/KOSDAQ, foreign/institutional flows (외국인/기관 매매동향), top stocks with PER/PBR
- **Global Macro**: Treasury yields, gold, oil, dollar index, USD/KRW
- **Crypto**: BTC, ETH, SOL and more
- **Watchlist**: Personal stock tracking with price alerts
- **News**: Financial news from RSS feeds (CNBC, MarketWatch, 한국경제, 매일경제)

## Quick Start

### Trigger

Say any of these in Claude Code:
- "시장 분석해줘" / "시장 현황" / "증시 분석"
- "market overview" / "market pulse" / "check the markets"

### Dependencies

```bash
pip3 install yfinance pykrx pyyaml feedparser
```

Dependencies are auto-installed on first run if missing.

## Configuration

### Watchlist (`config/watchlist.yaml`)

Edit to track your own stocks:

```yaml
us_stocks:
  - symbol: "AAPL"
    name: "Apple"
    alert_above: 250
    alert_below: 180
kr_stocks:
  - ticker: "005930"
    name: "삼성전자"
crypto:
  - symbol: "BTC-USD"
    name: "Bitcoin"
```

### Data Sources (`config/sources.yaml`)

Customize tracked symbols, sector ETFs, news RSS feeds, and scoring keywords.

## Architecture

```
Phase 1: Python Data Fetch (yfinance + pykrx + feedparser)
                    ↓
Phase 2: Parallel Analysis (3 agents)
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ US Market    │  │ KR Market    │  │ Crypto + Macro    │
│ Analyzer     │  │ Analyzer     │  │ Analyzer          │
└──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
       └─────────────────┼──────────────────┘
                         ↓
Phase 3: Synthesis (market-synthesizer)
                         ↓
              Dashboard Output
```

## Data Sources (All Free)

| Library | Purpose |
|---------|---------|
| `yfinance` | US stocks, ETFs, commodities, crypto, treasury yields |
| `pykrx` | Korean KOSPI/KOSDAQ, foreign/institutional trading, fundamentals |
| `feedparser` | Financial news RSS feeds |

## Disclaimer

This plugin provides market data and analysis for **informational purposes only**. It does not constitute financial advice. Investment decisions should be made based on your own judgment and responsibility.
