from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    commission_value: float
    estimated_conversion_rate: float
    status: str = "active"


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    commission_value: Optional[float] = None
    estimated_conversion_rate: Optional[float] = None
    status: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    commission_value: float
    estimated_conversion_rate: float
    status: str

    class Config:
        from_attributes = True