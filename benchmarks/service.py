from sqlalchemy.orm import Session
from core.learning_engine import LearningEngine
from core import models


def build_account_benchmarks(db: Session):

    engine = LearningEngine(db)

    global_data = engine.global_benchmarks()
    last_30d = engine.last_30d_benchmarks()

    product = db.query(models.Product).first()

    healthy_cpc = 0
    if product:
        healthy_cpc = engine.healthy_cpc(
            product.commission,
            global_data["cvr_global"]
        )

    return {
        **global_data,
        **last_30d,
        "healthy_cpc": healthy_cpc
    }