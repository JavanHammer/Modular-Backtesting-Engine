"""
main.py

Command-line interface for running the backtesting engine.

Allows the user to select a trading strategy, input stock ticker,
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

    # Initialize the Controller
    controller = Controller()

    # Get stock ticker input
    ticker = input("\nEnter the stock ticker symbol (ex, AAPL, MSFT, TSLA): ").strip().upper()

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

    # Golden Cross doesn't require user parameters — uses fixed 50/200 SMA

    # Run the backtest using the Controller
    print("\nRunning backtest... please wait.\n")

    try:
        results = controller.run_backtest(
            ticker=ticker,
            strategy_name=strategy_name,
            strategy_params=strategy_params
        )

        # Display the first few rows of results
        print(results.head())

        # ===============================
        # Calculate and display performance metrics
        # ===============================

        # Calculate daily returns
        results['Returns'] = results['Equity'].pct_change()

        # Calculate performance metrics
        cumulative_return = results['Equity'].iloc[-1] / results['Equity'].iloc[0] - 1
        annualized_return = (1 + cumulative_return) ** (252 / len(results)) - 1
        annualized_volatility = results['Returns'].std() * np.sqrt(252)
        sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0
        max_drawdown = ((results['Equity'].cummax() - results['Equity']) / results['Equity'].cummax()).max()

        # Prepare performance summary
        performance_summary = {
            "Cumulative Return (%)": cumulative_return * 100,
            "Annualized Return (%)": annualized_return * 100,
            "Annualized Volatility (%)": annualized_volatility * 100,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown (%)": max_drawdown * 100
        }

        # Print performance summary
        print("\nPerformance Summary:")
        for metric, value in performance_summary.items():
            print(f"{metric}: {value:.2f}")

        # ===============================
        # Save results to /performance/ folder
        # ===============================

        # Copy results DataFrame and add performance metrics
        results_to_save = results.copy()
        for metric, value in performance_summary.items():
            results_to_save[metric] = value

        # Create performance directory if it doesn't exist
        os.makedirs('performance', exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance/{ticker}_{strategy_name}_{timestamp}.csv"

        # Save to CSV
        results_to_save.to_csv(filename)

        print(f"\nResults saved to {filename}")

    except Exception as e:
        print(f"\nAn error occurred during the backtest: {str(e)}")

# Ensures that the main() function runs only when this script is executed directly,
# and not when it is imported as a module.
if __name__ == "__main__":
    main()