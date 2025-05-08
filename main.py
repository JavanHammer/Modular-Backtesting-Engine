"""
main.py

Command-line interface for running the backtesting engine.
Allows the user to select a data source, trading strategy, input stock ticker or CSV,
and execute a backtest using the modular backtesting system.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime
from app.controller import Controller

def main():
    """
    Main function to run the backtesting CLI workflow.
    Guides the user through selecting a data source, choosing a strategy,
    inputting parameters, executing the backtest, and saving results.
    """

    # Prompt the user to select a data source
    print("\nSelect data source:")
    print("1. Yahoo Finance (live)")
    print("2. Local CSV file")

    source_choice = input("\nEnter 1 or 2: ").strip()

    ticker = None
    csv_path = None

    if source_choice == "1":
        source = "yahoo"
        ticker = input("\nEnter the stock ticker symbol (ex. AAPL, MSFT, TSLA): ").strip().upper()
    elif source_choice == "2":
        source = "csv"
        csv_filename = input("Enter the CSV filename or press enter to use the 'sample_prices.csv'").strip()

        if csv_filename == "":
            csv_filename = "sample_prices.csv"

        csv_path = os.path.join("data", csv_filename)
    else:
        # Default to Yahoo Finance if invalid input
        print("Invalid selection. Defaulting to Yahoo Finance.")
        source = "yahoo"
        ticker = input("\nEnter the stock ticker symbol (ex. AAPL, MSFT, TSLA): ").strip().upper()

    # Set the source name for later file saving
    if source == "yahoo":
        source_name = ticker
    else:
        source_name = os.path.splitext(os.path.basename(csv_path))[0]

    controller = Controller(source=source)

    # Prompt the user to select a trading strategy
    print("\nSelect a trading strategy:")
    print("1. SMA Crossover Strategy")
    print("2. RSI Threshold Strategy")
    print("3. Golden Cross Strategy")
    print("4. Momentum Strategy (Rate of Change)")

    strategy_choice = input("\nEnter the number corresponding to your chosen strategy (1-4): ").strip()

    strategy_mapping = {
        "1": "sma_crossover",
        "2": "rsi_threshold",
        "3": "golden_cross",
        "4": "momentum"
    }

    if strategy_choice not in strategy_mapping:
        print("Invalid selection. Please run the program again and select a valid option (1-4).")
        return

    strategy_name = strategy_mapping[strategy_choice]
    strategy_params = {}

    # Collect parameters for strategies that require them
    if strategy_name == "sma_crossover":
        short_window = int(input("\nEnter the short-term SMA window (ex. 20): "))
        long_window = int(input("Enter the long-term SMA window (ex. 50): "))
        strategy_params = {"short_window": short_window, "long_window": long_window}

    elif strategy_name == "rsi_threshold":
        buy_threshold = int(input("\nEnter the RSI buy threshold (ex. 30): "))
        sell_threshold = int(input("Enter the RSI sell threshold (ex. 70): "))
        strategy_params = {"buy_threshold": buy_threshold, "sell_threshold": sell_threshold}

    elif strategy_name == "momentum":
        roc_period = int(input("\nEnter the Rate of Change (ROC) period (ex. 20): "))
        roc_threshold = float(input("Enter the momentum threshold for buying (ex. 0.05): "))
        strategy_params = {"roc_period": roc_period, "roc_threshold": roc_threshold}

    print("\nRunning backtest... please wait.\n")

    try:
        # Execute backtest
        equity_curve, performance_metrics, total_trades = controller.run_backtest(
            ticker=ticker,
            source_path=csv_path,
            strategy_name=strategy_name,
            strategy_params=strategy_params
        )

    except Exception as e:
        # Check if Yahoo Finance download failed
        if "Failed download" in str(e) or "No data" in str(e) or "Not enough data" in str(e):
            print("\n^^^^^^^Yahoo Finance download failed or returned no data (possible rate limit or no data available).")

            fallback = input("\nPress enter to use the default sample_prices.csv instead.\nOtherwise, type q to quit the program.").strip().lower()
            if fallback == "":
                # Switch to local CSV mode
                source = "csv"
                source_name = "sample_prices"
                csv_path = os.path.join("data", "sample_prices.csv")

                # Create a new Controller instance for CSV
                controller = Controller(source="csv")

                print("\nRunning backtest... please wait.\n")

                try:
                    # Rerun the backtest with sample_prices.csv
                    equity_curve, performance_metrics, total_trades = controller.run_backtest(
                        source_path=csv_path,
                        strategy_name=strategy_name,
                        strategy_params=strategy_params
                    )
                except Exception as e2:
                    print(f"\nAn error occurred even when trying with sample_prices.csv: {str(e2)}")
                    return
            else:
                print("\nExiting program. Please try again later.")
                return
        else:
            print(f"\nAn unexpected error occurred: {str(e)}")
            return

    # Check if any trades were made
    if total_trades == 0:
        print("\nNo trades were executed during the backtest.")
        return

    # Display performance summary
    print("\nPerformance Summary:")
    print(f"Total Trades Executed: {total_trades}")
    for metric, value in performance_metrics.items():
        if "Return" in metric or "Volatility" in metric or "Drawdown" in metric:
            print(f"{metric}: {value*100:.8f}%")
        else:
            print(f"{metric}: {value:.8f}")

    # Save results to performance/ folder
    os.makedirs('performance', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create filename including strategy parameters if any
    param_str = ''
    if strategy_params:
        param_str = '_' + '_'.join(f"{key}{value}" for key, value in strategy_params.items())

    filename = f"performance/{source_name}_{strategy_name}{param_str}_{timestamp}.csv"

    # Combine metrics and equity curve into one CSV
    metrics_df = pd.DataFrame([performance_metrics])
    metrics_df.index = ['Performance Summary']

    empty_row = pd.DataFrame([{}])  # Blank line between metrics and equity curve

    combined = pd.concat([metrics_df, empty_row, equity_curve])
    combined.to_csv(filename)

    print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    main()