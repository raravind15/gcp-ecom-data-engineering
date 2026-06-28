import pandas as pd

df = pd.read_csv(f"C:\Emp\GCP_LEARNING\pROJECT\data\orders.csv")

print(df.dtypes)

df.to_parquet(
    "orders_20260606.parquet",
    index=False,
    engine="pyarrow"
)

print("Parquet created successfully")