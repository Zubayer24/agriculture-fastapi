from app.utils.data_loaders import (
    load_harvest_data,
    load_crop_revenue
) 

from app.utils.filters import apply_filters
from app.utils.constants import water_requirement_map, benchmark_yield

import pandas as pd

def get_yield_efficiency(
    df: pd.DataFrame,
    crop_category=None,
    season=None,
    year=None,
    region=None,
    water_requirement=None
):

    filters = {
        "crop_category": crop_category,
        "season": season,
        "year": year,
        "region": region
    }

    # reusable centralized filtering
    df = apply_filters(df, filters)

    grouped = df.groupby(
        ["crop_name", "crop_category", "season"],
        as_index=False
    ).agg(
        total_area_planted_ha=("area_planted_ha", "sum"),
        total_yield=("quantity_harvested_ton", "sum")
    )

    grouped["actual_avg_yield_ton_per_ha"] = (
        grouped["total_yield"] / grouped["total_area_planted_ha"]
    ).round(1)

    grouped["avg_yield_benchmark_ton_per_ha"] = (
        grouped["crop_name"].map(benchmark_yield)
    )

    grouped["efficiency_pct"] = (
        grouped["actual_avg_yield_ton_per_ha"] /
        grouped["avg_yield_benchmark_ton_per_ha"]
    ) * 100

    grouped["efficiency_pct"] = (
        grouped["efficiency_pct"].round(1)
    )

    grouped["water_requirement"] = (
        grouped["crop_name"].map(water_requirement_map)
    )

    # water requirement filter
    if water_requirement is not None:

        grouped = grouped[
            grouped["water_requirement"]
            .astype(str)
            .str.lower() == water_requirement.strip().lower()
        ]

    return grouped 


def get_crop_trend(
    df: pd.DataFrame,
    crop_name=None,
    crop_category=None,
    year=None,
    quarter=None,
    market_type=None
):

    filters = {
        "crop_name": crop_name,
        "crop_category": crop_category,
        "year": year,
        "quarter": quarter,
        "market_type": market_type
    }

    df = apply_filters(df, filters)

    grouped = (
        df.groupby(
            ["crop_name", "year", "quarter", "season"],
            as_index=False
        )
        .agg(
            total_quantity_sold_ton=(
                "quantity_harvested_ton",
                "sum"
            ),

            total_revenue_bdt=(
                "revenue_bdt",
                "sum"
            ),

            avg_price_per_ton_bdt=(
                "price_per_ton_bdt",
                "mean"
            ),

            num_harvests=(
                "harvest_id",
                "count"
            )
        )
    )

    grouped["total_quantity_sold_ton"] = (
        grouped["total_quantity_sold_ton"].round(1)
    )

    grouped["total_revenue_bdt"] = (
        grouped["total_revenue_bdt"].round(1)
    )

    grouped["avg_price_per_ton_bdt"] = (
        grouped["avg_price_per_ton_bdt"].round(1)
    )

    return grouped


def get_quality_breakdown(
    crop_category=None
):

    df = load_harvest_data()

    filters = {
        "crop_category": crop_category
    }

    df = apply_filters(df, filters)

    grouped_df = (
        df.groupby(
            ["crop_name", "quality_grade"],
            as_index=False
        )
        .agg(
            total_quantity=("quantity_harvested_ton", "sum")
        )
    )

    return grouped_df