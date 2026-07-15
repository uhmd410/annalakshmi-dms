from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/annalakshmis", tags=["Annalakshmis"])

@router.post("/", response_model=schemas.AnnalakshmiResponse)
def create(data: schemas.AnnalakshmiCreate, db: Session = Depends(get_db)):
    return crud.create_annalakshmi(db, data)

@router.get("/", response_model=list[schemas.AnnalakshmiResponse])
def list_all(db: Session = Depends(get_db)):
    return crud.get_all_annalakshmis(db)

@router.get("/{id}", response_model=schemas.AnnalakshmiResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    record = crud.get_annalakshmi(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="Annalakshmi not found")
    return record
