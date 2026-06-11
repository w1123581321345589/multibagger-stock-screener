from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class StockData(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: float
    enterprise_value: float
    current_price: float
    total_equity: float
    total_assets: float
    free_cash_flow: float
    ebitda: float
    revenue: float
    net_income: float
    high_52_week: float
    low_52_week: float
    return_1_month: float
    return_3_month: float
    return_6_month: float
    asset_growth_yoy: float
    ebitda_growth_yoy: float
    last_updated: Optional[datetime] = None


class MacroData(BaseModel):
    fed_funds_rate: float
    fed_funds_rate_1y_ago: float
    fed_rate_trajectory: str


class FactorResult(BaseModel):
    score: float
    tier: str
    weight: float
    details: Optional[Dict[str, Any]] = None
    flag: Optional[str] = None


class StockScore(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str] = None
    composite_score: float
    classification: str
    color: str
    flags: List[str]
    factor_breakdown: Dict[str, Any]
    adjustments_applied: float
    optimal_combo: bool
    market_cap: float
    current_price: float
