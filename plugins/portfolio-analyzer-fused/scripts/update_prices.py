#!/usr/bin/env python3
"""
Update current prices for all holdings in portfolio.
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
FETCH_SCRIPT = Path(__file__).parent / "fetch_stock_data.py"

def update_prices():
    """
    Update current prices for all holdings by fetching latest data.

    Returns:
        0 on success, 1 on error
    """
    try:
        if not DB_PATH.exists():
            print(f"❌ Database not found: {DB_PATH}", file=sys.stderr)
            return 1

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get all holdings
        cursor.execute("SELECT ticker FROM holdings ORDER BY ticker")
        tickers = [row[0] for row in cursor.fetchall()]

        if not tickers:
            print("📭 Portfolio is empty - no prices to update")
            conn.close()
            return 0

        print(f"🔄 Updating prices for {len(tickers)} holdings...")
        print()

        updated_count = 0
        failed_count = 0

        for ticker in tickers:
            try:
                # Call fetch_stock_data.py to get latest data
                result = subprocess.run(
                    [sys.executable, str(FETCH_SCRIPT), ticker],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    current_price = data.get('price', {}).get('current')

                    if current_price:
                        # Update price in database
                        cursor.execute("""
                            UPDATE holdings
                            SET current_price = ?, last_updated = ?
                            WHERE ticker = ?
                        """, (current_price, datetime.now().isoformat(), ticker))

                        # Get avg_price for P&L calculation
                        cursor.execute("SELECT avg_price FROM holdings WHERE ticker = ?", (ticker,))
                        avg_price = cursor.fetchone()[0]
                        pl_pct = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0

                        print(f"✅ {ticker:<8} ${current_price:>10.2f}  ({pl_pct:+7.2f}%)")
                        updated_count += 1
                    else:
                        print(f"⚠️  {ticker:<8} Price not available", file=sys.stderr)
                        failed_count += 1
                else:
                    print(f"⚠️  {ticker:<8} Fetch failed", file=sys.stderr)
                    failed_count += 1

            except subprocess.TimeoutExpired:
                print(f"⚠️  {ticker:<8} Timeout", file=sys.stderr)
                failed_count += 1
            except Exception as e:
                print(f"⚠️  {ticker:<8} Error: {e}", file=sys.stderr)
                failed_count += 1

        conn.commit()
        conn.close()

        print()
        print(f"📊 Update Summary:")
        print(f"   Updated:  {updated_count}/{len(tickers)}")
        if failed_count > 0:
            print(f"   Failed:   {failed_count}/{len(tickers)}")

        print()
        print("💡 Run query_portfolio.py to see updated portfolio")

        return 0 if failed_count == 0 else 1

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(update_prices())
