import pandas as pd
import numpy as np


def prepare_ticker_data(dataframe, ticker):
    ticker = ticker.upper()
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()

    if ticker_df.empty:
        return None

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    return ticker_df


def get_volume_status(dataframe, ticker, window_days=20):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return {"error": f"No data found for {ticker}"}

    avg_volume = ticker_df["volume"].rolling(window_days).mean().iloc[-1]
    current_volume = ticker_df["volume"].iloc[-1]

    ratio = current_volume / avg_volume if avg_volume != 0 else 0

    if ratio > 1.5:
        interpretation = "High Volume: Strong participation in price movement."
        activity = "High"
    elif ratio < 0.7:
        interpretation = "Low Volume: Weak market participation."
        activity = "Low"
    else:
        interpretation = "Normal Volume: Typical trading activity."
        activity = "Normal"

    return {
        "ticker": ticker,
        "current_volume": int(current_volume),
        "average_volume": int(avg_volume),
        "volume_ratio": round(float(ratio), 2),
        "activity": activity,
        "interpretation": interpretation
    }