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
        # PRODUCTS (novo modelo CPC)
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
        # PROSPECTS (novo modelo CPA fixo)
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

        conn.execute(text("""
        ALTER TABLE prospects ADD COLUMN IF NOT EXISTS currency VARCHAR;
        """))

        # =========================
        # REMOVER OBRIGATORIEDADE ANTIGA (LEGADO)
        # =========================

        conn.execute(text("""
        ALTER TABLE prospects ALTER COLUMN niche DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ALTER COLUMN main_intent DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ALTER COLUMN avg_ticket DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ALTER COLUMN commission_percent DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE prospects ALTER COLUMN estimated_cpa DROP NOT NULL;
        """))
             
        # =========================
        # REMOVER NOT NULL LEGADO PRODUCTS
        # =========================

        conn.execute(text("""
        ALTER TABLE products ALTER COLUMN avg_ticket DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE products ALTER COLUMN commission DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE products ALTER COLUMN margin DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE products ALTER COLUMN max_cpa DROP NOT NULL;
        """))

        conn.execute(text("""
        ALTER TABLE products ALTER COLUMN min_roas DROP NOT NULL;
        """))

        conn.commit()