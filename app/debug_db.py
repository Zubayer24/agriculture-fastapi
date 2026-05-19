import pandas as pd
from app.database import engine

# Check distinct season values
season_df = pd.read_sql(
    "SELECT DISTINCT season FROM vw_harvest_full",
    engine
)

print("SEASON VALUES:")
print(season_df)


pd.set_option("display.max_columns", None)
growing_df = pd.read_sql(
    "SELECT * FROM vw_harvest_full",
    engine
)

print("\nGROWING SEASON VALUES:")
print(growing_df.columns)


