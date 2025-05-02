"""
controller.py

Module responsible for orchestrating the data retrieval, strategy initialization,
backtest execution, and result handling for the backtesting engine.

This acts as the central manager coordinating different modules together.
"""

import pandas as pd
from app.data_handler import DataHandler
from app.backtester import Backtester
from app.strategies import (
    SMACrossoverStrategy,
    RSIThresholdStrategy,
    GoldenCrossStrategy,
    MomentumStrategy,
    BreakoutStrategy
)

class Controller:
    """
    A class to orchestrate the workflow of the backtesting system.

    Parameters
    ----------
    None

    Attributes
    ----------
    data_handler : DataHandler
        Instance responsible for fetching market data.
    """

    def __init__(self):
        """
        Initializes the Controller instance and sets up the DataHandler.
        """
        self.data_handler = DataHandler()

    def run_backtest(self, ticker: str, strategy_name: str, strategy_params: dict, initial_cash: float = 100000.0) -> pd.DataFrame:
        """
        Runs the full backtesting workflow based on user input.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol to fetch data for.
        strategy_name : str
            The name of the strategy to use ('sma_crossover', 'rsi_threshold', etc.).
        strategy_params : dict
            Dictionary containing parameters for the selected strategy.
        initial_cash : float
            Initial portfolio cash for the backtest (default is 100,000).

        Returns
        -------
        pd.DataFrame
            DataFrame containing the equity curve over time.
        """

        # Fetch historical data
        data = self.data_handler.fetch_data(ticker)

        # Initialize the selected strategy
        strategy = self._initialize_strategy(strategy_name, data, strategy_params)

        # Initialize the backtester
        backtester = Backtester(data, strategy, initial_cash)

        # Run the backtest and return results
        results = backtester.run_backtest()

        return results

    def _initialize_strategy(self, strategy_name: str, data: pd.DataFrame, params: dict):
        """
        Internal method to initialize the appropriate strategy object based on user selection.

        Parameters
        ----------
        strategy_name : str
            Name of the selected strategy.
        data : pd.DataFrame
            Historical market data.
        params : dict
            Strategy-specific parameters.

        Returns
        -------
        object
            An instance of the selected strategy.
        """

        if strategy_name == "sma_crossover":
            return SMACrossoverStrategy(data, **params)
        elif strategy_name == "rsi_threshold":
            return RSIThresholdStrategy(data, **params)
        elif strategy_name == "golden_cross":
            return GoldenCrossStrategy(data)
        elif strategy_name == "momentum":
            return MomentumStrategy(data, **params)
        elif strategy_name == "breakout":
            return BreakoutStrategy(data, **params)
        else:
            raise ValueError(f"Unknown strategy name: {strategy_name}")
    