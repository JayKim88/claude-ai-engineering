"""
Dividend Tracking System for Portfolio Copilot (Sprint 1).

Tracks dividend income, forecasts future payments, and analyzes yield metrics.

Key Features:
- Track historical dividend payments
- Fetch upcoming dividend schedules
- Calculate dividend yields (forward yield and yield-on-cost)
- Forecast future dividend income
- Track qualified vs non-qualified dividends (US tax)
- Generate dividend income reports

Dividend Metrics:
- Forward Yield: Annual dividend / current price
- Yield on Cost (YOC): Annual dividend / original cost basis
- Dividend Growth Rate: Year-over-year dividend increase
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
from sqlalchemy import and_, func, desc
from sqlalchemy.orm import Session
import yfinance as yf
from database import get_database, Holding, Transaction, DividendCalendar
from data_fetcher import get_stock_data


class DividendSummary:
    """Container for dividend analysis results."""

    def __init__(
        self,
        ticker: str,
        annual_dividend: float,
        forward_yield: float,
        yield_on_cost: float,
        payment_frequency: str,
        next_ex_date: Optional[date] = None,
        next_payment_date: Optional[date] = None,
        qualified: bool = True,
    ):
        self.ticker = ticker
        self.annual_dividend = annual_dividend
        self.forward_yield = forward_yield
        self.yield_on_cost = yield_on_cost
        self.payment_frequency = payment_frequency
        self.next_ex_date = next_ex_date
        self.next_payment_date = next_payment_date
        self.qualified = qualified

    def __repr__(self):
        return (
            f"<DividendSummary({self.ticker}: yield={self.forward_yield:.2%}, "
            f"YOC={self.yield_on_cost:.2%}, freq={self.payment_frequency})>"
        )


class DividendTracker:
    """Dividend income tracking and forecasting system."""

    def __init__(self, db_path: str = None):
        """Initialize dividend tracker with database connection."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()

    def get_annual_dividend_income(self, portfolio_id: int, year: int) -> Dict:
        """
        Get total dividend income for a specific year.

        Args:
            portfolio_id: Portfolio ID
            year: Year to analyze (e.g., 2026)

        Returns:
            {
                'total_income': float,
                'us_qualified': float,
                'us_ordinary': float,
                'kr_dividends': float,
                'num_payments': int,
                'by_ticker': {ticker: amount}
            }
        """
        # Query all DIVIDEND transactions for the year
        dividend_txns = (
            self.session.query(Transaction)
            .join(Holding)
            .filter(
                and_(
                    Holding.portfolio_id == portfolio_id,
                    Transaction.type == "DIVIDEND",
                    func.strftime("%Y", Transaction.date) == str(year),
                )
            )
            .all()
        )

        total_income = 0.0
        us_qualified = 0.0
        us_ordinary = 0.0
        kr_dividends = 0.0
        by_ticker = {}

        for txn in dividend_txns:
            # Dividend amount can be stored in price field or as quantity * price
            amount = txn.price * txn.quantity if txn.quantity else txn.price or 0.0
            total_income += amount

            ticker = txn.holding.ticker
            by_ticker[ticker] = by_ticker.get(ticker, 0.0) + amount

            # Categorize by market and qualification
            if txn.holding.market == "US":
                # Assume qualified unless holding period < 60 days (simplified)
                us_qualified += amount
            elif txn.holding.market == "KR":
                kr_dividends += amount

        return {
            "total_income": total_income,
            "us_qualified": us_qualified,
            "us_ordinary": us_ordinary,
            "kr_dividends": kr_dividends,
            "num_payments": len(dividend_txns),
            "by_ticker": by_ticker,
        }

    def calculate_dividend_yields(self, portfolio_id: int) -> List[DividendSummary]:
        """
        Calculate dividend yields for all holdings.

        Returns:
            List of DividendSummary objects for each dividend-paying stock
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        summaries = []

        for holding in holdings:
            # Get current price
            stock_data = get_stock_data(holding.ticker, holding.market)
            if not stock_data or "current_price" not in stock_data:
                continue

            current_price = stock_data["current_price"]

            # Fetch dividend info from yfinance
            div_info = self._fetch_dividend_info(holding.ticker, holding.market)
            if not div_info or div_info["annual_dividend"] == 0:
                continue  # Skip non-dividend stocks

            # Calculate forward yield
            forward_yield = div_info["annual_dividend"] / current_price if current_price > 0 else 0

            # Calculate yield on cost (YOC)
            yield_on_cost = div_info["annual_dividend"] / holding.avg_price if holding.avg_price > 0 else 0

            summary = DividendSummary(
                ticker=holding.ticker,
                annual_dividend=div_info["annual_dividend"],
                forward_yield=forward_yield,
                yield_on_cost=yield_on_cost,
                payment_frequency=div_info["frequency"],
                next_ex_date=div_info.get("next_ex_date"),
                next_payment_date=div_info.get("next_payment_date"),
                qualified=holding.market == "US",  # Simplified
            )

            summaries.append(summary)

        # Sort by yield on cost (descending)
        summaries.sort(key=lambda x: x.yield_on_cost, reverse=True)

        return summaries

    def _fetch_dividend_info(self, ticker: str, market: str) -> Optional[Dict]:
        """
        Fetch dividend information from yfinance.

        Returns:
            {
                'annual_dividend': float,
                'frequency': str,
                'next_ex_date': date,
                'next_payment_date': date
            }
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Get annual dividend
            annual_dividend = info.get("dividendRate", 0.0)
            if annual_dividend == 0:
                # Try fallback
                trailing_annual = info.get("trailingAnnualDividendRate", 0.0)
                annual_dividend = trailing_annual

            # Get dividend frequency
            ex_dividend_date = info.get("exDividendDate")
            dividend_date = info.get("dividendDate")

            # Determine frequency from dividends history
            try:
                dividends = stock.dividends
                if len(dividends) >= 4:
                    # Count payments in last 12 months
                    one_year_ago = datetime.now() - timedelta(days=365)
                    recent_divs = dividends[dividends.index > one_year_ago]
                    num_payments = len(recent_divs)

                    if num_payments >= 12:
                        frequency = "monthly"
                    elif num_payments >= 4:
                        frequency = "quarterly"
                    elif num_payments >= 2:
                        frequency = "semi-annual"
                    else:
                        frequency = "annual"
                else:
                    frequency = "quarterly"  # Default assumption
            except:
                frequency = "quarterly"

            # Convert timestamps to dates
            next_ex_date = None
            next_payment_date = None

            if ex_dividend_date:
                try:
                    next_ex_date = datetime.fromtimestamp(ex_dividend_date).date()
                except:
                    pass

            if dividend_date:
                try:
                    next_payment_date = datetime.fromtimestamp(dividend_date).date()
                except:
                    pass

            return {
                "annual_dividend": annual_dividend,
                "frequency": frequency,
                "next_ex_date": next_ex_date,
                "next_payment_date": next_payment_date,
            }

        except Exception as e:
            print(f"⚠️  Error fetching dividend info for {ticker}: {e}")
            return None

    def forecast_dividends(self, portfolio_id: int, months: int = 12) -> List[Dict]:
        """
        Forecast future dividend payments.

        Args:
            portfolio_id: Portfolio ID
            months: Number of months to forecast (default 12)

        Returns:
            List of forecasted dividend payments:
            [
                {
                    'ticker': str,
                    'date': date,
                    'estimated_amount': float,
                    'confidence': str  # 'high', 'medium', 'low'
                }
            ]
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        forecasts = []
        end_date = datetime.now().date() + timedelta(days=months * 30)

        for holding in holdings:
            div_info = self._fetch_dividend_info(holding.ticker, holding.market)
            if not div_info or div_info["annual_dividend"] == 0:
                continue

            # Estimate payment schedule based on frequency
            frequency_map = {"monthly": 30, "quarterly": 90, "semi-annual": 180, "annual": 365}

            days_between = frequency_map.get(div_info["frequency"], 90)

            # Use next ex-date as starting point, or estimate from today
            next_date = div_info.get("next_ex_date") or datetime.now().date()

            # Generate forecast dates
            current_date = next_date
            payment_amount = div_info["annual_dividend"] / (365 / days_between)

            while current_date <= end_date:
                forecasts.append(
                    {
                        "ticker": holding.ticker,
                        "date": current_date,
                        "estimated_amount": payment_amount * holding.quantity,
                        "confidence": "high" if div_info.get("next_ex_date") else "medium",
                    }
                )
                current_date += timedelta(days=days_between)

        # Sort by date
        forecasts.sort(key=lambda x: x["date"])

        return forecasts

    def sync_dividend_calendar(self, portfolio_id: int):
        """
        Sync dividend calendar for all holdings from yfinance.

        Updates the dividend_calendar table with latest data.
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        synced_count = 0

        for holding in holdings:
            div_info = self._fetch_dividend_info(holding.ticker, holding.market)
            if not div_info or div_info["annual_dividend"] == 0:
                continue

            # Check if entry exists
            existing = (
                self.session.query(DividendCalendar)
                .filter_by(ticker=holding.ticker, ex_date=div_info.get("next_ex_date"))
                .first()
            )

            if not existing and div_info.get("next_ex_date"):
                # Create new entry
                calendar_entry = DividendCalendar(
                    ticker=holding.ticker,
                    ex_date=div_info["next_ex_date"],
                    payment_date=div_info.get("next_payment_date"),
                    amount=div_info["annual_dividend"] / 4,  # Quarterly estimate
                    frequency=div_info["frequency"],
                    currency=holding.currency,
                    qualified=1 if holding.market == "US" else 0,
                )

                self.session.add(calendar_entry)
                synced_count += 1

        self.session.commit()
        print(f"✅ Synced {synced_count} dividend calendar entries")

    def generate_dividend_report(self, portfolio_id: int, year: int = None) -> str:
        """
        Generate comprehensive dividend income report.

        Args:
            portfolio_id: Portfolio ID
            year: Year to report (default: current year)

        Returns:
            Formatted report string
        """
        if year is None:
            year = datetime.now().year

        # Get annual income
        annual_income = self.get_annual_dividend_income(portfolio_id, year)

        # Get yield analysis
        yields = self.calculate_dividend_yields(portfolio_id)

        # Get forecast
        forecast = self.forecast_dividends(portfolio_id, months=12)

        # Build report
        lines = []
        lines.append("=" * 70)
        lines.append(f"💵 DIVIDEND INCOME REPORT - {year}")
        lines.append("=" * 70)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {portfolio_id}")
        lines.append("")

        # Annual Income Summary
        lines.append("📊 ANNUAL DIVIDEND INCOME")
        lines.append("-" * 70)
        lines.append(f"Total Income:         ${annual_income['total_income']:>12,.2f}")
        lines.append(f"  US Qualified:       ${annual_income['us_qualified']:>12,.2f}")
        lines.append(f"  US Ordinary:        ${annual_income['us_ordinary']:>12,.2f}")
        lines.append(f"  Korean:             ${annual_income['kr_dividends']:>12,.2f}")
        lines.append(f"Number of Payments:   {annual_income['num_payments']:>14}")
        lines.append("")

        # Top Dividend Payers
        if annual_income["by_ticker"]:
            lines.append("🏆 TOP DIVIDEND PAYERS")
            lines.append("-" * 70)
            sorted_tickers = sorted(annual_income["by_ticker"].items(), key=lambda x: x[1], reverse=True)
            for ticker, amount in sorted_tickers[:5]:
                pct = (amount / annual_income["total_income"]) * 100 if annual_income["total_income"] > 0 else 0
                lines.append(f"  {ticker:<10} ${amount:>10,.2f}  ({pct:>5.1f}%)")
            lines.append("")

        # Yield Analysis
        if yields:
            lines.append("📈 DIVIDEND YIELD ANALYSIS")
            lines.append("-" * 70)
            lines.append(f"{'Ticker':<10} {'Annual Div':<12} {'Fwd Yield':<12} {'YOC':<12} {'Frequency'}")
            lines.append("-" * 70)
            for summary in yields[:10]:  # Top 10
                lines.append(
                    f"{summary.ticker:<10} "
                    f"${summary.annual_dividend:>10.2f} "
                    f"{summary.forward_yield:>10.2%} "
                    f"{summary.yield_on_cost:>10.2%} "
                    f"{summary.payment_frequency}"
                )
            lines.append("")

        # Upcoming Dividends
        if forecast:
            lines.append("📅 UPCOMING DIVIDENDS (Next 90 Days)")
            lines.append("-" * 70)
            today = datetime.now().date()
            upcoming = [f for f in forecast if f["date"] >= today and f["date"] <= today + timedelta(days=90)]

            if upcoming:
                lines.append(f"{'Date':<12} {'Ticker':<10} {'Amount':<12} {'Confidence'}")
                lines.append("-" * 70)
                for div in upcoming[:15]:  # Next 15 payments
                    lines.append(
                        f"{div['date']} {div['ticker']:<10} ${div['estimated_amount']:>10.2f} {div['confidence']}"
                    )

                total_upcoming = sum(d["estimated_amount"] for d in upcoming)
                lines.append("-" * 70)
                lines.append(f"Total (Next 90 Days): ${total_upcoming:>10,.2f}")
            else:
                lines.append("No upcoming dividends in the next 90 days")

            lines.append("")

        # Tax Information
        lines.append("💡 TAX INFORMATION")
        lines.append("-" * 70)
        lines.append("US Qualified Dividends: Taxed at long-term capital gains rate (0-20%)")
        lines.append("US Ordinary Dividends:  Taxed as ordinary income (up to 37%)")
        lines.append("Korean Dividends:       Taxed at 15.4% (14% + 1.4% local)")
        lines.append("")
        lines.append("💡 TIP: Hold US stocks for 60+ days to qualify for lower dividend tax rates")

        lines.append("=" * 70)

        return "\n".join(lines)

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 dividend_tracker.py <portfolio_id> [year]")
        print("\nExamples:")
        print("  python3 dividend_tracker.py 1")
        print("  python3 dividend_tracker.py 1 2026")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])
    year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year

    tracker = DividendTracker()

    try:
        # Sync dividend calendar first
        print("🔄 Syncing dividend calendar...")
        tracker.sync_dividend_calendar(portfolio_id)

        # Generate report
        report = tracker.generate_dividend_report(portfolio_id, year)
        print("\n" + report)

    finally:
        tracker.close()
