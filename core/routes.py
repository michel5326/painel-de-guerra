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

    log.setdefault("visitors", 0)
    log.setdefault("checkouts", 0)
    log.setdefault("upsells", 0)
    log.setdefault("bounce_rate", None)

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