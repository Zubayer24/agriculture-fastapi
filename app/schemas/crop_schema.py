from pydantic import BaseModel
from typing import List, Dict


class YieldEfficiencyItem(BaseModel):

    crop_name: str
    crop_category: str

    avg_yield_per_hectare: float
    total_area_ha: float


class YieldEfficiencyResponse(BaseModel):

    filters_applied: Dict

    data: List[YieldEfficiencyItem]


# ------------------------------------


class SeasonalTrendItem(BaseModel):

    crop_name: str
    crop_category: str
    year: int

    total_revenue_bdt: float


class SeasonalTrendResponse(BaseModel):

    filters_applied: Dict

    trend: List[Dict]


# ------------------------------------


class QualityBreakdownItem(BaseModel):

    crop_name: str
    quality_grade: str

    total_quantity: float


class QualityBreakdownResponse(BaseModel):

    quality_breakdown: List[
        QualityBreakdownItem
    ]