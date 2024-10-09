import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the stock data from a CSV file
df = pd.read_csv('historical_data.csv')

# Convert the 'Date' column to date format
df['Date'] = pd.to_datetime(df['Date'])

# Sort the data by date
df = df.sort_values('Date')

# Set the number of days for short and long moving averages
short_window = 3  # Short-term average over 3 days
long_window = 5   # Long-term average over 5 days

# Calculate the short-term and long-term moving averages
df['Short_MA'] = df['Close Price'].rolling(window=short_window).mean()
df['Long_MA'] = df['Close Price'].rolling(window=long_window).mean()

# Create signals based on moving averages
df['Signal'] = 0  # Start with no signal
df['Signal'][short_window:] = np.where(df['Short_MA'][short_window:] > df['Long_MA'][short_window:], 1, -1)

# Calculate trading positions (buy=1, sell=-1) by looking at changes in signals
df['Position'] = df['Signal'].diff()

# Plot the stock price, short-term MA, long-term MA, and buy/sell signals
plt.figure(figsize=(12, 6))

# Plot stock price
plt.plot(df['Date'], df['Close Price'], label='Close Price', color='blue')

# Plot short-term and long-term moving averages
plt.plot(df['Date'], df['Short_MA'], label=f'Short MA ({short_window} days)', color='green')
plt.plot(df['Date'], df['Long_MA'], label=f'Long MA ({long_window} days)', color='red')

# Plot buy signals (where position = 1) and sell signals (where position = -1)
plt.plot(df[df['Position'] == 1]['Date'], df[df['Position'] == 1]['Close Price'], '^', markersize=10, color='green', lw=0, label='Buy Signal')
plt.plot(df[df['Position'] == -1]['Date'], df[df['Position'] == -1]['Close Price'], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

# Add titles and labels
plt.title('Moving Average Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()