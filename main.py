from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from db import engine, Base

# =========================
# IMPORT MODELS (garante registro no SQLAlchemy)
# =========================
from core.migration import run_migration
from core import models as core_models
from prospecting import models as prospect_models

# =========================
# IMPORT ROUTERS
# =========================
from core.routes import router as core_router
from prospecting.routes import router as prospect_router
from funnel.routes import router as funnel_router
from benchmarks.routes import router as benchmarks_router
from core.products_routes import router as products_router
from core.campaigns_routes import router as campaigns_router
from core.keywords_routes import router as keywords_router
from core.logs_routes import router as logs_router
from core.dashboard_routes import router as dashboard_router
from intent.routes import router as intent_router
from product_intelligence.routes import router as product_intelligence_router
from campaign_generator.routes import router as campaign_generator_router


# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="Máquina de Guerra API",
    description="Sistema de inteligência operacional para afiliados em Google Ads",
    version="1.0.0"
)


# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # liberar para frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DATABASE INIT
# =========================
Base.metadata.create_all(bind=engine)

# executa migrações customizadas
run_migration()


# =========================
# DATABASE AUTO FIX
# =========================
# Evita erro caso coluna ainda não exista
with engine.connect() as conn:

    conn.execute(text("""
        ALTER TABLE products
        ADD COLUMN IF NOT EXISTS baseline_conversion_rate FLOAT DEFAULT 0.01
    """))

    conn.commit()


# =========================
# ROUTERS
# =========================
app.include_router(core_router)
app.include_router(prospect_router)
app.include_router(funnel_router)
app.include_router(benchmarks_router)
app.include_router(products_router)
app.include_router(campaigns_router)
app.include_router(keywords_router)
app.include_router(logs_router)
app.include_router(dashboard_router)
app.include_router(intent_router)
app.include_router(product_intelligence_router)
app.include_router(campaign_generator_router)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "online",
        "system": "Máquina de Guerra",
        "version": "1.0.0"
    }


# =========================
# API STATUS
# =========================
@app.get("/health")
def health():
    return {
        "api": "ok",
        "database": "connected"
    }