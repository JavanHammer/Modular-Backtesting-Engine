"""
breakout.py

Strategy that generates trading decisions based on price breakouts above past highs/lows.
"""

import pandas as pd

class BreakoutStrategy:
    """
    Strategy that buys when price exceeds recent high and sells when it falls below recent low.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data.
    entry_period : int
        Lookback period for entry breakout (default is 25).
    exit_period : int
        Lookback period for exit breakout (default is 15).

    Attributes
    ----------
    data : pd.DataFrame
        Market data with rolling highs and lows.
    """

    def __init__(self, data: pd.DataFrame, entry_period: int = 25, exit_period: int = 15):
        """
        Initializes BreakoutStrategy with entry and exit periods.
        """
        self.data = data.copy()
        self.entry_period = entry_period
        self.exit_period = exit_period

        # Calculate rolling highs for entry and rolling lows for exit
        self.data['rolling_high'] = self.data['Close'].rolling(window=self.entry_period).max()
        self.data['rolling_low'] = self.data['Close'].rolling(window=self.exit_period).min()

    def should_buy(self, row: pd.Series) -> bool:
        """
        Determines whether to buy based on breakout above recent high.
        """
        return row['Close'] > row['rolling_high']

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on breakdown below recent low.
        """
        return row['Close'] < row['rolling_low']
