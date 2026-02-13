#!/usr/bin/env python3
"""
Momentum Strategy for factor-lab

Based on Fama-French Momentum Factor:
- Buy stocks with strong 12-month price momentum (skip recent 1 month)
- Rebalance monthly/quarterly

Academic Evidence:
- Jegadeesh & Titman (1993): Momentum premium ~8-10% annually
- Asness et al. (2013): Momentum works across 40+ countries
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.base import Strategy


class MomentumStrategy(Strategy):
    """
    12-Month Momentum Strategy (skip recent 1 month)

    Selection Logic:
    1. Calculate 12-month return for each stock (skip recent 1 month to avoid reversal)
    2. Rank stocks by return (descending)
    3. Select top N stocks

    Parameters:
    - lookback_days: 252 (≈12 months trading days)
    - skip_days: 21 (≈1 month trading days)
    - top_n: Number of stocks to select
    """

    def __init__(self, lookback_days: int = 252, skip_days: int = 21):
        """
        Initialize Momentum Strategy

        Args:
            lookback_days: Number of trading days to look back (default: 252 ≈ 12 months)
            skip_days: Number of recent days to skip (default: 21 ≈ 1 month)
        """
        super().__init__(
            name="Momentum",
            description=f"{lookback_days}D momentum (skip recent {skip_days}D)"
        )
        self.lookback_days = lookback_days
        self.skip_days = skip_days

    def select_stocks(
        self,
        universe: List[str],
        date: str,
        data_manager,
        top_n: int = 50
    ) -> List[str]:
        """
        Select stocks with highest momentum

        Args:
            universe: List of ticker symbols
            date: Rebalance date (YYYY-MM-DD)
            data_manager: QuantDataManager instance
            top_n: Number of stocks to select

        Returns:
            List of top N tickers by momentum
        """
        momentum_scores = []

        # Calculate momentum for each stock
        for ticker in universe:
            try:
                momentum = self._calculate_momentum(ticker, date, data_manager)

                if momentum is not None:
                    momentum_scores.append({
                        'ticker': ticker,
                        'momentum': momentum
                    })

            except Exception as e:
                # Skip stocks with data errors
                print(f"  Warning: Error calculating momentum for {ticker}: {e}")
                continue

        # Sort by momentum (descending)
        momentum_scores.sort(key=lambda x: x['momentum'], reverse=True)

        # Select top N
        selected = [s['ticker'] for s in momentum_scores[:top_n]]

        return selected

    def _calculate_momentum(
        self,
        ticker: str,
        date: str,
        data_manager
    ) -> float:
        """
        Calculate momentum for a single stock

        Args:
            ticker: Stock ticker
            date: Rebalance date
            data_manager: Data manager instance

        Returns:
            12-month return (%) or None if insufficient data
        """
        # Parse date
        rebalance_date = datetime.strptime(date, '%Y-%m-%d')

        # Get historical data (need extra buffer for weekends/holidays)
        # 252 trading days + 21 skip + 100 buffer ≈ 500 calendar days
        start_date = (rebalance_date - timedelta(days=500)).strftime('%Y-%m-%d')
        end_date = date  # Up to (but not including) rebalance date

        hist = data_manager.get_historical_data(ticker, start_date, end_date)

        if hist is None or len(hist) < self.lookback_days + self.skip_days:
            return None

        # Point-in-time check: Only use data BEFORE rebalance date
        # Convert rebalance_date to pd.Timestamp to handle timezone-aware comparisons
        import pandas as pd
        rebalance_ts = pd.Timestamp(rebalance_date)

        # If hist.index is timezone-aware, localize rebalance_ts
        if hist.index.tz is not None:
            rebalance_ts = rebalance_ts.tz_localize(hist.index.tz)

        hist = hist[hist.index < rebalance_ts]

        if len(hist) < self.lookback_days + self.skip_days:
            return None

        # Calculate momentum
        # Skip recent skip_days, then look back lookback_days
        try:
            price_1m_ago = hist['Close'].iloc[-(self.skip_days + 1)]
            price_12m_ago = hist['Close'].iloc[-(self.lookback_days + self.skip_days + 1)]

            momentum_return = ((price_1m_ago - price_12m_ago) / price_12m_ago) * 100

            return momentum_return

        except (IndexError, KeyError):
            return None


def main():
    """Test Momentum Strategy"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from quant.data_manager import QuantDataManager

    print("=" * 60)
    print("TEST: Momentum Strategy")
    print("=" * 60)

    data_mgr = QuantDataManager()
    strategy = MomentumStrategy(lookback_days=252, skip_days=21)

    # Test with small universe
    test_universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD', 'NFLX', 'INTC']
    test_date = "2024-01-31"  # End of January 2024

    print(f"\nStrategy: {strategy}")
    print(f"Universe: {len(test_universe)} stocks")
    print(f"Rebalance Date: {test_date}")
    print(f"Top N: 5")

    selected = strategy.select_stocks(
        universe=test_universe,
        date=test_date,
        data_manager=data_mgr,
        top_n=5
    )

    print(f"\nSelected Stocks ({len(selected)}):")
    for i, ticker in enumerate(selected, 1):
        print(f"  {i}. {ticker}")

    # Test portfolio weights
    weights = strategy.get_portfolio_weights(selected)
    print(f"\nPortfolio Weights:")
    for ticker, weight in weights.items():
        print(f"  {ticker}: {weight*100:.1f}%")

    print(f"\n{'=' * 60}\n")


if __name__ == '__main__':
    main()
