from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

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
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = crud.get_all_annalakshmis(db, name, mobile, area, status, page, page_size)
    total_pages = (total + page_size - 1) // page_size if total else 0
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": items,
    }

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

