from app.utils.data_loaders import load_harvest_data
from app.utils.filters import apply_filters


def get_market_comparison(
    market_type=None,
    crop_category=None,
    year=None
):

    df = load_harvest_data()

    filters = {
        "market_type": market_type,
        "crop_category": crop_category,
        "year": year
    }

    df = apply_filters(df, filters)

    grouped_df = (
        df.groupby(
            [
                "market_name",
                "market_type",
                "crop_name"
            ],
            as_index=False
        )
        .agg(
            avg_price_per_ton_bdt=(
                "price_per_ton_bdt",
                "mean"
            ),

            total_revenue_bdt=(
                "revenue_bdt",
                "sum"
            )
        )
    )

    return grouped_df