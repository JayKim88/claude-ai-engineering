#!/usr/bin/env python3
"""
Delete a holding from portfolio (removes from holdings, keeps transaction history).
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"

def delete_holding(ticker, keep_transactions=True):
    """
    Delete a holding from the portfolio.

    Args:
        ticker: Stock ticker symbol
        keep_transactions: If True, keep transaction history (default)

    Returns:
        0 on success, 1 on error
    """
    try:
        if not DB_PATH.exists():
            print(f"❌ Database not found: {DB_PATH}", file=sys.stderr)
            return 1

        ticker = ticker.upper()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if holding exists
        cursor.execute("SELECT * FROM holdings WHERE ticker = ?", (ticker,))
        holding = cursor.fetchone()

        if not holding:
            print(f"❌ Holding not found: {ticker}", file=sys.stderr)
            conn.close()
            return 1

        # Delete holding
        cursor.execute("DELETE FROM holdings WHERE ticker = ?", (ticker,))

        print(f"✅ Deleted holding: {ticker}")
        print(f"   Shares: {holding[2]:.2f}")
        print(f"   Avg Price: ${holding[3]:.2f}")

        if not keep_transactions:
            # Also delete transaction history
            cursor.execute("DELETE FROM transactions WHERE ticker = ?", (ticker,))
            print(f"   Transaction history also deleted")
        else:
            print(f"   Transaction history preserved")

        conn.commit()
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

    parser = argparse.ArgumentParser(description="Delete a holding from portfolio")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("--delete-transactions", action="store_true",
                       help="Also delete transaction history (default: keep)")

    args = parser.parse_args()

    sys.exit(delete_holding(args.ticker, not args.delete_transactions))
