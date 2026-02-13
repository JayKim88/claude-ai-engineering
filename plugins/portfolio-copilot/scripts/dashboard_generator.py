#!/usr/bin/env python3
"""
Portfolio Dashboard Generator

Generates an interactive HTML dashboard with Chart.js visualizations for portfolio analysis.
"""

import os
import json
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional
from portfolio_manager import PortfolioManager


class PortfolioDashboardGenerator:
    """Generate HTML dashboard for portfolio with interactive charts"""

    def __init__(self, db_path: Optional[str] = None):
        self.portfolio_manager = PortfolioManager(db_path)

    def generate_dashboard(self, portfolio_id: int = 1, output_path: Optional[str] = None) -> str:
        """
        Generate HTML dashboard for portfolio

        Args:
            portfolio_id: Portfolio ID to generate dashboard for
            output_path: Optional output file path (default: ../data/portfolio-dashboard.html)

        Returns:
            Path to generated HTML file
        """
        # Set default output path
        if output_path is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            os.makedirs(data_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y-%m-%d')
            output_path = os.path.join(data_dir, f'portfolio-dashboard-{timestamp}.html')

        # Fetch portfolio data
        portfolio_data = self._fetch_portfolio_data(portfolio_id)

        # Calculate metrics
        metrics = self._calculate_metrics(portfolio_data)

        # Render HTML
        html = self._render_html(portfolio_data, metrics)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✅ Dashboard generated: {output_path}")

        # Open in browser
        webbrowser.open(f'file://{os.path.abspath(output_path)}')
        print(f"🌐 Opening dashboard in browser...")

        return output_path

    def _fetch_portfolio_data(self, portfolio_id: int) -> Dict:
        """Fetch all portfolio data with scores"""
        holdings = self.portfolio_manager.list_holdings(portfolio_id, with_current_price=True)

        # Get latest scores for all tickers
        tickers = [h['ticker'] for h in holdings]
        scores = self.portfolio_manager.get_latest_scores(tickers)

        # Merge scores into holdings
        for holding in holdings:
            ticker = holding['ticker']
            score = scores.get(ticker)
            if score:
                holding['score'] = {
                    'total': score.total_score,
                    'financial': score.financial_score,
                    'valuation': score.valuation_score,
                    'momentum': score.momentum_score,
                    'grade': self._get_grade(score.total_score)
                }
            else:
                holding['score'] = None

        return {
            'portfolio_id': portfolio_id,
            'holdings': holdings,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _calculate_metrics(self, portfolio_data: Dict) -> Dict:
        """Calculate portfolio-level metrics"""
        holdings = portfolio_data['holdings']

        total_value = sum(h.get('current_value', 0) for h in holdings)
        total_cost = sum(h.get('cost_basis', 0) for h in holdings)
        total_pnl = total_value - total_cost
        total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0

        # Calculate weighted average score
        scored_holdings = [h for h in holdings if h.get('score') is not None and 'current_value' in h]
        if scored_holdings:
            weighted_score = sum(
                h['score']['total'] * h['current_value']
                for h in scored_holdings
            ) / sum(h['current_value'] for h in scored_holdings)
        else:
            weighted_score = 0

        # Sector allocation
        sector_allocation = self._calculate_sector_allocation(holdings)

        # Score distribution
        score_distribution = self._calculate_score_distribution(holdings)

        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'num_holdings': len(holdings),
            'weighted_avg_score': weighted_score,
            'sector_allocation': sector_allocation,
            'score_distribution': score_distribution
        }

    def _calculate_sector_allocation(self, holdings: List[Dict]) -> Dict:
        """Calculate sector allocation percentages"""
        sector_values = {}
        total_value = sum(h.get('current_value', 0) for h in holdings)

        for holding in holdings:
            sector = holding.get('sector', 'Unknown')
            current_value = holding.get('current_value', 0)

            if sector not in sector_values:
                sector_values[sector] = 0
            sector_values[sector] += current_value

        # Convert to percentages
        sector_percentages = {
            sector: (value / total_value * 100) if total_value > 0 else 0
            for sector, value in sector_values.items()
        }

        return sector_percentages

    def _calculate_score_distribution(self, holdings: List[Dict]) -> Dict:
        """Calculate score distribution counts"""
        distribution = {
            'excellent': 0,  # 9-10
            'good': 0,       # 7-8.99
            'fair': 0,       # 5-6.99
            'weak': 0,       # 0-4.99
            'unscored': 0
        }

        for holding in holdings:
            score = holding.get('score')
            if score is None:
                distribution['unscored'] += 1
            else:
                total_score = score['total']
                if total_score >= 9:
                    distribution['excellent'] += 1
                elif total_score >= 7:
                    distribution['good'] += 1
                elif total_score >= 5:
                    distribution['fair'] += 1
                else:
                    distribution['weak'] += 1

        return distribution

    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 9.5:
            return "A+"
        elif score >= 9:
            return "A"
        elif score >= 8.5:
            return "A-"
        elif score >= 8:
            return "B+"
        elif score >= 7:
            return "B"
        elif score >= 6:
            return "B-"
        elif score >= 5:
            return "C+"
        elif score >= 4:
            return "C"
        elif score >= 3:
            return "D"
        else:
            return "F"

    def _render_html(self, portfolio_data: Dict, metrics: Dict) -> str:
        """Render HTML dashboard"""
        holdings = portfolio_data['holdings']

        # Generate holdings table rows
        holdings_rows = self._generate_holdings_table(holdings)

        # Prepare chart data
        sector_data = self._prepare_sector_chart_data(metrics['sector_allocation'])
        score_data = self._prepare_score_chart_data(metrics['score_distribution'])
        pnl_data = self._prepare_pnl_chart_data(holdings)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Copilot - Portfolio Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #fff1e5;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2em;
        }}

        .timestamp {{
            color: #7f8c8d;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}

        .card {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .card h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}

        .summary-item {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        .summary-label {{
            font-size: 0.85em;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .summary-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2c3e50;
        }}

        .positive {{
            color: #27ae60;
        }}

        .negative {{
            color: #e74c3c;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .score-excellent {{
            color: #27ae60;
            font-weight: bold;
        }}

        .score-good {{
            color: #16a085;
            font-weight: bold;
        }}

        .score-fair {{
            color: #f39c12;
            font-weight: bold;
        }}

        .score-weak {{
            color: #e74c3c;
            font-weight: bold;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}

        .chart-container {{
            position: relative;
            height: 300px;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}

        .ticker {{
            font-weight: bold;
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Portfolio Dashboard</h1>
        <div class="timestamp">Generated: {portfolio_data['generated_at']}</div>

        <!-- Portfolio Summary -->
        <div class="card">
            <h2>Portfolio Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-label">Total Value</div>
                    <div class="summary-value">${metrics['total_value']:,.2f}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Total Cost</div>
                    <div class="summary-value">${metrics['total_cost']:,.2f}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Total P&L</div>
                    <div class="summary-value {'positive' if metrics['total_pnl'] >= 0 else 'negative'}">
                        {'+' if metrics['total_pnl'] >= 0 else ''}{metrics['total_pnl_pct']:.2f}%
                    </div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Avg Score</div>
                    <div class="summary-value">{metrics['weighted_avg_score']:.1f}/10</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Holdings</div>
                    <div class="summary-value">{metrics['num_holdings']}</div>
                </div>
            </div>
        </div>

        <!-- Holdings Table -->
        <div class="card">
            <h2>Holdings</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Shares</th>
                        <th>Avg Cost</th>
                        <th>Current Price</th>
                        <th>Market Value</th>
                        <th>P&L %</th>
                        <th>Score</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
                    {holdings_rows}
                </tbody>
            </table>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <div class="card">
                <h2>Sector Allocation</h2>
                <div class="chart-container">
                    <canvas id="sector-chart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Score Distribution</h2>
                <div class="chart-container">
                    <canvas id="score-chart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>P&L by Holding</h2>
                <div class="chart-container">
                    <canvas id="pnl-chart"></canvas>
                </div>
            </div>
        </div>

        <div class="footer">
            Portfolio Copilot Dashboard | <a href="https://github.com/anthropics/claude-code" target="_blank">Built with Claude Code</a>
        </div>
    </div>

    <script>
        // Sector Allocation Pie Chart
        const sectorCtx = document.getElementById('sector-chart').getContext('2d');
        new Chart(sectorCtx, {{
            type: 'pie',
            data: {sector_data},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'right'
                    }},
                    title: {{
                        display: false
                    }}
                }}
            }}
        }});

        // Score Distribution Bar Chart
        const scoreCtx = document.getElementById('score-chart').getContext('2d');
        new Chart(scoreCtx, {{
            type: 'bar',
            data: {score_data},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});

        // P&L Bar Chart
        const pnlCtx = document.getElementById('pnl-chart').getContext('2d');
        new Chart(pnlCtx, {{
            type: 'bar',
            data: {pnl_data},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        return html

    def _generate_holdings_table(self, holdings: List[Dict]) -> str:
        """Generate HTML table rows for holdings"""
        rows = []

        for holding in holdings:
            score = holding.get('score')
            pnl_pct = holding.get('pnl_pct', 0)
            pnl_class = 'positive' if pnl_pct >= 0 else 'negative'

            if score:
                score_class = self._get_score_class(score['total'])
                score_text = f"{score['total']:.1f}"
                grade_text = score['grade']
            else:
                score_class = ''
                score_text = 'N/A'
                grade_text = 'N/A'

            row = f"""                    <tr>
                        <td class="ticker">{holding['ticker']}</td>
                        <td>{holding.get('quantity', 0):.2f}</td>
                        <td>${holding.get('avg_price', 0):.2f}</td>
                        <td>${holding.get('current_price', 0):.2f}</td>
                        <td>${holding.get('current_value', 0):,.2f}</td>
                        <td class="{pnl_class}">{'+' if pnl_pct >= 0 else ''}{pnl_pct:.2f}%</td>
                        <td class="{score_class}">{score_text}</td>
                        <td class="{score_class}">{grade_text}</td>
                    </tr>"""
            rows.append(row)

        return '\n'.join(rows)

    def _get_score_class(self, score: float) -> str:
        """Get CSS class for score"""
        if score >= 9:
            return 'score-excellent'
        elif score >= 7:
            return 'score-good'
        elif score >= 5:
            return 'score-fair'
        else:
            return 'score-weak'

    def _prepare_sector_chart_data(self, sector_allocation: Dict) -> str:
        """Prepare Chart.js data for sector allocation pie chart"""
        labels = list(sector_allocation.keys())
        data = [round(v, 1) for v in sector_allocation.values()]

        # Color palette
        colors = [
            '#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6',
            '#1abc9c', '#34495e', '#16a085', '#27ae60', '#2980b9'
        ]

        chart_data = {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': colors[:len(labels)],
                'borderWidth': 2,
                'borderColor': '#fff'
            }]
        }

        return json.dumps(chart_data)

    def _prepare_score_chart_data(self, score_distribution: Dict) -> str:
        """Prepare Chart.js data for score distribution bar chart"""
        labels = ['Excellent\n(9-10)', 'Good\n(7-9)', 'Fair\n(5-7)', 'Weak\n(<5)']
        data = [
            score_distribution['excellent'],
            score_distribution['good'],
            score_distribution['fair'],
            score_distribution['weak']
        ]

        colors = ['#27ae60', '#16a085', '#f39c12', '#e74c3c']

        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': 'Number of Holdings',
                'data': data,
                'backgroundColor': colors,
                'borderWidth': 0
            }]
        }

        return json.dumps(chart_data)

    def _prepare_pnl_chart_data(self, holdings: List[Dict]) -> str:
        """Prepare Chart.js data for P&L bar chart"""
        labels = [h['ticker'] for h in holdings]
        data = [round(h.get('pnl_pct', 0), 2) for h in holdings]

        # Color based on positive/negative
        colors = ['#27ae60' if d >= 0 else '#e74c3c' for d in data]

        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': 'P&L %',
                'data': data,
                'backgroundColor': colors,
                'borderWidth': 0
            }]
        }

        return json.dumps(chart_data)


def main():
    """CLI entry point"""
    import sys

    portfolio_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    generator = PortfolioDashboardGenerator()
    output_path = generator.generate_dashboard(portfolio_id)

    print(f"\n✅ Dashboard ready at: {output_path}")


if __name__ == '__main__':
    main()
