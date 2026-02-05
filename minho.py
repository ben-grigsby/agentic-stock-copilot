import pandas as pd
from scripts.analysis.rsi_analysis import get_current_rsi, calculate_rsi
df = pd.read_csv("/Users/minhochoi/agentic-stock-copilot/data/raw/daily_bars.csv")
print(get_current_rsi(df, "AAPL", 14))
print(calculate_rsi(df, "AAPL", 14).tail(5))
