def calculate_average_return(returns):
    return sum(returns) / len(returns)


def calculate_volatility(returns):
    average_return = calculate_average_return(returns)
    squared_differences = []

    for daily_return in returns:
        difference = daily_return - average_return
        squared_difference = difference ** 2
        squared_differences.append(squared_difference)

    variance = sum(squared_differences) / len(squared_differences)
    volatility = variance ** 0.5
    return volatility


asset_a_returns = [0.10, -0.04, 0.06, 0.02, -0.01, 0.07]
asset_b_returns = [0.02, 0.03, 0.01, -0.02, 0.04, 0.05]
asset_c_returns = [0.05, 0.04, 0.03, 0.06, -0.02, 0.01]

asset_a_average = calculate_average_return(asset_a_returns)
asset_b_average = calculate_average_return(asset_b_returns)
asset_c_average = calculate_average_return(asset_c_returns)

asset_a_volatility = calculate_volatility(asset_a_returns)
asset_b_volatility = calculate_volatility(asset_b_returns)
asset_c_volatility = calculate_volatility(asset_c_returns)

print("Asset A average return:", round(asset_a_average * 100, 2), "%")
print("Asset A volatility:", round(asset_a_volatility * 100, 2), "%")

print("Asset B average return:", round(asset_b_average * 100, 2), "%")
print("Asset B volatility:", round(asset_b_volatility * 100, 2), "%")

print("Asset C average return:", round(asset_c_average * 100, 2), "%")
print("Asset C volatility:", round(asset_c_volatility * 100, 2), "%")

