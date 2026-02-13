#!/usr/bin/env python3
"""
Quality Factor Strategy for factor-lab

Based on Fama-French Quality Factor:
- Buy stocks with high ROE, low debt, high margins
- Focus on sustainable profitability and financial strength

Academic Evidence:
- Fama & French (2015): Quality factor (profitability) premium ~3-4% annually
- Novy-Marx (2013): Gross profitability predicts cross-sectional returns
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.base import Strategy
from quant.factor_calculator import FactorCalculator
from typing import List


class QualityStrategy(Strategy):
    """
    Quality Factor Strategy (High ROE, Low Debt, High Margins)

    Selection Logic:
    1. Calculate quality score for each stock (ROE, Debt/Equity, Margins)
    2. Rank stocks by quality score (descending)
    3. Select top N stocks

    Higher quality score = Better fundamentals
    """

    def __init__(self):
        """Initialize Quality Factor Strategy"""
        super().__init__(
            name="Quality Factor",
            description="High ROE, Low Debt, High Margins"
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
        Select stocks with highest quality scores

        Args:
            universe: List of ticker symbols
            date: Rebalance date (YYYY-MM-DD)
            data_manager: QuantDataManager instance
            top_n: Number of stocks to select

        Returns:
            List of top N tickers by quality score
        """
        quality_scores = []

        # Calculate quality score for each stock
        for ticker in universe:
            try:
                # Get stock info (fundamentals)
                stock_info = data_manager.get_stock_info(ticker)

                if stock_info is None:
                    continue

                # Calculate quality score
                quality_score = self.factor_calc.calculate_quality_score(
                    ticker,
                    stock_info
                )

                if quality_score is not None:
                    quality_scores.append({
                        'ticker': ticker,
                        'quality_score': quality_score,
                        'roe': stock_info.get('roe'),
                        'debt_to_equity': stock_info.get('debt_to_equity'),
                        'operating_margin': stock_info.get('operating_margin')
                    })

            except Exception as e:
                # Skip stocks with data errors
                print(f"  Warning: Error calculating quality for {ticker}: {e}")
                continue

        # Sort by quality score (descending)
        quality_scores.sort(key=lambda x: x['quality_score'], reverse=True)

        # Select top N
        selected = [s['ticker'] for s in quality_scores[:top_n]]

        return selected


def main():
    """Test Quality Factor Strategy"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from quant.data_manager import QuantDataManager

    print("=" * 60)
    print("TEST: Quality Factor Strategy")
    print("=" * 60)

    data_mgr = QuantDataManager()
    strategy = QualityStrategy()

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
