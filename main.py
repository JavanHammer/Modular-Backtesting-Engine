"""
main.py

Command-line interface for running the backtesting engine.

Allows the user to select a trading strategy, input stock ticker,
and execute a backtest using the modular backtesting system.
"""

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

        # Display results
        print(results.head())

    except Exception as e:
        print(f"\nAn error occurred during the backtest: {str(e)}")

# Ensures that the main() function runs only when this script is executed directly,
# and not when it is imported as a module.
if __name__ == "__main__":
    main()
