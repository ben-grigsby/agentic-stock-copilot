import pandas as pd
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Functions.analytics import moving_average, percent_price_change, rolling_volatility, rsi

def test_analytics():
    # 1. Load the actual data to test with real-world scenarios
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'daily_bars.csv')
    df = pd.read_csv(data_path)
    
    ticker = 'AAPL'
    window = 5
    
    print(f"Testing Analytics Engine with Ticker: {ticker}, Window: {window}")
    
    try:
        # Test Moving Average
        sma = moving_average(df, ticker, window)
        print(f"SMA (last 5 values):\n{sma.tail()}")
        assert not sma.tail().isnull().any(), "SMA should not have nulls at the end"
        
        # Test Percent Change
        pct = percent_price_change(df, ticker, window)
        print(f"Percent Change (last 5 values):\n{pct.tail()}")
        assert not pct.tail().isnull().any(), "Percent change should not have nulls at the end"
        
        # Test Volatility
        vol = rolling_volatility(df, ticker, window)
        print(f"Rolling Volatility (last 5 values):\n{vol.tail()}")
        assert not vol.tail().isnull().any(), "Volatility should not have nulls at the end"
        
        # Test RSI
        rsi_vals = rsi(df, ticker, 14)
        print(f"RSI (last 5 values):\n{rsi_vals.tail()}")
        assert not rsi_vals.tail().isnull().any(), "RSI should not have nulls at the end"
        
        # Test Validation
        print("Testing validation for non-existent ticker...")
        try:
            moving_average(df, 'INVALID', 5)
            assert False, "Should have raised ValueError for invalid ticker"
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("Testing validation for invalid window...")
        try:
            moving_average(df, 'AAPL', 0)
            assert False, "Should have raised ValueError for window <= 0"
        except ValueError as e:
            print(f"Caught expected error: {e}")
            
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_analytics()
