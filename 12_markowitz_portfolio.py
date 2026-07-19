import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Download 2 years of real historical data
tickers = ["LLY", "TSM", "SU.PA"]
data = yf.download(tickers, period="2y")["Close"]

print(data.head())
print()
print("Number of trading days downloaded:", len(data))

# Remove rows with mising values
data= data.dropna()

# Calculate daily returns (percentage change)
returns = data.pct_change() .dropna()

print(returns.head())
print()
print("Annualized average returns:")
print(returns.mean() * 252)
print()
print("Annualized volatility:")
print(returns.std() * np.sqrt(252))

# Covariance matrix (annualized)
cov_matrix = returns.cov() * 252

print("Covariance matrix:")
print(cov_matrix)
correlation_matrix = returns.corr()
print("Correlation matrix")
print(correlation_matrix)

# Simulate 10 000 random portfolios 
n_portfolios = 10000
portfolio_returns = []
portfolio_volatilities = []
portfolio_weights = []

for i in range(n_portfolios): 
    # Generate random weights that sum to 1
    weights = np.random.random(3)
    weights = weights / np.sum(weights)

    # Portfolio return 
    port_return = np.sum(weights * returns.mean() * 252)

    # Portfolio volatility 
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    portfolio_returns.append(port_return)
    portfolio_volatilities.append(port_volatility)
    portfolio_weights.append(weights)

print("Simulation done")
print("Best return found :", round(max(portfolio_returns) * 100, 2), "%")
print("Lowest volatility found : ", round(min(portfolio_returns) * 100, 2), "%")

# Find the best portfolio (highest Sharpe ratio)
sharpe_ratios = [(r - 0.05) / v for r , v in zip(portfolio_returns, portfolio_volatilities)]
best_idx = sharpe_ratios.index(max(sharpe_ratios))
best_weights = portfolio_weights[best_idx]

print("Optimal portfolio (best Sharpe ratio)")
print("Eli Lilly:          ", round(best_weights[0] * 100, 2), "%")
print("TSMC:               ", round(best_weights[1] * 100, 2), "%")
print("Schneider Electric: ", round(best_weights[2] * 100, 2), "%")
print("Expected return:    ", round(portfolio_returns[best_idx] * 100, 2), "%")
print("Volatility:         ", round(portfolio_volatilities[best_idx] * 100, 2), "%")
print("Sharpe ratio:       ", round(max(sharpe_ratios), 2))

# Plot efficient frontier 
plt.figure(figsize=(10, 6))
scatter = plt.scatter(portfolio_volatilities, portfolio_returns, c=sharpe_ratios, cmap="viridis", alpha = 0.5)
plt.colorbar(scatter, label="Sharpe Ratio")

# Hightlight the optimal portfolio
plt.scatter(portfolio_volatilities[best_idx], portfolio_returns[best_idx], color="red", marker="*", s=300, label= "Optimal portfolio")

plt.xlabel("Volatility (Risk)")
plt.ylabel("Annual Return")
plt.title("Markowitz Efficient Frontier - LLY, TSM, SU.PA")
plt.legend()
plt.show()