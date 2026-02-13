"""
Benchmark Comparison Engine for Portfolio Copilot (Sprint 2).

Compares portfolio performance against market benchmarks and calculates
risk-adjusted performance metrics.

Key Features:
- Compare against major indices (S&P 500, NASDAQ, KOSPI)
- Calculate excess returns and tracking error
- Compute alpha, beta, correlation
- Sector-relative performance analysis
- Information ratio calculation

Benchmarks:
- SPY: S&P 500 ETF
- QQQ: NASDAQ 100 ETF
- DIA: Dow Jones Industrial Average ETF
- KOSPI: Korean Stock Price Index
- Sector ETFs: XLK, XLF, XLV, etc.
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
import yfinance as yf
from sqlalchemy import and_, func
from database import get_database, Holding, Transaction, PortfolioSnapshot


class BenchmarkComparison:
    """Container for benchmark comparison results."""

    def __init__(
        self,
        benchmark_ticker: str,
        portfolio_return: float,
        benchmark_return: float,
        excess_return: float,
        alpha: float,
        beta: float,
        correlation: float,
        tracking_error: float,
        information_ratio: float,
        sharpe_ratio_portfolio: float,
        sharpe_ratio_benchmark: float,
    ):
        self.benchmark_ticker = benchmark_ticker
        self.portfolio_return = portfolio_return
        self.benchmark_return = benchmark_return
        self.excess_return = excess_return
        self.alpha = alpha
        self.beta = beta
        self.correlation = correlation
        self.tracking_error = tracking_error
        self.information_ratio = information_ratio
        self.sharpe_ratio_portfolio = sharpe_ratio_portfolio
        self.sharpe_ratio_benchmark = sharpe_ratio_benchmark

    def __repr__(self):
        return (
            f"<BenchmarkComparison({self.benchmark_ticker}: "
            f"excess={self.excess_return:.2%}, alpha={self.alpha:.2%}, beta={self.beta:.2f})>"
        )


class BenchmarkAnalyzer:
    """Benchmark comparison and risk-adjusted performance analyzer."""

    # Common benchmarks
    BENCHMARKS = {
        "SPY": "S&P 500",
        "QQQ": "NASDAQ 100",
        "DIA": "Dow Jones",
        "IWM": "Russell 2000",
        "VTI": "Total US Stock Market",
        "^GSPC": "S&P 500 Index",
        "^IXIC": "NASDAQ Composite",
        "^KS11": "KOSPI Index",
    }

    # Sector ETFs for relative performance
    SECTOR_ETFS = {
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Finance": "XLF",
        "Consumer": "XLY",
        "Energy": "XLE",
        "Industrials": "XLI",
        "Materials": "XLB",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Communication": "XLC",
    }

    def __init__(self, db_path: str = None):
        """Initialize benchmark analyzer."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()

    def get_portfolio_returns(
        self, portfolio_id: int, start_date: date, end_date: date, frequency: str = "D"
    ) -> pd.Series:
        """
        Calculate portfolio returns over time period.

        Args:
            portfolio_id: Portfolio ID
            start_date: Start date
            end_date: End date
            frequency: 'D' for daily, 'W' for weekly, 'M' for monthly

        Returns:
            Pandas Series of returns indexed by date
        """
        # Get all holdings
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if not holdings:
            return pd.Series()

        # For simplicity, calculate based on current holdings
        # In production, would use PortfolioSnapshot for historical accuracy
        returns_data = []
        dates = pd.date_range(start=start_date, end=end_date, freq=frequency)

        for holding in holdings:
            try:
                stock = yf.Ticker(holding.ticker)
                hist = stock.history(start=start_date, end=end_date, interval="1d")

                if not hist.empty:
                    # Calculate daily returns
                    daily_returns = hist["Close"].pct_change()
                    returns_data.append(daily_returns)
            except Exception as e:
                print(f"⚠️  Could not fetch history for {holding.ticker}: {e}")

        if not returns_data:
            return pd.Series()

        # Equally weighted portfolio (simplified)
        # In production, would weight by actual position sizes
        portfolio_returns = pd.concat(returns_data, axis=1).mean(axis=1)

        return portfolio_returns

    def get_benchmark_returns(self, benchmark: str, start_date: date, end_date: date) -> pd.Series:
        """
        Get benchmark returns over time period.

        Args:
            benchmark: Benchmark ticker (e.g., 'SPY', 'QQQ')
            start_date: Start date
            end_date: End date

        Returns:
            Pandas Series of returns indexed by date
        """
        try:
            bench = yf.Ticker(benchmark)
            hist = bench.history(start=start_date, end=end_date, interval="1d")

            if hist.empty:
                print(f"⚠️  No data for benchmark {benchmark}")
                return pd.Series()

            returns = hist["Close"].pct_change()
            return returns

        except Exception as e:
            print(f"❌ Error fetching benchmark {benchmark}: {e}")
            return pd.Series()

    def calculate_beta(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate portfolio beta (systematic risk).

        Beta = Covariance(portfolio, benchmark) / Variance(benchmark)

        Beta interpretation:
        - 1.0: Moves with market
        - > 1.0: More volatile than market
        - < 1.0: Less volatile than market
        """
        # Align series by date
        aligned = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()

        if len(aligned) < 2:
            return 0.0

        covariance = np.cov(aligned["portfolio"], aligned["benchmark"])[0, 1]
        benchmark_variance = np.var(aligned["benchmark"])

        if benchmark_variance == 0:
            return 0.0

        beta = covariance / benchmark_variance
        return beta

    def calculate_alpha(
        self, portfolio_return: float, benchmark_return: float, beta: float, risk_free_rate: float = 0.02
    ) -> float:
        """
        Calculate Jensen's alpha (risk-adjusted excess return).

        Alpha = Portfolio Return - [Risk-free Rate + Beta * (Benchmark Return - Risk-free Rate)]

        Positive alpha = outperforming risk-adjusted expectations
        """
        expected_return = risk_free_rate + beta * (benchmark_return - risk_free_rate)
        alpha = portfolio_return - expected_return
        return alpha

    def calculate_tracking_error(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate tracking error (standard deviation of excess returns).

        Lower tracking error = closer tracking to benchmark
        """
        aligned = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()

        if len(aligned) < 2:
            return 0.0

        excess_returns = aligned["portfolio"] - aligned["benchmark"]
        tracking_error = np.std(excess_returns) * np.sqrt(252)  # Annualized

        return tracking_error

    def calculate_information_ratio(self, excess_return: float, tracking_error: float) -> float:
        """
        Calculate information ratio (risk-adjusted excess return).

        IR = Excess Return / Tracking Error

        Higher IR = better risk-adjusted performance vs benchmark
        """
        if tracking_error == 0:
            return 0.0

        return excess_return / tracking_error

    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio (risk-adjusted return).

        Sharpe = (Average Return - Risk-free Rate) / Std Dev of Returns

        Higher Sharpe = better risk-adjusted performance
        """
        if len(returns) < 2:
            return 0.0

        mean_return = returns.mean() * 252  # Annualized
        std_return = returns.std() * np.sqrt(252)  # Annualized

        if std_return == 0:
            return 0.0

        sharpe = (mean_return - risk_free_rate) / std_return
        return sharpe

    def compare_to_benchmark(
        self,
        portfolio_id: int,
        benchmark: str = "SPY",
        start_date: date = None,
        end_date: date = None,
        risk_free_rate: float = 0.02,
    ) -> BenchmarkComparison:
        """
        Compare portfolio performance to benchmark.

        Args:
            portfolio_id: Portfolio ID
            benchmark: Benchmark ticker (default: SPY = S&P 500)
            start_date: Start date (default: 1 year ago)
            end_date: End date (default: today)
            risk_free_rate: Annual risk-free rate (default: 2%)

        Returns:
            BenchmarkComparison object with all metrics
        """
        # Default date range: past 1 year
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        # Get returns
        portfolio_returns = self.get_portfolio_returns(portfolio_id, start_date, end_date)
        benchmark_returns = self.get_benchmark_returns(benchmark, start_date, end_date)

        if portfolio_returns.empty or benchmark_returns.empty:
            print(f"⚠️  Insufficient data for comparison")
            return None

        # Align dates
        aligned = pd.DataFrame({"portfolio": portfolio_returns, "benchmark": benchmark_returns}).dropna()

        if len(aligned) < 30:  # Need at least 30 days
            print(f"⚠️  Insufficient data points ({len(aligned)}), need at least 30 days")
            return None

        # Calculate cumulative returns
        portfolio_return = (1 + aligned["portfolio"]).prod() - 1
        benchmark_return = (1 + aligned["benchmark"]).prod() - 1
        excess_return = portfolio_return - benchmark_return

        # Calculate metrics
        beta = self.calculate_beta(aligned["portfolio"], aligned["benchmark"])
        alpha = self.calculate_alpha(portfolio_return, benchmark_return, beta, risk_free_rate)

        correlation = aligned["portfolio"].corr(aligned["benchmark"])
        tracking_error = self.calculate_tracking_error(aligned["portfolio"], aligned["benchmark"])
        information_ratio = self.calculate_information_ratio(excess_return, tracking_error)

        sharpe_portfolio = self.calculate_sharpe_ratio(aligned["portfolio"], risk_free_rate)
        sharpe_benchmark = self.calculate_sharpe_ratio(aligned["benchmark"], risk_free_rate)

        return BenchmarkComparison(
            benchmark_ticker=benchmark,
            portfolio_return=portfolio_return,
            benchmark_return=benchmark_return,
            excess_return=excess_return,
            alpha=alpha,
            beta=beta,
            correlation=correlation,
            tracking_error=tracking_error,
            information_ratio=information_ratio,
            sharpe_ratio_portfolio=sharpe_portfolio,
            sharpe_ratio_benchmark=sharpe_benchmark,
        )

    def multi_benchmark_comparison(
        self, portfolio_id: int, benchmarks: List[str] = None, start_date: date = None, end_date: date = None
    ) -> Dict[str, BenchmarkComparison]:
        """
        Compare portfolio against multiple benchmarks.

        Args:
            portfolio_id: Portfolio ID
            benchmarks: List of benchmark tickers (default: SPY, QQQ)
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary mapping benchmark ticker to BenchmarkComparison
        """
        if benchmarks is None:
            benchmarks = ["SPY", "QQQ"]

        results = {}

        for benchmark in benchmarks:
            print(f"📊 Comparing to {benchmark} ({self.BENCHMARKS.get(benchmark, benchmark)})...")
            comparison = self.compare_to_benchmark(portfolio_id, benchmark, start_date, end_date)

            if comparison:
                results[benchmark] = comparison

        return results

    def generate_benchmark_report(
        self, portfolio_id: int, benchmarks: List[str] = None, start_date: date = None, end_date: date = None
    ) -> str:
        """
        Generate comprehensive benchmark comparison report.

        Returns:
            Formatted report string
        """
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        if benchmarks is None:
            benchmarks = ["SPY", "QQQ"]

        # Get comparisons
        comparisons = self.multi_benchmark_comparison(portfolio_id, benchmarks, start_date, end_date)

        if not comparisons:
            return "❌ Could not generate benchmark report (insufficient data)"

        # Build report
        lines = []
        lines.append("=" * 80)
        lines.append("📊 BENCHMARK COMPARISON REPORT")
        lines.append("=" * 80)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {portfolio_id}")
        lines.append(f"Period: {start_date} to {end_date} ({(end_date - start_date).days} days)")
        lines.append("")

        # Summary table
        lines.append("📈 PERFORMANCE SUMMARY")
        lines.append("-" * 80)
        lines.append(
            f"{'Benchmark':<15} {'Return':<12} {'Excess':<12} {'Alpha':<10} {'Beta':<10} {'Sharpe':<10}"
        )
        lines.append("-" * 80)

        for bench_ticker, comp in comparisons.items():
            bench_name = self.BENCHMARKS.get(bench_ticker, bench_ticker)[:14]
            lines.append(
                f"{bench_name:<15} "
                f"{comp.benchmark_return:>10.2%} "
                f"{comp.excess_return:>10.2%} "
                f"{comp.alpha:>9.2%} "
                f"{comp.beta:>9.2f} "
                f"{comp.sharpe_ratio_benchmark:>9.2f}"
            )

        # Portfolio performance
        if comparisons:
            first_comp = list(comparisons.values())[0]
            lines.append("-" * 80)
            lines.append(
                f"{'Portfolio':<15} "
                f"{first_comp.portfolio_return:>10.2%} "
                f"{'':>10} "
                f"{'':>9} "
                f"{'':>9} "
                f"{first_comp.sharpe_ratio_portfolio:>9.2f}"
            )
            lines.append("")

        # Detailed metrics
        for bench_ticker, comp in comparisons.items():
            bench_name = self.BENCHMARKS.get(bench_ticker, bench_ticker)

            lines.append(f"📊 {bench_name} ({bench_ticker}) DETAILED ANALYSIS")
            lines.append("-" * 80)
            lines.append(f"Excess Return:      {comp.excess_return:>10.2%}")
            lines.append(f"Alpha (Jensen):     {comp.alpha:>10.2%}  {'✅ Outperforming' if comp.alpha > 0 else '⚠️  Underperforming'}")
            lines.append(f"Beta:               {comp.beta:>10.2f}  {self._interpret_beta(comp.beta)}")
            lines.append(f"Correlation:        {comp.correlation:>10.2f}")
            lines.append(f"Tracking Error:     {comp.tracking_error:>10.2%}")
            lines.append(f"Information Ratio:  {comp.information_ratio:>10.2f}  {self._interpret_ir(comp.information_ratio)}")
            lines.append("")

        # Recommendations
        lines.append("💡 INSIGHTS & RECOMMENDATIONS")
        lines.append("-" * 80)

        if comparisons:
            primary = list(comparisons.values())[0]

            if primary.alpha > 0.05:
                lines.append(f"✅ Strong alpha ({primary.alpha:.2%}) - Portfolio is generating excess returns!")
            elif primary.alpha < -0.05:
                lines.append(f"⚠️  Negative alpha ({primary.alpha:.2%}) - Consider reviewing strategy")

            if primary.beta > 1.2:
                lines.append(f"⚠️  High beta ({primary.beta:.2f}) - Portfolio is more volatile than market")
            elif primary.beta < 0.8:
                lines.append(f"✅ Low beta ({primary.beta:.2f}) - Portfolio is more stable than market")

            if primary.sharpe_ratio_portfolio > primary.sharpe_ratio_benchmark:
                diff = primary.sharpe_ratio_portfolio - primary.sharpe_ratio_benchmark
                lines.append(f"✅ Better risk-adjusted returns (+{diff:.2f} Sharpe) than benchmark")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _interpret_beta(self, beta: float) -> str:
        """Interpret beta value."""
        if beta > 1.2:
            return "High volatility"
        elif beta < 0.8:
            return "Low volatility"
        else:
            return "Market-like volatility"

    def _interpret_ir(self, ir: float) -> str:
        """Interpret information ratio."""
        if ir > 0.5:
            return "Excellent"
        elif ir > 0.25:
            return "Good"
        elif ir > 0:
            return "Modest"
        else:
            return "Poor"

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 benchmark_analyzer.py <portfolio_id> [benchmark1] [benchmark2] ...")
        print("\nExamples:")
        print("  python3 benchmark_analyzer.py 1")
        print("  python3 benchmark_analyzer.py 1 SPY QQQ")
        print("\nCommon Benchmarks:")
        for ticker, name in BenchmarkAnalyzer.BENCHMARKS.items():
            print(f"  {ticker:<10} - {name}")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])
    benchmarks = sys.argv[2:] if len(sys.argv) > 2 else ["SPY", "QQQ"]

    analyzer = BenchmarkAnalyzer()

    try:
        report = analyzer.generate_benchmark_report(portfolio_id, benchmarks)
        print("\n" + report)
    finally:
        analyzer.close()
