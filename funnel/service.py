from sqlalchemy.orm import Session
from core import models
from core.learning_engine import LearningEngine


def build_keyword_funnel(keyword_id: int, db: Session):

    logs = db.query(models.DailyLog).filter(
        models.DailyLog.keyword_id == keyword_id
    ).all()

    if not logs:
        return None

    impressions = sum(log.impressions for log in logs)
    clicks = sum(log.clicks for log in logs)
    visitors = sum(log.visitors for log in logs)
    checkouts = sum(log.checkouts for log in logs)
    sales = sum(log.conversions for log in logs)
    upsells = sum(log.upsells for log in logs)

    ctr = clicks / impressions if impressions > 0 else 0
    visit_rate = visitors / clicks if clicks > 0 else 0
    checkout_rate = checkouts / visitors if visitors > 0 else 0
    sales_rate = sales / checkouts if checkouts > 0 else 0
    upsell_rate = upsells / sales if sales > 0 else 0

    engine = LearningEngine(db)
    global_data = engine.global_benchmarks()

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

    if deviation(ctr, global_data["ctr_global"]) == "DESVIO_GRAVE":
        suggestions.append("CTR muito abaixo do padrão histórico.")

    if checkout_rate < 0.2 and visitors > 50:
        suggestions.append("Baixa progressão visitante → checkout.")

    if sales == 0 and clicks > 100:
        suggestions.append("Volume suficiente para já ter convertido.")

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