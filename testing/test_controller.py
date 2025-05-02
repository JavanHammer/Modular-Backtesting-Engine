"""
Unit tests for the Controller class in controller.py
"""

from app.controller import Controller

def test_controller_initialization_attributes():
    """Test that Controller initializes with correct attributes."""
    controller = Controller(ticker="AAPL", strategy_name="momentum", source="csv")
    
    assert controller.ticker == "AAPL"
    assert controller.strategy_name == "momentum"
    assert controller.data_handler is not None
    assert controller.data is not None

def test_controller_run_backtest_and_metrics():
    """Test that Controller can run and return a valid metrics dictionary."""
    controller = Controller(ticker="AAPL", strategy_name="momentum", source="csv")
    metrics = controller.run()
    
    assert isinstance(metrics, dict)
    assert "Total Return" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Max Drawdown" in metrics
    assert isinstance(metrics["Total Return"], float)