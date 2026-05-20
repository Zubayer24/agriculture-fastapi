import pandas as pd
from app.utils.data_loaders import load_harvest_data
from app.utils.filters import apply_filters


def get_market_price_comparison(
    market_type=None,
    crop_category=None,
    year=None,
    season=None,
    price_tier=None,
    district=None
):

    df = load_harvest_data()

    # standardize district naming (important cleanup)
    df["farm_district"] = df["farm_district"].replace({
        "Jessore": "Jashore"
    })

    filters = {
        "market_type": market_type,
        "crop_category": crop_category,
        "year": year,
        "season": season,
        "price_tier": price_tier,
        "farm_district": district
    }

    df = apply_filters(df, filters)

    comparison_df = (
        df.groupby(
            [
                "market_name",
                "market_type",
                "price_tier",
                "farm_district",
                "crop_name"
            ],
            as_index=False
        )
        .agg(
            avg_price_per_ton_bdt=("price_per_ton_bdt", "mean"),
            total_quantity_sold_ton=("quantity_sold_ton", "sum"),
            total_revenue_bdt=("revenue_bdt", "sum")
        )
    )

    # rounding for clean API output
    comparison_df["avg_price_per_ton_bdt"] = comparison_df["avg_price_per_ton_bdt"].round(1)
    comparison_df["total_quantity_sold_ton"] = comparison_df["total_quantity_sold_ton"].round(1)
    comparison_df["total_revenue_bdt"] = comparison_df["total_revenue_bdt"].round(1)

    # rename for API contract
    comparison_df = comparison_df.rename(
        columns={"farm_district": "district"}
    )

    return comparison_df