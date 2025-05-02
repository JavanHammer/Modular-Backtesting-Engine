"""
Unit tests for the DataHandler class in data_handler.py
"""

import pandas as pd
from app.data_handler import DataHandler

def test_datahandler_load_csv_data():
    """Test that DataHandler loads data correctly from a CSV file."""
    handler = DataHandler(ticker="sample_data.csv", source="csv")
    data = handler.load_data()
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert "Close" in data.columns

def test_datahandler_load_yahoo_data():
    """Test that DataHandler loads data correctly from Yahoo Finance."""
    handler = DataHandler(ticker="AAPL", source="yahoo")
    data = handler.load_data()
    
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    assert "Close" in data.columns