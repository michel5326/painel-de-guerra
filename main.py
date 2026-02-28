from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base

from core.routes import router as core_router
from prospecting.routes import router as prospect_router
from prospecting import models as prospect_models  # garante registro dos models

app = FastAPI()

# 🔥 CORS CONFIG (resolve erro 405 OPTIONS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cria tabelas
Base.metadata.create_all(bind=engine)

# registra rotas
app.include_router(core_router)
app.include_router(prospect_router)