import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
daily_bars = pd.read_csv("data/raw/daily_bars.csv")

daily_bars.columns          # observing the columns in the dataframe
daily_bars["symbol"].unique()   # observing the unique stock symbols in the dataframe

# Cleaning up the timestamp column to only have date information
daily_bars["timestamp"] = pd.to_datetime(daily_bars["timestamp"]).dt.date

tidy_bars = daily_bars.drop(columns = "timestamp")
tidy_bars

def add_returns(df, column='close'):
    # Group by symbol so the calculation resets for each asset
    # then apply pct_change to the specified column
    df['pct_change'] = df.groupby('symbol')[column].pct_change() * 100  # Convert to percentage
    
    # Optional: fill the first row of each symbol (NaN) with 0
    df['pct_change'] = df['pct_change'].fillna(0)
    
    return df
