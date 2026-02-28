from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    avg_ticket = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    max_cpa = Column(Float, nullable=False)
    min_roas = Column(Float, nullable=False)
    status = Column(String, default="active")

    campaigns = relationship("Campaign", back_populates="product")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    daily_budget = Column(Float, nullable=False)
    status = Column(String, default="active")

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="campaigns")

    keywords = relationship("Keyword", back_populates="campaign")


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False)
    match_type = Column(String, nullable=False)
    intent = Column(String, nullable=False)
    status = Column(String, default="active")

    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="keywords")

    from datetime import date

# ======================
# DAILY LOGS
# ======================

@app.post("/logs")
def create_log(log: dict, db: Session = Depends(get_db)):
    new_log = models.DailyLog(
        date=date.fromisoformat(log["date"]),
        impressions=log["impressions"],
        clicks=log["clicks"],
        cost=log["cost"],
        conversions=log["conversions"],
        revenue=log["revenue"],
        keyword_id=log["keyword_id"]
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {"id": new_log.id}


@app.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return db.query(models.DailyLog).all()