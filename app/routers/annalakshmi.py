from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from datetime import date
import csv
import io

router = APIRouter(prefix="/annalakshmis", tags=["Annalakshmis"])

@router.post("/", response_model=schemas.AnnalakshmiResponse)
def create(data: schemas.AnnalakshmiCreate, db: Session = Depends(get_db)):
    return crud.create_annalakshmi(db, data)

@router.get("/", response_model=schemas.PaginatedAnnalakshmiResponse)
def list_all(
    name: str = None,
    mobile: str = None,
    area: str = None,
    status: str = None,
    food_type: str = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = crud.get_all_annalakshmis(db, name, mobile, area, status, food_type, page, page_size)
    total_pages = (total + page_size - 1) // page_size if total else 0
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": items,
    }

CSV_COLUMNS = [
    "id", "full_name", "mobile_number", "email", "address", "area", "city",
    "state", "pin_code", "cuisine_specialization", "veg_or_nonveg",
    "signature_dishes", "available_timings", "max_orders_per_day",
    "date_joined", "status", "created_at", "updated_at",
]

@router.get("/export")
def export_csv(
    name: str = None,
    mobile: str = None,
    area: str = None,
    status: str = None,
    food_type: str = None,
    db: Session = Depends(get_db),
):
    records = crud.get_all_annalakshmis_for_export(db, name, mobile, area, status, food_type)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_COLUMNS)

    for r in records:
        writer.writerow([
            r.id, r.full_name, r.mobile_number, r.email or "", r.address,
            r.area, r.city, r.state, r.pin_code, r.cuisine_specialization,
            r.veg_or_nonveg, r.signature_dishes or "", r.available_timings or "",
            r.max_orders_per_day, r.date_joined, r.status,
            r.created_at, r.updated_at,
        ])

    buffer.seek(0)
    filename = f"annalakshmis_export_{date.today().isoformat()}.csv"

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

@router.get("/{id}", response_model=schemas.AnnalakshmiResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    record = crud.get_annalakshmi(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Annalakshmi not found")
    return record

@router.put("/{id}", response_model=schemas.AnnalakshmiResponse)
def update(id: int, data: schemas.AnnalakshmiUpdate, db: Session = Depends(get_db)):
    record = crud.update_annalakshmi(db, id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Annalakshmi not found")
    return record

@router.patch("/{id}/archive", response_model=schemas.AnnalakshmiResponse)
def archive(id: int, db: Session = Depends(get_db)):
    record = crud.archive_annalakshmi(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Annalakshmi not found")
    return record

