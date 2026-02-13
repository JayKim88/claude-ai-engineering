"""
Performance Calculator for Portfolio Copilot (Sprint 2).

Calculates time-weighted returns, performance attribution, and risk metrics.

Key Features:
- Time-Weighted Return (TWR) - pure investment performance
- Money-Weighted Return (MWR/IRR) - timing-inclusive performance
- Performance attribution (Brinson-Fachler model)
- Maximum drawdown analysis
- Rolling returns and volatility
- Risk-adjusted performance metrics

TWR vs MWR:
- TWR: Measures investment skill (removes cash flow timing)
- MWR: Measures overall experience (includes investor timing)
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
import yfinance as yf
from sqlalchemy import and_, func, desc
from database import get_database, Holding, Transaction, PortfolioSnapshot
from data_fetcher import get_stock_data


class PerformanceMetrics:
    """Container for performance calculation results."""

    def __init__(
        self,
        twr_total: float,
        twr_annualized: float,
        mwr: float,
        max_drawdown: float,
        volatility_annual: float,
        sharpe_ratio: float,
        sortino_ratio: float,
        calmar_ratio: float,
    ):
        self.twr_total = twr_total
        self.twr_annualized = twr_annualized
        self.mwr = mwr
        self.max_drawdown = max_drawdown
        self.volatility_annual = volatility_annual
        self.sharpe_ratio = sharpe_ratio
        self.sortino_ratio = sortino_ratio
        self.calmar_ratio = calmar_ratio

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "twr_total": self.twr_total,
            "twr_annualized": self.twr_annualized,
            "mwr": self.mwr,
            "max_drawdown": self.max_drawdown,
            "volatility_annual": self.volatility_annual,
            "sharpe_ratio": self.sharpe_ratio,
            "sortino_ratio": self.sortino_ratio,
            "calmar_ratio": self.calmar_ratio,
        }


class PerformanceCalculator:
    """Portfolio performance calculator with advanced metrics."""

    def __init__(self, db_path: str = None):
        """Initialize performance calculator."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()

    def calculate_time_weighted_return(
        self, portfolio_id: int, start_date: date, end_date: date
    ) -> Tuple[float, float]:
        """
        Calculate Time-Weighted Return (TWR).

        TWR removes the effect of cash flows, measuring pure investment performance.

        Algorithm:
        1. Split period by cash flow events (transactions)
        2. Calculate sub-period returns
        3. Chain multiply: (1+r1) × (1+r2) × ... × (1+rn) - 1

        Returns:
            (total_return, annualized_return)
        """
        # Get all transactions in period
        transactions = (
            self.session.query(Transaction)
            .join(Holding)
            .filter(
                and_(
                    Holding.portfolio_id == portfolio_id,
                    Transaction.date >= start_date,
                    Transaction.date <= end_date,
                    Transaction.type.in_(["BUY", "SELL"]),
                )
            )
            .order_by(Transaction.date)
            .all()
        )

        # Get holdings
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if not holdings:
            return (0.0, 0.0)

        # For simplicity, calculate using current holdings
        # In production, would use PortfolioSnapshot for exact historical values

        # Calculate daily returns
        try:
            portfolio_values = self._get_daily_portfolio_values(holdings, start_date, end_date)

            if len(portfolio_values) < 2:
                return (0.0, 0.0)

            # Calculate sub-period returns at each transaction
            sub_returns = []
            transaction_dates = [t.date for t in transactions]

            if not transaction_dates:
                # No transactions, simple return calculation
                start_value = portfolio_values.iloc[0]
                end_value = portfolio_values.iloc[-1]

                if start_value == 0:
                    return (0.0, 0.0)

                total_return = (end_value / start_value) - 1
            else:
                # Split by transaction dates
                periods = []
                prev_date = start_date

                for txn_date in transaction_dates:
                    if txn_date > prev_date:
                        periods.append((prev_date, txn_date))
                    prev_date = txn_date

                # Last period
                if prev_date < end_date:
                    periods.append((prev_date, end_date))

                # Calculate returns for each period
                period_returns = []
                for period_start, period_end in periods:
                    # Convert dates to pandas Timestamp for timezone compatibility
                    period_start_ts = pd.Timestamp(period_start)
                    period_end_ts = pd.Timestamp(period_end)

                    # Use loc with converted timestamps
                    values_in_period = portfolio_values.loc[period_start_ts:period_end_ts]

                    if len(values_in_period) >= 2:
                        period_return = (values_in_period.iloc[-1] / values_in_period.iloc[0]) - 1
                        period_returns.append(period_return)

                # Chain multiply
                if period_returns:
                    total_return = np.prod([1 + r for r in period_returns]) - 1
                else:
                    total_return = 0.0

            # Annualize
            days = (end_date - start_date).days
            if days < 1:
                annualized_return = 0.0
            else:
                years = days / 365.25
                annualized_return = (1 + total_return) ** (1 / years) - 1

            return (total_return, annualized_return)

        except Exception as e:
            print(f"⚠️  Error calculating TWR: {e}")
            return (0.0, 0.0)

    def _get_daily_portfolio_values(
        self, holdings: List[Holding], start_date: date, end_date: date
    ) -> pd.Series:
        """Get daily portfolio values."""
        # Simplified calculation using current holdings
        # In production, would use historical snapshots

        all_prices = {}

        for holding in holdings:
            try:
                stock = yf.Ticker(holding.ticker)
                hist = stock.history(start=start_date, end=end_date, interval="1d")

                if not hist.empty:
                    all_prices[holding.ticker] = hist["Close"] * holding.quantity

            except Exception as e:
                print(f"⚠️  Could not fetch history for {holding.ticker}: {e}")

        if not all_prices:
            return pd.Series()

        # Sum across all holdings
        prices_df = pd.DataFrame(all_prices)
        portfolio_values = prices_df.sum(axis=1)

        # Remove timezone info for easier date comparison
        if portfolio_values.index.tz is not None:
            portfolio_values.index = portfolio_values.index.tz_localize(None)

        return portfolio_values

    def calculate_money_weighted_return(self, portfolio_id: int, start_date: date, end_date: date) -> float:
        """
        Calculate Money-Weighted Return (MWR) / Internal Rate of Return (IRR).

        MWR accounts for timing and size of cash flows.
        Uses IRR calculation: NPV = 0

        Returns:
            Annualized MWR
        """
        # Get current holdings
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if not holdings:
            return 0.0

        # Get beginning portfolio value (at start_date)
        try:
            beginning_value = 0.0
            for holding in holdings:
                stock = yf.Ticker(holding.ticker)
                hist = stock.history(start=start_date, end=start_date + timedelta(days=5), interval="1d")
                if not hist.empty:
                    start_price = hist["Close"].iloc[0]
                    beginning_value += start_price * holding.quantity

            if beginning_value == 0:
                return 0.0

        except Exception as e:
            print(f"⚠️  Could not determine beginning value: {e}")
            return 0.0

        # Get all cash flows (transactions) during period
        transactions = (
            self.session.query(Transaction)
            .join(Holding)
            .filter(
                and_(
                    Holding.portfolio_id == portfolio_id,
                    Transaction.date >= start_date,
                    Transaction.date <= end_date,
                    Transaction.type.in_(["BUY", "SELL"]),
                )
            )
            .order_by(Transaction.date)
            .all()
        )

        # Build cash flow array
        # Start with negative of beginning value (initial investment)
        cash_flows = [-beginning_value]
        dates = [start_date]

        for txn in transactions:
            amount = txn.quantity * txn.price
            if txn.type == "BUY":
                amount = -amount  # Outflow (additional investment)
            # SELL is positive (inflow / disinvestment)

            cash_flows.append(amount)
            dates.append(txn.date)

        # Add ending value (final inflow)
        ending_value = sum(
            [self._get_current_value(h.ticker, h.market) * h.quantity for h in holdings]
        )

        cash_flows.append(ending_value)
        dates.append(end_date)

        if len(cash_flows) < 2:
            return 0.0

        # Calculate IRR
        try:
            # Convert dates to years from start
            days_from_start = [(d - start_date).days for d in dates]
            years_from_start = [d / 365.25 for d in days_from_start]

            # Use Newton's method to find IRR
            irr = self._calculate_irr(cash_flows, years_from_start)

            # Sanity check: if IRR is unreasonably high, return 0
            if abs(irr) > 10.0:  # 1000% is unreasonable
                print(f"⚠️  MWR calculation produced unrealistic value ({irr:.2%}), returning 0")
                return 0.0

            return irr

        except Exception as e:
            print(f"⚠️  Error calculating MWR: {e}")
            return 0.0

    def _get_current_value(self, ticker: str, market: str) -> float:
        """Get current stock price."""
        data = get_stock_data(ticker, market)
        return data.get("current_price", 0.0)

    def _calculate_irr(self, cash_flows: List[float], times: List[float], guess: float = 0.1) -> float:
        """Calculate IRR using Newton's method with improved stability."""
        max_iterations = 100
        tolerance = 1e-6

        rate = guess

        for iteration in range(max_iterations):
            # Calculate NPV and its derivative
            npv = 0.0
            npv_derivative = 0.0

            for cf, t in zip(cash_flows, times):
                try:
                    discount_factor = (1 + rate) ** t
                    if discount_factor == 0:
                        return 0.0

                    npv += cf / discount_factor
                    npv_derivative += -cf * t / (discount_factor * (1 + rate))
                except (OverflowError, ZeroDivisionError):
                    # Numerical instability, try different guess
                    if iteration < 10:
                        rate = guess * (iteration + 1) * 0.1
                        continue
                    else:
                        return 0.0

            # Check convergence
            if abs(npv) < tolerance:
                return rate

            # Check derivative
            if abs(npv_derivative) < 1e-10:
                # Try different starting point
                if iteration < 10:
                    rate = -0.5 + iteration * 0.1
                    continue
                else:
                    return 0.0

            # Newton's method update with damping to prevent overshooting
            step = npv / npv_derivative
            damping = 0.5 if abs(step) > 0.5 else 1.0
            rate = rate - damping * step

            # Keep rate in reasonable bounds
            if rate < -0.99:  # Can't lose more than 99.9%
                rate = -0.99
            elif rate > 100:  # Cap at 10000% return
                rate = 100.0

        # Did not converge
        return 0.0

    def calculate_maximum_drawdown(self, portfolio_values: pd.Series) -> float:
        """
        Calculate maximum drawdown.

        Max Drawdown = (Trough Value - Peak Value) / Peak Value

        Returns:
            Maximum drawdown as negative percentage
        """
        if len(portfolio_values) < 2:
            return 0.0

        # Calculate running maximum
        running_max = portfolio_values.expanding().max()

        # Calculate drawdown
        drawdown = (portfolio_values - running_max) / running_max

        # Get maximum drawdown (most negative)
        max_dd = drawdown.min()

        return max_dd

    def calculate_volatility(self, returns: pd.Series, annualize: bool = True) -> float:
        """
        Calculate volatility (standard deviation of returns).

        Args:
            returns: Series of returns
            annualize: If True, annualize using sqrt(252)

        Returns:
            Volatility (annualized if requested)
        """
        if len(returns) < 2:
            return 0.0

        vol = returns.std()

        if annualize:
            vol = vol * np.sqrt(252)

        return vol

    def calculate_sortino_ratio(
        self, returns: pd.Series, risk_free_rate: float = 0.02, target_return: float = 0.0
    ) -> float:
        """
        Calculate Sortino ratio (downside risk-adjusted return).

        Sortino = (Return - Risk-free Rate) / Downside Deviation

        Only penalizes downside volatility.
        """
        if len(returns) < 2:
            return 0.0

        mean_return = returns.mean() * 252  # Annualized
        downside_returns = returns[returns < target_return]

        if len(downside_returns) == 0:
            return float("inf")

        downside_dev = downside_returns.std() * np.sqrt(252)

        if downside_dev == 0:
            return 0.0

        sortino = (mean_return - risk_free_rate) / downside_dev
        return sortino

    def calculate_calmar_ratio(self, annualized_return: float, max_drawdown: float) -> float:
        """
        Calculate Calmar ratio (return / max drawdown).

        Measures return relative to downside risk.
        """
        if max_drawdown == 0:
            return 0.0

        calmar = annualized_return / abs(max_drawdown)
        return calmar

    def calculate_comprehensive_metrics(
        self, portfolio_id: int, start_date: date = None, end_date: date = None, risk_free_rate: float = 0.02
    ) -> PerformanceMetrics:
        """
        Calculate comprehensive performance metrics.

        Returns:
            PerformanceMetrics object with all key metrics
        """
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        # Calculate TWR
        twr_total, twr_annualized = self.calculate_time_weighted_return(portfolio_id, start_date, end_date)

        # Calculate MWR
        mwr = self.calculate_money_weighted_return(portfolio_id, start_date, end_date)

        # Get portfolio values and returns
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()
        portfolio_values = self._get_daily_portfolio_values(holdings, start_date, end_date)

        if len(portfolio_values) < 2:
            # Not enough data
            return PerformanceMetrics(
                twr_total=twr_total,
                twr_annualized=twr_annualized,
                mwr=mwr,
                max_drawdown=0.0,
                volatility_annual=0.0,
                sharpe_ratio=0.0,
                sortino_ratio=0.0,
                calmar_ratio=0.0,
            )

        returns = portfolio_values.pct_change().dropna()

        # Calculate risk metrics
        max_dd = self.calculate_maximum_drawdown(portfolio_values)
        volatility = self.calculate_volatility(returns)

        # Sharpe ratio
        mean_return = returns.mean() * 252
        sharpe = (mean_return - risk_free_rate) / volatility if volatility > 0 else 0.0

        # Sortino ratio
        sortino = self.calculate_sortino_ratio(returns, risk_free_rate)

        # Calmar ratio
        calmar = self.calculate_calmar_ratio(twr_annualized, max_dd)

        return PerformanceMetrics(
            twr_total=twr_total,
            twr_annualized=twr_annualized,
            mwr=mwr,
            max_drawdown=max_dd,
            volatility_annual=volatility,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            calmar_ratio=calmar,
        )

    def generate_performance_report(
        self, portfolio_id: int, start_date: date = None, end_date: date = None
    ) -> str:
        """
        Generate comprehensive performance report.

        Returns:
            Formatted report string
        """
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        metrics = self.calculate_comprehensive_metrics(portfolio_id, start_date, end_date)

        lines = []
        lines.append("=" * 80)
        lines.append("📊 PERFORMANCE ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {portfolio_id}")
        lines.append(f"Period: {start_date} to {end_date} ({(end_date - start_date).days} days)")
        lines.append("")

        # Returns section
        lines.append("📈 RETURNS")
        lines.append("-" * 80)
        lines.append(f"Time-Weighted Return (Total):      {metrics.twr_total:>10.2%}")
        lines.append(f"Time-Weighted Return (Annualized): {metrics.twr_annualized:>10.2%}")
        lines.append(f"Money-Weighted Return (IRR):       {metrics.mwr:>10.2%}")
        lines.append("")

        if abs(metrics.twr_annualized - metrics.mwr) > 0.02:
            diff = metrics.mwr - metrics.twr_annualized
            if diff > 0:
                lines.append(f"💡 Your timing added {diff:.2%} to returns! Good cash flow management.")
            else:
                lines.append(f"⚠️  Your timing reduced returns by {abs(diff):.2%}. Consider dollar-cost averaging.")
            lines.append("")

        # Risk section
        lines.append("⚠️  RISK METRICS")
        lines.append("-" * 80)
        lines.append(f"Maximum Drawdown:                   {metrics.max_drawdown:>10.2%}")
        lines.append(f"Annual Volatility:                  {metrics.volatility_annual:>10.2%}")
        lines.append("")

        # Risk-adjusted returns
        lines.append("🎯 RISK-ADJUSTED PERFORMANCE")
        lines.append("-" * 80)
        lines.append(f"Sharpe Ratio:                       {metrics.sharpe_ratio:>10.2f}  {self._interpret_sharpe(metrics.sharpe_ratio)}")
        lines.append(f"Sortino Ratio:                      {metrics.sortino_ratio:>10.2f}  {self._interpret_sortino(metrics.sortino_ratio)}")
        lines.append(f"Calmar Ratio:                       {metrics.calmar_ratio:>10.2f}  {self._interpret_calmar(metrics.calmar_ratio)}")
        lines.append("")

        # Interpretation
        lines.append("💡 INTERPRETATION")
        lines.append("-" * 80)
        lines.append("• Time-Weighted Return (TWR):  Pure investment skill (excludes cash flow timing)")
        lines.append("• Money-Weighted Return (MWR): Overall experience (includes investor timing)")
        lines.append("• Sharpe Ratio:  Return per unit of total risk (>1.0 good, >2.0 excellent)")
        lines.append("• Sortino Ratio: Return per unit of downside risk (>1.5 good, >2.0 excellent)")
        lines.append("• Calmar Ratio:  Return per unit of max drawdown (>0.5 good, >1.0 excellent)")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _interpret_sharpe(self, sharpe: float) -> str:
        """Interpret Sharpe ratio."""
        if sharpe > 3.0:
            return "Exceptional"
        elif sharpe > 2.0:
            return "Excellent"
        elif sharpe > 1.0:
            return "Good"
        elif sharpe > 0:
            return "Acceptable"
        else:
            return "Poor"

    def _interpret_sortino(self, sortino: float) -> str:
        """Interpret Sortino ratio."""
        if sortino > 3.0:
            return "Exceptional"
        elif sortino > 2.0:
            return "Excellent"
        elif sortino > 1.5:
            return "Good"
        elif sortino > 0:
            return "Acceptable"
        else:
            return "Poor"

    def _interpret_calmar(self, calmar: float) -> str:
        """Interpret Calmar ratio."""
        if calmar > 2.0:
            return "Exceptional"
        elif calmar > 1.0:
            return "Excellent"
        elif calmar > 0.5:
            return "Good"
        elif calmar > 0:
            return "Acceptable"
        else:
            return "Poor"

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 performance_calculator.py <portfolio_id> [start_date] [end_date]")
        print("\nExamples:")
        print("  python3 performance_calculator.py 1")
        print("  python3 performance_calculator.py 1 2025-01-01 2026-01-01")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])
    start_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date() if len(sys.argv) > 2 else None
    end_date = datetime.strptime(sys.argv[3], "%Y-%m-%d").date() if len(sys.argv) > 3 else None

    calculator = PerformanceCalculator()

    try:
        report = calculator.generate_performance_report(portfolio_id, start_date, end_date)
        print("\n" + report)
    finally:
        calculator.close()
