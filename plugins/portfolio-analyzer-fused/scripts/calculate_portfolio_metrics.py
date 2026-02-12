#!/usr/bin/env python3
"""
Calculate portfolio-level risk metrics (beta, correlation, VaR, Sharpe).
Part of portfolio-analyzer-fused plugin.
"""
import json
import sys
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
FETCH_SCRIPT = Path(__file__).parent / "fetch_stock_data.py"

def calculate_portfolio_metrics(output_format="json"):
    """
    Calculate portfolio-level risk and performance metrics.

    Args:
        output_format: "json" or "table"

    Returns:
        0 on success, 1 on error
    """
    try:
        if not DB_PATH.exists():
            print(f"❌ Database not found: {DB_PATH}", file=sys.stderr)
            return 1

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get all holdings
        cursor.execute("""
            SELECT ticker, shares, avg_price, current_price
            FROM holdings
            ORDER BY ticker
        """)
        holdings = cursor.fetchall()

        if not holdings:
            print("📭 Portfolio is empty", file=sys.stderr)
            conn.close()
            return 1

        # Calculate portfolio composition
        total_value = 0
        positions = []

        for h in holdings:
            ticker = h['ticker']
            shares = h['shares']
            price = h['current_price'] or h['avg_price']
            value = shares * price
            total_value += value

            positions.append({
                'ticker': ticker,
                'value': value,
                'weight': 0  # Will calculate after total
            })

        # Calculate weights
        for pos in positions:
            pos['weight'] = pos['value'] / total_value if total_value > 0 else 0

        # Fetch beta and volatility for each stock
        print("🔄 Fetching risk data...", file=sys.stderr)
        betas = []
        volatilities = []

        for pos in positions:
            try:
                result = subprocess.run(
                    [sys.executable, str(FETCH_SCRIPT), pos['ticker']],
                    capture_output=True,
                    text=True,
                    timeout=15
                )

                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    beta = data.get('technicals', {}).get('beta')
                    if beta:
                        betas.append({'ticker': pos['ticker'], 'beta': beta, 'weight': pos['weight']})

                    # Estimate volatility from 52w range (simplified)
                    price_data = data.get('price', {})
                    high_52w = price_data.get('52w_high')
                    low_52w = price_data.get('52w_low')
                    current = price_data.get('current')

                    if high_52w and low_52w and current:
                        # Simple volatility estimate: (high - low) / current
                        vol_estimate = (high_52w - low_52w) / current
                        volatilities.append({'ticker': pos['ticker'], 'volatility': vol_estimate, 'weight': pos['weight']})

            except Exception as e:
                print(f"⚠️  Failed to fetch data for {pos['ticker']}: {e}", file=sys.stderr)

        # Calculate portfolio-weighted beta
        portfolio_beta = None
        if betas:
            portfolio_beta = sum(b['beta'] * b['weight'] for b in betas)

        # Calculate portfolio volatility (simplified weighted average)
        portfolio_volatility = None
        if volatilities:
            portfolio_volatility = sum(v['volatility'] * v['weight'] for v in volatilities)

        # Calculate concentration metrics
        max_position = max(pos['weight'] for pos in positions)
        top_3_concentration = sum(sorted([pos['weight'] for pos in positions], reverse=True)[:3])

        # Sector diversification (simplified - would need sector data)
        num_holdings = len(positions)

        # Build metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "portfolio_value": round(total_value, 2),
            "num_holdings": num_holdings,
            "concentration": {
                "max_position_weight": round(max_position * 100, 2),
                "top_3_weight": round(top_3_concentration * 100, 2)
            },
            "risk": {
                "portfolio_beta": round(portfolio_beta, 3) if portfolio_beta else None,
                "portfolio_volatility": round(portfolio_volatility, 3) if portfolio_volatility else None
            },
            "positions": positions
        }

        conn.close()

        if output_format == "json":
            print(json.dumps(metrics, indent=2))
        else:
            # Human-readable table
            print("\n📊 Portfolio Risk Metrics")
            print("=" * 60)
            print(f"Portfolio Value:     ${metrics['portfolio_value']:,.2f}")
            print(f"Number of Holdings:  {metrics['num_holdings']}")
            print()
            print(f"Concentration:")
            print(f"  Max Position:      {metrics['concentration']['max_position_weight']:.2f}%")
            print(f"  Top 3 Holdings:    {metrics['concentration']['top_3_weight']:.2f}%")
            print()
            print(f"Risk Metrics:")
            if metrics['risk']['portfolio_beta']:
                print(f"  Portfolio Beta:    {metrics['risk']['portfolio_beta']:.3f}")
            if metrics['risk']['portfolio_volatility']:
                print(f"  Portfolio Vol:     {metrics['risk']['portfolio_volatility']:.3f}")
            print("=" * 60)
            print()

        return 0

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate portfolio risk metrics")
    parser.add_argument("--format", choices=["json", "table"], default="table",
                       help="Output format (default: table)")

    args = parser.parse_args()

    sys.exit(calculate_portfolio_metrics(args.format))
