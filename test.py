import pandas as pd

df = pd.read_parquet(
    "products_20260606.parquet"
)

print(df.columns)

print(df.head())