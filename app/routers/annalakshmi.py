from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/annalakshmis", tags=["Annalakshmis"])

@router.post("/", response_model=schemas.AnnalakshmiResponse)
def create(data: schemas.AnnalakshmiCreate, db: Session = Depends(get_db)):
    return crud.create_annalakshmi(db, data)

@router.get("/", response_model=list[schemas.AnnalakshmiResponse])
def list_all(
    name: str = None,
    mobile: str = None,
    area: str = None,
    status: str = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_annalakshmis(db, name, mobile, area, status)

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

