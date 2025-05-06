"""
Unit tests for the RSIThresholdStrategy class in rsi_threshold.py
"""

import pandas as pd
from app.strategies.rsi_threshold import RSIThresholdStrategy

def test_rsi_threshold_buy_and_sell_signals():
    """Test RSIThresholdStrategy triggers buy/sell based on RSI thresholds."""
    data = pd.DataFrame({'Close': [10, 11, 9, 12, 8, 7, 13, 14, 6, 5]})

    strategy = RSIThresholdStrategy(data, buy_threshold=30, sell_threshold=70)

    # Manually override RSI values
    strategy.data['RSI'] = [20, 25, 35, 40, 22, 15, 60, 72, 28, 18]

    buy_row = strategy.data.iloc[5]
    sell_row = strategy.data.iloc[7]

    # Assertions
    assert strategy.should_buy(buy_row)
    assert strategy.should_sell(sell_row)