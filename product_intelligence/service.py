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
    total_visitors = 0
    total_checkouts = 0
    total_cost = 0
    total_conversions = 0
    total_revenue = 0

    keywords_data = []

    # ==========================
    # COLETA DE DADOS
    # ==========================
    for campaign in product.campaigns or []:
        for keyword in campaign.keywords or []:

            logs = db.query(models.DailyLog).filter(
                models.DailyLog.keyword_id == keyword.id
            ).all()

            if not logs:
                continue

            impressions = sum((log.impressions or 0) for log in logs)
            clicks = sum((log.clicks or 0) for log in logs)
            visitors = sum((log.visitors or 0) for log in logs)
            checkouts = sum((log.checkouts or 0) for log in logs)
            cost = sum((log.cost or 0) for log in logs)
            conversions = sum((log.conversions or 0) for log in logs)
            revenue = sum((log.revenue or 0) for log in logs)

            total_impressions += impressions
            total_clicks += clicks
            total_visitors += visitors
            total_checkouts += checkouts
            total_cost += cost
            total_conversions += conversions
            total_revenue += revenue

            keywords_data.append({
                "cost": cost,
                "clicks": clicks,
                "visitors": visitors,
                "checkouts": checkouts,
                "conversions": conversions
            })

    # ==========================
    # SEM DADOS
    # ==========================
    if total_clicks == 0:
        return {
            "product": product.name,
            "status": "NO_DATA"
        }

    # ==========================
    # FUNIL
    # ==========================
    visit_rate = total_visitors / total_clicks if total_clicks > 0 else 0
    checkout_rate = total_checkouts / total_visitors if total_visitors > 0 else 0
    close_rate = total_conversions / total_checkouts if total_checkouts > 0 else 0

    cvr_real = visit_rate * checkout_rate * close_rate

    cpc_medio = total_cost / total_clicks if total_clicks > 0 else 0

    estimated_cvr = product.estimated_conversion_rate or 0
    commission = product.commission_value or 0

    conversion_base = cvr_real if total_conversions >= 5 else estimated_cvr

    healthy_cpc = commission * conversion_base
    gap_estrutural = healthy_cpc - cpc_medio

    margem_real_total = total_revenue - total_cost

    # ==========================
    # RISCO
    # ==========================
    custo_em_risco = 0

    for k in keywords_data:

        if k["clicks"] <= 0:
            continue

        cpc_k = k["cost"] / k["clicks"]

        visit_rate_k = k["visitors"] / k["clicks"] if k["clicks"] > 0 else 0
        checkout_rate_k = k["checkouts"] / k["visitors"] if k["visitors"] > 0 else 0
        close_rate_k = k["conversions"] / k["checkouts"] if k["checkouts"] > 0 else 0

        cvr_k = visit_rate_k * checkout_rate_k * close_rate_k

        base_k = cvr_k if k["conversions"] >= 5 else estimated_cvr

        healthy_k = commission * base_k

        if healthy_k > 0 and cpc_k > healthy_k:
            custo_em_risco += k["cost"]

    percentual_custo_em_risco = (
        (custo_em_risco / total_cost) * 100
        if total_cost > 0
        else 0
    )

    # ==========================
    # STATUS ESTRUTURAL
    # ==========================
    if healthy_cpc == 0:
        status = "⚪ Dados insuficientes"
    elif gap_estrutural < 0:
        status = "🔴 Estruturalmente Inviável"
    elif gap_estrutural < healthy_cpc * 0.2:
        status = "🟡 Estrutura Frágil"
    else:
        status = "🟢 Estruturalmente Saudável"

    # ==========================
    # TEST CONTROL
    # ==========================
    test_budget_limit = commission * 3

    test_progress = (
        (total_cost / test_budget_limit) * 100
        if test_budget_limit > 0
        else 0
    )

    if total_cost >= test_budget_limit and total_checkouts == 0:
        test_budget_status = "🔴 Kill Product (No Checkout)"
        recommendation = "STOP TEST"

    elif total_cost >= test_budget_limit and total_conversions == 0:
        test_budget_status = "🟠 Checkout Without Sales"
        recommendation = "Investigate Offer"

    else:
        test_budget_status = "🟢 Within Test Budget"
        recommendation = "Continue Testing"

    # ==========================
    # RESULTADO FINAL
    # ==========================
    return {

        "product": product.name,

        "visit_rate": round(visit_rate * 100, 2),
        "checkout_rate": round(checkout_rate * 100, 2),
        "close_rate": round(close_rate * 100, 2),

        "cpc_medio": round(cpc_medio, 2),
        "healthy_cpc_medio": round(healthy_cpc, 2),
        "gap_estrutural": round(gap_estrutural, 2),

        "status_estrutural": status,

        "receita_total": round(total_revenue, 2),
        "custo_total": round(total_cost, 2),
        "margem_real_total": round(margem_real_total, 2),

        "conversoes_totais": total_conversions,

        "percentual_custo_em_risco": round(percentual_custo_em_risco, 1),

        "test_budget_limit": round(test_budget_limit, 2),
        "test_budget_status": test_budget_status,
        "test_progress": round(test_progress, 1),
        "recommendation": recommendation
    }