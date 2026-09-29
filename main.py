from fastapi import FastAPI

import models  # makes sure the Note model is loaded before creating tables
from database import Base, engine
from routers import notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")

app.include_router(notes.router)