"""
13 - Value at Risk (VaR) and Conditional VaR (CVaR) on Eli Lilly

Method: historical simulation on daily returns.
Assumptions:
  - the position is kept at PORTFOLIO_VALUE every day (daily P&L = return x value)
  - simple daily returns from adjusted closing prices (yfinance default)
  - horizon: 1 day
VaR and CVaR are printed as positive numbers: they are losses in dollars.
"""

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats

# Parameters (fixed dates so results are reproducible) 
TICKER = "LLY"
START = "2024-11-01"
END = "2026-11-01"          # the end date is excluded by yfinance
PORTFOLIO_VALUE = 100000    # $100,000 invested
CONFIDENCE_LEVEL = 0.95


def historical_var(pnl, confidence):
    """Loss exceeded on only (1 - confidence) of the days."""
    # np.percentile expects a number between 0 and 100, hence the factor 100
    return -np.percentile(pnl, 100 * (1 - confidence))


def historical_cvar(pnl, confidence):
    """Average loss on the days where the loss is beyond the VaR."""
    var = historical_var(pnl, confidence)
    return -pnl[pnl <= -var].mean()


# Data and daily P&L
data = yf.download(TICKER, start=START, end=END)["Close"]
returns = data.pct_change().dropna().squeeze()
daily_pnl = returns * PORTFOLIO_VALUE

# VaR and CVaR 
var_95 = historical_var(daily_pnl, CONFIDENCE_LEVEL)
cvar_95 = historical_cvar(daily_pnl, CONFIDENCE_LEVEL)

print(f"Portfolio Value: ${PORTFOLIO_VALUE:,} invested in Eli Lilly")
print("-" * 45)
print(f"VaR  (95%): ${var_95:,.2f}")
print(f"CVaR (95%): ${cvar_95:,.2f}")

# Sanity checks 
sigma = float(returns.std())
mu = float(returns.mean())
z = stats.norm.ppf(CONFIDENCE_LEVEL)

print()
print("Sanity checks")
print("-" * 45)
print(f"Daily volatility:        {sigma * 100:.3f} %")
print(f"Normal approx VaR:       ${z * sigma * PORTFOLIO_VALUE:,.2f}")
param_var = -(mu - z * sigma) * PORTFOLIO_VALUE
print(f"Parametric VaR:          ${param_var:,.2f}")
# This only checks the code: with the historical method, the share is about 5% by construction
share = float((daily_pnl <= -var_95).mean())
print(f"Days beyond VaR:         {share * 100:.2f} %  (about 5% by construction)")
normal_ratio = stats.norm.pdf(z) / (1 - CONFIDENCE_LEVEL) / z
print(f"CVaR/VaR ratio:          {cvar_95 / var_95:.2f}  (normal distribution: {normal_ratio:.2f})")
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
f"{float(tail.nsmallest(3).sum() / tail.sum()) * 100:.1f} %")

# Plot: distribution of daily P&L with VaR, CVaR and a normal curve ---
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, density=True, color="blue", edgecolor="black", alpha=0.7,
         label="Daily P&L")
x = np.linspace(daily_pnl.min(), daily_pnl.max(), 300)
plt.plot(x, stats.norm.pdf(x, daily_pnl.mean(), daily_pnl.std()), color="black",
         label="Normal curve (same mean and volatility)")
plt.axvline(x=-var_95, color="red", linestyle="--", label=f"VaR 95%: ${var_95:,.0f}")
plt.axvline(x=-cvar_95, color="orange", linestyle="--", label=f"CVaR 95%: ${cvar_95:,.0f}")
plt.title("Eli Lilly: Daily P&L Distribution with VaR and CVaR")
plt.xlabel("Daily P&L ($)")
plt.ylabel("Density")
plt.legend()
plt.savefig("13_var_cvar.png", dpi=150, bbox_inches="tight")
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