import pandas as pd
import numpy as np


def prepare_ticker_data(dataframe, ticker):
    ticker = ticker.upper()
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()

    if ticker_df.empty:
        return None

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)
    return ticker_df


def get_volatility_status(dataframe, ticker, window_days=30):
    ticker_df = prepare_ticker_data(dataframe, ticker)
    if ticker_df is None:
        return {"error": f"No data found for {ticker}"}

    log_returns = np.log(ticker_df["close"] / ticker_df["close"].shift(1))
    rolling_vol = log_returns.rolling(window_days).std()

    latest_vol = rolling_vol.iloc[-1] * np.sqrt(252)  # annualized

    if latest_vol > 0.6:
        interpretation = "High Volatility: Large price swings."
        level = "High"
    elif latest_vol < 0.2:
        interpretation = "Low Volatility: Stable price movement."
        level = "Low"
    else:
        interpretation = "Moderate Volatility."
        level = "Moderate"

    return {
        "ticker": ticker,
        "annualized_volatility": round(float(latest_vol), 4),
        "level": level,
        "interpretation": interpretation
    }