def calculate_future_value(initial_capital, annual_return, years):
    future_value = initial_capital * (1 + annual_return) ** years
    return future_value


result_1 = calculate_future_value(1000, 0.07, 10)
result_2 = calculate_future_value(5000, 0.05, 20)
result_3 = calculate_future_value(10000, 0.08, 15)
result_4 = calculate_future_value(2000, 0.03, 30)
result_5 = calculate_future_value(15000, 0.06, 25)

print("Investment 1:", round(result_1, 2))
print("Investment 2:", round(result_2, 2))
print("Investment 3:", round(result_3, 2))
print("investment 4:", round(result_4, 2))
print("investment 5:", round(result_5, 2))