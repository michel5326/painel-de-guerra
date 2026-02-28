from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.models import DailyLog, Keyword


class LearningEngine:

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # GLOBAL BENCHMARKS
    # =========================

    def global_benchmarks(self):

        totals = self.db.query(
            func.sum(DailyLog.impressions),
            func.sum(DailyLog.clicks),
            func.sum(DailyLog.conversions),
            func.sum(DailyLog.cost)
        ).one()

        impressions = totals[0] or 0
        clicks = totals[1] or 0
        conversions = totals[2] or 0
        cost = totals[3] or 0

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
            func.sum(DailyLog.impressions),
            func.sum(DailyLog.clicks),
            func.sum(DailyLog.conversions),
            func.sum(DailyLog.cost)
        ).filter(
            DailyLog.date >= cutoff
        ).one()

        impressions = totals[0] or 0
        clicks = totals[1] or 0
        conversions = totals[2] or 0
        cost = totals[3] or 0

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
        return round(commission * cvr, 2)