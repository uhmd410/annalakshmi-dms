from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Annalakshmi Data Management System")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Annalakshmi DMS is running"}