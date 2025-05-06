"""
main.py

Command-line interface for running the backtesting engine.

Allows the user to select a data source, trading strategy, input stock ticker or CSV,
and execute a backtest using the modular backtesting system.
"""

import os
import numpy as np
from datetime import datetime
from app.controller import Controller

def main():
    """
    Main function to run the backtesting CLI workflow.
    """

    # Select your data source
    print("\nSelect data source:")
    print("1. Yahoo Finance (live)")
    print("2. Local CSV file") 

    source_choice = input("\nEnter 1 or 2: ").strip()

    ticker = None  # Default
    csv_path = None  # Default

    if source_choice == "1":
        source = "yahoo"
        ticker = input("\nEnter the stock ticker symbol (ex. AAPL, MSFT, TSLA): ").strip().upper()
    elif source_choice == "2":
        source = "csv"
        csv_filename = input("Enter the CSV filename (just the file name, e.g., 'sample_prices.csv'): ").strip()
        csv_path = os.path.join("data", csv_filename)
    else:
        print("Invalid selection. Defaulting to Yahoo Finance.")
        source = "yahoo"
        ticker = input("\nEnter the stock ticker symbol (ex. AAPL, MSFT, TSLA): ").strip().upper()

    # Initialize the Controller
    controller = Controller(source=source)

    # Display available strategies
    print("\nSelect a trading strategy:")
    print("1. SMA Crossover Strategy")
    print("2. RSI Threshold Strategy")
    print("3. Golden Cross Strategy")
    print("4. Momentum Strategy (Rate of Change)")
    print("5. Breakout Strategy")

    # Get user input for strategy selection
    strategy_choice = input("\nEnter the number corresponding to your chosen strategy (1-5): ").strip()

    # Map user choice to strategy name
    strategy_mapping = {
        "1": "sma_crossover",
        "2": "rsi_threshold",
        "3": "golden_cross",
        "4": "momentum",
        "5": "breakout"
    }

    if strategy_choice not in strategy_mapping:
        print("Invalid selection. Please run the program again and select a valid option (1-5).")
        return

    strategy_name = strategy_mapping[strategy_choice]

    # Prepare default parameters for each strategy
    strategy_params = {}

    if strategy_name == "sma_crossover":
        short_window = int(input("\nEnter the short-term SMA window (ex, 20): "))
        long_window = int(input("Enter the long-term SMA window (ex, 50): "))
        strategy_params = {"short_window": short_window, "long_window": long_window}

    elif strategy_name == "rsi_threshold":
        buy_threshold = int(input("\nEnter the RSI buy threshold (ex, 30): "))
        sell_threshold = int(input("Enter the RSI sell threshold (ex, 70): "))
        strategy_params = {"buy_threshold": buy_threshold, "sell_threshold": sell_threshold}

    elif strategy_name == "momentum":
        roc_period = int(input("\nEnter the Rate of Change (ROC) period (ex, 20): "))
        threshold = float(input("Enter the momentum threshold for buying (ex, 0.05): "))
        strategy_params = {"roc_period": roc_period, "threshold": threshold}

    elif strategy_name == "breakout":
        entry_period = int(input("\nEnter the breakout entry period (ex, 25): "))
        exit_period = int(input("Enter the breakout exit period (ex, 15): "))
        strategy_params = {"entry_period": entry_period, "exit_period": exit_period}

    # Golden Cross doesn't require user parameters

    # Run the backtest using the Controller
    print("\nRunning backtest... please wait.\n")

    try:
        equity_curve, performance_metrics = controller.run_backtest(
            ticker=ticker,
            source_path=csv_path,
            strategy_name=strategy_name,
            strategy_params=strategy_params
        )

        # Display the first few rows of the equity curve
        print(equity_curve.head())

        # ===============================
        # Display performance metrics
        # ===============================

        print("\nPerformance Summary:")
        for metric, value in performance_metrics.items():
            if "Return" in metric or "Volatility" in metric or "Drawdown" in metric:
                print(f"{metric}: {value*100:.2f}%")
            else:
                print(f"{metric}: {value:.2f}")

        # ===============================
        # Save results to /performance/ folder
        # ===============================

        # Copy results DataFrame and add performance metrics as new columns
        results_to_save = equity_curve.copy()
        for metric, value in performance_metrics.items():
            results_to_save[metric] = value

        # Create performance directory if it doesn't exist
        os.makedirs('performance', exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance/{ticker or csv_filename.replace('.csv', '')}_{strategy_name}_{timestamp}.csv"

        # Save to CSV
        results_to_save.to_csv(filename)

        print(f"\nResults saved to {filename}")

    except Exception as e:
        print(f"\nAn error occurred during the backtest: {str(e)}")


if __name__ == "__main__":
    main()