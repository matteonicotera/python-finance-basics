import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats

# Download real data for Eli Lilly (fixed dates so results are reproducible)
data = yf.download("LLY", start="2024-11-01", end="2026-11-01")["Close"]
returns = data.pct_change().dropna().squeeze()

# Portfolio value
portfolio_value = 100000  # $100,000 invested

# Daily profit and loss in dollars
daily_pnl = returns * portfolio_value

# VaR at 95% confidence level (historical method)
confidence_level = 0.95
var_95 = -np.percentile(daily_pnl, 100 * (1 - confidence_level))

# CVaR: average loss on the days beyond the VaR
cvar_95 = -daily_pnl[daily_pnl <= -var_95].mean()

print("Portfolio Value: $100,000 invested in Eli Lilly")
print("-" * 45)
print(f"VaR  (95%): ${round(var_95, 2)}")
print(f"CVaR (95%): ${round(cvar_95, 2)}")

# Sanity checks
sigma = float(returns.std())
mu = float(returns.mean())
z = stats.norm.ppf(confidence_level)

print()
print("Sanity checks")
print("-" * 45)
print(f"Daily volatility:        {round(sigma * 100, 3)} %")
print(f"Normal approx VaR:       ${round(z * sigma * portfolio_value, 2)}")
param_var = -(mu - z * sigma) * portfolio_value
print(f"Parametric VaR:          ${round(param_var, 2)}")
share = float((daily_pnl < -var_95).mean())
print(f"Days beyond VaR:         {round(share * 100, 2)} %  (should be about 5%)")
normal_ratio = stats.norm.pdf(z) / (1 - confidence_level) / z
print(f"CVaR/VaR ratio:          {round(cvar_95 / var_95, 2)}  (normal distribution: {round(normal_ratio, 2)})")
print("CVaR > VaR:", cvar_95 > var_95)

# Plot distribution of daily P&L with VaR and CVaR
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, color="blue", edgecolor="black", alpha=0.7)
plt.axvline(x=-var_95, color="red", linestyle="--", label=f"VaR 95%: ${round(var_95, 0)}")
plt.axvline(x=-cvar_95, color="orange", linestyle="--", label=f"CVaR 95%: ${round(cvar_95, 0)}")
plt.title("Eli Lilly: Daily P&L Distribution with VaR and CVaR")
plt.xlabel("Daily P&L ($)")
plt.ylabel("Frequency")
plt.legend()
plt.show()