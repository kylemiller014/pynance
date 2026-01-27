# Import libraries
import yfinance as yf
import pandas as pd
import seaborn as sns
import numpy as np
from pandas_datareader import data as pdr
import datetime as dt

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365*5)  # Last 5

# Stocks we care about
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Download stock data
df = yf.download(stocks, start=startDate, end=endDate)

# Look at adjusted prices only
adj_close_prices = df['Adj Close ]']

# Calculate daily returns
daily_returns = np.log(adj_close_prices / adj_close_prices.shift(1))

# Calculate cumulative returns
cumulative_returns = daily_returns.cumsum()

# Plot cumulative returns
cumulative_returns.plot(figsize=(14, 7), title='Cumulative Log Returns of Selected Stocks Over Last 5 Years')