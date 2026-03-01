from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from core import models

router = APIRouter(tags=["Campaigns"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# CREATE CAMPAIGN
# ======================

@router.post("/campaigns")
def create_campaign(campaign: dict, db: Session = Depends(get_db)):

    new_campaign = models.Campaign(**campaign)

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return new_campaign


# ======================
# LIST CAMPAIGNS
# ======================

@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()


# ======================
# UPDATE CAMPAIGN
# ======================

@router.put("/campaigns/{campaign_id}")
def update_campaign(campaign_id: int, updated_data: dict, db: Session = Depends(get_db)):

    campaign = db.query(models.Campaign).filter(
        models.Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    for key, value in updated_data.items():
        if hasattr(campaign, key):
            setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)

    return campaign


# ======================
# DELETE CAMPAIGN
# ======================

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):

    campaign = db.query(models.Campaign).filter(
        models.Campaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()

    return {"message": "Campaign deleted successfully"}