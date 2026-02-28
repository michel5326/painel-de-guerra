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

    # ======================
# KPI ENGINE
# ======================

@app.get("/keywords/{keyword_id}/kpis")
def get_keyword_kpis(keyword_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.DailyLog).filter(
        models.DailyLog.keyword_id == keyword_id
    ).all()

    if not logs:
        return {"message": "No data"}

    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    campaign = keyword.campaign
    product = campaign.product

    impressions = sum(log.impressions for log in logs)
    clicks = sum(log.clicks for log in logs)
    cost = sum(log.cost for log in logs)
    conversions = sum(log.conversions for log in logs)
    revenue = sum(log.revenue for log in logs)

    ctr = clicks / impressions if impressions > 0 else 0
    cpc = cost / clicks if clicks > 0 else 0
    cvr = conversions / clicks if clicks > 0 else 0
    cpa = cost / conversions if conversions > 0 else 0
    roas = revenue / cost if cost > 0 else 0

    # ECONOMIA AVANÇADA
    break_even_cpc = product.max_cpa * cvr if cvr > 0 else 0
    margem_real = revenue - cost
    conversoes_minimas = cost / product.max_cpa if product.max_cpa > 0 else 0

    # CLASSIFICAÇÃO
    if conversions == 0 and cost > product.max_cpa:
        status = "🔴 Inviável"
    elif roas >= product.min_roas:
        status = "🟢 Saudável"
    elif roas < product.min_roas:
        status = "🟡 Sob pressão"
    else:
        status = "⚪ Dados insuficientes"

    return {
        "impressions": impressions,
        "clicks": clicks,
        "cost": cost,
        "conversions": conversions,
        "revenue": revenue,
        "CTR": round(ctr, 4),
        "CPC": round(cpc, 2),
        "CVR": round(cvr, 4),
        "CPA": round(cpa, 2),
        "ROAS": round(roas, 2),
        "break_even_CPC": round(break_even_cpc, 2),
        "margem_real": round(margem_real, 2),
        "conversoes_minimas_para_empate": round(conversoes_minimas, 2),
        "status": status
    }