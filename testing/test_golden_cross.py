"""
Unit tests for the GoldenCrossStrategy class in golden_cross.py
"""

import pandas as pd
from app.strategies.golden_cross import GoldenCrossStrategy

def test_golden_cross_buy_and_sell_signals():
    """Test GoldenCrossStrategy detects golden cross and death cross signals."""
    data = pd.DataFrame({'Close': list(range(1, 301))})

    strategy = GoldenCrossStrategy(data)

    # Manually set SMA values
    strategy.data['sma_50'] = [None] * 199 + [89, 91] + [95] * 99
    strategy.data['sma_200'] = [None] * 199 + [90, 90] + [90] * 99

    # Golden cross at index 200 (prev: 90 < 92, now 91 > 91)
    buy_row = strategy.data.iloc[200]

    # Death cross at index 250 (simulate similarly)
    strategy.data.loc[249, 'sma_50'] = 91
    strategy.data.loc[249, 'sma_200'] = 90
    strategy.data.loc[250, 'sma_50'] = 89
    strategy.data.loc[250, 'sma_200'] = 90

    sell_row = strategy.data.iloc[250]

    assert strategy.should_buy(buy_row)
    assert strategy.should_sell(sell_row)