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

    for col, val in filters.items():
        if val is not None and col in df.columns:
            df = df[df[col] == val]


    grouped = df.groupby(
        ["crop_name", "crop_category", "season"],
        as_index=False
    ).agg(
        total_area_planted_ha=("area_planted_ha", "sum"),
        total_yield=("quantity_harvested_ton", "sum")
    )


    grouped["actual_avg_yield_ton_per_ha"] = (
        grouped["total_yield"] / grouped["total_area_planted_ha"]
    )

    grouped["avg_yield_benchmark_ton_per_ha"] = grouped["crop_name"].map(benchmark_yield)

    grouped["efficiency_pct"] = (
        grouped["actual_avg_yield_ton_per_ha"] /
        grouped["avg_yield_benchmark_ton_per_ha"]
    ) * 100


    grouped["water_requirement"] = grouped["crop_name"].map(water_requirement_map)

    if water_requirement is not None:
        grouped = grouped[grouped["water_requirement"] == water_requirement]

    return grouped


def get_crop_trend(
    crop_category=None,
    year=None
):

    df = load_crop_revenue()

    filters = {
        "crop_category": crop_category,
        "year": year
    }

    df = apply_filters(df, filters)

    return df


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