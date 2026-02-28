from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from db import engine, Base, SessionLocal
import models

app = FastAPI()

# cria tabelas
Base.metadata.create_all(bind=engine)

# sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "AFF-OS online"}


# ======================
# PRODUCTS
# ======================

@app.post("/products")
def create_product(product: dict, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product["name"],
        avg_ticket=product["avg_ticket"],
        commission=product["commission"],
        margin=product["margin"],
        max_cpa=product["max_cpa"],
        min_roas=product["min_roas"],
        status=product.get("status", "active")
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"id": new_product.id, "name": new_product.name}


@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# ======================
# CAMPAIGNS
# ======================

@app.post("/campaigns")
def create_campaign(campaign: dict, db: Session = Depends(get_db)):
    new_campaign = models.Campaign(
        name=campaign["name"],
        daily_budget=campaign["daily_budget"],
        status=campaign.get("status", "active"),
        product_id=campaign["product_id"]
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return {"id": new_campaign.id, "name": new_campaign.name}


@app.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()


# ======================
# KEYWORDS
# ======================

@app.post("/keywords")
def create_keyword(keyword: dict, db: Session = Depends(get_db)):
    new_keyword = models.Keyword(
        keyword=keyword["keyword"],
        match_type=keyword["match_type"],
        intent=keyword["intent"],
        status=keyword.get("status", "active"),
        campaign_id=keyword["campaign_id"]
    )
    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)

    return {"id": new_keyword.id, "keyword": new_keyword.keyword}


@app.get("/keywords")
def list_keywords(db: Session = Depends(get_db)):
    return db.query(models.Keyword).all()


# ======================
# DAILY LOGS
# ======================

@app.post("/logs")
def create_log(log: dict, db: Session = Depends(get_db)):
    new_log = models.DailyLog(
        date=date.fromisoformat(log["date"]),
        impressions=log["impressions"],
        clicks=log["clicks"],
        cost=log["cost"],
        conversions=log["conversions"],
        revenue=log["revenue"],
        keyword_id=log["keyword_id"]
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {"id": new_log.id}


@app.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return db.query(models.DailyLog).all()