"""
backtester.py

Module responsible for simulating the execution of trading strategies using historical
price data and predefined signals (from strategy.py).

This module calculates changes in portfolio cash, positions, and total equity over time.
It assumes trades are executed using closing prices and that one share is bought/sold per signal.
"""

import pandas as pd

class Backtester:
    """
    A class to simulate the execution of trading signals on historical data.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data containing at least a 'Close' column.
    signals : pd.Series
        Series of trading signals indexed by date. Values: 1 (buy), -1 (sell), 0 (hold).
    initial_cash : float
        Starting cash for the portfolio (default is 100,000).

    Attributes
    ----------
    cash : float
        Remaining cash in the portfolio.
    position : int
        Number of shares currently held.
    equity_curve : list
        Tracks the total value (cash + position*price) over time.
    """

    def __init__(self, data: pd.DataFrame, signals: pd.Series, initial_cash: float = 100000.0):
        """
        Initializes the Backtester instance with price data, signals, and starting capital.

        Parameters
        ----------
        data : pd.DataFrame
            Historical price data, must include a 'Close' column.
        signals : pd.Series
            Buy/sell/hold signals indexed by date.
        initial_cash : float
            Starting capital (default is 100,000).
        """
        self.data = data
        self.signals = signals
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0
        self.equity_curve = []

    def run_backtest(self) -> pd.DataFrame:
        """
        Executes the trading simulation over the historical data.

        For each day:
        - Buys 1 share if signal == 1 and there's enough cash.
        - Sells 1 share if signal == -1 and a position is held.
        - Holds if signal == 0 or if no trade can be made.

        Tracks daily portfolio value and returns a Dataframe of the equity curve.

        Returns
        -------
        pd.DataFrame
            Dataframe with two columns: 'Date' and 'Equity', indexed by date.
        """
        # This loop iterates over the data frame
        for date, row in self.data.iterrows():
            price = row['Close']
            signal = self.signals.get(date, 0)

            # Buys one share if there is enough cash
            if signal == 1 and self.cash >= price:
                self.position += 1
                self.cash -= price

            # Sells a share if we hold one
            elif signal == -1 and self.position > 0:
                self.position -= 1
                self.cash += price

            # Calculate equity as: cash + (shares * close price)
            total_equity = self.cash + self.position * price
            self.equity_curve.append((date, total_equity))

        return pd.DataFrame(self.equity_curve, columns=['Date', 'Equity']).set_index('Date')
