import pandas as pd
import numpy as np


def prepare_ticker_data(dataframe, ticker):
    ticker = ticker.upper()
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()

    if ticker_df.empty:
        return None

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    return ticker_df


def get_macd_status(dataframe, ticker):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return {"error": f"No data found for {ticker}"}

    close = ticker_df["close"]

    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()

    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()

    latest_macd = macd.iloc[-1]
    latest_signal = signal.iloc[-1]
    histogram = latest_macd - latest_signal

    if latest_macd > latest_signal:
        interpretation = "Bullish Crossover: Upward momentum building."
        trend = "Bullish"
    elif latest_macd < latest_signal:
        interpretation = "Bearish Crossover: Downward momentum building."
        trend = "Bearish"
    else:
        interpretation = "Neutral: Momentum is balanced."
        trend = "Neutral"

    return {
        "ticker": ticker,
        "macd": round(float(latest_macd), 4),
        "signal_line": round(float(latest_signal), 4),
        "histogram": round(float(histogram), 4),
        "trend": trend,
        "interpretation": interpretation
    }