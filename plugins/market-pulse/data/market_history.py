"""
Market History Database Manager
Stores historical OHLCV data and multi-period returns for market analysis.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd


class MarketHistoryDB:
    """
    SQLite database manager for storing and retrieving historical market data.

    Features:
    - Daily OHLCV prices (60-day rolling window)
    - Multi-period returns (1d, 5d, 20d, 60d)
    - Duplicate prevention with UNIQUE constraints
    - Efficient querying with indexes
    """

    def __init__(self, db_path: str = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file.
                     Defaults to plugins/market-pulse/data/market_history.db
        """
        if db_path is None:
            # Default path: same directory as this file
            db_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(db_dir, "market_history.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Table 1: Daily OHLCV prices
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_prices (
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                adj_close REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (symbol, date)
            )
        """)

        # Table 2: Multi-period returns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multi_period_returns (
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                return_1d REAL,
                return_5d REAL,
                return_20d REAL,
                return_60d REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (symbol, date)
            )
        """)

        # Table 3: Sector performance history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sector_performance (
                sector_symbol TEXT NOT NULL,
                sector_name TEXT NOT NULL,
                date TEXT NOT NULL,
                close REAL,
                return_1d REAL,
                return_5d REAL,
                return_20d REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (sector_symbol, date)
            )
        """)

        # Table 4: Korean market foreign/institutional flows
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kr_market_flows (
                date TEXT NOT NULL,
                kospi_foreign REAL,
                kospi_institutional REAL,
                kosdaq_foreign REAL,
                kosdaq_institutional REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (date)
            )
        """)

        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_daily_prices_symbol
            ON daily_prices(symbol)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_daily_prices_date
            ON daily_prices(date)
        """)

        self.conn.commit()

    def save_daily_prices(
        self,
        symbol: str,
        date: str,
        ohlcv: Dict[str, float]
    ) -> bool:
        """
        Save or update daily OHLCV data.

        Args:
            symbol: Stock/ETF ticker symbol (e.g., "^GSPC", "005930")
            date: Date in YYYY-MM-DD format
            ohlcv: Dictionary with keys: open, high, low, close, volume, adj_close

        Returns:
            True if saved successfully, False otherwise
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO daily_prices
                (symbol, date, open, high, low, close, volume, adj_close)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                symbol,
                date,
                ohlcv.get('open'),
                ohlcv.get('high'),
                ohlcv.get('low'),
                ohlcv.get('close'),
                ohlcv.get('volume'),
                ohlcv.get('adj_close', ohlcv.get('close'))  # Fallback to close if adj_close missing
            ))

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error saving daily prices for {symbol} on {date}: {e}")
            return False

    def save_multi_period_returns(
        self,
        symbol: str,
        date: str,
        returns: Dict[str, float]
    ) -> bool:
        """
        Save multi-period returns (1d, 5d, 20d, 60d).

        Args:
            symbol: Stock/ETF ticker symbol
            date: Date in YYYY-MM-DD format
            returns: Dictionary with keys: return_1d, return_5d, return_20d, return_60d

        Returns:
            True if saved successfully
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO multi_period_returns
                (symbol, date, return_1d, return_5d, return_20d, return_60d)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                symbol,
                date,
                returns.get('return_1d'),
                returns.get('return_5d'),
                returns.get('return_20d'),
                returns.get('return_60d')
            ))

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error saving returns for {symbol} on {date}: {e}")
            return False

    def get_historical_prices(
        self,
        symbol: str,
        days: int = 60,
        end_date: str = None
    ) -> pd.DataFrame:
        """
        Retrieve historical prices for a symbol.

        Args:
            symbol: Stock/ETF ticker symbol
            days: Number of days to retrieve (default: 60)
            end_date: End date in YYYY-MM-DD format (default: today)

        Returns:
            DataFrame with columns: date, open, high, low, close, volume, adj_close
        """
        cursor = self.conn.cursor()

        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        # Calculate start_date
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=days)
        start_date = start_dt.strftime('%Y-%m-%d')

        cursor.execute("""
            SELECT date, open, high, low, close, volume, adj_close
            FROM daily_prices
            WHERE symbol = ? AND date >= ? AND date <= ?
            ORDER BY date ASC
        """, (symbol, start_date, end_date))

        rows = cursor.fetchall()

        if not rows:
            return pd.DataFrame()

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close'])
        df['date'] = pd.to_datetime(df['date'])

        return df

    def get_latest_date(self, symbol: str) -> Optional[str]:
        """
        Get the most recent date for which data exists for a symbol.

        Args:
            symbol: Stock/ETF ticker symbol

        Returns:
            Latest date as YYYY-MM-DD string, or None if no data
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT MAX(date) as latest_date
            FROM daily_prices
            WHERE symbol = ?
        """, (symbol,))

        row = cursor.fetchone()
        return row['latest_date'] if row else None

    def calculate_and_save_returns(self, symbol: str) -> bool:
        """
        Calculate multi-period returns for all available dates and save to DB.

        Args:
            symbol: Stock/ETF ticker symbol

        Returns:
            True if calculation successful
        """
        # Get all historical prices
        df = self.get_historical_prices(symbol, days=365)  # Get up to 1 year

        if df.empty or len(df) < 2:
            return False

        # Calculate returns
        df = df.sort_values('date')
        df['return_1d'] = df['close'].pct_change(periods=1) * 100
        df['return_5d'] = df['close'].pct_change(periods=5) * 100
        df['return_20d'] = df['close'].pct_change(periods=20) * 100
        df['return_60d'] = df['close'].pct_change(periods=60) * 100

        # Save to database
        for _, row in df.iterrows():
            if pd.notna(row['return_1d']):  # Skip first row (NaN)
                self.save_multi_period_returns(
                    symbol=symbol,
                    date=row['date'].strftime('%Y-%m-%d'),
                    returns={
                        'return_1d': row['return_1d'],
                        'return_5d': row['return_5d'] if pd.notna(row['return_5d']) else None,
                        'return_20d': row['return_20d'] if pd.notna(row['return_20d']) else None,
                        'return_60d': row['return_60d'] if pd.notna(row['return_60d']) else None
                    }
                )

        return True

    def get_data_coverage(self, symbol: str) -> Dict[str, any]:
        """
        Get data coverage statistics for a symbol.

        Args:
            symbol: Stock/ETF ticker symbol

        Returns:
            Dictionary with keys: count, earliest_date, latest_date, days_covered
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as count,
                MIN(date) as earliest_date,
                MAX(date) as latest_date
            FROM daily_prices
            WHERE symbol = ?
        """, (symbol,))

        row = cursor.fetchone()

        if row and row['count'] > 0:
            earliest = datetime.strptime(row['earliest_date'], '%Y-%m-%d')
            latest = datetime.strptime(row['latest_date'], '%Y-%m-%d')
            days_covered = (latest - earliest).days + 1

            return {
                'count': row['count'],
                'earliest_date': row['earliest_date'],
                'latest_date': row['latest_date'],
                'days_covered': days_covered
            }

        return {'count': 0}

    def cleanup_old_data(self, days_to_keep: int = 90):
        """
        Delete data older than specified days to keep database size manageable.

        Args:
            days_to_keep: Number of days of history to retain (default: 90)
        """
        cursor = self.conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')

        cursor.execute("DELETE FROM daily_prices WHERE date < ?", (cutoff_date,))
        cursor.execute("DELETE FROM multi_period_returns WHERE date < ?", (cutoff_date,))
        cursor.execute("DELETE FROM sector_performance WHERE date < ?", (cutoff_date,))
        cursor.execute("DELETE FROM kr_market_flows WHERE date < ?", (cutoff_date,))

        self.conn.commit()

        print(f"Cleaned up data older than {cutoff_date}")

    def get_all_symbols(self) -> List[str]:
        """
        Get list of all symbols stored in database.

        Returns:
            List of unique symbol strings
        """
        cursor = self.conn.cursor()

        cursor.execute("SELECT DISTINCT symbol FROM daily_prices ORDER BY symbol")

        return [row['symbol'] for row in cursor.fetchall()]

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience function for one-off operations
def get_db(db_path: str = None) -> MarketHistoryDB:
    """
    Create and return a MarketHistoryDB instance.

    Args:
        db_path: Optional custom database path

    Returns:
        MarketHistoryDB instance
    """
    return MarketHistoryDB(db_path=db_path)


if __name__ == "__main__":
    # Test the database
    print("Testing MarketHistoryDB...")

    with MarketHistoryDB() as db:
        print(f"Database created at: {db.db_path}")

        # Test saving data
        test_symbol = "^GSPC"
        test_date = "2026-02-11"
        test_ohlcv = {
            'open': 5900.0,
            'high': 5920.5,
            'low': 5880.2,
            'close': 5915.3,
            'volume': 3500000000,
            'adj_close': 5915.3
        }

        success = db.save_daily_prices(test_symbol, test_date, test_ohlcv)
        print(f"Save test data: {'✅ Success' if success else '❌ Failed'}")

        # Test retrieval
        coverage = db.get_data_coverage(test_symbol)
        print(f"Data coverage for {test_symbol}: {coverage}")

        # Test historical retrieval
        hist = db.get_historical_prices(test_symbol, days=30)
        print(f"Historical data retrieved: {len(hist)} rows")

        # List all symbols
        symbols = db.get_all_symbols()
        print(f"Symbols in database: {symbols}")

    print("\n✅ MarketHistoryDB test completed!")
