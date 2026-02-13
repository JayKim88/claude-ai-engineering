"""
Risk Metrics Calculator for Portfolio Copilot (Sprint 3).

Comprehensive risk analysis including VaR, correlation analysis,
concentration risk, and diversification scoring.

Key Features:
- Value at Risk (VaR) - historical simulation method
- Conditional VaR (CVaR / Expected Shortfall)
- Correlation matrix and high-correlation warnings
- Concentration risk (sector, single stock, top holdings)
- Diversification score
- Risk warnings and recommendations

Risk Metrics:
- VaR: Maximum loss at given confidence level (e.g., 95%)
- CVaR: Average loss beyond VaR threshold
- Concentration: % in single sector/stock
- Diversification: Herfindahl index-based score
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
import yfinance as yf
from sqlalchemy import func
from database import get_database, Holding
from data_fetcher import get_stock_data


class RiskWarning:
    """Container for risk warning."""

    def __init__(self, level: str, category: str, message: str, recommendation: str = ""):
        self.level = level  # 'HIGH', 'MEDIUM', 'LOW'
        self.category = category  # 'CONCENTRATION', 'CORRELATION', 'VOLATILITY', 'VAR'
        self.message = message
        self.recommendation = recommendation

    def __repr__(self):
        return f"<RiskWarning({self.level}: {self.category} - {self.message})>"


class RiskMetricsCalculator:
    """Comprehensive risk metrics calculator."""

    def __init__(self, db_path: str = None):
        """Initialize risk metrics calculator."""
        self.db = get_database(db_path)
        self.session = self.db.get_session()

    def calculate_var(
        self,
        portfolio_id: int,
        confidence: float = 0.95,
        horizon_days: int = 1,
        lookback_days: int = 252,
    ) -> Dict:
        """
        Calculate Value at Risk (VaR) using historical simulation.

        Args:
            portfolio_id: Portfolio ID
            confidence: Confidence level (0.95 = 95%)
            horizon_days: Time horizon in days (default 1 day)
            lookback_days: Historical data window (default 252 trading days = 1 year)

        Returns:
            {
                'var_95_pct': float,      # VaR as percentage
                'var_95_amount': float,   # VaR in dollar amount
                'var_99_pct': float,
                'var_99_amount': float,
                'cvar_95': float,         # Expected shortfall (CVaR)
                'worst_day_loss': float,  # Worst historical loss
                'portfolio_value': float
            }
        """
        # Get holdings
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if not holdings:
            return {}

        # Get historical returns for all holdings
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days * 1.5)  # Extra buffer

        returns_data = []
        weights = []
        total_value = 0.0

        for holding in holdings:
            try:
                stock = yf.Ticker(holding.ticker)
                hist = stock.history(start=start_date, end=end_date, interval="1d")

                if not hist.empty:
                    # Get daily returns
                    daily_returns = hist["Close"].pct_change().dropna()

                    # Calculate position value
                    current_price = hist["Close"].iloc[-1]
                    position_value = current_price * holding.quantity
                    total_value += position_value

                    returns_data.append(daily_returns)
                    weights.append(position_value)

            except Exception as e:
                print(f"⚠️  Could not fetch data for {holding.ticker}: {e}")

        if not returns_data or total_value == 0:
            return {}

        # Normalize weights
        weights = np.array(weights) / total_value

        # Align returns
        returns_df = pd.DataFrame({f"stock_{i}": ret for i, ret in enumerate(returns_data)})
        returns_df = returns_df.dropna()

        if len(returns_df) < 30:
            print(f"⚠️  Insufficient data ({len(returns_df)} days), need at least 30")
            return {}

        # Calculate portfolio returns (weighted)
        portfolio_returns = (returns_df * weights).sum(axis=1)

        # Scale to horizon
        if horizon_days > 1:
            portfolio_returns = portfolio_returns * np.sqrt(horizon_days)

        # Calculate VaR at different confidence levels
        var_95_pct = np.percentile(portfolio_returns, (1 - 0.95) * 100)
        var_99_pct = np.percentile(portfolio_returns, (1 - 0.99) * 100)

        # Calculate CVaR (Conditional VaR / Expected Shortfall)
        # Average of losses beyond VaR threshold
        losses_beyond_var = portfolio_returns[portfolio_returns <= var_95_pct]
        cvar_95_pct = losses_beyond_var.mean() if len(losses_beyond_var) > 0 else var_95_pct

        # Convert to dollar amounts
        var_95_amount = total_value * abs(var_95_pct)
        var_99_amount = total_value * abs(var_99_pct)
        cvar_95_amount = total_value * abs(cvar_95_pct)

        # Worst day
        worst_day_loss = portfolio_returns.min()
        worst_day_amount = total_value * abs(worst_day_loss)

        return {
            "var_95_pct": var_95_pct,
            "var_95_amount": var_95_amount,
            "var_99_pct": var_99_pct,
            "var_99_amount": var_99_amount,
            "cvar_95_pct": cvar_95_pct,
            "cvar_95_amount": cvar_95_amount,
            "worst_day_loss_pct": worst_day_loss,
            "worst_day_loss_amount": worst_day_amount,
            "portfolio_value": total_value,
            "horizon_days": horizon_days,
            "confidence_95": 0.95,
            "confidence_99": 0.99,
        }

    def calculate_correlation_matrix(self, portfolio_id: int, lookback_days: int = 252) -> pd.DataFrame:
        """
        Calculate correlation matrix for portfolio holdings.

        Args:
            portfolio_id: Portfolio ID
            lookback_days: Historical data window

        Returns:
            Pandas DataFrame with correlation matrix
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if len(holdings) < 2:
            return pd.DataFrame()

        # Get returns
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days * 1.5)

        returns_dict = {}

        for holding in holdings:
            try:
                stock = yf.Ticker(holding.ticker)
                hist = stock.history(start=start_date, end=end_date, interval="1d")

                if not hist.empty:
                    returns = hist["Close"].pct_change().dropna()
                    returns_dict[holding.ticker] = returns

            except Exception as e:
                print(f"⚠️  Could not fetch data for {holding.ticker}: {e}")

        if len(returns_dict) < 2:
            return pd.DataFrame()

        # Build returns dataframe and calculate correlation
        returns_df = pd.DataFrame(returns_dict).dropna()
        correlation_matrix = returns_df.corr()

        return correlation_matrix

    def find_high_correlation_pairs(
        self, correlation_matrix: pd.DataFrame, threshold: float = 0.8
    ) -> List[Tuple[str, str, float]]:
        """
        Find pairs of stocks with high correlation.

        Args:
            correlation_matrix: Correlation matrix
            threshold: Correlation threshold (default 0.8)

        Returns:
            List of (ticker1, ticker2, correlation) tuples
        """
        high_corr_pairs = []

        for i in range(len(correlation_matrix)):
            for j in range(i + 1, len(correlation_matrix)):
                ticker1 = correlation_matrix.index[i]
                ticker2 = correlation_matrix.columns[j]
                corr = correlation_matrix.iloc[i, j]

                if abs(corr) >= threshold:
                    high_corr_pairs.append((ticker1, ticker2, corr))

        # Sort by absolute correlation (descending)
        high_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

        return high_corr_pairs

    def calculate_concentration_risk(self, portfolio_id: int) -> Dict:
        """
        Calculate concentration risk metrics.

        Returns:
            {
                'sector_concentration': {sector: weight},
                'max_sector_weight': float,
                'max_stock_weight': float,
                'top_3_weight': float,
                'top_5_weight': float,
                'herfindahl_index': float
            }
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()

        if not holdings:
            return {}

        # Calculate total portfolio value
        total_value = 0.0
        sector_values = {}
        stock_weights = []

        for holding in holdings:
            try:
                current_data = get_stock_data(holding.ticker, holding.market)
                current_price = current_data.get("current_price", 0)

                if current_price == 0:
                    continue

                position_value = current_price * holding.quantity
                total_value += position_value

                # Track by sector
                sector = holding.sector or "Unknown"
                sector_values[sector] = sector_values.get(sector, 0) + position_value

                stock_weights.append(position_value)

            except Exception as e:
                print(f"⚠️  Error processing {holding.ticker}: {e}")

        if total_value == 0:
            return {}

        # Calculate sector concentration
        sector_weights = {sector: value / total_value for sector, value in sector_values.items()}
        max_sector_weight = max(sector_weights.values()) if sector_weights else 0

        # Calculate stock concentration
        stock_weights_sorted = sorted([w / total_value for w in stock_weights], reverse=True)
        max_stock_weight = stock_weights_sorted[0] if stock_weights_sorted else 0
        top_3_weight = sum(stock_weights_sorted[:3]) if len(stock_weights_sorted) >= 3 else sum(stock_weights_sorted)
        top_5_weight = sum(stock_weights_sorted[:5]) if len(stock_weights_sorted) >= 5 else sum(stock_weights_sorted)

        # Herfindahl-Hirschman Index (HHI)
        # Sum of squared weights (ranges 0-1, lower = more diversified)
        hhi = sum([w ** 2 for w in stock_weights_sorted])

        return {
            "sector_concentration": sector_weights,
            "max_sector_weight": max_sector_weight,
            "max_stock_weight": max_stock_weight,
            "top_3_weight": top_3_weight,
            "top_5_weight": top_5_weight,
            "herfindahl_index": hhi,
            "num_holdings": len(holdings),
        }

    def calculate_diversification_score(self, concentration: Dict) -> float:
        """
        Calculate diversification score (0-100).

        Higher score = better diversified

        Based on:
        - Number of holdings
        - Herfindahl Index
        - Sector concentration
        - Top holdings concentration
        """
        if not concentration:
            return 0.0

        score = 100.0

        # Penalty for high HHI (max -40 points)
        hhi = concentration.get("herfindahl_index", 1.0)
        hhi_penalty = min(hhi * 40, 40)
        score -= hhi_penalty

        # Penalty for high sector concentration (max -30 points)
        max_sector = concentration.get("max_sector_weight", 1.0)
        if max_sector > 0.5:
            score -= 30
        elif max_sector > 0.4:
            score -= 20
        elif max_sector > 0.3:
            score -= 10

        # Penalty for high single stock weight (max -20 points)
        max_stock = concentration.get("max_stock_weight", 1.0)
        if max_stock > 0.3:
            score -= 20
        elif max_stock > 0.2:
            score -= 10

        # Bonus for number of holdings (max +20 points)
        num_holdings = concentration.get("num_holdings", 0)
        if num_holdings >= 20:
            score += 20
        elif num_holdings >= 10:
            score += 10

        return max(0, min(100, score))

    def generate_risk_warnings(
        self,
        portfolio_id: int,
        var_results: Dict = None,
        concentration: Dict = None,
        correlation_matrix: pd.DataFrame = None,
    ) -> List[RiskWarning]:
        """
        Generate risk warnings based on analysis.

        Returns:
            List of RiskWarning objects
        """
        warnings = []

        # VaR warnings
        if var_results:
            var_95_pct = abs(var_results.get("var_95_pct", 0))

            if var_95_pct > 0.05:  # > 5% daily loss
                warnings.append(
                    RiskWarning(
                        level="HIGH",
                        category="VAR",
                        message=f"High VaR: {var_95_pct:.2%} daily loss at 95% confidence",
                        recommendation="Consider reducing position sizes or adding defensive stocks",
                    )
                )
            elif var_95_pct > 0.03:
                warnings.append(
                    RiskWarning(
                        level="MEDIUM",
                        category="VAR",
                        message=f"Moderate VaR: {var_95_pct:.2%} daily loss possible",
                        recommendation="Monitor volatility and consider hedging strategies",
                    )
                )

        # Concentration warnings
        if concentration:
            max_sector = concentration.get("max_sector_weight", 0)
            max_stock = concentration.get("max_stock_weight", 0)

            if max_sector > 0.5:
                sector_name = max(concentration["sector_concentration"], key=concentration["sector_concentration"].get)
                warnings.append(
                    RiskWarning(
                        level="HIGH",
                        category="CONCENTRATION",
                        message=f"{sector_name} sector {max_sector:.1%} of portfolio - excessive concentration",
                        recommendation="Diversify into other sectors to reduce sector-specific risk",
                    )
                )

            if max_stock > 0.3:
                warnings.append(
                    RiskWarning(
                        level="HIGH",
                        category="CONCENTRATION",
                        message=f"Single stock {max_stock:.1%} of portfolio - high concentration risk",
                        recommendation="No single stock should exceed 20-25% of portfolio",
                    )
                )

        # Correlation warnings
        if correlation_matrix is not None and not correlation_matrix.empty:
            high_corr = self.find_high_correlation_pairs(correlation_matrix, threshold=0.9)

            if high_corr:
                for ticker1, ticker2, corr in high_corr[:3]:  # Top 3
                    warnings.append(
                        RiskWarning(
                            level="MEDIUM",
                            category="CORRELATION",
                            message=f"{ticker1} and {ticker2} highly correlated ({corr:.2f}) - redundant exposure",
                            recommendation="Consider replacing one with uncorrelated asset",
                        )
                    )

        return warnings

    def generate_risk_report(self, portfolio_id: int) -> str:
        """
        Generate comprehensive risk report.

        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("⚠️  PORTFOLIO RISK ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Portfolio ID: {portfolio_id}")
        lines.append("")

        # VaR Analysis
        print("📊 Calculating VaR...")
        var_results = self.calculate_var(portfolio_id)

        if var_results:
            lines.append("💰 VALUE AT RISK (VaR)")
            lines.append("-" * 80)
            lines.append(f"Portfolio Value:        ${var_results['portfolio_value']:>12,.2f}")
            lines.append(f"Time Horizon:           {var_results['horizon_days']:>13} day(s)")
            lines.append("")
            lines.append(f"VaR (95% confidence):   ${var_results['var_95_amount']:>12,.2f}  ({var_results['var_95_pct']:>6.2%})")
            lines.append(f"VaR (99% confidence):   ${var_results['var_99_amount']:>12,.2f}  ({var_results['var_99_pct']:>6.2%})")
            lines.append(f"CVaR (Expected Loss):   ${var_results['cvar_95_amount']:>12,.2f}  ({var_results['cvar_95_pct']:>6.2%})")
            lines.append(f"Worst Historical Day:   ${var_results['worst_day_loss_amount']:>12,.2f}  ({var_results['worst_day_loss_pct']:>6.2%})")
            lines.append("")
            lines.append("💡 Interpretation:")
            lines.append(f"   There is a 5% chance of losing more than ${var_results['var_95_amount']:,.2f} in one day")
            lines.append("")

        # Concentration Analysis
        print("📊 Analyzing concentration...")
        concentration = self.calculate_concentration_risk(portfolio_id)

        if concentration:
            lines.append("🎯 CONCENTRATION RISK")
            lines.append("-" * 80)
            lines.append(f"Number of Holdings:     {concentration['num_holdings']:>14}")
            lines.append(f"Max Single Stock:       {concentration['max_stock_weight']:>13.1%}")
            lines.append(f"Max Single Sector:      {concentration['max_sector_weight']:>13.1%}")
            lines.append(f"Top 3 Holdings:         {concentration['top_3_weight']:>13.1%}")
            lines.append(f"Top 5 Holdings:         {concentration['top_5_weight']:>13.1%}")
            lines.append(f"Herfindahl Index:       {concentration['herfindahl_index']:>14.3f}  (lower = better)")
            lines.append("")

            # Diversification score
            div_score = self.calculate_diversification_score(concentration)
            lines.append(f"Diversification Score:  {div_score:>13.0f}/100  {self._interpret_div_score(div_score)}")
            lines.append("")

            # Sector breakdown
            if concentration["sector_concentration"]:
                lines.append("📊 Sector Allocation:")
                for sector, weight in sorted(
                    concentration["sector_concentration"].items(), key=lambda x: x[1], reverse=True
                ):
                    lines.append(f"   {sector:<20} {weight:>6.1%}")
                lines.append("")

        # Correlation Analysis
        print("📊 Calculating correlations...")
        corr_matrix = self.calculate_correlation_matrix(portfolio_id)

        if not corr_matrix.empty:
            high_corr = self.find_high_correlation_pairs(corr_matrix, threshold=0.8)

            if high_corr:
                lines.append("🔗 HIGH CORRELATION PAIRS")
                lines.append("-" * 80)
                for ticker1, ticker2, corr in high_corr[:5]:
                    lines.append(f"   {ticker1} ↔ {ticker2}:  {corr:>6.2f}  {'⚠️  Very High' if abs(corr) > 0.9 else 'High'}")
                lines.append("")

        # Risk Warnings
        warnings = self.generate_risk_warnings(portfolio_id, var_results, concentration, corr_matrix)

        if warnings:
            lines.append("⚠️  RISK WARNINGS")
            lines.append("-" * 80)

            high_warnings = [w for w in warnings if w.level == "HIGH"]
            medium_warnings = [w for w in warnings if w.level == "MEDIUM"]

            if high_warnings:
                lines.append("🔴 HIGH PRIORITY:")
                for w in high_warnings:
                    lines.append(f"   • {w.message}")
                    if w.recommendation:
                        lines.append(f"     → {w.recommendation}")
                lines.append("")

            if medium_warnings:
                lines.append("🟡 MEDIUM PRIORITY:")
                for w in medium_warnings:
                    lines.append(f"   • {w.message}")
                    if w.recommendation:
                        lines.append(f"     → {w.recommendation}")
                lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _interpret_div_score(self, score: float) -> str:
        """Interpret diversification score."""
        if score >= 80:
            return "✅ Excellent"
        elif score >= 60:
            return "✅ Good"
        elif score >= 40:
            return "🟡 Fair"
        else:
            return "⚠️  Poor"

    def close(self):
        """Close database session."""
        self.session.close()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 risk_metrics.py <portfolio_id>")
        print("\nExample:")
        print("  python3 risk_metrics.py 1")
        sys.exit(1)

    portfolio_id = int(sys.argv[1])

    calculator = RiskMetricsCalculator()

    try:
        report = calculator.generate_risk_report(portfolio_id)
        print("\n" + report)
    finally:
        calculator.close()
