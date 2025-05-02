"""
data_handler.py

Module responsible for fetching and preprocessing historical financial market data
for use in backtesting trading strategies.

This is done by dropping rows with missing values or raising an error if there was 
no data found for the ticker or if there was a failure fetching the data.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class DataHandler:
    """
    A class to handle data retrieval and preprocessing from Yahoo Finance.
    """

    def __init__(self):
        """
        Initializes the DataHandler instance for fetching financial market data.
        """
        pass

    def fetch_data(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetches and preprocesses historical stock data using Yahoo Finance.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol (ex, 'AAPL').
        start_date : str, optional
            The start date for data retrieval in 'YYYY-MM-DD' format. Defaults to 3 years ago yesterday.
        end_date : str, optional
            The end date for data retrieval in 'YYYY-MM-DD' format. Defaults to yesterday.

        Returns
        -------
        pd.DataFrame
            A Dataframe containing the stock's historical data, cleaned of missing values.

        Raises
        ------
        RuntimeError
            If the data cannot be fetched or is empty.
        """

        # Set default start_date and end_date if not provided
        if start_date is None:
            start_date = (datetime.today() - timedelta(days=3*365 + 1)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Attempt to download historical stock data
        try:
            df = yf.download(ticker, start=start_date, end=end_date)

            # Check if the DataFrame is empty (no data returned)
            if df.empty:
                raise ValueError(f"No data found for ticker: {ticker}")

            # Drop any rows with missing values to ensure clean dataset
            df.dropna(inplace=True)

            return df

        # Handle any exceptions during data retrieval
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data for {ticker}: {str(e)}")
