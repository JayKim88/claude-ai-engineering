"""
All-in-One Portfolio Analysis Script.

Combines all Portfolio Copilot features into a comprehensive analysis:
- Sprint 1: Tax optimization (tax-loss harvesting, dividend tracking)
- Sprint 2: Performance analysis (TWR, MWR, benchmark comparison)
- Sprint 3: Risk management (VaR, correlation, diversification)
- Sprint 4: Fundamental analysis (scorecard, data quality)
- Sprint 5: Rebalancing recommendations

Usage:
    python3 all_in_one_analysis.py <portfolio_id> [--html]
"""

import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, List
import os

# Import all analysis modules
from tax_loss_harvester import TaxLossHarvester
from tax_calculator import TaxCalculator
from dividend_tracker import DividendTracker
from benchmark_analyzer import BenchmarkAnalyzer
from performance_calculator import PerformanceCalculator
from risk_metrics import RiskAnalyzer
from rebalance_engine import RebalanceEngine
from scorecard import CompanyScorecardGenerator
from database import get_database, Holding


class PortfolioCopilot:
    """Comprehensive portfolio analysis orchestrator."""

    def __init__(self, portfolio_id: int, db_path: str = None):
        """Initialize all analysis modules."""
        self.portfolio_id = portfolio_id
        self.db = get_database(db_path)
        self.session = self.db.get_session()

        # Initialize analyzers
        self.tax_harvester = TaxLossHarvester(db_path)
        self.tax_calculator = TaxCalculator(db_path)
        self.dividend_tracker = DividendTracker(db_path)
        self.benchmark_analyzer = BenchmarkAnalyzer(db_path)
        self.performance_calculator = PerformanceCalculator(db_path)
        self.risk_analyzer = RiskAnalyzer(db_path)
        self.rebalance_engine = RebalanceEngine(db_path)
        self.scorecard_generator = CompanyScorecardGenerator()

    def get_portfolio_summary(self) -> Dict:
        """Get basic portfolio information."""
        holdings = self.session.query(Holding).filter_by(portfolio_id=self.portfolio_id).all()

        total_value = 0.0
        total_cost = 0.0
        num_holdings = len(holdings)

        for holding in holdings:
            from data_fetcher import get_stock_data
            stock_data = get_stock_data(holding.ticker, holding.market)
            current_price = stock_data.get('current_price', holding.avg_price) if stock_data else holding.avg_price

            position_value = current_price * holding.quantity
            position_cost = holding.avg_price * holding.quantity

            total_value += position_value
            total_cost += position_cost

        unrealized_pnl = total_value - total_cost
        unrealized_pnl_pct = (unrealized_pnl / total_cost * 100) if total_cost > 0 else 0

        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'unrealized_pnl': unrealized_pnl,
            'unrealized_pnl_pct': unrealized_pnl_pct,
            'num_holdings': num_holdings
        }

    def run_comprehensive_analysis(self) -> Dict:
        """
        Run all analyses and return comprehensive results.

        Returns:
            Dictionary with all analysis results
        """
        results = {}

        print("🔍 Running comprehensive portfolio analysis...")
        print("=" * 80)

        # Portfolio Summary
        print("\n📊 Portfolio Summary...")
        results['summary'] = self.get_portfolio_summary()

        # Sprint 1: Tax Optimization
        print("💰 Tax Optimization Analysis...")
        results['tax_harvesting'] = self.tax_harvester.find_harvest_opportunities(
            self.portfolio_id,
            min_loss_threshold=500
        )
        results['tax_report'] = self.tax_calculator.calculate_annual_tax(
            self.portfolio_id,
            datetime.now().year
        )
        results['dividends'] = self.dividend_tracker.calculate_dividend_yields(self.portfolio_id)

        # Sprint 2: Performance Analysis
        print("📈 Performance Analysis...")
        results['benchmark_spy'] = self.benchmark_analyzer.compare_to_benchmark(
            self.portfolio_id,
            'SPY',
            days=365
        )
        results['performance'] = self.performance_calculator.calculate_performance_metrics(
            self.portfolio_id,
            start_date=datetime.now().date() - timedelta(days=365),
            end_date=datetime.now().date()
        )

        # Sprint 3: Risk Management
        print("⚠️  Risk Analysis...")
        results['var_analysis'] = self.risk_analyzer.calculate_var(
            self.portfolio_id,
            confidence=0.95,
            horizon_days=1
        )
        results['correlation'] = self.risk_analyzer.analyze_correlation_risk(self.portfolio_id)
        results['risk_warnings'] = self.risk_analyzer.generate_risk_warnings(self.portfolio_id)

        # Sprint 4: Rebalancing
        print("🔄 Rebalancing Analysis...")
        results['rebalancing'] = self.rebalance_engine.analyze_rebalancing(self.portfolio_id)

        print("✅ Analysis complete!\n")

        return results

    def generate_text_report(self, results: Dict) -> str:
        """Generate comprehensive text report."""
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("📋 PORTFOLIO COPILOT - COMPREHENSIVE ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {self.portfolio_id}")
        lines.append("")

        # Executive Summary
        summary = results['summary']
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Value:           ${summary['total_value']:>15,.2f}")
        lines.append(f"Total Cost:            ${summary['total_cost']:>15,.2f}")
        lines.append(f"Unrealized P&L:        ${summary['unrealized_pnl']:>15,.2f} ({summary['unrealized_pnl_pct']:+.2f}%)")
        lines.append(f"Number of Holdings:    {summary['num_holdings']:>15}")
        lines.append("")

        # Performance Overview
        perf = results['performance']
        lines.append("📈 PERFORMANCE OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"Time-Weighted Return:  {perf['twr']*100:>15.2f}%")
        lines.append(f"Sharpe Ratio:          {perf['sharpe_ratio']:>15.2f}")
        lines.append(f"Sortino Ratio:         {perf['sortino_ratio']:>15.2f}")
        lines.append(f"Max Drawdown:          {perf['max_drawdown']*100:>15.2f}%")
        lines.append(f"Volatility (Ann.):     {perf['volatility']*100:>15.2f}%")
        lines.append("")

        # Benchmark Comparison
        bench = results['benchmark_spy']
        lines.append("📊 BENCHMARK COMPARISON (vs S&P 500)")
        lines.append("-" * 80)
        lines.append(f"Portfolio Return:      {bench['portfolio_return']*100:>15.2f}%")
        lines.append(f"S&P 500 Return:        {bench['benchmark_return']*100:>15.2f}%")
        lines.append(f"Excess Return:         {bench['excess_return']*100:>15.2f}%")
        lines.append(f"Alpha:                 {bench['alpha']*100:>15.2f}%")
        lines.append(f"Beta:                  {bench['beta']:>15.2f}")
        lines.append(f"Information Ratio:     {bench['information_ratio']:>15.2f}")
        lines.append("")

        # Risk Metrics
        var = results['var_analysis']
        lines.append("⚠️  RISK METRICS")
        lines.append("-" * 80)
        lines.append(f"VaR (95%, 1-day):      ${var['var_95_amount']:>15,.2f} ({var['var_95_pct']*100:.2f}%)")
        lines.append(f"CVaR (95%, 1-day):     ${var['cvar_95_amount']:>15,.2f} ({var['cvar_95_pct']*100:.2f}%)")
        lines.append(f"VaR (99%, 1-day):      ${var['var_99_amount']:>15,.2f} ({var['var_99_pct']*100:.2f}%)")
        lines.append("")

        # Risk Warnings
        warnings = results['risk_warnings']
        if warnings:
            lines.append("🚨 RISK WARNINGS")
            lines.append("-" * 80)
            for warning in warnings:
                lines.append(f"  {warning}")
            lines.append("")

        # Tax Optimization
        tax_opps = results['tax_harvesting']
        lines.append("💰 TAX OPTIMIZATION OPPORTUNITIES")
        lines.append("-" * 80)
        if tax_opps:
            total_savings = sum(opp['tax_savings'] for opp in tax_opps)
            lines.append(f"Total Potential Savings: ${total_savings:,.2f}")
            lines.append("")
            lines.append(f"{'Ticker':<10} {'Loss':<15} {'Tax Savings':<15} {'Replacements'}")
            lines.append("-" * 80)
            for opp in tax_opps[:5]:
                replacements = ', '.join(opp['replacement_stocks'][:3])
                lines.append(
                    f"{opp['ticker']:<10} ${opp['current_loss']:>13,.0f} ${opp['tax_savings']:>13,.0f} {replacements}"
                )
        else:
            lines.append("No tax-loss harvesting opportunities found.")
        lines.append("")

        # Dividend Income
        dividends = results['dividends']
        if dividends:
            lines.append("💵 TOP DIVIDEND YIELDERS")
            lines.append("-" * 80)
            lines.append(f"{'Ticker':<10} {'Annual Div':<12} {'Yield':<10} {'YOC':<10}")
            lines.append("-" * 80)
            for div in dividends[:5]:
                lines.append(
                    f"{div.ticker:<10} ${div.annual_dividend:>10.2f} {div.forward_yield:>8.2%} {div.yield_on_cost:>8.2%}"
                )
            lines.append("")

        # Rebalancing
        rebal = results['rebalancing']
        lines.append("🔄 REBALANCING RECOMMENDATIONS")
        lines.append("-" * 80)
        if rebal.needs_rebalancing:
            lines.append(f"Status: ⚠️  REBALANCING RECOMMENDED (Max drift: {rebal.max_drift*100:.1f}%)")
            lines.append(f"Recommended Trades: {len(rebal.recommended_trades)}")
            lines.append(f"Tax Impact: ${rebal.total_tax_impact:,.2f}")
            lines.append(f"Transaction Costs: ${rebal.total_transaction_cost:,.2f}")
        else:
            lines.append(f"Status: ✅ Portfolio is balanced (Max drift: {rebal.max_drift*100:.1f}%)")
        lines.append("")

        # Action Items
        lines.append("✅ RECOMMENDED ACTIONS")
        lines.append("-" * 80)

        action_count = 1

        # Tax harvesting
        if tax_opps:
            lines.append(f"{action_count}. Consider tax-loss harvesting for ${sum(o['tax_savings'] for o in tax_opps):,.0f} in savings")
            action_count += 1

        # Rebalancing
        if rebal.needs_rebalancing:
            lines.append(f"{action_count}. Review {len(rebal.recommended_trades)} rebalancing trades")
            action_count += 1

        # Risk warnings
        if warnings:
            lines.append(f"{action_count}. Address {len(warnings)} risk warnings")
            action_count += 1

        # Performance
        if bench['excess_return'] < 0:
            lines.append(f"{action_count}. Portfolio underperforming S&P 500 - review holdings")
            action_count += 1

        if action_count == 1:
            lines.append("✅ No immediate action required - portfolio is well managed!")

        lines.append("")
        lines.append("=" * 80)
        lines.append("📝 For detailed analysis, use individual modules:")
        lines.append("   - scorecard.py <ticker>        : Stock fundamental analysis")
        lines.append("   - tax_loss_harvester.py <id>  : Tax optimization details")
        lines.append("   - benchmark_analyzer.py <id>  : Performance attribution")
        lines.append("   - risk_metrics.py <id>        : Risk analytics deep dive")
        lines.append("   - rebalance_engine.py <id>    : Rebalancing trade details")
        lines.append("=" * 80)

        return "\n".join(lines)

    def save_html_report(self, results: Dict, output_path: str):
        """Generate and save HTML report."""
        # This would create a comprehensive HTML dashboard
        # For now, we'll create a simplified version

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Copilot - Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 14px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .positive {{ color: #22c55e; }}
        .negative {{ color: #ef4444; }}
        .warning {{ color: #f59e0b; }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Portfolio Copilot</h1>
        <p>Comprehensive Portfolio Analysis Report</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="card">
        <h2>📊 Portfolio Overview</h2>
        <div class="metric">
            <div class="metric-label">Total Value</div>
            <div class="metric-value">${results['summary']['total_value']:,.2f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Unrealized P&L</div>
            <div class="metric-value {'positive' if results['summary']['unrealized_pnl'] > 0 else 'negative'}">
                ${results['summary']['unrealized_pnl']:,.2f} ({results['summary']['unrealized_pnl_pct']:+.2f}%)
            </div>
        </div>
        <div class="metric">
            <div class="metric-label">Holdings</div>
            <div class="metric-value">{results['summary']['num_holdings']}</div>
        </div>
    </div>

    <div class="card">
        <h2>📈 Performance Metrics</h2>
        <div class="metric">
            <div class="metric-label">Time-Weighted Return</div>
            <div class="metric-value">{results['performance']['twr']*100:.2f}%</div>
        </div>
        <div class="metric">
            <div class="metric-label">vs S&P 500</div>
            <div class="metric-value {'positive' if results['benchmark_spy']['excess_return'] > 0 else 'negative'}">
                {results['benchmark_spy']['excess_return']*100:+.2f}%
            </div>
        </div>
        <div class="metric">
            <div class="metric-label">Sharpe Ratio</div>
            <div class="metric-value">{results['performance']['sharpe_ratio']:.2f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Max Drawdown</div>
            <div class="metric-value negative">{results['performance']['max_drawdown']*100:.2f}%</div>
        </div>
    </div>

    <div class="card">
        <h2>⚠️ Risk Metrics</h2>
        <div class="metric">
            <div class="metric-label">VaR (95%, 1-day)</div>
            <div class="metric-value warning">${results['var_analysis']['var_95_amount']:,.2f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">CVaR (95%, 1-day)</div>
            <div class="metric-value warning">${results['var_analysis']['cvar_95_amount']:,.2f}</div>
        </div>
    </div>

    <div class="card">
        <h2>💰 Tax Optimization</h2>
        {"<p>Potential savings: $" + f"{sum(o['tax_savings'] for o in results['tax_harvesting']):,.2f}" + "</p>" if results['tax_harvesting'] else "<p>No tax-loss harvesting opportunities found.</p>"}
    </div>

    <div class="card">
        <h2>🔄 Rebalancing</h2>
        <p>Status: {"⚠️ Rebalancing recommended" if results['rebalancing'].needs_rebalancing else "✅ Portfolio is balanced"}</p>
        {f"<p>Max drift: {results['rebalancing'].max_drift*100:.1f}%</p>"}
    </div>

</body>
</html>"""

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"✅ HTML report saved to: {output_path}")

    def close(self):
        """Close all sessions."""
        self.session.close()
        self.tax_harvester.close()
        self.tax_calculator.close()
        self.dividend_tracker.close()
        self.benchmark_analyzer.close()
        self.performance_calculator.close()
        self.risk_analyzer.close()
        self.rebalance_engine.close()


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='Portfolio Copilot - Comprehensive Analysis')
    parser.add_argument('portfolio_id', type=int, help='Portfolio ID to analyze')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--output', type=str, help='Output path for HTML report')

    args = parser.parse_args()

    copilot = PortfolioCopilot(args.portfolio_id)

    try:
        # Run analysis
        results = copilot.run_comprehensive_analysis()

        # Generate text report
        report = copilot.generate_text_report(results)
        print(report)

        # Generate HTML if requested
        if args.html:
            output_path = args.output or f"portfolio-analysis-{args.portfolio_id}-{datetime.now().strftime('%Y-%m-%d')}.html"
            copilot.save_html_report(results, output_path)

    finally:
        copilot.close()


if __name__ == "__main__":
    main()
