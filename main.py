from fastapi import FastAPI
from db import engine, Base

from core.routes import router as core_router
from prospecting.routes import router as prospect_router
from prospecting import models as prospect_models

app = FastAPI()

# 🔥 DROP apenas prospects (força recriação correta)
prospect_models.Prospect.__table__.drop(engine, checkfirst=True)

# recria todas
Base.metadata.create_all(bind=engine)

app.include_router(core_router)
app.include_router(prospect_router)