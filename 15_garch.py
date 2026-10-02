import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from arch import arch_model

# Download real data for Eli Lilly
data = yf.download("LLy", period="2y")["Close"]
returns = data.pct_change().dropna()*100 # in percentage

print(f"Data downloaded: {len(returns)} daily returns")
print(f"Average return: {round(float(returns.mean().iloc[0]), 4)}%")
print(f"Volatility: {round(float(returns.std().iloc[0]), 4)}%")

# Fit GARCH(1,1) model
model = arch_model(returns, vol="Garch", p=1, q=1)
result = model.fit(disp="off")

print(result.summary())

# Plot conditional volatility
conditional_vol = result.conditional_volatility

plt.figure(figsize=(12, 6))
plt.plot(conditional_vol, color="orange", label="Conditional Volatility (GARCH)")
plt.title("Eli Lilly : Conditional Volatility (GARCH 1,1)")
plt.xlabel("Date")
plt.ylabel("Volatilty (%)")
plt.legend()
plt.show()
plt.close()

# Forecast next 10 days volatility
forecast = result.forecast(horizon=10)
forecast_vol = np.sqrt(forecast.variance.dropna().iloc[-1])

print("Volatility Forecast - next 10 days:")
print("-"*40)
for i, vol in enumerate(forecast_vol):
    print(f"Day {i+1}: {round(vol, 4)}%")

plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), forecast_vol, color="orange", marker="o")
plt.title("Eli Lilly - GARCH Volatility Forecast (next 10 days)")
plt.xlabel("Days ahead")
plt.ylabel("Predicted Volatility (%)")
plt.grid(True, alpha=0.3)
plt.show()
plt.close()