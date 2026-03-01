from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models
from core.schemas import ProductCreate, ProductResponse

router = APIRouter(tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# CREATE PRODUCT
# ======================

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    new_product = models.Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# ======================
# LIST PRODUCTS
# ======================

@router.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# ======================
# UPDATE PRODUCT
# ======================

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_data: ProductCreate, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


# ======================
# DELETE PRODUCT
# ======================

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}