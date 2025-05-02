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
            DataFrame containing 'Date' and 'Equity', indexed by date.
        """

        # Loop through each day in the dataset
        for idx, (date, row) in enumerate(self.data.iterrows()):

            price = row['Close']

            # Check if strategy signals a buy
            if self.strategy.should_buy(row) and self.cash >= price:
                self.position += 1
                self.cash -= price

            # Check if strategy signals a sell
            elif self.strategy.should_sell(row) and self.position > 0:
                self.position -= 1
                self.cash += price

            # Calculate current total equity: cash + (number of shares * current close price)
            total_equity = self.cash + self.position * price

            # Record the date and total equity
            self.equity_curve.append((date, total_equity))

        # Convert equity history into a DataFrame for output
        return pd.DataFrame(self.equity_curve, columns=['Date', 'Equity']).set_index('Date')