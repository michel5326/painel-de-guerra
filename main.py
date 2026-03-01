from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base

# IMPORTANTE: garantir que todos os models sejam carregados
from core.migration import run_migration
from core import models as core_models
from prospecting import models as prospect_models

from core.routes import router as core_router
from prospecting.routes import router as prospect_router
from funnel.routes import router as funnel_router
from benchmarks.routes import router as benchmarks_router
from core.products_routes import router as products_router
from core.campaigns_routes import router as campaigns_router
from core.keywords_routes import router as keywords_router
from core.logs_routes import router as logs_router
from core.dashboard_routes import router as dashboard_router

app = FastAPI(
    title="Máquina de Guerra API",
    version="1.0.0"
)

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE INIT
# =========================
Base.metadata.create_all(bind=engine)
run_migration()

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

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "Máquina de Guerra online"}