def calculate_kpis(logs, product):
    impressions = sum(log.impressions for log in logs)
    clicks = sum(log.clicks for log in logs)
    cost = sum(log.cost for log in logs)
    conversions = sum(log.conversions for log in logs)
    revenue = sum(log.revenue for log in logs)

    ctr = clicks / impressions if impressions > 0 else 0
    cpc = cost / clicks if clicks > 0 else 0
    cvr_real = conversions / clicks if clicks > 0 else 0

    # 🔥 Modelo oficial Máquina de Guerra (100% CPC-based)
    estimated_cvr = product.estimated_conversion_rate or 0

    conversion_base = (
        cvr_real if conversions >= 5
        else estimated_cvr
    )

    healthy_cpc = product.commission_value * conversion_base
    gap = healthy_cpc - cpc
    margem_real = revenue - cost

    if cpc > healthy_cpc:
        status = "🔴 CPC Acima do Viável"
    elif cpc > healthy_cpc * 0.8:
        status = "🟡 Zona de Atenção"
    else:
        status = "🟢 Operando Saudável"

    return {
        "impressions": impressions,
        "clicks": clicks,
        "cost": round(cost, 2),
        "conversions": conversions,
        "revenue": round(revenue, 2),
        "CTR": round(ctr, 4),
        "CPC": round(cpc, 2),
        "CVR_real": round(cvr_real, 4),
        "conversion_base": round(conversion_base, 4),
        "healthy_CPC": round(healthy_cpc, 2),
        "gap": round(gap, 2),
        "margem_real": round(margem_real, 2),
        "status": status
    }