# Momentum Trading Bot with Backtesting

## Overview

This project implements a momentum trading bot that uses technical indicators to generate buy and sell signals for stocks. The bot uses the KiteConnect API to connect to Zerodha for placing orders. The project also includes a backtesting script to evaluate the performance of the trading strategy.

## Functionality

The project consists of the following main components:

1.  **`Momentum_trading bot.py`:**
    *   Connects to the Zerodha Kite API using API key, API secret, and request token.
    *   Defines a list of stocks to trade.
    *   Retrieves historical data for each stock using the `yfinance` library.
    *   Calculates technical indicators such as RSI, MACD, and Bollinger Bands.
    *   Generates buy and sell signals based on the indicator values.
    *   Places orders using the KiteConnect API.
    *   Calculates net profit or loss and brokerage charges.
2.  **`Backtest_2.ipynb`:**
    *   Backtests the momentum trading strategy using the `backtesting.py` library.
    *   Defines the trading strategy based on RSI and Bollinger Bands.
    *   Optimizes the strategy parameters to maximize the Sharpe Ratio.
    *   Plots the backtesting results and analyzes the trades.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/git098/MFT_bot.git
    cd MFT_bot
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Set up Zerodha Kite API credentials:**

    *   Obtain API key, API secret, and request token from Zerodha Kite Developer Console.
    *   Replace the placeholder values in `Momentum_trading bot.py` with your actual credentials.
2.  **Run the Momentum Trading Bot:**

    ```bash
    python Momentum_trading bot.py
    ```

    The bot will connect to Zerodha Kite API, retrieve historical data, generate trading signals, and place orders.
3.  **Run the Backtesting Script:**

    *   Open `Backtest_2.ipynb` using Jupyter Notebook or JupyterLab.
    *   Run the cells in the notebook to backtest the trading strategy and optimize its parameters.

## Requirements

*   Python 3.6+
*   `kiteconnect`
*   `pandas`
*   `yfinance`
*   `matplotlib`
*   `ta-lib`
*   `backtesting`
*   `scipy`

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
