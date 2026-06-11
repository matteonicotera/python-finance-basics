import numpy as np

# Create an array of returns 
returns = np.array([0.10, -0.04, 0.06, 0.02, -0.01, 0.07])

# Calculations without loops
print("Average return:", round(np.mean(returns)*100, 2), "%")
print("Volatilty", round(np.std(returns)*100, 2), "%")
print("Max return", round(np.max(returns)*100, 2), "%")
print("Min return", round(np.min(returns)*100, 2), "%")
