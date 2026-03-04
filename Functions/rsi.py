import pandas as pd
import numpy as np


def prepare_ticker_data(dataframe, ticker):
    ticker = ticker.upper()
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()

    if ticker_df.empty:
        return None

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    return ticker_df


def get_rsi_status(dataframe, ticker, window_days=14):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return {"error": f"No data found for {ticker}"}

    delta = ticker_df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/window_days, min_periods=window_days).mean()
    avg_loss = loss.ewm(alpha=1/window_days, min_periods=window_days).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    latest_rsi = rsi.iloc[-1]

    if latest_rsi > 70:
        interpretation = "Overbought: The stock may be due for a pullback."
        signal = "High"
    elif latest_rsi < 30:
        interpretation = "Oversold: The stock may be due for a bounce."
        signal = "Low"
    else:
        interpretation = "Neutral: No extreme momentum conditions."
        signal = "Neutral"

    return {
        "ticker": ticker,
        "rsi": round(float(latest_rsi), 2),
        "signal": signal,
        "interpretation": interpretation
    }