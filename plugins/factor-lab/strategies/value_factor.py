#!/usr/bin/env python3
"""
Value Factor Strategy for factor-lab

Based on Fama-French Value Factor:
- Buy stocks with low P/E and P/B ratios (sector-relative)
- Classical value investing approach with quantitative screening

Academic Evidence:
- Fama & French (1992): Value premium ~4-5% annually
- Asness et al. (2013): Value factor works globally
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.base import Strategy
from quant.factor_calculator import FactorCalculator
from typing import List


class ValueFactorStrategy(Strategy):
    """
    Value Factor Strategy (Low P/E, Low P/B)

    Selection Logic:
    1. Calculate value score for each stock (P/E, P/B vs sector)
    2. Rank stocks by value score (descending)
    3. Select top N stocks

    Higher value score = More undervalued
    """

    def __init__(self):
        """Initialize Value Factor Strategy"""
        super().__init__(
            name="Value Factor",
            description="Low P/E, Low P/B (sector-relative)"
        )
        self.factor_calc = FactorCalculator()

    def select_stocks(
        self,
        universe: List[str],
        date: str,
        data_manager,
        top_n: int = 50
    ) -> List[str]:
        """
        Select stocks with highest value scores

        Args:
            universe: List of ticker symbols
            date: Rebalance date (YYYY-MM-DD)
            data_manager: QuantDataManager instance
            top_n: Number of stocks to select

        Returns:
            List of top N tickers by value score
        """
        value_scores = []

        # Calculate value score for each stock
        for ticker in universe:
            try:
                # Get stock info (fundamentals)
                stock_info = data_manager.get_stock_info(ticker)

                if stock_info is None:
                    continue

                sector = stock_info.get('sector', 'Unknown')

                # Calculate value score
                value_score = self.factor_calc.calculate_value_score(
                    ticker,
                    stock_info,
                    sector
                )

                if value_score is not None:
                    value_scores.append({
                        'ticker': ticker,
                        'value_score': value_score,
                        'pe_ratio': stock_info.get('pe_ratio'),
                        'pb_ratio': stock_info.get('pb_ratio')
                    })

            except Exception as e:
                # Skip stocks with data errors
                print(f"  Warning: Error calculating value for {ticker}: {e}")
                continue

        # Sort by value score (descending)
        value_scores.sort(key=lambda x: x['value_score'], reverse=True)

        # Select top N
        selected = [s['ticker'] for s in value_scores[:top_n]]

        return selected


def main():
    """Test Value Factor Strategy"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from quant.data_manager import QuantDataManager

    print("=" * 60)
    print("TEST: Value Factor Strategy")
    print("=" * 60)

    data_mgr = QuantDataManager()
    strategy = ValueFactorStrategy()

    # Test with small universe
    test_universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD', 'NFLX', 'INTC']
    test_date = "2024-01-31"

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
