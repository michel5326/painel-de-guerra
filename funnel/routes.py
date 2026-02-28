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
        return {"message": "No data"}

    return data