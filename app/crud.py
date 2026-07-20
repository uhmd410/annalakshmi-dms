from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
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

def get_all_annalakshmis(
    db: Session,
    name: str = None,
    mobile: str = None,
    area: str = None,
    status: str = None,
    food_type: str = None,
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(models.Annalakshmi)

    if name:
        query = query.filter(models.Annalakshmi.full_name.ilike(f"%{name}%"))
    if mobile:
        query = query.filter(models.Annalakshmi.mobile_number.ilike(f"%{mobile}%"))
    if area:
        query = query.filter(models.Annalakshmi.area.ilike(f"%{area}%"))
    if status:
        query = query.filter(models.Annalakshmi.status == status)
    if food_type:
        query = query.filter(models.Annalakshmi.veg_or_nonveg == food_type)

    total = query.count()
    items = (
        query.order_by(models.Annalakshmi.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total

def update_annalakshmi(db: Session, id: int, data: schemas.AnnalakshmiUpdate):
    record = get_annalakshmi(db, id)
    if not record:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # to make sure mobile number doesn't collide when changed
    if "mobile_number" in update_data:
        existing = (
            db.query(models.Annalakshmi)
            .filter(models.Annalakshmi.mobile_number == update_data["mobile_number"])
            .filter(models.Annalakshmi.id != id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Mobile number already registered")

    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record

def archive_annalakshmi(db: Session, id: int):
    record = get_annalakshmi(db, id)
    if not record:
        return None
    record.status = "inactive"
    db.commit()
    db.refresh(record)
    return record

def get_dashboard_summary(db: Session):
    total = db.query(models.Annalakshmi).count()
    active = db.query(models.Annalakshmi).filter(models.Annalakshmi.status == "active").count()
    inactive = db.query(models.Annalakshmi).filter(models.Annalakshmi.status == "inactive").count()
    return {"total": total, "active": active, "inactive": inactive}

