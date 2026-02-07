#!/usr/bin/env python3
"""
Market Pulse HTML Dashboard Generator
Generates interactive HTML dashboard with Chart.js visualizations
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def generate_html(data: Dict[str, Any], output_path: str = None) -> str:
    """Generate HTML dashboard from market data JSON."""

    if output_path is None:
        output_path = f"/tmp/market-pulse-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Pulse Dashboard - {datetime.now().strftime('%Y-%m-%d')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        /* Classic Newspaper Style - Financial Times Inspired */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Georgia, 'Times New Roman', Times, serif;
            background: #e8e4db;
            color: #2c2c2c;
            padding: 20px;
            line-height: 1.7;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #faf8f3;
            box-shadow: 0 0 30px rgba(0,0,0,0.2);
            border: 1px solid #d4cfc3;
        }}

        /* Masthead - Newspaper Header */
        header {{
            background: #faf8f3;
            color: #2c2c2c;
            padding: 40px 60px 30px;
            border-bottom: 4px double #2c2c2c;
            text-align: center;
        }}

        h1 {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 4em;
            font-weight: 900;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
            text-transform: uppercase;
            color: #1a1a1a;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.1);
        }}

        .masthead-subtitle {{
            font-family: Georgia, serif;
            font-size: 0.9em;
            font-style: italic;
            color: #666;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
        }}

        .timestamp {{
            font-family: Georgia, serif;
            font-size: 0.85em;
            color: #666;
            border-top: 1px solid #d4cfc3;
            border-bottom: 1px solid #d4cfc3;
            padding: 8px 0;
            margin-top: 12px;
        }}

        .status-bar {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 12px;
            font-size: 0.85em;
        }}

        .status-item {{
            font-weight: 600;
        }}

        .status-badge {{
            display: inline-block;
            padding: 2px 8px;
            border: 1px solid #2c2c2c;
            font-size: 0.9em;
            font-weight: 700;
            font-family: Arial, sans-serif;
        }}

        .badge-open {{
            background: #2c2c2c;
            color: #faf8f3;
        }}

        .badge-closed {{
            background: #faf8f3;
            color: #2c2c2c;
        }}

        /* Content Area */
        .content {{
            padding: 40px 60px;
        }}

        h2 {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 2.2em;
            font-weight: 900;
            margin: 30px 0 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #2c2c2c;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        /* Column Layout */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}

        .card {{
            background: #faf8f3;
            padding: 20px;
            border: 2px solid #2c2c2c;
            border-radius: 0;
        }}

        .card-title {{
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 16px;
            color: #1a1a1a;
            border-bottom: 2px solid #d4cfc3;
            padding-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .chart-container {{
            position: relative;
            height: 280px;
            margin-bottom: 16px;
            background: white;
            border: 1px solid #d4cfc3;
            padding: 10px;
        }}

        /* Tables - Newspaper Style */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
            margin: 16px 0;
            background: white;
        }}

        th {{
            text-align: left;
            padding: 10px 12px;
            background: #2c2c2c;
            color: #faf8f3;
            font-weight: 700;
            border: 1px solid #2c2c2c;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 10px 12px;
            border: 1px solid #d4cfc3;
            background: #faf8f3;
        }}

        tr:nth-child(even) td {{
            background: #f5f3ed;
        }}

        .positive {{
            color: #2c5f2d;
            font-weight: 700;
        }}

        .positive::before {{
            content: "▲ ";
        }}

        .negative {{
            color: #8b1e3f;
            font-weight: 700;
        }}

        .negative::before {{
            content: "▼ ";
        }}

        .neutral {{
            color: #666;
        }}

        /* Metrics Display */
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px dotted #d4cfc3;
        }}

        .metric:last-child {{
            border-bottom: none;
        }}

        .metric-label {{
            font-weight: 600;
            color: #4a4a4a;
        }}

        .metric-value {{
            font-weight: 700;
            font-size: 1.1em;
            font-family: 'Courier New', monospace;
        }}

        /* Sources Section */
        .sources {{
            background: #f5f3ed;
            padding: 40px 60px;
            border-top: 4px double #2c2c2c;
        }}

        .sources h2 {{
            font-size: 1.6em;
            margin-bottom: 20px;
        }}

        .source-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}

        .source-card {{
            background: #faf8f3;
            padding: 16px;
            border: 1px solid #d4cfc3;
        }}

        .source-provider {{
            font-weight: 700;
            font-size: 1.05em;
            color: #1a1a1a;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .source-link {{
            color: #2c2c2c;
            text-decoration: underline;
            font-size: 0.9em;
            display: inline-block;
            margin-top: 8px;
        }}

        .source-link:hover {{
            color: #666;
        }}

        .source-types {{
            color: #666;
            font-size: 0.85em;
            margin-top: 8px;
            font-style: italic;
        }}

        .disclaimer {{
            background: #fff9e6;
            padding: 16px;
            margin-top: 20px;
            border: 2px solid #2c2c2c;
            border-left: 6px solid #2c2c2c;
            font-size: 0.85em;
            color: #4a4a4a;
        }}

        footer {{
            text-align: center;
            padding: 24px;
            background: #2c2c2c;
            color: #faf8f3;
            font-size: 0.85em;
            border-top: 4px double #2c2c2c;
        }}

        /* Horizontal Rule */
        hr {{
            border: none;
            border-top: 2px solid #2c2c2c;
            margin: 30px 0;
        }}

        /* Mobile Responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .content {{
                padding: 20px 30px;
            }}

            header {{
                padding: 20px 30px;
            }}

            h1 {{
                font-size: 2.5em;
            }}

            h2 {{
                font-size: 1.6em;
            }}

            .grid {{
                grid-template-columns: 1fr;
            }}

            .sources {{
                padding: 20px 30px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>MARKET PULSE</h1>
            <div class="masthead-subtitle">Global Financial Markets Daily</div>
            <div class="timestamp">
                {datetime.now().strftime('%A, %B %d, %Y')} | Generated at {datetime.now().strftime('%H:%M')} KST
            </div>
            <div class="status-bar">
                <div class="status-item">
                    US Markets:
                    <span class="status-badge {'badge-open' if data.get('market_status', {}).get('us_open') else 'badge-closed'}">
                        {'OPEN' if data.get('market_status', {}).get('us_open') else 'CLOSED'}
                    </span>
                </div>
                <div class="status-item">
                    Korean Markets:
                    <span class="status-badge {'badge-open' if data.get('market_status', {}).get('kr_open') else 'badge-closed'}">
                        {'OPEN' if data.get('market_status', {}).get('kr_open') else 'CLOSED'}
                    </span>
                </div>
            </div>
        </header>

        <div class="content">
            {_generate_analysis_section(data)}
            <hr style="margin: 40px 0; border-top: 3px double #2c2c2c;">
            {_generate_us_section(data)}
            {_generate_kr_section(data)}
            {_generate_macro_section(data)}
            {_generate_crypto_section(data)}
        </div>

        {_generate_sources_section(data)}

        <footer>
            <strong>⚖️ Disclaimer:</strong> This analysis is for informational purposes only and does not constitute financial advice.
            All data is provided as-is from free public sources. Investment decisions are your own responsibility.
        </footer>
    </div>

    {_generate_charts_js(data)}
</body>
</html>"""

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


def _generate_analysis_section(data: Dict) -> str:
    """Generate AI analysis section - newspaper article style."""
    analysis = data.get('analysis', {})

    if not analysis:
        return ""

    synthesis = analysis.get('synthesis', '')
    us_analysis = analysis.get('us_market', '')
    kr_analysis = analysis.get('kr_market', '')
    crypto_analysis = analysis.get('crypto_macro', '')

    # Convert markdown to HTML paragraphs
    def format_text(text):
        if not text:
            return ""
        # Simple markdown to HTML conversion
        lines = text.split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                continue

            # Headers
            if line.startswith('### '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h3 style="font-size: 1.3em; margin: 20px 0 10px; font-weight: 700;">{line[4:]}</h3>')
            elif line.startswith('## '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h2 style="font-size: 1.6em; margin: 30px 0 15px; font-weight: 900; border-bottom: 2px solid #2c2c2c; padding-bottom: 8px;">{line[3:]}</h2>')
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                if not in_list:
                    html_lines.append('<ul style="margin: 10px 0 10px 30px; line-height: 1.8;">')
                    in_list = True
                html_lines.append(f'<li>{line[2:]}</li>')
            # Bold
            elif '**' in line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                line = line.replace('**', '<strong>').replace('**', '</strong>')
                html_lines.append(f'<p style="margin: 15px 0; text-align: justify; text-indent: 2em;">{line}</p>')
            # Regular paragraph
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<p style="margin: 15px 0; text-align: justify; text-indent: 2em;">{line}</p>')

        if in_list:
            html_lines.append('</ul>')

        return '\n'.join(html_lines)

    return f"""
    <div style="margin-bottom: 40px;">
        <h2 style="font-size: 2.5em; text-align: center; margin-bottom: 30px; border-bottom: 4px double #2c2c2c; padding-bottom: 15px; letter-spacing: 0.05em;">
            MARKET ANALYSIS
        </h2>

        <!-- Lead Story: Synthesis -->
        <div style="border: 3px solid #2c2c2c; padding: 24px; margin-bottom: 30px; background: white;">
            <h3 style="font-size: 1.8em; font-weight: 900; margin-bottom: 16px; text-transform: uppercase;">
                Today's Market Overview
            </h3>
            {format_text(synthesis)}
        </div>

        <!-- Three Column Layout -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">

            <!-- US Market Analysis -->
            <div style="border: 2px solid #2c2c2c; padding: 20px; background: #faf8f3;">
                <h3 style="font-size: 1.4em; font-weight: 900; margin-bottom: 12px; border-bottom: 2px solid #2c2c2c; padding-bottom: 8px; text-transform: uppercase;">
                    🇺🇸 US Markets
                </h3>
                {format_text(us_analysis)}
            </div>

            <!-- Korean Market Analysis -->
            <div style="border: 2px solid #2c2c2c; padding: 20px; background: #faf8f3;">
                <h3 style="font-size: 1.4em; font-weight: 900; margin-bottom: 12px; border-bottom: 2px solid #2c2c2c; padding-bottom: 8px; text-transform: uppercase;">
                    🇰🇷 Korean Markets
                </h3>
                {format_text(kr_analysis)}
            </div>

            <!-- Crypto & Macro Analysis -->
            <div style="border: 2px solid #2c2c2c; padding: 20px; background: #faf8f3;">
                <h3 style="font-size: 1.4em; font-weight: 900; margin-bottom: 12px; border-bottom: 2px solid #2c2c2c; padding-bottom: 8px; text-transform: uppercase;">
                    🌍 Global Macro & Crypto
                </h3>
                {format_text(crypto_analysis)}
            </div>

        </div>
    </div>
    """


def _generate_us_section(data: Dict) -> str:
    """Generate US market section."""
    us_data = data.get('data', {})
    indices = us_data.get('us_indices', {})
    sectors = us_data.get('us_sectors', [])
    vix = us_data.get('vix', {})

    if not indices:
        return ""

    # Indices table
    indices_rows = ""
    for symbol, info in indices.items():
        if 'error' in info:
            continue
        change_class = 'positive' if info.get('change_pct', 0) > 0 else 'negative' if info.get('change_pct', 0) < 0 else 'neutral'
        indices_rows += f"""
        <tr>
            <td><strong>{info.get('name', symbol)}</strong></td>
            <td>{info.get('value', 'N/A'):,.2f}</td>
            <td class="{change_class}">{info.get('change', 0):+.2f}</td>
            <td class="{change_class}">{info.get('change_pct', 0):+.2f}%</td>
        </tr>
        """

    # Sectors chart data
    sectors_labels = [s['name'] for s in sectors]
    sectors_1d = [s['change_1d'] for s in sectors]

    return f"""
    <h2 style="font-size: 2em; margin-bottom: 20px; color: #1f2937;">🇺🇸 US Market</h2>

    <div class="grid">
        <div class="card">
            <div class="card-title">📈 Major Indices</div>
            <table>
                <thead>
                    <tr>
                        <th>Index</th>
                        <th>Value</th>
                        <th>Change</th>
                        <th>Change %</th>
                    </tr>
                </thead>
                <tbody>
                    {indices_rows}
                </tbody>
            </table>

            <div class="metric" style="margin-top: 16px; border-top: 2px solid #e5e7eb; padding-top: 16px;">
                <span class="metric-label">VIX (Volatility)</span>
                <span class="metric-value {'positive' if vix.get('change_pct', 0) < 0 else 'negative'}">
                    {vix.get('value', 0):.2f} ({vix.get('change_pct', 0):+.2f}%)
                </span>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🏭 Sector Performance (1D)</div>
            <div class="chart-container">
                <canvas id="sectorChart"></canvas>
            </div>
        </div>
    </div>
    """


def _generate_kr_section(data: Dict) -> str:
    """Generate Korean market section."""
    kr_data = data.get('data', {})
    indices = kr_data.get('kr_indices', {})
    flows = kr_data.get('kr_foreign_institutional', {})
    top_stocks = kr_data.get('kr_top_stocks', [])[:5]  # Top 5

    if not indices:
        return ""

    # Indices metrics
    kospi = indices.get('kospi', {})
    kosdaq = indices.get('kosdaq', {})

    # Top stocks table
    stocks_rows = ""
    for stock in top_stocks:
        change_class = 'positive' if stock.get('change_pct', 0) > 0 else 'negative' if stock.get('change_pct', 0) < 0 else 'neutral'
        stocks_rows += f"""
        <tr>
            <td><strong>{stock.get('name', '')}</strong><br><small>{stock.get('ticker', '')}</small></td>
            <td>{stock.get('price', 0):,}원</td>
            <td class="{change_class}">{stock.get('change_pct', 0):+.2f}%</td>
            <td>{stock.get('per', 'N/A') if stock.get('per') else 'N/A'}</td>
        </tr>
        """

    foreign_mb = flows.get('foreign_net_buy', 0) / 100_000_000  # Convert to 억
    institutional_mb = flows.get('institutional_net_buy', 0) / 100_000_000
    individual_mb = flows.get('individual_net_buy', 0) / 100_000_000

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px; color: #1f2937;">🇰🇷 Korean Market</h2>

    <div class="grid">
        <div class="card">
            <div class="card-title">📊 Indices</div>
            <div class="metric">
                <span class="metric-label">KOSPI</span>
                <span class="metric-value {'positive' if kospi.get('change_pct', 0) > 0 else 'negative'}">
                    {kospi.get('value', 0):,.2f} ({kospi.get('change_pct', 0):+.2f}%)
                </span>
            </div>
            <div class="metric">
                <span class="metric-label">KOSDAQ</span>
                <span class="metric-value {'positive' if kosdaq.get('change_pct', 0) > 0 else 'negative'}">
                    {kosdaq.get('value', 0):,.2f} ({kosdaq.get('change_pct', 0):+.2f}%)
                </span>
            </div>
        </div>

        <div class="card">
            <div class="card-title">💰 Trading Flows (억원)</div>
            <div class="metric">
                <span class="metric-label">외국인</span>
                <span class="metric-value {'positive' if foreign_mb > 0 else 'negative'}">
                    {foreign_mb:+,.0f}억
                </span>
            </div>
            <div class="metric">
                <span class="metric-label">기관</span>
                <span class="metric-value {'positive' if institutional_mb > 0 else 'negative'}">
                    {institutional_mb:+,.0f}억
                </span>
            </div>
            <div class="metric">
                <span class="metric-label">개인</span>
                <span class="metric-value {'positive' if individual_mb > 0 else 'negative'}">
                    {individual_mb:+,.0f}억
                </span>
            </div>
        </div>

        <div class="card" style="grid-column: span 2;">
            <div class="card-title">🏢 Top Stocks by Market Cap</div>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Change %</th>
                        <th>PER</th>
                    </tr>
                </thead>
                <tbody>
                    {stocks_rows}
                </tbody>
            </table>
        </div>
    </div>
    """


def _generate_macro_section(data: Dict) -> str:
    """Generate global macro section."""
    macro_data = data.get('data', {})
    yields = macro_data.get('treasury_yields', {})
    commodities = macro_data.get('commodities', {})
    currencies = macro_data.get('currencies', {})

    if not yields and not commodities:
        return ""

    # Commodities rows
    commodity_rows = ""
    for name, info in commodities.items():
        change_class = 'positive' if info.get('change_pct', 0) > 0 else 'negative' if info.get('change_pct', 0) < 0 else 'neutral'
        commodity_rows += f"""
        <div class="metric">
            <span class="metric-label">{name}</span>
            <span class="metric-value {change_class}">
                ${info.get('price', 0):,.2f} ({info.get('change_pct', 0):+.2f}%)
            </span>
        </div>
        """

    # Currencies rows
    currency_rows = ""
    for name, info in currencies.items():
        change_class = 'positive' if info.get('change_pct', 0) > 0 else 'negative' if info.get('change_pct', 0) < 0 else 'neutral'
        currency_rows += f"""
        <div class="metric">
            <span class="metric-label">{name}</span>
            <span class="metric-value {change_class}">
                {info.get('value', 0):,.2f} ({info.get('change_pct', 0):+.2f}%)
            </span>
        </div>
        """

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px; color: #1f2937;">🌍 Global Macro</h2>

    <div class="grid">
        <div class="card">
            <div class="card-title">📈 Treasury Yields</div>
            <div class="metric">
                <span class="metric-label">5-Year</span>
                <span class="metric-value">{yields.get('5-Year', 0):.3f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">10-Year</span>
                <span class="metric-value">{yields.get('10-Year', 0):.3f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">30-Year</span>
                <span class="metric-value">{yields.get('30-Year', 0):.3f}%</span>
            </div>
            <div class="metric" style="border-top: 2px solid #e5e7eb; margin-top: 8px; padding-top: 8px;">
                <span class="metric-label">10Y-5Y Spread</span>
                <span class="metric-value">{yields.get('spread_10y_5y', 0):.3f}%</span>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🛢️ Commodities</div>
            {commodity_rows}
        </div>

        <div class="card">
            <div class="card-title">💱 Currencies</div>
            {currency_rows}
        </div>
    </div>
    """


def _generate_crypto_section(data: Dict) -> str:
    """Generate crypto section."""
    crypto_data = data.get('data', {}).get('crypto', [])

    if not crypto_data:
        return ""

    crypto_rows = ""
    for coin in crypto_data:
        change_class = 'positive' if coin.get('change_pct', 0) > 0 else 'negative' if coin.get('change_pct', 0) < 0 else 'neutral'
        crypto_rows += f"""
        <tr>
            <td><strong>{coin.get('name', '')}</strong><br><small>{coin.get('symbol', '')}</small></td>
            <td>${coin.get('price', 0):,.2f}</td>
            <td class="{change_class}">{coin.get('change_pct', 0):+.2f}%</td>
        </tr>
        """

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px; color: #1f2937;">₿ Cryptocurrency</h2>

    <div class="grid">
        <div class="card" style="grid-column: span 2;">
            <div class="card-title">💎 Major Coins (24h)</div>
            <table>
                <thead>
                    <tr>
                        <th>Coin</th>
                        <th>Price</th>
                        <th>24h Change</th>
                    </tr>
                </thead>
                <tbody>
                    {crypto_rows}
                </tbody>
            </table>
        </div>
    </div>
    """


def _generate_sources_section(data: Dict) -> str:
    """Generate data sources section."""
    sources = data.get('sources', {})

    if not sources:
        return ""

    source_cards = ""
    for key, info in sources.items():
        if key == 'disclaimer':
            continue
        if not isinstance(info, dict):
            continue

        data_types = ', '.join(info.get('data_types', []))
        source_cards += f"""
        <div class="source-card">
            <div class="source-provider">{info.get('provider', '')}</div>
            <div>Library: <code>{info.get('library', '')}</code></div>
            <a href="{info.get('url', '#')}" target="_blank" class="source-link">
                🔗 Visit {info.get('provider', '')}
            </a>
            {f'<div class="source-types">Data: {data_types}</div>' if data_types else ''}
        </div>
        """

    disclaimer = sources.get('disclaimer', '')

    return f"""
    <div class="sources">
        <h2>📚 Data Sources</h2>
        <div class="source-grid">
            {source_cards}
        </div>
        {f'<div class="disclaimer"><strong>ℹ️ Note:</strong> {disclaimer}</div>' if disclaimer else ''}
    </div>
    """


def _generate_charts_js(data: Dict) -> str:
    """Generate Chart.js initialization scripts - Newspaper style (minimal color)."""
    sectors = data.get('data', {}).get('us_sectors', [])

    if not sectors:
        return ""

    labels = [s['name'] for s in sectors]
    values = [s['change_1d'] for s in sectors]
    # Newspaper style: black for positive, gray for negative
    colors = ['#2c2c2c' if v > 0 else '#999999' if v < 0 else '#cccccc' for v in values]
    border_colors = ['#000000' if v > 0 else '#666666' if v < 0 else '#999999' for v in values]

    return f"""
    <script>
        // Sector Performance Chart - Newspaper Style
        const sectorCtx = document.getElementById('sectorChart');
        if (sectorCtx) {{
            new Chart(sectorCtx, {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(labels)},
                    datasets: [{{
                        label: '1-Day Performance (%)',
                        data: {json.dumps(values)},
                        backgroundColor: {json.dumps(colors)},
                        borderColor: {json.dumps(border_colors)},
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            backgroundColor: '#2c2c2c',
                            titleColor: '#faf8f3',
                            bodyColor: '#faf8f3',
                            borderColor: '#000',
                            borderWidth: 1
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            grid: {{
                                color: '#d4cfc3',
                                lineWidth: 1
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 11
                                }},
                                callback: function(value) {{
                                    return value + '%';
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 10
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
    """


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Market Pulse HTML Dashboard")
    parser.add_argument('--input', type=str, help='Input JSON file path')
    parser.add_argument('--output', type=str, help='Output HTML file path')

    args = parser.parse_args()

    # Read JSON data
    if args.input:
        with open(args.input, 'r') as f:
            data = json.load(f)
    else:
        # Read from stdin
        data = json.load(sys.stdin)

    # Generate HTML
    output_path = generate_html(data, args.output)
    print(output_path)


if __name__ == '__main__':
    main()
