from sqlalchemy.orm import Session
from core import models


def build_strategic_dashboard(product_id: int, db: Session):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return None

    total_impressions = 0
    total_clicks = 0
    total_cost = 0
    total_conversions = 0
    total_revenue = 0

    keywords_data = []

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
            revenue = sum(log.revenue for log in logs)

            total_impressions += impressions
            total_clicks += clicks
            total_cost += cost
            total_conversions += conversions
            total_revenue += revenue

            keywords_data.append({
                "cost": cost,
                "clicks": clicks,
                "conversions": conversions
            })

    if total_clicks == 0:
        return {
            "product": product.name,
            "status": "NO_DATA"
        }

    # ===== Estrutura Macro =====

    cpc_medio = total_cost / total_clicks
    cvr_real = total_conversions / total_clicks if total_clicks > 0 else 0

    estimated_cvr = product.estimated_conversion_rate or 0

    conversion_base = (
        cvr_real if total_conversions >= 5
        else estimated_cvr
    )

    healthy_cpc = product.commission_value * conversion_base
    gap_estrutural = healthy_cpc - cpc_medio

    margem_real_total = total_revenue - total_cost

    # ===== Distribuição de Risco =====

    custo_em_risco = 0

    for k in keywords_data:
        if k["clicks"] > 0:

            cpc_k = k["cost"] / k["clicks"]
            cvr_k = k["conversions"] / k["clicks"] if k["clicks"] > 0 else 0

            base_k = (
                cvr_k if k["conversions"] >= 5
                else estimated_cvr
            )

            healthy_k = product.commission_value * base_k

            if cpc_k > healthy_k:
                custo_em_risco += k["cost"]

    percentual_custo_em_risco = (
        (custo_em_risco / total_cost) * 100
        if total_cost > 0
        else 0
    )

    # ===== Status Estrutural =====

    if gap_estrutural < 0:
        status = "🔴 Estruturalmente Inviável"
    elif gap_estrutural < healthy_cpc * 0.2:
        status = "🟡 Estrutura Frágil"
    else:
        status = "🟢 Estruturalmente Saudável"

    # ==================================
    # TEST BUDGET CONTROL
    # ==================================

    commission = product.commission_value or 0
    test_budget_limit = commission * 3

    # progresso do teste
    test_progress = (
        (total_cost / test_budget_limit) * 100
        if test_budget_limit > 0
        else 0
    )

    if total_cost >= test_budget_limit and total_conversions == 0:
        test_budget_status = "🔴 Kill Product (Budget Exceeded)"
        recommendation = "STOP TEST"
    elif total_cost >= commission * 2 and total_conversions == 0:
        test_budget_status = "🟠 High Risk"
        recommendation = "Monitor Closely"
    else:
        test_budget_status = "🟢 Within Test Budget"
        recommendation = "Continue Testing"

    return {
        "product": product.name,
        "cpc_medio": round(cpc_medio, 2),
        "healthy_cpc_medio": round(healthy_cpc, 2),
        "gap_estrutural": round(gap_estrutural, 2),
        "status_estrutural": status,
        "receita_total": round(total_revenue, 2),
        "custo_total": round(total_cost, 2),
        "margem_real_total": round(margem_real_total, 2),
        "conversoes_totais": total_conversions,
        "percentual_custo_em_risco": round(percentual_custo_em_risco, 1),

        # TEST MONITOR
        "test_budget_limit": round(test_budget_limit, 2),
        "test_budget_status": test_budget_status,
        "test_progress": round(test_progress, 1),
        "recommendation": recommendation
    }