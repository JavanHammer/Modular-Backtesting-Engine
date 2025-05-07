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
        # Skip rows where moving averages are not available yet
        if pd.isna(row['short_sma']) or pd.isna(row['long_sma']):
            return False

        # Get the integer location of the current row
        row_idx = self.data.index.get_loc(row.name)

        # Prevents error on the very first row
        if row_idx == 0:
            return False

        # Get previous row's short and long SMA values
        prev = self.data.iloc[row_idx - 1]

        # Skip if previous row also has NaNs
        if pd.isna(prev['short_sma']) or pd.isna(prev['long_sma']):
            return False

        # Buy if short SMA crosses above long SMA
        return (prev['short_sma'] <= prev['long_sma']) and (row['short_sma'] > row['long_sma'])

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on SMA crossover.
        """
        # Skip rows where moving averages are not available yet
        if pd.isna(row['short_sma']) or pd.isna(row['long_sma']):
            return False

        # Get the integer location of the current row
        row_idx = self.data.index.get_loc(row.name)

        # Prevents error on the very first row
        if row_idx == 0:
            return False

        # Get previous row's short and long SMA values
        prev = self.data.iloc[row_idx - 1]

        # Skip if previous row also has NaNs
        if pd.isna(prev['short_sma']) or pd.isna(prev['long_sma']):
            return False

        # Sell if short SMA crosses below long SMA
        return (prev['short_sma'] >= prev['long_sma']) and (row['short_sma'] < row['long_sma'])