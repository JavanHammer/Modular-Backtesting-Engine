"""
Unit tests for the DataHandler class in data_handler.py
"""

import pandas as pd
import pytest
from app.data_handler import DataHandler

def test_datahandler_fetch_data(monkeypatch):
    """Test that DataHandler fetches dummy data correctly."""

    dummy_data = pd.DataFrame({
        "Close": [100, 102, 101, 105, 107]
    })

    def mock_download(ticker, start, end):
        return dummy_data

    import yfinance as yf
    monkeypatch.setattr(yf, "download", mock_download)

    handler = DataHandler()
    df = handler.fetch_data(ticker="AAPL")

    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns