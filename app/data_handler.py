"""
data_handler.py

Module responsible for fetching and preprocessing historical financial market data
for use in backtesting trading strategies.
"""

import yfinance as yf
import pandas as pd

class DataHandler:
    """
    A class to handle data retrieval from Yahoo Finance.

    Methods
    -------
    fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame
        Fetches historical OHLCV stock data for a specified ticker and time period.
    """

    def __init__(self):
        """
        Initializes the DataHandler class.

        Currently, no parameters are required. This structure allows future
        extension to support multiple data sources (e.g., IEX, Tiingo).
        """
        pass

    def fetch_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock data for a given ticker symbol using Yahoo Finance.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol (e.g., 'AAPL').
        start_date : str
            The start date in 'YYYY-MM-DD' format.
        end_date : str
            The end date in 'YYYY-MM-DD' format.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the stock's historical OHLCV data.

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
        
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data for {ticker}: {str(e)}")
