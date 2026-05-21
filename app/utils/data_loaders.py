import pandas as pd
from app.database import engine


def load_harvest_data():

    query = "SELECT * FROM vw_harvest_full"

    df = pd.read_sql(query, engine)

    df["full_date"] = pd.to_datetime(df["full_date"])

    df["loss_pct"] = (
        df["quantity_lost_ton"]
        / df["quantity_harvested_ton"]
    ) * 100

    df["yield_per_hectare"] = (
        df["quantity_harvested_ton"]
        / df["area_planted_ha"]
    )

    return df


def load_farm_profitability():

    query = "SELECT * FROM vw_farm_profitability"

    return pd.read_sql(query, engine)


def load_crop_revenue():

    query = "SELECT * FROM vw_revenue_by_crop_year"

    return pd.read_sql(query, engine)


def load_farm_by_id(farm_id: int):

    query = f"""
        SELECT *
        FROM dim_farm
        WHERE farm_id = {farm_id}
    """

    return pd.read_sql(query, engine)

def load_crop_dimension():

    return pd.read_sql(
        "SELECT * FROM dim_crop",
        engine
    )