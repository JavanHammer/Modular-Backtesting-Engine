# Modular Backtesting Engine (Phase 1)

A clean, modular Python backtesting engine for systematic trading strategy research.

Built for **local CLI-based backtesting**, with **unit-tested modules**, ready to evolve into full **cloud deployment** and **machine learning-driven strategy generation** in future phases.

---

## 📂 Project Structure

```plaintext
Modular-Backtesting-Engine/
├── app/
│   ├── backtester.py         # Simulates trading based on strategy signals
│   ├── controller.py         # Orchestrates data loading, strategy, backtesting, and results
│   ├── data_handler.py       # Loads historical data (Yahoo Finance or CSV)
│   ├── results.py            # Calculates performance metrics (Sharpe, Return, Drawdown)
│   └── strategies/
│       ├── __init__.py        # Strategy imports
│       ├── breakout.py        # Breakout trading strategy
│       ├── golden_cross.py    # Golden Cross (50/200 SMA) strategy
│       ├── momentum.py        # Momentum (Rate of Change) strategy
│       ├── rsi_threshold.py   # RSI threshold strategy
│       └── sma_crossover.py   # Short/long SMA crossover strategy
│
├── performance/              # Backtest result outputs (.csv)
├── data/                     # Local CSV files (ex. sample_prices.csv)
├── testing/                  # Unit tests
├── main.py                   # Command-line runner
├── requirements.txt          # Python dependencies
├── .gitignore                # Files/folders ignored by Git
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the backtesting engine (CLI)
```bash
python main.py
```
You'll be guided through:
- Choosing a **data source** (Yahoo Finance live or local CSV)
- Choosing a **strategy**
- Entering **strategy parameters**
- Running a **backtest**
- Saving performance results automatically

---

## 🛠 Supported Trading Strategies

| Strategy                    | Description |
|------------------------------|-------------|
| **SMA Crossover**            | Buy/sell based on short-term and long-term SMA crossovers |
| **RSI Threshold**            | Buy when RSI oversold, sell when overbought |
| **Golden Cross**             | Buy on 50-day SMA crossing above 200-day SMA |
| **Momentum (Rate of Change)**| Buy/sell based on momentum thresholds |
| **Breakout**                 | Buy breakouts above past highs, sell breakdowns below lows |

Each strategy is fully modular and easily extendable.

---

## 📈 Performance Metrics Calculated

After each backtest, the following are automatically computed:

- **Total Return**
- **Annualized Volatility**
- **Sharpe Ratio**
- **Maximum Drawdown**

Results are saved in the `/performance/` folder, including a copy of the equity curve and metrics.

---

## 🧪 Running Unit Tests

Unit tests cover:
- Data loading
- Backtester logic
- Controller orchestration
- Individual strategies
- Performance metric calculations

To run all tests (CLI):

```bash
pytest testing/
```

---

## 📋 Documentation and Code Style

This project follows strict documentation and commenting conventions:
- Every **file** has a **module-level docstring**.
- Every **class** has a **full docstring** (purpose, parameters, attributes).
- Every **method** has a **short docstring**.
- Important logic sections are explained with **inline comments**.

---

## 🔥 Project Roadmap

- **Phase 2**: Add Snowflake integration (store results in Snowflake DB)
- **Phase 3**: Build Streamlit UI inside Snowflake (SiS)
- **Phase 4**: Machine learning-driven strategy discovery (Databricks)
- **Phase 5**: Monte Carlo simulation for strategy stress testing

---

## 📜 License

This project is currently for educational, research, and personal use only.

---
