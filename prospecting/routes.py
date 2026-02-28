from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import SessionLocal
from prospecting import models

router = APIRouter(prefix="/prospects", tags=["Prospecting"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_prospect(data: dict, db: Session = Depends(get_db)):
    new_prospect = models.Prospect(**data)
    db.add(new_prospect)
    db.commit()
    db.refresh(new_prospect)
    return new_prospect


@router.get("/")
def list_prospects(db: Session = Depends(get_db)):
    return db.query(models.Prospect).all()