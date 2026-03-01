from sqlalchemy import text
from db import engine


def run_migration():
    with engine.connect() as conn:

        # =========================
        # DAILY LOGS
        # =========================

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

        # =========================
        # PRODUCTS
        # =========================

        conn.execute(text("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS commission_value DOUBLE PRECISION;
        """))

        conn.execute(text("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS estimated_conversion_rate DOUBLE PRECISION;
        """))

        # =========================
        # PROSPECTS
        # =========================

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS platform VARCHAR;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS search_volume_last_month INTEGER;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS commission_value DOUBLE PRECISION;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS top_bid_low DOUBLE PRECISION;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS top_bid_high DOUBLE PRECISION;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS temperature_ranking VARCHAR;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS observations TEXT;
        """))

        conn.commit()