from datetime import date
from sqlalchemy.orm import Session
from core import models


def build_intent_analysis(
    product_id: int,
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return None

    intent_data = {}

    # ==========================
    # Coleta dados por intenção
    # ==========================
    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            query = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            )

            if start_date:
                query = query.filter(models.DailyLog.date >= start_date)

            if end_date:
                query = query.filter(models.DailyLog.date <= end_date)

            logs = query.all()

            if not logs:
                continue

            intent = keyword.intent

            if intent not in intent_data:
                intent_data[intent] = {
                    "impressions": 0,
                    "clicks": 0,
                    "cost": 0,
                    "conversions": 0,
                    "revenue": 0
                }

            for log in logs:
                intent_data[intent]["impressions"] += log.impressions
                intent_data[intent]["clicks"] += log.clicks
                intent_data[intent]["cost"] += log.cost
                intent_data[intent]["conversions"] += log.conversions
                intent_data[intent]["revenue"] += log.revenue

    # ==========================
    # Cálculo estrutural por intenção
    # ==========================
    result = {}

    estimated_cvr = product.estimated_conversion_rate or 0
    commission = product.commission_value or 0

    for intent, data in intent_data.items():

        impressions = data["impressions"]
        clicks = data["clicks"]
        cost = data["cost"]
        conversions = data["conversions"]

        ctr = clicks / impressions if impressions > 0 else 0
        cpc = cost / clicks if clicks > 0 else 0
        cvr_real = conversions / clicks if clicks > 0 else 0

        # 🔒 Regra de proteção estatística
        conversion_base = (
            cvr_real if conversions >= 5
            else estimated_cvr
        )

        healthy_cpc = commission * conversion_base
        gap = healthy_cpc - cpc

        # Status estrutural
        if gap < 0:
            status = "🔴 Inviável"
        elif gap < healthy_cpc * 0.2:
            status = "🟡 Atenção"
        else:
            status = "🟢 Saudável"

        result[intent] = {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "CTR": round(ctr * 100, 2),
            "CPC": round(cpc, 2),
            "CVR": round(cvr_real * 100, 2),
            "healthy_CPC": round(healthy_cpc, 2),
            "gap": round(gap, 2),
            "status": status
        }

    return result