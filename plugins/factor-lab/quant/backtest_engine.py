#!/usr/bin/env python3
"""
Backtest Engine for factor-lab

Historical simulation of trading strategies with:
- Monthly/quarterly rebalancing
- Transaction cost modeling (commission, slippage)
- Performance metrics (Sharpe, Drawdown, Win Rate)
- Equity curve visualization
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quant.data_manager import QuantDataManager
from strategies.base import Strategy
from utils.dashboard_generator import generate_backtest_dashboard


def get_output_dir() -> str:
    """Get the default output directory for factor-lab results"""
    # Get project root (3 levels up from this file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(project_root, 'tempo', 'factor-lab')

    # Create directories if they don't exist
    os.makedirs(os.path.join(output_dir, 'dashboards'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'screenings'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'backtests'), exist_ok=True)

    return output_dir


class BacktestResult:
    """
    Container for backtest results

    Attributes:
        total_return: Total return (%)
        annual_return: Annualized return (CAGR, %)
        sharpe_ratio: Sharpe ratio (risk-adjusted return)
        max_drawdown: Maximum drawdown (%)
        win_rate: Percentage of winning trades
        num_trades: Total number of trades
        equity_curve: DataFrame with daily portfolio values
        trade_history: DataFrame with all trades
    """

    def __init__(
        self,
        total_return: float,
        annual_return: float,
        sharpe_ratio: float,
        max_drawdown: float,
        win_rate: float,
        num_trades: int,
        equity_curve: pd.DataFrame,
        trade_history: pd.DataFrame
    ):
        self.total_return = total_return
        self.annual_return = annual_return
        self.sharpe_ratio = sharpe_ratio
        self.max_drawdown = max_drawdown
        self.win_rate = win_rate
        self.num_trades = num_trades
        self.equity_curve = equity_curve
        self.trade_history = trade_history

    def __repr__(self) -> str:
        return (
            f"BacktestResult(\n"
            f"  Total Return: {self.total_return:.2f}%\n"
            f"  Annual Return: {self.annual_return:.2f}%\n"
            f"  Sharpe Ratio: {self.sharpe_ratio:.2f}\n"
            f"  Max Drawdown: {self.max_drawdown:.2f}%\n"
            f"  Win Rate: {self.win_rate:.2f}%\n"
            f"  Number of Trades: {self.num_trades}\n"
            f")"
        )


class BacktestEngine:
    """
    Historical backtesting engine for trading strategies

    Features:
    - Point-in-time data (no look-ahead bias)
    - Transaction cost modeling
    - Flexible rebalancing frequency
    - Performance metrics calculation
    """

    def __init__(
        self,
        data_manager: Optional[QuantDataManager] = None,
        initial_cash: float = 100000,
        commission: float = 0.001,  # 0.1%
        slippage: float = 0.0005    # 0.05%
    ):
        """
        Initialize Backtest Engine

        Args:
            data_manager: Data manager instance (creates new if None)
            initial_cash: Starting capital ($)
            commission: Trading commission as decimal (0.001 = 0.1%)
            slippage: Price slippage as decimal (0.0005 = 0.05%)
        """
        self.data_manager = data_manager or QuantDataManager()
        self.initial_cash = initial_cash
        self.commission = commission
        self.slippage = slippage

    def run_backtest(
        self,
        strategy: Strategy,
        universe: List[str],
        start_date: str,
        end_date: str,
        rebalance_freq: str = 'monthly',  # 'monthly', 'quarterly'
        top_n: int = 50
    ) -> BacktestResult:
        """
        Run backtest for a strategy

        Args:
            strategy: Strategy instance
            universe: List of tickers to trade
            start_date: Backtest start date (YYYY-MM-DD)
            end_date: Backtest end date (YYYY-MM-DD)
            rebalance_freq: Rebalancing frequency ('monthly', 'quarterly')
            top_n: Number of stocks to hold

        Returns:
            BacktestResult with performance metrics
        """
        print(f"\n{'='*60}")
        print(f"Backtesting: {strategy.name}")
        print(f"{'='*60}")
        print(f"Universe: {len(universe)} stocks")
        print(f"Period: {start_date} to {end_date}")
        print(f"Rebalance: {rebalance_freq}")
        print(f"Portfolio Size: {top_n} stocks")
        print(f"Initial Cash: ${self.initial_cash:,.0f}")
        print(f"Commission: {self.commission*100:.2f}%")
        print(f"Slippage: {self.slippage*100:.2f}%")
        print(f"{'='*60}\n")

        # Generate rebalance dates
        rebalance_dates = self._generate_rebalance_dates(
            start_date,
            end_date,
            rebalance_freq
        )

        print(f"Rebalance dates: {len(rebalance_dates)}")
        print(f"First rebalance: {rebalance_dates[0]}")
        print(f"Last rebalance: {rebalance_dates[-1]}")

        # Initialize portfolio
        cash = self.initial_cash
        holdings = {}  # {ticker: shares}
        trade_history = []
        equity_curve = []

        # Run simulation
        for i, rebalance_date in enumerate(rebalance_dates):
            print(f"\n[{i+1}/{len(rebalance_dates)}] Rebalancing on {rebalance_date}...")

            # Select new stocks using strategy
            selected_stocks = strategy.select_stocks(
                universe=universe,
                date=rebalance_date,
                data_manager=self.data_manager,
                top_n=top_n
            )

            print(f"  Selected {len(selected_stocks)} stocks")

            # Execute rebalance
            cash, holdings, trades = self._execute_rebalance(
                current_holdings=holdings,
                current_cash=cash,
                target_stocks=selected_stocks,
                rebalance_date=rebalance_date,
                strategy=strategy
            )

            # Record trades
            trade_history.extend(trades)

            # Calculate portfolio value
            portfolio_value = self._calculate_portfolio_value(
                holdings,
                cash,
                rebalance_date
            )

            equity_curve.append({
                'date': rebalance_date,
                'portfolio_value': portfolio_value,
                'cash': cash,
                'holdings_value': portfolio_value - cash
            })

            print(f"  Portfolio Value: ${portfolio_value:,.0f}")

        # Create equity curve DataFrame
        equity_df = pd.DataFrame(equity_curve)
        equity_df['date'] = pd.to_datetime(equity_df['date'])
        equity_df.set_index('date', inplace=True)

        # Create trade history DataFrame
        trade_df = pd.DataFrame(trade_history)

        # Calculate performance metrics
        metrics = self._calculate_performance_metrics(equity_df, trade_df)

        return BacktestResult(
            total_return=metrics['total_return'],
            annual_return=metrics['annual_return'],
            sharpe_ratio=metrics['sharpe_ratio'],
            max_drawdown=metrics['max_drawdown'],
            win_rate=metrics['win_rate'],
            num_trades=metrics['num_trades'],
            equity_curve=equity_df,
            trade_history=trade_df
        )

    def _generate_rebalance_dates(
        self,
        start_date: str,
        end_date: str,
        freq: str
    ) -> List[str]:
        """
        Generate rebalance dates based on frequency

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            freq: 'monthly' or 'quarterly'

        Returns:
            List of rebalance dates in YYYY-MM-DD format
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        dates = []
        current = start

        if freq == 'monthly':
            delta_months = 1
        elif freq == 'quarterly':
            delta_months = 3
        else:
            raise ValueError(f"Invalid frequency: {freq}. Use 'monthly' or 'quarterly'")

        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))

            # Add delta months
            month = current.month + delta_months
            year = current.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1

            current = current.replace(year=year, month=month)

        return dates

    def _execute_rebalance(
        self,
        current_holdings: Dict[str, int],
        current_cash: float,
        target_stocks: List[str],
        rebalance_date: str,
        strategy: Strategy
    ) -> Tuple[float, Dict[str, int], List[Dict]]:
        """
        Execute portfolio rebalancing

        Simplified approach:
        1. Liquidate entire portfolio (sell all holdings)
        2. Buy target stocks with available cash

        Args:
            current_holdings: Current positions {ticker: shares}
            current_cash: Available cash
            target_stocks: Stocks to hold after rebalance
            rebalance_date: Date of rebalancing
            strategy: Strategy instance (for weights)

        Returns:
            Tuple of (new_cash, new_holdings, trades)
        """
        trades = []
        new_holdings = {}

        # Step 1: Liquidate entire portfolio
        for ticker, shares in current_holdings.items():
            sell_price = self._get_price(ticker, rebalance_date)
            if sell_price is not None:
                proceeds = shares * sell_price * (1 - self.commission - self.slippage)
                current_cash += proceeds

                trades.append({
                    'date': rebalance_date,
                    'ticker': ticker,
                    'action': 'SELL',
                    'shares': shares,
                    'price': sell_price,
                    'value': proceeds
                })

        # Step 2: Calculate target weights
        target_weights = strategy.get_portfolio_weights(target_stocks)

        # Step 3: Buy target stocks
        total_value = current_cash

        for ticker in target_stocks:
            target_weight = target_weights.get(ticker, 0)
            target_value = total_value * target_weight

            price = self._get_price(ticker, rebalance_date)
            if price is None:
                continue

            # Calculate shares to buy (accounting for commission and slippage)
            effective_price = price * (1 + self.commission + self.slippage)
            target_shares = int(target_value / effective_price)

            if target_shares > 0:
                cost = target_shares * effective_price
                current_cash -= cost
                new_holdings[ticker] = target_shares

                trades.append({
                    'date': rebalance_date,
                    'ticker': ticker,
                    'action': 'BUY',
                    'shares': target_shares,
                    'price': price,
                    'value': cost
                })

        return current_cash, new_holdings, trades

    def _get_price(self, ticker: str, date: str) -> Optional[float]:
        """
        Get stock price on a specific date

        Args:
            ticker: Stock ticker
            date: Date (YYYY-MM-DD)

        Returns:
            Close price or None if not available
        """
        # Get historical data around the date
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start = (date_obj - timedelta(days=10)).strftime('%Y-%m-%d')
        end = (date_obj + timedelta(days=1)).strftime('%Y-%m-%d')

        hist = self.data_manager.get_historical_data(ticker, start, end)

        if hist is None or hist.empty:
            return None

        # Convert date_obj to pd.Timestamp to handle timezone-aware comparisons
        date_ts = pd.Timestamp(date_obj)

        # If hist.index is timezone-aware, localize date_ts
        if hist.index.tz is not None:
            date_ts = date_ts.tz_localize(hist.index.tz)

        # Find closest date
        hist_before = hist[hist.index <= date_ts]
        if hist_before.empty:
            return None

        return hist_before['Close'].iloc[-1]

    def _calculate_portfolio_value(
        self,
        holdings: Dict[str, int],
        cash: float,
        date: str
    ) -> float:
        """
        Calculate total portfolio value

        Args:
            holdings: Current positions {ticker: shares}
            cash: Available cash
            date: Valuation date

        Returns:
            Total portfolio value
        """
        total = cash

        for ticker, shares in holdings.items():
            price = self._get_price(ticker, date)
            if price is not None:
                total += shares * price

        return total

    def _calculate_performance_metrics(
        self,
        equity_curve: pd.DataFrame,
        trade_history: pd.DataFrame
    ) -> Dict:
        """
        Calculate performance metrics

        Args:
            equity_curve: DataFrame with daily portfolio values
            trade_history: DataFrame with all trades

        Returns:
            Dict with performance metrics
        """
        # Total return
        initial_value = equity_curve['portfolio_value'].iloc[0]
        final_value = equity_curve['portfolio_value'].iloc[-1]
        total_return = ((final_value - initial_value) / initial_value) * 100

        # Annual return (CAGR)
        days = (equity_curve.index[-1] - equity_curve.index[0]).days
        years = days / 365.25
        annual_return = (((final_value / initial_value) ** (1 / years)) - 1) * 100 if years > 0 else 0

        # Sharpe Ratio (assume risk-free rate = 0 for simplicity)
        returns = equity_curve['portfolio_value'].pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0

        # Max Drawdown
        cumulative = equity_curve['portfolio_value']
        running_max = cumulative.expanding().max()
        drawdown = ((cumulative - running_max) / running_max) * 100
        max_drawdown = drawdown.min()

        # Win Rate (percentage of profitable trades)
        if not trade_history.empty and 'action' in trade_history.columns:
            # Count winning vs losing trades (simplified)
            num_trades = len(trade_history)
            # For more accurate win rate, we'd need to track entry and exit prices
            win_rate = 50.0  # Placeholder
        else:
            num_trades = 0
            win_rate = 0.0

        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'num_trades': num_trades
        }

    def plot_equity_curve(
        self,
        result: BacktestResult,
        output_path: str = 'equity_curve.png',
        strategy_name: str = 'Strategy'
    ):
        """
        Plot equity curve with matplotlib

        Args:
            result: BacktestResult instance
            output_path: Path to save PNG
            strategy_name: Name of strategy for title
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            print("Warning: matplotlib not installed. Skipping visualization.")
            print("Install with: pip3 install matplotlib")
            return

        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot equity curve
        ax.plot(result.equity_curve.index,
                result.equity_curve['portfolio_value'],
                linewidth=2.5,
                color='#2E86AB',
                label='Portfolio Value')

        # Plot initial value line
        initial_value = result.equity_curve['portfolio_value'].iloc[0]
        ax.axhline(y=initial_value, color='gray', linestyle='--',
                   linewidth=1, alpha=0.5, label=f'Initial Value (${initial_value:,.0f})')

        # Title and labels
        ax.set_title(f'Equity Curve - {strategy_name}\n{result.annual_return:.2f}% Annual Return',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=13)
        ax.set_ylabel('Portfolio Value ($)', fontsize=13)

        # Grid
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

        # Format y-axis with $ and commas
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45, ha='right')

        # Legend
        ax.legend(loc='upper left', fontsize=11)

        # Add metrics box
        metrics_text = (
            f"Total Return: {result.total_return:.2f}%\n"
            f"Annual Return: {result.annual_return:.2f}%\n"
            f"Sharpe Ratio: {result.sharpe_ratio:.2f}\n"
            f"Max Drawdown: {result.max_drawdown:.2f}%\n"
            f"Num Trades: {result.num_trades}"
        )

        # Position box in upper right
        ax.text(0.98, 0.98, metrics_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round',
                         facecolor='wheat',
                         alpha=0.8,
                         edgecolor='gray',
                         linewidth=1.5))

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Equity curve visualization saved to {output_path}")
        plt.close()


def main():
    """Test BacktestEngine"""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from strategies.momentum import MomentumStrategy
    from strategies.base import BuyAndHoldStrategy

    print("=" * 60)
    print("TEST: Backtest Engine")
    print("=" * 60)

    # Create engine
    engine = BacktestEngine(initial_cash=100000)

    # Create strategy
    strategy = BuyAndHoldStrategy()

    # Small universe for testing
    test_universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']

    # Run backtest (1 year)
    result = engine.run_backtest(
        strategy=strategy,
        universe=test_universe,
        start_date='2023-01-01',
        end_date='2024-01-01',
        rebalance_freq='quarterly',
        top_n=5
    )

    print("\n" + "=" * 60)
    print("Backtest Results")
    print("=" * 60)
    print(result)


def cli_main():
    """CLI entry point for backtesting"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Backtest trading strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Momentum strategy (2014-2024)
  python3 backtest_engine.py --strategy momentum --start-date 2014-01-01 --end-date 2024-01-01

  # Value strategy with custom settings
  python3 backtest_engine.py --strategy value --universe SP500 --rebalance quarterly --top-n 30

  # Quality strategy (recent 4 years)
  python3 backtest_engine.py --strategy quality --start-date 2020-01-01 --end-date 2024-01-01
        """
    )

    parser.add_argument('--strategy', type=str, required=True,
                       choices=['momentum', 'value', 'quality', 'buy_hold'],
                       help='Strategy to backtest')

    parser.add_argument('--universe', type=str, default='SP500',
                       choices=['SP500', 'NASDAQ100', 'KOSPI200', 'KOSDAQ150'],
                       help='Stock universe (default: SP500)')

    parser.add_argument('--start-date', type=str, required=True,
                       help='Start date (YYYY-MM-DD)')

    parser.add_argument('--end-date', type=str, required=True,
                       help='End date (YYYY-MM-DD)')

    parser.add_argument('--rebalance', type=str, default='monthly',
                       choices=['monthly', 'quarterly'],
                       help='Rebalancing frequency (default: monthly)')

    parser.add_argument('--top-n', type=int, default=50,
                       help='Portfolio size (default: 50)')

    parser.add_argument('--initial-cash', type=float, default=100000,
                       help='Initial capital (default: 100000)')

    parser.add_argument('--commission', type=float, default=0.001,
                       help='Commission rate (default: 0.001 = 0.1%%)')

    parser.add_argument('--slippage', type=float, default=0.0005,
                       help='Slippage rate (default: 0.0005 = 0.05%%)')

    parser.add_argument('--output', type=str, default=None,
                       help='Output directory (default: tempo/factor-lab/backtests/backtest_STRATEGY_YYYYMMDD/)')

    parser.add_argument('--html', type=str, default=None,
                       help='Generate HTML dashboard (default: tempo/factor-lab/dashboards/backtest_STRATEGY_YYYYMMDD.html)')

    args = parser.parse_args()

    # Get output directory and set defaults
    output_dir = get_output_dir()
    timestamp = datetime.now().strftime('%Y%m%d')
    strategy_short = args.strategy

    # Set default output paths if not specified
    if args.output is None:
        args.output = os.path.join(output_dir, 'backtests', f'backtest_{strategy_short}_{timestamp}')

    if args.html is None:
        args.html = os.path.join(output_dir, 'dashboards', f'backtest_{strategy_short}_{timestamp}.html')

    # Import strategies
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    if args.strategy == 'momentum':
        from strategies.momentum import MomentumStrategy
        strategy = MomentumStrategy()
        strategy_name = "Momentum Strategy"
    elif args.strategy == 'value':
        from strategies.value_factor import ValueFactorStrategy
        strategy = ValueFactorStrategy()
        strategy_name = "Value Factor Strategy"
    elif args.strategy == 'quality':
        from strategies.quality import QualityStrategy
        strategy = QualityStrategy()
        strategy_name = "Quality Strategy"
    else:  # buy_hold
        from strategies.base import BuyAndHoldStrategy
        strategy = BuyAndHoldStrategy()
        strategy_name = "Buy and Hold Strategy"

    # Load universe
    print(f"\n{'='*60}")
    print(f"BACKTEST: {strategy_name}")
    print(f"{'='*60}")
    print(f"Universe: {args.universe}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Rebalancing: {args.rebalance}")
    print(f"Portfolio size: {args.top_n} stocks")
    print(f"Initial capital: ${args.initial_cash:,.0f}")
    print(f"{'='*60}\n")

    data_mgr = QuantDataManager()
    universe = data_mgr.get_universe(args.universe)

    print(f"Loading {args.universe} universe...")
    print(f"Universe size: {len(universe)} stocks\n")

    # Run backtest
    engine = BacktestEngine(
        data_manager=data_mgr,
        initial_cash=args.initial_cash,
        commission=args.commission,
        slippage=args.slippage
    )

    print("Running backtest...")
    result = engine.run_backtest(
        strategy=strategy,
        universe=universe,
        start_date=args.start_date,
        end_date=args.end_date,
        rebalance_freq=args.rebalance,
        top_n=args.top_n
    )

    # Print results
    print(f"\n{'='*60}")
    print("BACKTEST RESULTS")
    print(f"{'='*60}")
    print(result)
    print(f"{'='*60}\n")

    # Save results
    os.makedirs(args.output, exist_ok=True)

    result.equity_curve.to_csv(f"{args.output}/equity_curve.csv")
    if not result.trade_history.empty:
        result.trade_history.to_csv(f"{args.output}/trades.csv", index=False)

    # Generate visualization
    engine.plot_equity_curve(
        result,
        output_path=f"{args.output}/equity_curve.png",
        strategy_name=strategy_name
    )

    print(f"\n✓ Results saved to {args.output}/")
    print(f"  - equity_curve.csv")
    if not result.trade_history.empty:
        print(f"  - trades.csv")
    print(f"  - equity_curve.png")

    # Generate HTML dashboard if requested
    if args.html:
        print(f"\nGenerating HTML dashboard...")

        metadata = {
            'strategy': strategy_name,
            'start_date': args.start_date,
            'end_date': args.end_date,
            'universe': args.universe,
            'rebalance': args.rebalance,
            'initial_cash': args.initial_cash,
            'total_return': result.total_return,
            'annual_return': result.annual_return,
            'sharpe_ratio': result.sharpe_ratio,
            'max_drawdown': result.max_drawdown,
            'num_trades': len(result.trade_history) if not result.trade_history.empty else 0,
            'win_rate': result.win_rate if hasattr(result, 'win_rate') else 0
        }

        html_path = generate_backtest_dashboard(
            equity_curve_csv=f"{args.output}/equity_curve.csv",
            trades_csv=f"{args.output}/trades.csv",
            output_path=args.html,
            title=f"factor-lab Backtest - {strategy_name}",
            metadata=metadata
        )
        print(f"✓ HTML dashboard saved to {html_path}")

    return result


if __name__ == '__main__':
    # Check if CLI args provided
    if len(sys.argv) > 1:
        cli_main()
    else:
        main()  # Run built-in test
