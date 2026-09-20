import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf

# Download real data for Eli Lilly 
data = yf.download("LLY", period="2y")["Close"]
data= pd.DataFrame(data)
data.columns = ["Close"]

# Calculate movinf averages 
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

# Generate signals
data["Signal"]= 0
data.loc[data["MA20"] > data["MA50"], "Signal"] = 1  # Buy
data.loc[data["MA20"] < data["MA50"], "Signal"] = -1  # Sell

# Plot price and moving averages
plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Eli Lilly Price", color="blue", alpha=0.7)
plt.plot(data["MA20"], label="MA 20 days", color="orange")
plt.plot(data["MA50"], label="MA 50 days", color="red")
plt.title("Eli Lilly - Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.show()

# Plot buy and sell signals 
buy_signals = data[data["Signal"] == 1]
sell_signals = data[data["Signal"] == -1]

plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Eli Lilly Price", color="blue", alpha=0.7)
plt.plot(data["MA20"], label="MA 20 days", color="orange")
plt.plot(data["MA50"], label="MA 50 days", color="red")
plt.scatter(buy_signals.index, buy_signals["Close"], marker="^", color="green", s=100, label="Buy signal")
plt.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red", s=100, label="Sell signal")
plt.title("Eli Lilly - Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.show()

# Calculate strategy performance
data["Daily_Return"] = data["Close"].pct_change()
data["Startegy_Return"] = data["Signal"].shift(1) * data["Daily_Return"]

total_strategy = (1 + data["Strategy_Return"].dropna()).prod() - 1
total_buyhold = (1 + data["Daily_Return"].dropna()).prod() - 1

print("Startegy Performance vs Buy & Hold")
print("-"*40)
print(f"Startegy return:   {round(total_strategy * 100, 2)}%")
print(f"Buy & Hold return:   {round(total_buyhold * 100, 2)}%")