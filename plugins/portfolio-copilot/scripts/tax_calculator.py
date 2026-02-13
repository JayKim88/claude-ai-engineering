"""
Capital Gains Tax Calculator for Portfolio Copilot (Sprint 1).

Calculates capital gains taxes for US and Korean stocks with support for:
- Short-term vs long-term capital gains
- Different tax rates by country
- Realized vs unrealized gains/losses
- Annual tax reporting
- Tax-efficient portfolio optimization

Tax Rates:
- US: Short-term (< 1 year) = ordinary income rate (up to 37%)
       Long-term (>= 1 year) = 0%, 15%, or 20% based on income
- Korea: Flat 22% (20% capital gains + 2% local tax)
         Major shareholders: 27.5%
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from database import get_database, Transaction, Holding
import json


class TaxSummary:
    """Container for tax calculation results."""

    def __init__(
        self,
        tax_year: int,
        kr_realized_gains: float = 0.0,
        kr_tax: float = 0.0,
        us_short_term_gains: float = 0.0,
        us_long_term_gains: float = 0.0,
        us_tax: float = 0.0,
        total_tax: float = 0.0,
        dividend_income: float = 0.0,
        dividend_tax: float = 0.0,
    ):
        self.tax_year = tax_year
        self.kr_realized_gains = kr_realized_gains
        self.kr_tax = kr_tax
        self.us_short_term_gains = us_short_term_gains
        self.us_long_term_gains = us_long_term_gains
        self.us_tax = us_tax
        self.total_tax = total_tax
        self.dividend_income = dividend_income
        self.dividend_tax = dividend_tax

    @property
    def total_realized_gains(self) -> float:
        """Total realized gains across all markets."""
        return self.kr_realized_gains + self.us_short_term_gains + self.us_long_term_gains

    @property
    def effective_tax_rate(self) -> float:
        """Effective tax rate on realized gains."""
        if self.total_realized_gains == 0:
            return 0.0
        return (self.total_tax / self.total_realized_gains) * 100

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "tax_year": self.tax_year,
            "kr_realized_gains": round(self.kr_realized_gains, 2),
            "kr_tax": round(self.kr_tax, 2),
            "us_short_term_gains": round(self.us_short_term_gains, 2),
            "us_long_term_gains": round(self.us_long_term_gains, 2),
            "us_tax": round(self.us_tax, 2),
            "total_tax": round(self.total_tax, 2),
            "total_realized_gains": round(self.total_realized_gains, 2),
            "effective_tax_rate": round(self.effective_tax_rate, 2),
            "dividend_income": round(self.dividend_income, 2),
            "dividend_tax": round(self.dividend_tax, 2),
        }


class TaxCalculator:
    """Capital gains tax calculator for multi-market portfolios."""

    # Default tax rates
    DEFAULT_RATES = {
        "US": {
            "short_term": 0.37,  # Maximum federal rate (treated as ordinary income)
            "long_term": 0.20,  # Maximum long-term capital gains rate
            "dividend_qualified": 0.20,  # Qualified dividends
            "dividend_ordinary": 0.37,  # Non-qualified dividends
        },
        "KR": {
            "capital_gains": 0.22,  # 20% + 2% local tax
            "capital_gains_major": 0.275,  # Major shareholders: 25% + 2.5% local
            "dividend": 0.154,  # 14% + 1.4% local tax
        },
    }

    def __init__(self, db_path: str = None, tax_rates: Dict = None):
        """
        Initialize tax calculator.

        Args:
            db_path: Path to database file
            tax_rates: Custom tax rates (optional)
        """
        self.db = get_database(db_path)
        self.session = self.db.get_session()
        self.tax_rates = tax_rates or self.DEFAULT_RATES

    def calculate_realized_gains(
        self, portfolio_id: int, tax_year: int, holding_id: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Calculate realized gains/losses from SELL transactions.

        Args:
            portfolio_id: Portfolio ID
            tax_year: Year to calculate (e.g., 2026)
            holding_id: Optional - specific holding to analyze

        Returns:
            {
                'US_short_term': float,
                'US_long_term': float,
                'KR_gains': float,
                'total': float
            }
        """
        # Query all SELL transactions for the tax year
        query = self.session.query(Transaction).join(Holding).filter(
            and_(
                Holding.portfolio_id == portfolio_id,
                Transaction.type == "SELL",
                func.strftime("%Y", Transaction.date) == str(tax_year),
            )
        )

        if holding_id:
            query = query.filter(Transaction.holding_id == holding_id)

        sell_transactions = query.all()

        us_short_term = 0.0
        us_long_term = 0.0
        kr_gains = 0.0

        for txn in sell_transactions:
            if txn.realized_gain_loss is None:
                # Calculate if not already stored
                gain_loss = self._calculate_transaction_gain_loss(txn)
            else:
                gain_loss = txn.realized_gain_loss

            holding = txn.holding

            if holding.market == "US":
                if txn.holding_period == "short_term":
                    us_short_term += gain_loss
                else:
                    us_long_term += gain_loss
            elif holding.market == "KR":
                kr_gains += gain_loss

        return {
            "US_short_term": us_short_term,
            "US_long_term": us_long_term,
            "KR_gains": kr_gains,
            "total": us_short_term + us_long_term + kr_gains,
        }

    def _calculate_transaction_gain_loss(self, transaction: Transaction) -> float:
        """
        Calculate gain/loss for a specific transaction.

        For SELL: (sale_price - avg_cost) * quantity - fees
        """
        if transaction.type != "SELL":
            return 0.0

        holding = transaction.holding
        cost_basis = holding.avg_price * transaction.quantity
        proceeds = transaction.price * transaction.quantity
        fees = transaction.fees or 0.0

        return proceeds - cost_basis - fees

    def calculate_capital_gains_tax(
        self, portfolio_id: int, tax_year: int, is_major_shareholder: bool = False
    ) -> TaxSummary:
        """
        Calculate total capital gains tax liability for a tax year.

        Args:
            portfolio_id: Portfolio ID
            tax_year: Tax year (e.g., 2026)
            is_major_shareholder: True if owner is a major shareholder (Korea only)

        Returns:
            TaxSummary object with detailed tax breakdown
        """
        gains = self.calculate_realized_gains(portfolio_id, tax_year)

        # US Taxes
        us_short_term_tax = max(0, gains["US_short_term"] * self.tax_rates["US"]["short_term"])
        us_long_term_tax = max(0, gains["US_long_term"] * self.tax_rates["US"]["long_term"])
        us_total_tax = us_short_term_tax + us_long_term_tax

        # Korean Taxes
        kr_rate = self.tax_rates["KR"]["capital_gains_major"] if is_major_shareholder else self.tax_rates["KR"]["capital_gains"]
        kr_tax = max(0, gains["KR_gains"] * kr_rate)

        # Dividend taxes (from DIVIDEND transactions)
        dividend_data = self._calculate_dividend_taxes(portfolio_id, tax_year)

        summary = TaxSummary(
            tax_year=tax_year,
            kr_realized_gains=gains["KR_gains"],
            kr_tax=kr_tax,
            us_short_term_gains=gains["US_short_term"],
            us_long_term_gains=gains["US_long_term"],
            us_tax=us_total_tax,
            total_tax=kr_tax + us_total_tax + dividend_data["tax"],
            dividend_income=dividend_data["income"],
            dividend_tax=dividend_data["tax"],
        )

        return summary

    def _calculate_dividend_taxes(self, portfolio_id: int, tax_year: int) -> Dict[str, float]:
        """Calculate taxes on dividend income."""
        dividend_txns = (
            self.session.query(Transaction)
            .join(Holding)
            .filter(
                and_(
                    Holding.portfolio_id == portfolio_id,
                    Transaction.type == "DIVIDEND",
                    func.strftime("%Y", Transaction.date) == str(tax_year),
                )
            )
            .all()
        )

        us_qualified_dividends = 0.0
        us_ordinary_dividends = 0.0
        kr_dividends = 0.0

        for txn in dividend_txns:
            amount = txn.price * txn.quantity if txn.quantity else txn.price or 0.0

            if txn.holding.market == "US":
                # Assume qualified unless noted otherwise
                us_qualified_dividends += amount
            elif txn.holding.market == "KR":
                kr_dividends += amount

        us_div_tax = us_qualified_dividends * self.tax_rates["US"]["dividend_qualified"]
        kr_div_tax = kr_dividends * self.tax_rates["KR"]["dividend"]

        return {"income": us_qualified_dividends + kr_dividends, "tax": us_div_tax + kr_div_tax}

    def generate_annual_report(
        self, portfolio_id: int, tax_year: int, is_major_shareholder: bool = False, output_format: str = "text"
    ) -> str:
        """
        Generate comprehensive annual tax report.

        Args:
            portfolio_id: Portfolio ID
            tax_year: Tax year
            is_major_shareholder: Major shareholder status (Korea)
            output_format: 'text' or 'json'

        Returns:
            Formatted report string
        """
        summary = self.calculate_capital_gains_tax(portfolio_id, tax_year, is_major_shareholder)

        if output_format == "json":
            return json.dumps(summary.to_dict(), indent=2)

        # Text format
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append(f"📊 ANNUAL TAX REPORT - {tax_year}")
        report_lines.append("=" * 70)
        report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Portfolio ID: {portfolio_id}")
        report_lines.append("")

        # Realized Gains Section
        report_lines.append("💰 REALIZED GAINS/LOSSES")
        report_lines.append("-" * 70)
        report_lines.append(f"US Short-term (<1 year):  ${summary.us_short_term_gains:>12,.2f}")
        report_lines.append(f"US Long-term (>=1 year):  ${summary.us_long_term_gains:>12,.2f}")
        report_lines.append(f"Korean Stocks:            ${summary.kr_realized_gains:>12,.2f}")
        report_lines.append("-" * 70)
        report_lines.append(f"TOTAL REALIZED GAINS:     ${summary.total_realized_gains:>12,.2f}")
        report_lines.append("")

        # Tax Liability Section
        report_lines.append("💸 TAX LIABILITY")
        report_lines.append("-" * 70)
        report_lines.append(f"US Capital Gains Tax:     ${summary.us_tax:>12,.2f}")
        report_lines.append(f"  - Short-term @ 37%:     ${summary.us_short_term_gains * 0.37:>12,.2f}")
        report_lines.append(f"  - Long-term @ 20%:      ${summary.us_long_term_gains * 0.20:>12,.2f}")
        report_lines.append("")
        kr_rate_pct = 27.5 if is_major_shareholder else 22.0
        report_lines.append(f"Korean Capital Gains Tax: ${summary.kr_tax:>12,.2f}")
        report_lines.append(f"  - Rate: {kr_rate_pct}%")
        report_lines.append("")
        report_lines.append(f"Dividend Tax:             ${summary.dividend_tax:>12,.2f}")
        report_lines.append(f"  - Dividend Income:      ${summary.dividend_income:>12,.2f}")
        report_lines.append("-" * 70)
        report_lines.append(f"TOTAL TAX LIABILITY:      ${summary.total_tax:>12,.2f}")
        report_lines.append(f"Effective Tax Rate:       {summary.effective_tax_rate:>13.2f}%")
        report_lines.append("")

        # Tax Optimization Tips
        report_lines.append("💡 TAX OPTIMIZATION TIPS")
        report_lines.append("-" * 70)

        if summary.us_short_term_gains > 0:
            short_term_tax = summary.us_short_term_gains * 0.37
            long_term_tax = summary.us_short_term_gains * 0.20
            savings = short_term_tax - long_term_tax
            report_lines.append(f"⚠️  You paid ${short_term_tax:,.2f} in short-term capital gains tax.")
            report_lines.append(f"   If held >1 year, tax would be ${long_term_tax:,.2f} (saves ${savings:,.2f})")

        if summary.total_realized_gains < 0:
            loss = abs(summary.total_realized_gains)
            max_deduction = min(loss, 3000)
            report_lines.append(f"✅ You have ${loss:,.2f} in capital losses.")
            report_lines.append(f"   You can deduct up to ${max_deduction:,.2f} against ordinary income.")
            if loss > 3000:
                carryforward = loss - 3000
                report_lines.append(f"   Carry forward ${carryforward:,.2f} to future years.")

        report_lines.append("")
        report_lines.append("📋 RECOMMENDED ACTIONS:")
        report_lines.append("1. Review tax-loss harvesting opportunities (run tax_loss_harvester.py)")
        report_lines.append("2. Consider holding period impact before selling (short vs long-term)")
        report_lines.append("3. Maximize long-term holdings for lower tax rates")
        report_lines.append("4. Track dividend income and qualified status")
        report_lines.append("=" * 70)

        return "\n".join(report_lines)

    def export_tax_report(
        self, portfolio_id: int, tax_year: int, output_file: str = None, is_major_shareholder: bool = False
    ):
        """
        Export tax report to file.

        Args:
            portfolio_id: Portfolio ID
            tax_year: Tax year
            output_file: Output file path (default: data/tax_report_{year}.txt)
            is_major_shareholder: Major shareholder status
        """
        import os

        if output_file is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            os.makedirs(data_dir, exist_ok=True)
            output_file = os.path.join(data_dir, f"tax_report_{tax_year}.txt")

        report = self.generate_annual_report(portfolio_id, tax_year, is_major_shareholder)

        with open(output_file, "w") as f:
            f.write(report)

        print(f"✅ Tax report exported to: {output_file}")

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 tax_calculator.py <portfolio_id> [tax_year] [--major-shareholder]")
        print("\nExamples:")
        print("  python3 tax_calculator.py 1")
        print("  python3 tax_calculator.py 1 2026")
        print("  python3 tax_calculator.py 1 2026 --major-shareholder")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])
    tax_year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
    is_major = "--major-shareholder" in sys.argv

    calculator = TaxCalculator()

    try:
        # Generate and print report
        report = calculator.generate_annual_report(portfolio_id, tax_year, is_major)
        print(report)

        # Ask if user wants to export
        print("\n💾 Export this report? (y/n): ", end="")
        response = input().strip().lower()

        if response in ["y", "yes"]:
            calculator.export_tax_report(portfolio_id, tax_year, is_major_shareholder=is_major)

    finally:
        calculator.close()
