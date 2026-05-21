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
    VALID_REGIONS,
    VALID_YEARS,
    VALID_QUARTERS,
    VALID_MARKET_TYPES,
    VALID_PESTICIDE_RESIDUES,
    VALID_CROP_IDS
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


from app.database import engine
import pandas as pd

router = APIRouter()

@router.get(
    "/crops/yield-efficiency",
    response_model=YieldEfficiencyResponse
) 



def yield_efficiency(
    crop_category: str = Query(None, description="filter by crop category"),
    season: str = Query(None, description="filter by season"),
    year: int = Query(None, description="filter by year"),
    region: str = Query(None, description="filter by region"),
    water_requirement: str = Query(None, description="filter by water requirement (low, medium, high)")):

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

    crop_name: str = Query(
        None,
        description="Filter by crop name"
    ),

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    ),

    year: int = Query(
        None,
        description="Filter by year"
    ),

    quarter: int = Query(
        None,
        description="Filter by quarter"
    ),

    market_type: str = Query(
        None,
        description="Filter by market type"
    )
):

    try:

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

        quarter = validate_filter(
            quarter,
            VALID_QUARTERS,
            "quarter"
        )

        market_type = validate_filter(
            market_type,
            VALID_MARKET_TYPES,
            "market_type"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    df = pd.read_sql(
        "SELECT * FROM vw_harvest_full",
        engine
    )

    result_df = get_crop_trend(
        df,
        crop_name,
        crop_category,
        year,
        quarter,
        market_type
    )

    filters_applied = {}

    if crop_name is not None:
        filters_applied["crop_name"] = crop_name

    if crop_category is not None:
        filters_applied["crop_category"] = crop_category

    if year is not None:
        filters_applied["year"] = year

    if quarter is not None:
        filters_applied["quarter"] = quarter

    if market_type is not None:
        filters_applied["market_type"] = market_type

    return {

        "filters_applied": filters_applied,

        "trend": result_df[
            [
                "crop_name",
                "year",
                "quarter",
                "season",
                "total_quantity_sold_ton",
                "total_revenue_bdt",
                "avg_price_per_ton_bdt",
                "num_harvests"
            ]
        ].to_dict(orient="records")
    } 




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


@router.get(
    "/crops/quality-breakdown",
    response_model=QualityBreakdownResponse
)
def quality_breakdown(

    crop_id: int = Query(
        None,
        description="Filter by crop id"
    ),

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    ),

    year: int = Query(
        None,
        description="Filter by year"
    ),

    region: str = Query(
        None,
        description="Filter by region"
    ),

    market_type: str = Query(
        None,
        description="Filter by market type"
    ),

    pesticide_residue: str = Query(
        None,
        description="Filter by pesticide residue"
    )
):

    try:

        crop_category = validate_filter(
            crop_category,
            VALID_CROP_CATEGORIES,
            "crop_category"
        )

        crop_id = validate_filter(
            crop_id,
            VALID_CROP_IDS,
            "crop_id")

        year = validate_filter(
            year,
            VALID_YEARS,
            "year"
        )

        region = validate_filter(
            region,
            VALID_REGIONS,
            "region"
        )

        market_type = validate_filter(
            market_type,
            VALID_MARKET_TYPES,
            "market_type"
        )

        pesticide_residue = validate_filter(
            pesticide_residue,
            VALID_PESTICIDE_RESIDUES,
            "pesticide_residue"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    result = get_quality_breakdown(
        crop_id,
        crop_category,
        year,
        region,
        market_type,
        pesticide_residue
    )

    filters_applied = {}

    if crop_id is not None:
        filters_applied["crop_id"] = crop_id

    if crop_category is not None:
        filters_applied["crop_category"] = crop_category

    if year is not None:
        filters_applied["year"] = year

    if region is not None:
        filters_applied["region"] = region

    if market_type is not None:
        filters_applied["market_type"] = market_type

    if pesticide_residue is not None:
        filters_applied["pesticide_residue"] = pesticide_residue

    return {
        "filters_applied": filters_applied,
        "total_records": result["total_records"],
        "grade_distribution": result["grade_distribution"],
        "pesticide_residue_breakdown": result["pesticide_residue_breakdown"]
    }