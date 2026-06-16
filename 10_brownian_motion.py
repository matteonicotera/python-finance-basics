import numpy as np 
import matplotlib.pyplot as plt 

# Parameters 
S0 = 800      # initial price (Eli Lilly)
mu = 0.59     # annual return
sigma = 0.28  # annual volatility
T = 1         # 1 year 
N = 252       # trading days in a year
dt = T/N      # time step 

# Simulate price path 
prices = [S0]
for i in range (N) : 
     random_shock = np.random.normal(0, 1)
     price = prices[-1] * np.exp((mu-0.5*sigma**2)*dt + sigma*np.sqrt(dt)* random_shock)
     prices.append(price)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(prices, color="blue")
plt.title("Eli Lilly - Simulated Price Path (GBM)")
plt.xlabel("Trading Days")
plt.ylabel("Price ($)")
plt.show()