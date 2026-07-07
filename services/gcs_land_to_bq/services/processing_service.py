from datetime import datetime,timezone
from decimal import Decimal
import pandas as pd

def add_audit_columns(df, file_name):

    df["source_file_name"] = file_name

    df["load_timestamp"] = datetime.now()

    return df

def process_dataframe(df, file_name):
    df = add_audit_columns(
        df,
        file_name
        )

    if "order_date" in df.columns:

            df["order_date"] = pd.to_datetime(
                df["order_date"],
                format="%d-%m-%y"
            ).dt.date

    if "last_updated_date" in df.columns:

            df["last_updated_date"] = pd.to_datetime(
                df["last_updated_date"],
                format="%d-%m-%y"
            ).dt.date


    numeric_columns = [
            "unit_price",
            "order_amount"
        ]

    for col in numeric_columns:

            if col in df.columns:

                df[col] = df[col].apply(
                    lambda x: Decimal(str(x))
                )
    
    return df