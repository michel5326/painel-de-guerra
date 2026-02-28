from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from db import SessionLocal
from core import models
from core.kpi_engine import calculate_kpis

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {"status": "AFF-OS online"}


# ======================
# PRODUCTS
# ======================

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

    # Conversão base
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

# ======================
# CAMPAIGNS
# ======================

@router.post("/campaigns")
def create_campaign(campaign: dict, db: Session = Depends(get_db)):
    new_campaign = models.Campaign(**campaign)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign


@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()


@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(
        models.Campaign.id == campaign_id
    ).first()

    if not campaign:
        return {"error": "Campaign not found"}

    db.delete(campaign)
    db.commit()

    return {"message": "Campaign deleted successfully"}


# ======================
# KEYWORDS
# ======================

@router.post("/keywords")
def create_keyword(keyword: dict, db: Session = Depends(get_db)):
    new_keyword = models.Keyword(**keyword)
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)
    return new_keyword


@router.get("/keywords")
def list_keywords(db: Session = Depends(get_db)):
    return db.query(models.Keyword).all()


@router.delete("/keywords/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    if not keyword:
        return {"error": "Keyword not found"}

    db.delete(keyword)
    db.commit()

    return {"message": "Keyword deleted successfully"}


# ======================
# LOGS
# ======================

@router.get("/logs")
def list_logs(db: Session = Depends(get_db)):

    logs = db.query(models.DailyLog).all()

    result = []

    for log in logs:

        cpc = log.cost / log.clicks if log.clicks > 0 else 0

        result.append({
            "id": log.id,
            "date": log.date,
            "keyword_id": log.keyword_id,
            "impressions": log.impressions,
            "clicks": log.clicks,
            "cost": log.cost,
            "CPC": round(cpc, 2),
            "visitors": log.visitors,
            "checkouts": log.checkouts,
            "conversions": log.conversions,
            "revenue": log.revenue,
            "upsells": log.upsells
        })

    return result

# ======================
# KPI ENGINE
# ======================

@router.get("/keywords/{keyword_id}/kpis")
def get_keyword_kpis(keyword_id: int, db: Session = Depends(get_db)):

    logs = db.query(models.DailyLog).filter(
        models.DailyLog.keyword_id == keyword_id
    ).all()

    if not logs:
        return {"message": "No data"}

    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    product = keyword.campaign.product

    return calculate_kpis(logs, product)