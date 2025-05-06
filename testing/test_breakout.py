"""
Unit tests for the BreakoutStrategy class in breakout.py
"""

import pandas as pd
from app.strategies.breakout import BreakoutStrategy

def test_breakout_buy_and_sell_signals():
    """Test BreakoutStrategy identifies breakout buy/sell opportunities."""
    data = pd.DataFrame({'Close': [10, 11, 12, 13, 14, 20, 18, 16, 15, 17]})

    strategy = BreakoutStrategy(data, entry_period=3, exit_period=3)

    # Manually override rolling highs/lows
    strategy.data['rolling_high'] = [10, 11, 12, 13, 14, 14, 14, 14, 14, 14]
    strategy.data['rolling_low'] = [10, 10, 10, 11, 12, 13, 14, 16, 16, 16]

    buy_row = strategy.data.iloc[5]
    sell_row = strategy.data.iloc[8]

    # Assertions
    assert strategy.should_buy(buy_row)
    assert strategy.should_sell(sell_row)