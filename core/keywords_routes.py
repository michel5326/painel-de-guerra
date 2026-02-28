from fastapi import APIRouter, Depends
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