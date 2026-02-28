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