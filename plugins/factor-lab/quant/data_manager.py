#!/usr/bin/env python3
"""
Data Manager for factor-lab

Handles:
- Data fetching from yfinance (US stocks) and pykrx (KR stocks)
- SQLite caching (30-day validity)
- Universe definitions (S&P 500, KOSPI 200, etc.)
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import yfinance as yf

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cache directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(CACHE_DIR, exist_ok=True)

DB_PATH = os.path.join(CACHE_DIR, 'market_data_cache.db')
CACHE_VALIDITY_DAYS = 30


class QuantDataManager:
    """
    Data fetching and caching manager

    Features:
    - yfinance for US stocks (OHLCV + fundamentals)
    - pykrx for Korean stocks
    - SQLite caching (30-day validity)
    - Universe definitions (S&P 500, KOSPI 200, etc.)
    """

    def __init__(self):
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Table: stock_info (fundamentals)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_info (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                price REAL,
                market_cap REAL,
                pe_ratio REAL,
                pb_ratio REAL,
                roe REAL,
                debt_to_equity REAL,
                operating_margin REAL,
                net_margin REAL,
                current_ratio REAL,
                beta REAL,
                updated_at TEXT
            )
        ''')

        # Table: historical_prices (OHLCV)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_prices (
                ticker TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (ticker, date)
            )
        ''')

        # Table: universe_members
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS universe_members (
                universe TEXT,
                ticker TEXT,
                updated_at TEXT,
                PRIMARY KEY (universe, ticker)
            )
        ''')

        conn.commit()
        conn.close()

    def get_universe(self, name: str) -> List[str]:
        """
        Get list of tickers in a universe

        Args:
            name: Universe name (SP500, KOSPI200, NASDAQ100)

        Returns:
            List of ticker symbols
        """
        # Check cache first
        cached_tickers = self._get_cached_universe(name)
        if cached_tickers:
            print(f"✓ Using cached {name} universe ({len(cached_tickers)} tickers)")
            return cached_tickers

        # Fetch fresh data
        print(f"Fetching {name} universe from source...")

        if name == 'SP500':
            tickers = self._fetch_sp500()
        elif name == 'NASDAQ100':
            tickers = self._fetch_nasdaq100()
        elif name == 'KOSPI200':
            tickers = self._fetch_kospi200()
        elif name == 'KOSDAQ150':
            tickers = self._fetch_kosdaq150()
        else:
            raise ValueError(f"Unknown universe: {name}")

        # Cache the result
        self._cache_universe(name, tickers)

        print(f"✓ Fetched {len(tickers)} tickers from {name}")
        return tickers

    def _get_cached_universe(self, name: str) -> Optional[List[str]]:
        """Check if cached universe is still valid"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT ticker, updated_at FROM universe_members
            WHERE universe = ?
        ''', (name,))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return None

        # Check if cache is still valid (30 days)
        updated_at = datetime.fromisoformat(rows[0][1])
        if datetime.now() - updated_at > timedelta(days=CACHE_VALIDITY_DAYS):
            return None

        return [row[0] for row in rows]

    def _cache_universe(self, name: str, tickers: List[str]):
        """Cache universe members"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Delete old cache
        cursor.execute('DELETE FROM universe_members WHERE universe = ?', (name,))

        # Insert new cache
        updated_at = datetime.now().isoformat()
        for ticker in tickers:
            cursor.execute('''
                INSERT INTO universe_members (universe, ticker, updated_at)
                VALUES (?, ?, ?)
            ''', (name, ticker, updated_at))

        conn.commit()
        conn.close()

    def _fetch_sp500(self) -> List[str]:
        """Fetch S&P 500 tickers from Wikipedia"""
        try:
            import ssl
            import urllib.request

            # Create SSL context (bypass certificate verification for Wikipedia)
            ssl_context = ssl._create_unverified_context()

            # Read S&P 500 list from Wikipedia
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

            # Add User-Agent header to avoid 403 Forbidden
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (factor-lab/1.0)'}
            )

            # Pandas read_html with custom headers
            with urllib.request.urlopen(req, context=ssl_context) as response:
                tables = pd.read_html(response.read())

            df = tables[0]
            tickers = df['Symbol'].tolist()

            # Clean tickers (replace dots with dashes for yfinance)
            tickers = [t.replace('.', '-') for t in tickers]

            return tickers
        except Exception as e:
            print(f"Error fetching S&P 500: {e}")
            # Fallback: return major tech stocks
            return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'NFLX', 'INTC']

    def _fetch_nasdaq100(self) -> List[str]:
        """Fetch NASDAQ 100 tickers"""
        try:
            url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
            tables = pd.read_html(url)
            df = tables[4]  # NASDAQ-100 components table
            tickers = df['Ticker'].tolist()
            return tickers
        except Exception as e:
            print(f"Error fetching NASDAQ 100: {e}")
            # Fallback: return major tech stocks
            return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'NFLX']

    def _fetch_kospi200(self) -> List[str]:
        """Fetch KOSPI 200 tickers using pykrx"""
        try:
            from pykrx import stock

            # Get KOSPI 200 tickers
            tickers = stock.get_index_ticker_list("20250213", "1028")  # KOSPI 200 code
            return tickers
        except Exception as e:
            print(f"Error fetching KOSPI 200: {e}")
            # Fallback: return major Korean stocks
            return ['005930', '000660', '035420', '051910', '035720']  # Samsung, SK, Naver, LG Chem, Kakao

    def _fetch_kosdaq150(self) -> List[str]:
        """Fetch KOSDAQ 150 tickers using pykrx"""
        try:
            from pykrx import stock

            # Get KOSDAQ 150 tickers
            tickers = stock.get_index_ticker_list("20250213", "2203")  # KOSDAQ 150 code
            return tickers
        except Exception as e:
            print(f"Error fetching KOSDAQ 150: {e}")
            # Fallback
            return ['091990', '068270', '263750']  # Celltrion Healthcare, Celltrion, Pearl Abyss

    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Get stock fundamentals

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with fundamentals (price, PE, PB, ROE, etc.)
        """
        # Check cache first
        cached_info = self._get_cached_stock_info(ticker)
        if cached_info:
            return cached_info

        # Fetch from yfinance
        try:
            print(f"Fetching {ticker} info from yfinance...")
            stock = yf.Ticker(ticker)
            info = stock.info

            stock_info = {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'price': info.get('currentPrice', info.get('regularMarketPrice')),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'pb_ratio': info.get('priceToBook'),
                'roe': info.get('returnOnEquity'),
                'debt_to_equity': info.get('debtToEquity'),
                'operating_margin': info.get('operatingMargins'),
                'net_margin': info.get('profitMargins'),
                'current_ratio': info.get('currentRatio'),
                'beta': info.get('beta')
            }

            # Cache the result
            self._cache_stock_info(stock_info)

            return stock_info

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def _get_cached_stock_info(self, ticker: str) -> Optional[Dict]:
        """Check if cached stock info is still valid"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM stock_info WHERE ticker = ?
        ''', (ticker,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Check if cache is still valid (30 days)
        updated_at = datetime.fromisoformat(row[13])  # updated_at column
        if datetime.now() - updated_at > timedelta(days=CACHE_VALIDITY_DAYS):
            return None

        # Convert to dict
        columns = ['ticker', 'name', 'sector', 'price', 'market_cap', 'pe_ratio', 'pb_ratio',
                   'roe', 'debt_to_equity', 'operating_margin', 'net_margin', 'current_ratio', 'beta']

        return {col: row[i] for i, col in enumerate(columns)}

    def _cache_stock_info(self, stock_info: Dict):
        """Cache stock info"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        updated_at = datetime.now().isoformat()

        cursor.execute('''
            INSERT OR REPLACE INTO stock_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            stock_info['ticker'],
            stock_info['name'],
            stock_info['sector'],
            stock_info['price'],
            stock_info['market_cap'],
            stock_info['pe_ratio'],
            stock_info['pb_ratio'],
            stock_info['roe'],
            stock_info['debt_to_equity'],
            stock_info['operating_margin'],
            stock_info['net_margin'],
            stock_info['current_ratio'],
            stock_info['beta'],
            updated_at
        ))

        conn.commit()
        conn.close()

    def get_historical_data(self, ticker: str, start: str, end: str, force_refresh: bool = False) -> Optional[pd.DataFrame]:
        """
        Get historical OHLCV data

        Args:
            ticker: Stock ticker
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            DataFrame with OHLCV data
        """
        # Check cache first (unless force_refresh)
        if not force_refresh:
            cached_data = self._get_cached_historical(ticker, start, end)
            if cached_data is not None and len(cached_data) > 0:
                return cached_data

        # Fetch from yfinance
        try:
            print(f"Fetching {ticker} historical data ({start} to {end})...")
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end)

            if hist.empty:
                print(f"No data available for {ticker}")
                return None

            # Cache the result
            self._cache_historical(ticker, hist)

            return hist

        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None

    def _get_cached_historical(self, ticker: str, start: str, end: str) -> Optional[pd.DataFrame]:
        """Check if cached historical data covers the requested period"""
        conn = sqlite3.connect(DB_PATH)

        query = '''
            SELECT date, open, high, low, close, volume
            FROM historical_prices
            WHERE ticker = ? AND date >= ? AND date <= ?
            ORDER BY date
        '''

        df = pd.read_sql_query(query, conn, params=(ticker, start, end))
        conn.close()

        if df.empty:
            return None

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Capitalize column names to match yfinance format
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        return df

    def _cache_historical(self, ticker: str, df: pd.DataFrame):
        """Cache historical data"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for date, row in df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO historical_prices VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                ticker,
                date.strftime('%Y-%m-%d'),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                int(row['Volume'])
            ))

        conn.commit()
        conn.close()

    def _update_cache_validity(self, ticker: str, validity_days: int) -> None:
        """
        Update cache validity for a ticker

        Note: For historical prices, data is cached permanently in historical_prices table.
        This method is a no-op placeholder for future cache management features.

        Args:
            ticker: Stock ticker symbol
            validity_days: Number of days to keep cache valid
        """
        # Historical prices are already cached in historical_prices table
        # No need to update cache validity since we check by date range
        pass

    def get_financials(self, ticker: str) -> Optional[Dict]:
        """
        Get financial statements

        Args:
            ticker: Stock ticker

        Returns:
            Dict with income_stmt, balance_sheet, cashflow
        """
        try:
            stock = yf.Ticker(ticker)

            return {
                'income_stmt': stock.financials,
                'balance_sheet': stock.balance_sheet,
                'cashflow': stock.cashflow
            }
        except Exception as e:
            print(f"Error fetching financials for {ticker}: {e}")
            return None


def main():
    """Test data manager"""
    manager = QuantDataManager()

    # Test 1: Get universe
    print("\n" + "="*60)
    print("TEST 1: Get S&P 500 Universe")
    print("="*60)
    tickers = manager.get_universe('SP500')
    print(f"First 10 tickers: {tickers[:10]}")

    # Test 2: Get stock info
    print("\n" + "="*60)
    print("TEST 2: Get AAPL Stock Info")
    print("="*60)
    info = manager.get_stock_info('AAPL')
    if info:
        print(f"Name: {info['name']}")
        print(f"Sector: {info['sector']}")
        print(f"Price: ${info['price']:.2f}" if info['price'] else "Price: N/A")
        print(f"P/E: {info['pe_ratio']:.2f}" if info['pe_ratio'] else "P/E: N/A")
        print(f"ROE: {info['roe']*100:.2f}%" if info['roe'] else "ROE: N/A")

    # Test 3: Get historical data
    print("\n" + "="*60)
    print("TEST 3: Get AAPL Historical Data (1 year)")
    print("="*60)
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    hist = manager.get_historical_data('AAPL', start_date, end_date)
    if hist is not None:
        print(f"Data points: {len(hist)}")
        print(f"\nLast 5 days:")
        print(hist.tail())


if __name__ == '__main__':
    main()
