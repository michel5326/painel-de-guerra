from sqlalchemy.orm import Session
from core import models


def build_intent_performance(product_id: int, db: Session):

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

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

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

        # 🔒 Regra de proteção estatística (>=5 conversões)
        conversion_base = (
            cvr_real if conversions >= 5
            else estimated_cvr
        )

        healthy_cpc = commission * conversion_base
        gap = healthy_cpc - cpc

        # Status estrutural por intenção
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
            "CTR": round(ctr * 100, 2),  # agora já vem em %
            "CPC": round(cpc, 2),
            "CVR": round(cvr_real * 100, 2),  # em %
            "healthy_CPC": round(healthy_cpc, 2),
            "gap": round(gap, 2),
            "status": status
        }

    return result