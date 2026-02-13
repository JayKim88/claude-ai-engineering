"""
Tax-Loss Harvesting Engine for Portfolio Copilot (Sprint 1).

Automatically identifies opportunities to realize losses for tax benefits
while avoiding wash sale violations.

Key Features:
- Find stocks with unrealized losses
- Calculate potential tax savings
- Suggest replacement stocks to avoid wash sales
- Track 30-day wash sale window
- Optimize tax efficiency

References:
- IRS Wash Sale Rule: 30 days before/after sale
- Korean Tax: 22% capital gains tax (20% + 2% local)
- US Tax: 37% short-term, 15-20% long-term capital gains
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
import yfinance as yf
from database import get_database, Holding, Transaction
from data_fetcher import get_stock_data


class HarvestOpportunity:
    """Represents a tax-loss harvesting opportunity."""

    def __init__(
        self,
        ticker: str,
        holding_id: int,
        current_price: float,
        avg_price: float,
        quantity: float,
        unrealized_loss: float,
        tax_savings: float,
        holding_period: str,
        market: str,
        replacement_stocks: List[str] = None,
    ):
        self.ticker = ticker
        self.holding_id = holding_id
        self.current_price = current_price
        self.avg_price = avg_price
        self.quantity = quantity
        self.unrealized_loss = unrealized_loss
        self.tax_savings = tax_savings
        self.holding_period = holding_period  # 'short_term' or 'long_term'
        self.market = market
        self.replacement_stocks = replacement_stocks or []

    def __repr__(self):
        return (
            f"<HarvestOp({self.ticker}: loss=${self.unrealized_loss:.2f}, "
            f"savings=${self.tax_savings:.2f}, replacements={self.replacement_stocks})>"
        )


class TaxLossHarvester:
    """Tax-loss harvesting automation engine."""

    # Tax rates by market
    TAX_RATES = {
        "US": {"short_term": 0.37, "long_term": 0.20},  # Maximum federal rates
        "KR": {"short_term": 0.22, "long_term": 0.22},  # Korea: 22% flat (20% + 2% local)
    }

    WASH_SALE_DAYS = 30  # IRS wash sale rule: 30 days before/after

    def __init__(self, db_path: str = None):
        """Initialize tax loss harvester with database connection."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()

    def find_harvest_opportunities(
        self, portfolio_id: int, min_loss_threshold: float = 100.0, tax_rate_override: Dict = None
    ) -> List[HarvestOpportunity]:
        """
        Find tax-loss harvesting opportunities in portfolio.

        Args:
            portfolio_id: Portfolio to analyze
            min_loss_threshold: Minimum loss to consider (default $100)
            tax_rate_override: Custom tax rates {'US': {'short_term': 0.35, ...}}

        Returns:
            List of HarvestOpportunity objects sorted by tax savings (descending)
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        opportunities = []

        for holding in holdings:
            # Get current price
            stock_data = get_stock_data(holding.ticker, holding.market)
            if not stock_data or "current_price" not in stock_data:
                print(f"⚠️  Could not fetch price for {holding.ticker}, skipping")
                continue

            current_price = stock_data["current_price"]
            total_value = current_price * holding.quantity
            cost_basis = holding.avg_price * holding.quantity
            unrealized_loss = total_value - cost_basis

            # Only consider losses
            if unrealized_loss >= -min_loss_threshold:
                continue

            # Determine holding period
            first_purchase = (
                self.session.query(Transaction)
                .filter_by(holding_id=holding.id, type="BUY")
                .order_by(Transaction.date.asc())
                .first()
            )

            if not first_purchase:
                holding_period = "short_term"
            else:
                days_held = (datetime.now().date() - first_purchase.date).days
                holding_period = "long_term" if days_held >= 365 else "short_term"

            # Calculate tax savings
            tax_rates = tax_rate_override or self.TAX_RATES
            market_rates = tax_rates.get(holding.market, self.TAX_RATES["US"])
            applicable_rate = market_rates.get(holding_period, 0.22)
            tax_savings = abs(unrealized_loss) * applicable_rate

            # Check wash sale violations
            if self._has_recent_activity(holding.id, days=self.WASH_SALE_DAYS):
                print(f"⚠️  {holding.ticker} may violate wash sale rule (activity within 30 days)")

            # Find replacement stocks
            replacements = self._suggest_replacements(holding.ticker, holding.sector, holding.market)

            opportunity = HarvestOpportunity(
                ticker=holding.ticker,
                holding_id=holding.id,
                current_price=current_price,
                avg_price=holding.avg_price,
                quantity=holding.quantity,
                unrealized_loss=unrealized_loss,
                tax_savings=tax_savings,
                holding_period=holding_period,
                market=holding.market,
                replacement_stocks=replacements,
            )

            opportunities.append(opportunity)

        # Sort by tax savings (descending)
        opportunities.sort(key=lambda x: x.tax_savings, reverse=True)

        return opportunities

    def _has_recent_activity(self, holding_id: int, days: int = 30) -> bool:
        """Check if there's been any SELL activity within the past N days."""
        cutoff_date = datetime.now().date() - timedelta(days=days)

        recent_sales = (
            self.session.query(Transaction)
            .filter(Transaction.holding_id == holding_id, Transaction.type == "SELL", Transaction.date >= cutoff_date)
            .count()
        )

        return recent_sales > 0

    def _suggest_replacements(self, ticker: str, sector: str, market: str, top_n: int = 3) -> List[str]:
        """
        Suggest replacement stocks to avoid wash sale rule.

        Strategy:
        1. Same sector, different company
        2. High correlation (similar performance)
        3. Avoid same ticker for 30 days

        Args:
            ticker: Current ticker to replace
            sector: Stock sector
            market: US or KR
            top_n: Number of replacements to suggest

        Returns:
            List of ticker symbols
        """
        # Sector-based replacement suggestions
        REPLACEMENT_MAP = {
            # US Technology
            "AAPL": ["MSFT", "GOOGL", "META"],
            "MSFT": ["AAPL", "GOOGL", "ORCL"],
            "GOOGL": ["META", "MSFT", "AMZN"],
            "META": ["GOOGL", "SNAP", "PINS"],
            "NVDA": ["AMD", "INTC", "QCOM"],
            "AMD": ["NVDA", "INTC", "MU"],
            "TSLA": ["RIVN", "LCID", "F"],
            # US Finance
            "JPM": ["BAC", "WFC", "C"],
            "BAC": ["JPM", "WFC", "USB"],
            "V": ["MA", "AXP", "PYPL"],
            "MA": ["V", "AXP", "DFS"],
            # US Healthcare
            "JNJ": ["PFE", "UNH", "ABBV"],
            "PFE": ["JNJ", "MRK", "LLY"],
            "UNH": ["CVS", "CI", "HUM"],
            # US Consumer
            "AMZN": ["WMT", "TGT", "COST"],
            "WMT": ["TGT", "COST", "KR"],
            "KO": ["PEP", "MNST", "DPS"],
            "PEP": ["KO", "MNST", "KDP"],
            # Korean stocks (using sector similarity)
            "005930": ["000660", "SK하이닉스"],  # Samsung → SK Hynix
            "000660": ["005930", "삼성전자"],  # SK Hynix → Samsung
        }

        # Get direct replacements if available
        if ticker in REPLACEMENT_MAP:
            return REPLACEMENT_MAP[ticker][:top_n]

        # Fallback: generic sector-based suggestions
        SECTOR_ETFS = {
            "Technology": ["XLK", "QQQ", "VGT"] if market == "US" else ["TIGER 200 IT"],
            "Healthcare": ["XLV", "VHT", "IHI"] if market == "US" else [],
            "Finance": ["XLF", "VFH", "KBE"] if market == "US" else [],
            "Consumer": ["XLP", "XLY", "VDC"] if market == "US" else [],
            "Energy": ["XLE", "VDE", "IXC"] if market == "US" else [],
        }

        return SECTOR_ETFS.get(sector, ["SPY" if market == "US" else "KOSPI"])[:top_n]

    def calculate_wash_sale_window(self, sale_date: date) -> Tuple[date, date]:
        """
        Calculate the wash sale window (30 days before and after sale).

        Args:
            sale_date: Date of the sale

        Returns:
            Tuple of (start_date, end_date) for wash sale window
        """
        start_date = sale_date - timedelta(days=self.WASH_SALE_DAYS)
        end_date = sale_date + timedelta(days=self.WASH_SALE_DAYS)
        return (start_date, end_date)

    def generate_harvest_report(self, portfolio_id: int, min_loss_threshold: float = 100.0) -> Dict:
        """
        Generate comprehensive tax-loss harvesting report.

        Returns:
            {
                'opportunities': List[HarvestOpportunity],
                'total_potential_loss': float,
                'total_tax_savings': float,
                'num_opportunities': int,
                'report_date': datetime
            }
        """
        opportunities = self.find_harvest_opportunities(portfolio_id, min_loss_threshold)

        total_loss = sum(abs(opp.unrealized_loss) for opp in opportunities)
        total_savings = sum(opp.tax_savings for opp in opportunities)

        return {
            "opportunities": opportunities,
            "total_potential_loss": total_loss,
            "total_tax_savings": total_savings,
            "num_opportunities": len(opportunities),
            "report_date": datetime.now(),
        }

    def print_harvest_report(self, portfolio_id: int, min_loss_threshold: float = 100.0):
        """Print formatted tax-loss harvesting report to console."""
        report = self.generate_harvest_report(portfolio_id, min_loss_threshold)

        print("\n" + "=" * 70)
        print("💰 TAX-LOSS HARVESTING OPPORTUNITIES")
        print("=" * 70)
        print(f"Report Date: {report['report_date'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Min Loss Threshold: ${min_loss_threshold:.2f}")
        print(f"Opportunities Found: {report['num_opportunities']}")
        print(f"Total Potential Loss Realization: ${report['total_potential_loss']:,.2f}")
        print(f"Estimated Tax Savings: ${report['total_tax_savings']:,.2f}")
        print("=" * 70)

        if not report["opportunities"]:
            print("\n✅ No tax-loss harvesting opportunities found.")
            print("Your portfolio is currently in good shape with no significant losses.")
            return

        print(f"\n{'#':<4} {'Ticker':<8} {'Loss':<12} {'Tax Savings':<12} {'Period':<12} {'Replacements'}")
        print("-" * 70)

        for idx, opp in enumerate(report["opportunities"], 1):
            replacements_str = ", ".join(opp.replacement_stocks[:3])
            print(
                f"{idx:<4} {opp.ticker:<8} "
                f"${abs(opp.unrealized_loss):>10,.2f} "
                f"${opp.tax_savings:>10,.2f} "
                f"{opp.holding_period:<12} "
                f"{replacements_str}"
            )

        print("\n" + "=" * 70)
        print("📋 NEXT STEPS:")
        print("=" * 70)
        print("1. Review each opportunity and decide which losses to harvest")
        print("2. Sell the losing positions (creates realized loss)")
        print("3. Wait 31 days OR buy replacement stocks immediately")
        print("4. Use tax savings to offset capital gains or income (up to $3,000/year)")
        print("\n⚠️  WASH SALE WARNING:")
        print("Do NOT repurchase the same stock within 30 days before/after sale!")
        print("=" * 70 + "\n")

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 tax_loss_harvester.py <portfolio_id> [min_loss_threshold]")
        print("\nExample:")
        print("  python3 tax_loss_harvester.py 1")
        print("  python3 tax_loss_harvester.py 1 500  # Only show losses > $500")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])
    min_loss = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0

    harvester = TaxLossHarvester()

    try:
        harvester.print_harvest_report(portfolio_id, min_loss)
    finally:
        harvester.close()
