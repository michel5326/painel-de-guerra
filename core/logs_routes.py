from fastapi import APIRouter, Depends, HTTPException
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


# ======================
# CREATE LOG
# ======================

@router.post("/logs")
def create_log(log: dict, db: Session = Depends(get_db)):

    new_log = models.DailyLog(**log)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


# ======================
# LIST LOGS
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
# UPDATE LOG
# ======================

@router.put("/logs/{log_id}")
def update_log(log_id: int, updated_data: dict, db: Session = Depends(get_db)):

    log = db.query(models.DailyLog).filter(
        models.DailyLog.id == log_id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    for key, value in updated_data.items():
        if hasattr(log, key):
            setattr(log, key, value)

    db.commit()
    db.refresh(log)

    return log


# ======================
# DELETE LOG
# ======================

@router.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):

    log = db.query(models.DailyLog).filter(
        models.DailyLog.id == log_id
    ).first()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(log)
    db.commit()

    return {"message": "Log deleted successfully"}