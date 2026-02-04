#Parwaan


import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analysis.volatility_analysis import calculate_historical_volatility, get_current_volatility

def run():
    data_path = "data/raw/daily_bars.csv"
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    print(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    ticker = "AAPL"
    window = 20
    
    print(f"\n{'='*60}")
    print(f"Historical Volatility Analysis for {ticker}")
    print(f"{'='*60}\n")
    
    current = get_current_volatility(df, ticker, window)
    
    if "error" in current:
        print(current["error"])
        return
    
    print(f"Current {window}-day Historical Volatility: {current['current_volatility']}%")
    print(f"As of: {current['date']}")
    print(f"Assessment: {current['interpretation']}\n")
    
    print(f"Recent Volatility Trend (Last 10 Days):")
    print("-" * 60)
    
    result = calculate_historical_volatility(df, ticker, window)
    
    if not result.empty:
        display_cols = ['timestamp', 'close', 'daily_return', f'volatility_{window}d']
        recent = result[display_cols].tail(10)
        
        pd.options.display.float_format = '{:.2f}'.format
        print(recent.to_string(index=False))
        print("\nNote: Volatility is annualized (% per year)")
    else:
        print("Analysis failed or returned no data.")

if __name__ == "__main__":
    run()
