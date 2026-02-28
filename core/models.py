from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from db import Base


# ======================
# OPERACIONAL
# ======================

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

    campaigns = relationship(
        "Campaign",
        back_populates="product",
        cascade="all, delete-orphan"
    )


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    daily_budget = Column(Float, nullable=False)
    status = Column(String, default="active")

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE")
    )

    product = relationship("Product", back_populates="campaigns")

    keywords = relationship(
        "Keyword",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False)
    match_type = Column(String, nullable=False)
    intent = Column(String, nullable=False)
    status = Column(String, default="active")

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE")
    )

    campaign = relationship("Campaign", back_populates="keywords")

    logs = relationship(
        "DailyLog",
        back_populates="keyword",
        cascade="all, delete-orphan"
    )


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    conversions = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)

    keyword_id = Column(
        Integer,
        ForeignKey("keywords.id", ondelete="CASCADE")
    )

    keyword = relationship("Keyword", back_populates="logs")