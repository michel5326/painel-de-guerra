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

    # 🔥 orçamento máximo de teste
    test_budget_limit = commission * 3

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

        # ==========================
        # Probabilidade estatística
        # ==========================

        baseline_cvr = estimated_cvr if estimated_cvr > 0 else 0.01

        if clicks > 0:
            probability_no_conversion = (1 - baseline_cvr) ** clicks
        else:
            probability_no_conversion = 1

        if probability_no_conversion > 0.5:
            probability_status = "🟢 Testando"
        elif probability_no_conversion > 0.2:
            probability_status = "🟡 Atenção"
        elif probability_no_conversion > 0.05:
            probability_status = "🟠 Suspeito"
        else:
            probability_status = "🔴 Matar"

        # ==========================
        # NEW: Consumo do orçamento
        # ==========================

        if test_budget_limit > 0:
            budget_share = cost / test_budget_limit
        else:
            budget_share = 0

        if budget_share < 0.2:
            budget_status = "🟢 Baixo impacto"
        elif budget_share < 0.5:
            budget_status = "🟡 Relevante"
        elif budget_share < 0.8:
            budget_status = "🟠 Alto impacto"
        else:
            budget_status = "🔴 Estourando orçamento"

        result[intent] = {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "CTR": round(ctr * 100, 2),
            "CPC": round(cpc, 2),
            "CVR": round(cvr_real * 100, 2),
            "healthy_CPC": round(healthy_cpc, 2),
            "gap": round(gap, 2),
            "probability_no_conversion": round(probability_no_conversion * 100, 2),
            "probability_status": probability_status,
            "budget_share": round(budget_share * 100, 1),
            "budget_status": budget_status,
            "status": status
        }

    return result