#!/usr/bin/env python3
"""
Company Scorecard Generator

Evaluates stocks across three dimensions:
1. Financial Health (0-10): Profitability, Growth, Stability
2. Valuation (0-10): P/E, P/B vs sector and historical averages
3. Momentum (0-10): Moving averages, RSI, MACD

Total Score = Financial*0.4 + Valuation*0.3 + Momentum*0.3
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataSourceManager


class CompanyScorecardGenerator:
    """Generate comprehensive company scorecards"""

    def __init__(self):
        self.data_manager = DataSourceManager()

    def calculate_scorecard(self, ticker: str) -> Dict:
        """
        Calculate comprehensive scorecard for a stock

        Returns:
            {
                'ticker': str,
                'company_name': str,
                'price': float,
                'financial_score': float (0-10),
                'valuation_score': float (0-10),
                'momentum_score': float (0-10),
                'total_score': float (0-10),
                'details': {...}
            }
        """
        print(f"\n{'='*60}")
        print(f"Generating Scorecard for {ticker}")
        print(f"{'='*60}\n")

        # Fetch data
        stock_info = self.data_manager.get_stock_info(ticker)
        if not stock_info:
            return {'error': f'Failed to fetch data for {ticker}'}

        financials = self.data_manager.get_financials(ticker)
        historical_data = self.data_manager.get_historical_prices(ticker, period='1y')  # 1 year
        historical = historical_data if historical_data is not None else None

        # Calculate scores
        financial_score, financial_details = self._calculate_financial_score(
            stock_info, financials
        )

        valuation_score, valuation_details = self._calculate_valuation_score(
            stock_info, financials
        )

        momentum_score, momentum_details = self._calculate_momentum_score(
            ticker, historical
        )

        # Calculate total weighted score (Sprint 4 fix: cap all scores at 10)
        financial_score = min(max(financial_score, 0), 10)
        valuation_score = min(max(valuation_score, 0), 10)
        momentum_score = min(max(momentum_score, 0), 10)

        total_score = (
            financial_score * 0.40 +
            valuation_score * 0.30 +
            momentum_score * 0.30
        )
        total_score = min(max(total_score, 0), 10)

        return {
            'ticker': ticker,
            'company_name': stock_info.get('name', ticker),
            'price': stock_info.get('price'),
            'sector': stock_info.get('sector'),
            'market_cap': stock_info.get('market_cap'),
            'financial_score': round(financial_score, 2),
            'valuation_score': round(valuation_score, 2),
            'momentum_score': round(momentum_score, 2),
            'total_score': round(total_score, 2),
            'grade': self._get_grade(total_score),
            'details': {
                'financial': financial_details,
                'valuation': valuation_details,
                'momentum': momentum_details
            }
        }

    def _calculate_financial_score(
        self,
        stock_info: Dict,
        financials: Dict
    ) -> Tuple[float, Dict]:
        """
        Calculate Financial Health Score (0-10)

        Components:
        - Profitability (40%): ROE, Operating Margin, Net Margin
        - Growth (30%): Revenue YoY, Operating Income YoY
        - Stability (30%): Debt-to-Equity, Current Ratio
        """
        details = {}

        # Extract metrics
        roe = stock_info.get('roe', 0) or 0
        operating_margin = stock_info.get('operating_margin', 0) or 0
        net_margin = stock_info.get('net_margin', 0) or 0
        debt_to_equity = stock_info.get('debt_to_equity', 0) or 0
        current_ratio = stock_info.get('current_ratio', 1) or 1

        # Calculate revenue growth from financials if available
        revenue_growth = 0
        operating_income_growth = 0

        if financials and 'income_stmt' in financials:
            try:
                income = financials['income_stmt']
                if isinstance(income, pd.DataFrame) and len(income.columns) >= 2:
                    # Get most recent two periods
                    recent = income.iloc[:, 0]
                    previous = income.iloc[:, 1]

                    if 'Total Revenue' in income.index:
                        rev_recent = recent['Total Revenue']
                        rev_prev = previous['Total Revenue']
                        if rev_prev != 0:
                            revenue_growth = ((rev_recent - rev_prev) / abs(rev_prev)) * 100

                    if 'Operating Income' in income.index:
                        op_recent = recent['Operating Income']
                        op_prev = previous['Operating Income']
                        if op_prev != 0:
                            operating_income_growth = ((op_recent - op_prev) / abs(op_prev)) * 100
            except Exception as e:
                print(f"Warning: Could not calculate growth rates: {e}")

        # 1. Profitability Score (0-10)
        roe_score = self._normalize(roe * 100, excellent=20, good=15, acceptable=10, poor=5)
        margin_score = self._normalize(
            (operating_margin + net_margin) * 50,  # Average of margins
            excellent=20, good=15, acceptable=10, poor=5
        )
        profitability_score = (roe_score + margin_score) / 2

        # 2. Growth Score (0-10)
        growth_score = self._normalize(
            revenue_growth * 0.6 + operating_income_growth * 0.4,
            excellent=20, good=10, acceptable=5, poor=0
        )

        # 3. Stability Score (0-10)
        # Lower debt is better
        debt_score = self._normalize(
            100 / (1 + debt_to_equity) if debt_to_equity >= 0 else 0,
            excellent=80, good=60, acceptable=40, poor=20
        )
        liquidity_score = self._normalize(
            current_ratio * 50,
            excellent=100, good=75, acceptable=50, poor=25
        )
        stability_score = (debt_score + liquidity_score) / 2

        # Weighted average
        financial_score = (
            profitability_score * 0.40 +
            growth_score * 0.30 +
            stability_score * 0.30
        )

        details = {
            'profitability_score': round(profitability_score, 2),
            'growth_score': round(growth_score, 2),
            'stability_score': round(stability_score, 2),
            'roe': round(roe * 100, 2) if roe else 0,
            'operating_margin': round(operating_margin * 100, 2) if operating_margin else 0,
            'net_margin': round(net_margin * 100, 2) if net_margin else 0,
            'revenue_growth': round(revenue_growth, 2),
            'operating_income_growth': round(operating_income_growth, 2),
            'debt_to_equity': round(debt_to_equity, 2),
            'current_ratio': round(current_ratio, 2)
        }

        return financial_score, details

    def _calculate_valuation_score(
        self,
        stock_info: Dict,
        financials: Dict
    ) -> Tuple[float, Dict]:
        """
        Calculate Valuation Score (0-10)

        Lower valuation = Higher score (undervalued is better)

        Components:
        - Sector Relative (60%): P/E, P/B vs sector average
        - Historical (40%): P/E, P/B vs 3-year average
        """
        details = {}

        pe_ratio = stock_info.get('pe_ratio', 0) or 0
        pb_ratio = stock_info.get('pb_ratio', 0) or 0

        # For MVP, we'll use general market benchmarks
        # In Phase 2, we'll calculate actual sector averages

        # Typical sector P/E ranges (simplified)
        sector = stock_info.get('sector', 'Unknown')
        sector_pe_benchmarks = {
            'Technology': 30,
            'Healthcare': 25,
            'Financial Services': 15,
            'Consumer Cyclical': 20,
            'Consumer Defensive': 22,
            'Energy': 15,
            'Industrials': 20,
            'Communication Services': 18,
            'Utilities': 18,
            'Real Estate': 20,
            'Basic Materials': 15
        }

        sector_pb_benchmarks = {
            'Technology': 7,
            'Healthcare': 5,
            'Financial Services': 1.5,
            'Consumer Cyclical': 4,
            'Consumer Defensive': 5,
            'Energy': 2,
            'Industrials': 3,
            'Communication Services': 3,
            'Utilities': 2,
            'Real Estate': 2,
            'Basic Materials': 2
        }

        sector_pe = sector_pe_benchmarks.get(sector, 20)
        sector_pb = sector_pb_benchmarks.get(sector, 3)

        # Calculate valuation scores
        # Lower P/E = Higher score
        if pe_ratio > 0:
            pe_discount = ((sector_pe - pe_ratio) / sector_pe) * 100
            pe_score = self._normalize(
                pe_discount,
                excellent=30,  # 30% discount = excellent
                good=10,       # 10% discount = good
                acceptable=-10, # 10% premium = acceptable
                poor=-30        # 30% premium = poor
            )
        else:
            pe_score = 5  # Neutral if P/E not available

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
            pb_score = 5

        # Sector relative score (60%)
        sector_relative_score = (pe_score + pb_score) / 2

        # Historical comparison (40%)
        # For MVP, use simple heuristics
        # In Phase 2, calculate actual 3-year averages
        historical_score = 5  # Neutral for now

        valuation_score = (
            sector_relative_score * 0.60 +
            historical_score * 0.40
        )

        details = {
            'sector_relative_score': round(sector_relative_score, 2),
            'historical_score': round(historical_score, 2),
            'pe_ratio': round(pe_ratio, 2) if pe_ratio else 0,
            'sector_pe': sector_pe,
            'pe_discount_pct': round(pe_discount, 2) if pe_ratio > 0 else 0,
            'pb_ratio': round(pb_ratio, 2) if pb_ratio else 0,
            'sector_pb': sector_pb,
            'pb_discount_pct': round(pb_discount, 2) if pb_ratio > 0 else 0
        }

        return valuation_score, details

    def _calculate_momentum_score(
        self,
        ticker: str,
        historical: pd.DataFrame
    ) -> Tuple[float, Dict]:
        """
        Calculate Momentum Score (0-10)

        Components:
        - Moving Average Alignment (40%): Price > MA20 > MA60 > MA120
        - RSI (30%): Ideal range 40-60
        - MACD (20%): MACD > Signal line
        - Volume Trend (10%): Increasing volume on up days
        """
        details = {}

        if historical is None or len(historical) < 20:
            return 5.0, {'error': 'Insufficient historical data'}

        # Calculate moving averages
        prices = historical['Close']

        ma20 = prices.rolling(window=20).mean().iloc[-1] if len(prices) >= 20 else None
        ma60 = prices.rolling(window=60).mean().iloc[-1] if len(prices) >= 60 else None
        ma120 = prices.rolling(window=120).mean().iloc[-1] if len(prices) >= 120 else None

        current_price = prices.iloc[-1]

        # 1. Moving Average Alignment (0-10)
        ma_score = 0
        if ma20:
            if current_price > ma20:
                ma_score += 2.5
            if ma60 and ma20 > ma60:
                ma_score += 2.5
            if ma120 and ma60 and ma60 > ma120:
                ma_score += 2.5
            if ma120 and current_price > ma120:
                ma_score += 2.5
        else:
            ma_score = 5  # Neutral if not enough data

        # 2. RSI (0-10)
        rsi = self._calculate_rsi(prices)
        if rsi:
            # Ideal range: 40-60 (sustainable)
            if 40 <= rsi <= 60:
                rsi_score = 10
            elif 30 <= rsi < 40 or 60 < rsi <= 70:
                rsi_score = 7
            elif rsi < 30 or rsi > 70:
                rsi_score = 4  # Overbought or oversold
            else:
                rsi_score = 5
        else:
            rsi_score = 5

        # 3. MACD (0-10)
        macd, signal = self._calculate_macd(prices)
        if macd is not None and signal is not None:
            if macd > signal:
                macd_score = 8  # Bullish
            elif macd > signal * 0.95:  # Close
                macd_score = 6
            else:
                macd_score = 4  # Bearish
        else:
            macd_score = 5

        # 4. Volume Trend (0-10)
        volume_score = 5  # Neutral for MVP
        if 'Volume' in historical.columns:
            recent_volume = historical['Volume'].iloc[-10:].mean()
            prev_volume = historical['Volume'].iloc[-30:-10].mean()
            if prev_volume > 0:
                volume_change = (recent_volume - prev_volume) / prev_volume
                if volume_change > 0.2:
                    volume_score = 8
                elif volume_change > 0:
                    volume_score = 6
                else:
                    volume_score = 4

        # Weighted average
        momentum_score = (
            ma_score * 0.40 +
            rsi_score * 0.30 +
            macd_score * 0.20 +
            volume_score * 0.10
        )

        details = {
            'ma_score': round(ma_score, 2),
            'rsi_score': round(rsi_score, 2),
            'macd_score': round(macd_score, 2),
            'volume_score': round(volume_score, 2),
            'current_price': round(current_price, 2),
            'ma20': round(ma20, 2) if ma20 else None,
            'ma60': round(ma60, 2) if ma60 else None,
            'ma120': round(ma120, 2) if ma120 else None,
            'rsi': round(rsi, 2) if rsi else None,
            'macd': round(macd, 2) if macd else None,
            'signal': round(signal, 2) if signal else None
        }

        return momentum_score, details

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None

        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None

    def _calculate_macd(
        self,
        prices: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[Optional[float], Optional[float]]:
        """Calculate MACD and Signal line"""
        if len(prices) < slow + signal:
            return None, None

        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()

        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal).mean()

        return macd.iloc[-1], signal_line.iloc[-1]

    def _normalize(
        self,
        value: float,
        excellent: float,
        good: float,
        acceptable: float,
        poor: float
    ) -> float:
        """
        Normalize a value to 0-10 scale (Sprint 4 fix: cap at 10)

        Args:
            value: Input value to normalize
            excellent: Value for 10 points
            good: Value for 7.5 points
            acceptable: Value for 5 points
            poor: Value for 2.5 points
        """
        if value >= excellent:
            return 10.0
        elif value >= good:
            # Linear interpolation between good and excellent
            ratio = (value - good) / (excellent - good)
            return 7.5 + (ratio * 2.5)
        elif value >= acceptable:
            ratio = (value - acceptable) / (good - acceptable)
            return 5.0 + (ratio * 2.5)
        elif value >= poor:
            ratio = (value - poor) / (acceptable - poor)
            return 2.5 + (ratio * 2.5)
        else:
            # Below poor: scale down to 0 (capped at 10)
            score = 2.5 * (value / poor) if poor != 0 else 0
            return min(max(0, score), 10.0)

    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 9.0:
            return 'A+  (Exceptional)'
        elif score >= 8.0:
            return 'A   (Excellent)'
        elif score >= 7.0:
            return 'B+  (Good)'
        elif score >= 6.0:
            return 'B   (Fair)'
        elif score >= 5.0:
            return 'C   (Weak)'
        else:
            return 'D   (Poor)'

    def print_scorecard(self, scorecard: Dict):
        """Print formatted scorecard to terminal"""
        if 'error' in scorecard:
            print(f"❌ Error: {scorecard['error']}")
            return

        print(f"\n{'='*60}")
        print(f"📊 {scorecard['company_name']} ({scorecard['ticker']}) Stock Analysis")
        print(f"{'='*60}\n")

        print(f"📈 Current Price: ${scorecard['price']:.2f}")
        print(f"🏢 Sector: {scorecard['sector']}")
        if scorecard['market_cap']:
            print(f"💰 Market Cap: ${scorecard['market_cap']:,.0f}")

        print(f"\n🏆 Overall Score: {scorecard['total_score']:.1f} / 10  {scorecard['grade']}\n")

        # Score breakdown with visual bars
        print("Score Breakdown:")
        print("─" * 60)
        self._print_score_bar("Financial Health", scorecard['financial_score'])
        self._print_score_bar("Valuation", scorecard['valuation_score'])
        self._print_score_bar("Momentum", scorecard['momentum_score'])

        # Detailed metrics
        fin = scorecard['details']['financial']
        val = scorecard['details']['valuation']
        mom = scorecard['details']['momentum']

        print(f"\n💰 Financial Metrics")
        print("─" * 60)
        print(f"ROE:              {fin['roe']:.1f}%")
        print(f"Operating Margin: {fin['operating_margin']:.1f}%")
        print(f"Net Margin:       {fin['net_margin']:.1f}%")
        print(f"Debt/Equity:      {fin['debt_to_equity']:.2f}")
        print(f"Revenue Growth:   {fin['revenue_growth']:.1f}% YoY")

        print(f"\n📊 Valuation")
        print("─" * 60)
        print(f"P/E Ratio:  {val['pe_ratio']:.1f}   (Sector: {val['sector_pe']:.1f}, {val['pe_discount_pct']:+.1f}%)")
        print(f"P/B Ratio:  {val['pb_ratio']:.1f}   (Sector: {val['sector_pb']:.1f}, {val['pb_discount_pct']:+.1f}%)")

        print(f"\n📈 Technical Indicators")
        print("─" * 60)
        if mom.get('ma20'):
            alignment = "✅" if mom['current_price'] > mom['ma20'] > (mom.get('ma60') or 0) else "⚠️"
            print(f"MA Alignment:  {alignment}")
            print(f"  Price: ${mom['current_price']:.2f}")
            print(f"  MA20:  ${mom['ma20']:.2f}")
            if mom.get('ma60'):
                print(f"  MA60:  ${mom['ma60']:.2f}")
            if mom.get('ma120'):
                print(f"  MA120: ${mom['ma120']:.2f}")

        if mom.get('rsi'):
            rsi_status = "⚠️ Overbought" if mom['rsi'] > 70 else "⚠️ Oversold" if mom['rsi'] < 30 else "✅ Neutral"
            print(f"RSI(14):       {mom['rsi']:.1f}      {rsi_status}")

        if mom.get('macd') and mom.get('signal'):
            macd_status = "✅ Bullish" if mom['macd'] > mom['signal'] else "⚠️ Bearish"
            print(f"MACD:          {macd_status}")

        print()

    def _print_score_bar(self, label: str, score: float):
        """Print a score with a visual bar"""
        bar_length = 20
        filled = int((score / 10) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"{label:20s}: {score:4.1f} / 10  {bar}")


def main():
    """CLI interface for scorecard generation"""
    if len(sys.argv) < 2:
        print("Usage: python scorecard.py TICKER")
        print("Example: python scorecard.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    generator = CompanyScorecardGenerator()
    scorecard = generator.calculate_scorecard(ticker)
    generator.print_scorecard(scorecard)


if __name__ == '__main__':
    main()
