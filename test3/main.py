import pandas as pd

df = pd.read_csv("data/sales_data.csv")

df = df[df["sq__ft"] > 0]

df["price_per_sqft"] = df["price"] / df["sq__ft"]

avg_price_per_sqft = df["price_per_sqft"].mean()

print(f"Average price per sq ft: {avg_price_per_sqft:.2f}")

df_below_avg = df[df["price_per_sqft"] < avg_price_per_sqft]
df_below_avg.to_csv("sales_below_avg.csv", index=False)

print(f"Filtered CSV saved with {len(df_below_avg)} properties.")
