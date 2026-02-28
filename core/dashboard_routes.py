from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models

router = APIRouter(tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/{product_id}/dashboard")
def product_dashboard(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    total_impressions = 0
    total_clicks = 0
    total_cost = 0
    total_conversions = 0
    total_revenue = 0

    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

            for log in logs:
                total_impressions += log.impressions
                total_clicks += log.clicks
                total_cost += log.cost
                total_conversions += log.conversions
                total_revenue += log.revenue

    ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    cpc = total_cost / total_clicks if total_clicks > 0 else 0
    cvr_real = total_conversions / total_clicks if total_clicks > 0 else 0

    if total_conversions >= 5:
        conversion_base = cvr_real
    else:
        conversion_base = product.estimated_conversion_rate or 0

    commission = product.commission_value or 0
    healthy_cpc = commission * conversion_base
    max_cpc = healthy_cpc * 1.3

    if cpc > max_cpc:
        status = "🔴 CPC Acima do Viável"
    elif cpc > healthy_cpc:
        status = "🟡 Zona de Atenção"
    else:
        status = "🟢 Operando Saudável"

    return {
        "product": product.name,
        "impressions": total_impressions,
        "clicks": total_clicks,
        "cost": round(total_cost, 2),
        "revenue": round(total_revenue, 2),
        "CTR": round(ctr, 4),
        "CPC_medio": round(cpc, 2),
        "CVR_real": round(cvr_real, 4),
        "conversion_base_usada": round(conversion_base, 4),
        "healthy_CPC": round(healthy_cpc, 2),
        "max_CPC": round(max_cpc, 2),
        "status_operacional": status
    }