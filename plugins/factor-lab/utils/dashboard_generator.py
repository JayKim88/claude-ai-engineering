#!/usr/bin/env python3
"""
HTML Dashboard Generator

Generates interactive HTML dashboards for screening and backtest results.
"""

import os
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd


def generate_screening_dashboard(
    results_df: pd.DataFrame,
    output_path: str,
    title: str = "Factor Lab - Screening Results",
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate an interactive HTML dashboard for screening results

    Args:
        results_df: DataFrame with screening results
        output_path: Path to save HTML file
        title: Dashboard title
        metadata: Additional metadata (universe, factors, etc.)

    Returns:
        Path to generated HTML file
    """

    # Prepare data
    top_30 = results_df.head(30)

    # Calculate statistics
    avg_score = top_30['composite_score'].mean()
    sector_counts = top_30['sector'].value_counts().to_dict()
    grade_counts = top_30['grade'].value_counts().to_dict()

    # Generate sector chart data
    sector_labels = json.dumps(list(sector_counts.keys()))
    sector_values = json.dumps(list(sector_counts.values()))

    # Generate factor distribution data
    factor_cols = ['value_score', 'quality_score', 'momentum_score', 'low_vol_score', 'size_score']
    factor_avgs = {col: top_30[col].mean() for col in factor_cols if col in top_30.columns}
    factor_labels = json.dumps(['Value', 'Quality', 'Momentum', 'Low Vol', 'Size'])
    factor_values = json.dumps([factor_avgs.get(f'{f.lower()}_score', 0) for f in ['value', 'quality', 'momentum', 'low_vol', 'size']])

    # Generate table rows
    table_rows = ""
    for idx, row in top_30.iterrows():
        rank = idx + 1 if isinstance(idx, int) else list(top_30.index).index(idx) + 1

        # Color code scores
        composite_color = _get_score_color(row['composite_score'])
        value_color = _get_score_color(row.get('value_score', 0))
        quality_color = _get_score_color(row.get('quality_score', 0))
        momentum_color = _get_score_color(row.get('momentum_score', 0))

        table_rows += f"""
        <tr>
            <td>{rank}</td>
            <td><strong>{row['ticker']}</strong></td>
            <td class="company-name">{row.get('name', 'N/A')}</td>
            <td><span class="score-badge" style="background-color: {composite_color};">{row['composite_score']:.1f}</span></td>
            <td><span class="score-badge" style="background-color: {value_color};">{row.get('value_score', 0):.1f}</span></td>
            <td><span class="score-badge" style="background-color: {quality_color};">{row.get('quality_score', 0):.1f}</span></td>
            <td><span class="score-badge" style="background-color: {momentum_color};">{row.get('momentum_score', 0):.1f}</span></td>
            <td>{row.get('sector', 'N/A')}</td>
            <td>{row.get('grade', 'N/A')}</td>
            <td>${row.get('price', 0):.2f}</td>
            <td>{_format_large_number(row.get('market_cap', 0))}</td>
            <td>{f"{row.get('pe_ratio', 0):.2f}" if pd.notna(row.get('pe_ratio')) and row.get('pe_ratio') else 'N/A'}</td>
            <td>{f"{row.get('pb_ratio', 0):.2f}" if pd.notna(row.get('pb_ratio')) and row.get('pb_ratio') else 'N/A'}</td>
            <td>{f"{row.get('roe', 0) * 100:.2f}%" if pd.notna(row.get('roe')) and row.get('roe') else 'N/A'}</td>
        </tr>
        """

    # Metadata section
    metadata_html = ""
    if metadata:
        metadata_html = f"""
        <div class="metadata">
            <p><strong>Universe:</strong> {metadata.get('universe', 'N/A')}</p>
            <p><strong>Factor Weights:</strong> {metadata.get('factors', 'N/A')}</p>
            <p><strong>Total Screened:</strong> {metadata.get('total_screened', len(results_df))}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """

    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        }}
        .card h3 {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .card h2 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 5px;
        }}
        .card p {{
            color: #6c757d;
            font-size: 0.95em;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section h2 {{
            color: #2d3748;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        .chart-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }}
        .chart-card h3 {{
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 1.2em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }}
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .score-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: 600;
            color: white;
            font-size: 0.9em;
        }}
        .company-name {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .metadata p {{
            margin-bottom: 8px;
            color: #495057;
        }}
        .metadata strong {{
            color: #2d3748;
        }}
        .download-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-top: 40px;
        }}
        .download-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            margin: 10px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
        }}
        footer {{
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        @media print {{
            body {{ background: white; }}
            .download-section {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 {title}</h1>
            <p>Quantitative Factor Screening Results</p>
        </header>

        <div class="summary-cards">
            <div class="card">
                <h3>Top Stock</h3>
                <h2>{top_30.iloc[0]['ticker']}</h2>
                <p>Score: {top_30.iloc[0]['composite_score']:.1f}</p>
            </div>
            <div class="card">
                <h3>Total Stocks</h3>
                <h2>{len(top_30)}</h2>
                <p>Selected from {len(results_df)}</p>
            </div>
            <div class="card">
                <h3>Avg Score</h3>
                <h2>{avg_score:.1f}</h2>
                <p>{'Exceptional' if avg_score >= 90 else 'Excellent' if avg_score >= 80 else 'Good'}</p>
            </div>
            <div class="card">
                <h3>Sectors</h3>
                <h2>{len(sector_counts)}</h2>
                <p>Diversified</p>
            </div>
        </div>

        <div class="content">
            {metadata_html}

            <div class="charts-container">
                <div class="chart-card">
                    <h3>📈 Sector Distribution</h3>
                    <canvas id="sectorChart"></canvas>
                </div>
                <div class="chart-card">
                    <h3>📊 Average Factor Scores</h3>
                    <canvas id="factorChart"></canvas>
                </div>
            </div>

            <div class="section">
                <h2>🏆 Top 30 Stocks</h2>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Ticker</th>
                                <th>Company</th>
                                <th>Score</th>
                                <th>Value</th>
                                <th>Quality</th>
                                <th>Momentum</th>
                                <th>Sector</th>
                                <th>Grade</th>
                                <th>Price</th>
                                <th>Market Cap</th>
                                <th>P/E</th>
                                <th>P/B</th>
                                <th>ROE</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="download-section">
                <h3>📥 Export Results</h3>
                <p style="margin-bottom: 20px;">Download this data in various formats</p>
                <a href="#" class="download-btn" onclick="window.print(); return false;">Print / Save as PDF</a>
            </div>
        </div>

        <footer>
            <p>Generated by <strong>factor-lab</strong> | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Made with 📊 for quantitative investors</p>
        </footer>
    </div>

    <script>
        // Sector Distribution Chart
        const sectorCtx = document.getElementById('sectorChart').getContext('2d');
        new Chart(sectorCtx, {{
            type: 'pie',
            data: {{
                labels: {sector_labels},
                datasets: [{{
                    data: {sector_values},
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                        '#a8edea', '#fed6e3'
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 15,
                            font: {{ size: 12 }}
                        }}
                    }}
                }}
            }}
        }});

        // Factor Scores Chart
        const factorCtx = document.getElementById('factorChart').getContext('2d');
        new Chart(factorCtx, {{
            type: 'bar',
            data: {{
                labels: {factor_labels},
                datasets: [{{
                    label: 'Average Score',
                    data: {factor_values},
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(240, 147, 251, 0.8)',
                        'rgba(79, 172, 254, 0.8)',
                        'rgba(67, 233, 123, 0.8)'
                    ],
                    borderWidth: 0,
                    borderRadius: 8
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
    """

    # Write to file
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path


def generate_backtest_dashboard(
    equity_curve_csv: str,
    trades_csv: str,
    output_path: str,
    title: str = "Factor Lab - Backtest Results",
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate an interactive HTML dashboard for backtest results

    Args:
        equity_curve_csv: Path to equity curve CSV file
        trades_csv: Path to trades CSV file
        output_path: Path to save HTML file
        title: Dashboard title
        metadata: Additional metadata (strategy, period, metrics)

    Returns:
        Path to generated HTML file
    """

    # Load data
    equity_df = pd.read_csv(equity_curve_csv)
    trades_df = pd.read_csv(trades_csv) if os.path.exists(trades_csv) else pd.DataFrame()

    # Extract metrics from metadata
    total_return = metadata.get('total_return', 0)
    annual_return = metadata.get('annual_return', 0)
    sharpe_ratio = metadata.get('sharpe_ratio', 0)
    max_drawdown = metadata.get('max_drawdown', 0)
    num_trades = len(trades_df) if not trades_df.empty else metadata.get('num_trades', 0)
    win_rate = metadata.get('win_rate', 0)

    # Prepare equity curve data for Chart.js (handle both uppercase and lowercase column names)
    date_col = 'Date' if 'Date' in equity_df.columns else 'date'
    value_col = 'Portfolio_Value' if 'Portfolio_Value' in equity_df.columns else 'portfolio_value'

    equity_dates = json.dumps(equity_df[date_col].tolist())
    equity_values = json.dumps(equity_df[value_col].tolist())

    # Calculate monthly returns if possible
    monthly_returns_html = ""
    if date_col in equity_df.columns and len(equity_df) > 1:
        equity_df[date_col] = pd.to_datetime(equity_df[date_col])
        equity_df['Returns'] = equity_df[value_col].pct_change() * 100
        monthly_returns_html = "<p>Monthly returns calculation available in equity curve.</p>"

    # Generate trades table (last 20 trades)
    trades_table_rows = ""
    if not trades_df.empty:
        # Handle both uppercase and lowercase column names
        trades_date_col = 'Date' if 'Date' in trades_df.columns else 'date'
        trades_ticker_col = 'Ticker' if 'Ticker' in trades_df.columns else 'ticker'
        trades_action_col = 'Action' if 'Action' in trades_df.columns else 'action'
        trades_shares_col = 'Shares' if 'Shares' in trades_df.columns else 'shares'
        trades_price_col = 'Price' if 'Price' in trades_df.columns else 'price'
        trades_value_col = 'Total' if 'Total' in trades_df.columns else 'value'

        recent_trades = trades_df.tail(20)
        for idx, row in recent_trades.iterrows():
            action = row.get(trades_action_col, 'BUY')
            action_color = '#10b981' if action.upper() == 'BUY' else '#ef4444'
            trades_table_rows += f"""
            <tr>
                <td>{row.get(trades_date_col, 'N/A')}</td>
                <td><strong>{row.get(trades_ticker_col, 'N/A')}</strong></td>
                <td><span style="color: {action_color}; font-weight: 600;">{action.upper()}</span></td>
                <td>{row.get(trades_shares_col, 0):.0f}</td>
                <td>${row.get(trades_price_col, 0):.2f}</td>
                <td>${row.get(trades_value_col, 0):.2f}</td>
            </tr>
            """
    else:
        trades_table_rows = "<tr><td colspan='6' style='text-align: center;'>No trade data available</td></tr>"

    # Metadata section
    metadata_html = ""
    if metadata:
        metadata_html = f"""
        <div class="metadata">
            <p><strong>Strategy:</strong> {metadata.get('strategy', 'N/A')}</p>
            <p><strong>Period:</strong> {metadata.get('start_date', 'N/A')} to {metadata.get('end_date', 'N/A')}</p>
            <p><strong>Universe:</strong> {metadata.get('universe', 'N/A')}</p>
            <p><strong>Rebalancing:</strong> {metadata.get('rebalance', 'N/A')}</p>
            <p><strong>Initial Capital:</strong> ${metadata.get('initial_cash', 100000):,.0f}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """

    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .metrics-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        }}
        .metric-card h3 {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        .metric-card h2 {{
            font-size: 2.2em;
            margin-bottom: 5px;
        }}
        .metric-card h2.positive {{
            color: #10b981;
        }}
        .metric-card h2.negative {{
            color: #ef4444;
        }}
        .metric-card h2.neutral {{
            color: #667eea;
        }}
        .metric-card p {{
            color: #6c757d;
            font-size: 0.95em;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section h2 {{
            color: #2d3748;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            margin-bottom: 40px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }}
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .metadata p {{
            margin-bottom: 8px;
            color: #495057;
        }}
        .metadata strong {{
            color: #2d3748;
        }}
        .download-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-top: 40px;
        }}
        .download-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            margin: 10px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
        }}
        footer {{
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        @media print {{
            body {{ background: white; }}
            .download-section {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 {title}</h1>
            <p>Historical Strategy Performance Analysis</p>
        </header>

        <div class="metrics-cards">
            <div class="metric-card">
                <h3>Total Return</h3>
                <h2 class="{'positive' if total_return > 0 else 'negative'}">{total_return:+.2f}%</h2>
                <p>Cumulative</p>
            </div>
            <div class="metric-card">
                <h3>Annual Return</h3>
                <h2 class="{'positive' if annual_return > 0 else 'negative'}">{annual_return:+.2f}%</h2>
                <p>Annualized</p>
            </div>
            <div class="metric-card">
                <h3>Sharpe Ratio</h3>
                <h2 class="neutral">{sharpe_ratio:.2f}</h2>
                <p>{'Excellent' if sharpe_ratio > 2 else 'Good' if sharpe_ratio > 1 else 'Fair'}</p>
            </div>
            <div class="metric-card">
                <h3>Max Drawdown</h3>
                <h2 class="negative">{max_drawdown:.2f}%</h2>
                <p>Peak to Trough</p>
            </div>
            <div class="metric-card">
                <h3>Total Trades</h3>
                <h2 class="neutral">{num_trades:,.0f}</h2>
                <p>Executions</p>
            </div>
            <div class="metric-card">
                <h3>Win Rate</h3>
                <h2 class="{'positive' if win_rate > 50 else 'negative'}">{win_rate:.1f}%</h2>
                <p>Winning Trades</p>
            </div>
        </div>

        <div class="content">
            {metadata_html}

            <div class="section">
                <h2>📈 Equity Curve</h2>
                <div class="chart-container">
                    <canvas id="equityChart"></canvas>
                </div>
            </div>

            <div class="section">
                <h2>💼 Recent Trades (Last 20)</h2>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Ticker</th>
                                <th>Action</th>
                                <th>Shares</th>
                                <th>Price</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {trades_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            {monthly_returns_html}

            <div class="download-section">
                <h3>📥 Export Results</h3>
                <p style="margin-bottom: 20px;">Download this report in various formats</p>
                <a href="#" class="download-btn" onclick="window.print(); return false;">Print / Save as PDF</a>
            </div>
        </div>

        <footer>
            <p>Generated by <strong>factor-lab</strong> | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Made with 📊 for quantitative investors</p>
        </footer>
    </div>

    <script>
        // Equity Curve Chart
        const equityCtx = document.getElementById('equityChart').getContext('2d');
        new Chart(equityCtx, {{
            type: 'line',
            data: {{
                labels: {equity_dates},
                datasets: [{{
                    label: 'Portfolio Value',
                    data: {equity_values},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }},
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString();
                            }}
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Value: $' + context.parsed.y.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
    """

    # Write to file
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path


def _get_score_color(score: float) -> str:
    """Get color for score badge"""
    if score >= 90:
        return '#10b981'  # Green
    elif score >= 80:
        return '#3b82f6'  # Blue
    elif score >= 70:
        return '#f59e0b'  # Orange
    elif score >= 60:
        return '#ef4444'  # Red
    else:
        return '#6c757d'  # Gray


def _format_large_number(num: float) -> str:
    """Format large numbers (market cap)"""
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    else:
        return f"${num:,.0f}"


if __name__ == '__main__':
    print("Dashboard Generator utility - use from factor_screener.py or backtest_engine.py")
