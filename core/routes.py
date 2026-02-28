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

            cost = sum(log.cost for log in logs)
            revenue = sum(log.revenue for log in logs)
            conversions = sum(log.conversions for log in logs)

            total_cost += cost
            total_revenue += revenue
            total_conversions += conversions

            roas = revenue / cost if cost > 0 else 0

            if roas >= product.min_roas:
                status = "🟢"
            else:
                status = "🟡"

            all_keywords.append({
                "keyword": keyword.keyword,
                "roas": round(roas, 2),
                "conversions": conversions,
                "cost": round(cost, 2),
                "revenue": round(revenue, 2),
                "status": status
            })

    roas_total = total_revenue / total_cost if total_cost > 0 else 0
    cpa_medio = total_cost / total_conversions if total_conversions > 0 else 0

    if roas_total >= product.min_roas:
        product_status = "🟢 Saudável"
    else:
        product_status = "🟡 Sob pressão"

    return {
        "product": product.name,
        "receita_total": round(total_revenue, 2),
        "custo_total": round(total_cost, 2),
        "roas_medio": round(roas_total, 2),
        "cpa_medio": round(cpa_medio, 2),
        "status_geral": product_status,
        "keywords": all_keywords
    }