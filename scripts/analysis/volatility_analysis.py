#Parwaan


import pandas as pd
import numpy as np

def calculate_historical_volatility(dataframe: pd.DataFrame, ticker: str, window_days: int = 20) -> pd.DataFrame:
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()
    
    if ticker_df.empty:
        print(f"Warning: No data found for ticker {ticker}")
        return ticker_df

    ticker_df = ticker_df.sort_values("timestamp", ascending=True)

    ticker_df['daily_return'] = ticker_df['close'].pct_change() * 100

    volatility_col = f"volatility_{window_days}d"
    ticker_df[volatility_col] = ticker_df['daily_return'].rolling(window=window_days).std() * np.sqrt(252)

    return ticker_df


def get_current_volatility(dataframe: pd.DataFrame, ticker: str, window_days: int = 20) -> dict:

    result_df = calculate_historical_volatility(dataframe, ticker, window_days)
    
    if result_df.empty:
        return {"error": f"No data found for {ticker}"}
    
    volatility_col = f"volatility_{window_days}d"
    latest = result_df[result_df[volatility_col].notna()].iloc[-1]
    
    vol_value = latest[volatility_col]
    
    if vol_value < 15:
        interpretation = "Low volatility - relatively stable price movement"
    elif vol_value < 25:
        interpretation = "Moderate volatility - typical for established stocks"
    elif vol_value < 40:
        interpretation = "High volatility - significant price swings"
    else:
        interpretation = "Very high volatility - extreme price fluctuations"
    
    return {
        "ticker": ticker,
        "current_volatility": round(vol_value, 2),
        "window_days": window_days,
        "date": latest['timestamp'],
        "interpretation": interpretation
    }
