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

# Extreme days
print()
print("5 worst days (P&L in $):")
print(daily_pnl.nsmallest(5))
print()
print("5 best days (P&L in $):")
print(daily_pnl.nlargest(5))

tail = daily_pnl[daily_pnl <= -var_95]
print()
print("Days in the tail:", len(tail))
print("Share of tail loss from the 3 worst days:",
round(float(tail.nsmallest(3).sum() / tail.sum()) * 100, 1), "%")

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


# Conclusion
# Period: November 2024 to October 2026, $100,000 invested in Eli Lilly.
# The 1-day 95% VaR is about $3,270 and the CVaR is about $5,270.
# This means that on about 1 day out of 20, the loss was above $3,270,
# and on those days the average loss was about $5,270.
#
# The CVaR/VaR ratio is 1.61, while it would be 1.25 for a normal distribution.
# On the histogram, I can see extreme values, both losses and gains, far from
# the CVaR. The worst day (2025-08-07) lost about $14,100, which is 14% of the
# portfolio, and the best day (2025-04-17) gained about $14,300.
# The 3 worst days represent about 25% of the total loss of the 25 days in the
# tail. This explains the high ratio: the CVaR is an average, so a few very
# large losses push it up a lot. The VaR is only a threshold (a percentile),
# so it does not depend on how large the extreme losses are.
# The extreme days also increase the volatility, which is consistent with the
# normal approximation of the VaR ($3,970) being above the historical VaR.
#
# Limitations: the historical method only sees the 500 days of the sample, so
# a day worse than the worst one in the data cannot appear. This is also a
# single stock with a 1-day horizon, and the results depend on the chosen dates.