import pandas as pd 
import numpy as np

# Create a simple DataFrame (like an Excel table)
data = {
    "asset": ["Eli Lilly", "TSMC", "schneider Electric"],
    "price": [800, 180, 230], 
    "return": [0.59, 0.89, 0.22],
    "volatility": [0.28, 0.32, 0.18]}

df = pd.DataFrame(data)

print(df)
print()
print("Average return:", round(df["return"].mean()* 100, 2), "%")
print("Most volatile asset:", df.loc[df["volatility"].idxmax(), "asset"])
