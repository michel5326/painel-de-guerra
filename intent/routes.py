from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from intent.service import build_intent_analysis

router = APIRouter(tags=["Intent"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/{product_id}/intent-analysis")
def product_intent_analysis(product_id: int, db: Session = Depends(get_db)):

    result = build_intent_analysis(product_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return result