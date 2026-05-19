from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query
)

from app.schemas.farm_schema import (
    FarmSummaryResponse,
    FarmPerformanceResponse,
    TopFarmResponse,
    LossAnalysisResponse
) 

from app.services.farm_service import (
    get_farm_summary,
    get_farm_performance,
    get_top_farms,
    get_loss_analysis
)

from app.utils.validators import (
    VALID_YEARS,
    validate_filter,
    VALID_REGIONS,
    VALID_FARM_TYPES,
    VALID_CROP_CATEGORIES,
    VALID_MARKET_TYPES,
    VALID_SEASONS,
    VALID_YEARS,
    VALID_QUALITY_GRADES 
) 

router = APIRouter()

@router.get(
    "/farms/summary",
    response_model=FarmSummaryResponse
) 
def farm_summary(

    region: str = Query(
        None,
        description="Filter by region"
    ),

    farm_type: str = Query(
        None,
        description="Filter by farm type"
    ),

    year: int = Query(
        None,
        description="Filter by year"
    ),

    season: str = Query(
        None,
        description="Filter by season"
    )
):

    try:

        region = validate_filter(
            region,
            VALID_REGIONS,
            "region"
        )

        farm_type = validate_filter(
            farm_type,
            VALID_FARM_TYPES,
            "farm_type"
        )

        year = validate_filter(
            year,
            VALID_YEARS,
            "year")

        season = validate_filter(
            season,
            VALID_SEASONS,
            "season")

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    grouped_df = get_farm_summary(
        region,
        farm_type,
        year,
        season
    )

        # Round avg_loss_pct to 1 decimal place
    grouped_df["avg_loss_pct"] = (
        grouped_df["avg_loss_pct"]
        .round(1)) 
    
    filters_applied = {}

    if region is not None:
        filters_applied["region"] = region

    if farm_type is not None:
        filters_applied["farm_type"] = farm_type

    if year is not None:
        filters_applied["year"] = year

    if season is not None:
        filters_applied["season"] = season

    return {

        "total_farms": grouped_df.shape[0],

        "filters_applied": filters_applied,

        "data": grouped_df.to_dict(
            orient="records"
        )
    }


@router.get(
    "/farms/{farm_id}/performance",
    response_model=FarmPerformanceResponse,
    summary= "Single Farm Performance"
) 
def farm_performance(

    farm_id: int = Path(..., description="ID of the farm",example=1),

    year: int = Query(
        None,
        description="Filter by year",
        example=2023
    ),

    crop_category: str = Query(None, description="Filter by crop category", example="Cereal"),

    market_type: str = Query(
        None,
        description="Filter by market type", example="Wholesale"
    )
): 

    try:

        crop_category = validate_filter(crop_category,
        VALID_CROP_CATEGORIES,
        "crop_category")

        market_type = validate_filter(
            market_type,
            VALID_MARKET_TYPES,
            "market_type"
        )

        year = validate_filter(
            year,
            VALID_YEARS,
            "year")

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    farm_df, performance_df = get_farm_performance(
        farm_id,
        year,
        crop_category,
        market_type
    ) 

    if farm_df.empty:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    # Round numeric values
    performance_df["quantity_sold_ton"] = (performance_df["quantity_sold_ton"].round(1))

    filters_applied = {}

    if year is not None:
        filters_applied["year"] = year

    if crop_category is not None:
        filters_applied["crop_category"] = crop_category

    if market_type is not None:
        filters_applied["market_type"] = market_type

    farm_info = farm_df.to_dict(
        orient="records"
    )[0]

    print(farm_df.columns)
    print(farm_df.head())

    return {

        "farm_id": farm_info["farm_id"],

        "farm_name": farm_info["farm_name"],

        "owner": farm_info["owner_name"], 

        "region": farm_info["region"],

        "filters_applied": filters_applied,

        "performance": performance_df.to_dict(
            orient="records")

    }



@router.get(
    "/farms/top",
    response_model=TopFarmResponse
) 
def top_farms(

    metric: str = Query(
        "profit",
        description="profit or revenue or yield"
    ),

    region: str = Query(
        None,
        description="Filter by region"
    ),

    farm_type: str = Query(
        None,
        description="Filter by farm type"
    ),

    year: int = Query(
        None,
        description="Filter by year"
    ),

    limit: int = Query(
        10,
        description="Top N farms"
    )
):

    try:

        region = validate_filter(
            region,
            VALID_REGIONS,
            "region"
        )

        farm_type = validate_filter(
            farm_type,
            VALID_FARM_TYPES,
            "farm_type")

        year = validate_filter(
        year,
        VALID_YEARS,
        "year") 

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )



    filters_applied = {}

    if region is not None:
        filters_applied["region"] = region

    if farm_type is not None:
        filters_applied["farm_type"] = farm_type

    if year is not None:
        filters_applied["year"] = year

    filters_applied["limit"] = limit

    df = get_top_farms(
        metric,
        region,
        farm_type,
        year,
        limit 
    )

    df = df.rename(columns={"total_profit_bdt": "net_profit_bdt"}) 

    return {

        "metric": metric,
        "filters_applied": filters_applied,
        "rankings": df[["rank", "farm_name", "region", "farm_type", "net_profit_bdt", "total_revenue_bdt"]]
        .to_dict(orient="records")
    } 



@router.get(
    "/farms/loss-analysis",
    response_model=LossAnalysisResponse
) 
def loss_analysis(

    region: str = Query(
        None,
        description="Filter by region"
    ),

    year: int = Query(
        None,
        description="Filter by year" 
    ), 

    season: str = Query(
        None,
        description="Filter by season"
    ),

    quality_grade: str = Query(
        None,
        description="Filter by quality grade"
    ),

    crop_category: str = Query(
        None,
        description="Filter by crop category"
    )
):

    try:

        region = validate_filter(
            region,
            VALID_REGIONS,
            "region"
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

        quality_grade = validate_filter(
            quality_grade,
            VALID_QUALITY_GRADES,
            "quality_grade")

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

    summary, breakdown_df = get_loss_analysis(
        region,
        year,
        season,
        quality_grade,
        crop_category
    ) 

    filters_applied = {}

    if region is not None:
        filters_applied["region"] = region

    if year is not None:
        filters_applied["year"] = year

    if season is not None:
        filters_applied["season"] = season

    if quality_grade is not None:
        filters_applied["quality_grade"] = quality_grade

    if crop_category is not None:
        filters_applied["crop_category"] = crop_category

    return {

        "filters_applied": filters_applied,

        "summary": summary,

        "breakdown": breakdown_df[[
            "region",
            "crop_category",
            "quality_grade",
            "total_lost_ton",
            "loss_pct",
            "pesticide_residue"
        ]].to_dict(orient="records")
    }  