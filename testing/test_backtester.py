"""
Unit tests for the Backtester class in backtester.py
"""

import pandas as pd
from app.backtester import Backtester

class DummyStrategy:
    def should_buy(self, row):
        return row['Close'] < 102
    
    def should_sell(self, row):
        return row['Close'] > 104

def test_backtester_equity_curve_generation():
    """Test that Backtester generates a valid equity curve from price data and strategy."""
    # Dummy price data
    dates = pd.date_range(start="2022-01-01", periods=5)
    price_data = pd.DataFrame({"Close": [100, 102, 101, 105, 107]}, index=dates)

    # Initialize and run Backtester
    backtester = Backtester(data=price_data, strategy=DummyStrategy())
    equity_curve = backtester.run_backtest()

    # Assertions
    assert isinstance(equity_curve, pd.DataFrame)
    assert 'Portfolio Value' in equity_curve.columns
    assert not equity_curve.empty