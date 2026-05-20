import pandas as pd
from app.database import engine

# Check distinct season values
season_df = pd.read_sql(
    "SELECT DISTINCT farm_district FROM vw_harvest_full",
    engine
)

print("SEASON VALUES:")
print(season_df)


pd.set_option("display.max_columns", None)
growing_df = pd.read_sql(
    "SELECT * FROM vw_revenue_by_crop_year",
    engine
)



print(growing_df.columns)
