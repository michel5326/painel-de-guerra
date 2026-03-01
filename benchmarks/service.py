from sqlalchemy.orm import Session
from core.learning_engine import LearningEngine
from core import models


def build_account_benchmarks(db: Session):

    engine = LearningEngine(db)

    global_data = engine.global_benchmarks()
    last_30d = engine.last_30d_benchmarks()

    product = db.query(models.Product).first()

    if not product:
        return {
            **global_data,
            **last_30d,
            "healthy_cpc": 0,
            "message": "Nenhum produto cadastrado"
        }

    commission = product.commission_value or 0
    estimated_cvr = product.estimated_conversion_rate or 0

    cvr_global = global_data.get("cvr_global", 0)

    # 🔥 Regra oficial Máquina de Guerra
    cvr_base = cvr_global if cvr_global > 0 else estimated_cvr

    healthy_cpc = commission * cvr_base

    return {
        **global_data,
        **last_30d,
        "healthy_cpc": round(healthy_cpc, 2),
        "cvr_base_used": round(cvr_base, 4)
    }