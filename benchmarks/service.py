from sqlalchemy.orm import Session
from core.learning_engine import LearningEngine
from core import models


def build_account_benchmarks(product_id: int, db: Session):

    engine = LearningEngine(db)

    global_data = engine.global_benchmarks()
    last_30d = engine.last_30d_benchmarks()

    # ==========================
    # GLOBAL MODE (ALL PRODUCTS)
    # ==========================
    if product_id == 0:

        total_clicks = global_data.get("clicks_global", 0)
        total_cost = global_data.get("cost_global", 0)

        cpc_global = total_cost / total_clicks if total_clicks > 0 else 0

        return {
            **global_data,
            **last_30d,
            "healthy_cpc": round(cpc_global, 2),
            "mode": "account"
        }

    # ==========================
    # PRODUCT MODE
    # ==========================

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {
            **global_data,
            **last_30d,
            "healthy_cpc": 0,
            "message": "Produto não encontrado"
        }

    commission = product.commission_value or 0
    estimated_cvr = product.estimated_conversion_rate or 0

    total_conversions = global_data.get("conversions_global", 0)
    cvr_global = global_data.get("cvr_global", 0)

    # Regra de proteção estatística
    if total_conversions >= 5:
        cvr_base = cvr_global
    else:
        cvr_base = estimated_cvr

    healthy_cpc = commission * cvr_base

    return {
        **global_data,
        **last_30d,
        "healthy_cpc": round(healthy_cpc, 2),
        "cvr_base_used": round(cvr_base, 4),
        "estimated_cvr": round(estimated_cvr, 4),
        "mode": "product"
    }