from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app import models
from app.routers import annalakshmi, dashboard, pages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Annalakshmi Data Management System")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(loc) for loc in err["loc"] if loc != "body"), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Validation failed", "details": errors},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error"},
    )

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(annalakshmi.router)
app.include_router(dashboard.router)
app.include_router(pages.router)

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/pages/dashboard", status_code=302)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Annalakshmi DMS is running"}