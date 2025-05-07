"""
golden_cross.py

Strategy that generates long-term trading decisions based on 50-day and 200-day moving averages (Golden Cross).
"""

import pandas as pd

class GoldenCrossStrategy:
    """
    Strategy that buys on Golden Cross (50-day SMA crosses above 200-day) and sells on Death Cross.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data.

    Attributes
    ----------
    data : pd.DataFrame
        Market data with computed 50-day and 200-day SMAs.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes GoldenCrossStrategy and calculates moving averages.
        """
        self.data = data.copy()

        # Calculate 50-day and 200-day SMAs
        self.data['sma_50'] = self.data['Close'].rolling(window=50).mean()
        self.data['sma_200'] = self.data['Close'].rolling(window=200).mean()

    def should_buy(self, row: pd.Series) -> bool:
        """
        Determines whether to buy based on Golden Cross.
        """
        # Get the integer index of the current row
        row_idx = self.data.index.get_loc(row.name)

        # Prevent index error on the first row
        if row_idx == 0:
            return False
        
        # Get previous row's SMA values
        prev = self.data.iloc[row_idx - 1]

        # Buy signal: 50-day SMA crosses above 200-day SMA
        return (prev['sma_50'] <= prev['sma_200']) and (row['sma_50'] > row['sma_200'])

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on Death Cross.
        """
        # Get the integer index of the current row
        row_idx = self.data.index.get_loc(row.name)

        # Prevent index error on the first row
        if row_idx == 0:
            return False
        
        # Get previous row's SMA values
        prev = self.data.iloc[row_idx - 1]

        # Sell signal: 50-day SMA crosses below 200-day SMA
        return (prev['sma_50'] >= prev['sma_200']) and (row['sma_50'] < row['sma_200'])