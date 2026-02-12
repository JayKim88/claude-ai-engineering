#!/usr/bin/env python3
"""
Multi-source stock data fetcher with fallback chain: MCP → yfinance → pykrx.
Part of portfolio-analyzer-fused plugin.
"""
import json
import sys
from datetime import datetime, timedelta

def fetch_from_mcp(ticker):
    """
    Try fetching from UsStockInfo MCP server (primary source).

    Returns:
        dict with stock data or None if unavailable
    """
    try:
        # TODO: Implement actual MCP server call when available
        # For now, return None to trigger fallback
        # import subprocess
        # result = subprocess.run(['claude-mcp', 'call', 'UsStockInfo', 'get_stock_info', ticker],
        #                        capture_output=True, text=True, timeout=10)
        # if result.returncode == 0:
        #     return json.loads(result.stdout)
        return None
    except Exception:
        return None

def fetch_from_yfinance(ticker):
    """
    Fallback to yfinance for US and global stocks.

    Returns:
        dict with stock data or None if unavailable
    """
    try:
        import yfinance as yf

        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")

        if hist.empty or not info:
            return None

        # Calculate technical indicators
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not current_price and not hist.empty:
            current_price = hist['Close'].iloc[-1]

        # 50-day and 200-day moving averages
        ma_50 = hist['Close'].tail(50).mean() if len(hist) >= 50 else None
        ma_200 = hist['Close'].tail(200).mean() if len(hist) >= 200 else None

        # 3-month return
        if len(hist) >= 60:
            three_mo_return = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-60]) / hist['Close'].iloc[-60]) * 100
        else:
            three_mo_return = None

        # Volume trend
        avg_volume = hist['Volume'].mean() if len(hist) > 0 else None

        data = {
            "ticker": ticker,
            "source": "yfinance",
            "timestamp": datetime.now().isoformat(),
            "price": {
                "current": current_price,
                "open": info.get('open'),
                "high": info.get('dayHigh'),
                "low": info.get('dayLow'),
                "previous_close": info.get('previousClose'),
                "52w_high": info.get('fiftyTwoWeekHigh'),
                "52w_low": info.get('fiftyTwoWeekLow')
            },
            "fundamentals": {
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "forward_pe": info.get('forwardPE'),
                "peg_ratio": info.get('pegRatio'),
                "pb_ratio": info.get('priceToBook'),
                "ps_ratio": info.get('priceToSalesTrailing12Months'),
                "debt_to_equity": info.get('debtToEquity'),
                "roe": info.get('returnOnEquity'),
                "profit_margin": info.get('profitMargins'),
                "revenue_growth": info.get('revenueGrowth'),
                "earnings_growth": info.get('earningsGrowth')
            },
            "technicals": {
                "ma_50": ma_50,
                "ma_200": ma_200,
                "three_month_return": three_mo_return,
                "beta": info.get('beta'),
                "avg_volume": avg_volume
            },
            "company": {
                "name": info.get('longName') or info.get('shortName'),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "country": info.get('country'),
                "currency": info.get('currency', 'USD')
            }
        }

        return data

    except ImportError:
        print("⚠️  yfinance not installed. Install: pip install yfinance", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️  yfinance error for {ticker}: {e}", file=sys.stderr)
        return None

def fetch_from_pykrx(ticker):
    """
    Fallback to pykrx for Korean stocks (KOSPI/KOSDAQ).

    Returns:
        dict with stock data or None if unavailable
    """
    try:
        from pykrx import stock
        from datetime import datetime, timedelta

        # Try to fetch Korean stock data
        today = datetime.now().strftime("%Y%m%d")
        one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

        # Get OHLCV data
        df = stock.get_market_ohlcv_by_date(one_year_ago, today, ticker)

        if df.empty:
            return None

        current_price = df['종가'].iloc[-1]

        # Calculate indicators
        ma_50 = df['종가'].tail(50).mean() if len(df) >= 50 else None
        ma_200 = df['종가'].tail(200).mean() if len(df) >= 200 else None

        if len(df) >= 60:
            three_mo_return = ((df['종가'].iloc[-1] - df['종가'].iloc[-60]) / df['종가'].iloc[-60]) * 100
        else:
            three_mo_return = None

        # Get fundamental data
        try:
            fundamental = stock.get_market_fundamental(today, today, ticker)
            if not fundamental.empty:
                per = fundamental['PER'].iloc[0] if 'PER' in fundamental else None
                pbr = fundamental['PBR'].iloc[0] if 'PBR' in fundamental else None
            else:
                per, pbr = None, None
        except:
            per, pbr = None, None

        data = {
            "ticker": ticker,
            "source": "pykrx",
            "timestamp": datetime.now().isoformat(),
            "price": {
                "current": current_price,
                "open": df['시가'].iloc[-1],
                "high": df['고가'].iloc[-1],
                "low": df['저가'].iloc[-1],
                "previous_close": df['종가'].iloc[-2] if len(df) >= 2 else None,
                "52w_high": df['고가'].max(),
                "52w_low": df['저가'].min()
            },
            "fundamentals": {
                "market_cap": None,
                "pe_ratio": per,
                "pb_ratio": pbr
            },
            "technicals": {
                "ma_50": ma_50,
                "ma_200": ma_200,
                "three_month_return": three_mo_return,
                "avg_volume": df['거래량'].mean()
            },
            "company": {
                "name": ticker,
                "country": "KR",
                "currency": "KRW"
            }
        }

        return data

    except ImportError:
        print("⚠️  pykrx not installed. Install: pip install pykrx", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️  pykrx error for {ticker}: {e}", file=sys.stderr)
        return None

def fetch_stock_data(ticker):
    """
    Fetch stock data with fallback chain: MCP → yfinance → pykrx.

    Args:
        ticker: Stock ticker symbol

    Returns:
        0 on success (prints JSON to stdout), 1 on failure
    """
    # Try each source in order
    data = fetch_from_mcp(ticker)

    if not data:
        data = fetch_from_yfinance(ticker)

    if not data:
        data = fetch_from_pykrx(ticker)

    if data:
        print(json.dumps(data, indent=2, default=str))
        return 0
    else:
        error = {
            "error": f"No data found for ticker: {ticker}",
            "ticker": ticker,
            "tried_sources": ["mcp", "yfinance", "pykrx"]
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_stock_data.py TICKER", file=sys.stderr)
        print("Example: python3 fetch_stock_data.py AAPL", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    sys.exit(fetch_stock_data(ticker))
