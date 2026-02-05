# Minho

import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsi_analysis import calculate_rsi, get_current_rsi


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
    window = 14
    
    print(f"\n{'='*60}")
    print(f"RSI Analysis for {ticker}")
    print(f"{'='*60}\n")
    
    current = get_current_rsi(df, ticker, window)
    
    if "error" in current:
        print(current["error"])
        return

    print(f"Current {window}-day RSI: {current.get('current_rsi', current.get('rsi'))}")
    print(f"As of: {current.get('date', 'N/A')}")
    print(f"Assessment: {current['interpretation']}\n")
    
    print(f"Recent RSI (Last 10 Days):")
    print("-" * 60)
    
    result = calculate_rsi(df, ticker, window)
    
    if not result.empty:
        display_cols = ['timestamp', 'close', f'rsi_{window}d']
        recent = result[display_cols].tail(10)
        
        pd.options.display.float_format = '{:.2f}'.format
        print(recent.to_string(index=False))
    else:
        print("Analysis failed or returned no data.")

if __name__ == "__main__":
    run()
