"""
momentum.py

Strategy that generates trading decisions based on rate of change (momentum).
"""

import pandas as pd

class MomentumStrategy:
    """
    Strategy that buys when rate of change exceeds a threshold and sells when it drops.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data.
    roc_period : int
        Lookback period for rate of change (default is 20).
    roc_threshold : float
        Minimum ROC value to trigger a buy (default is 0).

    Attributes
    ----------
    data : pd.DataFrame
        Market data with computed rate of change (ROC).
    roc_period : int
        Rate of change calculation window.
    roc_threshold : float
        Threshold value for buy trigger.
    """

    def __init__(self, data: pd.DataFrame, roc_period: int = 20, roc_threshold: float = 0.0):
        """
        Initializes MomentumStrategy and calculates the rate of change (ROC).
        """
        self.data = data.copy()
        self.roc_period = roc_period
        self.roc_threshold = roc_threshold

        # Calculate the Rate of Change (ROC)
        self.data['ROC'] = self.data['Close'].pct_change(periods=self.roc_period)

    def should_buy(self, row: pd.Series) -> bool:
        """
        Determines whether to buy based on rate of change.
        """
        return row['ROC'] >= self.roc_threshold

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on rate of change.
        """
        return row['ROC'] < 0
