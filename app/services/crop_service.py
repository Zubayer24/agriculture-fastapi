from app.utils.data_loaders import (
    load_harvest_data,
    load_crop_revenue
) 

from app.utils.filters import apply_filters


def get_yield_efficiency(
    crop_category=None,
    region=None
):

    df = load_harvest_data()

    filters = {
        "crop_category": crop_category,
        "region": region
    }

    df = apply_filters(df, filters)

    grouped_df = (
        df.groupby(
            ["crop_name", "crop_category"],
            as_index=False
        )
        .agg(
            avg_yield_per_hectare=(
                "yield_per_hectare",
                "mean"
            ),

            total_area_ha=(
                "area_planted_ha",
                "sum"
            )
        )
    )

    return grouped_df


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