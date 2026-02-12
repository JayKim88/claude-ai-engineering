#!/usr/bin/env python3
"""
Generate interactive HTML dashboard for portfolio visualization.
Part of portfolio-analyzer-fused plugin.
"""
import sqlite3
import sys
import json
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "data" / "portfolio.db"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "portfolio_dashboard.html"
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "dashboard.html"
FETCH_SCRIPT = Path(__file__).parent / "fetch_stock_data.py"

def generate_dashboard(auto_open=True):
    """
    Generate interactive HTML dashboard with Chart.js visualizations.

    Args:
        auto_open: Automatically open in browser

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

        # Get holdings with scores
        cursor.execute("""
            SELECT
                h.*,
                s.overall_score,
                s.financial_score,
                s.valuation_score,
                s.momentum_score,
                s.grade
            FROM holdings h
            LEFT JOIN (
                SELECT ticker, overall_score, financial_score, valuation_score, momentum_score, grade,
                       ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) as rn
                FROM score_history
            ) s ON h.ticker = s.ticker AND s.rn = 1
            ORDER BY h.ticker
        """)
        holdings = cursor.fetchall()

        if not holdings:
            print("📭 Portfolio is empty", file=sys.stderr)
            conn.close()
            return 1

        # Fetch sector data
        print("🔄 Fetching company data...", file=sys.stderr)
        sector_allocation = defaultdict(float)
        total_value = 0

        holdings_data = []
        for h in holdings:
            ticker = h['ticker']
            shares = h['shares']
            avg_price = h['avg_price']
            current_price = h['current_price'] or avg_price
            value = shares * current_price
            pl_pct = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0

            total_value += value

            # Fetch sector info
            sector = "Other"
            try:
                result = subprocess.run(
                    [sys.executable, str(FETCH_SCRIPT), ticker],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    sector = data.get('company', {}).get('sector') or "Other"
            except:
                pass

            sector_allocation[sector] += value

            holdings_data.append({
                'ticker': ticker,
                'shares': shares,
                'avg_price': avg_price,
                'current_price': current_price,
                'value': value,
                'pl_pct': pl_pct,
                'sector': sector,
                'score': h['overall_score'],
                'grade': h['grade']
            })

        # Calculate weights
        for h in holdings_data:
            h['weight'] = (h['value'] / total_value * 100) if total_value > 0 else 0

        # Prepare chart data
        sector_labels = list(sector_allocation.keys())
        sector_values = [sector_allocation[s] for s in sector_labels]

        score_distribution = defaultdict(int)
        for h in holdings_data:
            if h['score']:
                grade = h['grade']
                score_distribution[grade] += 1

        # Calculate summary statistics
        total_cost = sum(h['shares'] * h['avg_price'] for h in holdings_data)
        total_pl = total_value - total_cost
        total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0

        scores = [h['score'] for h in holdings_data if h['score']]
        avg_score = sum(scores) / len(scores) if scores else 0

        weighted_score = sum(h['score'] * h['weight'] / 100 for h in holdings_data if h['score'])

        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f0f23; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #00d9ff; font-size: 2em; margin-bottom: 10px; }}
        .timestamp {{ color: #888; font-size: 0.9em; margin-bottom: 30px; }}
        .summary-card {{ background: #1a1a2e; padding: 20px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #333; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .metric {{ text-align: center; }}
        .metric-label {{ color: #888; font-size: 0.9em; margin-bottom: 5px; }}
        .metric-value {{ font-size: 1.8em; font-weight: bold; }}
        .metric-value.positive {{ color: #00ff88; }}
        .metric-value.negative {{ color: #ff4444; }}
        .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px; margin-bottom: 30px; }}
        .chart-card {{ background: #1a1a2e; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
        .chart-card h2 {{ color: #00d9ff; margin-bottom: 15px; font-size: 1.3em; }}
        table {{ width: 100%; border-collapse: collapse; background: #1a1a2e; border-radius: 10px; overflow: hidden; }}
        th {{ background: #252540; color: #00d9ff; padding: 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 12px; border-top: 1px solid #333; }}
        tr:hover {{ background: #252540; }}
        .grade-A {{ color: #00ff88; font-weight: bold; }}
        .grade-B {{ color: #00d9ff; font-weight: bold; }}
        .grade-C {{ color: #ffaa00; font-weight: bold; }}
        .grade-D {{ color: #ff4444; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Portfolio Dashboard</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="summary-card">
            <div class="summary-grid">
                <div class="metric">
                    <div class="metric-label">Total Value</div>
                    <div class="metric-value">${total_value:,.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total P&L</div>
                    <div class="metric-value {'positive' if total_pl >= 0 else 'negative'}">${total_pl:,.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">P&L %</div>
                    <div class="metric-value {'positive' if total_pl_pct >= 0 else 'negative'}">{total_pl_pct:+.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Weighted Score</div>
                    <div class="metric-value">{weighted_score:.1f}/10</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Holdings</div>
                    <div class="metric-value">{len(holdings_data)}</div>
                </div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                <h2>Sector Allocation</h2>
                <canvas id="sectorChart"></canvas>
            </div>
            <div class="chart-card">
                <h2>Score Distribution</h2>
                <canvas id="scoreChart"></canvas>
            </div>
            <div class="chart-card">
                <h2>Top Holdings by Value</h2>
                <canvas id="holdingsChart"></canvas>
            </div>
        </div>

        <div class="chart-card">
            <h2>Portfolio Holdings</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Sector</th>
                        <th>Shares</th>
                        <th>Avg Price</th>
                        <th>Current</th>
                        <th>Value</th>
                        <th>Weight</th>
                        <th>P&L %</th>
                        <th>Score</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
"""

        for h in sorted(holdings_data, key=lambda x: x['value'], reverse=True):
            grade_class = f"grade-{h['grade'][0]}" if h['grade'] else ""
            html += f"""
                    <tr>
                        <td><strong>{h['ticker']}</strong></td>
                        <td>{h['sector']}</td>
                        <td>{h['shares']:.2f}</td>
                        <td>${h['avg_price']:.2f}</td>
                        <td>${h['current_price']:.2f}</td>
                        <td>${h['value']:,.2f}</td>
                        <td>{h['weight']:.1f}%</td>
                        <td class="{'positive' if h['pl_pct'] >= 0 else 'negative'}">{h['pl_pct']:+.2f}%</td>
                        <td>{h['score']:.1f if h['score'] else 'N/A'}</td>
                        <td class="{grade_class}">{h['grade'] if h['grade'] else 'N/A'}</td>
                    </tr>
"""

        html += f"""
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Sector Allocation Chart
        new Chart(document.getElementById('sectorChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(sector_labels)},
                datasets: [{{
                    data: {json.dumps(sector_values)},
                    backgroundColor: ['#00d9ff', '#00ff88', '#ffaa00', '#ff4444', '#aa00ff', '#ff00aa', '#88ff00']
                }}]
            }},
            options: {{
                plugins: {{ legend: {{ labels: {{ color: '#e0e0e0' }} }} }}
            }}
        }});

        // Score Distribution Chart
        new Chart(document.getElementById('scoreChart'), {{
            type: 'bar',
            data: {{
                labels: ['A+', 'A', 'B+', 'B', 'C', 'D'],
                datasets: [{{
                    label: 'Number of Stocks',
                    data: {json.dumps([score_distribution.get(g, 0) for g in ['A+', 'A', 'B+', 'B', 'C', 'D']])},
                    backgroundColor: '#00d9ff'
                }}]
            }},
            options: {{
                scales: {{
                    y: {{ ticks: {{ color: '#e0e0e0' }}, grid: {{ color: '#333' }} }},
                    x: {{ ticks: {{ color: '#e0e0e0' }}, grid: {{ color: '#333' }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#e0e0e0' }} }} }}
            }}
        }});

        // Top Holdings Chart
        new Chart(document.getElementById('holdingsChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([h['ticker'] for h in holdings_data[:5]])},
                datasets: [{{
                    label: 'Value ($)',
                    data: {json.dumps([h['value'] for h in holdings_data[:5]])},
                    backgroundColor: '#00ff88'
                }}]
            }},
            options: {{
                indexAxis: 'y',
                scales: {{
                    x: {{ ticks: {{ color: '#e0e0e0' }}, grid: {{ color: '#333' }} }},
                    y: {{ ticks: {{ color: '#e0e0e0' }}, grid: {{ color: '#333' }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#e0e0e0' }} }} }}
            }}
        }});
    </script>
</body>
</html>
"""

        # Write dashboard
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, 'w') as f:
            f.write(html)

        conn.close()

        print(f"✅ Dashboard generated: {OUTPUT_PATH}")

        if auto_open:
            webbrowser.open(f"file://{OUTPUT_PATH.absolute()}")
            print("🌐 Opened in browser")

        return 0

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate portfolio dashboard")
    parser.add_argument("--no-open", action="store_true",
                       help="Don't automatically open in browser")

    args = parser.parse_args()

    sys.exit(generate_dashboard(not args.no_open))
