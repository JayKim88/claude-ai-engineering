#!/usr/bin/env python3
"""
Query portfolio holdings and display summary.
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"

def query_portfolio(output_format="table", with_scores=False):
    """
    Query and display portfolio holdings.

    Args:
        output_format: "table" (human-readable) or "json" (machine-readable)
        with_scores: Include latest scores in output

    Returns:
        0 on success, 1 on error
    """
    try:
        if not DB_PATH.exists():
            print(f"❌ Database not found: {DB_PATH}", file=sys.stderr)
            print("💡 Run init_portfolio.py first", file=sys.stderr)
            return 1

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query holdings
        if with_scores:
            query = """
                SELECT
                    h.*,
                    s.overall_score,
                    s.grade,
                    s.date as score_date
                FROM holdings h
                LEFT JOIN (
                    SELECT ticker, overall_score, grade, date,
                           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) as rn
                    FROM score_history
                ) s ON h.ticker = s.ticker AND s.rn = 1
                ORDER BY h.ticker
            """
        else:
            query = "SELECT * FROM holdings ORDER BY ticker"

        cursor.execute(query)
        holdings = cursor.fetchall()

        if not holdings:
            print("📭 Portfolio is empty")
            print("💡 Use add_to_portfolio.py to add holdings")
            conn.close()
            return 0

        # Calculate portfolio totals
        total_cost = 0
        total_value = 0

        for holding in holdings:
            cost = holding['shares'] * holding['avg_price']
            value = holding['shares'] * (holding['current_price'] or holding['avg_price'])
            total_cost += cost
            total_value += value

        total_pl = total_value - total_cost
        total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0

        if output_format == "json":
            # JSON output for agent consumption
            output = {
                "holdings": [dict(h) for h in holdings],
                "summary": {
                    "total_cost": round(total_cost, 2),
                    "total_value": round(total_value, 2),
                    "total_pl": round(total_pl, 2),
                    "total_pl_pct": round(total_pl_pct, 2),
                    "count": len(holdings)
                }
            }
            print(json.dumps(output, indent=2))
        else:
            # Human-readable table output
            print("\n📊 Portfolio Holdings")
            print("=" * 100)

            if with_scores:
                print(f"{'Ticker':<8} {'Shares':>10} {'Avg $':>10} {'Current $':>10} {'P&L %':>10} {'Score':>8} {'Grade':>6}")
                print("-" * 100)
            else:
                print(f"{'Ticker':<8} {'Shares':>10} {'Avg $':>10} {'Current $':>10} {'P&L %':>10} {'Market':>8}")
                print("-" * 100)

            for h in holdings:
                ticker = h['ticker']
                shares = h['shares']
                avg_price = h['avg_price']
                current_price = h['current_price'] or avg_price
                pl_pct = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0

                if with_scores:
                    score = f"{h['overall_score']:.1f}" if h['overall_score'] else "N/A"
                    grade = h['grade'] if h['grade'] else "N/A"
                    print(f"{ticker:<8} {shares:>10.2f} ${avg_price:>9.2f} ${current_price:>9.2f} {pl_pct:>9.2f}% {score:>8} {grade:>6}")
                else:
                    market = h['market'] or 'US'
                    print(f"{ticker:<8} {shares:>10.2f} ${avg_price:>9.2f} ${current_price:>9.2f} {pl_pct:>9.2f}% {market:>8}")

            print("=" * 100)
            print(f"\n💰 Portfolio Summary")
            print(f"   Total Cost:   ${total_cost:,.2f}")
            print(f"   Total Value:  ${total_value:,.2f}")
            print(f"   Total P&L:    ${total_pl:,.2f} ({total_pl_pct:+.2f}%)")
            print(f"   Holdings:     {len(holdings)} stocks\n")

        conn.close()
        return 0

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Query portfolio holdings")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                       help="Output format (default: table)")
    parser.add_argument("--with-scores", action="store_true",
                       help="Include latest scores")

    args = parser.parse_args()
    sys.exit(query_portfolio(args.format, args.with_scores))
