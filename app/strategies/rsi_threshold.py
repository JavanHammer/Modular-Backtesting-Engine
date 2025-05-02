"""
rsi_threshold.py

Strategy that generates trading decisions based on Relative Strength Index (RSI) thresholds.
"""

import pandas as pd

class RSIThresholdStrategy:
    """
    Strategy that buys when RSI falls below a threshold and sells when it rises above another.

    Parameters
    ----------
    data : pd.DataFrame
        Historical market data.
    buy_threshold : float
        RSI value below which to buy (default is 30).
    sell_threshold : float
        RSI value above which to sell (default is 70).

    Attributes
    ----------
    data : pd.DataFrame
        Market data with computed RSI.
    buy_threshold : float
        Buy threshold for RSI.
    sell_threshold : float
        Sell threshold for RSI.
    """

    def __init__(self, data: pd.DataFrame, buy_threshold: float = 30.0, sell_threshold: float = 70.0):
        """
        Initializes RSIThresholdStrategy and calculates RSI.
        """
        self.data = data.copy()
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

        # Calculate the RSI
        self._calculate_rsi()

    def _calculate_rsi(self, period: int = 14):
        """
        Calculates the Relative Strength Index (RSI).
        """
        delta = self.data['Close'].diff()

        # Separate gains and losses
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        # Calculate average gains and losses
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        # Compute the RSI
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

    def should_buy(self, row: pd.Series) -> bool:
        """
        Determines whether to buy based on RSI threshold.
        """
        return row['RSI'] <= self.buy_threshold

    def should_sell(self, row: pd.Series) -> bool:
        """
        Determines whether to sell based on RSI threshold.
        """
        return row['RSI'] >= self.sell_threshold