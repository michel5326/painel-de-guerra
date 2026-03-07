from fastapi import APIRouter
from .schemas import CampaignGenerationRequest, CampaignGenerationResponse
from .service import CampaignGeneratorService

router = APIRouter()

service = CampaignGeneratorService()


@router.post("/campaign-generator", response_model=CampaignGenerationResponse)
def generate_campaign(data: CampaignGenerationRequest):

    campaigns = service.generate_campaign_structure(
        product_name=data.product_name,
        price=data.price_per_unit,
        discount_value=data.discount_value,
        discount_percent=data.discount_percent,
        country=data.country,
        guarantee_days=data.guarantee_days,
        installments_text=data.installments_text,
        currency=data.currency,
        bundle_offer=data.bundle_offer,
        free_shipping=data.free_shipping,
        stock_urgency=data.stock_urgency
    )

    return {
        "product": data.product_name,
        "campaigns": campaigns
    }