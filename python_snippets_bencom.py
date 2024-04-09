# Python Snippets
# print table to share in slack
from tabulate import tabulate
print(tabulate(df_uns_stats, tablefmt="grid", headers=df_uns_stats.columns))

# Connect to view from pacific
query = """
(select * from [Sales].[PW_Daily_Overview_Report_v]) as result
"""

df = spark.read.jdbc(url=jdbcUrl, table=query, properties=conn_Prop).toPandas()

import pandas as pd
def glimpse(df):
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    for col in df.columns:
        print(f"$ {col} <{df[col].dtype}> {df[col].head(1).values}")

import pandas as pd
def glimpse_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Similar to R's glimpse()

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    sample_size = min(df.shape[0], 3)

    return (
        df.sample(sample_size)
        .T.assign(dtypes=df.dtypes)
        .loc[
            :, lambda x: sorted(x.columns, key=lambda col: 0 if col == "dtypes" else 1)
        ]
    )