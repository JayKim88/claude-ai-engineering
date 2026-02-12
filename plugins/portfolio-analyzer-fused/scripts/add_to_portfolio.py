#!/usr/bin/env python3
"""
Add stock holdings to portfolio database.
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"

def add_to_portfolio(ticker, action, shares, price, market="US", notes=""):
    """
    Add a transaction and update holdings.

    Args:
        ticker: Stock ticker symbol
        action: "buy" or "sell"
        shares: Number of shares
        price: Price per share
        market: Market (US, KR, etc.)
        notes: Optional transaction notes

    Returns:
        0 on success, 1 on error
    """
    try:
        if not DB_PATH.exists():
            print(f"❌ Database not found: {DB_PATH}", file=sys.stderr)
            print("💡 Run init_portfolio.py first", file=sys.stderr)
            return 1

        if action not in ["buy", "sell"]:
            print(f"❌ Invalid action: {action}. Must be 'buy' or 'sell'", file=sys.stderr)
            return 1

        if shares <= 0:
            print(f"❌ Invalid shares: {shares}. Must be positive", file=sys.stderr)
            return 1

        if price <= 0:
            print(f"❌ Invalid price: {price}. Must be positive", file=sys.stderr)
            return 1

        ticker = ticker.upper()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Record transaction
        cursor.execute("""
            INSERT INTO transactions (ticker, action, shares, price, date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticker, action, shares, price, datetime.now().isoformat(), notes))

        # Update holdings
        cursor.execute("SELECT * FROM holdings WHERE ticker = ?", (ticker,))
        holding = cursor.fetchone()

        if action == "buy":
            if holding:
                # Update existing holding
                current_shares = holding[2]  # shares column
                current_avg_price = holding[3]  # avg_price column
                new_shares = current_shares + shares
                new_avg_price = ((current_shares * current_avg_price) + (shares * price)) / new_shares

                cursor.execute("""
                    UPDATE holdings
                    SET shares = ?, avg_price = ?, last_updated = ?
                    WHERE ticker = ?
                """, (new_shares, new_avg_price, datetime.now().isoformat(), ticker))

                print(f"✅ Updated holding: {ticker}")
                print(f"   Shares: {current_shares:.2f} → {new_shares:.2f}")
                print(f"   Avg Price: ${current_avg_price:.2f} → ${new_avg_price:.2f}")
            else:
                # Create new holding
                cursor.execute("""
                    INSERT INTO holdings (ticker, shares, avg_price, current_price, market, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (ticker, shares, price, price, market, datetime.now().isoformat()))

                print(f"✅ Added new holding: {ticker}")
                print(f"   Shares: {shares:.2f}")
                print(f"   Avg Price: ${price:.2f}")
                print(f"   Market: {market}")

        elif action == "sell":
            if not holding:
                print(f"❌ Cannot sell: {ticker} not in portfolio", file=sys.stderr)
                conn.rollback()
                conn.close()
                return 1

            current_shares = holding[2]

            if shares > current_shares:
                print(f"❌ Cannot sell {shares:.2f} shares: only {current_shares:.2f} available", file=sys.stderr)
                conn.rollback()
                conn.close()
                return 1

            new_shares = current_shares - shares

            if new_shares == 0:
                # Remove holding if fully sold
                cursor.execute("DELETE FROM holdings WHERE ticker = ?", (ticker,))
                print(f"✅ Sold all shares of {ticker}")
                print(f"   Removed from portfolio")
            else:
                # Update remaining shares (keep same avg_price)
                cursor.execute("""
                    UPDATE holdings
                    SET shares = ?, last_updated = ?
                    WHERE ticker = ?
                """, (new_shares, datetime.now().isoformat(), ticker))

                print(f"✅ Sold shares of {ticker}")
                print(f"   Shares: {current_shares:.2f} → {new_shares:.2f}")

            # Calculate P&L for this transaction
            avg_price = holding[3]
            realized_pl = (price - avg_price) * shares
            realized_pl_pct = ((price - avg_price) / avg_price * 100) if avg_price > 0 else 0

            print(f"   Realized P&L: ${realized_pl:,.2f} ({realized_pl_pct:+.2f}%)")

        conn.commit()
        conn.close()

        print(f"\n💡 Run query_portfolio.py to see updated portfolio")
        return 0

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add stock transaction to portfolio")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument("action", choices=["buy", "sell"], help="Transaction action")
    parser.add_argument("shares", type=float, help="Number of shares")
    parser.add_argument("price", type=float, help="Price per share")
    parser.add_argument("--market", default="US", help="Market (default: US)")
    parser.add_argument("--notes", default="", help="Optional transaction notes")

    args = parser.parse_args()

    sys.exit(add_to_portfolio(
        args.ticker,
        args.action,
        args.shares,
        args.price,
        args.market,
        args.notes
    ))
