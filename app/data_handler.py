"""
data_handler.py

Module responsible for fetching and preprocessing historical financial market data
for use in backtesting trading strategies.

This is done by dropping rows with missing values or raising an error if there was 
no data found for the ticker or if there was a failure fetching the data.
"""

import yfinance as yf
import pandas as pd

class DataHandler:
    """
    A class to handle data retrieval from Yahoo Finance.

    Methods
    -------
    fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame
        Fetches historical stock data for a specified ticker and time period.
    """

    def __init__(self):
        """
        Initializes the DataHandler class for fetching data.

        No parameters are required. This class is for tailored for retrieving
        historical market data using the yfinance API.
        """
        pass

    def fetch_data(self, ticker: str, start_date: str = '2024-01-01', end_date: str = '2024-12-31') -> pd.DataFrame:
        """
        Fetches historical stock data for a given ticker symbol using Yahoo Finance.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol (ex 'AAPL').
        start_date : str
            The start date in 'YYYY-MM-DD' format. Defaults to '2024-01-01'.
        end_date : str
            The end date in 'YYYY-MM-DD' format. Defaults to '2024-12-31'.

        Returns
        -------
        pd.DataFrame
            A Dataframe containing the stock's historical data.

        Raises
        ------
        RuntimeError
            If the data cannot be fetched or is empty.
        """

        # Attempt to download data from Yahoo Finance
        try:
            df = yf.download(ticker, start=start_date, end=end_date)

            # Check if the Dataframe is empty
            if df.empty:
                raise ValueError(f"No data found for ticker: {ticker}")

            # Clean the data (drop rows with missing values)
            df.dropna(inplace=True)

            return df
        
        # Tells user that the module failed to fetch the data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data for {ticker}: {str(e)}")
