from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base

# IMPORTANTE: garantir que todos os models sejam carregados
from core import models as core_models
from prospecting import models as prospect_models

from core.routes import router as core_router
from prospecting.routes import router as prospect_router

app = FastAPI(
    title="Máquina de Guerra API",
    version="1.0.0"
)

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir ao domínio do front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE INIT
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# ROUTERS
# =========================
app.include_router(core_router)
app.include_router(prospect_router)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "Máquina de Guerra online"}