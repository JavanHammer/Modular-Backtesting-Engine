"""
Unit tests for the Controller class in controller.py
"""

import pandas as pd
import pytest
from app.controller import Controller

def test_controller_run_backtest_and_metrics(monkeypatch):
    """Test that Controller can run a backtest and return equity curve and metrics."""

    # Dummy price data with SMA columns
    dummy_data = pd.DataFrame({
        "Close": [100, 102, 101, 105, 107],
        "short_sma": [99, 101, 100, 104, 106],
        "long_sma": [100, 101, 101, 103, 105]
    })

    def mock_fetch_data(self, ticker, start_date=None, end_date=None):
        return dummy_data

    from app.data_handler import DataHandler
    monkeypatch.setattr(DataHandler, "fetch_data", mock_fetch_data)

    controller = Controller()

    ticker = "AAPL"
    strategy_name = "sma_crossover"
    strategy_params = {"short_window": 1, "long_window": 2}

    equity_curve, metrics = controller.run_backtest(
        ticker=ticker,
        strategy_name=strategy_name,
        strategy_params=strategy_params
    )

    assert isinstance(equity_curve, pd.DataFrame)
    assert "Portfolio Value" in equity_curve.columns
    assert isinstance(metrics, dict)
    assert "Total Return" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Max Drawdown" in metrics