from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models
from core.kpi_engine import calculate_kpis

router = APIRouter(tags=["Keywords"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# CREATE KEYWORD
# ======================

@router.post("/keywords")
def create_keyword(keyword: dict, db: Session = Depends(get_db)):

    new_keyword = models.Keyword(**keyword)

    db.add(new_keyword)
    db.commit()
    db.refresh(new_keyword)

    return new_keyword


# ======================
# LIST KEYWORDS
# ======================

@router.get("/keywords")
def list_keywords(db: Session = Depends(get_db)):
    return db.query(models.Keyword).all()


# ======================
# UPDATE KEYWORD
# ======================

@router.put("/keywords/{keyword_id}")
def update_keyword(keyword_id: int, updated_data: dict, db: Session = Depends(get_db)):

    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")

    for key, value in updated_data.items():
        if hasattr(keyword, key):
            setattr(keyword, key, value)

    db.commit()
    db.refresh(keyword)

    return keyword


# ======================
# DELETE KEYWORD
# ======================

@router.delete("/keywords/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):

    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")

    db.delete(keyword)
    db.commit()

    return {"message": "Keyword deleted successfully"}


# ======================
# KEYWORD KPIS
# ======================

@router.get("/keywords/{keyword_id}/kpis")
def get_keyword_kpis(keyword_id: int, db: Session = Depends(get_db)):

    logs = db.query(models.DailyLog).filter(
        models.DailyLog.keyword_id == keyword_id
    ).all()

    keyword = db.query(models.Keyword).filter(
        models.Keyword.id == keyword_id
    ).first()

    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")

    if not logs:
        return {
            "impressions": 0,
            "clicks": 0,
            "cost": 0,
            "conversions": 0,
            "revenue": 0,
            "CTR": 0,
            "CPC": 0,
            "CVR_real": 0,
            "healthy_CPC": 0,
            "margem_real": 0,
            "status": "NO_DATA"
        }

    product = keyword.campaign.product

    return calculate_kpis(logs, product)