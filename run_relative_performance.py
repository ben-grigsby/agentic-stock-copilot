# Minho

import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relative_performance_analysis import (calculate_relative_performance)


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
    benchmark = "SPY"
    window = 90

    print(f"\n{'='*60}")
    print(f"Relative Performance Analysis")
    print(f"{ticker} vs {benchmark}")
    print(f"{'='*60}\n")

    result = calculate_relative_performance(
        df,
        ticker,
        benchmark=benchmark,
        window_days=window
    )

    if "error" in result:
        print(result["error"])
        return

    print(f"Window: {window} trading days")
    print(f"As of: {result['as_of']}\n")

    print(f"{ticker} Return: {result['ticker_return'] * 100:.2f}%")
    print(f"{benchmark} Return: {result['benchmark_return'] * 100:.2f}%")
    print(f"Relative Return: {result['relative_return'] * 100:.2f}%")
    print(f"Assessment: {result['interpretation']}")


if __name__ == "__main__":
    run()
