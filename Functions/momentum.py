# Andrew
import pandas as pd
import numpy as np

def prepare_ticker_data(dataframe, ticker):
    ticker = ticker.upper()
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()

    if ticker_df.empty:
        return None

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    return ticker_df


def calculate_sma(dataframe, ticker, window_days):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return None

    sma = ticker_df["close"].rolling(window=window_days).mean().iloc[-1]

    return {
        "ticker": ticker,
        "window_days": window_days,
        "sma": round(float(sma), 2)
    }
    
def calculate_ema(dataframe, ticker, window_days):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return None

    ema = ticker_df["close"].ewm(span=window_days).mean().iloc[-1]

    return {
        "ticker": ticker,
        "window_days": window_days,
        "ema": round(float(ema), 2)
    }

def get_momentum_status(dataframe, ticker, window_days):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return {"error": f"No data found for {ticker}"}

    current_price = ticker_df.iloc[-1]["close"]

    sma_result = calculate_sma(dataframe, ticker, window_days)
    ema_result = calculate_ema(dataframe, ticker, window_days)

    latest_sma = sma_result["sma"]
    latest_ema = ema_result["ema"]

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
        "current_price": round(float(current_price), 2),
        "ema": latest_ema,
        "sma": latest_sma,
        "momentum": momentum,
        "interpretation": interpretation
    }
