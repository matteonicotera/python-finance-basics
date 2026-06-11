def calculate_average_return(returns):
    sum_of_returns = sum(returns)
    number_of_returns = len(returns)
    average_return = sum_of_returns / number_of_returns
    return average_return


asset_a_returns = [0.10, -0.04, 0.06, 0.02, -0.01, 0.07]
asset_b_returns = [0.02, 0.03, 0.01, -0.02, 0.04, 0.05]
asset_c_returns = [0.05, 0.04, 0.03, 0.06, -0.02, 0.01]

asset_a_average = calculate_average_return(asset_a_returns)
asset_b_average = calculate_average_return(asset_b_returns)
asset_c_average = calculate_average_return(asset_c_returns)

print("Asset A average return:", round(asset_a_average * 100, 2), "%")
print("Asset B average return:", round(asset_b_average * 100, 2), "%")
print("Asset C average return:", round(asset_c_average * 100, 2), "%")


