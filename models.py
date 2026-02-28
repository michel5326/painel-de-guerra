from sqlalchemy import Column, Integer, String, Float
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