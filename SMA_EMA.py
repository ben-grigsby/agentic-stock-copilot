# Andrew
import pandas as pd
import numpy as np

def calculate_simple_moving_average(dataframe, ticker, window_days):
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()
    if ticker_df.empty:
        return ticker_df

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    # Calculate the simple moving average
    sma_col = f"sma_{window_days}d"
    ticker_df[sma_col] = ticker_df['close'].rolling(window=window_days).mean()
    
    return ticker_df

def calculate_exponential_moving_average(dataframe, ticker, window_days):
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()
    if ticker_df.empty:
        return ticker_df
    
    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    # Calculate the exponential moving average
    ema_col = f"ema_{window_days}d"
    ticker_df[ema_col] = ticker_df['close'].ewm(span=window_days).mean()

    
def get_momentum_status(dataframe, ticker, window_days):
    """
    Combines SMA and EMA to give a comprehensive momentum 'score'.
    """
    sma_df = calculate_simple_moving_average(dataframe, ticker, window_days)
    ema_df = calculate_exponential_moving_average(dataframe, ticker, window_days)
    
    if sma_df.empty or ema_df.empty:
        return {"error": f"No data found for {ticker}"}

    latest_sma = sma_df.iloc[-1][f'sma_{window_days}d']
    latest_ema = ema_df.iloc[-1][f'ema_{window_days}d']
    current_price = sma_df.iloc[-1]['close']
    
    if current_price > latest_ema and latest_ema > latest_sma:
        interpretation = "Strong Bullish: The price is accelerating upwards and is above its long-term average."
        momentum = "High"
    elif current_price > latest_ema and current_price < latest_sma:
        interpretation = "Recovery: The price is bouncing back quickly, but still below its long-term average."
        momentum = "Low-Medium"
    elif current_price < latest_ema and latest_ema < latest_sma:
        interpretation = "Strong Bearish: The price is falling quickly and the overall trend is downward."
        momentum = "Very Low"
    else:
        interpretation = "Consolidation: The indicators are mixed, suggesting the price is moving sideways."
        momentum = "Neutral"

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "ema": round(latest_ema, 2),
        "sma": round(latest_sma, 2),
        "momentum": momentum,
        "interpretation": interpretation
    }