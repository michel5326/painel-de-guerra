from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from funnel.service import build_keyword_funnel

router = APIRouter(prefix="/funnel", tags=["Funnel"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/keywords/{keyword_id}")
def get_keyword_funnel(keyword_id: int, db: Session = Depends(get_db)):

    data = build_keyword_funnel(keyword_id, db)

    if not data:
        return {
            "funnel": {
                "impressions": 0,
                "clicks": 0,
                "visitors": 0,
                "checkouts": 0,
                "sales": 0,
                "upsells": 0
            },
            "rates": {
                "ctr": 0,
                "visit_rate": 0,
                "checkout_rate": 0,
                "sales_rate": 0,
                "upsell_rate": 0
            },
            "suggestions": []
        }

    return data