import pandas as pd
import numpy as np

def validate_inputs(df, ticker, window):
    """
    Validates that the ticker exists in the dataframe and the window is positive.
    """
    if ticker not in df['symbol'].unique():
        raise ValueError(f"Ticker '{ticker}' not found in dataset.")
    if window <= 0:
        raise ValueError("Window must be a positive integer.")

def get_ticker_data(df, ticker):
    """
    Filters the dataframe for a specific ticker and ensures it's sorted by timestamp.
    """
    ticker_df = df[df['symbol'] == ticker].copy()
    ticker_df['timestamp'] = pd.to_datetime(ticker_df['timestamp'])
    return ticker_df.sort_values('timestamp')

def moving_average(df, ticker, window):
    """
    Calculates the Simple Moving Average (SMA) for a given ticker and window.
    """
    validate_inputs(df, ticker, window)
    ticker_df = get_ticker_data(df, ticker)
    return ticker_df['close'].rolling(window=window).mean()

def percent_price_change(df, ticker, window):
    """
    Calculates the percentage price change over a given window.
    """
    validate_inputs(df, ticker, window)
    ticker_df = get_ticker_data(df, ticker)
    return ticker_df['close'].pct_change(periods=window) * 100

def rolling_volatility(df, ticker, window):
    """
    Calculates the rolling volatility (standard deviation of daily returns) over a window.
    """
    validate_inputs(df, ticker, window)
    ticker_df = get_ticker_data(df, ticker)
    daily_returns = ticker_df['close'].pct_change()
    return daily_returns.rolling(window=window).std()

def rsi(df, ticker, window=14):
    """
    Calculates the Relative Strength Index (RSI) for a given ticker and window.
    """
    validate_inputs(df, ticker, window)
    ticker_df = get_ticker_data(df, ticker)
    
    delta = ticker_df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi_vals = 100 - (100 / (1 + rs))
    return rsi_vals
