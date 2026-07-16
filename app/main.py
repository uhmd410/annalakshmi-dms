from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app import models
from app.routers import annalakshmi, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Annalakshmi Data Management System")

app.include_router(annalakshmi.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Annalakshmi DMS is running"}