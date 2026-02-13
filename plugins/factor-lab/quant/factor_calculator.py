#!/usr/bin/env python3
"""
Factor Calculator for factor-lab

Calculates 5-factor scores based on Fama-French 5-Factor Model:
1. Value Factor (P/E, P/B, EV/EBITDA)
2. Quality Factor (ROE, Debt, Margins)
3. Momentum Factor (12M returns)
4. Low Volatility Factor (Beta, Std Dev)
5. Size Factor (Market Cap)
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Optional
import pandas as pd
import numpy as np
import yaml

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import QuantDataManager

# Load factor definitions
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'factor_definitions.yaml')
with open(CONFIG_PATH, 'r') as f:
    FACTOR_CONFIG = yaml.safe_load(f)

SECTOR_BENCHMARKS = FACTOR_CONFIG['sector_benchmarks']


class FactorCalculator:
    """
    5-Factor Score Calculator (0-100 scale)

    Based on Fama-French 5-Factor Model
    """

    def __init__(self):
        self.data_manager = QuantDataManager()

    def calculate_value_score(self, ticker: str, stock_info: Dict, sector: str) -> float:
        """
        Value Factor (0-100)

        Metrics:
        - P/E ratio vs sector (40%)
        - P/B ratio vs sector (40%)
        - EV/EBITDA vs sector (20%)

        Lower valuation = Higher score
        """
        try:
            pe_ratio = stock_info.get('pe_ratio') or 0
            pb_ratio = stock_info.get('pb_ratio') or 0

            # Get sector benchmarks
            sector_pe = SECTOR_BENCHMARKS.get(sector, {}).get('pe_ratio', 20.0)
            sector_pb = SECTOR_BENCHMARKS.get(sector, {}).get('pb_ratio', 3.0)

            # Calculate discount/premium vs sector
            pe_score = 0
            if pe_ratio > 0:
                pe_discount = ((sector_pe - pe_ratio) / sector_pe) * 100
                # Normalize: 30% discount = 100, 0% = 50, 30% premium = 0
                pe_score = self._normalize(
                    pe_discount,
                    excellent=30,
                    good=10,
                    acceptable=-10,
                    poor=-30
                )
            else:
                pe_score = 50  # Neutral if P/E not available

            pb_score = 0
            if pb_ratio > 0:
                pb_discount = ((sector_pb - pb_ratio) / sector_pb) * 100
                pb_score = self._normalize(
                    pb_discount,
                    excellent=30,
                    good=10,
                    acceptable=-10,
                    poor=-30
                )
            else:
                pb_score = 50

            # Weighted average (P/E 40%, P/B 40%, EV/EBITDA 20% - skip EV for MVP)
            value_score = (pe_score * 0.5 + pb_score * 0.5)

            return max(0, min(100, value_score))

        except Exception as e:
            print(f"Error calculating value score for {ticker}: {e}")
            return 50  # Neutral on error

    def calculate_quality_score(self, ticker: str, stock_info: Dict) -> float:
        """
        Quality Factor (0-100)

        Metrics:
        - ROE > 15% (40%)
        - Debt/Equity < 0.5 (30%)
        - Operating Margin (20%)
        - Earnings Stability (10% - skip for MVP)

        Higher quality = Higher score
        """
        try:
            roe = stock_info.get('roe') or 0
            debt_to_equity = stock_info.get('debt_to_equity') or 0
            operating_margin = stock_info.get('operating_margin') or 0

            # ROE score (40%)
            roe_pct = roe * 100 if roe else 0
            roe_score = self._normalize(
                roe_pct,
                excellent=20,
                good=15,
                acceptable=10,
                poor=5
            )

            # Debt score (30%) - lower is better
            if debt_to_equity >= 0:
                # Invert: low debt = high score
                debt_score = self._normalize(
                    100 / (1 + debt_to_equity),
                    excellent=80,
                    good=60,
                    acceptable=40,
                    poor=20
                )
            else:
                debt_score = 50  # Neutral if negative (unusual)

            # Operating margin score (20%)
            margin_pct = operating_margin * 100 if operating_margin else 0
            margin_score = self._normalize(
                margin_pct,
                excellent=20,
                good=15,
                acceptable=10,
                poor=5
            )

            # Weighted average
            quality_score = (
                roe_score * 0.40 +
                debt_score * 0.30 +
                margin_score * 0.30  # Adjust weight since we skip earnings stability
            )

            return max(0, min(100, quality_score))

        except Exception as e:
            print(f"Error calculating quality score for {ticker}: {e}")
            return 50

    def calculate_momentum_score(self, ticker: str, period: int = 252) -> float:
        """
        Momentum Factor (0-100)

        Metrics:
        - 12-month return (skip recent 1 month) (60%)
        - 6-month return (30%)
        - Relative strength vs sector (10% - skip for MVP)

        Higher momentum = Higher score
        """
        try:
            # Get historical data
            # Need ~450 calendar days to ensure 252 trading days (account for weekends/holidays)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=450)).strftime('%Y-%m-%d')

            hist = self.data_manager.get_historical_data(ticker, start_date, end_date)

            if hist is None or len(hist) < period:
                return 50  # Neutral if insufficient data

            # 12-month return (skip recent 1 month)
            # period=252 trading days ≈ 12 months, skip_days=21 ≈ 1 month
            if len(hist) >= 252:
                price_12m_ago = hist['Close'].iloc[-252]
                price_1m_ago = hist['Close'].iloc[-21] if len(hist) >= 21 else hist['Close'].iloc[-1]

                return_12m = ((price_1m_ago - price_12m_ago) / price_12m_ago) * 100
            else:
                return 50

            # 6-month return
            if len(hist) >= 126:
                price_6m_ago = hist['Close'].iloc[-126]
                price_current = hist['Close'].iloc[-1]
                return_6m = ((price_current - price_6m_ago) / price_6m_ago) * 100
            else:
                return_6m = 0

            # Normalize returns to 0-100 scale
            # Typical annual return: 10-20% = good, 30%+ = excellent
            mom_12m_score = self._normalize(
                return_12m,
                excellent=30,
                good=15,
                acceptable=5,
                poor=-10
            )

            mom_6m_score = self._normalize(
                return_6m,
                excellent=15,
                good=8,
                acceptable=3,
                poor=-5
            )

            # Weighted average
            momentum_score = (
                mom_12m_score * 0.70 +
                mom_6m_score * 0.30
            )

            return max(0, min(100, momentum_score))

        except Exception as e:
            print(f"Error calculating momentum score for {ticker}: {e}")
            return 50

    def calculate_low_vol_score(self, ticker: str, stock_info: Dict) -> float:
        """
        Low Volatility Factor (0-100)

        Metrics:
        - Beta < 0.8 (50%)
        - 60-day volatility (40%)
        - Max Drawdown (10% - skip for MVP)

        Lower volatility = Higher score
        """
        try:
            beta = stock_info.get('beta') or 1.0

            # Beta score (50%) - lower is better
            # Beta < 0.8 = excellent, 0.8-1.0 = good, 1.0-1.2 = acceptable, > 1.2 = poor
            beta_score = self._normalize(
                1.5 - beta,  # Invert: low beta = high score
                excellent=0.7,
                good=0.5,
                acceptable=0.3,
                poor=0
            )

            # 60-day volatility (40%)
            try:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

                hist = self.data_manager.get_historical_data(ticker, start_date, end_date)

                if hist is not None and len(hist) >= 60:
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.tail(60).std() * np.sqrt(252) * 100  # Annualized %

                    # Lower volatility = higher score
                    # 15% vol = excellent, 20% = good, 25% = acceptable, 30%+ = poor
                    vol_score = self._normalize(
                        50 - volatility,  # Invert
                        excellent=35,
                        good=30,
                        acceptable=25,
                        poor=20
                    )
                else:
                    vol_score = 50
            except:
                vol_score = 50

            # Weighted average
            low_vol_score = (
                beta_score * 0.50 +
                vol_score * 0.50
            )

            return max(0, min(100, low_vol_score))

        except Exception as e:
            print(f"Error calculating low vol score for {ticker}: {e}")
            return 50

    def calculate_size_score(self, ticker: str, stock_info: Dict) -> float:
        """
        Size Factor (0-100)

        Metrics:
        - Market Cap (smaller = higher score)

        Typical scoring:
        - < $2B (Small Cap): 100
        - $2B-$10B (Mid Cap): 70
        - $10B-$50B (Large Cap): 40
        - > $50B (Mega Cap): 20
        """
        try:
            market_cap = stock_info.get('market_cap') or 0

            if market_cap == 0:
                return 50

            # Convert to billions
            market_cap_b = market_cap / 1_000_000_000

            if market_cap_b < 2:
                return 100
            elif market_cap_b < 10:
                return 70
            elif market_cap_b < 50:
                return 40
            else:
                return 20

        except Exception as e:
            print(f"Error calculating size score for {ticker}: {e}")
            return 50

    def calculate_composite_score(
        self,
        ticker: str,
        weights: Dict[str, float]
    ) -> Dict:
        """
        Calculate composite score (weighted average of factors)

        Args:
            ticker: Stock ticker
            weights: Factor weights dict
                     e.g. {'value': 0.3, 'quality': 0.4, 'momentum': 0.3}

        Returns:
            Dict with all scores and metadata
        """
        try:
            # Get stock info
            stock_info = self.data_manager.get_stock_info(ticker)

            if not stock_info:
                return None

            sector = stock_info.get('sector', 'Unknown')

            # Calculate individual factor scores
            value_score = self.calculate_value_score(ticker, stock_info, sector)
            quality_score = self.calculate_quality_score(ticker, stock_info)
            momentum_score = self.calculate_momentum_score(ticker)
            low_vol_score = self.calculate_low_vol_score(ticker, stock_info)
            size_score = self.calculate_size_score(ticker, stock_info)

            # Calculate composite score
            composite = (
                value_score * weights.get('value', 0) +
                quality_score * weights.get('quality', 0) +
                momentum_score * weights.get('momentum', 0) +
                low_vol_score * weights.get('low_volatility', 0) +
                size_score * weights.get('size', 0)
            )

            # Get grade
            grade = self._get_grade(composite)

            return {
                'ticker': ticker,
                'name': stock_info.get('name', ticker),
                'sector': sector,
                'price': stock_info.get('price'),
                'market_cap': stock_info.get('market_cap'),
                'composite_score': round(composite, 2),
                'value_score': round(value_score, 2),
                'quality_score': round(quality_score, 2),
                'momentum_score': round(momentum_score, 2),
                'low_vol_score': round(low_vol_score, 2),
                'size_score': round(size_score, 2),
                'grade': grade,
                'pe_ratio': stock_info.get('pe_ratio'),
                'pb_ratio': stock_info.get('pb_ratio'),
                'roe': stock_info.get('roe'),
                'debt_to_equity': stock_info.get('debt_to_equity'),
                'beta': stock_info.get('beta')
            }

        except Exception as e:
            print(f"Error calculating composite score for {ticker}: {e}")
            return None

    def _normalize(
        self,
        value: float,
        excellent: float,
        good: float,
        acceptable: float,
        poor: float
    ) -> float:
        """
        Normalize a value to 0-100 scale

        Args:
            value: Input value
            excellent: Value for 100 points
            good: Value for 75 points
            acceptable: Value for 50 points
            poor: Value for 25 points
        """
        if value >= excellent:
            return 100.0
        elif value >= good:
            # Linear interpolation between good and excellent
            ratio = (value - good) / (excellent - good)
            return 75.0 + (ratio * 25.0)
        elif value >= acceptable:
            ratio = (value - acceptable) / (good - acceptable)
            return 50.0 + (ratio * 25.0)
        elif value >= poor:
            ratio = (value - poor) / (acceptable - poor)
            return 25.0 + (ratio * 25.0)
        else:
            # Below poor: scale down to 0
            # For values worse than "poor", linearly scale from 25 to 0
            # Distance below poor threshold determines how much to reduce
            if poor != 0:
                # Calculate how far below poor we are (as a ratio)
                # If value is 2x worse than poor, score approaches 0
                distance_ratio = max(0, min(1, 1 - abs((value - poor) / poor)))
                return 25.0 * distance_ratio
            else:
                return 0

    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90:
            return 'A+ (Exceptional)'
        elif score >= 80:
            return 'A  (Excellent)'
        elif score >= 70:
            return 'B+ (Good)'
        elif score >= 60:
            return 'B  (Fair)'
        elif score >= 50:
            return 'C  (Weak)'
        else:
            return 'D  (Poor)'


def main():
    """Test factor calculator"""
    calculator = FactorCalculator()

    # Test with AAPL
    print("\n" + "="*60)
    print("TEST: Calculate Factor Scores for AAPL")
    print("="*60)

    weights = {
        'value': 0.3,
        'quality': 0.4,
        'momentum': 0.3,
        'low_volatility': 0.0,
        'size': 0.0
    }

    result = calculator.calculate_composite_score('AAPL', weights)

    if result:
        print(f"\n{result['name']} ({result['ticker']})")
        print(f"Sector: {result['sector']}")
        print(f"Price: ${result['price']:.2f}" if result['price'] else "Price: N/A")
        print(f"\n{'='*60}")
        print(f"Composite Score: {result['composite_score']:.1f} / 100  {result['grade']}")
        print(f"{'='*60}\n")

        print("Factor Breakdown:")
        print(f"  Value:       {result['value_score']:.1f} / 100")
        print(f"  Quality:     {result['quality_score']:.1f} / 100")
        print(f"  Momentum:    {result['momentum_score']:.1f} / 100")
        print(f"  Low Vol:     {result['low_vol_score']:.1f} / 100")
        print(f"  Size:        {result['size_score']:.1f} / 100")

        print(f"\nFundamentals:")
        print(f"  P/E:         {result['pe_ratio']:.2f}" if result['pe_ratio'] else "  P/E:         N/A")
        print(f"  P/B:         {result['pb_ratio']:.2f}" if result['pb_ratio'] else "  P/B:         N/A")
        print(f"  ROE:         {result['roe']*100:.2f}%" if result['roe'] else "  ROE:         N/A")
        print(f"  Debt/Equity: {result['debt_to_equity']:.2f}" if result['debt_to_equity'] else "  Debt/Equity: N/A")
        print(f"  Beta:        {result['beta']:.2f}" if result['beta'] else "  Beta:        N/A")


if __name__ == '__main__':
    main()
