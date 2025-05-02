"""
__init__.py

Imports all strategy classes for easy access from the strategies module.
"""

from .sma_crossover import SMACrossoverStrategy
from .rsi_threshold import RSIThresholdStrategy
from .golden_cross import GoldenCrossStrategy
from .momentum import MomentumStrategy
from .breakout import BreakoutStrategy

__all__ = [
    "SMACrossoverStrategy",
    "RSIThresholdStrategy",
    "GoldenCrossStrategy",
    "MomentumStrategy",
    "BreakoutStrategy"
]