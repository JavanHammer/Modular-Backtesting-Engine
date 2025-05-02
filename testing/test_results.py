"""
Unit tests for the Results class in results.py
"""

import pandas as pd
from app.results import Results

def test_results_calculate_performance_metrics():
    """Test that Results calculates key performance metrics correctly."""
    # Dummy portfolio value
    dates = pd.date_range(start="2022-01-01", periods=5)
    portfolio_data = pd.DataFrame({"Portfolio Value": [10000, 10200, 10100, 10400, 10600]}, index=dates)
    
    # Initialize Results
    results = Results(portfolio=portfolio_data)
    metrics = results.calculate_performance_metrics()
    
    # Assertions
    assert isinstance(metrics, dict)
    assert "Total Return" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Max Drawdown" in metrics
    assert isinstance(metrics["Total Return"], float)
    assert isinstance(metrics["Sharpe Ratio"], float)
    assert isinstance(metrics["Max Drawdown"], float)