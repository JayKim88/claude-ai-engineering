# Portfolio Copilot - Setup Guide

Quick installation guide to get portfolio-copilot running in under 5 minutes.

## Prerequisites

- **Python 3.8+** - Check with: `python3 --version`
- **pip3** - Package installer for Python
- **Claude Code** - Installed and configured
- **Internet connection** - Required for fetching stock data

## Installation

### Step 1: Install Python Dependencies

Navigate to the plugin directory and install requirements:

```bash
cd /Users/jaykim/Documents/Projects/claude-ai-engineering/plugins/portfolio-copilot
pip3 install -r requirements.txt
```

**Dependencies installed**:
- `yfinance` - US stock data from Yahoo Finance
- `pykrx` - Korean stock market data (optional)
- `pandas` - Data processing
- `numpy` - Numerical operations
- `sqlalchemy` - Database ORM

**Note**: If you only track US stocks, you can skip `pykrx`:
```bash
pip3 install yfinance pandas numpy sqlalchemy
```

### Step 2: Initialize Portfolio Database

Create your first portfolio:

```bash
cd scripts
python3 portfolio_manager.py create "My Portfolio"
```

**Expected output**:
```
✅ Portfolio created successfully!
Portfolio ID: 1
Name: My Portfolio
```

### Step 3: Link Plugin to Claude Code (if in monorepo)

If you're using the monorepo structure:

```bash
cd /Users/jaykim/Documents/Projects/claude-ai-engineering
npm run link
```

**Expected output**:
```
📦 Plugin: portfolio-copilot
  ✓ Linked skill: analyze-stock
  ✓ Linked skill: portfolio-review
```

### Step 4: Verify Installation

Test the Python scripts:

```bash
cd plugins/portfolio-copilot/scripts

# Test data fetching
python3 data_fetcher.py

# Test stock analysis
python3 scorecard.py AAPL

# Test portfolio viewing
python3 portfolio_manager.py show
```

**All commands should run without errors.**

## Quick Start

### In Claude Code Conversation

The plugin is now ready to use conversationally!

#### 1. Analyze a Stock

```
User: "analyze AAPL"
```

Claude Code will:
- Run stock analysis
- Show comprehensive scorecard (Financial, Valuation, Momentum)
- Provide investment grade (A+ to D)

#### 2. Review Your Portfolio

```
User: "review my portfolio"
```

Claude Code will:
- Score all holdings
- Generate interactive HTML dashboard
- Show terminal summary with scores
- Open dashboard in browser automatically

### Command-Line Usage (Optional)

You can also use the scripts directly:

```bash
cd plugins/portfolio-copilot/scripts

# Add stock to portfolio
python3 portfolio_manager.py add AAPL 100 275.50 --notes "Long term hold"

# Score all holdings
python3 portfolio_manager.py score

# View portfolio with scores
python3 portfolio_manager.py show --with-scores

# Generate dashboard
python3 dashboard_generator.py
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'yfinance'`

**Solution**: Install dependencies:
```bash
cd plugins/portfolio-copilot
pip3 install -r requirements.txt
```

### Issue: No portfolio found

**Error**: `Error: No portfolio found`

**Solution**: Create a portfolio first:
```bash
cd plugins/portfolio-copilot/scripts
python3 portfolio_manager.py create "My Portfolio"
```

### Issue: Invalid ticker symbol

**Error**: `Error: Could not fetch data for TICKER`

**Solution**:
- Verify the ticker symbol exists on Yahoo Finance
- Check your internet connection
- Try a known ticker like AAPL or MSFT

### Issue: Database locked

**Error**: `database is locked`

**Solution**: Close other applications accessing the database:
```bash
# Check for processes using the database
lsof | grep portfolio.db

# Force close if needed
pkill python3
```

### Issue: Skills not appearing in Claude Code

**Solution**: Re-link the plugin:
```bash
cd /Users/jaykim/Documents/Projects/claude-ai-engineering
npm run link
```

Then restart Claude Code.

## Configuration

### Data Sources

Portfolio-copilot uses multiple data sources:

- **US Stocks**: Yahoo Finance via `yfinance`
- **Korean Stocks**: KRX via `pykrx` (optional)
- **Historical Data**: Up to 5 years for technical indicators

### Database Location

SQLite database is stored at:
```
plugins/portfolio-copilot/data/portfolio.db
```

**Backup your database**:
```bash
cp data/portfolio.db data/portfolio-backup-$(date +%Y%m%d).db
```

### Dashboard Output

HTML dashboards are generated in:
```
plugins/portfolio-copilot/data/portfolio-dashboard-YYYY-MM-DD.html
```

## What's Next?

### Add Your First Stock

```bash
cd plugins/portfolio-copilot/scripts
python3 portfolio_manager.py add AAPL 50 180.50 --notes "Tech leader"
```

### Analyze It

```
User (in Claude Code): "analyze AAPL"
```

### Review Your Portfolio

```
User (in Claude Code): "review my portfolio"
```

## Advanced Usage

### Multiple Portfolios

Create separate portfolios for different strategies:

```bash
python3 portfolio_manager.py create "Growth Portfolio"
python3 portfolio_manager.py create "Value Portfolio"
python3 portfolio_manager.py create "Retirement Portfolio"
```

### Korean Stocks

Add Korean stocks using KRX codes:

```bash
python3 portfolio_manager.py add 005930 100 65000  # Samsung Electronics
python3 portfolio_manager.py add 000660 50 120000  # SK Hynix
```

### Batch Operations

Score multiple stocks at once:

```bash
# Score entire portfolio
python3 portfolio_manager.py score

# Score specific tickers
for ticker in AAPL MSFT GOOGL; do
  python3 scorecard.py $ticker
done
```

## Uninstallation

To remove portfolio-copilot:

```bash
# 1. Backup your data
cp data/portfolio.db ~/portfolio-backup.db

# 2. Remove symlinks
rm ~/.claude/skills/analyze-stock
rm ~/.claude/skills/portfolio-review

# 3. Uninstall Python packages (optional)
pip3 uninstall yfinance pykrx pandas numpy sqlalchemy

# 4. Delete plugin directory (if desired)
rm -rf plugins/portfolio-copilot
```

## Support

For issues or questions:

1. Check [README.md](README.md) for feature documentation
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. See [SESSION_SUMMARY.md](SESSION_SUMMARY.md) for development history
4. Report bugs at: https://github.com/JayKim88/claude-ai-engineering/issues

## Version

- **Current Version**: 1.0.0
- **Phase**: Phase 1 Complete (Observer Mode)
- **Last Updated**: 2026-02-13
