from prospecting import models as prospect_models
from fastapi import FastAPI
from db import engine, Base
from core.routes import router
from prospecting.routes import router as prospect_router
app.include_router(prospect_router)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)