def calculate_kpis(logs, product):
    impressions = sum(log.impressions for log in logs)
    clicks = sum(log.clicks for log in logs)
    cost = sum(log.cost for log in logs)
    conversions = sum(log.conversions for log in logs)
    revenue = sum(log.revenue for log in logs)

    ctr = clicks / impressions if impressions > 0 else 0
    cpc = cost / clicks if clicks > 0 else 0
    cvr = conversions / clicks if clicks > 0 else 0
    cpa = cost / conversions if conversions > 0 else 0
    roas = revenue / cost if cost > 0 else 0

    break_even_cpc = product.max_cpa * cvr if cvr > 0 else 0
    margem_real = revenue - cost
    conversoes_minimas = cost / product.max_cpa if product.max_cpa > 0 else 0

    if conversions == 0 and cost > product.max_cpa:
        status = "🔴 Inviável"
    elif roas >= product.min_roas:
        status = "🟢 Saudável"
    elif roas < product.min_roas:
        status = "🟡 Sob pressão"
    else:
        status = "⚪ Dados insuficientes"

    return {
        "impressions": impressions,
        "clicks": clicks,
        "cost": cost,
        "conversions": conversions,
        "revenue": revenue,
        "CTR": round(ctr, 4),
        "CPC": round(cpc, 2),
        "CVR": round(cvr, 4),
        "CPA": round(cpa, 2),
        "ROAS": round(roas, 2),
        "break_even_CPC": round(break_even_cpc, 2),
        "margem_real": round(margem_real, 2),
        "conversoes_minimas_para_empate": round(conversoes_minimas, 2),
        "status": status
    }