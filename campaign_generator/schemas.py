from pydantic import BaseModel
from typing import List


class CampaignGenerationRequest(BaseModel):

    product_name: str
    price_per_unit: float
    discount_value: float | None = None
    discount_percent: float | None = None

    guarantee_days: int | None = None
    installments_text: str | None = None
    currency: str | None = None
    country: str = "US"

    bundle_offer: str | None = None
    free_shipping: bool | None = None
    stock_urgency: str | None = None


class AdAsset(BaseModel):

    headlines: List[str]
    descriptions: List[str]


class CampaignStructure(BaseModel):

    campaign_name: str
    ad_group: str
    keywords: List[str]
    ads: AdAsset
    callouts: List[str]


class CampaignGenerationResponse(BaseModel):

    product: str
    campaigns: List[CampaignStructure]