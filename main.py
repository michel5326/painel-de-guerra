from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "AFF-OS online"}

@app.post("/products")
def create_product(product: dict, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=product["name"],
        avg_ticket=product["avg_ticket"],
        commission=product["commission"],
        margin=product["margin"],
        max_cpa=product["max_cpa"],
        min_roas=product["min_roas"],
        status=product.get("status", "active")
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"id": new_product.id, "name": new_product.name}