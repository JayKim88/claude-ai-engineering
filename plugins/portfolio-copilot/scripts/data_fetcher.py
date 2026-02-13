"""
DataSourceManager - Unified interface for fetching stock data from multiple sources.

Supports:
- UsStockInfo MCP (primary for US stocks when available)
- yfinance (fallback for US stocks, primary for global data)
- pykrx (primary for Korean stocks)

Auto-detects market (US vs KR) based on ticker format and provides seamless fallback.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import yfinance as yf


class DataSourceManager:
    """
    Unified data source manager with automatic market detection and fallback logic.

    Priority:
    - US stocks: MCP (if available) → yfinance
    - KR stocks: pykrx
    - Global indices/FX: yfinance
    """

    def __init__(self, mcp_available=False):
        """
        Initialize data source manager.

        Args:
            mcp_available: Whether UsStockInfo MCP is available in current session
        """
        self.mcp_available = mcp_available
        self.cache = {}  # In-memory cache for session

    def detect_market(self, ticker: str) -> str:
        """
        Detect market (US or KR) based on ticker format.

        Args:
            ticker: Stock ticker symbol

        Returns:
            'US' for US stocks, 'KR' for Korean stocks

        Examples:
            detect_market('AAPL') → 'US'
            detect_market('005930') → 'KR'
        """
        # Korean stocks: 6-digit numbers
        if re.match(r'^\d{6}$', ticker):
            return 'KR'
        # US stocks: 1-5 letter symbols
        elif re.match(r'^[A-Z]{1,5}$', ticker.upper()):
            return 'US'
        else:
            # Default to US for mixed formats
            return 'US'

    def get_stock_info(self, ticker: str) -> Dict:
        """
        Get comprehensive stock information.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with stock info including:
            - price: current price
            - market_cap: market capitalization
            - pe_ratio: price-to-earnings ratio
            - pb_ratio: price-to-book ratio
            - sector: industry sector
            - ... and more
        """
        market = self.detect_market(ticker)

        if market == 'US':
            return self._get_us_stock_info(ticker)
        elif market == 'KR':
            return self._get_kr_stock_info(ticker)

    def get_historical_prices(self, ticker: str, period: str = '1y', interval: str = '1d') -> Dict:
        """
        Get historical price data.

        Args:
            ticker: Stock ticker symbol
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo')

        Returns:
            Dictionary with OHLCV data
        """
        market = self.detect_market(ticker)

        if market == 'US':
            return self._get_us_historical(ticker, period, interval)
        elif market == 'KR':
            return self._get_kr_historical(ticker, period)

    def get_financials(self, ticker: str) -> Dict:
        """
        Get financial statements (income statement, balance sheet, cash flow).

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with quarterly and annual financials
        """
        market = self.detect_market(ticker)

        if market == 'US':
            return self._get_us_financials(ticker)
        elif market == 'KR':
            return self._get_kr_financials(ticker)

    # ===== US Stock Methods =====

    def _get_us_stock_info(self, ticker: str) -> Dict:
        """Get US stock info with MCP fallback to yfinance."""

        # Try MCP first if available
        if self.mcp_available:
            try:
                # TODO: Implement MCP call when session is active
                # data = mcp__claude_ai_PlayMCP__UsStockInfo_get_stock_info(ticker)
                # return self._parse_mcp_stock_info(data)
                pass
            except Exception as e:
                print(f"⚠️  MCP failed: {e}, falling back to yfinance")

        # Fallback to yfinance
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'price': info.get('currentPrice', info.get('regularMarketPrice')),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'pb_ratio': info.get('priceToBook'),
                'ps_ratio': info.get('priceToSalesTrailing12Months'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'eps': info.get('trailingEps'),
                'revenue': info.get('totalRevenue'),
                # Financial metrics (Sprint 4 fix)
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'operating_margin': info.get('operatingMargins'),
                'net_margin': info.get('profitMargins'),
                'profit_margin': info.get('profitMargins'),
                'gross_margin': info.get('grossMargins'),
                'ebitda_margin': info.get('ebitdaMargins'),
                'revenue_growth': info.get('revenueGrowth'),
                'earnings_growth': info.get('earningsGrowth'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'debt_to_equity': info.get('debtToEquity'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'avg_volume': info.get('averageVolume'),
                'shares_outstanding': info.get('sharesOutstanding'),
                'source': 'yfinance',
                'fetched_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to fetch {ticker}: {str(e)}", 'ticker': ticker}

    def _get_us_historical(self, ticker: str, period: str, interval: str) -> Dict:
        """Get US stock historical prices from yfinance."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)

            if hist.empty:
                return {'error': f"No data found for {ticker}", 'ticker': ticker}

            return {
                'ticker': ticker,
                'period': period,
                'interval': interval,
                'data': hist.to_dict(orient='index'),  # Date as key
                'source': 'yfinance',
                'fetched_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to fetch historical data for {ticker}: {str(e)}", 'ticker': ticker}

    def _get_us_financials(self, ticker: str) -> Dict:
        """Get US stock financials from yfinance (with MCP fallback in future)."""
        try:
            stock = yf.Ticker(ticker)

            return {
                'ticker': ticker,
                'income_stmt': stock.income_stmt.to_dict() if hasattr(stock, 'income_stmt') and stock.income_stmt is not None else {},
                'quarterly_income_stmt': stock.quarterly_income_stmt.to_dict() if hasattr(stock, 'quarterly_income_stmt') and stock.quarterly_income_stmt is not None else {},
                'balance_sheet': stock.balance_sheet.to_dict() if hasattr(stock, 'balance_sheet') and stock.balance_sheet is not None else {},
                'quarterly_balance_sheet': stock.quarterly_balance_sheet.to_dict() if hasattr(stock, 'quarterly_balance_sheet') and stock.quarterly_balance_sheet is not None else {},
                'cashflow': stock.cashflow.to_dict() if hasattr(stock, 'cashflow') and stock.cashflow is not None else {},
                'quarterly_cashflow': stock.quarterly_cashflow.to_dict() if hasattr(stock, 'quarterly_cashflow') and stock.quarterly_cashflow is not None else {},
                'source': 'yfinance',
                'fetched_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to fetch financials for {ticker}: {str(e)}", 'ticker': ticker}

    # ===== Korean Stock Methods =====

    def _get_kr_stock_info(self, ticker: str) -> Dict:
        """Get Korean stock info from pykrx."""
        try:
            # Import pykrx only when needed
            from pykrx import stock

            # Get latest trading day
            today = datetime.now().strftime('%Y%m%d')

            # Get current price
            df = stock.get_market_ohlcv_by_date(today, today, ticker)
            if df.empty:
                return {'error': f"No data found for Korean stock {ticker}", 'ticker': ticker}

            latest = df.iloc[-1]

            # Get fundamental data
            fundamental = stock.get_market_fundamental_by_date(today, today, ticker)

            result = {
                'ticker': ticker,
                'price': int(latest['종가']),
                'currency': 'KRW',
                'volume': int(latest['거래량']),
                'market': 'KR',
                'source': 'pykrx',
                'fetched_at': datetime.now().isoformat()
            }

            # Add fundamental ratios if available
            if not fundamental.empty:
                fund = fundamental.iloc[-1]
                result.update({
                    'pe_ratio': float(fund['PER']) if 'PER' in fund else None,
                    'pb_ratio': float(fund['PBR']) if 'PBR' in fund else None,
                    'dividend_yield': float(fund['DIV']) if 'DIV' in fund else None,
                })

            return result

        except ImportError:
            return {'error': 'pykrx not installed. Run: pip install pykrx', 'ticker': ticker}
        except Exception as e:
            return {'error': f"Failed to fetch Korean stock {ticker}: {str(e)}", 'ticker': ticker}

    def _get_kr_historical(self, ticker: str, period: str) -> Dict:
        """Get Korean stock historical prices from pykrx."""
        try:
            from pykrx import stock

            # Convert period to date range
            end_date = datetime.now()
            if period == '1mo':
                start_date = end_date - timedelta(days=30)
            elif period == '3mo':
                start_date = end_date - timedelta(days=90)
            elif period == '6mo':
                start_date = end_date - timedelta(days=180)
            elif period == '1y':
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=365)  # Default 1 year

            start_str = start_date.strftime('%Y%m%d')
            end_str = end_date.strftime('%Y%m%d')

            df = stock.get_market_ohlcv_by_date(start_str, end_str, ticker)

            if df.empty:
                return {'error': f"No historical data for {ticker}", 'ticker': ticker}

            return {
                'ticker': ticker,
                'period': period,
                'data': df.to_dict(orient='index'),
                'source': 'pykrx',
                'fetched_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to fetch Korean historical data for {ticker}: {str(e)}", 'ticker': ticker}

    def _get_kr_financials(self, ticker: str) -> Dict:
        """Get Korean stock financials from pykrx."""
        # pykrx has limited financial data, mainly focused on price/volume
        # For detailed Korean financials, would need DART API integration (Phase 2)
        return {
            'ticker': ticker,
            'note': 'Detailed Korean financials require DART API (coming in Phase 2)',
            'source': 'pykrx',
            'fetched_at': datetime.now().isoformat()
        }


# Convenience functions
def get_data_source_manager(mcp_available=False) -> DataSourceManager:
    """Get a DataSourceManager instance."""
    return DataSourceManager(mcp_available=mcp_available)


def get_stock_data(ticker: str, market: str = None) -> Dict:
    """
    Simple convenience function to get stock data.

    Args:
        ticker: Stock ticker symbol
        market: Market hint ('US' or 'KR'), auto-detected if not provided

    Returns:
        Dictionary with stock info including 'current_price', 'pe_ratio', 'sector', etc.
    """
    dsm = get_data_source_manager()
    info = dsm.get_stock_info(ticker)

    if 'error' in info:
        return {}

    # Normalize field names for backward compatibility
    result = info.copy()
    if 'price' in result and 'current_price' not in result:
        result['current_price'] = result['price']

    return result


if __name__ == "__main__":
    # Test data source manager
    print("Testing DataSourceManager...")
    print()

    dsm = get_data_source_manager()

    # Test US stock
    print("🇺🇸 Testing US stock (AAPL)...")
    aapl_info = dsm.get_stock_info('AAPL')
    if 'error' not in aapl_info:
        print(f"✅ {aapl_info['name']}")
        print(f"   Price: ${aapl_info['price']:.2f}")
        print(f"   P/E: {aapl_info['pe_ratio']:.2f}" if aapl_info['pe_ratio'] else "   P/E: N/A")
        print(f"   Sector: {aapl_info['sector']}")
    else:
        print(f"❌ Error: {aapl_info['error']}")

    print()

    # Test Korean stock
    print("🇰🇷 Testing Korean stock (005930 - Samsung)...")
    samsung_info = dsm.get_stock_info('005930')
    if 'error' not in samsung_info:
        print(f"✅ Samsung Electronics (005930)")
        print(f"   Price: ₩{samsung_info['price']:,}")
        print(f"   P/E: {samsung_info.get('pe_ratio', 'N/A')}")
    else:
        print(f"❌ Error: {samsung_info['error']}")

    print()
    print("✅ DataSourceManager test complete!")
