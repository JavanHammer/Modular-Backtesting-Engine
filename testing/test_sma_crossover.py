"""
Unit tests for the SMACrossoverStrategy class in sma_crossover.py
"""

import pandas as pd
from app.strategies.sma_crossover import SMACrossoverStrategy

def test_sma_crossover_buy_and_sell_signals():
    """Test SMACrossoverStrategy generates correct buy/sell signals based on SMA crossover."""
    data = pd.DataFrame({
        'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    })

    strategy = SMACrossoverStrategy(data, short_window=2, long_window=3)

    # Set SMAs to simulate crossover at index 3
    strategy.data['short_sma'] = [None, 10.5, 11.5, 11.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5]
    strategy.data['long_sma'] = [None, None, 11.5, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]

    # Previous (index 2): short_sma = 11.5, long_sma = 11.5 → equal
    # Current (index 3): short_sma = 11.5, long_sma = 12.0 → still no buy signal

    # Let's fix it properly
    strategy.data.loc[strategy.data.index[2], 'short_sma'] = 11.0  # lower than long_sma
    strategy.data.loc[strategy.data.index[2], 'long_sma'] = 11.5

    strategy.data.loc[strategy.data.index[3], 'short_sma'] = 12.0  # crosses above
    strategy.data.loc[strategy.data.index[3], 'long_sma'] = 11.5

    row = strategy.data.iloc[3]

    assert strategy.should_buy(row)
    assert not strategy.should_sell(row)