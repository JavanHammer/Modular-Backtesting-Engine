"""
data_handler.py

Module responsible for fetching and preparing financial data
either from Yahoo Finance API or from a local CSV file.
"""

import pandas as pd
import yfinance as yf

class DataHandler:
    """
    A class to handle data loading from different sources.

    Parameters
    ----------
    source : str
        The data source to use ('yahoo' or 'csv').

    Attributes
    ----------
    source : str
        Data source identifier ('yahoo' or 'csv').
    data : pd.DataFrame
        Loaded historical market data.
    """

    def __init__(self, source: str = "yahoo"):
        """
        Initialize the DataHandler instance.

        Parameters
        ----------
        source : str, optional
            Data source to use ('yahoo' or 'csv'), default is 'yahoo'.
        """
        self.source = source
        self.data = None

    def load_data(self, source_identifier: str):
        """
        Loads data from the appropriate source based on source type.

        Parameters
        ----------
        source_identifier : str
            Ticker symbol (for Yahoo) or CSV file path (for CSV).

        Returns
        -------
        None
        """
        if self.source == "yahoo":
            self.data = self.fetch_yahoo_data(source_identifier)
        elif self.source == "csv":
            self.data = self.fetch_csv_data(source_identifier)
        else:
            raise ValueError(f"Unsupported source type: {self.source}")

    def fetch_yahoo_data(self, ticker: str) -> pd.DataFrame:
        """
        Fetch historical data for a given stock ticker from Yahoo Finance.

        Parameters
        ----------
        ticker : str
            Stock ticker symbol.

        Returns
        -------
        pd.DataFrame
            Historical daily price data.
        """
        df = yf.download(ticker, period="3y", interval="1d") # Gets the 3 year dataframe from Yahoo Finance
        df = df[["Close"]].dropna()
        df.index.name = "Date"
        return df

    def fetch_csv_data(self, file_path: str) -> pd.DataFrame:
        """
        Load historical data from a local CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.

        Returns
        -------
        pd.DataFrame
            Historical daily price data.
        """
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
        df = df[["Close"]].dropna()
        return df

    def fetch_data(self) -> pd.DataFrame:
        """
        Returns the currently loaded market data.

        Returns
        -------
        pd.DataFrame
            Historical daily price data.
        """
        if self.data is None:
            raise ValueError("No data loaded. Please call load_data() first.")
        return self.data