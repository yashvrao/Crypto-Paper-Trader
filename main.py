import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import schedule
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize exchange
def init_exchange():
    logging.info("Initializing exchange...")
    return ccxt.binance({
        'apiKey': 'BINANCE_API_KEY',
        'secret': 'BINANCE_API_SECRET',
    })

# Fetch data
def fetch_data(exchange, symbol, timeframe):
    logging.info(f"Fetching data for {symbol} with timeframe {timeframe}...")
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except ccxt.BaseError as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Calculate moving averages and signals
def calculate_indicators(df):
    logging.info("Calculating indicators...")
    df['short_ma'] = df['close'].rolling(window=5).mean()
    df['long_ma'] = df['close'].rolling(window=20).mean()
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
    return df

# Place order
def place_order(exchange, signal, symbol):
    try:
        if signal == 1:
            logging.info(f"Placing Buy Order for {symbol}...")
            order = exchange.create_market_buy_order(symbol, 0.001)
            print("Buy Order:", order)
        elif signal == -1:
            logging.info(f"Placing Sell Order for {symbol}...")
            order = exchange.create_market_sell_order(symbol, 0.001)
            print("Sell Order:", order)
    except Exception as e:
        logging.info(f"No action for signal {signal}")
        print(f"Error placing order: {e}")

# Plot performance
def plot_performance(df):
    logging.info("Plotting performance...")
    df['position'] = df['signal'].shift(1)
    df['returns'] = df['close'].pct_change() * df['position']
    cumulative_returns = (1 + df['returns']).cumprod()
    plt.plot(df['timestamp'], cumulative_returns, label='Strategy')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()

# Run bot
def run_bot():
    logging.info("Running bot...")
    exchange = init_exchange()
    symbol = 'ETH/USDT'
    timeframe = '1h'
    df = fetch_data(exchange, symbol, timeframe)
    if df.empty:
        logging.error("No data fetched. Exiting bot run.")
        return
    df = calculate_indicators(df)
    latest_signal = df['signal'].iloc[-1]
    place_order(exchange, latest_signal, symbol)
    plot_performance(df)

# Schedule bot to run every hour
schedule.every(1).hours.do(run_bot)

if __name__ == "__main__":
    logging.info("Starting trading bot...")
    run_bot()
    while True:
        schedule.run_pending()
        time.sleep(1)