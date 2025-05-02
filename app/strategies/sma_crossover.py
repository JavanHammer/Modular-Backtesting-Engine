"""
sma_crossover.py

Strategy that generates trading decisions based on short and long simple moving average (SMA) crossovers.
"""

import pandas as pd

class SMACrossoverStrategy:
    """
    Strategy that buys when short-term SMA crosses above long-term SMA and sells when it crosses below.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data.
    short_window : int
        Period for short-term SMA (default is 20).
    long_window : int
        Period for long-term SMA (default is 50).

    Attributes
    ----------
    data : pd.DataFrame
        Market data with computed short and long SMAs.
    short_window : int
        Short-term moving average window.
    long_window : int
        Long-term moving average window.
    """

    def __init__(self, data: pd.DataFrame, short_window: int = 20, long_window: int = 50):
        """
        Initializes SMACrossoverStrategy and calculates moving averages.
        """
        self.data = data.copy()
        self.short_window = short_window
        self.long_window = long_window

        # Calculates short and long term SMAs
        self.data['short_sma'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['long_sma'] = self.data['Close'].rolling(window=self.long_window).mean()

    def should_buy(self, row: pd.Series) -> bool:
        """
        Determines whether to buy based on SMA crossover.
        """
        idx = row.name

        # Prevents index error on the first row
        if idx == 0:
            return False
        
        # Get prev row's SMA values
        prev = self.data.iloc[idx - 1]

        # Buy signal: short SMA crosses above long SMA
        return (prev['short_sma'] <= prev['long_sma']) and (row['short_sma'] > row['long_sma'])

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on SMA crossover.
        """
        idx = row.name

        # Prevents index error on the first row
        if idx == 0:
            return False
        
        # Get prev row's SMA values
        prev = self.data.iloc[idx - 1]

        # Sell signal: short SMA crosses below long SMA
        return (prev['short_sma'] >= prev['long_sma']) and (row['short_sma'] < row['long_sma'])