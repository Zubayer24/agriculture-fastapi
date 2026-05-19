from pydantic import BaseModel
from typing import List, Dict


class MarketComparisonItem(BaseModel):

    market_name: str
    market_type: str
    crop_name: str

    avg_price_per_ton_bdt: float
    total_revenue_bdt: float


class MarketComparisonResponse(BaseModel):

    filters_applied: Dict

    comparison: List[
        MarketComparisonItem
    ]