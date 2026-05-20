from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from app.services.market_service import (
    get_market_price_comparison
)

from app.schemas.market_schema import (
    MarketPriceComparisonResponse
)

from app.utils.validators import (
    validate_filter,
    VALID_MARKET_TYPES,
    VALID_CROP_CATEGORIES,
    VALID_YEARS,
    VALID_SEASONS,
    VALID_PRICE_TIERS,
    VALID_DISTRICTS
)

router = APIRouter()


@router.get(
    "/markets/price-comparison",
    response_model=MarketPriceComparisonResponse
)
def market_price_comparison(

    market_type: str = Query(
        None,
        description="Filter by market type"
    ),

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    ),

    year: int = Query(
        None,
        description="Filter by year"
    ),

    season: str = Query(
        None,
        description="Filter by season"
    ),

    price_tier: str = Query(
        None,
        description="Filter by price tier"
    ),

    district: str = Query(
        None,
        description="Filter by district"
    )
):

    try:

        market_type = validate_filter(
            market_type,
            VALID_MARKET_TYPES,
            "market_type"
        )

        crop_category = validate_filter(
            crop_category,
            VALID_CROP_CATEGORIES,
            "crop_category"
        )

        year = validate_filter(
            year,
            VALID_YEARS,
            "year"
        )

        season = validate_filter(
            season,
            VALID_SEASONS,
            "season"
        )

        price_tier = validate_filter(
            price_tier,
            VALID_PRICE_TIERS,
            "price_tier"
        )

        district = validate_filter(
            district,
            VALID_DISTRICTS,
            "district"
)

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    comparison_df = get_market_price_comparison(
        market_type,
        crop_category,
        year,
        season,
        price_tier,
        district
    )

    filters_applied = {}

    if market_type is not None:
        filters_applied["market_type"] = market_type

    if crop_category is not None:
        filters_applied["crop_category"] = crop_category

    if year is not None:
        filters_applied["year"] = year

    if season is not None:
        filters_applied["season"] = season

    if price_tier is not None:
        filters_applied["price_tier"] = price_tier

    if district is not None:
        filters_applied["district"] = district

    return {

        "filters_applied": filters_applied,

        "comparison": comparison_df[
            [
                "market_name",
                "market_type",
                "price_tier",
                "district",
                "crop_name",
                "avg_price_per_ton_bdt",
                "total_quantity_sold_ton",
                "total_revenue_bdt"
            ]
        ].to_dict(orient="records")
    }