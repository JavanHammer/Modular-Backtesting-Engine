"""
results.py

Module to calculate performance metrics from the portfolio equity curve.
"""

import pandas as pd
import numpy as np

class Results:
    """
    Analyze a portfolio's equity curve and calculate performance metrics.

    Parameters:
    portfolio (pd.DataFrame): A Dataframe containing a 'Portfolio Value' column.

    Attributes:
    portfolio (pd.DataFrame): The input equity curve data.
    """

    def __init__(self, portfolio: pd.DataFrame):
        """Initialize the Results object with a portfolio equity curve."""
        self.portfolio = portfolio

    def calculate_performance_metrics(self) -> dict:
        """
        Calculate and return key performance metrics.

        Returns:
        dict: A dictionary containing Total Return, Volatility, Sharpe Ratio, and Max Drawdown.
        """
        returns = self.portfolio['Portfolio Value'].pct_change().dropna()

        total_return = (self.portfolio['Portfolio Value'].iloc[-1] / self.portfolio['Portfolio Value'].iloc[0]) - 1
        volatility = returns.std() * (252 ** 0.5)  # Annualized volatility (Think 252 trading days in a year)
        sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5) if returns.std() != 0 else 0
        max_drawdown = ((self.portfolio['Portfolio Value'].cummax() - self.portfolio['Portfolio Value']) / self.portfolio['Portfolio Value'].cummax()).max()

        return {
            "Total Return": total_return,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
        }