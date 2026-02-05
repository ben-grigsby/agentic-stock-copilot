from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta

from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

load_dotenv()

### FILLER FOR RN, DONT NEED TO RUN

client = StockHistoricalDataClient(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
)

symbols = ["AAPL", "MSFT", "NVDA", "SPY"]

end = datetime.utcnow()
start = end - timedelta(days=365 * 2)

request = StockBarsRequest(
    symbol_or_symbols=symbols,
    timeframe=TimeFrame.Day,
    start=start,
    end=end,
    feed="iex"
)

bars = client.get_stock_bars(request)

# Convert to DataFrame
df = bars.df.reset_index()

# Save locally
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/daily_bars.csv", index=False)

print("Saved data/raw/daily_bars.csv")