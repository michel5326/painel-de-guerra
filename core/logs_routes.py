from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models

router = APIRouter(tags=["Logs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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