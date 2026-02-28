from sqlalchemy import Column, Integer, String, Float, Text
from db import Base


class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    country = Column(String, nullable=False)

    main_intent = Column(String, nullable=False)

    structure_observed = Column(Text, nullable=True)
    angles_identified = Column(Text, nullable=True)

    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)

    opportunity_score = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)