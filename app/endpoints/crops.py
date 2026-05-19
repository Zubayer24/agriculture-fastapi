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


from app.database import engine
import pandas as pd

router = APIRouter()

@router.get(
    "/crops/yield-efficiency",
    response_model=YieldEfficiencyResponse
) 



def yield_efficiency(
    crop_category: str = Query(None),
    season: str = Query(None),
    year: int = Query(None),
    region: str = Query(None),
    water_requirement: str = Query(None)):

    df = pd.read_sql("SELECT * FROM vw_harvest_full", engine)

    result_df = get_yield_efficiency(
        df,
        crop_category,
        season,
        year,
        region,
        water_requirement
    )


    filters_applied = {}

    if crop_category:
        filters_applied["crop_category"] = crop_category
    if season:
        filters_applied["season"] = season
    if year:
        filters_applied["year"] = year
    if region:
        filters_applied["region"] = region
    if water_requirement:
        filters_applied["water_requirement"] = water_requirement


    return {
        "filters_applied": filters_applied,
        "data": result_df[[
            "crop_name",
            "crop_category",
            "avg_yield_benchmark_ton_per_ha",
            "actual_avg_yield_ton_per_ha",
            "efficiency_pct",
            "total_area_planted_ha",
            "season"
        ]].to_dict(orient="records")
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