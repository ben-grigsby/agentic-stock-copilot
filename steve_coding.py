import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
daily_bars = pd.read_csv("data/raw/daily_bars.csv")

daily_bars.columns          # observing the columns in the dataframe
daily_bars["symbol"].unique()   # observing the unique stock symbols in the dataframe

# Cleaning up the timestamp column to only have date information
daily_bars["timestamp"] = pd.to_datetime(daily_bars["timestamp"]).dt.date

# Add a new column for percentage change in closing price.
def add_returns(df, column='close'):
    # Avoid modifying the original dataframe
    df = df.copy()  

    # Group by symbol so the calculation resets for each asset
    # then apply pct_change to the specified column
    df['pct_change'] = df.groupby('symbol')[column].pct_change() * 100  # Convert to percentage
    
    # Optional: fill the first row of each symbol (NaN) with 0
    df['pct_change'] = df['pct_change'].fillna(0)
    
    return df

# Create a new dataframe with the largest either positive or negative percentage change for each stock.
# df = dataframe, indicator = '+' (for largest positive) or '-' (for the largest negative), symbol = stock symbol, n = number of rows to show
def largest_pct_change(df, indicator, symbol, n):
    # Avoid modifying the original dataframe
    df = df.copy()  

    # Cleaning up the timestamp column to only have date
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.date
    # Filter the dataframe for the specified symbols
    df = df[df['symbol'] == symbol]
    df['pct_change'] = df.groupby('symbol')['close'].pct_change() * 100  # Ensure pct_change is calculated

    # Fill the first row with 0
    df['pct_change'] = df['pct_change'].fillna(0)

    # Select the relevant columns
    df = df[['symbol', 'timestamp', 'pct_change']]

    # Indicator can be either '+' or '-'. (input by the user) This shows the largest positive or negative percentage change for each stock.
    if indicator == '+':
        df = df.sort_values(by='pct_change', ascending=False)  # Sort in descending order
    elif indicator == '-':
        df = df.sort_values(by='pct_change', ascending=True)    # Sort in ascending order

    return df.head(n)   # only shows the first n rows of the dataframe.

# Find the correlation between two stocks. Measures the linear association, not causation.
def calculate_correlation(df, symbol1, symbol2):
    # Filter the dataframe for the two symbols
    df1 = df[df['symbol'] == symbol1]
    df2 = df[df['symbol'] == symbol2]
    
    # Merge on timestamp to align the data
    merged = pd.merge(df1, df2, on='timestamp', suffixes=('_' + symbol1, '_' + symbol2))
    
    # Calculate the correlation between the percentage changes of the two stocks
    correlation = merged['pct_change_' + symbol1].corr(merged['pct_change_' + symbol2])
    
    return correlation