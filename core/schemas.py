from pydantic import BaseModel


# ======================
# PRODUCT
# ======================

class ProductCreate(BaseModel):
    name: str
    commission_value: float
    estimated_conversion_rate: float


class ProductResponse(BaseModel):
    id: int
    name: str
    commission_value: float
    estimated_conversion_rate: float
    status: str

    class Config:
        from_attributes = True