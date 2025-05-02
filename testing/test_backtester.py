"""
Unit tests for the Backtester class in backtester.py
"""

import pandas as pd
from app.backtester import Backtester

def test_backtester_equity_curve_generation():
    """Test that Backtester generates a valid equity curve from price data and signals."""
    # Dummy price data
    dates = pd.date_range(start="2022-01-01", periods=5)
    price_data = pd.DataFrame({"Close": [100, 102, 101, 105, 107]}, index=dates)
    
    # Dummy signals
    signals = pd.DataFrame({"Signal": [0, 1, 0, -1, 1]}, index=dates)
    
    # Initialize and run Backtester
    backtester = Backtester(price_data=price_data, signals=signals)
    backtester.run_backtest()
    
    # Assertions
    assert backtester.equity_curve is not None
    assert "Portfolio Value" in backtester.equity_curve.columns
    assert len(backtester.equity_curve) == len(price_data)