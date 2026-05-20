from pydantic import BaseModel
from typing import List, Dict


from pydantic import BaseModel
from typing import List, Dict


class YieldEfficiencyItem(BaseModel):

    crop_name: str
    crop_category: str

    avg_yield_benchmark_ton_per_ha: float
    actual_avg_yield_ton_per_ha: float

    efficiency_pct: float
    total_area_planted_ha: float

    season: str


class YieldEfficiencyResponse(BaseModel):

    filters_applied: Dict
    data: List[YieldEfficiencyItem]


# ------------------------------------


class SeasonalTrendItem(BaseModel):

    crop_name: str
    year: int
    quarter: int
    season: str

    total_quantity_sold_ton: float
    total_revenue_bdt: float
    avg_price_per_ton_bdt: float

    num_harvests: int


class SeasonalTrendResponse(BaseModel):

    filters_applied: Dict

    trend: List[SeasonalTrendItem] 


# ------------------------------------


class QualityBreakdownItem(BaseModel):

    crop_name: str
    quality_grade: str

    total_quantity: float


class QualityBreakdownResponse(BaseModel):

    quality_breakdown: List[
        QualityBreakdownItem
    ]