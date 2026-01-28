import pandas as pd


data = pd.read_csv("data/raw/daily_bars.csv")

def moving_avg_dataframe(dataframe, ticker, MA_int):
    ticker_df = (
        dataframe[dataframe['symbol'] == ticker]
        .sort_values("timestamp", ascending=True)
    )

    ticker_df[f"ma_{MA_int}"] = ticker_df['close'].rolling(window=20).mean()

    return ticker_df

print(moving_avg_dataframe(data, 'AAPL', 20).head(50))