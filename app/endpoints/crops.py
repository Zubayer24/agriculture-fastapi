from fastapi import (
    APIRouter,
    HTTPException,
    Query
)

from app.services.crop_service import (
    get_yield_efficiency,
    get_crop_trend,
    get_quality_breakdown
)

from app.schemas.crop_schema import (
    YieldEfficiencyResponse,
    SeasonalTrendResponse,
    QualityBreakdownResponse
) 

from app.utils.validators import (
    validate_filter,
    VALID_CROP_CATEGORIES,
    VALID_REGIONS
)

router = APIRouter()

@router.get(
    "/crops/yield-efficiency",
    response_model=YieldEfficiencyResponse
) 
def yield_efficiency(

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    ),

    region: str = Query(
        None,
        description="Filter by region"
    )
):

    try:

        crop_category = validate_filter(
            crop_category,
            VALID_CROP_CATEGORIES,
            "crop_category"
        )

        region = validate_filter(
            region,
            VALID_REGIONS,
            "region"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    df = get_yield_efficiency(
        crop_category,
        region
    )

    return {

        "filters_applied": {
            "crop_category": crop_category,
            "region": region
        },

        "data": df.to_dict(
            orient="records"
        )
    }


@router.get(
    "/crops/seasonal-trend",
    response_model=SeasonalTrendResponse
) 
def seasonal_trend(

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

    df = get_crop_trend(
        crop_category,
        year
    )

    return {

        "filters_applied": {
            "crop_category": crop_category,
            "year": year
        },

        "trend": df.to_dict(
            orient="records"
        )
    }


@router.get(
    "/crops/quality-breakdown",
    response_model=QualityBreakdownResponse
) 
def quality_breakdown(

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    )
):

    try:

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

    df = get_quality_breakdown(
        crop_category
    )

    return {

        "quality_breakdown": df.to_dict(
            orient="records"
        )
    }