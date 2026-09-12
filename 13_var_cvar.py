import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download real data for Eli Lilly
data = yf.download("LLY", period="2y")["Close"]
returns = data.pct_change().dropna()

# Portfolio value
portfolio_value = 100000 # $100,000 invested

# Calculate daily returns in dollars 
daily_pnl = returns*portfolio_value

# VaR at 95% confidence level
confidence_level = 0.95
var_95 = np.percentile(daily_pnl, 1 - confidence_level)*(-1)

# CVaR : average loss beyond VaR
cvar_95 = float(daily_pnl[daily_pnl < -var_95].mean())*(-1)

print("Portfolio Value: $100,000 invested in Eli Lilly")
print("-"*45)
print(f"VaR  (95%): ${round(var_95, 2)}")
print(f"CVaR  (95%): ${round(cvar_95, 2)}")

# Plot distribution of daily P&L with VaR and CVaR
plt.figure(figsize=(10,6))
plt.hist(daily_pnl, bins=50, color="blue", edgecolor="black", alpha=0.7)
plt.axvline(x=-var_95, color="red", linestyle="--", label=f"VaR 95%: ${round(var_95, 0)}")
plt.axvline(x=-cvar_95, color="orange", linestyle="--", label=f"CVaR 95%: ${round(cvar_95, 0)}")
plt.title("Eli Lilly : Daily P&L Distribution with VaR and CVaR")
plt.xlabel("Daily P&L ($)")
plt.ylabel("Frequency")
plt.legend()
plt.show()