from fastapi import APIRouter, Depends, HTTPException
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


# ======================
# CREATE
# ======================

@router.post("/")
def create_prospect(data: dict, db: Session = Depends(get_db)):

    new_prospect = models.Prospect(**data)
    db.add(new_prospect)
    db.commit()
    db.refresh(new_prospect)

    return new_prospect


# ======================
# LIST
# ======================

@router.get("/")
def list_prospects(db: Session = Depends(get_db)):

    prospects = db.query(models.Prospect).all()

    result = []

    for p in prospects:

        average_bid = (
            (p.top_bid_low + p.top_bid_high) / 2
            if p.top_bid_low and p.top_bid_high
            else 0
        )

        cost_20_clicks = average_bid * 20

        viability_ratio = (
            p.commission_value / cost_20_clicks
            if cost_20_clicks > 0
            else 0
        )

        # NEW METRICS
        break_even_clicks = (
            p.commission_value / average_bid
            if average_bid > 0
            else 0
        )

        required_cvr = (
            average_bid / p.commission_value
            if p.commission_value > 0
            else 0
        )

        if required_cvr < 0.02:
            difficulty_status = "🟢 Muito forte"
        elif required_cvr < 0.03:
            difficulty_status = "🟢 Bom"
        elif required_cvr < 0.04:
            difficulty_status = "🟡 Médio"
        else:
            difficulty_status = "🔴 Difícil"

        if viability_ratio > 1:
            viability_status = "🟢 Promissor"
        elif viability_ratio > 0.7:
            viability_status = "🟡 Arriscado"
        else:
            viability_status = "🔴 Inviável"

        result.append({
            "id": p.id,
            "product_name": p.product_name,
            "platform": p.platform,
            "country": p.country,
            "search_volume_last_month": p.search_volume_last_month,
            "commission_value": p.commission_value,
            "top_bid_low": p.top_bid_low,
            "top_bid_high": p.top_bid_high,
            "average_bid": round(average_bid, 2),
            "cost_20_clicks": round(cost_20_clicks, 2),
            "break_even_clicks": round(break_even_clicks, 2),
            "required_cvr": round(required_cvr * 100, 2),
            "difficulty_status": difficulty_status,
            "viability_ratio": round(viability_ratio, 2),
            "viability_status": viability_status,
            "temperature_ranking": p.temperature_ranking,
            "observations": p.observations
        })

    return result


# ======================
# UPDATE
# ======================

@router.put("/{prospect_id}")
def update_prospect(prospect_id: int, data: dict, db: Session = Depends(get_db)):

    prospect = db.query(models.Prospect).filter(
        models.Prospect.id == prospect_id
    ).first()

    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    for key, value in data.items():
        if hasattr(prospect, key):
            setattr(prospect, key, value)

    db.commit()
    db.refresh(prospect)

    return prospect


# ======================
# DELETE
# ======================

@router.delete("/{prospect_id}")
def delete_prospect(prospect_id: int, db: Session = Depends(get_db)):

    prospect = db.query(models.Prospect).filter(
        models.Prospect.id == prospect_id
    ).first()

    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    db.delete(prospect)
    db.commit()

    return {"message": "Prospect deleted successfully"}