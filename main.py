from fastapi import FastAPI
from db import engine, Base
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "AFF-OS online"}