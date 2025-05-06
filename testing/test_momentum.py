"""
Unit tests for the MomentumStrategy class in momentum.py
"""

import pandas as pd
from app.strategies.momentum import MomentumStrategy

def test_momentum_buy_and_sell_signals():
    """Test MomentumStrategy triggers buy/sell based on ROC threshold."""
    data = pd.DataFrame({'Close': [10, 12, 14, 16, 18, 20]})

    strategy = MomentumStrategy(data, roc_period=1, roc_threshold=0.05)

    # Override ROC values manually
    strategy.data['ROC'] = [None, 0.2, 0.1667, 0.1428, 0.125, -0.05]

    buy_row = strategy.data.iloc[1]
    sell_row = strategy.data.iloc[5]

    assert strategy.should_buy(buy_row)
    assert strategy.should_sell(sell_row)