# Minho 
# RSI: Relative Strength Index

import pandas as pd


def calculate_rsi(dataframe: pd.DataFrame, ticker: str, window_days: int = 14) -> pd.DataFrame:
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()

    if ticker_df.empty:
        print(f"Warning: No data found for ticker {ticker}")
        return ticker_df

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)

    # Price changes
    delta = ticker_df['close'].diff()

    # Gains and losses
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    # Wilder's smoothing using an EMA with alpha=1/window_days
    avg_gain = gain.ewm(alpha=1.0 / window_days, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / window_days, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    rsi_col = f"rsi_{window_days}d"
    ticker_df[rsi_col] = rsi

    return ticker_df


def get_current_rsi(dataframe: pd.DataFrame, ticker: str, window_days: int = 14) -> dict:
    result_df = calculate_rsi(dataframe, ticker, window_days)

    if result_df.empty:
        return {"error": f"No data found for {ticker}"}

    rsi_col = f"rsi_{window_days}d"
    latest = result_df[result_df[rsi_col].notna()].iloc[-1]

    rsi_value = latest[rsi_col]

    if rsi_value < 30:
        interpretation = "Oversold (RSI < 30) — potential buy signal"
    elif rsi_value > 70:
        interpretation = "Overbought (RSI > 70) — potential sell signal"
    else:
        interpretation = "Neutral (RSI 30-70) — no extreme momentum"

    return {
        "ticker": ticker,
        "current_rsi": round(rsi_value, 2),
        "window_days": window_days,
        "date": latest['timestamp'],
        "interpretation": interpretation
    }