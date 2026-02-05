import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/daily_bars.csv")

def dataset_overview(df):
    print(df.head())
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns)
    print("\nMissing Values:")
    print(df.isna().sum())
    print("\nData Types:")
    print(df.dtypes)

dataset_overview(df)

def price_graph(df, symbol):
    symbol_df = df[df["symbol"] == symbol]
    date = pd.to_datetime(symbol_df["timestamp"])
    plt.figure(figsize=(10, 6)) 
    plt.plot(date, symbol_df["high"], label="Daily High", color="green") 
    plt.plot(date, symbol_df["low"], label="Daily Low", color="red") 
    plt.plot(date, symbol_df["vwap"], label= "Daily Volume Weighted Average Price", color="purple") 
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{symbol} Prices Time Plot')
    plt.show()

price_graph(df, "AAPL")
