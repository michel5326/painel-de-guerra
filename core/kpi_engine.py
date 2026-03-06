def calculate_kpis(logs, product):

    # ==========================
    # AGREGAÇÃO DOS LOGS
    # ==========================

    impressions = sum((log.impressions or 0) for log in logs)
    clicks = sum((log.clicks or 0) for log in logs)
    cost = sum((log.cost or 0) for log in logs)
    conversions = sum((log.conversions or 0) for log in logs)
    revenue = sum((log.revenue or 0) for log in logs)

    # ==========================
    # MÉTRICAS BÁSICAS
    # ==========================

    ctr = clicks / impressions if impressions > 0 else 0
    cpc = cost / clicks if clicks > 0 else 0
    cvr_real = conversions / clicks if clicks > 0 else 0

    # ==========================
    # MODELO BASE DE CONVERSÃO
    # ==========================

    estimated_cvr = product.estimated_conversion_rate or 0
    baseline_cvr = product.baseline_conversion_rate or 0.01
    commission = product.commission_value or 0

    # Se já houver dados suficientes, usar CVR real
    conversion_base = cvr_real if conversions >= 5 else estimated_cvr

    # ==========================
    # ECONOMIA DO CLIQUE
    # ==========================

    healthy_cpc = commission * conversion_base
    gap = healthy_cpc - cpc
    margem_real = revenue - cost

    # ==========================
    # PROBABILIDADE DE NÃO CONVERSÃO
    # ==========================

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
    # STATUS OPERACIONAL
    # ==========================

    if healthy_cpc == 0:
        status = "⚪ Sem dados suficientes"
    elif cpc > healthy_cpc:
        status = "🔴 CPC Acima do Viável"
    elif cpc > healthy_cpc * 0.8:
        status = "🟡 Zona de Atenção"
    else:
        status = "🟢 Operando Saudável"

    # ==========================
    # SCORE OPERACIONAL (0–100)
    # ==========================

    # Viabilidade econômica
    if gap > 0:
        viability_score = min(gap * 10, 50)
    else:
        viability_score = max(50 + (gap * 20), 0)

    # Eficiência de conversão
    if estimated_cvr > 0:
        efficiency_ratio = cvr_real / estimated_cvr
        efficiency_score = min(efficiency_ratio * 30, 30)
    else:
        efficiency_score = 0

    # Volume de dados
    volume_score = min(clicks / 10, 20)

    operational_score = round(
        min(viability_score + efficiency_score + volume_score, 100),
        1
    )

    # ==========================
    # RETORNO FINAL
    # ==========================

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

        "probability_no_conversion": round(probability_no_conversion * 100, 2),
        "probability_status": probability_status,

        "status": status,

        "operational_score": operational_score
    }