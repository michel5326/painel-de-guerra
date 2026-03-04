from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models
from core.kpi_engine import calculate_kpis

router = APIRouter(tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/{product_id}/dashboard")
def product_dashboard(
    product_id: int,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    all_logs = []

    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            query = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            )

            if start_date:
                query = query.filter(models.DailyLog.date >= start_date)

            if end_date:
                query = query.filter(models.DailyLog.date <= end_date)

            logs = query.all()
            all_logs.extend(logs)

    if not all_logs:
        return {
            "product": product.name,
            "status": "NO_DATA"
        }

    kpis = calculate_kpis(all_logs, product)

    return {
        "product": product.name,
        "start_date": start_date,
        "end_date": end_date,
        **kpis
    }