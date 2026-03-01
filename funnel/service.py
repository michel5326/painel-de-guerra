from sqlalchemy.orm import Session
from core import models
from core.learning_engine import LearningEngine


def build_keyword_funnel(keyword_id: int, db: Session):

    logs = db.query(models.DailyLog).filter(
        models.DailyLog.keyword_id == keyword_id
    ).all()

    # =========================
    # SEM DADOS → estrutura padrão
    # =========================
    if not logs:
        return {
            "funnel": {
                "impressions": 0,
                "clicks": 0,
                "visitors": 0,
                "checkouts": 0,
                "sales": 0,
                "upsells": 0
            },
            "rates": {
                "ctr": 0,
                "visit_rate": 0,
                "checkout_rate": 0,
                "sales_rate": 0,
                "upsell_rate": 0
            },
            "suggestions": []
        }

    # =========================
    # AGREGAÇÃO
    # =========================
    impressions = sum(log.impressions or 0 for log in logs)
    clicks = sum(log.clicks or 0 for log in logs)
    visitors = sum(log.visitors or 0 for log in logs)
    checkouts = sum(log.checkouts or 0 for log in logs)
    sales = sum(log.conversions or 0 for log in logs)
    upsells = sum(log.upsells or 0 for log in logs)

    # =========================
    # TAXAS (PROTEÇÃO DIV ZERO)
    # =========================
    ctr = clicks / impressions if impressions > 0 else 0
    visit_rate = visitors / clicks if clicks > 0 else 0
    checkout_rate = checkouts / visitors if visitors > 0 else 0
    sales_rate = sales / checkouts if checkouts > 0 else 0
    upsell_rate = upsells / sales if sales > 0 else 0

    # =========================
    # BENCHMARK SEGURO
    # =========================
    try:
        engine = LearningEngine(db)
        global_data = engine.global_benchmarks() or {}
        ctr_global = global_data.get("ctr_global", 0)
    except Exception:
        ctr_global = 0

    # =========================
    # DESVIO
    # =========================
    def deviation(current, benchmark):
        if benchmark == 0:
            return "NO_DATA"
        diff = (current - benchmark) / benchmark
        if abs(diff) < 0.10:
            return "NORMAL"
        elif abs(diff) < 0.25:
            return "ALERTA"
        else:
            return "DESVIO_GRAVE"

    suggestions = []

    if deviation(ctr, ctr_global) == "DESVIO_GRAVE":
        suggestions.append("CTR muito abaixo do padrão histórico.")

    if checkout_rate < 0.2 and visitors > 50:
        suggestions.append("Baixa progressão visitante → checkout.")

    if sales == 0 and clicks > 100:
        suggestions.append("Volume suficiente para já ter convertido.")

    # =========================
    # RETORNO PADRÃO
    # =========================
    return {
        "funnel": {
            "impressions": impressions,
            "clicks": clicks,
            "visitors": visitors,
            "checkouts": checkouts,
            "sales": sales,
            "upsells": upsells
        },
        "rates": {
            "ctr": round(ctr, 4),
            "visit_rate": round(visit_rate, 4),
            "checkout_rate": round(checkout_rate, 4),
            "sales_rate": round(sales_rate, 4),
            "upsell_rate": round(upsell_rate, 4)
        },
        "suggestions": suggestions
    }