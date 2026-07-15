from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app import models, schemas

def create_annalakshmi(db: Session, data: schemas.AnnalakshmiCreate):
    record = models.Annalakshmi(**data.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    db.refresh(record)
    return record

def get_annalakshmi(db: Session, id: int):
    return db.query(models.Annalakshmi).filter(models.Annalakshmi.id == id).first()

def get_all_annalakshmis(db: Session):
    return db.query(models.Annalakshmi).all()
