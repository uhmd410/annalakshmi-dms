from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/pages", tags=["Pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@router.get("/records")
def records_page(request: Request):
    return templates.TemplateResponse(request=request, name="view_records.html")


@router.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(request=request, name="add_annalakshmi.html")


@router.get("/edit/{record_id}")
def edit_page(request: Request, record_id: int):
    return templates.TemplateResponse(
        request=request, name="edit_annalakshmi.html", context={"record_id": record_id}
    )


@router.get("/profile/{record_id}")
def profile_page(request: Request, record_id: int):
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"record_id": record_id}
    )
