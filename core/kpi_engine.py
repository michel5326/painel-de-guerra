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

    # ==========================
    # STATUS OPERACIONAL
    # ==========================
    if cpc > healthy_cpc:
        status = "🔴 CPC Acima do Viável"
    elif cpc > healthy_cpc * 0.8:
        status = "🟡 Zona de Atenção"
    else:
        status = "🟢 Operando Saudável"

    # ==========================
    # SCORE OPERACIONAL (0–100)
    # ==========================

    # 1️⃣ Viabilidade (0–50)
    if gap > 0:
        viability_score = min(gap * 10, 50)
    else:
        viability_score = max(50 + (gap * 20), 0)

    # 2️⃣ Eficiência (0–30)
    if estimated_cvr > 0:
        efficiency_ratio = cvr_real / estimated_cvr
        efficiency_score = min(efficiency_ratio * 30, 30)
    else:
        efficiency_score = 0

    # 3️⃣ Volume (0–20)
    volume_score = min(clicks / 10, 20)

    operational_score = round(
        min(viability_score + efficiency_score + volume_score, 100),
        1
    )

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
        "status": status,
        "operational_score": operational_score
    }