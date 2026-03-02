from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from product_intelligence.service import build_strategic_dashboard

router = APIRouter(tags=["Product Intelligence"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/{product_id}/strategic-dashboard")
def strategic_dashboard(product_id: int, db: Session = Depends(get_db)):

    result = build_strategic_dashboard(product_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result