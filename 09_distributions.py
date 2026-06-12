import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

# Simulate 1000 daily returns (normal distribution)
mean = 0.001       # average daily return 0.1%
std = 0.02         # daily volatility 2%
returns = np.random.normal(mean, std, 1000)

# Plot the distribution 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left chart - histogram of returns 
ax1.hist(returns, bins=50, color="blue", edgecolor="black")
ax1.set_title("Distribution of daily returns")
ax1.set_xlabel("Return")
ax1.set_ylabel("Frequency")

# Right chart - normal curve
x = np.linspace(-0.08, 0.08, 100)
ax2.plot(x, stats.norm.pdf(x, mean, std), color="blue")
ax2.set_title("Normal Distribution Curve")
ax2.set_xlabel("Return")
ax2.set_ylabel("Probability")

plt.tight_layout()
plt.show()