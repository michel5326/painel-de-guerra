from sqlalchemy.orm import Session
from core import models


def build_intent_analysis(product_id: int, db: Session):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return None

    intent_data = {}

    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

            if not logs:
                continue

            impressions = sum(log.impressions for log in logs)
            clicks = sum(log.clicks for log in logs)
            cost = sum(log.cost for log in logs)
            conversions = sum(log.conversions for log in logs)

            intent = keyword.intent

            if intent not in intent_data:
                intent_data[intent] = {
                    "impressions": 0,
                    "clicks": 0,
                    "cost": 0,
                    "conversions": 0
                }

            intent_data[intent]["impressions"] += impressions
            intent_data[intent]["clicks"] += clicks
            intent_data[intent]["cost"] += cost
            intent_data[intent]["conversions"] += conversions

    result = {}

    for intent, data in intent_data.items():

        clicks = data["clicks"]
        impressions = data["impressions"]
        cost = data["cost"]
        conversions = data["conversions"]

        ctr = clicks / impressions if impressions > 0 else 0
        cpc = cost / clicks if clicks > 0 else 0
        cvr = conversions / clicks if clicks > 0 else 0

        result[intent] = {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "CTR": round(ctr, 4),
            "CPC": round(cpc, 2),
            "CVR": round(cvr, 4)
        }

    return result