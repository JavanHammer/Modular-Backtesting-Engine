"""
controller.py

Module responsible for orchestrating the data retrieval, strategy initialization,
backtest execution, and result handling for the backtesting engine.
"""

import pandas as pd
from app.data_handler import DataHandler
from app.backtester import Backtester
from app.results import Results
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
    source : str
        Data source to use ('yahoo' or 'csv').

    Attributes
    ----------
    data_handler : DataHandler
        Instance responsible for fetching market data.
    """

    def __init__(self, source: str = "yahoo"):
        """
        Initializes the Controller instance and sets up the DataHandler.

        Parameters
        ----------
        source : str, optional
            Data source to use ('yahoo' or 'csv'), default is 'yahoo'.
        """
        self.source = source  # Save the source type
        self.data_handler = DataHandler(source=source)

    def run_backtest(self, ticker: str = None, source_path: str = None, strategy_name: str = None, strategy_params: dict = None, initial_cash: float = 100000.0) -> tuple:
        """
        Runs the full backtesting workflow based on user input.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol to fetch data for (Yahoo).
        source_path : str
            The CSV file path to load data from (CSV).
        strategy_name : str
            The name of the strategy to use ('sma_crossover', 'rsi_threshold', etc.).
        strategy_params : dict
            Dictionary containing parameters for the selected strategy.
        initial_cash : float
            Initial portfolio cash for the backtest (default is 100,000).

        Returns
        -------
        tuple
            Tuple containing the equity curve DataFrame and performance metrics dictionary.
        """

        # Load data based on source
        if self.source == "yahoo":
            self.data_handler.load_data(ticker)
        elif self.source == "csv":
            self.data_handler.load_data(source_path)

        # Fetch historical data
        data = self.data_handler.fetch_data()

        # Initialize the selected strategy
        strategy = self._initialize_strategy(strategy_name, data, strategy_params)

        # Initialize the backtester
        backtester = Backtester(data, strategy, initial_cash)

        # Run the backtest and get the equity curve
        equity_curve = backtester.run_backtest()

        # Calculate the performance metrics
        results_analyzer = Results(equity_curve)
        performance_metrics = results_analyzer.calculate_performance_metrics()

        return equity_curve, performance_metrics

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