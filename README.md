# Crypto Paper Trader

Crypto Paper Trader is a Python-based trading bot that uses the Binance exchange to fetch market data, calculate trading signals, and place buy/sell orders based on moving average indicators. This bot is designed for paper trading, allowing you to test trading strategies without risking real money.

## Features

- Fetches market data from Binance
- Calculates short-term and long-term moving averages
- Generates buy/sell signals based on moving average crossovers
- Places market buy/sell orders
- Plots cumulative returns of the trading strategy

## Requirements

- Python 3.13.1
- `ccxt` library
- `pandas` library
- `matplotlib` library
- `schedule` library

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/YashV/Crypto-Paper-Trader.git
    cd Crypto-Paper-Trader
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install ccxt pandas matplotlib schedule
    ```

4. Set up your Binance API keys in the `.env` file:
    ```properties
    BINANCE_API_KEY=your_api_key_here
    BINANCE_API_SECRET=your_api_secret_here
    ```

## Usage

1. Activate the virtual environment:
    ```sh
    source .venv/bin/activate
    ```

2. Run the trading bot:
    ```sh
    python main.py
    ```

The bot will fetch market data, calculate indicators, place orders, and plot the performance of the trading strategy. It is scheduled to run every hour.

## Disclaimer

This bot is for educational purposes only, and trades fake crypto.

## License

This project is licensed under the MIT License.