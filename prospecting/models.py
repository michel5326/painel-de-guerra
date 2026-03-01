from sqlalchemy import Column, Integer, String, Float, Text
from db import Base


class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    country = Column(String, nullable=False)

    search_volume_last_month = Column(Integer, nullable=False)

    commission_value = Column(Float, nullable=False)

    top_bid_low = Column(Float, nullable=False)
    top_bid_high = Column(Float, nullable=False)

    temperature_ranking = Column(String, nullable=True)
    observations = Column(Text, nullable=True)