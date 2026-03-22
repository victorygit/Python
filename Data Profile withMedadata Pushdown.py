
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus
import os
from datetime import datetime

class SQLServerProfiler:
    def __init__(
        self,
        server: str,
        database: str,
        trusted_connection: bool = False,
        username: str | None = None,
        password: str | None = None,
        driver: str = "ODBC Driver 17 for SQL Server",
    ):
        """
        Connect to SQL Server via SQLAlchemy (uses pyodbc under the hood but
        exposes a clean, warning-free interface).

        Args:
            server:             Host name or IP, e.g. "localhost" or
                                "myserver\\SQLEXPRESS".
            database:           Target database name.
            trusted_connection: Use Windows / Kerberos auth (no password needed).
            username / password: SQL Server auth credentials (ignored when
                                 trusted_connection=True).
            driver:             ODBC driver name installed on the machine.
                                Common values:
                                  "ODBC Driver 17 for SQL Server"
                                  "ODBC Driver 18 for SQL Server"
        """
        odbc = (
                f"DRIVER={{{driver}}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;"
            )

        # SQLAlchemy connection URL for mssql+pyodbc using a pre-built ODBC string.
        url = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc)}"
        self.engine: Engine = create_engine(url, fast_executemany=True)
        # Verify connectivity eagerly so errors surface at construction time.
        with self.engine.connect():
            pass

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    def _get_columns(self, schema: str, table: str) -> pd.DataFrame:
        """Return column names and data types from INFORMATION_SCHEMA."""
        sql = """
            SELECT
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME   = :table
            ORDER BY ORDINAL_POSITION
        """
        with self.engine.connect() as conn:
            return pd.read_sql(text(sql), conn, params={"schema": schema, "table": table})

    @staticmethod
    def _is_numeric(data_type: str) -> bool:
        numeric_types = {
            "int", "bigint", "smallint", "tinyint",
            "decimal", "numeric", "money", "smallmoney",
            "float", "real",
        }
        return data_type.lower() in numeric_types

    # ------------------------------------------------------------------
    # SQL builder
    # ------------------------------------------------------------------

    def _build_profile_sql(
        self,
        schema: str,
        table: str,
        columns: pd.DataFrame,
    ) -> str:
        """
        Build a single SELECT that computes all metrics server-side.
        Numeric columns get min/max/mean/stddev/variance.
        Non-numeric columns get NULL for those aggregates.
        All columns get null_count, unique_count, and total_rows.
        Percentiles are fetched separately via _build_percentile_sql.
        """
        total_rows_expr = "COUNT_BIG(*)"
        col_exprs = []

        for _, row in columns.iterrows():
            col = row["COLUMN_NAME"]
            dtype = row["DATA_TYPE"]
            charSize = row["CHARACTER_MAXIMUM_LENGTH"]
            numprecision = row["NUMERIC_PRECISION"]
            numscale = row["NUMERIC_SCALE"]
            columdefault = row["COLUMN_DEFAULT"]
            quoted = f"[{col}]"
            is_num = self._is_numeric(dtype)

            # Null count & unique count apply to every column type
            null_count   = f"SUM(CASE WHEN {quoted} IS NULL THEN 1 ELSE 0 END)"
            unique_count = f"COUNT(DISTINCT {quoted})"

            if is_num:
                # CAST to FLOAT to avoid integer overflow on SUM/AVG
                as_float = f"CAST({quoted} AS FLOAT)"
                min_val  = f"MIN({as_float})"
                max_val  = f"MAX({as_float})"
                mean_val = f"AVG({as_float})"
                # SQL Server has no STDDEV; use the variance formula directly.
                # VAR() / VARP() are built-in; STDEV() / STDEVP() also built-in.
                stddev   = f"STDEV({as_float})"
                variance = f"VAR({as_float})"
            else:
                min_val = max_val = mean_val = stddev = variance = "NULL"

            col_exprs.append(
                f"  -- {col} ({dtype})\n"
                f"  '{col}'      AS col_name_{col},\n"
                f"  '{dtype}'    AS data_type_{col},\n"
                f"  '{charSize}'    AS char_max_Size_{col},\n"
                f"  '{numprecision}'    AS number_precision_{col},\n"
                f"  '{numscale}'    AS number_scale_{col},\n"
                f"  '{columdefault}'    AS default_value_{col},\n"
                f"  {null_count}   AS null_count_{col},\n"
                f"  {unique_count} AS unique_count_{col},\n"
                f"  {min_val}      AS min_{col},\n"
                f"  {max_val}      AS max_{col},\n"
                f"  {mean_val}     AS mean_{col},\n"
                f"  {stddev}       AS stddev_{col},\n"
                f"  {variance}     AS variance_{col}"
            )

        all_exprs = ",\n".join(col_exprs)
        sql = (
            f"SELECT\n"
            f"  {total_rows_expr} AS __total_rows__,\n"
            f"{all_exprs}\n"
            f"FROM [{schema}].[{table}] WITH (NOLOCK)"
        )
        return sql

    def _build_percentile_sql(
        self,
        schema: str,
        table: str,
        numeric_cols: list,
        percentiles: list,
    ) -> str:
        """
        Build a server-side percentile query using PERCENTILE_CONT.

        PERCENTILE_CONT is a window function in T-SQL — it cannot be mixed with
        plain GROUP BY aggregates.  The approach here is:

            SELECT TOP 1
                PERCENTILE_CONT(0.20) WITHIN GROUP (ORDER BY CAST([col] AS FLOAT))
                    OVER () AS [p20_col],
                PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY CAST([col] AS FLOAT))
                    OVER () AS [p50_col],
                ...
            FROM [schema].[table] WITH (NOLOCK)

        OVER () means "the whole table as one partition", so every row gets the
        same value.  TOP 1 returns just one row — no data pulled into Python.
        """
        pct_exprs = []
        for col in numeric_cols:
            quoted = f"[{col}]"
            as_float = f"CAST({quoted} AS FLOAT)"
            for pct in percentiles:
                label = f"p{int(pct * 100)}_{col}"
                pct_exprs.append(
                    f"  PERCENTILE_CONT({pct}) WITHIN GROUP (ORDER BY {as_float})"
                    f" OVER () AS [{label}]"
                )

        inner_cols = ",\n".join(pct_exprs)
        sql = (
            f"SELECT TOP 1\n"
            f"{inner_cols}\n"
            f"FROM [{schema}].[{table}] WITH (NOLOCK)"
        )
        return sql

    # ------------------------------------------------------------------
    # Main profile method
    # ------------------------------------------------------------------

    def profile(self, table_ref: str, percentiles: list = None) -> pd.DataFrame:
        """
        Profile a table and return a tidy DataFrame (one row per column).

        Args:
            table_ref:   Fully qualified name, e.g. "dbo.Orders" or just "Orders"
                         (defaults schema to "dbo" if omitted).
            percentiles: List of fractions to compute, e.g. [0.20, 0.50, 0.75].
                         Defaults to [0.20, 0.50, 0.75].  Only applies to numeric
                         columns.  Pass [] to skip percentile computation.

        Returns:
            DataFrame with columns:
                column_name, data_type, total_rows,
                null_count, null_pct, unique_count,
                min, max, mean, stddev, variance,
                p20, p50, p75  (numeric columns only)
        """
        if percentiles is None:
            percentiles = [0.20, 0.50, 0.75]

        # Parse schema.table
        parts = table_ref.strip("[]").split(".")
        if len(parts) == 2:
            schema, table = parts
        else:
            schema, table = "dbo", parts[0]

        print(f"[profiler] Introspecting [{schema}].[{table}] …")
        cols_df = self._get_columns(schema, table)
        if cols_df.empty:
            raise ValueError(
                f"Table [{schema}].[{table}] not found or has no columns."
            )

        print(f"[profiler] Found {len(cols_df)} columns. Building profile query …")
        sql = self._build_profile_sql(schema, table, cols_df)
    
        print("[profiler] Executing aggregate profile query on SQL Server …")
        with self.engine.connect() as conn:
            raw = pd.read_sql(text(sql), conn)

        total_rows = int(raw["__total_rows__"].iloc[0])
        print(f"[profiler] Table has {total_rows:,} rows.")

        if  total_rows == 0:
            records = []
            return pd.DataFrame(records)

        # ------------------------------------------------------------------
        # Percentile query (numeric columns only, server-side)
        # ------------------------------------------------------------------
        numeric_cols = [
            row["COLUMN_NAME"]
            for _, row in cols_df.iterrows()
            if self._is_numeric(row["DATA_TYPE"])
        ]

        pct_raw = None
        if percentiles and numeric_cols:
            pct_sql = self._build_percentile_sql(schema, table, numeric_cols, percentiles)
            print(f"[profiler] Executing percentile query (P{[int(p*100) for p in percentiles]}) …")
            with self.engine.connect() as conn:
                pct_raw = pd.read_sql(text(pct_sql), conn)

        # ------------------------------------------------------------------
        # Assemble one record per column
        # ------------------------------------------------------------------
        records = []
        for _, row in cols_df.iterrows():
            col   = row["COLUMN_NAME"]
            dtype = row["DATA_TYPE"]
            charSize = row["CHARACTER_MAXIMUM_LENGTH"]
            numprecision = row["NUMERIC_PRECISION"]
            numscale = row["NUMERIC_SCALE"]
            columdefault = row["COLUMN_DEFAULT"]
            nc    = raw[f"null_count_{col}"].iloc[0]
            nc    = int(nc) if pd.notna(nc) else 0
            is_num = self._is_numeric(dtype)

            record = {
                "column_name":  col,
                "data_type":    dtype,
                "char_max_size": charSize,
                "number_precision": numprecision,
                "number_scale": numscale,
                "default_value": columdefault,
                "total_rows":   total_rows,
                "null_count":   nc,
                "null_pct":     round(nc / total_rows * 100, 2) if total_rows else None,
                "unique_count": int(raw[f"unique_count_{col}"].iloc[0]),
                "min":          raw[f"min_{col}"].iloc[0],
                "max":          raw[f"max_{col}"].iloc[0],
                "mean":         raw[f"mean_{col}"].iloc[0],
                "stddev":       raw[f"stddev_{col}"].iloc[0],
                "variance":     raw[f"variance_{col}"].iloc[0],
            }

            # Attach percentiles for numeric columns
            for pct in percentiles:
                label = f"p{int(pct * 100)}"
                if is_num and pct_raw is not None:
                    record[label] = pct_raw[f"{label}_{col}"].iloc[0]
                else:
                    record[label] = None

            records.append(record)

        return pd.DataFrame(records)

   
    def close(self):
        """Dispose the SQLAlchemy connection pool."""
        self.engine.dispose()


# ------------------------------------------------------------------
# Example usage
# ------------------------------------------------------------------
if __name__ == "__main__":    
    profiler = SQLServerProfiler(
        server="ODS",          # e.g. "localhost" or "myserver\\SQLEXPRESS"
        database="ORSUSR",
        trusted_connection=True,            # set False and use username/password for SQL auth
        # username="sa",
        # password="your_password",
        driver="ODBC Driver 18 for SQL Server"   # adjust if you have v18
    )

    Table_List_file_path = "c:/supply chain/Table_List.csv"
    df_Table_List = pd.read_csv(Table_List_file_path)
    df_Table_List = df_Table_List[df_Table_List["TABLE_SCHEMA"]=='ORSUSR']
    df_Table_List["Full_Table_Name"] = df_Table_List["TABLE_SCHEMA"] + "." + df_Table_List["table_name"]

    file_path = "c:/supply chain/summary_output_Pushdown.csv"
    count = 0
    Table_list = df_Table_List["Full_Table_Name"]
    for table in  Table_list:
        count = count + 1
        print("---------------------------------")
        print("Table counter is: ", str(count))
        print("---------------------------------")
        print("Data profile is started at " +str(datetime.now()))
        try:
            print("Table " + table + " Data profile is running")
            df_summary = profiler.profile(
                table,                       # change to your table
                percentiles=[0.20, 0.50, 0.75],        # P20, P50, P75 — pass [] to skip
            )
            df_summary.insert(0, "table_name", table.split(".")[1])
            #print(df_summary)
            # Save to CSV
            if not os.path.exists(file_path) or count == 1:
                df_summary.to_csv(file_path, header=True, index=False)
                print('Header')
            else:
                df_summary.to_csv(file_path, mode="a", header=False, index=False)

        finally:
            print(table +' Profile Finished')
            print("Data profile is finished at " + str(datetime.now()))
    
   
    profiler.close()