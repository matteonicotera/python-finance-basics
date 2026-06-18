import numpy as np
from scipy import stats 
import matplotlib.pyplot as plt

# Black-Scholes function 
def black_scholes(S, K, T, r, sigma) : 
    d1 = (np.log(S/K)+ (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    put = K * np.exp(-r*T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)

    return call, put

# Eli Lilly parameters
S = 800   # current price 
K = 850   # strike price 
T = 1     # 1 year 
r = 0.05  # risk-free rate
sigma = 0.28  # volatility

# Calculate prices
call_price, put_price = black_scholes(S, K, T, r, sigma)

print("Eli Lilly Option Pricing - Black-Scholes")
print("---------------------------")
print("Call price: $", round(call_price, 2))
print("Put price: $", round(put_price, 2))

# Visualize how option price changes with strike price
strikes = np.linspace(600, 1000, 50)
call_prices = []
put_prices = []

for k in strikes: 
    c, p = black_scholes(S, k, T, r, sigma)
    call_prices.append(c)
    put_prices.append(p)

plt.figure(figsize=(10, 5))
plt.plot(strikes, call_prices, label="Call price", color="blue")
plt.plot(strikes, put_prices, label="Put price", color="red")
plt.axvline(x=S, color="gray", linestyle="--", label="Current price")
plt.title("Eli Lilly - Option Price vs Strike")
plt.xlabel("Strike price ($)")
plt.ylabel("Option price ($)")
plt.legend()
plt.show()