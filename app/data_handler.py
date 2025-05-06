"""
data_handler.py

Module responsible for fetching and loading historical market data 
either from Yahoo Finance or from a local CSV file.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class DataHandler:
    """
    A class to fetch and preprocess market data for backtesting.

    Parameters
    ----------
    source : str
        Source of data ('yahoo' or 'csv').

    Attributes
    ----------
    source : str
        Data source being used.
    """

    def __init__(self, source: str = "yahoo"):
        """
        Initializes the DataHandler with a specified data source.

        Parameters
        ----------
        source : str, optional
            Data source ('yahoo' or 'csv'), default is 'yahoo'.
        """
        self.source = source

    def fetch_data(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetches and preprocesses historical stock data.

        Parameters
        ----------
        ticker : str
            Stock ticker (if using Yahoo) or CSV file path (if using CSV).
        start_date : str, optional
            Start date for Yahoo Finance download (format 'YYYY-MM-DD').
        end_date : str, optional
            End date for Yahoo Finance download (format 'YYYY-MM-DD').

        Returns
        -------
        pd.DataFrame
            A DataFrame containing historical price data.

        Raises
        ------
        RuntimeError
            If the data cannot be fetched or is empty.
        """

        # Determine which fetching method to use based on the source
        if self.source == "yahoo":
            return self._fetch_from_yahoo(ticker, start_date, end_date)
        elif self.source == "csv":
            return self._fetch_from_csv(ticker)
        else:
            raise ValueError(f"Unsupported data source: {self.source}")

    def _fetch_from_yahoo(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetch data from Yahoo Finance.

        Parameters
        ----------
        ticker : str
            Stock ticker symbol.
        start_date : str, optional
            Start date for data (defaults to 3 years ago).
        end_date : str, optional
            End date for data (defaults to yesterday).

        Returns
        -------
        pd.DataFrame
            Historical market data.

        Raises
        ------
        RuntimeError
            If data fetching fails.
        """

        # Set default date range if none provided
        if start_date is None:
            start_date = (datetime.today() - timedelta(days=3*365 + 1)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        try:
            # Attempt to download stock data
            df = yf.download(ticker, start=start_date, end=end_date)

            # Raise an error if no data was returned
            if df.empty:
                raise ValueError(f"No data found for ticker: {ticker}")

            # Drop any rows with missing values
            df.dropna(inplace=True)

            return df

        except Exception as e:
            raise RuntimeError(f"Failed to fetch data for {ticker}: {str(e)}")

    def _fetch_from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Fetch data from a local CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.

        Returns
        -------
        pd.DataFrame
            Historical market data from CSV.

        Raises
        ------
        RuntimeError
            If reading the CSV fails.
        """
        try:
            # Attempt to load CSV file
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)

            # Drop any rows with missing values
            df.dropna(inplace=True)

            return df

        except Exception as e:
            raise RuntimeError(f"Failed to read CSV file {file_path}: {str(e)}")