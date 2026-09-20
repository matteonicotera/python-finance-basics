import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Download real data for Eli Lilly
data = yf.download("LLY", period="2y")["Close"]
data = pd.DataFrame(data)
data.columns = ["Close"]

# Calculate moving averages
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

# Generate signals — only at crossover points
data["Signal"] = 0
data.loc[data["MA20"] > data["MA50"], "Signal"] = 1
data.loc[data["MA20"] < data["MA50"], "Signal"] = -1
data["Position"] = data["Signal"].diff()

# Buy and sell crossover points only
buy_signals = data[data["Position"] == 2]
sell_signals = data[data["Position"] == -2]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Eli Lilly Price", color="blue", alpha=0.7)
plt.plot(data["MA20"], label="MA 20 days", color="orange")
plt.plot(data["MA50"], label="MA 50 days", color="red")
plt.scatter(buy_signals.index, buy_signals["Close"],marker="^", color="green", s=200, label="Buy signal", zorder=5)
plt.scatter(sell_signals.index, sell_signals["Close"],marker="v", color="red", s=200, label="Sell signal", zorder=5)
plt.title("Eli Lilly — Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.show()
plt.close()

# Calculate strategy performance
data["Daily_Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Signal"].shift(1) * data["Daily_Return"]

total_strategy = (1 + data["Strategy_Return"].dropna()).prod() - 1
total_buyhold = (1 + data["Daily_Return"].dropna()).prod() - 1

print("Strategy Performance vs Buy & Hold")
print("-" * 40)
print(f"Strategy return:   {round(total_strategy * 100, 2)}%")
print(f"Buy & Hold return: {round(total_buyhold * 100, 2)}%")

# Plot cumulative returns 
cumulative_strategy = (1 + data["Strategy_Return"].dropna()).cumprod()
cumulative_buyhold= (1 + data["Daily_Return"].dropna()).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(cumulative_strategy, label="MA Crossover Strategy", color="orange")
plt.plot(cumulative_buyhold, label="Buy & Hold", color="blue")
plt.title("Strategy vs Buy & Hold / Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Portfolio Growth ($1 invested)")
plt.legend()
plt.show()
plt.close()
