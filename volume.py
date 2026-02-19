# Andrew
import pandas as pd
def volume_analysis(dataframe, ticker, window_days=20):
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()
    if ticker_df.empty:
        return {"error": f"No data found for {ticker}"} 
    
    latest_volume = ticker_df.iloc[-1]['volume']
    average_volume = ticker_df.tail(window_days)['volume'].mean()
    
    ratio = latest_volume / average_volume
    
    if ratio > 2.0:
        interpretation = "Extremely High Volume: Massive interest or 'Big Money' movement detected. High conviction."
    elif ratio > 1.5:
        interpretation = "High Volume: More activity than usual, confirming the current price move."
    elif ratio < 0.5:
        interpretation = "Low Volume: Very thin trading activity. Watch out for liquidity risk or 'fake' price moves."
    else:
        interpretation = "Normal Volume: Standard trading activity with no major surprises."
        
    return {
        "ticker": ticker,
        "current_volume": int(latest_volume),
        "avg_volume": int(average_volume),
        "interpretation": interpretation
    }
    
def vwap_analysis(dataframe, ticker):
    ticker_df = dataframe[dataframe['symbol'] == ticker].copy()
    if ticker_df.empty:
        return {"error": f"No data found for {ticker}"} 
    latest = ticker_df.sort_values("timestamp").iloc[-1]
    
    current_price = latest['close']
    vwap_value = latest['vwap']
    
    if current_price > vwap_value:
        interpretation = "Price is above average cost. Buyers are in control."
    else:
        interpretation = "Price is below average cost. May be a value entry or showing weakness."

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "vwap": round(vwap_value, 2),
        "interpretation": interpretation
    }