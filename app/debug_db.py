import pandas as pd
from app.database import engine

# Check distinct season values
season_df = pd.read_sql(
    "SELECT * FROM vw_harvest_full",
    engine
)


print(season_df.columns)


pd.set_option("display.max_columns", None)
growing_df = pd.read_sql(
    "SELECT * FROM vw_harvest_full",
    engine
)


print(growing_df.head(5))

