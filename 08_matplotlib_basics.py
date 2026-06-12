import matplotlib.pyplot as plt
import numpy as np

# Data 
assets = ["Eli Lilly", "TSMC", "Schneider Electric"]
returns = [0.59, 0.89, 0.22]
volatility = [0.28, 0.32, 0.18]

# Create one figure with 2 charts side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# First chart - Returns
ax1.bar(assets, returns, color=["blue", "green", "orange"])
ax1.set_title("Annual Returns 2024")
ax1.set_xlabel("Asset")
ax1.set_ylabel("Return(%)")

# Second chart - Volatility
ax2.bar(assets, volatility, color=["blue", "green", "orange"])
ax2.set_title("Volatility 2024")
ax2.set_xlabel("Asset")
ax2.set_ylabel("Volatility(%)")

plt.tight_layout() 
plt.show()