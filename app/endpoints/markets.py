from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from app.services.market_service import (
    get_market_comparison
)

from app.schemas.market_schema import (
    MarketComparisonResponse
)

from app.utils.validators import (
    validate_filter,
    VALID_MARKET_TYPES,
    VALID_CROP_CATEGORIES
)

router = APIRouter()


@router.get(
    "/markets/price-comparison",
    response_model=MarketComparisonResponse
)   
def market_comparison(

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

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    df = get_market_comparison(
        market_type,
        crop_category,
        year
    )

    return {

        "filters_applied": {
            "market_type": market_type,
            "crop_category": crop_category,
            "year": year
        },

        "comparison": df.to_dict(
            orient="records"
        )
    } 