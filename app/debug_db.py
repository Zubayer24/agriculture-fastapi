import pandas as pd
from app.database import engine

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

farm_name = "Green Valley Farm"
year = 2023

df = pd.read_sql(
    """
    SELECT *
    FROM vw_harvest_full
    WHERE farm_name = %s
    AND year = %s
    """,
    engine,
    params=(farm_name, year)
)

print(df)