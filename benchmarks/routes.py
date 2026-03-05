from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from benchmarks.service import build_account_benchmarks

router = APIRouter(prefix="/account", tags=["Benchmarks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/benchmarks/{product_id}")
def get_account_benchmarks(product_id: int, db: Session = Depends(get_db)):
    return build_account_benchmarks(product_id, db)