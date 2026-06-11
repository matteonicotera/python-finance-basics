returns = [0.10, -0.04, 0.06, 0.02, -0.01, 0.07]

number_of_returns = len(returns)
sum_of_returns = sum(returns)
average_return = sum_of_returns / number_of_returns

print("Returns:", returns)
print("Number of returns:", number_of_returns)
print("Sum of returns:", round(sum_of_returns, 4))
print("Average return:", round(average_return, 4))
print("Average return in percent:", round(average_return * 100, 2), "%")

