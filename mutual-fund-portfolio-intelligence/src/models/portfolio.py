from pydantic import BaseModel, Field
from typing import List


class InvestorProfile(BaseModel):
    age: int = Field(gt=0, le=100)
    risk_tolerance: str
    investment_goal: str
    investment_horizon_years: int = Field(gt=0)


class PortfolioHolding(BaseModel):
    fund_name: str
    units: float = Field(gt=0)
    purchase_price: float = Field(gt=0)


class Portfolio(BaseModel):
    investor: InvestorProfile
    holdings: List[PortfolioHolding]