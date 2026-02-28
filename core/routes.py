from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from db import SessionLocal
from core import models
from core.kpi_engine import calculate_kpis

router = APIRouter()

# ======================
# DATABASE SESSION
# ======================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# ROOT
# ======================

@router.get("/")
def root():
    return {"status": "AFF-OS online"}


# ======================
# PRODUCTS
# ======================

@router.post("/products")
def create_product(product: dict, db: Session = Depends(get_db)):
    new_product = models.Product(**product)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


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

@router.post("/logs")
def create_log(log: dict, db: Session = Depends(get_db)):
    log["date"] = date.fromisoformat(log["date"])
    new_log = models.DailyLog(**log)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


@router.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return db.query(models.DailyLog).all()


@router.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.DailyLog).filter(
        models.DailyLog.id == log_id
    ).first()

    if not log:
        return {"error": "Log not found"}

    db.delete(log)
    db.commit()

    return {"message": "Log deleted successfully"}


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


# ======================
# PRODUCT DASHBOARD
# ======================

@router.get("/products/{product_id}/dashboard")
def product_dashboard(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"message": "Product not found"}

    all_keywords = []
    total_cost = 0
    total_revenue = 0
    total_conversions = 0

    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

            if not logs:
                continue

            logs_sorted = sorted(logs, key=lambda x: x.date)

            cost = sum(log.cost for log in logs_sorted)
            revenue = sum(log.revenue for log in logs_sorted)
            conversions = sum(log.conversions for log in logs_sorted)

            total_cost += cost
            total_revenue += revenue
            total_conversions += conversions

            roas = revenue / cost if cost > 0 else 0

            roas_series = [
                (log.revenue / log.cost) if log.cost > 0 else 0
                for log in logs_sorted
            ]

            trend = "→"
            if len(roas_series) >= 3:
                if roas_series[-1] > roas_series[-2] > roas_series[-3]:
                    trend = "↑"
                elif roas_series[-1] < roas_series[-2] < roas_series[-3]:
                    trend = "↓"

            status = "🟢" if roas >= product.min_roas else "🟡"

            all_keywords.append({
                "keyword": keyword.keyword,
                "roas": round(roas, 2),
                "trend": trend,
                "conversions": conversions,
                "cost": round(cost, 2),
                "revenue": round(revenue, 2),
                "status": status
            })

    roas_total = total_revenue / total_cost if total_cost > 0 else 0
    cpa_medio = total_cost / total_conversions if total_conversions > 0 else 0

    product_status = "🟢 Saudável" if roas_total >= product.min_roas else "🟡 Sob pressão"

    return {
        "product": product.name,
        "receita_total": round(total_revenue, 2),
        "custo_total": round(total_cost, 2),
        "roas_medio": round(roas_total, 2),
        "cpa_medio": round(cpa_medio, 2),
        "status_geral": product_status,
        "keywords": all_keywords
    }