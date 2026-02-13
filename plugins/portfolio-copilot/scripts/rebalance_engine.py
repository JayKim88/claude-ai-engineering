"""
Rebalancing Engine for Portfolio Copilot.

Analyzes portfolio allocation drift and generates rebalancing recommendations.

Key Features:
- Compare current allocation vs target allocation
- Calculate drift from target percentages
- Generate tax-efficient rebalancing trades
- Consider transaction costs and tax implications
- Provide detailed rebalancing reports

Usage:
    python3 rebalance_engine.py <portfolio_id>
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy.orm import Session
from database import get_database, Holding, Portfolio
from data_fetcher import get_stock_data
from tax_loss_harvester import TaxLossHarvester


@dataclass
class TargetAllocation:
    """Target allocation for a category."""
    category: str
    target_weight: float  # 0.0 to 1.0
    tolerance: float  # Acceptable deviation (e.g., 0.05 = ±5%)
    rebalance_threshold: float  # Trigger rebalancing when drift exceeds this


@dataclass
class RebalanceTrade:
    """Recommended rebalancing trade."""
    action: str  # 'BUY' or 'SELL'
    ticker: str
    current_value: float
    target_value: float
    trade_amount: float
    shares: int
    tax_impact: float  # Estimated tax from sale
    reason: str


@dataclass
class RebalanceReport:
    """Comprehensive rebalancing analysis."""
    portfolio_id: int
    total_value: float
    needs_rebalancing: bool
    max_drift: float
    current_allocation: Dict[str, float]
    target_allocation: Dict[str, float]
    drift_by_category: Dict[str, float]
    recommended_trades: List[RebalanceTrade]
    total_tax_impact: float
    total_transaction_cost: float
    report_date: datetime


class RebalanceEngine:
    """Portfolio rebalancing engine."""

    def __init__(self, db_path: str = None):
        """Initialize rebalancing engine."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()
        self.tax_harvester = TaxLossHarvester(db_path)

        # Default target allocations (can be customized)
        self.default_targets = {
            'Technology': TargetAllocation('Technology', 0.30, 0.05, 0.10),
            'Healthcare': TargetAllocation('Healthcare', 0.20, 0.05, 0.10),
            'Finance': TargetAllocation('Finance', 0.20, 0.05, 0.10),
            'Consumer': TargetAllocation('Consumer', 0.15, 0.05, 0.10),
            'Energy': TargetAllocation('Energy', 0.15, 0.05, 0.10),
        }

    def set_target_allocation(self, targets: Dict[str, TargetAllocation]):
        """Set custom target allocation."""
        self.default_targets = targets

    def get_current_allocation(self, portfolio_id: int) -> Tuple[Dict[str, float], float]:
        """
        Get current portfolio allocation by sector.

        Returns:
            (allocation_dict, total_value)
            allocation_dict: {sector: percentage}
            total_value: Total portfolio value in USD
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        sector_values = {}
        total_value = 0.0

        for holding in holdings:
            # Get current price
            stock_data = get_stock_data(holding.ticker, holding.market)
            if not stock_data or 'current_price' not in stock_data:
                print(f"⚠️  Warning: Could not fetch price for {holding.ticker}")
                current_price = holding.avg_price  # Fallback
            else:
                current_price = stock_data['current_price']

            # Get sector (fallback to 'Other' if not available)
            sector = stock_data.get('sector', 'Other') if stock_data else 'Other'

            # Calculate value
            position_value = current_price * holding.quantity
            total_value += position_value

            # Aggregate by sector
            sector_values[sector] = sector_values.get(sector, 0.0) + position_value

        # Convert to percentages
        allocation = {}
        if total_value > 0:
            for sector, value in sector_values.items():
                allocation[sector] = value / total_value

        return allocation, total_value

    def calculate_drift(self,
                       current_allocation: Dict[str, float],
                       target_allocation: Dict[str, TargetAllocation]) -> Dict[str, float]:
        """
        Calculate drift from target allocation.

        Returns:
            {sector: drift_percentage}
            Positive = overweight, Negative = underweight
        """
        drift = {}

        # Check drift for each target
        for sector, target in target_allocation.items():
            current_weight = current_allocation.get(sector, 0.0)
            drift[sector] = current_weight - target.target_weight

        return drift

    def needs_rebalancing(self, drift: Dict[str, float],
                         target_allocation: Dict[str, TargetAllocation]) -> Tuple[bool, float]:
        """
        Check if rebalancing is needed.

        Returns:
            (needs_rebalancing, max_drift)
        """
        max_drift = 0.0
        needs_rebalance = False

        for sector, drift_value in drift.items():
            abs_drift = abs(drift_value)
            max_drift = max(max_drift, abs_drift)

            target = target_allocation.get(sector)
            if target and abs_drift > target.rebalance_threshold:
                needs_rebalance = True

        return needs_rebalance, max_drift

    def generate_rebalancing_trades(self,
                                   portfolio_id: int,
                                   current_allocation: Dict[str, float],
                                   target_allocation: Dict[str, TargetAllocation],
                                   total_value: float) -> List[RebalanceTrade]:
        """
        Generate specific rebalancing trade recommendations.

        Strategy:
        1. Identify overweight and underweight sectors
        2. Select stocks to sell from overweight sectors (tax-efficient)
        3. Select stocks to buy in underweight sectors
        4. Calculate exact trade amounts
        """
        trades = []
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        # Calculate target values for each sector
        target_values = {
            sector: target.target_weight * total_value
            for sector, target in target_allocation.items()
        }

        # Calculate current values by sector and stock
        holdings_by_sector = {}
        for holding in holdings:
            stock_data = get_stock_data(holding.ticker, holding.market)
            if not stock_data:
                continue

            sector = stock_data.get('sector', 'Other')
            current_price = stock_data.get('current_price', holding.avg_price)
            position_value = current_price * holding.quantity

            if sector not in holdings_by_sector:
                holdings_by_sector[sector] = []

            holdings_by_sector[sector].append({
                'holding': holding,
                'ticker': holding.ticker,
                'current_price': current_price,
                'quantity': holding.quantity,
                'value': position_value,
                'avg_price': holding.avg_price,
                'unrealized_gain': (current_price - holding.avg_price) * holding.quantity
            })

        # Generate trades for each sector
        for sector, target in target_allocation.items():
            current_sector_value = sum(
                h['value'] for h in holdings_by_sector.get(sector, [])
            )
            target_sector_value = target_values[sector]
            difference = current_sector_value - target_sector_value

            if abs(difference) < 100:  # Skip if difference is too small
                continue

            if difference > 0:
                # SELL: Overweight sector
                stocks_to_sell = self._select_stocks_to_sell(
                    holdings_by_sector.get(sector, []),
                    difference
                )
                for stock, amount in stocks_to_sell:
                    # Calculate tax impact
                    tax_impact = self._estimate_tax_impact(
                        stock['holding'],
                        stock['current_price'],
                        amount / stock['current_price']
                    )

                    shares = int(amount / stock['current_price'])
                    if shares > 0:
                        trades.append(RebalanceTrade(
                            action='SELL',
                            ticker=stock['ticker'],
                            current_value=stock['value'],
                            target_value=stock['value'] - amount,
                            trade_amount=amount,
                            shares=shares,
                            tax_impact=tax_impact,
                            reason=f"{sector} overweight by {difference/total_value*100:.1f}%"
                        ))

            elif difference < 0:
                # BUY: Underweight sector
                buy_amount = abs(difference)

                # Suggest buying existing stocks in sector or new additions
                if holdings_by_sector.get(sector):
                    # Add to existing positions (simple strategy)
                    existing_stocks = holdings_by_sector[sector]
                    stock = existing_stocks[0]  # Buy the first stock in sector
                    shares = int(buy_amount / stock['current_price'])

                    if shares > 0:
                        trades.append(RebalanceTrade(
                            action='BUY',
                            ticker=stock['ticker'],
                            current_value=stock['value'],
                            target_value=stock['value'] + buy_amount,
                            trade_amount=buy_amount,
                            shares=shares,
                            tax_impact=0.0,  # No tax on buying
                            reason=f"{sector} underweight by {abs(difference)/total_value*100:.1f}%"
                        ))
                else:
                    # Sector not in portfolio - suggest manual stock selection
                    trades.append(RebalanceTrade(
                        action='BUY',
                        ticker=f"[{sector}_STOCK]",  # Placeholder
                        current_value=0.0,
                        target_value=buy_amount,
                        trade_amount=buy_amount,
                        shares=0,
                        tax_impact=0.0,
                        reason=f"{sector} underweight by {abs(difference)/total_value*100:.1f}% - Manual stock selection needed"
                    ))

        return trades

    def _select_stocks_to_sell(self,
                               sector_holdings: List[Dict],
                               target_amount: float) -> List[Tuple[Dict, float]]:
        """
        Select stocks to sell from a sector (tax-efficient).

        Strategy: Prioritize stocks with losses (tax-loss harvesting),
        then stocks with smallest gains.
        """
        # Sort by unrealized gain (ascending) - sell losers first
        sorted_holdings = sorted(sector_holdings, key=lambda x: x['unrealized_gain'])

        selections = []
        remaining_amount = target_amount

        for stock in sorted_holdings:
            if remaining_amount <= 0:
                break

            # Sell up to full position
            sell_amount = min(stock['value'], remaining_amount)
            selections.append((stock, sell_amount))
            remaining_amount -= sell_amount

        return selections

    def _estimate_tax_impact(self, holding: Holding, current_price: float, shares_sold: float) -> float:
        """Estimate tax impact of selling shares."""
        if shares_sold <= 0:
            return 0.0

        gain_per_share = current_price - holding.avg_price
        total_gain = gain_per_share * shares_sold

        if total_gain <= 0:
            return 0.0  # No tax on losses

        # Assume short-term capital gains (worst case)
        # US: 37%, Korea: 22%
        tax_rate = 0.37 if holding.market == 'US' else 0.22

        return total_gain * tax_rate

    def analyze_rebalancing(self, portfolio_id: int) -> RebalanceReport:
        """
        Perform comprehensive rebalancing analysis.

        Returns:
            RebalanceReport with all analysis results
        """
        # Get current allocation
        current_allocation, total_value = self.get_current_allocation(portfolio_id)

        # Calculate drift
        drift = self.calculate_drift(current_allocation, self.default_targets)

        # Check if rebalancing needed
        needs_rebalance, max_drift = self.needs_rebalancing(drift, self.default_targets)

        # Generate trades if needed
        recommended_trades = []
        if needs_rebalance:
            recommended_trades = self.generate_rebalancing_trades(
                portfolio_id,
                current_allocation,
                self.default_targets,
                total_value
            )

        # Calculate total tax impact
        total_tax_impact = sum(trade.tax_impact for trade in recommended_trades)

        # Estimate transaction costs (0.1% per trade)
        total_transaction_cost = sum(trade.trade_amount * 0.001 for trade in recommended_trades)

        # Build target allocation dict
        target_dict = {
            sector: target.target_weight
            for sector, target in self.default_targets.items()
        }

        return RebalanceReport(
            portfolio_id=portfolio_id,
            total_value=total_value,
            needs_rebalancing=needs_rebalance,
            max_drift=max_drift,
            current_allocation=current_allocation,
            target_allocation=target_dict,
            drift_by_category=drift,
            recommended_trades=recommended_trades,
            total_tax_impact=total_tax_impact,
            total_transaction_cost=total_transaction_cost,
            report_date=datetime.now()
        )

    def generate_report(self, report: RebalanceReport) -> str:
        """Generate human-readable rebalancing report."""
        lines = []
        lines.append("=" * 80)
        lines.append("🔄 PORTFOLIO REBALANCING ANALYSIS")
        lines.append("=" * 80)
        lines.append(f"Report Date: {report.report_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {report.portfolio_id}")
        lines.append(f"Total Value: ${report.total_value:,.2f}")
        lines.append("")

        # Rebalancing Status
        lines.append("📊 REBALANCING STATUS")
        lines.append("-" * 80)
        if report.needs_rebalancing:
            lines.append(f"Status: ⚠️  REBALANCING RECOMMENDED")
            lines.append(f"Max Drift: {report.max_drift*100:.2f}%")
        else:
            lines.append(f"Status: ✅ Portfolio is balanced")
            lines.append(f"Max Drift: {report.max_drift*100:.2f}%")
        lines.append("")

        # Allocation Comparison
        lines.append("📈 ALLOCATION ANALYSIS")
        lines.append("-" * 80)
        lines.append(f"{'Sector':<20} {'Current':<12} {'Target':<12} {'Drift':<12} {'Status'}")
        lines.append("-" * 80)

        for sector in report.target_allocation.keys():
            current = report.current_allocation.get(sector, 0.0)
            target = report.target_allocation[sector]
            drift = report.drift_by_category.get(sector, 0.0)

            status = "✅" if abs(drift) < 0.05 else "⚠️" if abs(drift) < 0.10 else "❌"
            drift_str = f"{drift*100:+.1f}%"

            lines.append(
                f"{sector:<20} {current*100:>10.1f}% {target*100:>10.1f}% "
                f"{drift_str:>10} {status}"
            )
        lines.append("")

        # Recommended Trades
        if report.recommended_trades:
            lines.append("💼 RECOMMENDED TRADES")
            lines.append("-" * 80)
            lines.append(f"{'Action':<6} {'Ticker':<10} {'Shares':<8} {'Amount':<12} {'Tax Impact':<12} {'Reason'}")
            lines.append("-" * 80)

            for trade in report.recommended_trades:
                lines.append(
                    f"{trade.action:<6} {trade.ticker:<10} {trade.shares:>6} "
                    f"${trade.trade_amount:>10,.0f} ${trade.tax_impact:>10,.0f} {trade.reason}"
                )

            lines.append("-" * 80)
            lines.append(f"Total Tax Impact:        ${report.total_tax_impact:>10,.2f}")
            lines.append(f"Transaction Costs:       ${report.total_transaction_cost:>10,.2f}")
            lines.append(f"Total Rebalancing Cost:  ${report.total_tax_impact + report.total_transaction_cost:>10,.2f}")
            lines.append("")

        # Summary
        lines.append("💡 RECOMMENDATIONS")
        lines.append("-" * 80)
        if not report.needs_rebalancing:
            lines.append("✅ Your portfolio is well balanced. No action needed.")
        else:
            lines.append(f"⚠️  {len(report.recommended_trades)} trades recommended to rebalance portfolio.")
            lines.append(f"💰 Estimated cost: ${report.total_tax_impact + report.total_transaction_cost:,.2f}")
            lines.append("")
            lines.append("Consider:")
            lines.append("  1. Execute trades during low-volatility periods")
            lines.append("  2. Review tax-loss harvesting opportunities")
            lines.append("  3. Prioritize selling positions with losses")
            lines.append("  4. Consider market conditions before execution")

        lines.append("=" * 80)

        return "\n".join(lines)

    def close(self):
        """Close database session."""
        self.session.close()
        self.tax_harvester.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 rebalance_engine.py <portfolio_id>")
        print("\nExamples:")
        print("  python3 rebalance_engine.py 1")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])

    engine = RebalanceEngine()

    try:
        # Analyze rebalancing needs
        print("🔄 Analyzing portfolio rebalancing needs...\n")
        report = engine.analyze_rebalancing(portfolio_id)

        # Display report
        print(engine.generate_report(report))

    finally:
        engine.close()
