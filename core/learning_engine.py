from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.models import DailyLog


class LearningEngine:

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # GLOBAL BENCHMARKS
    # =========================

    def global_benchmarks(self):

        totals = self.db.query(
            func.coalesce(func.sum(DailyLog.impressions), 0),
            func.coalesce(func.sum(DailyLog.clicks), 0),
            func.coalesce(func.sum(DailyLog.conversions), 0),
            func.coalesce(func.sum(DailyLog.cost), 0)
        ).first()

        impressions, clicks, conversions, cost = totals

        ctr = clicks / impressions if impressions > 0 else 0
        cvr = conversions / clicks if clicks > 0 else 0
        cpc = cost / clicks if clicks > 0 else 0
        clicks_per_sale = clicks / conversions if conversions > 0 else 0

        return {
            "ctr_global": round(ctr, 4),
            "cvr_global": round(cvr, 4),
            "cpc_global": round(cpc, 2),
            "clicks_per_sale": round(clicks_per_sale, 2)
        }

    # =========================
    # LAST 30 DAYS BENCHMARKS
    # =========================

    def last_30d_benchmarks(self):

        cutoff = datetime.utcnow().date() - timedelta(days=30)

        totals = self.db.query(
            func.coalesce(func.sum(DailyLog.impressions), 0),
            func.coalesce(func.sum(DailyLog.clicks), 0),
            func.coalesce(func.sum(DailyLog.conversions), 0),
            func.coalesce(func.sum(DailyLog.cost), 0)
        ).filter(
            DailyLog.date >= cutoff
        ).first()

        impressions, clicks, conversions, cost = totals

        ctr = clicks / impressions if impressions > 0 else 0
        cvr = conversions / clicks if clicks > 0 else 0
        cpc = cost / clicks if clicks > 0 else 0

        return {
            "ctr_30d": round(ctr, 4),
            "cvr_30d": round(cvr, 4),
            "cpc_30d": round(cpc, 2)
        }

    # =========================
    # HEALTHY CPC
    # =========================

    def healthy_cpc(self, commission: float, cvr: float):
        if not commission or not cvr:
            return 0
        return round(commission * cvr, 2)