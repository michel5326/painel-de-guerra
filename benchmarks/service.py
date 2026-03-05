from sqlalchemy.orm import Session
from core.learning_engine import LearningEngine
from core import models


def build_account_benchmarks(product_id: int, db: Session):

    engine = LearningEngine(db)

    global_data = engine.global_benchmarks()
    last_30d = engine.last_30d_benchmarks()

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {
            **global_data,
            **last_30d,
            "healthy_cpc": 0,
            "baseline_cvr": 0,
            "message": "Produto não encontrado"
        }

    commission = product.commission_value or 0
    estimated_cvr = product.estimated_conversion_rate or 0
    baseline_cvr = product.baseline_conversion_rate or 0.01

    total_clicks = global_data.get("clicks_global", 0)
    total_conversions = global_data.get("conversions_global", 0)

    cvr_global = global_data.get("cvr_global", 0)

    # Regra de proteção estatística
    if total_conversions >= 5:
        cvr_base = cvr_global
    else:
        cvr_base = estimated_cvr

    healthy_cpc = commission * cvr_base

    # Probabilidade de ainda não ter conversão baseada no baseline
    if total_clicks > 0:
        probability_no_conversion = (1 - baseline_cvr) ** total_clicks
    else:
        probability_no_conversion = 1

    return {
        **global_data,
        **last_30d,
        "healthy_cpc": round(healthy_cpc, 2),
        "cvr_base_used": round(cvr_base, 4),
        "baseline_cvr": round(baseline_cvr, 4),
        "probability_no_conversion": round(probability_no_conversion * 100, 2)
    }