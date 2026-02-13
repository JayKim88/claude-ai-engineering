#!/usr/bin/env python3
"""
Base Strategy Class for factor-lab

All trading strategies must inherit from this base class
and implement the select_stocks() method.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class Strategy(ABC):
    """
    Abstract base class for trading strategies

    All strategies must implement:
    - select_stocks(): Returns list of tickers to buy on a given date

    Optional overrides:
    - get_portfolio_weights(): Custom position sizing (default: equal weight)
    - validate_selection(): Custom validation logic
    """

    def __init__(self, name: str, description: str):
        """
        Initialize strategy

        Args:
            name: Strategy name (e.g., "Momentum", "Value Factor")
            description: Brief description of strategy logic
        """
        self.name = name
        self.description = description

    @abstractmethod
    def select_stocks(
        self,
        universe: List[str],
        date: str,
        data_manager,
        top_n: int = 50
    ) -> List[str]:
        """
        Select stocks to buy on a specific date

        Args:
            universe: List of ticker symbols to choose from
            date: Date in YYYY-MM-DD format (backtest rebalance date)
            data_manager: QuantDataManager instance for fetching data
            top_n: Number of stocks to select

        Returns:
            List of selected ticker symbols (up to top_n stocks)

        Note:
            This method should only use data available BEFORE the given date
            to avoid look-ahead bias in backtesting.
        """
        pass

    def get_portfolio_weights(self, selected_stocks: List[str]) -> Dict[str, float]:
        """
        Calculate portfolio weights for selected stocks

        Args:
            selected_stocks: List of ticker symbols

        Returns:
            Dict mapping ticker -> weight (sum to 1.0)

        Default: Equal weight
        Override this method for custom position sizing
        """
        if not selected_stocks:
            return {}

        weight = 1.0 / len(selected_stocks)
        return {ticker: weight for ticker in selected_stocks}

    def validate_selection(self, selected_stocks: List[str]) -> bool:
        """
        Validate stock selection

        Args:
            selected_stocks: List of selected tickers

        Returns:
            True if selection is valid, False otherwise

        Default: Always valid
        Override for custom validation logic (e.g., sector limits)
        """
        return True

    def __repr__(self) -> str:
        return f"{self.name} Strategy"

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class BuyAndHoldStrategy(Strategy):
    """
    Simple buy-and-hold benchmark strategy

    Buys top N stocks at the start and holds until end.
    Useful for benchmarking against active strategies.
    """

    def __init__(self):
        super().__init__(
            name="Buy and Hold",
            description="Buy top N stocks and hold (benchmark)"
        )
        self._initial_selection = None

    def select_stocks(
        self,
        universe: List[str],
        date: str,
        data_manager,
        top_n: int = 50
    ) -> List[str]:
        """
        Select stocks once at the start, then hold

        For subsequent rebalance dates, return the same stocks
        """
        if self._initial_selection is None:
            # First selection: just take first top_n from universe
            self._initial_selection = universe[:top_n]

        return self._initial_selection
