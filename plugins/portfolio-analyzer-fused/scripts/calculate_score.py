#!/usr/bin/env python3
"""
Calculate investment score for a stock (financial + valuation + momentum).
Part of portfolio-analyzer-fused plugin.
"""
import json
import sys
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
FETCH_SCRIPT = Path(__file__).parent / "fetch_stock_data.py"

def score_financial_health(fundamentals):
    """Score financial health (0-10) based on profitability, growth, stability."""
    score = 5.0  # Start at neutral

    # ROE (Return on Equity)
    roe = fundamentals.get('roe')
    if roe:
        if roe > 0.20:
            score += 1.5
        elif roe > 0.15:
            score += 1.0
        elif roe > 0.10:
            score += 0.5
        elif roe < 0:
            score -= 1.5

    # Profit Margin
    margin = fundamentals.get('profit_margin')
    if margin:
        if margin > 0.20:
            score += 1.5
        elif margin > 0.10:
            score += 1.0
        elif margin > 0.05:
            score += 0.5
        elif margin < 0:
            score -= 1.5

    # Debt to Equity
    de_ratio = fundamentals.get('debt_to_equity')
    if de_ratio is not None:
        if de_ratio < 0.5:
            score += 1.0
        elif de_ratio < 1.0:
            score += 0.5
        elif de_ratio > 2.0:
            score -= 1.0

    # Revenue Growth
    rev_growth = fundamentals.get('revenue_growth')
    if rev_growth:
        if rev_growth > 0.20:
            score += 1.0
        elif rev_growth > 0.10:
            score += 0.5
        elif rev_growth < -0.05:
            score -= 1.0

    return max(0, min(10, score))

def score_valuation(fundamentals):
    """Score valuation (0-10) based on P/E, PEG, P/B ratios."""
    score = 5.0  # Start at neutral

    # P/E Ratio
    pe = fundamentals.get('pe_ratio')
    if pe:
        if 10 < pe < 20:
            score += 1.5  # Sweet spot
        elif 20 <= pe < 30:
            score += 0.5
        elif pe < 10:
            score += 1.0  # Potentially undervalued
        elif pe > 40:
            score -= 1.5  # Expensive

    # PEG Ratio (P/E to Growth)
    peg = fundamentals.get('peg_ratio')
    if peg:
        if peg < 1.0:
            score += 2.0  # Growth at reasonable price
        elif peg < 1.5:
            score += 1.0
        elif peg > 2.0:
            score -= 1.0

    # P/B Ratio
    pb = fundamentals.get('pb_ratio')
    if pb:
        if pb < 1.0:
            score += 1.0  # Potentially undervalued
        elif pb < 3.0:
            score += 0.5
        elif pb > 5.0:
            score -= 1.0

    return max(0, min(10, score))

def score_momentum(price_data, technicals):
    """Score momentum (0-10) based on price trends and moving averages."""
    score = 5.0  # Start at neutral

    current = price_data.get('current')
    if not current:
        return score

    # 50-day MA
    ma_50 = technicals.get('ma_50')
    if ma_50:
        if current > ma_50:
            score += 1.0  # Above 50-day MA
        else:
            score -= 0.5

    # 200-day MA
    ma_200 = technicals.get('ma_200')
    if ma_200:
        if current > ma_200:
            score += 1.0  # Above 200-day MA
        else:
            score -= 0.5

    # 3-month return
    three_mo_return = technicals.get('three_month_return')
    if three_mo_return is not None:
        if three_mo_return > 20:
            score += 1.5
        elif three_mo_return > 10:
            score += 1.0
        elif three_mo_return > 0:
            score += 0.5
        elif three_mo_return < -20:
            score -= 1.5
        elif three_mo_return < -10:
            score -= 1.0

    # 52-week position
    high_52w = price_data.get('52w_high')
    low_52w = price_data.get('52w_low')
    if high_52w and low_52w and high_52w > low_52w:
        position = (current - low_52w) / (high_52w - low_52w)
        if position > 0.8:
            score += 1.0  # Near 52w high
        elif position < 0.2:
            score -= 1.0  # Near 52w low

    return max(0, min(10, score))

def calculate_score(ticker, save_to_db=False):
    """
    Calculate comprehensive investment score for a stock.

    Args:
        ticker: Stock ticker symbol
        save_to_db: If True, save score to database

    Returns:
        0 on success, 1 on error
    """
    try:
        # Fetch stock data
        result = subprocess.run(
            [sys.executable, str(FETCH_SCRIPT), ticker],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            print(f"❌ Failed to fetch data for {ticker}", file=sys.stderr)
            return 1

        data = json.loads(result.stdout)

        # Calculate component scores
        fundamentals = data.get('fundamentals', {})
        price_data = data.get('price', {})
        technicals = data.get('technicals', {})

        financial_score = score_financial_health(fundamentals)
        valuation_score = score_valuation(fundamentals)
        momentum_score = score_momentum(price_data, technicals)

        # Weighted overall score (Financial 40%, Valuation 35%, Momentum 25%)
        overall_score = (
            financial_score * 0.40 +
            valuation_score * 0.35 +
            momentum_score * 0.25
        )

        # Assign grade
        if overall_score >= 9.0:
            grade = "A+"
        elif overall_score >= 8.0:
            grade = "A"
        elif overall_score >= 7.0:
            grade = "B+"
        elif overall_score >= 6.0:
            grade = "B"
        elif overall_score >= 5.0:
            grade = "C"
        else:
            grade = "D"

        # Build result
        result = {
            "ticker": ticker,
            "date": datetime.now().isoformat(),
            "overall_score": round(overall_score, 2),
            "grade": grade,
            "component_scores": {
                "financial_health": round(financial_score, 2),
                "valuation": round(valuation_score, 2),
                "momentum": round(momentum_score, 2)
            },
            "company": data.get('company', {}),
            "current_price": price_data.get('current')
        }

        # Save to database if requested
        if save_to_db and DB_PATH.exists():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO score_history
                (ticker, date, overall_score, financial_score, valuation_score, momentum_score, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker,
                datetime.now().date().isoformat(),
                overall_score,
                financial_score,
                valuation_score,
                momentum_score,
                grade
            ))

            conn.commit()
            conn.close()

        # Output result
        print(json.dumps(result, indent=2))
        return 0

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout fetching data for {ticker}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate investment score for a stock")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("--save", action="store_true",
                       help="Save score to database")

    args = parser.parse_args()

    sys.exit(calculate_score(args.ticker.upper(), args.save))
