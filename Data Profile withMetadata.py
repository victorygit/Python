import pandas as pd
import numpy as np
import pyodbc
import os
from sqlalchemy import create_engine
import urllib


metadata_file_path = "c:/supply chain/ASODS Table Fields.csv"
df_meta_data = pd.read_csv(metadata_file_path)
#print(df_meta_data)

file_path = "c:/supply chain/summary_output.csv"

def spark_like_summary(df):
    stats = []
    for col in df.columns:
        s = df[col]
        is_numeric = pd.api.types.is_numeric_dtype(s)

        stats.append({
            "column": col,
            "count": s.count(),
            "mean": s.mean() if is_numeric else None,
            "stddev": s.std() if is_numeric else None,
            "min": s.min(),
            "25%": s.quantile(0.25) if is_numeric else None,
            "50%": s.quantile(0.50) if is_numeric else None,
            "75%": s.quantile(0.75) if is_numeric else None,
            "max": s.max(),
            "null_count": s.isna().sum(),
            "distinct_count": s.nunique(),
        })
        stats
    return pd.DataFrame(stats)

# --- SQL Server connection ---
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=ODS;"
    "Database=ORSUSR;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

Table_list = [
    "ORSUSR.FISCAL_CLDR",
    "ORSUSR.TIDFCMST"
#    "ORSUSR.TIDTRACE"
]
count = 0
for table in Table_list:
    count = count + 1
# Load table into DataFrame
    sql_str = "SELECT * FROM " +table
    print(sql_str)
    df = pd.read_sql(sql_str, engine)
    # Show summary
    summary_df = spark_like_summary(df)
    summary_df.insert(0, "table_name", table.split(".")[1]
)    
    summary_df = summary_df.merge(
    df_meta_data,
    left_on=["table_name", "column"],
    right_on=["TABLE_NAME", "COLUMN_NAME"],
    how="inner")
    summary_df = summary_df.drop(columns=["TABLE_NAME", "COLUMN_NAME","IS_NULLABLE"])

    # print(summary_df)
    # Write or append to CSV
    if not os.path.exists(file_path) or count == 1:
        summary_df.to_csv(file_path, index=False)
    else:
        summary_df.to_csv(file_path, mode="a", header=False, index=False)

