from pydantic import BaseModel
from typing import List, Optional, Dict


class FarmSummaryItem(BaseModel):

    farm_name: str
    region: str
    farm_type: str

    total_revenue_bdt: float
    total_cost_bdt: float
    net_profit_bdt: float
    avg_loss_pct: float


class FarmSummaryResponse(BaseModel):

    total_farms: int

    filters_applied: Dict

    data: List[FarmSummaryItem]




class FarmPerformanceItem(BaseModel):

    crop_name: str
    year: int
    market_type: str

    quantity_sold_ton: float
    revenue_bdt:float
    net_profit_bdt: float
    quality_grade: str


class FarmPerformanceResponse(BaseModel):

    farm_id: int
    farm_name: str
    owner:str
    region:str 
    filters_applied: Dict
    performance: List[FarmPerformanceItem]




class TopFarmItem(BaseModel):

    farm_name: str
    region: str
    farm_type: str

    total_revenue_bdt: float
    net_profit_bdt: float


class TopFarmResponse(BaseModel):

    metric: str
    filters_applied: Dict
    rankings: List[Dict]




class LossBreakdownItem(BaseModel):

    region: str
    crop_category: str
    quality_grade: str

    total_lost_ton: float
    loss_pct: float

    pesticide_residue: str


class LossSummary(BaseModel):

    total_harvested_ton: float
    total_lost_ton: float
    overall_loss_pct: float


class LossAnalysisResponse(BaseModel):

    filters_applied: Dict

    summary: LossSummary

    breakdown: List[LossBreakdownItem] 