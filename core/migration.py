from sqlalchemy import text
from db import engine


def run_migration():
    with engine.connect() as conn:

        conn.execute(text("""
        ALTER TABLE daily_logs
        ADD COLUMN IF NOT EXISTS visitors INTEGER DEFAULT 0;
        """))

        conn.execute(text("""
        ALTER TABLE daily_logs
        ADD COLUMN IF NOT EXISTS checkouts INTEGER DEFAULT 0;
        """))

        conn.execute(text("""
        ALTER TABLE daily_logs
        ADD COLUMN IF NOT EXISTS upsells INTEGER DEFAULT 0;
        """))

        conn.execute(text("""
        ALTER TABLE daily_logs
        ADD COLUMN IF NOT EXISTS bounce_rate DOUBLE PRECISION;
        """))

        conn.commit()

                # =========================
        # PRODUCT UPDATE
        # =========================

        conn.execute(text("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS commission_value DOUBLE PRECISION;
        """))

        conn.execute(text("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS estimated_conversion_rate DOUBLE PRECISION;
        """))