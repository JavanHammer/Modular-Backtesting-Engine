"""
backtester.py

Module responsible for simulating the execution of trading strategies using historical
price data and strategy decision logic (buy/sell conditions).

This module tracks portfolio cash, position holdings, and total equity over time,
assuming trades are executed at the daily closing price.
"""

import pandas as pd

class Backtester:
    """
    A class to simulate the execution of trading strategies on historical market data.

    Purpose
    -------
    Simulates trading decisions day-by-day using strategy buy/sell signals, and tracks 
    portfolio value over the backtest period.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data containing at least a 'Close' column.
    strategy : object
        Strategy instance that implements should_buy(row) and should_sell(row) methods.
    initial_cash : float
        Starting cash amount for the portfolio (default is 100,000).

    Attributes
    ----------
    data : pd.DataFrame
        The historical market data used for the backtest.
    strategy : object
        The trading strategy instance applied during the backtest.
    initial_cash : float
        The starting portfolio cash amount.
    cash : float
        Current available cash during the backtest.
    position : int
        Number of shares currently held.
    equity_curve : list
        List of (date, total equity) tracking portfolio value over time.
    """

    def __init__(self, data: pd.DataFrame, strategy: object, initial_cash: float = 100000.0):
        """
        Initializes the Backtester instance with market data, a trading strategy, and starting capital.
        """
        self.data = data
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0
        self.equity_curve = []
        self.trades_executed = 0

        # Validate data sufficiency for the selected strategy
        self._validate_data_for_strategy()

    def _validate_data_for_strategy(self):
        """
        Validates that there is enough historical data to support the selected strategy.
        Raises an error if not enough data is available.
        """
        # SMA Crossover Strategy check
        if hasattr(self.strategy, "long_window"):
            if len(self.data) < self.strategy.long_window:
                raise ValueError(
                    f"Not enough data ({len(self.data)} rows) for SMA Crossover strategy. "
                    f"Requires at least {self.strategy.long_window} days of data."
                )

        # RSI Threshold Strategy check
        if hasattr(self.strategy, "data") and 'RSI' in self.strategy.data.columns:
            if len(self.data) < 14:  # Assuming default RSI period
                raise ValueError(
                    "Not enough data for RSI Threshold strategy. Requires at least 14 days of data."
                )

        # Golden Cross Strategy check
        if hasattr(self.strategy, "data") and 'sma_200' in self.strategy.data.columns:
            if len(self.data) < 200:
                raise ValueError(
                    "Not enough data for Golden Cross strategy. Requires at least 200 days of data."
                )

        # Momentum Strategy (Rate of Change) check
        if hasattr(self.strategy, "roc_period"):
            if len(self.data) < self.strategy.roc_period:
                raise ValueError(
                    f"Not enough data ({len(self.data)} rows) for Momentum strategy. "
                    f"Requires at least {self.strategy.roc_period} days of data."
                )

        # Breakout Strategy check
        if hasattr(self.strategy, "entry_period") and hasattr(self.strategy, "exit_period"):
            required_days = max(self.strategy.entry_period, self.strategy.exit_period)
            if len(self.data) < required_days:
                raise ValueError(
                    f"Not enough data ({len(self.data)} rows) for Breakout strategy. "
                    f"Requires at least {required_days} days of data."
                )

    def run_backtest(self) -> pd.DataFrame:
        """
        Runs the trading simulation over the historical data.

        For each day:
        - Evaluates the strategy's buy/sell logic.
        - Executes trades at the daily close price.
        - Updates cash, positions, and total equity.

        Returns
        -------
        pd.DataFrame
            DataFrame containing 'Date' and 'Portfolio Value', indexed by date.
        """

        # Loop through each day in the dataset
        for row_idx, (date, row) in enumerate(self.data.iterrows()):

            price = row['Close']

            # Check if strategy signals a buy
            if self.strategy.should_buy(row) and self.cash >= price:
                self.position += 1
                self.cash -= price
                self.trades_executed += 1

            # Check if strategy signals a sell
            elif self.strategy.should_sell(row) and self.position > 0:
                self.position -= 1
                self.cash += price
                self.trades_executed += 1

            # Calculate current total equity: cash + (number of shares * current close price)
            total_equity = self.cash + self.position * price

            # Record the date and total equity
            self.equity_curve.append((date, total_equity))

        # Convert equity history into a DataFrame for output
        return pd.DataFrame(self.equity_curve, columns=['Date', 'Portfolio Value']).set_index('Date')